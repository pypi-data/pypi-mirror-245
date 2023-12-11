from tpltable.utils import *
import inspect

class _Pipe_decorator:
    InK_ATTR = "_tpltable_Pipe_in_keys"
    OutK_ATTR = "_tpltable_Pipe_out_keys"
    RpK_ATTR = "_tpltable_Pipe_replace"
    Rn_ATTR = "_tpltable_Pipe_raw_name"

    @staticmethod
    def _wrap_target(func, in_keys: Union[list, tuple, str]=None, out_keys: Union[list, tuple, str]=None, replace: bool=False):
        if hasattr(func, _Pipe_decorator.Rn_ATTR) and hasattr(func, _Pipe_decorator.InK_ATTR) and \
            hasattr(func, _Pipe_decorator.OutK_ATTR) and hasattr(func, _Pipe_decorator.RpK_ATTR):
            return func

        # 检查第一个参数的名字
        if inspect.getfullargspec(func).args and inspect.getfullargspec(func).args[0] == "self":
            log.error(ValueError, f"Cannot support the method: {func}. If it isn't a method, please do not use 'self' as the first argument", exit=True)

        if isinstance(in_keys, str):
            in_keys = tpl_keysplit(in_keys, advance=True)
        if isinstance(out_keys, str):
            out_keys = tpl_keysplit(out_keys, advance=False)
        if in_keys is None:
            in_keys = []
        if out_keys is None:
            out_keys = []

        _raw_func_name = func.__name__

        wrarpped = ClassicalDecorator(func)

        setattr(wrarpped, _Pipe_basic.Rn_ATTR, _raw_func_name)
        setattr(wrarpped, _Pipe_basic.InK_ATTR, in_keys)
        setattr(wrarpped, _Pipe_basic.OutK_ATTR, out_keys)
        setattr(wrarpped, _Pipe_basic.RpK_ATTR, replace)
        return wrarpped

    @staticmethod
    def _get_finfo(func):
        """
        获取函数的信息
        :param func:
        :return:
        """
        in_keys = getattr(func, _Pipe_basic.InK_ATTR)
        out_keys = getattr(func, _Pipe_basic.OutK_ATTR)
        replace = getattr(func, _Pipe_basic.RpK_ATTR)
        fname = getattr(func, _Pipe_basic.Rn_ATTR)

        if in_keys is None or not isinstance(in_keys, (list, tuple)):
            log.error(TypeError, f"the {getattr(func, _Pipe_basic.Rn_ATTR, func.__name__)} must have a {_Pipe_basic.InK_ATTR} attribute", exit=True)

        if in_keys is None:
            in_keys = []

        # if out_keys is None:
        #     out_keys = [_ for _ in in_keys]

        return fname, in_keys, out_keys, replace

    @staticmethod
    def Func(in_keys: Union[list, tuple, str] = None, out_keys: Union[list, tuple, str] = None, replace=False) -> Callable:
        """
        将目标函数装饰成一个Pipe可以直接使用的函数
        这种处理函数必须返回简单类型或是(list, tuple)[简单类型]
        :param in_keys:
        :param out_keys:
        :param replace: bool, 是否用输出的目标名称替换输入的目标名称
        :return:
        """
        def _inner(func):
            return _Pipe_decorator._wrap_target(func, in_keys, out_keys, replace)

        return _inner

