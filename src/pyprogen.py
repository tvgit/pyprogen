#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# PyCharm:
# New Editor Window: click on tab > Split Vertically
# ALT left/right  -> editor history back & forth
# Ctrl Tab        -> list/switch editor windows
# Ctrl B          -> go to declaration
# Alt F7          -> find usages
# Shift F6        -> run file
# Shift Ctrl C    -> toggle comment
# F12             -> open last Run
#
# Filetypes association:
# File > Settings > Editor > File Types ... (ie: *.cfg like *.ini)
#
# git-credential-winstore.exe
#
# äöüÄÖÜß
#

__author__ = "rh"
__date__   = "$05.05.2015 21:55:22$"

"""
Also: zusätzlich zum Beschriebenen, (nicht ausreichend Dokumentierten), macht das
Programm folgendes:

1. Veränderungen in >y_main.cfg<
 Wenn pyprogen läuft, wird immer eine aktuelle >y_main_TIMESTAMP.cfg< File erzeugt.
 Diese wird dann mit der bisher gültigen >y_main.cfg< verglichen, und zwar

 über den Vergleich von Hash Werten der Sektion [defaults]
 oder
 über den Vergleich von Hash Werten der Variablen (nicht deren Werte) der Sektion [defaults]


 in den beiden cfg - Files: Falls sich hier nichts verändert hat,
 dann bleibt >y_main.cfg< unverändert,

2. erkläre warum die Parameter so seltsame Namen haben (x_glbls.arg_ns.fn_data_in)
 (wg Namespace + der Name des Parameters aus der *.cfg) oder:
 benenne das Ganze in y_main.py beim import um:
 import lib.x_glbls.arg_ns    as args

finde heraus wo/wann die >y_main.cfg< geschrieben wird =>
    sortiere output in >y_main.cfg< alphabetisch

doc: erkläre, was es mit dem prefix auf sich hat (i.e. automatisch generierte variablen).

Die Namen der Log-Files, Data-Files etc überprüfen: zB in y_main.cfg ...
names of out_file (? what is this) in /y_main/cfg/y_main.cfg is wrong: P:log etc instead of y_main.log

in p_utils make examples how to open files, scan dirs etc ...
"""

"""
    0.
    First do a >pip install ConfArgParse< (as admin in windows)

    pyprogen:
    generates a very simple python program, that offers a basic functionality,
    (initialising and logging) and the corresponding directory structure.

    The generated python program may be initialised via command line arguments
    and/or via a configuration file (*.cfg).

    Assume the name of the new program is >y_main.py<.
    Then the generated directory structure is:

    y_main/y_main.py  # y_main.py == new generated python prog
        /cfg/*.cfg    # configuration file(s)
        /lib/*.py     # some py modules
        /log/*.log    # log-files
        /DataIn/*.*   # DataIn files (proposal)
        /DataOut/*.*  # DataOut files (proposal)

    Pyprogen gets some information by two configuration files:

    >new_prog.ini<:
    Here You configure the name of the generated python
    script (default: >y_main.py<) and the extent of its logging (TODO),
    and the 'prefix', i.e. a letter followed by an underscore, for example 'y_' or 'b_'.
    The prefix serves to mark the variables that are automatically generated in the new
    python program. So name conflicts with variables that You are coding yourself are
    avoided (hopefully).

    >new_prog_args.cfg<:
    Here You configure the commandline arguments of >y_main.py< and their defaults.
    Your new program (>y_main.py<) will use >ConfArgParse<, a python library to handle
    commandline arguments. This module offers an easy way to combine command line
    arguments and configuration files simultaneously.

    Example:
    <new_prog.ini>

    [properties]
    prog_name  = s_create_subdirs
    prefix     = s_

    </new_prog.ini>

"""
    # <technical note>
    # >ConfArgParse< is able to read and to write (!) configuration files.
    # This ability is used by >pyprogen<:
    # in a first step >pyprogen< writes the code for >y_main.py<'s parser
    # >y_CAParser.py<.
    # Then it executes this program (>y_CAParser.py<) with the
    # "--export-conf-file > ./y_main/cfg/y_main.cfg" commandline parameter.
    # After that you will find a config file: >y_main.cfg<
    # for your new >y_main.py< in the ./y_main/cfg/ dir.
    #
    # (http://martin-thoma.com/configuration-files-in-python/)
    #
    # 100.
    # Dark sides of py:
    # py can not protect vars inside a module from being modified from outside.
    # [
    # module want_be_private
    # var_priv = 66
    #
    # module outside
    # import want_be_private
    # want_be_private.var_priv = 99   !!!
    # ]
    #
    # py can not prevent creating attributes to this module from outside.
    # [
    # module want_be_private
    # var_priv = 100
    #
    # module outside
    # import want_be_private
    # want_be_private.var_NEW = 1 # but inside >module want_be_private< you know nothing
    #   about >var_NEW<!!!
    # ]
    #
    # Badly bad:
    # Composing a path string by adding strings via >os.path.join()< and >os.path.normpath()<
    # for example joining 'c:' plus 'my_path' plus 'x_program.sh'
    # in Windows eventually there may be coming up a string containing an unexpected escape sequence:
    # 'c:\my_path\x_program.sh' namely '\x', which is NOT prevented by >os.path.normpath()<!!
    #
    # </technical note>
