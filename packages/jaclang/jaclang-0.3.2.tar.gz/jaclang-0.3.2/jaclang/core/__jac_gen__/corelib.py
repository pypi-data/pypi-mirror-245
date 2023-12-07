"""Jac's Key Elemental Abstractions"""
from __future__ import annotations
from enum import Enum as __jac_Enum__, auto as __jac_auto__
from jaclang import jac_import as __jac_import__
from jaclang.jac.plugin.feature import JacFeature as _JacFeature
from datetime import datetime
from uuid import UUID, uuid4
from jaclang.jac.constant import EdgeDir
from jaclang.jac.plugin import Architype, AbsRootHook, hookimpl
__jac_import__(target='corelib_impl', base_path=__file__)
from corelib_impl import *
import corelib_impl

class AccessMode(__jac_Enum__):
    READ_ONLY = __jac_auto__()
    READ_WRITE = __jac_auto__()
    PRIVATE = __jac_auto__()

@_JacFeature.make_architype('obj')
class Memory:
    (index): dict[UUID, Element] = {}
    (save_queue): list[Element] = []

    def get_obj(self, caller_id: UUID, item_id: UUID, override: bool=False) -> Element:
        ret = self.index.get(item_id)
        if override or ret.__is_readable(ret is not None and caller_id):
            return ret

    def has_obj(self, item_id: UUID) -> bool:
        return item_id in self.index

    def save_obj(self, caller_id: UUID, item: Element) -> None:
        if item.is_writable(caller_id):
            self.index[item.id] = item
            if item._persist:
                self.save_obj_list.add(item)
        self.mem[item.id] = item
        if item._persist:
            self.save_obj_list.add(item)

    def del_obj(self, caller_id: UUID, item: Element) -> None:
        if item.is_writable(caller_id):
            self.index.pop(item.id)
            if item._persist:
                self.save_obj_list.remove(item)

    def get_object_distribution(self) -> dict:
        dist = {}
        for i in self.index.keys():
            t = type(self.index[i])
            if t in dist:
                dist[t] += 1
            else:
                dist[t] = 1
        return dist

    def get_mem_size(self) -> float:
        return sys.getsizeof(self.index) / 1024.0

@_JacFeature.make_architype('obj')
class ExecutionContext:
    (master): Master = uuid4()
    (memory): Memory = Memory()

    def reset(self) -> None:
        self.__init__()

    def get_root(self) -> Node:
        if type(self.master) == UUID:
            self.master = Master()
        return self.master.root_node
'Global Execution Context, should be monkey patched by the user.'
exec_ctx = ExecutionContext()

@_JacFeature.make_architype('obj')
class ElementInterface:
    (jid): UUID = uuid4()
    (timestamp): datetime = datetime.now()
    (persist): bool = False
    (access_mode): AccessMode = AccessMode.PRIVATE
    (rw_access): set = set()
    (ro_access): set = set()
    (owner_id): UUID = exec_ctx.master
    (mem): Memory = exec_ctx.memory

    def make_public_ro(self) -> None:
        self.__jinfo.access_mode = AccessMode.READ_ONLY

    def make_public_rw(self) -> None:
        self.__jinfo.access_mode = AccessMode.READ_WRITE

    def make_private(self) -> None:
        self.__jinfo.access_mode = AccessMode.PRIVATE

    def is_public_ro(self) -> bool:
        return self.__jinfo.access_mode == AccessMode.READ_ONLY

    def is_public_rw(self) -> bool:
        return self.__jinfo.access_mode == AccessMode.READ_WRITE

    def is_private(self) -> bool:
        return self.__jinfo.access_mode == AccessMode.PRIVATE

    def is_readable(self, caller_id: UUID) -> bool:
        return caller_id == self.owner_id or (self.is_public_read() or (caller_id in self.ro_access or caller_id in self.rw_access))

    def is_writable(self, caller_id: UUID) -> bool:
        return caller_id == self.owner_id or (self.is_public_write() or caller_id in self.rw_access)

    def give_access(self, caller_id: UUID, read_write: bool=False) -> None:
        if read_write:
            self.rw_access.add(caller_id)
        else:
            add.ro_access.self(caller_id)

    def revoke_access(self, caller_id: UUID) -> None:
        self.ro_access.discard(caller_id)
        self.rw_access.discard(caller_id)

@_JacFeature.make_architype('obj')
class ObjectInterface(ElementInterface):
    pass

@_JacFeature.make_architype('obj')
class DataSpatialInterface(ObjectInterface):
    (ds_entry_funcs): list[dict] = []
    (ds_exit_funcs): list[dict] = []

    @staticmethod
    def on_entry(cls: type, triggers: list[type]) -> None:

        def decorator(func: callable) -> callable:
            cls.ds_entry_funcs.append({'types': triggers, 'func': func})

            def wrapper(*args: list, **kwargs: dict) -> callable:
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def on_exit(cls: type, triggers: list[type]) -> None:

        def decorator(func: callable) -> callable:
            cls.ds_exit_funcs.append({'types': triggers, 'func': func})

            def wrapper(*args: list, **kwargs: dict) -> callable:
                return func(*args, **kwargs)
            return wrapper
        return decorator

