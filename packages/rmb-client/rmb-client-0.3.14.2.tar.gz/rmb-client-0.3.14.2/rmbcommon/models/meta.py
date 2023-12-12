from functools import wraps
import json
from tabulate import tabulate


def json_to_string(func):
    # 将函数返回的JSON dict对象转换为字符串
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return json.dumps(result, indent=4, ensure_ascii=False)
    return wrapper


class DataBaseObject:
    _save_in_db_properties = []

    @property
    def db_properties(self):
        return {k: v for k, v in self.__dict__.items()
                if k in self._save_in_db_properties}

    def to_dict(self):
        raise NotImplementedError

    def to_dict_for_llm(self):
        raise NotImplementedError

    @json_to_string
    def to_string(self):
        return self.to_dict()

    @json_to_string
    def to_string_for_llm(self):
        return self.to_dict_for_llm()

    def __str__(self):
        return self.to_string()


class DataField(DataBaseObject):

    _save_in_db_properties = ['name', 'full_name', 'origin_desc',
                              'curr_desc', 'curr_desc_stat']

    def __init__(self, name, table, origin_desc=None, curr_desc=None,
                 curr_desc_stat=None, related_field=None, **kwargs):
        self.name = name
        self.origin_desc = origin_desc
        self.table = table  # Reference to the DataTable
        self.full_name = f"{self.table.schema.name}.{self.table.name}.{self.name}"
        if curr_desc:
            self.curr_desc = curr_desc
            self.curr_desc_stat = curr_desc_stat
        else:
            self.curr_desc = origin_desc
            self.curr_desc_stat = 'origin'
        self.related_field = related_field  # Reference to related DataField, if any

    def set_related_field(self, field):
        self.related_field = field

    def __repr__(self):
        return f"<DataField(name='{self.full_name}', curr_desc='{self.curr_desc}')>"

    def to_dict(self):
        result = {
            'name': self.name,
            'origin_desc': self.origin_desc,
            'curr_desc': self.curr_desc
        }
        if self.related_field:
            result['related_field'] = self.related_field.full_name
        return result

    def to_dict_for_llm(self):
        result = {
            'name': self.name,
            'curr_desc': self.curr_desc,
        }
        if self.related_field:
            result['related_field'] = self.related_field.full_name
        return result


class DataTable(DataBaseObject):

    _save_in_db_properties = ['name', 'full_name', 'origin_desc',
                              'curr_desc', 'curr_desc_stat']

    def __init__(self, name, schema, origin_desc=None,
                 curr_desc=None, curr_desc_stat=None, **kwargs):
        self.name = name
        self.origin_desc = origin_desc
        self.schema = schema  # Reference to the DataSchema
        self.full_name = f"{self.schema.name}.{self.name}"
        if curr_desc:
            self.curr_desc = curr_desc
            self.curr_desc_stat = curr_desc_stat
        else:
            # 如果没有指定 curr_desc，则默认使用 origin_desc
            self.curr_desc = origin_desc
            self.curr_desc_stat = 'origin'
        self.fields = []

    def add_field(self, field: DataField):
        self.fields.append(field)

    def __repr__(self):
        return f"<DataTable(name='{self.full_name}', curr_desc='{self.curr_desc}')>"

    def to_dict(self, level='field'): # level: field, table, schema
        _d = {
            'name': self.name,
            'origin_desc': self.origin_desc,
            'curr_desc': self.curr_desc,
        }
        if level == 'field':
            _d['fields'] = [field.to_dict() for field in self.fields]
        return _d

    def to_dict_for_llm(self):
        # 如果有任何一个字段的 curr_desc 为空，则需要AI生成
        need_infer = 0
        for f in self.fields:
            if not f.curr_desc:
                need_infer = 1

        if need_infer:
            return {
                'name': self.name,
                'full_name': self.full_name,
                'curr_desc': self.curr_desc,
                'fields': [field.to_dict_for_llm() for field in self.fields]
            }
        else:
            return {}


