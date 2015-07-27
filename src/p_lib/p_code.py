#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'rh'
__date__ = "$18.07.2015 15:55:22$"

import os
import string
import ConfigParser  # read configfile
import hashlib
import shutil
import re

import p_glbls  # share global values
import p_utils
from   p_log import p_log_this
import p_cfg.patterns as patterns

# may be used in: def p_read_ini():
# pyprogen_ini = """
# [properties]
# prog_name = y_main
# """
# read it via:
# parser.readfp(io.BytesIO(pyprogen_ini))

def p_read_ini(dir_cfg='.', cfg_fn='pyprogen.ini'):
    """ reads defaults for generated program: name ..."""
    # http://www.karoltomala.com/blog/?p=622
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    # print 'p_read_ini: dir_path = ', p_utils.p_act_dir_path()
    # print 'p_read_ini: dir_path = ', dir_path
    # print p_glbls.__file__
    p_log_this()
    cfg_path = os.path.join(dir_cfg, cfg_fn)
    cfg_path = os.path.normpath(cfg_path)
    parser = ConfigParser.SafeConfigParser(allow_no_value=True)
    p_log_this('cfg_path: ' + cfg_path)
    cfg_file = parser.read(cfg_path)
    p_log_this('cfg file: ' + str(cfg_file))

    # p_glbls.prog_name
    try:
        p_glbls.prog_name = parser.get("properties", "prog_name")
        p_log_this('prog_name = ' + p_glbls.prog_name)
        if (len(p_glbls.prog_name) < 4):
            p_glbls.prog_name = p_glbls.prog_name + '.py'
            p_log_this('          =>' + p_glbls.prog_name)
        if ((string.lower(p_glbls.prog_name[-3:])) <> '.py'):
            p_glbls.prog_name = p_glbls.prog_name + '.py'
            p_log_this('          =>' + p_glbls.prog_name)
    except ConfigParser.NoOptionError:
        p_glbls.prog_name = 'z_main.py'
        p_log_this('no >prog_name< in: ' + cfg_path + ' !')
        p_log_this('prog_name set to: ' + p_glbls.prog_name)

    # p_glbls.prog_path
    p_glbls.prog_path = os.path.normpath(p_glbls.prog_name[:-3])
    # print 'p_read_ini: p_glbls.prog_path = ', p_glbls.prog_path
    p_log_this("prog_path = " + p_glbls.prog_path)

    # p_glbls.prefix
    try:
        p_glbls.prefix = parser.get("properties", "prefix")
        p_log_this('prefix = ' + p_glbls.prefix)
        if (len(p_glbls.prefix) < 2):
            p_log_this('prefix = ' + p_glbls.prefix)
            p_glbls.prefix = p_glbls.prog_name[0] + '_'  # prefix for generated program
            p_log_this('prefix set to: ' + p_glbls.prefix)
    except ConfigParser.NoOptionError:
        p_glbls.prefix = p_glbls.prog_name[0] + '_'  # prefix for generated program
        p_log_this('prefix set to: ' + p_glbls.prefix)

    # p_glbls.my_code_fn
    try:
        p_glbls.my_code_fn = parser.get("properties", "my_code_fn")
        p_log_this('my_code_fn = ' + p_glbls.my_code_fn)
        if (len(p_glbls.my_code_fn) < 3):
            p_glbls.my_code_fn = p_glbls.my_code_fn + '.py'
            p_log_this('          =>' + p_glbls.my_code_fn)
        if ((string.lower(p_glbls.my_code_fn[-3:])) <> '.py'):
            p_glbls.my_code_fn = p_glbls.my_code_fn + '.py'
            p_log_this('          =>' + p_glbls.my_code_fn)
    except ConfigParser.NoOptionError:
        p_glbls.my_code_fn = 'my_code.py'
        p_log_this('no >my_code_fn< in: ' + cfg_path + ' !')
        p_log_this('my_code_fn set to: ' + p_glbls.my_code_fn)

