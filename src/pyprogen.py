#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# NetBeans:  
# New Editor Window: Im Editor auf Filenamen: New Document on Tab Group
#
# PyCharm:
# New Editor Window: click on tab > Split Vertically
# ALT left/right  -> switch editor windows
# Ctrl Tab        -> list/switch editor windows
# Shift F6        -> run file
#
# Ctrl + Alt + S  -> Settings
#
# C:\Users\rh\.PyCharm40\config\colors
#     <option name="CONSOLE_BACKGROUND_KEY" value="121e31" />
# Editor Background color (HTML) :  272822  (grau-braun)
# Editor Background color (HTML) :  121e31  (blau)
#
# Filetypes association:
# File > Settings > Editor > File Types ... (ie: *.cfg like *.ini)
#
# git-credential-winstore.exe
#
# äöüÄÖÜß
#

__author__ = "rh"
__date__ = "$05.05.2015 21:55:22$"


"""
    0.
    First do a >pip install ConfArgParse< (as admin in windows)

    pyprogen:
    generates a basic python program structure, that offers a basic file
    tree for logging and initialising and the corresponding functionality.
    The generated python program may be initialised via command line
    arguments and/or configuration files (*.ini).

    y_main/y_main.py  # y_main.py == new generated python prog
        /cfg/*.cfg    # configuration files
        /lib/*.py     # some py modules; your code will reside in >my_code.py<
        /log/*.log    # log-files

    Pyprogen itself is easily configured via its own configuration file:
    >new_prog.ini<. Here You configure the name of the generated python
    script (default: >y_main.py<), the extent of its logging.
    Commandline arguments of >y_main.py< and their defaults are configured
    via >new_prog_args.conf<.

    Pyprogen uses >ConfArgParse<, to handle commandline arguments.
    This module offers a rather easy way to combine command line arguments
    and configuration files.
    >ConfArgParse< is able to read and to write configuration files.
    This ability is used by >pyprogen<: it writes firstly
    the program code for the parser >y_CAParser.py<, then executes
    >y_CAParser.py< with the "--export-conf-file > ./y_main/cfg/y_main.cfg".
    Then you will find the new >y_main.conf< for your >y_main.py<
    in the ./y_main/cfg/ dir.

    (http://martin-thoma.com/configuration-files-in-python/)


    100.
    Dark sides of py:
    py can not protect vars inside a module from being modified from outside.
    [
    module want_be_private
    var_priv = 66

    module outside
    import want_be_private
    want_be_private.var_priv = 99   !!!
    ]


    py can not prevent creating attributes to this module from outside.
    [
    module want_be_private
    var_priv = 100

    module outside
    import want_be_private
    want_be_private.var_NEW = 1 # but inside >module want_be_private< you know nothing
      about >var_NEW<!!!
    ]

"""
###

# ad pytest:

# ad decorator:
# https://pythonconquerstheuniverse.wordpress.com/2012/04/29/python-decorators/

import os
import shutil
import subprocess
import p_lib.p_glbls as p_glbls  # share global values
import p_lib.p_utils as p_utils  # utils for pyprogen
import p_lib.p_code  as p_code   # funcs generating python code
from   p_lib.p_log   import p_log_init, p_log_start, p_log_this, p_log_end
from   p_lib.p_ConfArgParser import p_ConfArgParser

def create_maindir(prog_path) :
    """ """
    p_log_this()
    p_glbls.dir_main = p_utils.p_subdir_make(prog_path)
    p_glbls.dir_main = os.path.join('.', p_glbls.dir_main)


