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
# äöüÄÖÜß
#

__author__ = "rh"
__date__ = "$05.05.2015 21:55:22$"


"""
    0.

    Do a >pip install ConfArgParse< (as admin in windows)


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
    in the ./y_main/cfg/ dir.  ,mnb

    1. confargparse verstehen / ok

    2. argparse verstehen / ok

    3. howto import modules from subdirs / ok

    4. howto log / ok

    5.  howto config/ini / ok
    (http://martin-thoma.com/configuration-files-in-python/)

    6. python program schreiben, das als Input ein paar Parameter hat ...

    7.
    Ein python Program schreiben, das das ein parametrierbares Grundgeruest
    fuer Obiges (6.) erledigt, und
    zugleich eine vernuenftige Grundarchitektur fuer ein mittelgrosses
    python Programm anbietet: naemlich log-Files, configurations-files,
    paramater Uebernahme (6.) (mit einer Untermenge der cfg - Paramter),
    ein subdir in dem sich die Module befinden:
    y_main
        /cfg   # Konfiguration
        /lib   # Moduls
        /log   # Log

"""
###

# ad pytest:

# ad decorator:
# https://pythonconquerstheuniverse.wordpress.com/2012/04/29/python-decorators/

import os
import subprocess
import p_utils.p_glbls as p_glbls  # share global values
import p_utils.p_utils as p_utils
from   p_utils.p_utils import p_read_ini
from   p_utils.p_log   import p_log_init, p_log_start, p_log_this, p_log_end
from   p_utils.p_ConfArgParser import p_ConfArgParser

def create_maindir(dir_name):
    """ """
    p_log_this()
    p_glbls.dir_main = p_utils.p_subdir_make(dir_name)
    p_glbls.dir_main = os.path.join('.', p_glbls.dir_main)

def create_subdirs(prog_name):
    """ """
    p_log_this()
    p_glbls.dir_cfg = p_utils.p_subdir_make(os.path.join(prog_name, 'cfg'))
    p_glbls.dir_cfg = os.path.join('.', p_glbls.dir_cfg)

    p_glbls.dir_lib = p_utils.p_subdir_make(os.path.join(prog_name, 'lib'))
    p_glbls.dir_lib = os.path.join('.', p_glbls.dir_lib)

    p_glbls.dir_log = p_utils.p_subdir_make(os.path.join(prog_name, 'log'))
    p_glbls.dir_log = os.path.join('.', p_glbls.dir_log)

def create_ca_parser(prog_name):
    """ Writes via p_ConfArgParser() in ./y_main/lib a new
    confargparser == >y_CAParser.py< for the new program >y_main.py<.
    Configure it according to >pyprogen_XXX.conf<

    Then call >y_CAParser.py< via subprocess.
    Since >y_CAParser.py< is prepared to write a conf file, if called as
    script, it will write a config-file to ./y_main/cfg
    """
    p_log_this()
    p_ConfArgParser('./pyprogen_001.conf') # create confargparser for >y_main.py<
    loc_path = os.getcwd()
    #print loc_path
    #subprocess_path  = os.path.join(loc_path, p_glbls.CAParser_path)
    subprocess_path  = p_glbls.CAParser_path
    p_log_this("subprocess_path = " + subprocess_path)
    p_glbls.cfg_fn = prog_name + '.cfg'   # cfg-file of new y_main.py
    cfg_path = os.path.join(p_glbls.dir_cfg, p_glbls.cfg_fn)
    p_log_this("cfg_path = " + cfg_path)
    # http://pymotw.com/2/subprocess/
    # start new ConfArgParser to create cfg-file for >y_main.py<
    subprocess.call([subprocess_path, cfg_path], shell=True)

def create_main():
    """
    writes new y_main.py
    """
    p_log_this()
    p_utils.p_main()
    # print 'p_glbls.dir_main = ', p_glbls.dir_main
    # print '-----------------'
    # p_glbls.print_p_cfg_vars()

def pyprogen():
    """
    creates basic dir-structure
    creates basic python program according to >pyprogen.conf< and .....
    """
    p_read_ini(".", "pyprogen.ini")  # dir relative to >.<
    prog_name = p_glbls.prog_name
    p_log_this('prog_name = ' + prog_name)
    create_maindir(prog_name)
    create_subdirs(prog_name)
    create_ca_parser(prog_name)   # create & start new ConfArgParser


if __name__ == "__main__":
    p_log_init(log_dir = 'p_log', log_fn = 'pyprogen')
    p_log_start()
    pyprogen()
    #prog_name = p_glbls.prog_name
    create_main()
    p_log_end()
    p_utils.p_exit()
