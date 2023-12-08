"""
This is the implementation of the command line interface tool for the
Jac language. It's built with the Jac language via bootstraping and
represents the first such production Jac program.
"""
from __future__ import annotations
from jaclang import jac_import as __jac_import__
from jaclang.jac.plugin.feature import JacFeature as _JacFeature
__jac_import__(target='cli', base_path=__file__)
from cli import cmd_registry as cmd_reg
__jac_import__(target='cmds_impl', base_path=__file__)
from cmds_impl import *
import cmds_impl

@cmd_reg.register
def run(filename: str, main: bool=True) -> None:
    if filename.endswith('.jac'):
        [base, mod] = os.path.split(filename)
        base = './' if not base else base
        mod = mod[:-4]
        __jac_import__(target=mod, base_path=base, override_name='__main__' if main else None)
    else:
        print('Not a .jac file.')

@cmd_reg.register
def enter(filename: str, entrypoint: str, args: list) -> None:
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

@cmd_reg.register
def test(filename: str) -> None:
    if filename.endswith('.jac'):
        [base, mod] = os.path.split(filename)
        base = './' if not base else base
        mod = mod[:-4]
        mod = __jac_import__(target=mod, base_path=base)
        unittest.TextTestRunner().run(mod.__jac_suite__)
    else:
        print('Not a .jac file.')

@cmd_reg.register
def ast_tool(tool: str, args: list=[]) -> None:
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

@cmd_reg.register
def clean() -> None:
    current_dir = os.getcwd()
    py_cache = '__pycache__'
    for root, dirs, files in os.walk(current_dir, topdown=True):
        for folder_name in dirs[:]:
            if folder_name == C.JAC_GEN_DIR or folder_name == py_cache:
                folder_to_remove = os.path.join(root, folder_name)
                shutil.rmtree(folder_to_remove)
                print(f'Removed folder: {folder_to_remove}')
    print('Done cleaning.')