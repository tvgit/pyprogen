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

import ppg_glbls  # share global values
import ppg_utils
from   ppg_log import p_log_this
import ppg_cfg.ppg_patterns as patterns

# may be used in: def p_read_ini():
# pyprogen_ini = """
# [properties]
# prog_name = y_main
# """
# read it via:
# parser.readfp(io.BytesIO(pyprogen_ini))

def get_datetime_str(txt_line):
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

def adjust_cfg_path(cfg_file_path):
    # adjust path of y_main.cfg so it can be read by >y_main.py< via cmd-line directive:
    # http://stackoverflow.com/questions/4579908/cross-platform-splitting-of-path-in-python AND
    # http://stackoverflow.com/questions/14826888/python-os-path-join-on-a-list
    path_str = str(cfg_file_path)
    path_split = []
    while True:
        path_str, leaf = os.path.split(path_str)
        if (leaf):
            path_split = [leaf] + path_split  # Adds one element, at the beginning of the list
        else:
            # Uncomment the following line to have also the drive, in the format "Z:\"
            # path_split = [path_str] + path_split
            break;
    del path_split[1]
    new_path_str = os.path.join(*path_split)
    return new_path_str

def p_read_ini(dir_cfg='.', cfg_fn='new_prog.ini'):
    """ reads defaults for generated program: name ..."""
    # http://www.karoltomala.com/blog/?p=622
    p_log_this()
    cfg_path = os.path.join(dir_cfg, cfg_fn)     # cfg_path_tmp of >pyprogen.py< !
    cfg_path = os.path.normpath(cfg_path)        #      not of >y_main.py<  !!
    parser = ConfigParser.SafeConfigParser(allow_no_value=True)
    p_log_this('cfg_path_tmp: ' + cfg_path)
    cfg_file = parser.read(cfg_path)
    p_log_this('cfg file: ' + str(cfg_file))

    # p_glbls.prog_name
    try:
        ppg_glbls.prog_name = parser.get("properties", "prog_name")
        p_log_this('prog_name = ' + ppg_glbls.prog_name)
        if (len(ppg_glbls.prog_name) < 4):
            ppg_glbls.prog_name = ppg_glbls.prog_name + '.py'
            p_log_this('          =>' + ppg_glbls.prog_name)
        if ((string.lower(ppg_glbls.prog_name[-3:])) <> '.py'):
            ppg_glbls.prog_name = ppg_glbls.prog_name + '.py'
            p_log_this('          =>' + ppg_glbls.prog_name)
    except ConfigParser.NoOptionError:
        ppg_glbls.prog_name = 'z_main.py'
        p_log_this('no >prog_name< in: ' + cfg_path + ' !')
        p_log_this('prog_name set to: ' + ppg_glbls.prog_name)

    # p_glbls.prog_path
    ppg_glbls.prog_path = os.path.normpath(ppg_glbls.prog_name[:-3])
    p_log_this("prog_path = " + ppg_glbls.prog_path)

    # p_glbls.prefix
    try:
        ppg_glbls.prefix = parser.get("properties", "prefix")
        p_log_this('prefix = ' + ppg_glbls.prefix)
        if (len(ppg_glbls.prefix) < 2):
            p_log_this('prefix = ' + ppg_glbls.prefix)
            ppg_glbls.prefix = ppg_glbls.prog_name[0] + '_'  # prefix for generated program
            p_log_this('prefix set to: ' + ppg_glbls.prefix)
    except ConfigParser.NoOptionError:
        ppg_glbls.prefix = ppg_glbls.prog_name[0] + '_'  # prefix for generated program
        p_log_this('prefix set to: ' + ppg_glbls.prefix)

    # p_glbls.date_time_str
    ppg_glbls.date_time_str = ppg_utils.p_make_act_date_str()
    # filename of globals of created program
    ppg_glbls.glbls_fn      = ppg_glbls.prefix + 'glbls.py'    # globals of ! >y_main.py< !


