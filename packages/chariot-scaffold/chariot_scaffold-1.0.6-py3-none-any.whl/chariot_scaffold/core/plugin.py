import os
import sys
import abc
import json
import yaml
import requests
from chariot_scaffold import plugin_spec, lang
from chariot_scaffold.tools import generate_file
from chariot_scaffold.core.base import Base
from chariot_scaffold.tools import generate_online_pack, generate_offline_pack


requests.packages.urllib3.disable_warnings() # noqa


class Connection(Base):
    def __init__(self, model=None):
        """
        连接器
        :param model: 强类型校验
        """
        super().__init__(model=model)

    def hook(self):
        connection = {}
        for k, v in self.input.items():
            connection[k] = {"title": {lang: v["title"]}, "description": {lang: v["description"]}, "type": v["type"]}

            if v["required"]:
                connection[k]["required"] = v["required"]
            if v["default"] is not None:
                connection[k]["default"] = v["default"]
        plugin_spec.connection = connection


class Action(Base):
    def __init__(self, title=None, description=None, model=None): # noqa
        """
        动作
        :param title: 名称
        :param description: 描述
        :param model: 强类型校验
        """
        super().__init__(title, description, model)

    def hook(self):
        actions = {self._func_name: {"title": {lang: self.title} , "description": {lang: self.description}, "input": {}, "output":{}}}

        for k, v in self.input.items():
            actions[self._func_name]["input"][k] = {"title": {lang: v["title"]}, "description": {lang: v["description"]}, "type": v["type"]}

            if v["required"]:
                actions[self._func_name]["input"][k]["required"] = v["required"]
            if v["default"] is not None:
                actions[self._func_name]["input"][k]["default"] = v["default"]

        if not self.output.get("output"):
            # 返回值注解绑定
            for k, v in self.output.items():
                actions[self._func_name]["output"][k] = {"title": {lang: v["title"]}, "description": {lang: v["description"]}, "type": v["type"]}
        else:
            # 默认返回值绑定
            actions[self._func_name]["output"]["output"] = {"title": {lang: "输出"}, "description": {lang: "输出"}, "type": self.output["output"]["type"]}

        plugin_spec.actions.update(actions)


class Trigger(Base):
    def __init__(self, title=None, description=None, model=None, trigger_type="alarm_receivers"):   # noqa
        """
        触发器
        :param title: 名称
        :param description: 描述
        :param model: 强类型校验
        :param trigger_type: 触发器类型, 目前就两种告警触发器和资产触发器即alarm_receivers, asset_receivers. 默认alarm_receivers.
        """
        trigger_types = ["alarm_receivers", "asset_receivers"]
        assert trigger_type in trigger_types, AssertionError("请传入一个正确的触发器类型")

        self.trigger_type = trigger_type
        super().__init__(title, description, model)

    def hook(self):
        trigger = {self._func_name: {"title": {lang: self.title} , "description": {lang: self.description},
                                            "input": {}}}
        for k, v in self.input.items():
            trigger[self._func_name]["input"][k] = {"title": {lang: v["title"]},
                                                            "description": {lang: v["description"]}, "type": v["type"]}

            if v["required"]:
                trigger[self._func_name]["input"][k]["required"] = v["required"]
            if v["default"] is not None:
                trigger[self._func_name]["input"][k]["default"] = v["default"]
        plugin_spec[self.trigger_type].update(trigger)


class TriggerExtend:
    def __init__(self, dispatcher_url, cache_url):
        self.__session = requests.Session()
        self.dispatcher_url = dispatcher_url
        self.cache_url = cache_url

    def send(self, alarm):
        """发送告警给千乘"""
        response = self.__session.post(self.dispatcher_url, verify=False, json=alarm)
        assert response.status_code == 200, "调用失败"

    def set_cache(self, data):
        cache = {
            "method": "set",
            "data": json.dumps(data),
        }
        response = self.__session.post(self.cache_url, json=cache, verify=False)
        assert response.status_code == 200, "调用失败"
        return response.json()

    def get_cache(self):
        method = {
            "method": "get"
        }
        response = self.__session.post(self.cache_url, json=method, verify=False)
        assert response.status_code == 200, "调用失败"
        return response.json()


