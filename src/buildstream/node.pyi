from typing import Generic, List, Mapping, Optional, Sequence, TypeVar

from ._project import Project

TNode = TypeVar("TNode", bound="Node")
TValidNodeValue = TypeVar("TValidNodeValue", int, str, bool, Mapping, Sequence)

class ProvenanceInformation: ...

class Node:
    def clone(self) -> "Node": ...
    def get_provenance(self) -> ProvenanceInformation: ...

class MappingNode(Node, Generic[TNode]):
    def __init__(self, file_index: int, line: int, column: int, value: Mapping[str, TValidNodeValue]) -> None: ...
    def clone(self) -> MappingNode[TNode]: ...
    def get_str_list(self, key: str, default: List[str] = None) -> List[str]: ...

class ScalarNode(Node):
    def as_str(self) -> str: ...
    def clone(self) -> "ScalarNode": ...

class SequenceNode(Node, Generic[TNode]):
    def as_str_list(self) -> List[str]: ...
    def clone(self) -> "SequenceNode[TNode]": ...

def _assert_symbol_name(
    symbol_name: str, purpose: str, *, ref_node: Optional[Node] = None, allow_dashes: bool = True
) -> None: ...
def _new_synthetic_file(filename: str, project: Optional[Project] = None) -> MappingNode[TNode]: ...