# ad decorator:
# https://pythonconquerstheuniverse.wordpress.com/2012/04/29/python-decorators/

# Ad ConfArgParse
# https://pypi.python.org/pypi/ConfArgParse

import os
import shutil
import subprocess
import ppg_lib.ppg_glbls as p_glbls  # share global values
import ppg_lib.ppg_utils as p_utils  # utils for pyprogen
import ppg_lib.ppg_code  as p_code   # funcs generating python code
from   ppg_lib.ppg_log   import p_log_init, p_log_start, p_log_this, p_log_end
from   ppg_lib.ppg_ConfArgParser import p_create_ConfArgParser

def create_maindir(prog_path) :
    """ """
    p_log_this()
    p_glbls.main_dir = p_utils.p_subdir_make(prog_path)
    p_glbls.main_dir = os.path.join('.', p_glbls.main_dir)


def create_subdirs(prog_path):
    """ """
    p_log_this()
    p_glbls.cfg_dir = p_utils.p_subdir_make(os.path.join(prog_path, 'cfg'))
    p_glbls.cfg_dir = os.path.join('.', p_glbls.cfg_dir)  # cfg-dir of new y_main.py

    p_glbls.cfg_fn  = prog_path + '.cfg'   # cfg-file of new y_main.py
    p_glbls.cfg_path= os.path.join(p_glbls.cfg_dir, p_glbls.cfg_fn)

    p_glbls.cfg_fn_tmp   = p_glbls.cfg_fn[:-4] + '_' + p_glbls.date_time_str + p_glbls.cfg_fn[-4:]
    p_glbls.cfg_path_tmp = os.path.join(p_glbls.cfg_dir, p_glbls.cfg_fn_tmp)

    p_glbls.lib_dir = p_utils.p_subdir_make(os.path.join(prog_path, 'lib'))
    p_glbls.lib_dir = os.path.join('.', p_glbls.lib_dir)

    p_glbls.log_dir = p_utils.p_subdir_make(os.path.join(prog_path, 'log'))
    p_glbls.log_dir = os.path.join('.', p_glbls.log_dir)

    p_glbls.dir_DataIn  = p_utils.p_subdir_make(os.path.join(prog_path, 'DataIn'))
    p_glbls.dir_DataIn  = os.path.join('.', p_glbls.dir_DataIn)

    p_glbls.dir_DataOut = p_utils.p_subdir_make(os.path.join(prog_path, 'DataOut'))
    p_glbls.dir_DataOut = os.path.join('.', p_glbls.dir_DataOut)


