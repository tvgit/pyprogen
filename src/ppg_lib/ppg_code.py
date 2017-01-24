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
# prog_name = y_main
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
    cfg_path = os.path.join(dir_cfg, cfg_fn)     # cfg_path_new of >pyprogen.py< !
    cfg_path = os.path.normpath(cfg_path)        #      not of >y_main.py<  !!
    parser = ConfigParser.SafeConfigParser(allow_no_value=True)
    p_log_this('cfg_path_new: ' + cfg_path)
    cfg_file = parser.read(cfg_path)
    p_log_this('cfg file: ' + str(cfg_file))

    # ppg_glbls.prog_name
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
        ppg_glbls.prog_name = 'default_main.py'
        p_log_this('no >prog_name< in: ' + cfg_path + ' !')
        p_log_this('prog_name set to: ' + ppg_glbls.prog_name)

    # ppg_glbls.prog_path
    ppg_glbls.prog_path = os.path.normpath(ppg_glbls.prog_name[:-3])
    p_log_this("prog_path = " + ppg_glbls.prog_path)

    # ppg_glbls.prefix
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

    # ppg_glbls.date_time_str
    ppg_glbls.date_time_str = ppg_utils.p_make_act_date_str()
    # filename of globals of created program
    ppg_glbls.glbls_fn      = ppg_glbls.prefix + 'glbls.py'    # globals of ! >y_main.py< !
    # ppg_glbls.glbls_path    = os.path.join(ppg_glbls.lib_dir, ppg_glbls.glbls_fn)
    print ppg_glbls.lib_dir
    ppg_glbls.glbls_path    = os.path.join('xxxxxx', ppg_glbls.glbls_fn)



def p_inform_about_paths_and_filenames():
    cfg_path = os.path.join(ppg_glbls.cfg_dir, ppg_glbls.cfg_fn)

    headline = '\n' + '-'*10 + ' ' + ppg_glbls.prog_name_new + ' ' + '-' * 60 + '\n'


    mssge  = ''
    mssge += headline
    len_dir_main = len(ppg_glbls.main_dir) + 1
    mssge += '\n Filename of YOUR code is:    ' + ' '*len_dir_main + ppg_glbls.prog_name
    mssge += '\n Dir  of YOUR code is:        ' + os.path.join(ppg_glbls.main_dir, '')
    mssge += '\n Path of YOUR code is:        ' + os.path.join(ppg_glbls.main_dir, ppg_glbls.prog_name)
    mssge += '\n'
    mssge += '\n Filename of new version is:  ' + ' '*len_dir_main + ppg_glbls.prog_name_new
    mssge += '\n Dir  of new version is:      ' + os.path.join(ppg_glbls.main_dir, '')
    mssge += '\n Path of new version is:      ' + os.path.join(ppg_glbls.main_dir, ppg_glbls.prog_name_new)
    # mssge += '(>' + ppg_glbls.prog_name + '< was not changed.)'
    # cfg_path_new
    mssge += '\n'
    len_cfg_dir = len(os.path.dirname(ppg_glbls.cfg_path_new)) + 1
    mssge += '\n Path of new cfg-file is:     ' + ppg_glbls.cfg_path_new
    mssge += '\n Filename of new cfg-file is: ' + ' '*len_cfg_dir + os.path.basename(ppg_glbls.cfg_path_new)
    # mssge += ' The new files have a timestamp  >' + ppg_glbls.prog_name[:-3] + '_YYYY_MM_DD-hh_mm_ss.py<.'
    mssge += '\n'
    mssge += '\n You may configure the comand line _args_     of >' + ppg_glbls.prog_name + '<  via:  >new_prog_args.cfg<'
    mssge += '\n  ... but run >pyprogen.py< again!'
    mssge += '\n You may configure the comand line _defaults_ of >' + ppg_glbls.prog_name + '<  via:  >' + cfg_path + '<'
    mssge += '\n >' + cfg_path + '<  will be preserved, if changed. '
    mssge += '\n'
    mssge += '\n  newer generated files will have a timestamp in their filename: >' + ppg_glbls.prog_name[:-3] + '_YYYY_MM_DD-hh_mm_ss.py<.'
    mssge += '\n'
    mssge += '\n Do not change the >' + ppg_glbls.lib_dir + '\*.py< files!'
    mssge += '\n'
    mssge += headline
    mssge += '\n'
    print (mssge)


