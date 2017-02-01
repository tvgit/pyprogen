#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'rh'
__date__ = "$18.07.2015 15:55:22$"

import os
import ConfigParser  # read configfile
import glob
import hashlib
import re
import shutil
import string

import ppg_glbls  # share global values
import ppg_utils
from   ppg_log import p_log_this
import ppg_cfg.ppg_patterns as patterns

# may be used in: def p_read_ini():
# pyprogen_ini = """
# [properties]
# main_name = y_main
# """
# read it via:
# parser.readfp(io.BytesIO(pyprogen_ini))


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

    # ppg_glbls.main_name
    try:
        ppg_glbls.main_name = parser.get("properties", "main_name")
        p_log_this('main_name = ' + ppg_glbls.main_name)
        if (len(ppg_glbls.main_name) < 4):
            ppg_glbls.main_name = ppg_glbls.main_name + '.py'
            p_log_this('         -> ' + ppg_glbls.main_name)
        if ((string.lower(ppg_glbls.main_name[-3:])) <> '.py'):
            ppg_glbls.main_name = ppg_glbls.main_name + '.py'
            p_log_this('         -> ' + ppg_glbls.main_name)
    except ConfigParser.NoOptionError:
        mssges = []
        mssges.append('no >main_name< in: ' + cfg_path + ' !')
        mssges.append('main_name set to: ' + ppg_glbls.main_name)
        for mssge in mssges:
            p_log_this(mssge)
            ppg_utils.p_terminal_mssge_error(mssge)

    # ppg_glbls.main_dir & ppg_glbls.main_path
    ppg_glbls.main_dir = os.path.normpath(ppg_glbls.main_name[:-3])
    ppg_glbls.main_dir = os.path.join('.', ppg_glbls.main_dir)
    p_log_this("main_dir  = " + ppg_glbls.main_dir)
    ppg_glbls.main_path= os.path.join(ppg_glbls.main_dir, ppg_glbls.main_name)
    p_log_this("main_path = " + ppg_glbls.main_path)

    # ppg_glbls.confarg_dir
    ppg_glbls.confarg_dir = ppg_glbls.main_dir
    p_log_this("confarg_dir  = " + ppg_glbls.confarg_dir)
    ppg_glbls.confarg_path= os.path.join(ppg_glbls.confarg_dir, ppg_glbls.confarg_name)
    p_log_this("confarg_path = " + ppg_glbls.confarg_path)

    # ppg_glbls.prefix
    try:
        ppg_glbls.prefix = parser.get("properties", "prefix")
        p_log_this('prefix    = ' + ppg_glbls.prefix)
        if (len(ppg_glbls.prefix) < 2):
            p_log_this('prefix = ' + ppg_glbls.prefix)
            ppg_glbls.prefix = ppg_glbls.main_name[0] + '_'  # prefix for generated program
            p_log_this('prefix set to: ' + ppg_glbls.prefix)
    except ConfigParser.NoOptionError:
        ppg_glbls.prefix = ppg_glbls.main_name[0] + '_'  # prefix for generated program
        p_log_this('prefix set to: ' + ppg_glbls.prefix)

    # ppg_glbls.date_time_str
    ppg_glbls.date_time_str = ppg_utils.p_act_date_str_rtrn()
    # filename of globals of created program
    ppg_glbls.glbls_fn      = ppg_glbls.prefix + 'glbls.py'    # globals of ! >y_main.py< !
    # ppg_glbls.glbls_path    = os.path.join(ppg_glbls.lib_dir, ppg_glbls.glbls_fn)
    ppg_glbls.glbls_path    = os.path.join('xxxxxx', ppg_glbls.glbls_fn)

def eval_confargs():
    pass