def create_subdirs(prog_path):
    """ """
    p_log_this()
    p_glbls.dir_cfg = p_utils.p_subdir_make(os.path.join(prog_path, 'cfg'))
    p_glbls.dir_cfg = os.path.join('.', p_glbls.dir_cfg)

    p_glbls.cfg_fn = prog_path + '.cfg'   # cfg-file of new y_main.py
    p_glbls.cfg_path = os.path.join(p_glbls.dir_cfg, p_glbls.cfg_fn)

    p_glbls.dir_lib = p_utils.p_subdir_make(os.path.join(prog_path, 'lib'))
    p_glbls.dir_lib = os.path.join('.', p_glbls.dir_lib)

    p_glbls.dir_log = p_utils.p_subdir_make(os.path.join(prog_path, 'log'))
    p_glbls.dir_log = os.path.join('.', p_glbls.dir_log)


def copy_p_utils_p_log_init():
    """ """
    # dammed '__init__.py'! 2 hrs of nirwana!
    # for every file in fn_list:
    fn_list = ['p_utils.py', 'p_log.py', '__init__.py']
    for fn in fn_list:
        # create an normalize source path:
        p_utils_srce_path = os.path.join('.', 'p_lib', fn)
        p_utils_srce_path = os.path.normpath(p_utils_srce_path )
        # create an normalize destination path:
        p_utils_dest_path = os.path.join('.', p_glbls.dir_lib, fn)
        p_utils_dest_path = os.path.normpath(p_utils_dest_path )
        # copy from source to dest
        shutil.copy(p_utils_srce_path, p_utils_dest_path)
        p_log_this( fn + 'copied')


def create_ca_parser(prog_path):
    """ Writes via p_ConfArgParser() in ./y_main/lib a new
    confargparser == >y_CAParser.py< for the new program >y_main.py<.
    Configure it according to >pyprogen_XXX.conf<

    Then call >y_CAParser.py< via subprocess. Since >y_CAParser.py< is
    prepared to write a conf file, if called as script, it will write
    a config-file to ./y_main/cfg
    """
    p_log_this()
    p_ConfArgParser('./new_prog_args.conf') # create confargparser for >y_main.py<
    subprocess_path  = p_glbls.CAParser_path
    p_log_this("subprocess_path = " + subprocess_path)
    p_log_this("cfg_path = " + p_glbls.cfg_path)
    # http://pymotw.com/2/subprocess/
    # start new ConfArgParser to create cfg-file (aka >cfg_path<) for >y_main.py<
    subprocess.call([subprocess_path, p_glbls.cfg_path], shell=True)

def pyprogen():
    """
    creates basic dir-structure
    creates basic python program according to >pyprogen.conf< and .....
    """
    p_log_this()
    # "new_prog.ini" =>>>  umbenennen nach: basic.conf oä ???
    p_code.p_read_ini(".", "new_prog.ini")  # dir relative to >.<
    prog_path = p_glbls.prog_path # ./y_main; >y_main.py< will live here
    p_code.p_create_paths_and_fns() # i.e.: glbls_path,
    create_maindir(prog_path)     # create dir  ./y_main
    create_subdirs(prog_path)     # create dirs ./y_main/lib; ./y_main/log; ./y_main/cfg
    copy_p_utils_p_log_init()     # copy some utilities to ./y_main/lib
    p_code.p_main_cfg_check_hash()# check if ./y_main/y_main.cfg exists; if changed -> save it.
    create_ca_parser(prog_path)   # create & start ./y_main/lib/ConfArgParser.py
    p_code.p_main()               # create progr ./y_main/y_main.py
    p_code.p_globals()            # create modul ./y_main/lib/y_glbls.py
    p_code.p_my_code()            # create modul ./y_main/lib/y_my_code.py  == YOUR code
    # p_glbls.print_p_cfg_args()    # print variables in ./pyprogen/lib/p_glbls.
    p_code.p_main_cfg_create_hash_and_timestamp() # Do what your name says with ./y_main/cfg/y_main.cfg
    p_code.p_inform_about_paths_and_filenames()   # Do what your name says


if __name__ == "__main__":
    p_log_init(log_dir = 'p_log', log_fn = 'pyprogen')
    p_log_start()
    pyprogen()
    p_log_end()
    p_utils.p_exit()
