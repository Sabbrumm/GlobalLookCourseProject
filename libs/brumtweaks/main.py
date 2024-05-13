import json
import warnings

from pydantic import BaseModel


def struct(cls):
    def fxn():
        warnings.warn("user", UserWarning)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        class NewClass(BaseModel, cls):
            pass

        def to_json(self):
            return self.model_dump_json()

        def from_json(release_json:str|dict):
            if isinstance(release_json, str):
                release_json = json.loads(release_json)
            assert isinstance(release_json, dict), "Json must be a string or a dict"
            return NewClass(**release_json)


        NewClass.__name__ = cls.__name__
        NewClass.__qualname__ = cls.__qualname__
        NewClass.__module__ = cls.__module__

        setattr(cls, "from_json", staticmethod(from_json))
        setattr(cls, "to_json", to_json)


        return NewClass