def p_inform_about_paths_and_filenames():
    """ """
    cfg_path = os.path.join(ppg_glbls.cfg_dir, ppg_glbls.cfg_fn)
    p_log_or_print_cfg_mssges(do_print=True, do_log=False)

    mssge  = ''
    # mssge += headline
    len_dir_main = len(ppg_glbls.main_dir) + 1
    mssge += '\n Filename of YOUR code is:      ' + ' '*len_dir_main + ppg_glbls.main_name
    mssge += '\n Dir  of YOUR code is:          ' + os.path.join(ppg_glbls.main_dir, '')
    mssge += '\n Path of YOUR code is:          ' + os.path.join(ppg_glbls.main_dir, ppg_glbls.main_name)
    mssge += '\n'
    mssge += '\n Filename of new code is:       ' + ' '*len_dir_main + ppg_glbls.code_new_name
    mssge += '\n Dir  of new code is:           ' + os.path.join(ppg_glbls.main_dir, '')
    mssge += '\n Path of new code is:           ' + ppg_glbls.code_new_path
    # cfg_path_tmp
    mssge += '\n'
    len_cfg_dir = len(os.path.dirname(ppg_glbls.cfg_path)) + 1
    mssge += '\n Path of valid cfg-file is:     ' + ppg_glbls.cfg_path
    mssge += '\n Filename of valid cfg-file is: ' + ' '*len_cfg_dir + os.path.basename(ppg_glbls.cfg_path)
    # mssge += ' The new files have a timestamp  >' + ppg_glbls.main_name[:-3] + '_YYYY_MM_DD-hh_mm_ss.py<.'
    mssge += '\n'
    mssge += '\n You may configure the comand line _args_     of >' + ppg_glbls.main_name + '<  via:  >new_prog_args.cfg<'
    mssge += '\n  ... but run >pyprogen.py< again!'
    mssge += '\n'
    mssge += '\n You may configure the comand line _defaults_ of >' + ppg_glbls.main_name + '<  via:  >' + cfg_path + '<'
    mssge += '\n >' + cfg_path + '<  will be preserved, if changed. '
    mssge += '\n'
    # mssge += '\n newer generated files will have a timestamp in their filename: >' + ppg_glbls.main_name[:-3] + '_YYYY_MM_DD-hh_mm_ss.py<.'
    # mssge += '\n'
    mssge += '\n Do not change the >' + ppg_glbls.lib_dir + '\*.py< files!'
    mssge += '\n'
    # mssge += '\n'
    print (mssge)
    ppg_glbls.print_headline()


def p_subst_vars_in_patterns (input_dict):
    """ substitutes in code parts (input_dict) some words (xx_....) with variable names """
    pattern = dict()
    for key, patt in input_dict.iteritems():
        txt = patt.replace("xx_CAParser", ppg_glbls.CAParser_fn[:-3])
        txt =  txt.replace("xx_main", ppg_glbls.main_name[:-3])
        txt =  txt.replace("xx_parser", ppg_glbls.CAParser_func)
        txt =  txt.replace("xx_glbls", ppg_glbls.glbls_fn[:-3])
        pattern[key] = txt
    return pattern


def p_write_code(input_dict, outfile_path):
    """ writes >input_dict< to outfile """
    p_log_this('writing: ' + outfile_path)
    with open(outfile_path, 'w') as outfile:
        for key, pattern in sorted(input_dict.iteritems()):
            outfile.write(pattern)
        outfile.write('# ' + ppg_glbls.date_time_str)

def p_glbls_create():
    """ creates ./y_main/lib/y_glbls.py  """
    # fn and path of  >y_glbls.py<
    p_log_this()

    outfile_path = os.path.join(ppg_glbls.lib_dir, ppg_glbls.glbls_fn)
    p_log_this('creating: ' + outfile_path)

    txt =       ' '*4 + '# optional args(ConfArgParser):\n'
    for arg in ppg_glbls.opt_arg_vars:
        txt = txt + ' '*4 + 'arg_ns.' + arg + ' = None\n'
    txt += ' '*4 + '# positional args(ConfArgParser):\n'
    for arg in ppg_glbls.pos_arg_vars:
        txt += ' '*4 + 'arg_ns.' + arg + ' = None\n'
    txt += ' '*4 + 'return arg_ns\n'
    patterns.y_glbls[04] = txt

    # txt = '' ; patterns.y_glbls[96] = txt
    code = p_subst_vars_in_patterns (patterns.y_glbls)
    p_write_code (code, outfile_path)

