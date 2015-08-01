#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "rh"
__date__ = "$05.05.2015 21:55:22$"

# ad decorator:
# https://pythonconquerstheuniverse.wordpress.com/2012/04/29/python-decorators/
# https://gist.github.com/techtonik/2151727

import os
import sys

import datetime
import inspect
import difflib

from   p_log   import p_log_init, p_log_start, p_log_this, p_log_end

def scriptinfo():
    ''' returns name of running script. See:
    http://code.activestate.com/recipes/579018-python-determine-name-and-directory-of-the-top-lev/
    '''
    import os, sys, inspect
    for part in inspect.stack():
        if part[1].startswith("<"):
            continue
        if part[1].upper().startswith(sys.exec_prefix.upper()):
            continue
        trc = part[1]

    if getattr(sys, 'frozen', False):
        scriptdir, scriptname = os.path.split(sys.executable)
        return {"dir": scriptdir,
                "name": scriptname,
                "source": trc}
    scriptdir, trc = os.path.split(trc)
    if not scriptdir:
        scriptdir = os.getcwd()

    scr_dict ={"name": trc, "source": trc, "dir": scriptdir}
    return scr_dict

def p_act_dir_path():
    # http://www.karoltomala.com/blog/?p=622
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    # see also:
    # http://stackoverflow.com/questions/247770/retrieving-python-module-path
    return dir_path


def p_make_act_date_str():
    now     = datetime.datetime.now()
    now_str =                 str(now.year)
    now_str = now_str + '_' + str(now.month).zfill(2)
    now_str = now_str + '_' + str(now.day).zfill(2)
    now_str = now_str + '-' + str(now.hour).zfill(2)
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
        p_log_this(mssg_1); p_log_this(mssg_2) ; p_log_this(mssg_3)
        p_exit()  # exit !
    if (dir == ''): dir = '.'
    return dir

def p_dir_make(dir):
    """ makes dir if dir """
    dir = os.path.normpath(dir)
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
            p_log_this(' creating dir: ' + dir )
        except IOError:
            mssge = (' creating dir: ' + dir + ' failed!')
            p_log_this(mssge) ; print mssge
    else:
        p_log_this(' dir exists : >' + dir + '<')
    return dir

def p_subdir_make(dir):
    """ creates sub_dir """
    dir = p_dir_check_isabs(dir)
    p_dir_make(dir)
    return dir


def p_file_open(fn, mode = 'r'):
    """ open files if file exists - error otherwise """
    if os.path.isfile(fn):
        try:
            f_open = open(fn, mode)
        except EnvironmentError:
            msg = (p_here('', 2) + 'unable to open file : >' + fn + '< EnvironmentError!')
            p_log_this(msg, 'error') ; print msg
        else:
            msg = (p_here('', 2) + ' file : >' + fn + '< open for ' + mode)
            p_log_this(msg)
            return f_open
    else:
        msg = (' file : >' + fn + '< does not exist')
        p_log_this(msg, 'error'); print msg


def p_file_close(f):
    file.close(f)

def p_exit(txt=''):
    """ gentle program p_exit  """
    print txt
    sys.exit()

def p_here(txt='', level=2):
    """ print txt; echoes from the stack the callee """
    mssge = inspect.stack()[level][3] + ': '
    if txt: print txt, mssge
    return mssge

def show_diff (txt_1, txt_2):
    diff = difflib.ndiff(code.splitlines(), code_of_file.splitlines())
    print '\n'.join(list(diff))



if __name__ == "__main__":
    p_log_init(log_dir='', log_fn='p_lib')
    p_log_start()
    print p_here('', 1)        # does not work
    prog_info = scriptinfo()
    prog_name = prog_info['name']
    print '\n' + '__main__ : ' + prog_name + '\n'
    p_log_end('')
    p_exit('Program gentle exiting')
else:
    # logger = p_log_init(log_fn='default')
    pass
