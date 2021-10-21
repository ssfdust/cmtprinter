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
###############################################################################
#                              Filename: main.py                              #
#              Description: The entry module for comment printer              #
#                      Created Time: 2021-10-20 15:24:59                      #
#                             Created By: ssfdust                             #
#                  Last Moidified Time: 2021-10-20 15:24:59                   #
#                         Last Moidified By: ssfdust                          #
###############################################################################
# Change Log:                                                                 #
#   - Initilize.                                                              #
###############################################################################
# Functions:                                                                  #
#   - main: The program main entry                                            #
###############################################################################
"""
from argparse import ArgumentParser
from pathlib import Path

from cmtprinter.core import dump_module_nodes, parse_ast_tree, print_table


def main():
    """The program main entry"""
    parser = ArgumentParser()
    parser.add_argument("filepath", help="the target python script path")
    parser.add_argument("--desc", help="the module description.", default="")
    parser.add_argument("--tablechar", help="the char used for table drawing.", default="#")
    args = parser.parse_args()
    filepath = Path(args.filepath).expanduser().absolute()
    module_nodes = parse_ast_tree(filepath)
    data = dump_module_nodes(module_nodes)
    print_table(data, args.desc, args.tablechar)