def p_inform_about_paths_and_filenames():
    cfg_path = os.path.join(ppg_glbls.dir_cfg, ppg_glbls.cfg_fn)

    mssge  = ''
    mssge += '\n' + '-'*10 + ' ' + ppg_glbls.prog_name + ' ' + '-' * 60 + '\n'
    len_dir_main = len(ppg_glbls.dir_main) + 1
    mssge += '\n Path of YOUR code is:             ' + os.path.join(ppg_glbls.dir_main, ppg_glbls.prog_name)
    mssge += '\n Filename of YOUR code is:         ' + ' '*len_dir_main + ppg_glbls.prog_name
    mssge += '\n You will find the new version in: ' + os.path.join(ppg_glbls.dir_main, '')
    mssge += '\n Path of new version is:           ' + os.path.join(ppg_glbls.dir_main, ppg_glbls.prog_name_new_cfg)
    mssge += '\n Filename of new version is:       ' + ' '*len_dir_main + ppg_glbls.prog_name_new_cfg
    # mssge += '(>' + p_glbls.prog_name + '< was not changed.)'
    # cfg_path_tmp
    len_cfg_dir = len(os.path.dirname(ppg_glbls.cfg_path_tmp)) + 1
    mssge += '\n Path of new cfg-file is:          ' + ppg_glbls.cfg_path_tmp
    mssge += '\n Filename of new cfg-file is:      ' + ' '*len_cfg_dir + os.path.basename(ppg_glbls.cfg_path_tmp)
    # mssge += ' The new files have a timestamp  >' + p_glbls.prog_name[:-3] + '_YYYY_MM_DD-hh_mm_ss.py<.'
    mssge += '\n'
    mssge += '\n You may configure the comand line _args_     of >' + ppg_glbls.prog_name + '<  via:  >new_prog_args.cfg<'
    mssge += '\n  ... but run >pyprogen.py< again!'
    mssge += '\n You may configure the comand line _defaults_ of >' + ppg_glbls.prog_name + '<  via:  >' + cfg_path + '<'
    mssge += '\n >' + cfg_path + '<  will be preserved, if changed. '
    mssge += '\n'
    mssge += '\n  newer generated files will have a timestamp in their filename: >' + ppg_glbls.prog_name[:-3] + '_YYYY_MM_DD-hh_mm_ss.py<.'
    mssge += '\n'
    mssge += '\n Do not change the >' + ppg_glbls.dir_lib + '\*.py< files!'
    mssge += '\n' + '-'*10 + ' ' + ppg_glbls.prog_name + ' ' + '-' * 60
    mssge += '\n'
    print (mssge)


def p_create_paths_and_fns():
    """ creates later needed paths and filenames  """
    ppg_glbls.glbls_fn      = ppg_glbls.prefix + 'glbls.py'    # globals of ! >y_main.py< !
#    p_glbls.CAParser_func = p_glbls.prefix + 'parser'      # name of parser func in >y_CAParser<


def p_subst_vars_in_patterns (input_dict):
    """ substitutes in code parts (input_dict) some words (xx_....) with variable names """
    patts = dict()
    for key, patt in input_dict.iteritems():
        txt = patt.replace("xx_CAParser", ppg_glbls.CAParser_fn[:-3])
        txt =  txt.replace("xx_main", ppg_glbls.prog_name[:-3])
        txt =  txt.replace("xx_parser", ppg_glbls.CAParser_func)
        txt =  txt.replace("xx_glbls", ppg_glbls.glbls_fn[:-3])
        patts[key] = txt
    return patts

def p_write_code(input_dict, outfile_path):
    """ writes >input_dict< to outfile """
    p_log_this('writing: ' + outfile_path)
    with open(outfile_path, 'w') as outfile:
        outfile.write('# -*- coding: utf-8 -*-\n')
        outfile.write('# ' + ppg_glbls.date_time_str + ' generated by: >pyprogen.py<\n')
        #for key, patt in patts.iteritems():
        for key, patt in sorted(input_dict.iteritems()):
            outfile.write(patt)
        outfile.write('# ' + ppg_glbls.date_time_str)

