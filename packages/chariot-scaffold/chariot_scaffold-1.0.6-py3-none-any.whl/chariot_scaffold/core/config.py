import json
import yaml


class PluginSpecYaml:
    def __init__(self):
        self.__dict__.update({
            "plugin_spec_version": "v2",
            "extension": "plugin",
            "entrypoint": None,
            "module": None,
            "name": None,
            "title": None,
            "description": None,
            "version": "0.1.0",
            "vendor": "chariot",
            "tags": [],
            "connection": {},
            "actions": {},
            "alarm_receivers": {},
            "asset_receivers": {},
            # "indicator_receivers": {} 已弃用
        })

    def __getitem__(self, item):
        return self.__dict__.get(item)

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        self.__dict__.pop(key)

    def __repr__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

    def __getattr__(self, item):
        return self.__dict__.get(item)

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def deserializer(self, yml=None):
        if yml:
            stream = open(yml, 'r', encoding='utf8').read()
        else:
            stream = open('plugin.spec.yaml', 'r', encoding='utf8').read()
        plugin_spec = yaml.safe_load(stream)
        self.__dict__.update(plugin_spec)    # todo 强类型校验


class DataMapping:
    def __init__(self):
        self.__data_mapping = {    # todo 待添加更多数据类型
            "<class 'int'>": "integer",
            "<class 'float'>": "float",
            "<class 'str'>": "string",
            "<class 'list'>": "[]",
            "<class 'dict'>": "object",
            "<class 'bool'>": "boolean",
            "<built-in function any>": "any",
            "list[str]": "[]string",
            "list[dict]": "[]object"
        }

    def __getitem__(self, item):
        return self.__data_mapping.get(item, "any")

    def __setitem__(self, key, value):
        self.__data_mapping[key] = value

    def __delitem__(self, key):
        self.__data_mapping.pop(key)

    def __repr__(self):
        return json.dumps(self.__data_mapping, ensure_ascii=False)