# def p_create_paths_and_fns():
#     """ creates later needed filename  """
#     # globals of ! >y_main.py< !
#     ppg_glbls.glbls_fn      = ppg_glbls.prefix + 'glbls.py'
#     # name of parser func in >y_CAParser<
#     # ppg_glbls.CAParser_func = ppg_glbls.prefix + 'parser'


def p_subst_vars_in_patterns (input_dict):
    """ substitutes in code parts (input_dict) some words (xx_....) with variable names """
    pattern = dict()
    for key, patt in input_dict.iteritems():
        txt = patt.replace("xx_CAParser", ppg_glbls.CAParser_fn[:-3])
        txt =  txt.replace("xx_main", ppg_glbls.prog_name[:-3])
        txt =  txt.replace("xx_parser", ppg_glbls.CAParser_func)
        txt =  txt.replace("xx_glbls", ppg_glbls.glbls_fn[:-3])
        pattern[key] = txt
    return pattern


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
    outfile_path = os.path.join(ppg_glbls.lib_dir, ppg_glbls.glbls_fn)
    p_log_this('creating: ' + outfile_path)

    txt =       ' '*4 + '# optional args(ConfArgParser):\n'
    for arg in ppg_glbls.opt_arg_vars:
        txt = txt + ' '*4 + 'arg_ns.' + arg + ' = None\n'
    txt = txt + ' '*4 + '# positional args(ConfArgParser):\n'
    for arg in ppg_glbls.pos_arg_vars:
        txt = txt + ' '*4 + 'arg_ns.' + arg + ' = None\n'
    txt = txt + ' '*4 + 'return arg_ns\n'
    patterns.y_glbls[04] = txt

    # txt = '' ; patterns.y_glbls[96] = txt
    code = p_subst_vars_in_patterns (patterns.y_glbls)
    p_write_code (code, outfile_path)

def p_get_hash_strg(txt_line):
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


def calc_hash_of_text(txt):
    " Calculates the hash of txt"
    txt_to_hash = ''
    for line in txt:
        txt_to_hash += line

    hash_md5    = hashlib.md5()
    hash_md5.update(txt_to_hash)    # calc hash
    return hash_md5.hexdigest()


def p_cfg_create_hash():
    """ Calculates the hash of default vars in section [defaults] in >y_main.cfg<.
    Then creates in >y_main.cfg< the section [signature] with items:
    >timestamp< and >hash<.
    Called by >pyprogen.py< after >ca_parser_make< was called,
    i.e after a new >y_main_TimeStamp.cfg< was written."""

    p_log_this('cfg_path_new     = ' + ppg_glbls.cfg_path_new)

    parser = ConfigParser.SafeConfigParser(allow_no_value=True)
    cfg_file = parser.read(ppg_glbls.cfg_path_new)
    try:  # read defaults and calc their hash
        defaults = parser.items("defaults")  # read section "defaults"
        vars_str = ''
        for key_val in defaults:   # type(defaults) == list[tuple, tuple ...]
            # vars_str += key_val[0] + key_val[1]
            vars_str += key_val[0]
        hash_of_vars = calc_hash_of_text(vars_str)
    except ConfigParser.NoSectionError:
        p_log_this("No section: 'defaults' in: >" + ppg_glbls.cfg_path_new + '< !')
        return

    # add to >y_main.cfg< a section "signature" with hash & time_stamp
    parser.add_section("signature")
    parser.set("signature", "hash", hash_of_vars)
    parser.set("signature", "timestamp", ppg_glbls.date_time_str)
    parser.write(open(ppg_glbls.cfg_path_new, "w"))
    return hash_of_vars

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