def get_hash_strg(txt_line):
    """ rgx for >hash< inp_line / thx to: http://txt2re.com"""
    re1='(>)'	# Any Single Character 1
    re2='(([a-z0-9]*))'	# Alphanum 1
    re3='(<)'	# Any Single Character 2
    rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
    m  = rg.search(txt_line)
    if m:
        c1=m.group(1)
        alphanum1=m.group(2)
        c2=m.group(3)
        old_hash_str = alphanum1
    else:
        old_hash_str = 'NO_HASH_FOUND'
        p_log_this(old_hash_str)
    return old_hash_str


def calc_hash(txt):
    " Calculates the hash of txt"
    txt_to_hash = ''
    for line in txt:
        txt_to_hash += line
    hash_md5    = hashlib.md5()
    hash_md5.update(txt_to_hash)    # calc hash
    return hash_md5.hexdigest()


def p_cfg_calc_hash():
    """ Calculates the hash of default vars in section [defaults] 
    in >y_main_tmp.cfg<. Called after >ca_parser_make< was called,
    i.e after a new >y_main_tmp.cfg< was written."""
    
    cfg_path_new = ppg_glbls.cfg_path_tmp
    p_log_this('cfg_path_tmp  = ' + cfg_path_new)
    parser = ConfigParser.SafeConfigParser(allow_no_value=True)
    cfg_file = parser.read(cfg_path_new)
    try:  # read defaults and calc their hash
        defaults = parser.items("defaults")  # read section "defaults"
        vars_str = ''
        for key_val in defaults:   # type(defaults) == list[tuple, tuple ...]
            # vars_str += key_val[0] + key_val[1]
            vars_str += key_val[0]
    except ConfigParser.NoSectionError:
        p_log_this("No section: 'defaults' in: >" + cfg_path_new + '< !')
        return

    hash_of_vars = calc_hash(vars_str)
    return hash_of_vars

def p_cfg_write_section_signature(hash_of_vars):
    """ writes section [signature] (hash and timestamp) to >y_main_tmp.cfg<."""

    cfg_path_new = ppg_glbls.cfg_path_tmp
    p_log_this('cfg_path_tmp  = ' + cfg_path_new)

    parser = ConfigParser.SafeConfigParser(allow_no_value=True)
    cfg_file = parser.read(cfg_path_new)

    # add to >y_main_tmp.cfg< a section "signature" with hash & time_stamp
    try:
        parser.add_section("signature")
        parser.set("signature", "hash", hash_of_vars)
        parser.set("signature", "timestamp", ppg_glbls.date_time_str)
        parser.write(open(cfg_path_new, "w"))
    except ConfigParser.Error:
        p_log_this("Error writing section [signature] in: >" + cfg_path_new + '< !')
        return


def p_cfg_read_hash(cfg_path):
    """ return the val of var >hash< in cfg-file in section [signature] """
    parser = ConfigParser.SafeConfigParser(allow_no_value=True)
    # cfg_file = parser.read(cfg_path)
    parser.read(cfg_path)
    try:  # read val of var hash
        hash_val = parser.get("signature", "hash")
    except ConfigParser.NoSectionError or ConfigParser.NoOptionError:
        if ConfigParser.NoSectionError:
            p_log_this("No section: 'signature' in: >" + ppg_glbls.cfg_path + '< !')
        return
    return hash_val

