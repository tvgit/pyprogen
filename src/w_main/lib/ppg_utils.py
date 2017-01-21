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

from   ppg_log   import p_log_init, p_log_start, p_log_this, p_log_end


def print_format_table():
    """
    prints table of formatted text format options
    """
    for style in range(8):
        for fg in range(30,38):
            s1 = ''
            for bg in range(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')


def p_error():
    # http://stackoverflow.com/questions/287871
    #     ... print-in-terminal-with-colors-using-python
    # print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')
    print('\x1b[1;35;40m' + 'Error' + '\x1b[0m')
    pass

def p_success():
    # http://stackoverflow.com/questions/287871
    #     ... print-in-terminal-with-colors-using-python
    # print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')
    print('\x1b[1;32;40m' + 'Success' + '\x1b[0m')
    pass

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


def p_get_prog_name():
    prog_info = scriptinfo()
    prog_name = prog_info['name']
    return prog_name


def p_get_prog_dir():
    prog_info = scriptinfo()
    prog_dir  = prog_info['dir']
    return prog_dir


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


def p_dir_is_abs(dir):
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
    dir = p_dir_is_abs(dir)
    p_dir_make(dir)
    return dir


def p_file_exists (fn, print_message = False):
    """ open files if file exists - error otherwise """
    if os.path.isfile(fn):
        return True
    else:
        msg = (' file : >' + fn + '< does not exist')
        p_log_this(msg, 'error')
        if print_message: print msg
        return False


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
    elif (mode == 'w'):
        open(fn, 'w').close()
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
    fn = os.path.basename(f.name)
    msg = ('closing file: ' + fn)
    file.close(f)
    p_log_this(msg); print msg

def p_file_delete(fn):
    msg = ''
    if os.path.exists(fn):
        try:
            os.remove(fn)
        except OSError, err:
            msg = ("Error: %s - %s." % (err.fn, err.strerror))
            p_log_this(msg); print msg
    else:
        msg = ("Error: %s - %s." % (err.fn, err.strerror))
        p_log_this(msg); print msg

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
    p_log_init(log_dir='', log_fn='ppg_lib')
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
