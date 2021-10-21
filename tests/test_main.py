from pathlib import Path

from cmtprinter.core import dump_module_nodes, parse_ast_tree, print_table


def test_parse_ast_tree(simple_py_script: Path) -> None:
    module_nodes = parse_ast_tree(simple_py_script)
    data = dump_module_nodes(module_nodes)
    print_table(data)