class _Pipe_basic(_Pipe_decorator):
    """
    处理ndarr_dict这样的数据
    用来挂载一组函数, 并且可以按照顺序执行这组函数
    """
    def __init__(self, format: dict):
        """
        :param format: dict, 格式为: {"$XXX": vec4, ...}
        :param warn: bool, 是否开启警告
        """
        self.__funcs = []
        self._input_format = format
        self._last_format = format.copy()

        self._warn = True


    @property
    def funcs(self):
        return self.__funcs.copy()

    def _login(self, func):
        """
        注册信息到一个处理函数
        :param func: 必须已经被copy.deepcopy 了
        :return:
        """
        if not hasattr(func, self.InK_ATTR) or not hasattr(func, self.OutK_ATTR) or not hasattr(func, self.RpK_ATTR):
            # raise TypeError("The function must be decorated by Pipe.Func or use Pipe.add to add it")
            log.error(TypeError, "The function must be decorated by Pipe.Func or use Pipe.add to add it", exit=True)

        func = copy.deepcopy(func)  # 防止raw_func被修改
        fname, in_keys, out_keys, replace = self._get_finfo(func)

        ## check&build in_keys
        _new_inkeys, expand_flag = [], False
        for i, k in enumerate(in_keys):
            if not k.startswith("$"):
                log.error(ValueError, f"the {fname}.in_keys: '{k}' must be startswith '$'", exit=True)
            # 检查是否需要展开
            if ":" in k:
                _new = expand_area_key(k, self._last_format)
                _new_inkeys.extend(_new)
                expand_flag = True
            else:
                _new = [k]
                _new_inkeys.append(k)
            # 检查k in _new是否存在
            for _ in _new:
                if _ not in self._last_format:
                    log.error(ValueError, f"the {fname}.in_keys: '{_}' not in last layer output format: {self._last_format}", exit=True)
        if expand_flag:
            setattr(func, self.InK_ATTR, _new_inkeys)

        ## check out_keys
        for k in out_keys:
            if not k.startswith("$"):
                log.error(ValueError, f"the {fname}.out_keys: '{k}' must be startswith '$'", exit=True)
        if expand_flag and out_keys!= in_keys:
            setattr(func, self.OutK_ATTR, _new_inkeys.copy())

        self._last_format = self._induce_format(self._last_format, [func], self._warn)
        self.__funcs.append(func)

    def add(self, func, in_keys: Union[list, tuple, str] = None, out_keys: Union[list, tuple, str] = None, replace=False):
        """
        添加一个处理函数, 这种处理函数必须返回简单类型或是(list, tuple)[简单类型]
        :param func: 用于处理数据的函数, 要求函数的形参数量与in_keys的长度一致, 返回值的数量与out_keys的长度一致
        :param in_keys: 函数关注的目标名称, like: $XXX, ...
        :param out_keys: 函数输出的目标名称, like: $XXX, ...
            out_keys=None, 表示输出的目标名称和输入的目标名称一致
        :param replace: bool, 是否用输出的目标名称替换输入的目标名称
        :return:
        """

        func = self._wrap_target(func, in_keys, out_keys, replace)
        self._login(func)

    def __iadd__(self, other):
        """
        重载 += 操作符, 用于添加一个处理函数
        :param other:
        :return:
        """
        self._login(other)
        return self


    @staticmethod
    def _create_indata(func, data, inkeys, replace):
        """
        创建函数的输入
        :param func:
        :param data:
        :param inkeys:
        :param replace:
        :return:
        """
        in_data = []
        for k in inkeys:
            if k not in data:
                # raise ValueError(f"the {getattr(func, _Pipe_basic.Rn_ATTR, func.__name__)} need a key {k}, but not in data: {data}")
                log.error(ValueError, f"the {getattr(func, _Pipe_basic.Rn_ATTR, func.__name__)} need a key {k}, but not in data: {data}", exit=True)
            if replace:
                _ = data.pop(k)
            else:
                _ = data[k]
            if _ is None:
                _ = ""
            in_data.append(str(_))
        # 检查None, 替换为''
        for i, v in enumerate(in_data):
            if v is None:
                in_data[i] = ''
        return in_data

    @staticmethod
    def _update_fdata(fname, fdata, outdata, outkeys, warn) -> dict:
        """
        更新fdata
        :param fname:
        :param fdata: dict
        :param outdata:
        :param outkeys:
        :param warn:
        :return:
        """
        if len(outkeys) == 1:
            outdata = [outdata]
        if not isinstance(outdata, (list, tuple)):
            # raise ValueError(f"the {fname} must return a list or tuple. But got {outdata}")
            log.error(ValueError, f"the {fname} must return a list or tuple. But got {outdata}", exit=True)
        if len(list(outdata)) != len(outkeys):
            #raise ValueError(
            #    f"the {fname} must return {len(outkeys)} values. But got {outdata}")
            log.error(ValueError, f"the {fname} must return {len(outkeys)} values. But got {outdata}", exit=True)

        for out_k, v in zip(outkeys, outdata):
            if out_k in fdata and warn:
                # warn
                #warnings.warn(f"the {fname} will overwrite the {out_k} in data")
                log.warn(f"the {fname} will overwrite the {out_k} in data")
            fdata[out_k] = v
        return fdata

    @staticmethod
    def _unit(func, data: np.ndarray, debug=False) -> np.ndarray:
        """
        执行单个函数
        """
        fname, in_keys, out_keys, replace = _Pipe_basic._get_finfo(func)
        # assert isinstance(data, np.ndarray), f"the data must be a ndarray. But got {type(data)}"
        if not isinstance(data, np.ndarray):
            log.error(TypeError, f"the data must be a ndarray. But got {type(data)}", exit=True)
        if data.ndim != 2:
            # raise ValueError("The ndarr must be a 2d array")
            log.error(ValueError, "The ndarr must be a 2d array", exit=True)
        yCnt, xCnt = data.shape

        # ----------------------- unpack ndarr ----------------------- #
        for ix in range(yCnt):
            for iy in range(xCnt):
                fdata = data[ix, iy]
                if not isinstance(fdata, dict):
                    # raise TypeError("The data must be a ndarray of dict {'$XXX': str}")
                    log.error(TypeError, "The data must be a ndarray of dict {'$XXX': str}", exit=True)
                if not fdata:
                    continue

                # 检查是否需要执行
                if not in_keys:
                    continue

                in_data = _Pipe_basic._create_indata(func, fdata, in_keys, replace)  # 创建函数的输入数据

                # 执行函数
                if debug:
                    # print(f"Test<{fname}>.Input: {in_data}")
                    log.info(f"Test<{fname}>.Input: {in_data}")
                out_data = func(*in_data)
                if debug:
                    # print(f"Test<{fname}>.Output: {out_data}")
                    log.info(f"Test<{fname}>.Output: {out_data}")

                # 更新fdata
                fdata = _Pipe_basic._update_fdata(fname, fdata, out_data, out_keys, debug)

        # ----------------------- final adjustment ndarr ----------------------- #
        new_data = data
        if in_keys:
            return new_data
        if out_keys and debug:
            # warnings.warn(f"the {getattr(func, _Pipe_basic.Rn_ATTR, func.__name__)} will change the hole data but has out_keys. Will Ignore")
            log.warn(f"the {getattr(func, _Pipe_basic.Rn_ATTR, func.__name__)} will change the hole data but has out_keys. Will Ignore")

        # 执行函数
        out_data = func(np.array(new_data))
        if not isinstance(out_data, np.ndarray):
            # raise ValueError(f"the {getattr(func, _Pipe_basic.Rn_ATTR, func.__name__)} must return a ndarray. But got {out_data}")
            log.error(ValueError, f"the {getattr(func, _Pipe_basic.Rn_ATTR, func.__name__)} must return a ndarray. But got {out_data}", exit=True)
        if out_data.ndim != 2 and debug:
            # warnings.warn(f"the {getattr(func, _Pipe_basic.Rn_ATTR, func.__name__)} need return a 2d ndarray. But got {out_data.ndim}d ndarray")
            log.warn(f"the {getattr(func, _Pipe_basic.Rn_ATTR, func.__name__)} need return a 2d ndarray. But got {out_data.ndim}d ndarray")
        new_data = out_data

        if new_data.ndim != 2:
            #raise ValueError(
            #    "The pipe-out ndarr must be a 2d array. If only got this msg, please turn on the warn by use warn=True to see where is wrong")
            log.error(ValueError, "The pipe-out ndarr must be a 2d array. If only got this msg, please turn on the warn by use warn=True to see where is wrong", exit=True)
        return new_data

    @staticmethod
    def test(func, data: Union[dict, np.ndarray], debug=False) -> Union[dict, np.ndarray]:
        """
        测试单个函数
        :param func:
        :param data:
        :param debug: bool, 是否开启debug模式. 开启后, 会在每次执行test函数后, 打印出目标函数的输入和输出. 并且会显示warn信息
        :return:
        """
        itype = type(data)

        if isinstance(data, dict):
            data = np.array([[data]])
        elif not isinstance(data, np.ndarray):
            # raise TypeError("The data must be a dict or a ndarray of dict {'$XXX': str}. but got {type(data)}")
            log.error(TypeError, "The data must be a dict or a ndarray of dict {'$XXX': str}. but got {type(data)}", exit=True)

        new_data = _Pipe_basic._unit(func, data, debug)

        if itype == dict:
            if new_data.shape != (1, 1) and debug:
                #warnings.warn(
                #    f"the {getattr(func, _Pipe_basic.Rn_ATTR, func.__name__)} need return a (1, 1) ndarray (because you input a dict). But got {new_data.shape} ndarray")
                log.warn(f"the {getattr(func, _Pipe_basic.Rn_ATTR, func.__name__)} need return a (1, 1) ndarray (because you input a dict). But got {new_data.shape} ndarray")
            return new_data[0, 0]
        return new_data

    def __call__(self, data: np.ndarray) -> np.array:
        """
        执行pipe, 处理2d ndarray of dict
        """
        # _unit
        for func in self.__funcs:
            data = self._unit(func, data)
        return data

    @staticmethod
    def _induce_format(input_format: dict, funcs, warn):
        """
        根据funcs中的函数, 推断出输出的格式
        :param input_format: {"$XXX":any }
        :param funcs
        :param warn: bool, 是否开启警告
        :return:
        """
        _new_format = input_format.copy()
        for func in funcs:
            fname, in_keys, out_keys, replace = _Pipe_basic._get_finfo(func)

            if in_keys is None or not isinstance(in_keys, (list, tuple)):
                log.error(TypeError, f"the {fname} must have a {_Pipe_basic.InK_ATTR} attribute", exit=True)
            if out_keys is None:
                out_keys = [_ for _ in in_keys]


            if replace:
                for k in in_keys:
                    if k not in _new_format:
                        #raise ValueError(
                        #    f"the {getattr(func, _Pipe_basic.Rn_ATTR, func.__name__)} need a key {k}, but not in last layer output format: {input_format}")
                        log.error(ValueError, f"the {fname} need a key {k}, but not in last layer output format: {input_format}", exit=True)
                    else:
                        _new_format.pop(k)
            if in_keys:
                for k in out_keys:
                    _v4 = None
                    if k in input_format:
                        _v4 = input_format[k]
                        if warn and not replace:
                            # warn
                            log.warn(f"the {fname} will overwrite the {k} in data")

                    _new_format[k] = _v4 if _v4 is not None else Vec4Zero()
            elif out_keys and warn:
                #warnings.warn(f"the {getattr(func, _Pipe_basic.Rn_ATTR, func.__name__)} will change the hole data but has out_keys. Will Ignore")
                log.warn(f"the {fname} will change the hole data but has out_keys. Will Ignore")

        return _new_format

    @property
    def input_format(self):
        """
        获取pipe的输入的格式
        :return:
        """
        return self._input_format

    @property
    def format(self):
        """
        获取pipe的输出的格式
        自动根据__funcs中的函数, 推断出输出的格式
        :return:
        """
        return self._induce_format(self._input_format, self.__funcs, self._warn)

class Pipe(_Pipe_basic):
    ...


pFunc = Pipe.Func  # 装饰器: 将目标函数装饰成一个Pipe可以直接使用的函数

if __name__ == '__main__':
    fmt = {'$a': Vec4Zero(), '$b': Vec4Zero()}
    pipe = Pipe(fmt)
    pipe.add(lambda a, b: (b, a + b), ['$a', '$b'], ['$a', '$add'])
    pipe.add(lambda a, b: a - b, ['$a', '$b'], ['$sub'])
    pipe.add(lambda a, b: a * b, ['$a', '$b'], ['$mul'])
    pipe.add(lambda a, b: a / b, ['$a', '$b'], ['$div'])
    print(pipe.format)
    # -------------------------------->
    # data:
    data = np.array([
        [{'$a': 1, '$b': 2}, {'$a': 3, '$b': 4}],
        [{'$a': 5, '$b': 6}, {'$a': 7, '$b': 8}]
    ])
    print(pipe.test(pipe.funcs[0], data, debug=False))
    exit()
    print(data, '\n----------------------------------------------------')
    odata = pipe(data)
    print(odata)