def p_log_or_print_cfg_mssges(do_print = False, do_log = False):
    mssges = []
    if not ppg_glbls.cfg_exists:
        mssges.append('There is no    ' + ppg_glbls.cfg_path + ' =>')
        mssges.append('renaming:      ' + ppg_glbls.cfg_path_tmp)
        mssges.append('to:            ' + ppg_glbls.cfg_path)
    else:
        mssges.append('There is already a          >' + ppg_glbls.cfg_path + '< ')
        if ppg_glbls.cfg_changed:
            mssges.append('Since vars in [defaults] in >' + ppg_glbls.cfg_path + '<      have changed:')
            mssges.append(' => 1)     config file:     >' + ppg_glbls.cfg_path + '<      stays unchanged.')
            mssges.append('    2) new config file is:  >' + ppg_glbls.cfg_path_tmp + '<.')
            if ppg_glbls.main_changed :
                mssges.append('    3) corresponding new version of main: >' + ppg_glbls.main_new_name + '<.')
        else: # ppg_glbls.cfg_changed == False
            mssges.append('vars in [defaults] in >' + ppg_glbls.cfg_path + '< are not changed =>')

    if do_log:
        for mssge in mssges:
            p_log_this (mssge)

    if do_print:
        for mssge in mssges:
            print(mssge)


def p_cfg_check_if_modified():
    """ checks if y_main.cfg was modified (== hash of code is different) """
    # >ppg_glbls.cfg_path<  == path of cfg-file == >./y_main/cfg/y_main.cfg<

    p_log_this('cfg_path: ' + ppg_glbls.cfg_path)

    # if it was first run of pyprogen with >.new_prog.ini<:
    ppg_glbls.cfg_exists = ppg_utils.p_file_exists(ppg_glbls.cfg_path)

    # there is no >y_main.cfg<:
    if not ppg_glbls.cfg_exists:
        # rename >y_main_tmp.cfg< to >y_main.cfg<
        os.rename(ppg_glbls.cfg_path_tmp, ppg_glbls.cfg_path)
        # ppg_glbls.cfg_path_tmp = ppg_glbls.cfg_path
        # ppg_glbls.cfg_path_tmp = ''
    else: # there is already a >y_main.cfg< => compare hashes:
        hash_of_old_vars = p_cfg_read_hash(ppg_glbls.cfg_path)     # >y_main.cfg<
        p_log_this('hash_of_old_vars =' + hash_of_old_vars)
        hash_of_new_vars = p_cfg_read_hash(ppg_glbls.cfg_path_tmp) # >y_main_tmp.cfg<
        p_log_this('hash_of_new_vars =' + hash_of_new_vars)

        # if (hash_of_new_vars == hash_of_old_vars )
        if (hash_of_old_vars == hash_of_new_vars):
            ppg_glbls.cfg_changed = False
            # shutil.move(ppg_glbls.cfg_path_tmp, ppg_glbls.cfg_path)
            ppg_glbls.cfg_path_tmp = ppg_glbls.cfg_path
        else:  # act_hash != old_hash
            ppg_glbls.cfg_changed = True

    p_log_or_print_cfg_mssges(do_print = False, do_log = True)

def p_cfg_find_identical_hash(hash):
    """"find in dir >ppg_glbls.cfg_fn< files >y_main*.cfg< with identical hash-values"""
    list_of_cfg_identical_hash   = []  # list of >y_main_timestamp.cfg< with identical hash

    glob_path = os.path.join(ppg_glbls.cfg_dir, ppg_glbls.cfg_fn)
    glob_path = glob_path[:-len('.cfg')] + '*.cfg' # == >.../y_main_*.cfg<

    for fn in glob.glob(glob_path):
        tmp_hash = p_cfg_read_hash(fn)
        if tmp_hash == hash:
            list_of_cfg_identical_hash.append(fn)

    return list_of_cfg_identical_hash


