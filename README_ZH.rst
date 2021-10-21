Module Comment Generator
============================

之前看到 `红警
<https://github.com/electronicarts/CnC_Remastered_Collection/blob/master/REDALERT/2KEYFRAM.CPP>`_ 的代码注释，感觉真的很好看，就做了一个这种风格注释生成器。

注释生成器会解析Python代码的AST，提取其中的函数与类的定义以及Docstring，以及git信息，来生成一张表格。暂时应该只在Archlinux上测试通过，如果windows上有问题，欢迎提交issue或者PR。

使用
---------------------------
============
帮助
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

1. 描述(desc): 用于显示在 ``Description`` 栏目的内容，默认为空
2. 表格符(tablechar): 设定绘制表格的字符默认为 ``#``

============
示例
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
