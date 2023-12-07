import sys
import json
from chariot_scaffold import log, version
from chariot_scaffold.api_server.app import  runserver


class Runtime:
    def __init__(self, pack: type):
        self.pack = pack
        self.__func_types = ["action", "trigger", "alarm", "receiver", "asset"]

    @staticmethod
    def init_arguments():
        """
        插件初始化运行参数

        #   此方法用于获取需要的运行数据
        #   在千乘系统中，可能并不会传入json数据文件，而是会直接传入json数据或字典数据，此时输入cmd指令长度不足（输入数据不计长度）
        #   所以使用sys.stdin.read()读取可能存在的数据
        """
        arguments = sys.stdin.read()
        assert arguments, "未检测到初始化参数"

        data = json.loads(arguments)
        assert data, "初始化参数, 序列化失败"

        log.debug(f"接收初始化参数: {data}")  # todo data 校验
        return data

    def func_types_check(self, data):
        # 验证功能类型是否为 动作、触发器、告警接收器、情报接收器、资产接收器
        type_ = None
        for i in self.__func_types:
            if data.get(i):
                type_ = i
                break
        assert type_, AssertionError("请传入一个正确的功能类型参数")
        return type_

    def start(self):
        log.debug("正在启动插件")
        log.debug(f"获取初始化参数,{sys.argv}")

        if sys.argv.count("run"):
            data = self.init_arguments()

            self.pack.dispatcher_url = data["body"]["dispatcher"]["url"]
            self.pack.cache_url = data["body"]["dispatcher"]["cache_url"]
            self.pack.webhook_url = data["body"]["dispatcher"]["webhook_url"]

            module = self.pack()
            func_type = self.func_types_check(data["body"])

            if data["body"]["connection"]:
                module.connection(**data["body"]["connection"])

            module.__getattribute__(data["body"][func_type])(**data["body"]["input"])

        elif sys.argv.count("http"):
            #   默认工作进程
            workers = 4
            log.debug(f"启动plugin server V{version}")
            runserver(workers)
