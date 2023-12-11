from rmbcommon.models import DataSourceCore, MetaData
from rmbserver.brain.dao_service import service_dao
from rmbserver.brain.dao_meta import meta_dao
from rmbserver.log import log
from rmbserver.exceptions import DataSourceNotFound
from rmbserver.ai.tools.meta import gen_meta_desc_and_relations
from rmbserver.plugins.dataaccessor import create_data_accessor


class DataSource(DataSourceCore):

    @classmethod
    def get(cls, datasource_id: str):
        _datasource = service_dao.get_datasource_by_id(datasource_id)
        if not _datasource:
            raise DataSourceNotFound(f"DataSource not found: {datasource_id}")
        return cls(**_datasource.to_dict())


    @property
    def accessor(self):
        # 数据源的数据访问器
        return create_data_accessor(
            self.type,
            ds_name=self.name,
            ds_access_config=self.access_config
        )

    @classmethod
    def create(cls, ds_name, ds_type, ds_access_config):
        """
        创建数据源
        """
        _datasource = service_dao.add_datasource(
            ds_name=ds_name,
            ds_type=ds_type,
            ds_access_config=ds_access_config
        )

        this = cls(**_datasource.to_dict())
        this.create_or_update_brain_meta()
        return this

    def delete(self):
        self.delete_brain_meta()
        service_dao.delete_datasource(self.id)
        log.info(f"DataSource deleted! {self}")


    @classmethod
    def list(cls, name=None):
        # 获取所有的数据源
        if name:
            ds = service_dao.get_datasource_by_name(name)
            return [cls(**ds.to_dict())] if ds else []
        else:
            return [cls(**ds.to_dict()) for ds in service_dao.get_all_datasources()]

    @property
    def runtime_meta(self) -> MetaData:
        """
        实时获取数据源的 MetaData
        """
        if hasattr(self, "_runtime_meta"):
            return self._runtime_meta

        # 数据源的元数据
        metadata = self.accessor.retrieve_meta_data()
        metadata.datasource_id = self.id
        self._runtime_meta = metadata
        return metadata

    @property
    def brain_meta(self) -> MetaData:
        """
        获取 Brain 中的 MetaData
        """
        return meta_dao.get_meta_data(self.id)

    def create_or_update_brain_meta(self):
        """
        1. 使用最新的 MetaData 更新 Brain（但不会覆盖之前生成的描述）
        2. 对于新增的Schema/Table/Field，使用AI生成注释和关系
        TODO：
        1）支持关系的更新；
        2）支持深度注释更新（从Data中分析，比如枚对于状态类的字段，需要在Brain中记录有哪些枚举值）
        3）支持人工编辑注释
        3. 将生成的注释，更新到 Vector（采用从Graph中全部同步的方式）
        """
        # 保存 MetaData
        _runtime_meta = self.runtime_meta
        meta_dao.sync_to_graph(self.id, _runtime_meta)
        log.info(f"已经使用最新的 MetaData 更新 Brain（但不会覆盖之前生成的描述）")

        # 先保存，后推理，因为有可能有些 Meta 的注释被人工设置过或者之前由AI生成过，没必要再重复生成
        _brain_meta = self.brain_meta
        need_inferred_schemas = _brain_meta.to_dict_for_llm()["schemas"]
        if need_inferred_schemas:

            log.info(f"AI自动生成注释中... 可能需要一点时间 \n{_brain_meta.to_table()}")
            inferred_meta = gen_meta_desc_and_relations(_brain_meta)

            log.info(f"注释已生成！开始更新 Brain...  \n{inferred_meta.to_table()}")
            meta_dao.update_meta_data_in_graph(self.id, inferred_meta)
            meta_dao.sync_to_vector(self.id, self.brain_meta)

            log.info(f"注释更新完成！\n{self.brain_meta.to_table()}")
        else:
            log.info(f"所有 Meta 都已经有注释了，无需AI生成。")

        return self.brain_meta

    def delete_brain_meta(self):
        """
        删除 Brain 中的 MetaData
        """
        meta_dao.delete_meta_data_from_graph(self.id)
        meta_dao.delete_meta_data_from_vector(self.id)
        log.info(f"Meta in brain(graph&vector) deleted! {self}")


