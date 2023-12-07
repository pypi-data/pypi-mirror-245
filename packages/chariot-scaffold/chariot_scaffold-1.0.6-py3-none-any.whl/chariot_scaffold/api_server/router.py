from fastapi import APIRouter
from chariot_scaffold.tools import clean_logs, read_logs
from chariot_scaffold.core.config import PluginSpecYaml
import importlib


class ActionRouter(APIRouter):
    def __init__(self):
        super().__init__()
        self.add_api_route("/actions/{action_name}", self.actions, methods=["POST"])
        self.plugin_spec = PluginSpecYaml()
        self.plugin_spec.deserializer()

    def actions(self, action_name: str, plugin_stdin: dict):    # todo plugin_stdin 数据校验
        """
        # 动作接口
        action_name = func_name
        version='v1' type='action_start' body=ACTION_TEST_BODY_MODEL(meta={}, connection={}, dispatcher=DISPATCHER_MODEL(url='http://127.0.0.1:10001/transpond', cache_url=''), input={'data': 'hello'}, enable_web=False, config={}, action='test')
        {'version': 'v1', 'type': 'action', 'body': {'output': {'result': 'hello'}, 'status': 'True', 'log': '[2023-09-20 07:11:16] INFO\n  根据 PLUGIN_TEST_MODEL 校验数据中\n[2023-09-20 07:11:16] INFO\n  校验完成\n[2023-09-20 07:11:16] INFO\n  插件运行中\n[2023-09-20 07:11:16] INFO\n  未传入配置信息，使用默认配置\n[2023-09-20 07:11:16] INFO\n  校验连接器数据\n[2023-09-20 07:11:16] INFO\n  根据 CONNECTION 校验数据中\n[2023-09-20 07:11:16] INFO\n  校验完成\n[2023-09-20 07:11:16] INFO\n  运行连接器中\n[2023-09-20 07:11:16] INFO\n  连接器运行正常\n[2023-09-20 07:11:16] INFO\n  构建连接器运行信息\n[2023-09-20 07:11:16] INFO\n  构建输出数据\n', 'error_trace': ''}}
        """
        output = {'version': 'v1', 'type': 'action', 'body': {'output': {}, 'status': 'True', 'log': '暂时没日志', 'error_trace': ''}}  # todo 日志返回

        # import module
        module = importlib.import_module(self.plugin_spec['entrypoint'])
        pack = module.__getattribute__(self.plugin_spec['module'])()

        # connection
        if plugin_stdin.get("body", {}).get("connection"):
            pack.connection(**plugin_stdin["body"]["connection"])

        # action running
        res = pack.__getattribute__(action_name)(**plugin_stdin["body"]["input"])
        output["body"]["log"] = read_logs()
        # check output
        if self.plugin_spec["actions"].get(action_name):
            if self.plugin_spec["actions"][action_name]["output"].get("output"):
                output["body"]["output"]["output"] = res
            else:
                output["body"]["output"] = res

        clean_logs()
        return output
