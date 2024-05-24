from xing.core.BaseThread import BaseThread


class ThreadMap(BaseThread):
    def __init__(self, fun, items, arg=None, concurrency=6):
        super(ThreadMap, self).__init__(targets=items, concurrency=concurrency)
        if not callable(fun):
            raise TypeError("fun must be callable.")

        self._arg = arg
        self._fun = fun
        self._result_map = {}

    def work(self, item):
        if self._arg:
            result = self._fun(item, self._arg)
        else:
            result = self._fun(item)

        if result:
            self._result_map[str(item)] = result

    def run(self):
        self._run()
        return self._result_map


def thread_map(fun, items, arg=None, concurrency=6):
    t = ThreadMap(fun=fun, items=items, arg=arg, concurrency=concurrency)
    return t.run()