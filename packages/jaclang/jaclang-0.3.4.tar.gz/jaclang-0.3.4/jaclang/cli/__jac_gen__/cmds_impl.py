"""Implementations for the jac command line interface."""
from __future__ import annotations
from jaclang import jac_import as __jac_import__
from jaclang.jac.plugin.feature import JacFeature as _JacFeature
import os
import shutil
import unittest
from jaclang.jac.constant import Constants as C

def c_run(filename: str, main: bool=True) -> None:
    if filename.endswith('.jac'):
        [base, mod] = os.path.split(filename)
        base = './' if not base else base
        mod = mod[:-4]
        __jac_import__(target=mod, base_path=base, override_name='__main__' if main else None)
    else:
        print('Not a .jac file.')

def c_enter(filename: str, entrypoint: str, args: list) -> None:
    if filename.endswith('.jac'):
        [base, mod] = os.path.split(filename)
        base = './' if not base else base
        mod = mod[:-4]
        mod = __jac_import__(target=mod, base_path=base)
        if not mod:
            print('Errors occured while importing the module.')
            return
        else:
            getattr(mod, entrypoint)()
    else:
        print('Not a .jac file.')

def c_test(filename: str) -> None:
    if filename.endswith('.jac'):
        [base, mod] = os.path.split(filename)
        base = './' if not base else base
        mod = mod[:-4]
        mod = __jac_import__(target=mod, base_path=base)
        unittest.TextTestRunner().run(mod.__jac_suite__)
    else:
        print('Not a .jac file.')

def c_ast_tool(tool: str, args: list) -> None:
    from jaclang.utils.lang_tools import AstTool
    if hasattr(AstTool, tool):
        try:
            if len(args):
                print(getattr(AstTool(), tool)(args))
            else:
                print(getattr(AstTool(), tool)())
        except Exception:
            print(f'Error while running ast tool {tool}, check args.')
    else:
        print(f'Ast tool {tool} not found.')

def c_clean() -> None:
    current_dir = os.getcwd()
    py_cache = '__pycache__'
    for root, dirs, files in os.walk(current_dir, topdown=True):
        for folder_name in dirs[:]:
            if folder_name == C.JAC_GEN_DIR or folder_name == py_cache:
                folder_to_remove = os.path.join(root, folder_name)
                shutil.rmtree(folder_to_remove)
                print(f'Removed folder: {folder_to_remove}')
    print('Done cleaning.')