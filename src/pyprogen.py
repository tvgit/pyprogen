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
# äöüÄÖÜß
#

__author__ = "rh"
__date__   = "$05.05.2015 21:55:22$"

"""
    pyprogen needs >ConfArgParse<. So first of all do a
    >pip install ConfArgParse< (as admin in windows).

    pyprogen:
    generates a very simple python program, that offers some basic functionality,
    (initialising and logging) and a corresponding directory structure.

    The generated python program may be initialised via command line arguments
    and/or via a configuration file (*.cfg).

    Assume the name of the new program is >my_main.py<.
    Then the generated directory structure is:

    my_main/my_main.py  # my_main.py == new generated python prog
        /cfg/*.cfg      # configuration file(s)
        /lib/*.py       # some py modules
        /log/*.log      # log-files
        /DataIn         # DataIn dir (proposal)
        /DataOut        # DataOut dir (proposal)

    Pyprogen gets its information by two configuration files:

    >new_prog.ini<:
    Here You configure the name of the generated python
    script (default: >y_main.py<).

    And the extent of its logging (TODO).

    There is also a 'prefix', i.e. a letter followed by an underscore, for example 'y_' or 'b_'.
    The prefix serves to mark the variables that are automatically generated in the new
    python program. So name conflicts with variables that You are coding yourself are
    avoided (hopefully). You need not to change this.

    Example:
    <new_prog.ini>
    [properties]
    main_name  = my_program
    # do not change this
    patterns   = patterns.py
    prefix     = x_
    </new_prog.ini>


    >new_prog_args.cfg<:
    Here You configure the commandline arguments of >y_main.py< and their defaults.
    Your new program (>y_main.py<) will use >ConfArgParse<, a python library to handle
    commandline arguments. This module offers an easy way to combine command line
    arguments and configuration files simultaneously.

    Example:
    <new_prog_args.cfg>
        parser.add_argument('-a', '--aaaa', default='aaaa_def_val', help = ' help aaaa')
        parser.add_argument('-b', '--bbbb', default='bbbb_def_val', help = ' help bbbb')
    </new_prog_args.cfg>

    Executing >pyprogen.py< will generate: >my_program.py< and some dirs
    and files, for example >./cfg/my_program.cfg<

    You may call >my_program.py< with commandline arguments:
    >my_program.py -a AaAaA --bbbb BbBbBbB
    Then it will evaluate the cmdline arguments >a< and >b<.

    Or you call it via:
    >my_program.py -c ./cfg/my_program.cfg
    Then it will evaluate the config file >./cfg/my_program.cfg<

"""
    # >ConfArgParse< is able to read and to write configuration files.
    # This latter ability is used by >pyprogen<:
    # in a first step >pyprogen< writes the code for >y_main.py<'s parser
    # >y_CAParser.py<.
    # Then it executes this program (>y_CAParser.py<) with the
    # "--export-conf-file > ./y_main/cfg/y_main.cfg" commandline parameter.
    # After that you will find a config file: >y_main.cfg<
    # for your new >y_main.py< in the ./y_main/cfg/ dir.
    #
    # (http://martin-thoma.com/configuration-files-in-python/)

# ad decorator:
# https://pythonconquerstheuniverse.wordpress.com/2012/04/29/python-decorators/

# Ad ConfArgParse
# https://pypi.python.org/pypi/ConfArgParse

import os
import shutil
import subprocess
import ppg_lib.ppg_glbls as p_glbls  # share global values
import ppg_lib.ppg_utils as p_utils  # utils for pyprogen
import ppg_lib.ppg_code  as p_code   # functions generating python code
from   ppg_lib.ppg_log   import p_log_init, p_log_start, p_log_this, p_log_end
from   ppg_lib.ppg_ConfArgParser import p_create_ConfArgParser

def maindir_make(prog_path) :
    """ """
    p_log_this()
    p_glbls.main_dir = p_utils.p_subdir_make(prog_path)


def subdirs_make(prog_path):
    """ """
    p_log_this()
    # p_utils.p_terminal_mssge_note_this()  # some visible sign

    p_glbls.cfg_dir     = p_utils.p_subdir_make(os.path.join(prog_path, 'cfg'))
    p_glbls.cfg_fn      = p_glbls.main_name[:-3] + '.cfg'   # cfg-file of new y_main.py
    p_glbls.cfg_path    = os.path.join(p_glbls.cfg_dir, p_glbls.cfg_fn)

    p_glbls.cfg_fn_tmp  = p_glbls.cfg_fn[:-4] + '_Tmp' + p_glbls.cfg_fn[-4:]
    p_glbls.cfg_path_tmp= os.path.join(p_glbls.cfg_dir, p_glbls.cfg_fn_tmp)

    p_glbls.lib_dir     = p_utils.p_subdir_make(os.path.join(prog_path, 'lib'))

    p_glbls.log_dir     = p_utils.p_subdir_make(os.path.join(prog_path, 'log'))

    p_glbls.dir_DataIn  = p_utils.p_subdir_make(os.path.join(prog_path, 'DataIn'))
    p_glbls.dir_DataOut = p_utils.p_subdir_make(os.path.join(prog_path, 'DataOut'))

