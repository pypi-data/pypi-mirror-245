"""
This is the implementation of the command line interface tool for the
Jac language. It's built with the Jac language via bootstraping and
represents the first such complete Jac program.
"""
from __future__ import annotations
from jaclang import jac_import as __jac_import__
from jaclang.jac.plugin.feature import JacFeature as _JacFeature
import inspect
import argparse
import cmd
__jac_import__(target='cli_impl', base_path=__file__)
from cli_impl import *
import cli_impl

@_JacFeature.make_architype('obj')
class Command:
    func: callable
    sig: inspect.Signature

    def __init__(self, func: callable) -> None:
        self.func = func
        self.sig = inspect.signature(func)

    def call(self, *args: list, **kwargs: dict) -> None:
        return self.func(*args, **kwargs)

@_JacFeature.make_architype('obj')
class CommandRegistry:
    registry: dict[str, Command]
    sub_parsers: argparse._SubParsersActionp
    parser: argparse.ArgumentParser

    def __init__(self) -> None:
        self.registry = {}
        self.parser = argparse.ArgumentParser(prog='CLI')
        self.sub_parsers = self.parser.add_subparsers(title='commands', dest='command')

    def register(self, func: callable) -> None:
        name = func.__name__
        cmd = Command(func)
        self.registry[name] = cmd
        cmd_parser = self.sub_parsers.add_parser(name)
        param_items = cmd.sig.parameters.items
        first = True
        for param_name, param in cmd.sig.parameters.items():
            if param_name == 'args':
                cmd_parser.add_argument('args', nargs=argparse.REMAINDER)
            elif param.default is param.empty:
                if first:
                    first = False
                    cmd_parser.add_argument(f'{param_name}', type=eval(param.annotation))
                else:
                    cmd_parser.add_argument(f'-{param_name[:1]}', f'--{param_name}', required=True, type=eval(param.annotation))
            elif first:
                first = False
                cmd_parser.add_argument(f'{param_name}', default=param.default, type=eval(param.annotation))
            else:
                cmd_parser.add_argument(f'-{param_name[:1]}', f'--{param_name}', default=param.default, type=eval(param.annotation))
        return func

    def get(self, name: str) -> Command:
        return self.registry.get(name)

    def items(self) -> dict[str, Command]:
        return self.registry.items()

@_JacFeature.make_architype('obj')
class CommandShell(cmd.Cmd):
    (intro): str = 'Welcome to the Jac CLI!'
    (prompt): str = 'jac> '
    cmd_reg: CommandRegistry

    def __init__(self, cmd_reg: CommandRegistry) -> None:
        self.cmd_reg = cmd_reg
        cmd.Cmd.__init__(self)

    def do_exit(self, arg: list) -> bool:
        return True

    def default(self, line: str) -> None:
        try:
            args = vars(self.cmd_reg.parser.parse_args(line.split()))
            command = self.cmd_reg.get(args['command'])
            if command:
                args.pop('command')
                ret = command.call(**args)
                if ret:
                    print(ret)
        except Exception as e:
            print(e)
cmd_registry = CommandRegistry()

def start_cli() -> None:
    parser = cmd_registry.parser
    args = parser.parse_args()
    command = cmd_registry.get(args.command)
    if command:
        args = vars(args)
        args.pop('command')
        ret = command.call(**args)
        if ret:
            print(ret)
    else:
        shell = CommandShell(cmd_registry).cmdloop()