def copy_p_utils_p_log_init():
    # dammed '__init__.py'! 2 hrs of nirwana!
    # for every file in fn_list:
    p_log_this()
    fn_list = ['ppg_utils.py', 'ppg_log.py', '__init__.py']
    for fn in fn_list:
        # create an normalize source path:
        p_utils_srce_path = os.path.join('.', 'ppg_lib', fn)
        p_utils_srce_path = os.path.normpath(p_utils_srce_path)
        # create an normalize destination path:
        p_utils_dest_path = os.path.join('.', p_glbls.lib_dir, fn)
        p_utils_dest_path = os.path.normpath(p_utils_dest_path )
        # copy from source to dest
        shutil.copy(p_utils_srce_path, p_utils_dest_path)
        p_log_this( fn + 'copied')


def create_ca_parser(prog_path):
    """ Writes via p_create_ConfArgParser() in ./y_main/lib a new
    confargparser == >y_CAParser.py< for the new program >y_main.py<.
    Configure it according to >new_prog_args.cfg<

    Then call >y_CAParser.py< via subprocess. Since >y_CAParser.py< is
    prepared to write a conf file - if called as script - it will write
    a config-file to >./y_main/cfg<.
    It is this config-file that You will use to configure >y_main<.
    """
    p_log_this()
    p_create_ConfArgParser('./new_prog_args.cfg') # create confargparser for >y_main.py<
    subprocess_path  = p_glbls.CAParser_path
    p_log_this("subprocess_path   = " + subprocess_path)

    # http://pymotw.com/2/subprocess/
    # start new ConfArgParser to create cfg-file (aka >cfg_path_tmp<) for >y_main.py<
    cfg_path = p_glbls.cfg_path_tmp         # == >y_main_TimeStamp.cfg<
    p_log_this("cfg_path_tmp      = " + cfg_path)
    subprocess.call([subprocess_path, cfg_path], shell=True)

def pyprogen():
    """
    creates basic directory structure and basic python program
      according to the configuration files: >new_prog.ini< and new_>prog_args.conf<.
    """
    # dwyns == Do what your name says
    p_log_this()                  # in ./ppg_log/pyprogen.log
    p_code.p_read_ini(".", "new_prog.ini")  # read >new_prog.ini< and create some global fn's, path's and var's
                                  # These data is stored in module >ppg_glbls.py<
    #
    # >y_main< is in this comment the symbolic name of the generated program.
    #
    prog_path = p_glbls.prog_path # ./y_main; >y_main.py< will live here
    create_maindir(prog_path)     # create dir  ./y_main
    create_subdirs(prog_path)     # create dirs ./y_main/lib; ./y_main/log; ./y_main/cfg
    copy_p_utils_p_log_init()     # copy some utilities to ./y_main/lib
    #
    create_ca_parser(prog_path)   # create & run: ./y_main/lib/y_CAParser.py
                                  # => create: >y_main_TimeStamp.cfg<
    p_code.p_cfg_create_hash()    # create hash for vars in >y_main_TimeStamp.cfg<
    p_code.p_cfg_check_hash()     # check if >./y_main/y_main.cfg exists;<
       # if (exists && changed): => keep it;
       # else: => overwrite it with >y_main_TimeStamp.cfg_YYYY_MM_DD-HH_mm_SS.cfg<
    #
    p_code.p_glbls_create()       # create modul ./y_main/lib/y_glbls.py
    # Finally HERE >y_main.py< will be created:
    p_code.p_main_create()        # create progr ./y_main/y_main.py
    p_code.p_inform_about_paths_and_filenames()   # dwyns
    p_glbls.print_p_cfg_and_args()# print variables and command line args in ./pyprogen/ppg_lib/ppg_glbls.


if __name__ == "__main__":
    p_log_init(log_dir = 'ppg_log', log_fn = 'pyprogen')
    p_log_start(p_utils.p_get_prog_name())
    pyprogen()
    p_log_end()
    p_utils.p_success()
    # p_utils.print_format_table()
    p_utils.p_exit()
