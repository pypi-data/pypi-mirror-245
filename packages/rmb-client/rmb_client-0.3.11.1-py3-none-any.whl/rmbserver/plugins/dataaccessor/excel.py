import pandas as pd
import os
import sqlite3
import requests
from io import BytesIO
import tempfile
import time
import hashlib
from apscheduler.schedulers.background import BackgroundScheduler

from rmbserver.plugins.dataaccessor.da_base import BaseDataAccessor
from rmbserver.plugins.dataaccessor.da_register import register_data_accessor
from rmbserver.log import log
from rmbcommon.models import MetaData, DataSchema, DataTable, DataField
from rmbserver.plugins.model.excel import ExcelQuery, ExcelQueryResult
from rmbserver import config
from rmbserver.exceptions import DataSourceConfigError


@register_data_accessor
class ExcelDataAccessor(BaseDataAccessor):
    __source_type__ = "Excel"

    # location_type: local, http
    # location_url: local file path or http(s) url
    __access_config_keys_must__ = ['location_type', 'location_url']

    PROMPT_GEN_STRUC_QUERY = """这是一个Excel文件，将会被导入到一个SQLite数据库中，每个sheet对应一个表。
请根据要求提供可以直接执行的SQL语句。"""

    # 创建临时目录
    TEMP_DIR = tempfile.mkdtemp()
    # 设置过期时间（例如5分钟）
    EXPIRATION_TIME = 300  # 300秒

    # 缓存sqlite连接
    _cached_sqlite_conns = {}

    def _get_file_name(self):
        location_type = self.ds_access_config.get('location_type')
        location_url = self.ds_access_config.get('location_url')

        if location_type == 'local':
            file_name, file_ext = os.path.basename(location_url).split('.')
        elif location_type == 'http':
            file_name, file_ext = location_url.split('/')[-1].split('.')
        else:
            raise ValueError('location_type must be local or http')

        # 对URL应用哈希函数
        url_hash_object = hashlib.sha256(location_url.encode())
        hashed_url = url_hash_object.hexdigest()

        # 创建一个基于哈希值的唯一文件名
        unique_filename = f"{hashed_url}.{file_ext}"
        return file_name, file_ext, unique_filename

    def _read_excel(self):
        location_type = self.ds_access_config.get('location_type')
        location_url = self.ds_access_config.get('location_url')
        max_file_size = config.rmb_max_exec_file_size

        if location_type == 'local':
            # 检查文件大小
            file_size = os.path.getsize(location_url)
            if file_size > max_file_size:
                raise DataSourceConfigError(f"The file size exceeds the limit of {max_file_size} bytes.")
            excel_data = pd.read_excel(location_url, sheet_name=None)

        elif location_type == 'http':
            # 先发送HEAD请求以获取文件大小
            response = requests.head(location_url)
            content_length = int(response.headers.get('content-length', 0))
            if content_length > max_file_size:
                raise DataSourceConfigError(f"The file size exceeds the limit of {max_file_size} bytes.")

            # 然后发送GET请求以获取数据
            response = requests.get(location_url)
            response.raise_for_status()  # 确保请求成功
            excel_data = pd.read_excel(BytesIO(response.content), sheet_name=None)

        else:
            raise ValueError('location_type must be local or http')

        return excel_data

    def retrieve_meta_data(self) -> MetaData:
        excel_data = self._read_excel()

        file_name, _, _ = self._get_file_name()
        # Create MetaData object
        metadata_object = MetaData(name=f"Excel_{file_name}")

        # Create 1 DataSchema for whole excel file
        data_schema = DataSchema(
            name=file_name,
            metadata=metadata_object,
            origin_desc=""
        )

        for sheet_name, sheet_data in excel_data.items():
            # Create DataTable for each sheet
            data_table = DataTable(
                name=sheet_name,
                origin_desc="",
                schema=data_schema
            )
            # Create DataField for each column in the sheet
            for column_name in sheet_data.columns:
                data_field = DataField(
                    name=column_name,
                    origin_desc="",
                    table=data_table
                )
                data_table.add_field(data_field)

            # Add DataTable to DataSchema
            data_schema.add_table(data_table)

            # Add DataSchema to MetaData
            metadata_object.add_schema(data_schema)

        return metadata_object

    def query(self, struc_query: ExcelQuery) -> ExcelQueryResult:
        file_name, _, unique_filename = self._get_file_name()
        temp_sqlite_db_file = os.path.join(self.TEMP_DIR, unique_filename)

        conn = self._cached_sqlite_conns.get(unique_filename)

        if os.path.exists(temp_sqlite_db_file) and conn:
            log.info(f"使用缓存的sqlite连接：{unique_filename}")
        else:
            log.info(f"创建sqlite连接：{unique_filename}")
            conn = sqlite3.connect(temp_sqlite_db_file)
            excel_data = self._read_excel()
            for sheet_name, sheet_data in excel_data.items():
                sheet_data.to_sql(sheet_name, con=conn, if_exists='replace', index=False)
            self._cached_sqlite_conns[unique_filename] = conn

        result = pd.read_sql_query(struc_query.content, conn)
        return ExcelQueryResult(content=result)

    @classmethod
    def cleanup_temp_dir(cls):
        for file in os.listdir(cls.TEMP_DIR):
            file_path = os.path.join(cls.TEMP_DIR, file)
            # 检查文件最后访问时间
            if os.path.getatime(file_path) + cls.EXPIRATION_TIME < time.time():
                log.info(f"删除临时文件：{file_path}")
                os.remove(file_path)


log.info(f"registering data accessor: {ExcelDataAccessor.__source_type__}")


# 创建一个后台调度器
scheduler = BackgroundScheduler()
scheduler.add_job(ExcelDataAccessor.cleanup_temp_dir, 'interval', minutes=5)
log.info(f"启动后台任务：删除ExcelDataAccessor的临时文件...")
scheduler.start()