def copy_p_utils():
    # dammed '__init__.py'! 2 hrs of nirwana!
    # for every file in fn_list:
    p_log_this()
    fn_list = ['ppg_utils.py', 'ppg_log.py', '__init__.py']
    for fn in fn_list:
        # create and normalize source path:
        p_utils_srce_path = os.path.join('.', 'ppg_lib', fn)
        p_utils_srce_path = os.path.normpath(p_utils_srce_path)
        # create and normalize destination path:
        p_utils_dest_path = os.path.join('.', p_glbls.lib_dir, fn)
        p_utils_dest_path = os.path.normpath(p_utils_dest_path )
        # copy from source to dest
        shutil.copy(p_utils_srce_path, p_utils_dest_path)
        p_log_this( fn + ' copied')

def ca_parser_make():
    """ Writes via p_create_ConfArgParser() in ./y_main/lib a new
    confargparser == >y_CAParser.py< for the new program >y_main.py<.
    Configure it according to >new_prog_args.cfg<
    """
    p_log_this()
    p_create_ConfArgParser('./new_prog_args.cfg') # create confargparser for >y_main.py<

def ca_parser_run():
    """ Call >y_CAParser.py< via subprocess. >y_CAParser.py< is able
    to write a conf file (if called as script), so it will write
    the config-file to >./y_main/cfg<.
    It is this config-file that You will use to configure >y_main<.
    """

    subprocess_path  = p_glbls.CAParser_path
    p_log_this("subprocess_path   = " + subprocess_path)
    # http://pymotw.com/2/subprocess/
    # start new ConfArgParser to create cfg-file (aka >cfg_path_tmp<) for >y_main.py<
    cfg_path_tmp = p_glbls.cfg_path_tmp         # == >y_main_Tmp.cfg<
    p_log_this("cfg_path_tmp      = " + cfg_path_tmp)
    subprocess.call([subprocess_path, cfg_path_tmp], shell=True)

def pyprogen():
    """
    creates basic directory structure and basic python program
      according to the configuration files: >new_prog.ini< and new_>prog_args.conf<.
    """
    # dwyns == Do what your name says
    p_log_this()                  # in ./ppg_log/pyprogen.log
    p_code.p_read_ini(".", "new_prog.ini")  # read >new_prog.ini< and create some global fn's, path's and var's
                                  # This data will be stored in module >ppg_glbls.py<
    # in the comments >y_main< is a symbolic the name of the generated program.
    prog_dir = p_glbls.main_dir   # ./y_main; >y_main.py< will live here

    maindir_make(prog_dir)        # make dir  ./y_main
    subdirs_make(prog_dir)        # make dirs ./y_main/lib; ./y_main/log; ./y_main/cfg
    copy_p_utils()                # copy some utilities to ./y_main/lib
    #
    ca_parser_make()              # make ./y_main/lib/y_CAParser.py
    ca_parser_run()               # run: y_CAParser.py => create: >y_main_Tmp.cfg<

    p_code.p_cfg_clear_versions() # check (via hash) if there are yet identical versions of >y_main_*.cfg<
    p_code.p_glbls_create()       # create modul ./y_main/lib/y_glbls.py

    # Finally create >./y_main/y_main.py< or >./y_main/evaluate_confargs.py<
    p_code.p_code_make()          # create progr >./y_main/y_main.py< or >./y_main/evaluate_confargs.py<

    p_glbls.print_p_cfg_and_args()# print variables and command line args in ./pyprogen/ppg_lib/ppg_glbls.
    p_code.p_inform_about_paths_and_filenames()   # dwyns


if __name__ == "__main__":
    p_log_init(log_dir = 'ppg_log', log_fn = 'pyprogen')
    p_log_start()        # log is in ./ppg_log/pyprogen.log
    pyprogen()           # python program generator
    p_log_end()          # dwyns
    # p_utils.p_terminal_mssge_note_this()  # some visible sign
    p_utils.p_terminal_mssge_success()  # some visible sign
    p_utils.p_exit()     # exit program
