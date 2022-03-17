import datetime
import typing
import json

import pydantic

def dictify(class_orig):
    def to_dict(self) -> typing.Dict[str, typing.Any]:
        if "__fields__" in class_orig.__dict__:
            _variables = class_orig.__dict__["__fields__"]
        elif "__annotations__" in class_orig.__dict__:
            _variables = class_orig.__dict__["__annotations__"]
        else:
            return str(class_orig)
        _out_dict: typing.Dict[str, typing.Any] = {}
        for variable in _variables:
            try:
                json.dumps(getattr(self, variable))
                _out_dict[variable] = getattr(self, variable)
            except TypeError:
                if isinstance(getattr(self, variable), dict):
                    _out_dict[variable] = {}
                    for key, value in getattr(self, variable).items():
                        try:
                            json.dumps(value)
                            _out_dict[variable][key] = value
                        except TypeError as e:
                            _out_dict[variable][key] = value.to_dict()
                else:
                    try:
                        _out_dict[variable] = getattr(self, variable).to_dict()
                    except AttributeError:
                        _out_dict[variable] = str(getattr(self, variable))
        return _out_dict
    class_orig.to_dict = to_dict
    return class_orig

