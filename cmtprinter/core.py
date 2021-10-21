# Copyright 2021 RedLotus <ssfdust@gmail.com>
# Author: RedLotus <ssfdust@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
*******************************************************************************
*                              Filename: core.py                              *
*                 Description: The core module for cmtprinter                 *
*                      Created Time: 2021-10-21 14:33:47                      *
*                             Created By: ssfdust                             *
*                  Last Moidified Time: 2021-10-21 14:33:47                   *
*                         Last Moidified By: ssfdust                          *
*******************************************************************************
* Change Log:                                                                 *
*   - Initilize.                                                              *
*-----------------------------------------------------------------------------*
* Functions:                                                                  *
*   - parse_ast_tree: extract functions and classes from python script.       *
*   - dump_module_nodes: convert the ModuleNodes class into a dictionary,     *
*     which means dumping.                                                    *
*   - print_table: Print the information from the dumped node json.           *
*-----------------------------------------------------------------------------*
* Classes:                                                                    *
*   - DumpedModuleNodes: A typed dict class for dumped ModuleNodes class.     *
*   - ModuleNodes: The data class with parsed ast tree data.                  *
*-----------------------------------------------------------------------------*
"""
import ast
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import cjkwrap
from typing import Optional, TypedDict

import git
from texttable import Texttable


class DumpedModuleNodes(TypedDict):
    """A typed dict class for dumped ModuleNodes class.

    Attributes:
        filename: the filename of source file.
        functions: the public function names in source file.
        classes: the public class names in source file.
        created: the created time of the source file
        modified: the modified time of the source file
    """

    filename: str
    created: str
    modified: str
    functions: str
    classes: str


@dataclass
class ModuleNodes:
    """The data class with parsed ast tree data.

    Attributes:
        filename: the filename of source file.
        functions: the public function names in source file.
        classes: the public class names in source file.
    """

    filename: str
    created: datetime
    modified: datetime
    classes: list[str] = field(default_factory=list)
    funces: list[str] = field(default_factory=list)


def parse_ast_tree(py_script_path: Path) -> ModuleNodes:
    """extract functions and classes from python script.

    This function will try to extract all the ast nodes from python source file
    and gather all the class and function definitions into the ModuleNodes
    class.

    Args:
        py_script_path: the source file path

    Return:
        The ModuleNodes class with gathered information.
    """
    file_stat = py_script_path.stat()
    module_nodes = ModuleNodes(
        py_script_path.name,
        created=datetime.fromtimestamp(file_stat.st_ctime),
        modified=datetime.fromtimestamp(file_stat.st_mtime),
    )
    src_code = py_script_path.read_text()
    astmodule = ast.parse(src_code)
    nodes = ast.NodeVisitor()
    for node in ast.walk(astmodule):
        ast_dumps = ast.dump(node)
        if ast_dumps.startswith("ClassDef"):
            _generate_def_item(node, module_nodes.classes)
        elif ast_dumps.startswith("FunctionDef"):
            _generate_def_item(node, module_nodes.funces)
    return module_nodes


def _generate_def_item(node: ast.AST, store: list[str]) -> None:
    docstring = _get_the_first_not_empty_line(
        ast.get_docstring(node)
    )
    desc = "{}: {}".format(node.name, docstring)
    if not node.name.startswith("_"):
        desc = f"{desc:70}"
        for i in cjkwrap.wrap(
            desc,
            width=70,
            initial_indent="- ",
            subsequent_indent="  ",
        ):
            store.append(i)


def _get_the_first_not_empty_line(data: Optional[str]) -> str:
    if not data:
        return ""
    for line in data.split("\n"):
        if line:
            return line
    return ""


def dump_module_nodes(
    module_nodes: ModuleNodes, indent: int = 2
) -> DumpedModuleNodes:
    """convert the ModuleNodes class into a dictionary, which means dumping.

    Args:
        module_nodes: the ModuleNodes with parsed ast tree information.
        indent: the indent for each line.

    Returns:
        The dumped dictionary corresponding to ModuleNodes class.
    """
    node_json = {"filename": "", "functions": "", "classes": ""}
    for items, key, header in [
        (module_nodes.classes, "classes", "Classes:\n"),
        (module_nodes.funces, "functions", "Functions:\n"),
    ]:
        if len(items) > 0:
            node_json[key] += header
            for name in items:
                node_json[key] += " " * indent + f"{name}\n"
    node_json["filename"] = module_nodes.filename
    node_json["created"] = module_nodes.created.strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    node_json["modified"] = module_nodes.modified.strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    return node_json


def print_table(node_json: DumpedModuleNodes, desc: str, tablechar: str) -> None:
    """Print the information from the dumped node json.

    Args:
        node_json: The dumped dictionary corresponding to ModuleNodes class.
        desc: the short description for the module.
        tablechar: the character used for drawing a table.
    """
    data = [
        [node_json[key].strip()]
        for key in ["functions", "classes"]
        if node_json[key]
    ]
    globalconfig = git.GitConfigParser(
        [os.path.normpath(os.path.expanduser("~/.gitconfig"))],
        read_only=True,
    )
    username = globalconfig.get("user", "name")
    baseinfo = "Filename: {}\n".format(node_json["filename"])
    if desc:
        baseinfo += "Description: {}\n".format(desc)
    baseinfo += "Created Time: {}\n".format(node_json["modified"])
    baseinfo += "Created By: {}\n".format(username)
    baseinfo += "Last Moidified Time: {}\n".format(node_json["modified"])
    baseinfo += "Last Moidified By: {}".format(username)
    changelog = "Change Log: \n  - Initilize."
    data.insert(0, [changelog])
    data.insert(0, [baseinfo])

    table = Texttable()
    table.set_cols_width([75])
    table.set_chars(['-'] + [tablechar] * 3)
    table.add_rows(data)
    table_text = _redraw_the_header_line(table.draw(), tablechar)
    print(table_text)


def _redraw_the_header_line(table_text: str, tablechar: str) -> str:
    linecnt = 0
    new_table_text_list = []
    for line in table_text.splitlines():
        if line:
            linecnt += 1
            if linecnt == 1:
                line = tablechar * len(line)
            new_table_text_list.append(line)
    return "\n".join(new_table_text_list)
