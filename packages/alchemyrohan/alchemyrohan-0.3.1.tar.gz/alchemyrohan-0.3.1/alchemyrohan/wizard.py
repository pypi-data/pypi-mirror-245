

import os

from alchemyrohan.meta_data import *


__all__ = [
    'generate_model',
    'generate_code',
    'generate_init_file',
    'construct_model',
    'AlchemyRohanPathError'
]   


std_imports = [
    'from sqlalchemy import Column'
]


class AlchemyRohanPathError(Exception): ...

class AlchemyRohanGenerateModelError(Exception): ...


def _write_template(
        file: str, 
        mode: str,
        template: str
        ) -> None:
    
    with open(file, mode) as f:
        f.write(template)
        f.close()


def generate_model(
    filename: str,
    model_template: str,
    abs_os_path_to_model: str
    ) -> None:

    if os.path.isdir(abs_os_path_to_model):
        file = os.path.join(
            abs_os_path_to_model, 
            filename.capitalize() + '.py'
            )
    else:
        raise AlchemyRohanPathError(
            f'No path: {abs_os_path_to_model}'
            )
    
    try:
        
        _write_template(file, 'w', model_template)

    except Exception as e:
        raise AlchemyRohanGenerateModelError(e)


def generate_code(
    table_meta_data: MetaDataHolder,
    py_path_to_model: str
    ) -> dict:

    imp = f'from {py_path_to_model} import Base'
    if imp not in std_imports:
        std_imports.append(f'from {py_path_to_model} import Base')

    code_holder = {
        'name': table_meta_data.name,
        'py_path_to_model': py_path_to_model,
        'imports': std_imports,
        'class_name': f'class {table_meta_data.name.capitalize()}(Base):',
        'table_name': f"__tablename__ = '{table_meta_data.name}'",
    }    
    
    if table_meta_data.rdbms == 'sqlite':
        
        from alchemyrohan.sqlite import read_sqlite_and_build_code

        read_sqlite_and_build_code(code_holder, table_meta_data)

    elif table_meta_data.rdbms == 'mysql':  
        
        None
        # TODO

    elif table_meta_data.rdbms == 'oracle':  
        
        from alchemyrohan.oracle import read_oracle_and_build_code

        read_oracle_and_build_code(code_holder, table_meta_data)
    
    else:
        raise AlchemyRohanDatabaseError(
            f'No supported dialect: {table_meta_data.rdbms}'
            )

    return code_holder


def construct_model(
    code_holder: dict
    ) -> str:

    def _add(tmp_list):
        for e in tmp_list:
            yield e

    BACKSLASH = '\n'

    template = f"""

{f'{BACKSLASH}'.join(_add(code_holder['imports']))}


{code_holder['class_name']}
    {code_holder['table_name']}

{''.join(_add(code_holder['columns']))}

{''.join(_add(code_holder['relations']))}

    def __post_init__(self):
{''.join(code_holder['validations'])}
    
    def __str__(self):
{code_holder['str_print']}
"""
    
    return template


def generate_init_file(
    table_name: str,
    abs_os_path_to_model: str,
    py_path_to_model: str
    ) -> None:

    file = os.path.join(
        abs_os_path_to_model, 
        '__init__.py'
        )

    if os.path.isfile(file):
        
        model_name = table_name.capitalize()
        template = f'\nfrom {py_path_to_model}.{model_name} import {model_name}'

        _write_template(file, 'a', template)

    else:

        model_name = table_name.capitalize()

        template = f"""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from {py_path_to_model}.{model_name} import {model_name}
"""
        
        _write_template(file, 'w', template)