class DataSchema(DataBaseObject):

    _save_in_db_properties = ['name', 'origin_desc', 'curr_desc',
                              'curr_desc_stat', 'curr_desc_stat']

    def __init__(self, name, metadata, origin_desc=None,
                 curr_desc=None, curr_desc_stat=None, **kwargs):
        self.name = name
        self.metadata = metadata  # Reference to the MetaData
        self.origin_desc = origin_desc
        if curr_desc:
            self.curr_desc = curr_desc
            self.curr_desc_stat = curr_desc_stat
        else:
            self.curr_desc = origin_desc
            self.curr_desc_stat = 'origin'
        self.tables = []

    def add_table(self, table: DataTable):
        self.tables.append(table)

    def __repr__(self):
        return f"<Schema: {self.name}>"

    def to_dict(self, level='field'):  # level: field, table, schema
        _d = {
            'name': self.name,
            'origin_desc': self.origin_desc,
            'curr_desc': self.curr_desc,
        }
        if level in ('table', 'field'):
            _d['tables'] = [table.to_dict(level) for table in self.tables]
        return _d

    def to_dict_for_llm(self):
        # if table.to_dict_for_llm() is empty, it will be ignored
        need_infer_tables = [table.to_dict_for_llm() for table in self.tables
                             if table.to_dict_for_llm()]
        if need_infer_tables or (not self.curr_desc):
            return {
                'name': self.name,
                'curr_desc': self.curr_desc,
                'tables': need_infer_tables
            }
        else:
            return {}


