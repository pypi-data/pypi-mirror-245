

import os
import importlib

from typing import Type
from sqlalchemy.ext.declarative import DeclarativeMeta

from alchemyrohan.meta_data import MetaDataHolder


__all__ = [
    'is_model',
    'is_module',
    'get_model',
    'reload_module'
    ]


def str_print(
    code_holder: dict, 
    table_meta_data: MetaDataHolder
    ) -> None:

    tmp = []
    a = "f'User("
    for c in table_meta_data.columns:
        tmp.append(f"{c['name']}={{self.{c['name']}}}")
    b = ",'\\\n\t\t\tf'".join(tmp)
    c = ")'"
    d = a + b + c
    txt = f"""
        return {d}
"""
    
    code_holder.update({'str_print': txt})


def is_model(
    table_name: str,
    abs_os_path_to_model: str,
    ) -> bool:

    if os.path.isfile(os.path.join(
            abs_os_path_to_model, 
            table_name.capitalize() + '.py'
            )):
        return True
    else:
        return False
    

def is_module(
    py_path_to_model: str
    ) -> bool:

    try:
        importlib.import_module(py_path_to_model)
        return True
    except:
        return False


def reload_module(
    py_path_to_model: object
    ) -> None:

    importlib.reload(py_path_to_model)


def get_model(
    table_name: str,
    py_path_to_model: str
    ) -> Type[DeclarativeMeta] or None:

    module = importlib.import_module(
        f'{py_path_to_model}.{table_name.capitalize()}')
    
    if hasattr(module, table_name.capitalize()):
        return getattr(module, table_name.capitalize())
    else:
        return None