def p_cfg_check_if_modified():
    """ checks if y_main.cfg was modified (== hash of code is different) """
    p_log_this('cfg_path:      ' + ppg_glbls.cfg_path)

    mssges    = ['']*3 # dict of mssges
    dest_path = ppg_glbls.cfg_path
    mssges[0] = ('')
    mssges[1] = ('renaming:      ' + ppg_glbls.cfg_path_new)
    mssges[2] = ('to:            ' + dest_path)

    # if there is no >y_main.cfg<:
    if not ppg_utils.p_file_exists (ppg_glbls.cfg_path):
        dest_path = ppg_glbls.cfg_path
        mssges[0] = ('There is no    ' + ppg_glbls.cfg_path + ' =>')
        for mssge in mssges:
            p_log_this (mssge)
        # move source to dest:
        shutil.move(ppg_glbls.cfg_path_new, dest_path)
        ppg_glbls.cfg_path_new = dest_path
        ppg_glbls.cfg_file_tmp = ppg_glbls.cfg_fn
        return

    # if there is already a >y_main.cfg<:
    hash_of_old_defaults = p_cfg_read_hash(ppg_glbls.cfg_path)     # >y_main.cfg<
    p_log_this('hash_of_old_defaults =' + hash_of_old_defaults)
    hash_of_new_defaults = p_cfg_read_hash(ppg_glbls.cfg_path_new) # >y_main_TimeStamp.cfg<
    p_log_this('hash_of_new_defaults =' + hash_of_new_defaults)

    # if (act_hash == old_hash)
    if (hash_of_new_defaults == hash_of_old_defaults):
        mssges[0] = ('vars in [defaults] in >' + ppg_glbls.cfg_path + '< are not changed =>')
        shutil.move(ppg_glbls.cfg_path_new, dest_path)
        ppg_glbls.cfg_path_new = dest_path
        ppg_glbls.cfg_file_tmp = ppg_glbls.cfg_fn
    else:  # act_hash != old_hash
        mssges[0] = ('vars in [defaults] in >' + ppg_glbls.cfg_path + '< have been modified.')
        mssges[1] = (' => 1) leave >' + ppg_glbls.cfg_path + '< unchanged.')
        mssges[2] = ('    2) write new version of config file: >' + ppg_glbls.cfg_path_new + '<.')
        ppg_glbls.cfg_changed = True

    for mssge in mssges:
        p_log_this (mssge)
    for mssge in mssges:
        print(mssge)

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
    """ finds and deletes >y_main_timestamp.cfg< with identical hash
    """

    p_log_this('cfg_path:      ' + ppg_glbls.cfg_path)
    hash = p_cfg_create_hash() # create hash for vars in most recent >y_main_TimeStamp.cfg<
    p_cfg_check_if_modified()  # check if >./y_main/y_main.cfg exists<

    list_of_cfg_w_identical_hash = p_cfg_find_identical_hash(hash)

    if not ppg_glbls.cfg_path_new in list_of_cfg_w_identical_hash:
        ppg_utils.p_error()
    else:
        list_of_cfg_w_identical_hash.remove(ppg_glbls.cfg_path_new)
        p_delete_files_in_list(list_of_cfg_w_identical_hash)


def p_main_find_identical_hash(y_main_path, hash):
    """"find in dir >y_main_path< files with identical hash-values in line 1 .. 5"""
    list_of_y_main_identical_hash = [] # list of >y_main_timestamp.py< with identical hash
    lngth = len(ppg_glbls.date_time_str + '.py')
    y_main_path = y_main_path[:-lngth]  # == .../y_main_*
    line_max = 6 # search hash in first 5 lines
    for fn in glob.glob(y_main_path + '*.py'):
        hash_found = False
        line_cnt = 1
        with open(fn) as fp:
            for line in fp:
                hash_found = hash in line
                if (line_cnt > line_max):    # hash isn't found in line_max lines
                    break
                if hash_found:
                    list_of_y_main_identical_hash.append(fn)
                    break
                line_cnt += 1
    return list_of_y_main_identical_hash


