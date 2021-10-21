Module Comment Generator
============================

The comment style is as a tribute to the comment from the `RA
<https://github.com/electronicarts/CnC_Remastered_Collection/blob/master/REDALERT/2KEYFRAM.CPP>`_ .

The comment generator can parse the ast tree from the python script, then extract docstring from classes and functions. The information about user comes from git config. There could be some problems on windows, because it's only tested on arch linux. Issues or PR are welcome.

Usage
---------------------------
============
Help Info
============
::

    usage: cmtprinter [-h] [--desc DESC] [--tablechar TABLECHAR] filepath

    positional arguments:
      filepath              the target python script path

    optional arguments:
      -h, --help            show this help message and exit
      --desc DESC           the module description.
      --tablechar TABLECHAR
                            the char used for table drawing.

1. Description(desc): the content filled in ``Description`` key，default is empty.
2. Tbla(tablechar): the char used for table drawing, default is ``#``

============
Example
============
::

    cmtprinter ./cmtprinter/core.py --desc "The entry module for comment printer"
    ###############################################################################
    #                              Filename: core.py                              #
    #              Description: The entry module for comment printer              #
    #                      Created Time: 2021-10-20 15:21:06                      #
    #                             Created By: ssfdust                             #
    #                  Last Moidified Time: 2021-10-20 15:21:06                   #
    #                         Last Moidified By: ssfdust                          #
    ###############################################################################
    # Change Log:                                                                 #
    #   - Initilize.                                                              #
    ###############################################################################
    # Functions:                                                                  #
    #   - parse_ast_tree: extract functions and classes from python script.       #
    #   - dump_module_nodes: convert the ModuleNodes class into a dictionary,     #
    #     which means dumping.                                                    #
    #   - print_table: Print the information from the dumped node json.           #
    ###############################################################################
    # Classes:                                                                    #
    #   - DumpedModuleNodes: A typed dict class for dumped ModuleNodes class.     #
    #   - ModuleNodes: The data class with parsed ast tree data.                  #
    ###############################################################################
