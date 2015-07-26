#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# NetBeans:  
# New Editor Window: Im Editor auf Filenamen: New Document on Tab Group
#
# PyCharm:
# New Editor Window: ??
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
    generates a basic python program structure, that offers
    a basic file tree for logging (,testing (ToDo)) and
    initialising and the corresponding functionality.
    The generated python program may be initialised via command
    line arguments and/or configuration files.

    Pyprogen itself is easily configured via its own configuration file:
    >pyprogen.ini<. Here You configure the name of the generated python
    script (default: >y_main.py<), the extent of its logging, its the
    commandline arguments and its configuration file.

    !!! Falsch:
    commandline arguments and its configuration file. <=> pyprogen_001.conf
    !!! Falsch:

    Pyprogen uses >ConfArgParse<, a module that offers a rather
    easy way to combine command line arguments and configuration
    files.

    >ConfArgParse< is able to read and to write configuration files.
    If you want to generate a configuration file for later modification,
    add the desired options as arguments to your >ConfArgParse< - parser.
    Then call your program with the "-n --export-conf-file > y_main.cfg"
    argument and the configuration file will be written.

    The same procedure is followed by pyprogen, to produce the the
    configuration file for your >y_main.py<. Pyprogen writes firstly
    the program code for the parser >y_CAParser.py<, then executes
    >y_CAParser.py< with the "--export-conf-file > ./y_main/cfg/y_main.cfg".
    Then you will find the new >y_main.conf< for your >y_main.py<
    in the ./y_main/cfg/ dir.

    1. confargparse verstehen / ok

    2. argparse verstehen / ok

    3. howto import modules from subdirs / ok

    4. howto log / ok

    5. howto config/ini / ok
    (http://martin-thoma.com/configuration-files-in-python/)

    7.
    Ein python Program schreiben, das das ein parametrierbares Grundgeruest
    fuer Obiges (6.) erledigt, und
    zugleich eine vernuenftige Grundarchitektur fuer ein mittelgrosses
    python Programm anbietet: naemlich log-Files, configurations-files,
    paramater Uebernahme (6.) (mit einer Untermenge der cfg - Paramter),
    ein subdir in dem sich die Module befinden:
    y_main
        /cfg   # configuration
        /lib   # modules
        /log   # log

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
    p_glbls.dir_cfg = os.path.join(p_glbls.dir_cfg)

    p_glbls.dir_lib = p_utils.p_subdir_make(os.path.join(prog_path, 'lib'))
    p_glbls.dir_lib = os.path.join(p_glbls.dir_lib)

    p_glbls.dir_log = p_utils.p_subdir_make(os.path.join(prog_path, 'log'))
    p_glbls.dir_log = os.path.join('.', p_glbls.dir_log)


def copy_p_utils_p_log_init():
    """ """
    p_log_this()
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

    Then call >y_CAParser.py< via subprocess.
    Since >y_CAParser.py< is prepared to write a conf file, if called as
    script, it will write a config-file to ./y_main/cfg
    """
    p_log_this()
    p_ConfArgParser('./pyprogen_001.conf') # create confargparser for >y_main.py<
    subprocess_path  = p_glbls.CAParser_path
    p_log_this("subprocess_path = " + subprocess_path)
    cfg_fn = prog_path + '.cfg'   # cfg-file of new y_main.py
    cfg_path = os.path.join(p_glbls.dir_cfg, cfg_fn)
    p_log_this("cfg_path = " + cfg_path)
    p_glbls.cfg_fn = cfg_fn
    # http://pymotw.com/2/subprocess/
    # start new ConfArgParser to create cfg-file (aka >cfg_path<) for >y_main.py<
    subprocess.call([subprocess_path, cfg_path], shell=True)

def pyprogen():
    """
    creates basic dir-structure
    creates basic python program according to >pyprogen.conf< and .....
    """
    p_log_this()
    # "pyprogen.ini" =>>>  umbenennen nach: basic.conf oä ???
    p_code.p_read_ini(".", "pyprogen.ini")  # dir relative to >.<
    prog_path = p_glbls.prog_path # ./y_main; >y_main.py< will live here
    p_code.create_some_file_names() # i.e.: glbls_path,
    create_maindir(prog_path)     # create dir  ./y_main
    create_subdirs(prog_path)     # create dirs ./y_main/lib; ./y_main/log; ./y_main/cfg
    create_ca_parser(prog_path)   # create & start ./y_main/lib/ConfArgParser.py
    copy_p_utils_p_log_init()     # copy some utilities to ./y_main/lib
    p_code.p_main()               # create progr ./y_main/y_main.py
    p_code.p_globals()            # create modul ./y_main/lib/y_glbls.py
    p_code.p_my_code()            # create modul ./y_main/lib/y_my_code.py  == YOUR code
    p_glbls.print_p_cfg_args()    # print variables in ./pyprogen/lib/p_glbls.


if __name__ == "__main__":
    p_log_init(log_dir = 'p_log', log_fn = 'pyprogen')
    p_log_start()
    pyprogen()
    p_log_end()
    p_utils.p_exit()