def p_glbls_create():
    """ creates ./y_main/lib/y_glbls.py  """
    # fn and path of  >y_glbls.py<
    outfile_fn   = ppg_glbls.glbls_fn
    outfile_path = os.path.join(ppg_glbls.dir_lib, ppg_glbls.glbls_fn)
    p_log_this('creating: ' + outfile_path)

    txt =       ' '*4 + '# optional args(ConfArgParser):\n'
    for arg in ppg_glbls.opt_arg_vars:
        txt = txt + ' '*4 + 'arg_ns.' + arg + ' = None\n'
    txt = txt + ' '*4 + '# positional args(ConfArgParser):\n'
    for arg in ppg_glbls.pos_arg_vars:
        txt = txt + ' '*4 + 'arg_ns.' + arg + ' = None\n'
    txt = txt + ' '*4 + 'return arg_ns\n'
    patterns.y_glbls[04] = txt

    txt = ''
    patterns.y_glbls[96] = txt

    code = p_subst_vars_in_patterns (patterns.y_glbls)
    p_write_code (code, outfile_path)

def rgx_get_old_hash_strg(inp_line):
    """ rgx for >hash< inp_line / thx to: http://txt2re.com"""
    re1='(>)'	# Any Single Character 1
    re2='(([a-z0-9]*))'	# Alphanum 1
    re3='(<)'	# Any Single Character 2
    rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
    m  = rg.search(inp_line)
    if m:
        c1=m.group(1)
        alphanum1=m.group(2)
        c2=m.group(3)
        old_hash_str = alphanum1
    else:
        old_hash_str = 'NO_HASH_FOUND'
        p_log_this(old_hash_str)
    return old_hash_str


# def calc_cfg_hash(defaults):
#     """ Calculates the hash of members of a list (list[tuple, tuple ...].)"""
#     defaults_str = ''
#     for key_val in defaults:  # type(defaults) == list[(arg,val),(arg,val), tuple ...]
#         defaults_str = defaults_str + key_val[0] + key_val[1]
#     hash_md5 = hashlib.md5()
#     hash_md5.update(defaults_str)  # calc hash
#     hash_of_defaults = hash_md5.hexdigest()
#     return hash_of_defaults

def p_cfg_create_hash():
    """ Calculates the hash of default vars in section [defaults] in >y_main.cfg<.
    Then creates in >y_main.cfg< the section [signature] with items:
    >timestamp< and >hash<.
    Called by >pyprogen.py< after >create_ca_parser< was called,
    i.e after a new >y_main_TimeStamp.cfg< is written."""

    p_log_this('cfg_path_tmp     = ' + ppg_glbls.cfg_path_tmp)

    parser = ConfigParser.SafeConfigParser(allow_no_value=True)
    cfg_file = parser.read(ppg_glbls.cfg_path_tmp)
    try:  # read defaults and calc their hash
        defaults = parser.items("defaults")  # read section "defaults"
        defaults_str = ''
        for key_val in defaults:             # type(defaults) == list[tuple, tuple ...]
            # defaults_str = defaults_str + key_val[0] + key_val[1]
            defaults_str = defaults_str + key_val[0]
        hash_md5           = hashlib.md5()
        hash_md5.update(defaults_str)            # calc hash
        hash_of_defaults   = hash_md5.hexdigest()
    except ConfigParser.NoSectionError:
        p_log_this("No section: 'defaults' in: >" + ppg_glbls.cfg_path_tmp + '< !')
        return

    # to >y_main.cfg< add a section "signature" with hash & time_stamp
    parser.add_section("signature")
    parser.set("signature", "hash", hash_of_defaults)
    parser.set("signature", "timestamp", ppg_glbls.date_time_str)
    parser.write(open(ppg_glbls.cfg_path_tmp, "w"))

