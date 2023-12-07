_NewBase_banned_keywords_secret_var_jsonr_python = [
    '_NewBase_json_secret_var_jsonr_python',
    '_NewBase_args_secret_var_jsonr_python',
    '_NewBase_kwargs_secret_var_jsonr_python',
    '_NewBase_auto_unique_secret_var_jsonr_python',
    '_NewBase_limit_secret_var_jsonr_python'
]

class NewBase:
    def __init__(self, auto=False, limit=None, *args, **kwargs):
        if auto:
            for key, value in kwargs.items():
                setattr(self, key, value)

        self._NewBase_json_secret_var_jsonr_python = {**kwargs}
        self._NewBase_args_secret_var_jsonr_python = args
        self._NewBase_kwargs_secret_var_jsonr_python = kwargs

        self._NewBase_auto_unique_secret_var_jsonr_python = auto
        self._NewBase_limit_secret_var_jsonr_python = limit

    def _trim(self):
        if self._NewBase_limit_secret_var_jsonr_python is not None:
            self._NewBase_json_secret_var_jsonr_python = dict(list(self._NewBase_json_secret_var_jsonr_python.items())[:self._NewBase_limit_secret_var_jsonr_python])
        return self._NewBase_json_secret_var_jsonr_python

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name not in _NewBase_banned_keywords_secret_var_jsonr_python: self._NewBase_json_secret_var_jsonr_python[name] = value

    def __delattr__(self, name):
        super().__delattr__(name)
        if name not in _NewBase_banned_keywords_secret_var_jsonr_python: del self._NewBase_json_secret_var_jsonr_python[name]

    def __getattr__(self, name):
        return super().__getattr__(name)

    def __class_getitem__(cls, item):
        return item

    def __repr__(self):
        return self._NewBase_json_secret_var_jsonr_python

    def __len__(self):
        return len(self._NewBase_json_secret_var_jsonr_python)

    def __getitem__(self, key):
        return self._NewBase_json_secret_var_jsonr_python[key]

    def __setitem__(self, key, value):
        self._NewBase_json_secret_var_jsonr_python[key] = value
        if self._NewBase_auto_unique_secret_var_jsonr_python:
            setattr(self, key, value)

        self._trim()

    def __delitem__(self, key):
        del self._NewBase_json_secret_var_jsonr_python[key]

    def __contains__(self, key):
        return key in self._NewBase_json_secret_var_jsonr_python

    def __iter__(self):
        return iter(self._NewBase_json_secret_var_jsonr_python)

    def __reversed__(self):
        return reversed(self._NewBase_json_secret_var_jsonr_python)

    def __eq__(self, other):
        return self._NewBase_json_secret_var_jsonr_python == other

    def __ne__(self, other):
        return self._NewBase_json_secret_var_jsonr_python != other

    def __lt__(self, other):
        return len(self._NewBase_json_secret_var_jsonr_python) < other

    def __le__(self, other):
        return len(self._NewBase_json_secret_var_jsonr_python) <= other

    def __gt__(self, other):
        return len(self._NewBase_json_secret_var_jsonr_python) > other

    def __ge__(self, other):
        return len(self._NewBase_json_secret_var_jsonr_python) >= other

    def __add__(self, other):
        if self._NewBase_auto_unique_secret_var_jsonr_python:
            try:
                self._NewBase_json_secret_var_jsonr_python = {**self._NewBase_json_secret_var_jsonr_python, **other}
                self._trim()
                
                for key, value in other.items():
                    setattr(self, key, value)
            except:
                return self.__len__() + other
        return self._NewBase_json_secret_var_jsonr_python

    def __iadd__(self, other):
        return self.__add__()

    def __sub__(self, other):
        try:
            for key in other:
                del self._NewBase_json_secret_var_jsonr_python[key]
        except:
            return self.__len__() - other
        return self._NewBase_json_secret_var_jsonr_python

    def __isub__(self, other):
        return self.__sub__()

    def __mul__(self, other):
        try:
            self._NewBase_json_secret_var_jsonr_python = {**self._NewBase_json_secret_var_jsonr_python, **other}
            self._trim()
            
            for key, value in other.items():
                setattr(self, key, value)
        except:
            return self.__len__() * other
        return self._NewBase_json_secret_var_jsonr_python

    def __imul__(self, other):
        return self.__mul__()

    def __truediv__(self, other):
        try:
            for key, value in other.items():
                del (self, key, value)
        except:
            return self.__len__() / other
        return self._NewBase_json_secret_var_jsonr_python

    def __itruediv__(self, other):
        return self.__truediv__()

    def __floordiv__(self, other):
        try:
            self._NewBase_json_secret_var_jsonr_python = {**self._NewBase_json_secret_var_jsonr_python, **other}
            self._trim()
            
            for key, value in other.items():
                delattr(self, key, value)
        except:
            return self.__len__() // other
        return self._NewBase_json_secret_var_jsonr_python

    def __ifloordiv__(self, other):
        return self.__floordiv__()

    def __mod__(self, other):
        try:
            self._NewBase_json_secret_var_jsonr_python = {**self._NewBase_json_secret_var_jsonr_python, **other}
            self._trim()
            
            for key, value in other.items():
                delattr(self, key, value)
        except:
            return self.__len__() % int(other)
        return self._NewBase_json_secret_var_jsonr_python

    def __imod__(self, other):
        return self.__mod__()

    def __pow__(self, other):
        try:
            self._NewBase_json_secret_var_jsonr_python = {**self._NewBase_json_secret_var_jsonr_python, **other}
            self._trim()
            
            for key, value in other.items():
                setattr(self, key, value)
        except:
            return self.__len__() ** int(other)
        return self._NewBase_json_secret_var_jsonr_python

    def __ipow__(self, other):
        return self.__pow__()

    def __lshift__(self, other):
        return self.__len__() << other

    def __ilshift__(self, other):
        return self.__len__() << other

    def __rshift__(self, other):
        return self.__len__() >> other

    def __irshift__(self, other):
        return self.__len__() >> other

    def __and__(self, other):
        return self.__len__() & other

    def __iand__(self, other):
        return self.__len__() & other

    def __xor__(self, other):
        return self.__len__() ^ other

    def __ixor__(self, other):
        return self.__len__() ^ other

    def __or__(self, other):
        return self.__len__() | other

    def __ior__(self, other):
        return self.__len__() | other

    def __neg__(self):
        return -self.__len__()

    def __pos__(self):
        return +self.__len__()

    def __abs__(self):
        return abs(self.__len__())

    def __invert__(self):
        return ~self.__len__()

    def __str__(self):
        return str(self.__repr__())

    def __int__(self):
        return int(self.__len__())

    def __float__(self):
        return float(self.__len__())

    def __complex__(self):
        return complex(self.__len__())

    def __round__(self):
        return round(self.__len__())

    def __trunc__(self):
        return trunc(self.__len__())

    def __floor__(self):
        return floor(self.__len__())

    def __ceil__(self):
        return ceil(self.__len__())

    def __call__(self, *args, **kwargs):
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return (f'jsonr.exit <exc_type: {exc_type}, exc_value: {exc_value}, traceback: {traceback}>')
