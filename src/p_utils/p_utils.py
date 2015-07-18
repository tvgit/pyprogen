#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "rh"
__date__ = "$05.05.2015 21:55:22$"

# ad decorator:
# https://pythonconquerstheuniverse.wordpress.com/2012/04/29/python-decorators/
# https://gist.github.com/techtonik/2151727

import os
import sys
import io

import ConfigParser  # read configfile

import datetime
import inspect

import p_glbls  # share global values
from   p_log   import p_log_init, p_log_start, p_log_this, p_log_end

# used in: def p_read_cfg():
pyprogen_cfg = """
[properties]
prog_name = y_main
"""

def p_read_cfg(dir_cfg='.', cfg_fn='pyprogen.cfg'):
    """ reads defaults for generated program: name ..."""
    cfg_path = os.path.join(dir_cfg, cfg_fn)
    parser = ConfigParser.SafeConfigParser(allow_no_value=True)
    # parser.readfp(io.BytesIO(pyprogen_cfg))
    p_log_this('cfg_path: ' + cfg_path)
    cfg_file = parser.read(cfg_path)
    p_log_this('cfg file: ' + str(cfg_file))
    p_glbls.prog_name = parser.get("properties", "prog_name")
    if not p_glbls.prog_name:
        p_glbls.prog_name = 'z_main'
    p_glbls.prefix    = p_glbls.prog_name[0] + '_'  # prefix for generated program
    p_log_this("prog_name = " + p_glbls.prog_name)

def make_act_date_str():
    now = datetime.datetime.now()
    now_str =                 str(now.year)
    now_str = now_str + '_' + str(now.month).zfill(2)
    now_str = now_str + '_' + str(now.day).zfill(2)
    now_str = now_str + '_' + str(now.hour).zfill(2)
    now_str = now_str + '_' + str(now.minute).zfill(2)
    now_str = now_str + '_' + str(now.second).zfill(2)
    return now_str

def p_dir_check_isabs(dir):
    """ checks if dir is abs dir """
    dir = os.path.normpath(dir)
    if (os.path.isabs(dir)):
        mssg_1 = (' dir: >' + dir + '< is absolute, should be relative!')
        mssg_2 = (' please change dir: >' + dir + '<    to relative subdir (i.e. ./log) ')
        mssg_3 = ('       ....  exiting!')
        print mssg_1 + mssg_2 + mssg_3
        p_exit()  # exit !
        p_log_this(mssg_1)
        p_log_this(mssg_2)
        p_log_this(mssg_3)
    if (dir == ''): dir = '.'
    return dir

def p_dir_make(dir):
    """ makes dir if dir """
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
            mssge = (' creating dir: ' + dir )
            p_log_this(mssge)
        except IOError:
            mssge = (' creating dir: ' + dir + ' failed!')
            print mssge
            p_log_this(mssge)
    else:
        mssge = (' dir exists : >' + dir + '<')
        p_log_this(mssge)
    return dir

def p_subdir_make(dir):
    """ creates sub_dir """
    dir = p_dir_check_isabs(dir)
    p_dir_make(dir)
    return dir


def p_file_open(fn, mode = 'r'):
    """ open files if file exists """
    if os.path.isfile(fn):
        try:
            f_to_open = open(fn, mode)
        except EnvironmentError:
            msg = (here('', 1) + 'unable to open file : >' + fn + '< EnvironmentError!')
            p_log_this(msg, 'error')
            print msg
        else:
            p_log_this(' file : >' + fn + '< open for ' + mode)
            return f_to_open
    else:
        msg = (' file : >' + fn + '< does not exist')
        p_log_this(msg, 'error')
        print msg


def p_file_close(f):
    file.close(f)

def p_exit(txt=''):
    """ gentle program p_exit  """
    print txt
    sys.exit()

def here(txt='', level=2):
    """ print txt; echoes from the stack the callee """
    mssge = inspect.stack()[level][3] + ': '
    if txt: print txt, mssge
    return mssge

if __name__ == "__main__":
    print here('', 1)
    # logger = p_log_init(log_fn='p_utils')
    p_log_init(log_dir='', log_fn='p_utils')
    p_log_start()
    p_read_cfg()
    print '\n' + '__main__ : ' + p_glbls.prog_name + '\n'
    p_log_end('p_utils')
    p_exit('Program gentle exiting')
else:
    # logger = p_log_init(log_fn='default')
    pass
