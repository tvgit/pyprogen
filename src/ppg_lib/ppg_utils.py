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
import difflib
import inspect
import re


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


def p_terminal_mssge_note_this(mssge ='note this'):
    # http://stackoverflow.com/questions/287871
    #     ... print-in-terminal-with-colors-using-python
    # print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')
    print('\x1b[6;36;40m' + mssge + '\x1b[0m')
    pass

def p_terminal_mssge_error(mssge ='Error'):
    # http://stackoverflow.com/questions/287871
    #     ... print-in-terminal-with-colors-using-python
    # print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')
    print('\x1b[1;35;40m' + mssge + '\x1b[0m')
    pass

def p_terminal_mssge_success(mssge ='Success'):
    # http://stackoverflow.com/questions/287871
    #     ... print-in-terminal-with-colors-using-python
    # print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')
    print('\x1b[1;32;40m' + mssge + '\x1b[0m')
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

def program_name_and_dir_print():
    prog_name = p_program_name_get()
    prog_dir  = p_program_dir_rtrn()
    print '-' * 8
    print 'program name: ' + prog_name
    print 'program dir : ' + prog_dir
    print '-' * 8

def p_program_name_get():
    prog_info = scriptinfo()
    prog_name = prog_info['name']
    return prog_name


def p_program_dir_rtrn():
    prog_info = scriptinfo()
    prog_dir  = prog_info['dir']
    return prog_dir


def p_current_module_path_rtrn():
    """" print path of act module independent of calling program """
    # http://www.karoltomala.com/blog/?p=622
    # http://stackoverflow.com/questions/247770/retrieving-python-module-path
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    return dir_path


def p_datetime_str_rtrn(txt_line):
    """ thx to: http://txt2re.com"""
    re1='((?:(?:[1]{1}\\d{1}\\d{1}\\d{1})|(?:[2]{1}\\d{3})))(?![\\d])'	# Year 1
    re2='(_)'	# Any Single Character 1
    re3='(\\d+)'	# Integer Number 1
    re4='(_)'	# Any Single Character 2
    re5='(\\d+)'	# Integer Number 2
    re6='(-)'	# Any Single Character 3
    re7='(\\d+)'	# Integer Number 3
    re8='(_)'	# Any Single Character 4
    re9='(\\d+)'	# Integer Number 4
    re10='(_)'	# Any Single Character 5
    re11='(\\d+)'	# Integer Number 5

    rg = re.compile(re1+re2+re3+re4+re5+re6+re7+re8+re9+re10+re11,re.IGNORECASE|re.DOTALL)
    m = rg.search(txt_line)
    if m:
        year1=m.group(1)
        c1=m.group(2)
        int1=m.group(3)
        c2=m.group(4)
        int2=m.group(5)
        c3=m.group(6)
        int3=m.group(7)
        c4=m.group(8)
        int4=m.group(9)
        c5=m.group(10)
        int5=m.group(11)
        sgntr = '_'+year1+c1+int1+c2+int2+c3+int3+c4+int4+c5+int5
        return sgntr
    else:
        return '_UNKNOWN_DATE_TIME'

def p_act_date_str_rtrn():
    now     = datetime.datetime.now()
    now_str =                 str(now.year)
    now_str = now_str + '_' + str(now.month).zfill(2)
    now_str = now_str + '_' + str(now.day).zfill(2)
    now_str = now_str + '-' + str(now.hour).zfill(2)
    now_str = now_str + '_' + str(now.minute).zfill(2)
    now_str = now_str + '_' + str(now.second).zfill(2)
    return now_str


def p_path_abs_is(path):
    """ checks if path is abs path """
    ldg = ''
    if path[:2] == '.' + os.path.sep:
        ldg = path[:2]
    path = ldg + os.path.normpath(path)

    if (os.path.isabs(path)):
        mssg_1 = (' path: >' + path + '< is absolute, but should be relative!')
        mssg_2 = (' please change path: >' + path + '<    to relative subdir (i.e. ./log) ')
        mssg_3 = ('       ....  exiting!')
        print mssg_1 + mssg_2 + mssg_3
        p_log_this(mssg_1); p_log_this(mssg_2) ; p_log_this(mssg_3)
        p_exit()  # exit !
    if (path == ''): path = '.'
    return path

def p_dir_make(dir):
    """ if dir does not exist -> make dir """
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
    dir = p_path_abs_is(dir)
    p_dir_make(dir)
    return dir


# def p_dir_traverse_recursively(path, regex):
#     """http://stackoverflow.com/questions/7012921/recursive-grep-using-python"""
#     # http: // txt2re.com
#     # regex = "(.+?)(\.[^.]*$|$)"  # == filename
#     # regObj = re.compile(regex)
#     # http://codereview.stackexchange.com/questions/19103/python-function-to-match-filenames-with-extension-names
#     result_list = []
#     for root, dirs, fnames in os.walk(path):
#         for fname in fnames:
#             if regObj.match(fname):
#                 result_list.append(os.path.join(root, fname))
#     return sorted(result_list)

def p_check_filename_pattern():
    regex = "(.+?)(\.[^.]*$|$)"  # == filename
    regObj = re.compile(regex)
    pass

def p_dir_traverse_recursively(path):
    """http://stackoverflow.com/questions/7012921/recursive-grep-using-python"""
    # http: // txt2re.com
    # regex = "(.+?)(\.[^.]*$|$)"  # == filename
    # regObj = re.compile(regex)
    # http://codereview.stackexchange.com/questions/19103/python-function-to-match-filenames-with-extension-names
    result_list = []
    for root, dirs, fnames in os.walk(path):
        for fname in fnames:
            if regObj.match(fname):
                result_list.append(os.path.join(root, fname))
    return sorted(result_list)

def grep_in_file(filepath, regex):
    """http://stackoverflow.com/questions/7012921/recursive-grep-using-python"""
    regObj = re.compile(regex)
    result_list = []
    with open(filepath) as f:
        for line in f:
            if regObj.match(line):
                result_list.append(line)
    return result_list


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
    p_log_this(msg); #print msg

def p_file_delete(fn):
    if os.path.exists(fn):
        try:
            os.remove(fn)
            msg = ("%s removed" % fn)
            p_log_this(msg) #; print msg
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
    p_terminal_mssge_error()
    p_terminal_mssge_note_this()
    print_format_table()
    print p_here('', 1)        # does not work
    prog_info = scriptinfo()
    prog_name = prog_info['name']
    print '\n' + '__main__ : ' + prog_name + '\n'
    p_exit('Program gentle exiting')
else:
    # logger = p_log_init(log_fn='default')
    pass