class Pack(metaclass=abc.ABCMeta):
    def __init__(self):
        self.create_trigger_extend()

    @abc.abstractmethod
    def connection(self, *args, **kwargs):  # 该裹的裹脚布一个也少不了
        ...

    @classmethod
    def plugin_config_init(cls, name, title=None, description=None, version=None, tags: list| None =None, vendor="chariot"):
        """
        初始化参数配置
        :param name: 插件id, 以字母、下划线方式命名, 例如chariot_plugin. 请勿使用特殊字符
        :param title: 插件标题, 即展示在千乘页面的插件名称
        :param description: 插件描述, 即展示在千乘页面的插件描述
        :param version: 插件版本
        :param tags:    插件标签, 为了方便在插件社区里搜索
        :param vendor:  作者
        :return:
        """
        plugin_spec.entrypoint = os.path.split(os.path.abspath(sys.modules[cls.__module__].__file__))[-1].replace('.py', '')

        plugin_spec.module= cls.__name__
        plugin_spec.title =  title if title else cls.__name__
        plugin_spec.version =  version if version else "0.1.0"
        plugin_spec.description = description
        plugin_spec.name = name
        plugin_spec.tags = tags if tags else []
        plugin_spec.vendor = vendor # 作者

    @classmethod
    def generate_online_pack(cls, path=None):
        file_path = os.path.abspath(sys.modules[cls.__module__].__file__) if path is None else path
        assert os.path.exists(file_path), FileNotFoundError("目录不存在")
        generate_online_pack(file_path, plugin_spec.name, plugin_spec.vendor, plugin_spec.version)

    @classmethod
    def generate_offline_pack(cls, path=None):
        file_path = os.path.abspath(sys.modules[cls.__module__].__file__) if path is None else path
        assert os.path.exists(file_path), FileNotFoundError("目录不存在")
        generate_offline_pack(file_path, plugin_spec.name, plugin_spec.vendor, plugin_spec.version)

    @classmethod
    def multi_name_detect(cls, func_name):
        """注册类重名检测"""
        if func_name in cls.__dict__.keys() and func_name != "__init__":
            raise NameError("注册类方法名请勿与插件类方法重名")

    def create_trigger_extend(self):
        """热加载Session"""
        if plugin_spec.alarm_receivers or plugin_spec.asset_receivers:
            self.register(TriggerExtend, *(self.dispatcher_url, self.cache_url))

    def register(self, object_: object, *args, **kwargs):
        """
        注册其他类方法到插件中, 用于分模块编写插件，便于阅读。*args, **kwargs是给你传的object用的。
        """
        obj = object_(*args, **kwargs)  # noqa
        for k, v in object_.__dict__.items():
            if hasattr(v, "__call__") and k != "__init__":
                self.multi_name_detect(k)
                exec(f"self.__dict__[k] = obj.{k}")

    def create_yaml(self, path=None):
        file_path = path if path is not None else "./"
        assert os.path.exists(file_path), FileNotFoundError("目录不存在")
        stream = open(os.path.join(file_path, "plugin.spec.yaml"), 'w', encoding='utf8')
        yaml.safe_dump(self.json, stream, allow_unicode=True, sort_keys=False, default_flow_style=False)

    def generate_project(self, path=None):
        self.create_yaml(path=path)
        generate_file(module=plugin_spec.module, entrypoint=plugin_spec.entrypoint, path=path)

    @property
    def yaml(self):
        return yaml.safe_dump(self.json, allow_unicode=True, sort_keys=False)

    @property
    def json(self):
        return json.loads(plugin_spec.__repr__())

    @property
    def dispatcher_url(self):
        return "http://127.0.0.1:10001/transpond"

    @dispatcher_url.setter
    def dispatcher_url(self, url):
        self.dispatcher_url = url

    @property
    def cache_url(self):
        return ""

    @cache_url.setter
    def cache_url(self, url):
        self.cache_url = url

    @property
    def webhook_url(self):
        return ""

    @webhook_url.setter
    def webhook_url(self, url):
        self.webhook_url = url

    def __repr__(self):
        return plugin_spec.__repr__()
