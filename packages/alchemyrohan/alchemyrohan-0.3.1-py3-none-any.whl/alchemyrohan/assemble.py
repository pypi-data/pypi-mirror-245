

import os
from sqlalchemy.engine import Engine

from alchemyrohan.meta_data import MetaDataHolder
from alchemyrohan.utils import is_model
from alchemyrohan.utils import is_module
from alchemyrohan.wizard import *


__all__ = ['assemble_model']


class AlchemyRohanModuleError(Exception): ...


def assemble_model(
	engine: Engine, 
	table_name: str,
    abs_os_path_to_model: str,
    py_path_to_model: str
	) -> None:
    """
    Arguments:
    
    <engine> --> Engine (sqlalchemy.engine),
    <table_name> --> Name of database table,
    <abs_os_path_to_model> --> Absolute path to the directory where are models,
    <py_path_to_model> --> Pythonic path to the models like: <program_dir.some_dir.model_dir>.

    """

    if not os.path.isdir(abs_os_path_to_model):
        raise AlchemyRohanPathError(
            f'No path: {abs_os_path_to_model}'
            )
    elif not is_module(py_path_to_model):
        raise AlchemyRohanModuleError(
            f'No Module: {py_path_to_model}'
            )
    else:

        if is_model(table_name, abs_os_path_to_model):
            return # file with model name already exist

        code_holder = generate_code(MetaDataHolder(
            engine,
            table_name
            ),
            py_path_to_model
            )

        model_template = construct_model(code_holder)

        generate_model(
            table_name,
            model_template,
            abs_os_path_to_model
            )
        
        generate_init_file(
            table_name,
            abs_os_path_to_model,
            py_path_to_model
        )




    