def p_cfg_read_hash(cfg_path):
    """ return the val of var >hash< in cfg-file in section [signature] """
    parser = ConfigParser.SafeConfigParser(allow_no_value=True)
    cfg_file = parser.read(cfg_path)

    try:  # read val of var hash
        hash_val = parser.get("signature", "hash")
    except ConfigParser.NoSectionError or ConfigParser.NoOptionError:
        if ConfigParser.NoSectionError:
            p_log_this("No section: 'signature' in: >" + ppg_glbls.cfg_path + '< !')
        return
    return hash_val

def p_cfg_check_hash():
    """ called by >pyprogen.py< after >create_ca_parser< has
    written >y_main.cfg< and after p_cfg_create_hash() has
    added the hash of default vars to >./y_main/cfg/y_main_TimeStamp.cfg<

    Replaces >y_main.cfg< with >./y_main/cfg/y_main_TimeStamp.cfg<
    according to:

    if not (>y_main.cfg< exists)
        move >y_main_TimeStamp.cfg< to >y_main.cfg<
        return
    elsif (>y_main.cfg< != >y_main_TimeStamp.cfg<):
        # keep >y_main.cfg< && keep >y_main_TimeStamp.cfg<;
        return
    else:
        move >y_main_TimeStamp.cfg< to >y_main.cfg<
    """

    p_log_this('cfg_path:      ' + ppg_glbls.cfg_path)

    mssges    = ['','','']        # badly bad. really. I know
    dest_path = ppg_glbls.cfg_path
    mssges[1] = ('renaming:      ' + ppg_glbls.cfg_path_tmp)
    mssges[2] = ('to:            ' + dest_path)

    # There is no >y_main.cfg<:
    if not ppg_utils.p_file_exists (ppg_glbls.cfg_path):
        dest_path = ppg_glbls.cfg_path
        mssges[0] = ('There is no    ' + ppg_glbls.cfg_path + ' =>')
        for mssge in mssges:
            p_log_this (mssge)
        # move source to dest:
        shutil.move(ppg_glbls.cfg_path_tmp, dest_path)
        return

    # There is already a >y_main.cfg<:
    old_hash_of_defaults = p_cfg_read_hash(ppg_glbls.cfg_path)     # >y_main.cfg<
    p_log_this('old_hash_of_defaults =' + old_hash_of_defaults)
    act_hash_of_defaults = p_cfg_read_hash(ppg_glbls.cfg_path_tmp) # >y_main_TimeStamp.cfg<
    p_log_this('act_hash_of_defaults =' + act_hash_of_defaults)

    # act_hash == old_hash
    if (act_hash_of_defaults == old_hash_of_defaults):
        mssges[0] = ('section: "signature" in >' + ppg_glbls.cfg_path + '< unchanged. =>')
        for mssge in mssges:
            p_log_this (mssge)
        # move source to dest: ?? should I ? Or not?
        # shutil.move(p_glbls.cfg_path_tmp, dest_path)
    else:  # act_hash != old_hash
        mssges[0] = ('section: "signature" in >' + ppg_glbls.cfg_path + '< has been modified.')
        mssges[1] = (' => 1) leave >' + ppg_glbls.cfg_path + '< unchanged.')
        mssges[2] = ('    2) most recent config file is: >' + ppg_glbls.cfg_path_tmp + '<.')

        for mssge in mssges:
            p_log_this (mssge)
        for mssge in mssges:
            print(mssge + '\n')


