"""Jac's Key Elemental Abstractions"""
from __future__ import annotations
from enum import Enum as __jac_Enum__, auto as __jac_auto__
import sys
from uuid import UUID, uuid4
from jaclang.jac.constant import EdgeDir
from jaclang.jac.plugin import hookimpl

def o_Memory_c_get_obj(self, caller_id: UUID, item_id: UUID, override: bool=False) -> Element:
    ret = self.index.get(item_id)
    if override or ret.__is_readable(ret is not None and caller_id):
        return ret

def o_Memory_c_has_obj(self, item_id: UUID) -> bool:
    return item_id in self.index

def o_Memory_c_save_obj(self, caller_id: UUID, item: Element) -> None:
    if item.is_writable(caller_id):
        self.index[item.id] = item
        if item._persist:
            self.save_obj_list.add(item)
    self.mem[item.id] = item
    if item._persist:
        self.save_obj_list.add(item)

def o_Memory_c_del_obj(self, caller_id: UUID, item: Element) -> None:
    if item.is_writable(caller_id):
        self.index.pop(item.id)
        if item._persist:
            self.save_obj_list.remove(item)

def o_Memory_c_get_object_distribution(self) -> dict:
    dist = {}
    for i in self.index.keys():
        t = type(self.index[i])
        if t in dist:
            dist[t] += 1
        else:
            dist[t] = 1
    return dist

def o_Memory_c_get_mem_size(self) -> float:
    return sys.getsizeof(self.index) / 1024.0

def o_ExecutionContext_c_get_root(self) -> None:
    if type(self.master) == UUID:
        self.master = Master()
    return self.master.root_node

def o_ExecutionContext_c_reset(self) -> None:
    self.__init__()

class e_AccessMode(__jac_Enum__):
    READ_ONLY = __jac_auto__()
    READ_WRITE = __jac_auto__()
    PRIVATE = __jac_auto__()

def o_ElementInterface_c_make_public_ro(self) -> None:
    self.__jinfo.access_mode = AccessMode.READ_ONLY

def o_ElementInterface_c_make_public_rw(self) -> None:
    self.__jinfo.access_mode = AccessMode.READ_WRITE

def o_ElementInterface_c_make_private(self) -> None:
    self.__jinfo.access_mode = AccessMode.PRIVATE

def o_ElementInterface_c_is_public_ro(self) -> bool:
    return self.__jinfo.access_mode == AccessMode.READ_ONLY

def o_ElementInterface_c_is_public_rw(self) -> bool:
    return self.__jinfo.access_mode == AccessMode.READ_WRITE

def o_ElementInterface_c_is_private(self) -> bool:
    return self.__jinfo.access_mode == AccessMode.PRIVATE

def o_ElementInterface_c_is_readable(self, caller_id: UUID) -> bool:
    return caller_id == self.owner_id or (self.is_public_read() or (caller_id in self.ro_access or caller_id in self.rw_access))

def o_ElementInterface_c_is_writable(self, caller_id: UUID) -> bool:
    return caller_id == self.owner_id or (self.is_public_write() or caller_id in self.rw_access)

def o_ElementInterface_c_give_access(self, caller_id: UUID, read_write: bool=False) -> None:
    if read_write:
        self.rw_access.add(caller_id)
    else:
        add.ro_access.self(caller_id)

def o_ElementInterface_c_revoke_access(self, caller_id: UUID) -> None:
    self.ro_access.discard(caller_id)
    self.rw_access.discard(caller_id)

def o_DataSpatialInterface_c_on_entry(cls: type, triggers: list) -> None:

    def decorator(func: callable) -> callable:
        cls.ds_entry_funcs.append({'types': triggers, 'func': func})

        def wrapper(*args: list, **kwargs: dict) -> callable:
            return func(*args, **kwargs)
        return wrapper
    return decorator

def o_DataSpatialInterface_c_on_exit(cls: type, triggers: list) -> None:

    def decorator(func: callable) -> callable:
        cls.ds_exit_funcs.append({'types': triggers, 'func': func})

        def wrapper(*args: list, **kwargs: dict) -> callable:
            return func(*args, **kwargs)
        return wrapper
    return decorator

def o_NodeInterface_c_connect_node(self, nd: Node, edg: Edge) -> Node:
    edg.attach(self.py_obj, nd)
    return self

def o_NodeInterface_c_edges_to_nodes(self, dir: EdgeDir) -> list[Node]:
    ret_nodes = []
    if dir in [EdgeDir.OUT, EdgeDir.ANY]:
        for i in self.edges[EdgeDir.OUT]:
            ret_nodes.append(i.target)
    elif dir in [EdgeDir.IN, EdgeDir.ANY]:
        for i in self.edges[EdgeDir.IN]:
            ret_nodes.append(i.source)
    return ret_nodes

def o_EdgeInterface_c_apply_dir(self, dir: EdgeDir) -> Edge:
    self.dir = dir
    return self

def o_EdgeInterface_c_attach(self, src: Node, trg: Node) -> Edge:
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

def o_WalkerInterface_c_visit_node(self, nds: list[Node] | (list[Edge] | (Node | Edge))) -> None:
    if isinstance(nds, list):
        for i in nds:
            if i not in self.ignores:
                self.next.append(i)
    elif nds not in self.ignores:
        self.next.append(nds)
    return len(nds) if isinstance(nds, list) else 1

def o_WalkerInterface_c_ignore_node(self, nds: list[Node] | (list[Edge] | (Node | Edge))) -> None:
    if isinstance(nds, list):
        for i in nds:
            self.ignores.append(i)
    else:
        self.ignores.append(nds)

def o_WalkerInterface_c_disengage_now(self) -> None:
    self.next = []
    self.disengaged = True

def o_NodeInterface_c___call__(self, walk: Walker) -> None:
    if not isinstance(walk, Walker):
        raise TypeError('Argument must be a Walker instance')
    walk(self)

def o_EdgeInterface_c___call__(self, walk: Walker) -> None:
    if not isinstance(walk, Walker):
        raise TypeError('Argument must be a Walker instance')
    walk(self._jac_.target)

def o_WalkerInterface_c___call__(self, nd: Node) -> None:
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

@hookimpl
def o_JacPlugin_c_bind_architype(arch: AT, arch_type: str) -> bool:
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

@hookimpl
def o_JacPlugin_c_get_root() -> None:
    return exec_ctx.get_root()