def p_inform_about_paths_and_filenames():

    print
    print '-' *60
    print 'You will find your program in: ' + os.path.join(p_glbls.dir_main, '')
    print 'Start it via:                  ' + os.path.join(p_glbls.dir_main, p_glbls.prog_name)
    print 'YOUR CODE should reside in:    ' + os.path.join(p_glbls.dir_lib, p_glbls.my_code_fn)
    print 'It will be preserved, if changed.'
    print 'Beware of modifying the other *.py files.'
    # TODO rename 'pyprogen_001.conf'
    print 'Configure the comand line args via: ' + 'pyprogen_001.conf'
    print 'Configure the comand line defaults via: ' + os.path.join(p_glbls.dir_cfg, p_glbls.cfg_fn)
    # TODO rename pyprogen ?
    print 'Note that >' + p_glbls.cfg_fn + '< is changed every time you run >' + 'pyprogen.py' + '<'
    print '-' *60
    print





def create_some_file_names():
    p_glbls.glbls_fn      = p_glbls.prefix + 'glbls.py'          # globals of >y_main.py< !
    # p_glbls.my_code_fn    = p_glbls.prefix + p_glbls.my_code_fn  # path globals
    p_glbls.CAParser_func = p_glbls.prefix + 'parser'         # name of parser func in >y_CAParser<


def p_subst_vars_in_patterns (input_dict):
    """ substitutes in code parts (input_dict) some words (xx_....) with variable names """
    p_log_this()
    patts = dict()
    for key, patt in input_dict.iteritems():
        txt = patt.replace("xx_CAParser", p_glbls.CAParser_fn[:-3])
        txt =  txt.replace("xx_main",     p_glbls.prog_name[:-3])
        txt =  txt.replace("xx_parser",   p_glbls.CAParser_func)
        txt =  txt.replace("xx_glbls",    p_glbls.glbls_fn[:-3])
        txt =  txt.replace("xx_my_code",  p_glbls.my_code_fn[:-3])
        patts[key] = txt
    return patts

def p_write_code (input_dict, outfile_fn, outfile_path):
    """ writes >input_dict< to outfile """
    p_log_this()
    now_str = p_utils.p_make_act_date_str()
    p_log_this('writing: ' + outfile_path)
    with open(outfile_path, 'w') as outfile:
        outfile.write('# ' + now_str + ' generated by: >pyprogen.py<\n')
        #for key, patt in patts.iteritems():
        for key, patt in sorted(input_dict.iteritems()):
            outfile.write(patt)
        outfile.write('# ' + now_str)

def p_globals():
    """ creates ./y_main/lib/y_glbls.py  """
    p_log_this(' begin')

    txt =       ' '*4 + '# optional args(ConfArgParser):\n'
    for arg in p_glbls.opt_arg_vars:
        txt = txt + ' '*4 + 'arg_ns.' + arg + ' = None\n'
    txt = txt + ' '*4 + '# positional args(ConfArgParser):\n'
    for arg in p_glbls.pos_arg_vars:
        txt = txt + ' '*4 + 'arg_ns.' + arg + ' = None\n'
    txt = txt + ' '*4 + 'return arg_ns\n'
    patterns.y_glbls[04] = txt

    txt = ''
    patterns.y_glbls[96] = txt

    # fn and path of  >y_glbls.py<
    outfile_fn   = p_glbls.glbls_fn
    outfile_path = os.path.join(p_glbls.dir_lib, p_glbls.glbls_fn)

    # p_subst(patterns.y_glbls, outfile_fn, outfile_path)
    code = p_subst_vars_in_patterns (patterns.y_glbls)
    p_write_code (code, outfile_fn, outfile_path)
    p_log_this(' end' )

def get_old_hash_strg(hash_line):
    """ extract originally calculated hash from inp_line / thx to: http://txt2re.com"""
    re1='(>)'	# Any Single Character 1
    re2='(([a-z0-9]*))'	# Alphanum 1
    re3='(<)'	# Any Single Character 2
    rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
    m  = rg.search(hash_line)
    if m:
        c1=m.group(1)
        alphanum1=m.group(2)
        c2=m.group(3)
        # print c1 ; print alphanum1 ; print c2
        old_hash_str = alphanum1
    else:
        old_hash_str = 'NO_HASH_FOUND'
        p_log_this(old_hash_str)
    return old_hash_str