def p_cfg_clear_versions():
    """ finds and deletes >y_main_timestamp.cfg< with hash identical to >y_main_tmp.cfg< """

    p_log_this()
    p_log_this('cfg_path:    ' + ppg_glbls.cfg_path)

    # create hash for vars in >y_main_tmp.cfg<
    hash_of_vars = p_cfg_calc_hash()
    # write hash_of_vars in section [signature] in >y_main_tmp.cfg<
    p_cfg_write_section_signature(hash_of_vars)

    p_cfg_check_if_modified()  # check if >./y_main/y_main.cfg exists<

    list_of_cfg_w_identical_hash = p_cfg_find_identical_hash(hash_of_vars)
    if not ppg_glbls.cfg_path_tmp in list_of_cfg_w_identical_hash:
        pass
        ppg_utils.p_terminal_mssge_error('p_cfg_clear_versions: no >' + ppg_glbls.cfg_path_tmp + '<' )
    else:
        list_of_cfg_w_identical_hash.remove(ppg_glbls.cfg_path_tmp)
        p_delete_files_in_list(list_of_cfg_w_identical_hash)


def p_find_files_w_identical_hash(file_path, hash):
    """"find in >file_path< files with identical hash-str in line 1 or 2 or .. 5"""
    list_of_files_w_identical_hash = [] # list of >y_main_timestamp.py< with identical hash
    lngth = len(ppg_glbls.date_time_str + '.py')  # == length of timestamp
    file_path = file_path[:-lngth]  # == .../y_main_*
    line_max = 6 # search hash in first 5 lines
    for fn in glob.glob(file_path + '*.py'):
        hash_found = False
        line_cnt = 1
        with open(fn) as fp:
            for line in fp:
                hash_found = hash in line
                if (line_cnt > line_max):    # hash isn't found in line_max lines
                    break
                if hash_found:
                    list_of_files_w_identical_hash.append(fn)
                    break
                line_cnt += 1
    return list_of_files_w_identical_hash


def p_delete_files_in_list(list_of_paths):
    """"find in dir >outfile_path< files with identical hash-values in line 1 .. 5"""
    for fn in list_of_paths:
        ppg_utils.p_file_delete(fn)


def p_eval_confargs_make_code():
    # create code of function >eval_confargs()< in: >y_main.py<
    # make code txt for >if<'s for >confarg_vars< as of >new_prog_args.cfg<
    txt  = '\n'
    txt += 'def eval_confargs():\n'
    txt += '    p_log_this()\n'
    txt += '    # xx_glbls.print_arg_ns()\n'
    txt += '    # eval cmd-line args and/or conf-file args (always read by ConfArgParser):\n'

    for arg in ppg_glbls.opt_arg_vars:
        txt +=  '    if ' + 'confargs.' + arg + ' == confargs.' + arg + ':\n'
        txt +=  '        evaluate(confargs.' + arg +')\n'
        txt += '\n'
    return txt


def p_main_make_code():
    # create code of new main program: >y_main.py<
    # - Some variables (and their logic) in the new >y_main.py< are
    # generated according to the parameters in >new_prog_args.cfg<.
    # - Additionally some variable names are adjusted.
    # - Program code is made mainly by copying text from dict
    # >patterns.y_main[]<  (in module >ppg_patterns.py<) to the
    # new >y_main.py< program code.
    # >ppg_patterns.py< is a _dict_ whose elements contain parts of
    # program patterns.

    patterns.y_main[10] = p_eval_confargs_make_code()

    # make code txt for optional reading of cfg-file via
    # xx_CAParser.xx_parser('--conf-file', 'ppg_glbls.cfg_path')
    # (and adjust dir of config-file by removing highest dir level:)
    adjusted_cfg_path = adjust_cfg_path(ppg_glbls.cfg_path)
    txt =  ' '*4 + "# optional reading of cfg-file: (r' == raw string) \n"
    txt += ' '*4 + "# xx_CAParser.xx_parser('--conf-file', r'"
    txt += str(adjusted_cfg_path)
    txt += "')" + '\n'
    patterns.y_main[84] = txt       # add txt to pattern

    # adjust some var names in >patterns.y_main< .
    patterns.y_main = p_subst_vars_in_patterns(patterns.y_main)

    # now code for >y_main< is complete. => put code together:
    # stick all elements of dict >patterns.y_main< in one
    # new str-var: >code_lines<
    code_lines = ''
    for key, line in sorted(patterns.y_main.iteritems()):
        code_lines += line
    return code_lines