def p_main_was_modified(outfile_path):
    """ check if y_main.py was modified (== hash is different) """
    old_main_file = ppg_utils.p_file_open(outfile_path, mode ='r')
    if not old_main_file:
        return False
    with old_main_file:
        lines = old_main_file.readlines()
    ppg_utils.p_file_close(old_main_file)

    code_line = lines[0]    # line 0 contains coding, i.e.: -*- coding: utf-8 -*-
    date_line = lines[1]    # line 1 contains date-time string
    hash_line = lines[2]    # line 2 contains hash (of lines 3 to n-1) at moment of generating
    # calc hash of code, i.e. of hash all lines, ignoring first 3 lines and last line:
    code_to_hash = ''
    for line in lines[3:-1]:
        code_to_hash = code_to_hash + line

    hash_md5         = hashlib.md5()
    hash_md5.update(code_to_hash)            # calc hash
    hash_of_new_code = hash_md5.hexdigest()

    hash_of_old_code = rgx_get_old_hash_strg(hash_line)  # get hash at moment of generating
    if hash_of_old_code != hash_of_new_code:         # hashes are identical?
        mssge = ('>' + outfile_path + '< has been modified')
        p_log_this (mssge) # ; print mssge
        ppg_glbls.prog_changed = True
        return True
    else:
        p_log_this ('>' + outfile_path + '<  + is unchanged')
        ppg_glbls.prog_changed = False
        return False


def p_main_create():
    """ if (>y_main.py< exists && >y_main.py< was modified) => save it.
    else: => create new >y_main.py<  """
    outfile_fn   = ppg_glbls.prog_name      # fn and path of >y_main.py<
    outfile_path = os.path.join(ppg_glbls.dir_main, outfile_fn)
    p_log_this('creating: ' + outfile_path)

    # Make new code:

    # make code txt for >if<'s for >confarg_vars< of commandline
    txt = ' '*4 + '# optional args(ConfArgParser):\n'
    for arg in ppg_glbls.opt_arg_vars:
        txt +=  ' '*4 + 'if ' + 'confargs.' + arg + ' == confargs.' + arg + ':\n'
        txt +=  ' '*8 + 'eval_arg(confargs.' + arg +')\n'
        txt +=  '\n'

    patterns.y_main[10] = txt       # add txt to pattern

    # make code txt for optional reading of cfg-file via
    # xx_CAParser.xx_parser('--conf-file', 'p_glbls.cfg_path')
    # but adjust dir of config-file by removing highest dir level:
    adjusted_cfg_path = adjust_cfg_path(ppg_glbls.cfg_path)
    txt =  ' '*4 + "# optional reading of cfg-file: (r' == raw string) \n"
    txt += ' '*4 + "# xx_CAParser.xx_parser('--conf-file', r'"
    txt += str(adjusted_cfg_path)
    txt += "')" + '\n'

    patterns.y_main[84] = txt       # add txt to pattern

    # generate correct var names
    y_main = p_subst_vars_in_patterns (patterns.y_main)
    # now >y_main< is complete. => calculate hash for generated program:

    code = ''   # put all code parts together in ane string.
    for key, chunk in sorted(y_main.iteritems()):
        code = code + chunk

    # print '=' *40 ; print len(code)  ;print '=' *40
    hash_md5 = hashlib.md5()
    hash_md5.update(code)                      # calculate hash of code
    hash_of_code = hash_md5.hexdigest()        # here (>hash_of_mytext<) it is

    # Add hash as heading line to the code:
    code_dict    = dict()                           # p_write_code wants dict as input
    code_dict[1] = '# >' + hash_of_code + '< \n'    # second line of y_main.py
    code_dict[2] = code                             #

    # if existing >y_main.py< was modified => new >y_main.py< gets timestamp in fn
    if p_main_was_modified(outfile_path):
        outfile_path = outfile_path[:-3] + '_' + ppg_glbls.date_time_str + '.py'
        ppg_glbls.prog_name_act_cfg = os.path.basename(outfile_path)
    # finally write code (adding timestamp in first line & lastline)
    p_write_code (code_dict, outfile_path)  # write >y_main(_+/-timestamp.py<


if __name__ == "__main__":
    print ppg_glbls.my_name()
    ppg_utils.p_exit()