class MetaData(DataBaseObject):
    def __init__(self, name, datasource_id=''):
        self.name = name
        self.datasource_id = datasource_id
        self.schemas = []

    def add_schema(self, schema: DataSchema):
        self.schemas.append(schema)

    @classmethod
    def load_from_dict(cls, data: dict):
        """
        Load metadata from a dictionary structure.
        The expected format is:
        {
            'name': 'metadata_name',
            'datasource_id': '',
            'schemas': [
                {
                    'name': 'schema_name',
                    'tables': [
                        {
                            'name': 'table_name',
                            'fields': [
                                {
                                    'name': 'field_name',
                                    'origin_desc': 'original description',
                                    'related_field': 'schema2.table2.field2'
                                    ...
                                },
                                ...
                            ],
                            ...
                        },
                        ...
                    ],
                    ...
                },
                ...
            ]
        }
        """
        # 临时字典，用于存储字段引用
        field_refs = {}
        metadata = cls(data.get('name'), data.get('datasource_id'))
        # 首先，创建所有的 schema、table 和 field，但不设置 related_field
        for schema_data in data.get('schemas', []):
            schema = DataSchema(
                name=schema_data.get('name', ''),
                metadata=metadata,
                origin_desc=schema_data.get('origin_desc'),
                curr_desc=schema_data.get('curr_desc'),
                curr_desc_stat=schema_data.get('curr_desc_stat')
            )

            for table_data in schema_data.get('tables', []):
                table = DataTable(
                    name=table_data.get('name', ''),
                    schema=schema,
                    origin_desc=table_data.get('origin_desc'),
                    curr_desc=table_data.get('curr_desc'),
                    curr_desc_stat=table_data.get('curr_desc_stat')
                )

                for field_data in table_data.get('fields', []):
                    field = DataField(
                        name=field_data.get('name', ''),
                        table=table,
                        origin_desc=field_data.get('origin_desc'),
                        curr_desc=field_data.get('curr_desc'),
                        curr_desc_stat=field_data.get('curr_desc_stat'),
                    )
                    table.add_field(field)
                    # 创建一个唯一键来标识每个字段
                    field_key = f"{schema.name}.{table.name}.{field.name}"
                    field_refs[field_key] = field

                schema.add_table(table)

            metadata.add_schema(schema)

        # 现在，使用 field_refs 字典来设置 related_field 属性
        for schema_data in data.get('schemas', []):
            for table_data in schema_data.get('tables', []):
                for field_data in table_data.get('fields', []):
                    field_key = f"{schema_data.get('name', '')}.{table_data.get('name', '')}.{field_data.get('name', '')}"
                    field = field_refs.get(field_key)
                    related_field_key = field_data.get('related_field')
                    if related_field_key and related_field_key in field_refs:
                        # 设置相关字段的引用
                        field.set_related_field(field_refs[related_field_key])
        return metadata

    def __repr__(self):
        return f"{self.datasource_id} {self.summary} \n\n{self.to_table()}"

    def to_dict(self, level='field'):  # level: field, table, schema
        return {
            'name': self.name,
            'datasource_id': self.datasource_id,
            'schemas': [schema.to_dict(level) for schema in self.schemas]
        }

    def to_dict_for_llm(self):
        return {
            'name': self.name,
            'datasource_id': self.datasource_id,
            'schemas': [schema.to_dict_for_llm() for schema
                        in self.schemas if schema.to_dict_for_llm()]
        }

    @property
    def summary(self):
        """
        Summarize the metadata。只有Schema和Table给出前10条 item，Field不给出。
        Like this:
            共有：1 Schema (public), 1 Table (users), 2 Fields.
        """
        summary = f"共有："

        # Summarizing schemas
        schema_count = len(self.schemas)
        if schema_count <= 1:
            summary += f"{schema_count} Schema ("
        else:
            summary += f"{schema_count} Schemas ("
        for i, schema in enumerate(self.schemas[:10]):
            summary += schema.name
            if i < min(9, schema_count - 1):  # Add comma if not the last item
                summary += ","
        if schema_count > 10:
            summary += "..."
        summary += "), "

        # Summarizing tables and fields
        total_tables = 0
        total_fields = 0
        table_names = []

        for schema in self.schemas:
            total_tables += len(schema.tables)
            for table in schema.tables:
                total_fields += len(table.fields)
                if len(table_names) <= 5:
                    table_names.append(table.full_name)

        # Formatting tables list
        table_list = ",".join(table_names)
        if len(table_names) > 5:
            table_list += "..."

        if total_tables <= 1:
            summary += f"{total_tables} Table ({table_list}), "
        else:
            summary += f"{total_tables} Tables ({table_list}), "
        if total_fields <= 1:
            summary += f"{total_fields} Field."
        else:
            summary += f"{total_fields} Fields."
        return summary

    def get_field_by_full_name(self, full_name):
        """
        根据字段的完整名称来查找字段对象。
        完整名称格式为 "schema_name.table_name.field_name"
        """
        schema_name, table_name, field_name = full_name.split('.')
        for schema in self.schemas:
            if schema.name == schema_name:
                for table in schema.tables:
                    if table.name == table_name:
                        for field in table.fields:
                            if field.name == field_name:
                                return field
        return None

    def to_table(self, level='field'):  # level: field, table, schema
        data = []
        for schema in self.schemas:
            schema_desc = schema.name
            schema_desc += f"({schema.curr_desc})" if schema.curr_desc else ""
            if level == 'schema':
                _s = {
                    'Schemas': schema_desc,
                }
                data.append(_s)
            elif level in ('table', 'field'):
                for table in schema.tables:
                    table_desc = table.name
                    table_desc += f"({table.curr_desc})" if table.curr_desc else ""
                    _t = {
                        'Schemas': schema_desc,
                        'Tables': table_desc,
                    }
                    if level == 'field':
                        known_f = len([f for f in table.fields if f.curr_desc])
                        all_f = len(table.fields)
                        fields = f"{known_f}/{all_f}"
                        _t['Fields(known/all)'] = fields
                    data.append(_t)
            else:
                raise ValueError(f"Invalid level: {level}")
        return tabulate(data, headers="keys", tablefmt="plain")