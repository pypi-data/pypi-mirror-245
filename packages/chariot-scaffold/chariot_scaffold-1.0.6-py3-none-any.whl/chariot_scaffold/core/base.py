import abc
from chariot_scaffold import data_mapping


class Base(metaclass=abc.ABCMeta):
    def __init__(self, title=None, description=None, model=None):
        self.__vars_name = None
        self.__defaults = None
        self.__comments = None
        self.__annotations = None
        self.__params_name = None
        self._func_name = None

        self.model = model
        self.title = title
        self.description = description

        self.input = {}
        self.output = {}

    def __call__(self, func):
        self.bind_func_info(func)
        self.generate_func_info()
        self.hook()

        def wrapper(*args, **kwargs):
            mapping = self.get_params_mapping(*args, **kwargs)
            if self.model:
                self.check_model(mapping)

            res = func(*args, **kwargs)
            return res
        return wrapper

    def generate_func_info(self):
        self.bind_param()
        self.bind_datatype()
        self.bind_defaults()
        self.bind_comments()
        self.bind_output()

    def bind_func_info(self, func):
        self.__vars_name = func.__code__.co_varnames
        self.__params_name = [self.__vars_name[i] for i in range(func.__code__.co_argcount)]  # 参数名
        self.__annotations = func.__annotations__ # 注解
        self.__comments = func.__doc__ # 注释
        self.__defaults = func.__defaults__ # 默认值
        self._func_name = func.__name__

    def bind_param(self):
        for i in self.__params_name:
            if i != 'self':
                self.input[i] = {"name": i, "default": None, "title": None, "description": None, "type": None, "required": False}

    def bind_datatype(self):
        # 连接器参数类型绑定
        for i in self.__params_name:
            if i != "self":
                anno = self.__annotations.get(i)
                if "Annotated" in str(anno):
                    self.input[i]["type"] =  data_mapping[str(anno.__origin__)]
                else:
                    self.input[i]["type"] = data_mapping[str(anno)]

    def bind_defaults(self):
        # required和default属性绑定
        defaults_length = len(self.__defaults) if self.__defaults else 0
        for i in range(len(self.__params_name)):
            if self.__params_name[::-1][i] != 'self':
                # 有默认值可以不传参, 无默认值则必传
                if i < defaults_length:
                    self.input[self.__params_name[::-1][i]]["default"] = self.__defaults[::-1][i]

                    if self.input[self.__params_name[::-1][i]]["default"] is None:  # 参数类型为list,dict的默认值为None的全部处理成[],{}
                        if self.input[self.__params_name[::-1][i]]["type"] == "[]":     # 千乘array,object类型无法传入null
                            self.input[self.__params_name[::-1][i]]["default"] = []
                        if self.input[self.__params_name[::-1][i]]["type"] == "object":
                            self.input[self.__params_name[::-1][i]]["default"] = {}
                else:
                    self.input[self.__params_name[::-1][i]]["required"] = True

    def bind_comments(self):
        for i in self.__params_name:
            if i != "self":
                anno = self.__annotations.get(i)
                if "Annotated" in str(anno):
                    assert len(anno.__metadata__) == 2, "既然决定用Annotated了,那就把title, description都写了吧"
                    self.input[i]["title"] = anno.__metadata__[0]
                    self.input[i]["description"] =  anno.__metadata__[1]
                else:
                    self.input[i]["title"] = i
                    self.input[i]["description"] = None

    def bind_output(self):
        output_type = self.__annotations.get("return")

        if output_type:
            # 返回值注解绑定
            if type(output_type) is dict:
                for k, v in output_type.items():
                    assert type(v).__name__ == "_AnnotatedAlias", "请使用Annotated作为返回值的注解"
                    assert len(v.__metadata__) == 2, "既然决定用Annotated了,那就把title, description都写了吧"
                    self.output[k] = {"title": v.__metadata__[0], "description": v.__metadata__[1], "type": data_mapping[str(v.__origin__)]}
            else:
                # 返回值默认绑定
                self.output["output"] = {}
                self.output["output"]["type"] = data_mapping[str(output_type)]
                # self.output["output"]["required"] = True

    def check_model(self, kwargs):
        """
        参数强类型校验
        :param kwargs: 参数
        :return: None
        """
        self.model(**kwargs)

    def get_params_mapping(self, *args, **kwargs) -> dict:
        """
        绑定args、kwargs与参数之间的映射关系, 便于强类型校验使用
        :param args:
        :param kwargs:
        :return: mapping
        """
        mapping = {}

        # 先绑定默认值
        if self.__defaults:
            for i in range(len(self.__defaults)):
                mapping[list(self.__params_name)[::-1][i]] = list(self.__defaults)[::-1][i]

        # 再按顺序填入arg
        for i in range(len(args)):
            if self.__params_name[i] != "self":
                mapping[self.__params_name[i]] = args[i]

        # 最后合并kwargs
        mapping.update(kwargs)
        return mapping

    @abc.abstractmethod
    def hook(self):
        ...