@_JacFeature.make_architype('obj')
class NodeInterface(DataSpatialInterface):
    (edges): dict[EdgeDir, list[Edge]] = {EdgeDir.IN: [], EdgeDir.OUT: []}

    def connect_node(self, nd: Node, edg: Edge) -> Node:
        edg.attach(self.py_obj, nd)
        return self

    def edges_to_nodes(self, dir: EdgeDir) -> list[Node]:
        ret_nodes = []
        if dir in [EdgeDir.OUT, EdgeDir.ANY]:
            for i in self.edges[EdgeDir.OUT]:
                ret_nodes.append(i.target)
        elif dir in [EdgeDir.IN, EdgeDir.ANY]:
            for i in self.edges[EdgeDir.IN]:
                ret_nodes.append(i.source)
        return ret_nodes

    def __call__(self, walk: Walker) -> None:
        if not isinstance(walk, Walker):
            raise TypeError('Argument must be a Walker instance')
        walk(self)

@_JacFeature.make_architype('obj')
class EdgeInterface(DataSpatialInterface):
    (source): Node = None
    (target): Node = None
    (dir): EdgeDir = None

    def apply_dir(self, dir: EdgeDir) -> Edge:
        self.dir = dir
        return self

    def attach(self, src: Node, trg: Node) -> Edge:
        if self.dir == EdgeDir.IN:
            self.source = trg
            self.target = src
            src._jac_.edges[EdgeDir.IN].append(self)
            trg._jac_.edges[EdgeDir.OUT].append(self)
        else:
            self.source = src
            self.target = trg
            src._jac_.edges[EdgeDir.OUT].append(self)
            trg._jac_.edges[EdgeDir.IN].append(self)
        return self

    def __call__(self, walk: Walker) -> None:
        if not isinstance(walk, Walker):
            raise TypeError('Argument must be a Walker instance')
        walk(self._jac_.target)

@_JacFeature.make_architype('obj')
class WalkerInterface(DataSpatialInterface):
    (path): list[Node] = []
    (next): list[Node] = []
    (ignores): list[Node] = []
    (disengaged): bool = False

    def visit_node(self, nds: list[Node] | (list[Edge] | (Node | Edge))) -> None:
        if isinstance(nds, list):
            for i in nds:
                if i not in self.ignores:
                    self.next.append(i)
        elif nds not in self.ignores:
            self.next.append(nds)
        return len(nds) if isinstance(nds, list) else 1

    def ignore_node(self, nds: list[Node] | (list[Edge] | (Node | Edge))) -> None:
        if isinstance(nds, list):
            for i in nds:
                self.ignores.append(i)
        else:
            self.ignores.append(nds)

    def disengage_now(self) -> None:
        self.next = []
        self.disengaged = True

    def __call__(self, nd: Node) -> None:
        self._jac_.path = []
        self._jac_.next = [nd]
        walker_type = self.__class__.__name__
        while len(self._jac_.next):
            nd = self._jac_.next.pop(0)
            node_type = nd.__class__.__name__
            for i in nd._jac_ds_.ds_entry_funcs:
                if i['func'].__qualname__.split('.')[0] == node_type and type(self) in i['types']:
                    i['func'](nd, self)
                if self._jac_.disengaged:
                    return
            for i in self._jac_ds_.ds_entry_funcs:
                if i['func'].__qualname__.split('.')[0] == walker_type and (type(nd) in i['types'] or nd in i['types']):
                    i['func'](self, nd)
                if self._jac_.disengaged:
                    return
            for i in self._jac_ds_.ds_exit_funcs:
                if i['func'].__qualname__.split('.')[0] == walker_type and (type(nd) in i['types'] or nd in i['types']):
                    i['func'](self, nd)
                if self._jac_.disengaged:
                    return
            for i in nd._jac_ds_.ds_exit_funcs:
                if i['func'].__qualname__.split('.')[0] == node_type and type(self) in i['types']:
                    i['func'](nd, self)
                if self._jac_.disengaged:
                    return
            self._jac_.path.append(nd)
        self._jac_.ignores = []

@_JacFeature.make_architype('obj')
class Root(AbsRootHook):
    _jac_: NodeInterface
    RootType: type

@_JacFeature.make_architype('obj')
class Master:
    (_jac_): ElementInterface = ElementInterface()
    (root_node): Root = Root(NodeInterface(), Root)

@_JacFeature.make_architype('obj')
class JacPlugin:

    @staticmethod
    def bind_architype(arch: AT, arch_type: str) -> bool:
        match arch_type:
            case 'obj':
                arch._jac_ = ObjectInterface()
            case 'node':
                arch._jac_ = NodeInterface()
            case 'edge':
                arch._jac_ = EdgeInterface()
            case 'walker':
                arch._jac_ = WalkerInterface()
            case _:
                raise TypeError('Invalid archetype type')
        return True

    @staticmethod
    def get_root() -> Architype:
        return exec_ctx.get_root()