def p_check_via_hash_if_modified(file_path):
    """ check if >file_to_check< was modified ==  (hash != hash_str in line 3) """
    file_to_check = ppg_utils.p_file_open(file_path, mode ='r')
    if not file_to_check:
        return False
    with file_to_check:
        code_lines = file_to_check.readlines()

    code_line = code_lines[0]    # line 0 contains coding, i.e.: -*- coding: utf-8 -*-
    date_line = code_lines[1]    # line 1 contains date-time string
    hash_line = code_lines[2]    # line 2 contains hash-str (of code_lines 3 to n-1) at moment of generating

    hashstr_of_code = get_hash_strg(hash_line)     # get hash str in line #3
    # calc hash of code, i.e. of hash all code_lines, ignoring first 3 code_lines and last line:
    hash_of_code    = calc_hash(code_lines[3:-1])

    # identical hash values?
    if hashstr_of_code != hash_of_code:
        mssge = ('>' + file_path + '< has been modified')
        p_log_this (mssge) # ; print mssge
        # ppg_glbls.main_changed = True
        return True
    else:
        p_log_this ('>' + file_path + '<  + is unchanged')
        # ppg_glbls.main_changed = False
        return False


def p_calc_hash_add_hash_str(code_lines):
    # calculate hash:
    hash_of_new_codelines = calc_hash(code_lines)  # calculate hash of code

    # Add hash as heading line to the code:
    code_dict    = dict()     # p_write_code wants dict as input

    txt  = '# -*- coding: utf-8 -*-\n'
    txt += ('# ' + ppg_glbls.date_time_str + ' generated by: >pyprogen.py<\n')

    code_dict[0]  = txt
    code_dict[1]  = '# >' + hash_of_new_codelines + '< \n'    # third line of >y_main.py<
    code_dict[2]  = code_lines
    return code_dict, hash_of_new_codelines


def p_code_make():
    """ create >./y_main/y_main.py< or >./y_main/eval_confargs.py< """

    # ppg_glbls.main_dir is dir of >y_main.py< AND of >eval_confargs.py<
    f_dir = ppg_glbls.main_dir

    # First run: there is no >y_main.py<
    if not ppg_utils.p_file_exists(ppg_glbls.main_path):
        f_new_name     = ppg_glbls.main_name
        f_new_path     = os.path.join(f_dir, f_new_name)

        p_log_this('creating: ' + f_new_path)

        ppg_glbls.main_new_name = f_new_name
        ppg_glbls.main_new_path = f_new_path
        ppg_glbls.main_changed  = True
        code_lines = p_main_make_code()
    else:
        f_path         = ppg_glbls.confarg_path
        f_new_name     = ppg_glbls.confarg_name
        f_new_path = os.path.join(f_dir, f_new_name)
        f_changed      = p_check_via_hash_if_modified(f_path)
        ppg_glbls.confarg_new_name = f_new_name
        ppg_glbls.confarg_new_path = f_new_path
        ppg_glbls.confarg_changed  = f_changed

        code_lines = p_eval_confargs_make_code()
        pass

    p_log_this('creating: ' + f_new_path)

    ppg_glbls.code_new_name = f_new_name
    ppg_glbls.code_new_path = f_new_path

    # if there is/are existing >f_name_TIMESTAMP.py< with identical hash:
    # remember their names to delete them later:
    code_dict, hash_of_new_codelines = p_calc_hash_add_hash_str(code_lines)
    list_of_files_w_identical_hash = []
    list_of_files_w_identical_hash = p_find_files_w_identical_hash(f_new_path, hash_of_new_codelines)
    if list_of_files_w_identical_hash:
        p_delete_files_in_list (list_of_files_w_identical_hash)

    # write >y_main.py< respectively >eval_confargs_+/-timestamp.py< :
    p_write_code (code_dict, f_new_path)


if __name__ == "__main__":
    print ppg_glbls.main_name
    # ppg_utils.p_terminal_mssge_note_this()
    ppg_utils.p_exit()