def get_datetime_str(txt_line):
    """ thx to: http://txt2re.com"""
    re1='((?:(?:[1]{1}\\d{1}\\d{1}\\d{1})|(?:[2]{1}\\d{3})))(?![\\d])'	# Year 1
    re2='(_)'	# Any Single Character 1
    re3='(\\d+)'	# Integer Number 1
    re4='(_)'	# Any Single Character 2
    re5='(\\d+)'	# Integer Number 2
    re6='(_)'	# Any Single Character 3
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


def save_modified_my_code(outfile_path):
    """ if y_my_code.py was modified (== hash is different),
    rename it with date-time signature """
    old_my_code_file = p_utils.p_file_open(outfile_path, mode = 'r')
    if not old_my_code_file:
        return
    with old_my_code_file:
        lines = old_my_code_file.readlines()
    p_utils.p_file_close(old_my_code_file)

    date_line = lines[0]    # first  line contains date-time string
    hash_line = lines[1]    # second line contains hash (of lines 3 to n-1) at moment of generating
    # hash of file w/o first 2 lines and w/o last line in >old_code_to_hash<:
    old_code_to_hash = ''
    for line in lines[2:-1]:
        old_code_to_hash = old_code_to_hash + line

    hash_md5           = hashlib.md5()
    hash_md5.update(old_code_to_hash)            # calc hash
    hash_of_old_code   = hash_md5.hexdigest()

    # print 'hash_line     = '   , hash_line.rstrip()
    # print 'hash_of_old_code = ', hash_of_old_code

    old_hash_str = get_old_hash_strg(hash_line)  # get hash at moment of generating
    if old_hash_str != hash_of_old_code:         # hashes are identical?
        # print outfile_path + ' changed!'
        # copy from source to dest:
        # print 'date_line =', date_line
        date_time = get_datetime_str(date_line)  # date_line == first line of y_my_code-py
        dest_path = outfile_path[:-3] + date_time + '.py'
        # print dest_path
        p_log_this ( '>' + outfile_path + '< renamed to: >' + dest_path + '<')
        shutil.move(outfile_path, dest_path)
    return hash_of_old_code

def p_my_code():
    """ if modified, saves old >y_my_code.py< / creates new y_my_code.py """
    p_log_this(' begin')
    # fn and path of  >y_main.py<
    outfile_fn = p_glbls.my_code_fn
    outfile_path = os.path.join(p_glbls.dir_lib, outfile_fn)
    # if modified, save old >y_my_code.py<:
    save_modified_my_code(outfile_path)

    # Make new code:
    # make txt for >if<'s for >opt_arg_vars< of commandline
    txt =       ' '*4 + '# optional args(ConfArgParser):\n'
    for arg in p_glbls.opt_arg_vars:
        txt = txt + ' '*4 + 'if ' + 'y_glbls.arg_ns.' + arg + ' == "something":\n'
        txt = txt + ' '*8 + 'eval_arg(y_glbls.arg_ns.' + arg +')\n'
        txt = txt + '\n'
    # add this txt to pattern:
    patterns.y_my_code[10] = txt

    # now >y_my_code< is complete. => calculate hash for generated program:
    y_my_code = p_subst_vars_in_patterns (patterns.y_my_code)
    code = ''
    for key, chunk in sorted(y_my_code.iteritems()):
        code = code + chunk

    # print '=' *40 ; print len(code)  ;print '=' *40
    hash_md5 = hashlib.md5()
    hash_md5.update(code)                      # calculate hash
    hash_of_mytext = hash_md5.hexdigest()

    code_dict    = dict()                               # p_write_code wants dict as input
    code_dict[1] = '# >' + hash_of_mytext + '< \n'      # second line of y_my_code.py
    code_dict[2] = code                                 #
    p_write_code (code_dict, outfile_fn, outfile_path)  # write >y_my_code.py<
    p_log_this(' end' )


def p_main():
    """ creates y_main.py """
    p_log_this(' begin')
    # fn and path of  >y_main.py<
    outfile_fn = p_glbls.prog_name
    outfile_path = os.path.join(p_glbls.dir_main, outfile_fn)
    # write code of  >y_main.py<
    code = p_subst_vars_in_patterns (patterns.y_main)
    p_write_code (code, outfile_fn, outfile_path)
    p_log_this(' end' )


if __name__ == "__main__":
    print p_glbls.my_name()
    p_utils.p_exit()