def p_delete_files_in_list(list_of_paths):
    """"find in dir >outfile_path< files with identical hash-values in line 1 .. 5"""
    for fn in list_of_paths:
        ppg_utils.p_file_delete(fn)


def p_main_check_if_modified(y_main_path):
    """ check if y_main.py was modified (== hash of code is different) """
    old_main_file = ppg_utils.p_file_open(y_main_path, mode ='r')
    if not old_main_file:
        return False
    with old_main_file:
        code_lines = old_main_file.readlines()
    # ppg_utils.p_file_close(old_main_file)

    code_line = code_lines[0]    # line 0 contains coding, i.e.: -*- coding: utf-8 -*-
    date_line = code_lines[1]    # line 1 contains date-time string
    hash_line = code_lines[2]    # line 2 contains hash (of code_lines 3 to n-1) at moment of generating

    # calc hash of code, i.e. of hash all code_lines, ignoring first 3 code_lines and last line:
    hash_of_new_code = calc_hash_of_text(code_lines[3:-1])
    hash_of_old_code = p_get_hash_strg(hash_line)  # get hash at moment of generating

    # identical hashes?
    if hash_of_old_code != hash_of_new_code:
        mssge = ('>' + y_main_path + '< has been modified')
        p_log_this (mssge) # ; print mssge
        ppg_glbls.prog_changed = True
        return True
    else:
        p_log_this ('>' + y_main_path + '<  + is unchanged')
        ppg_glbls.prog_changed = False
        return False

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

    # Make code for >def evaluate_opt_args():< in >y_main.py<
    # make code txt for >if<'s for >confarg_vars< as of >new_prog_args.cfg<
    txt = ' '*4 + '# optional args(ConfArgParser):\n'
    for arg in ppg_glbls.opt_arg_vars:
        txt +=  ' '*4 + 'if ' + 'confargs.' + arg + ' == confargs.' + arg + ':\n'
        txt +=  ' '*8 + 'eval_arg(confargs.' + arg +')\n'
        txt +=  '\n'
    patterns.y_main[10] = txt       # add txt to pattern

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


def p_main_make():
    # create code_lines > calc hash of code_lines
    code_lines = p_main_make_code()

    # => calculate hash:
    # hash_of_old_defaults
    hash_of_new_codelines = calc_hash_of_text(code_lines)  # calculate hash of code

    # Add hash as heading line to the code:
    code_dict    = dict()     # p_write_code wants dict as input
    code_dict[1] = '# >' + hash_of_new_codelines + '< \n'    # second line of y_main.py
    code_dict[2] = code_lines

    new_main_fn   = ppg_glbls.prog_name  # fn and path of future >y_main.py<
    new_main_path = os.path.join(ppg_glbls.main_dir, new_main_fn)
    p_log_this('creating: ' + new_main_path)

    # if existing >y_main.py<  was modified => new >y_main.py< becomes >y_main_TIMESTAMP.py<
    # if          >y_main.cfg< was modified => new >y_main.py< becomes >y_main_TIMESTAMP.py<
    if p_main_check_if_modified(new_main_path) or ppg_glbls.cfg_changed:
        new_main_path = new_main_path[:-3] + '_' + ppg_glbls.date_time_str + '.py'
        ppg_glbls.prog_name_new = os.path.basename(new_main_path)

    # if there is/are existing >y_main_TIMESTAMP.py< with identical hash:
    # remember their names to delete them later:
    list_of_main_w_identical_hash = []
    list_of_main_w_identical_hash = p_main_find_identical_hash(new_main_path, hash_of_new_codelines)

    # Now finally write code of new >y_main(_+/-timestamp.py<
    # and add timestamp in first line & lastline
    p_write_code (code_dict, new_main_path)  # write >y_main(_+/-timestamp.py<

    if list_of_main_w_identical_hash:
        p_delete_files_in_list (list_of_main_w_identical_hash)


if __name__ == "__main__":
    print ppg_glbls.prog_name
    # ppg_utils.p_note_this()
    # ppg_utils.p_note_this()
    ppg_utils.p_exit()
