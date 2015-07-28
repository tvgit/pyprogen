#! /usr/bin/python
# -*- coding: utf-8 -*-

# https://parezcoydigo.wordpress.com/2012/08/04/from-argparse-to-dictionary-in-python-2-7/
# http://stackoverflow.com/questions/16878315/what-is-the-right-way-to-treat-python-argparse-namespace-as-a-dictionary

__author__ = "rh"
__date__ = "$02.07.2015 21:55:22$"

import StringIO
import re
import os

import p_code
import p_glbls
import p_utils
import p_code
from   p_log   import p_log_this
import p_cfg.patterns as patterns


def make_regex_opt_arg_minus():
    """ '-f' // thx to http://txt2re.com !"""
    re1='(\')'	# Any Single Character 1
    re2='(-)'	# Any Single Character 2
    re3='([a-z])'	# Any Single Word Character (Not Whitespace) 1
    re4='(\')'	# Any Single Character 3
    rgx_minus = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)
    return rgx_minus


def make_regex_opt_arg_minus_minus():
    """ '--foo' // thx to http://txt2re.com !"""
    re1='(\')'	# Any Single Character 1
    re2='(-)'	# Any Single Character 2
    re3='(-)'	# Any Single Character 3
    # re4='((?:[a-z][a-z]+))'	# Word 1
    re4='((?:[a-z][a-z0-9_]*))'	# Variable Name 1
    re5='(\')'	# Any Single Character 4
    rgx_minus_minus = re.compile(re1+re2+re3+re4+re5,re.IGNORECASE|re.DOTALL)
    return rgx_minus_minus


def make_regex_pos_arg():
    """ 'bar' // thx to http://txt2re.com !"""
    re1='(\')'	# Any Single Character 1
    # re4='((?:[a-z][a-z]+))'	# Word 1
    re4='((?:[a-z][a-z0-9_]*))'	# Variable Name 1
    re5='(\')'	# Any Single Character 4  >'<
    rgx_pos_arg = re.compile(re1+re4+re5,re.IGNORECASE|re.DOTALL)
    return rgx_pos_arg

def p_subst_vars_in_patterns (input_dict):
    """ substitutes in code parts (input_dict) some words (xx_....) with variable names """
    patts = dict()
    for key, patt in input_dict.iteritems():
        txt = patt.replace("xx_CAParser", p_glbls.CAParser_fn[:-3])
        txt =  txt.replace("xx_main",     p_glbls.prog_name[:-3])
        txt =  txt.replace("xx_glbls",    p_glbls.glbls_fn[:-3])
        txt =  txt.replace("xx_parser",   p_glbls.CAParser_func)
        txt =  txt.replace("xx_program_name", p_glbls.prog_name)
        txt =  txt.replace("xx_dir_log",  p_glbls.dir_log)
        patts[key] = txt
    return patts


def p_ConfArgParser(conf_file_fn='./pyprogen.conf'):
    """ creates >y_CAParser.py<; executes it, to generate a conf file >y_main.cfg< for >y_main.py<  """
    p_log_this(conf_file_fn)
    opt_args             = []  # local list of opt-args
    pos_args             = []  # local list of pos-args
    # >p_ConfArgParser< sets vars in p_glbls. ... for later use in >p_code.p_globals<
    p_glbls.opt_arg_vars = []  # list (in p_glbls) of opt-args
    p_glbls.pos_arg_vars = []  # list (in p_glbls) of pos-args

    opt_arg_lines      = []  # lines with optional args
    pos_arg_lines      = []  # lines with positional args
    # regex: searching for whitespace
    rgx_whitespace = re.compile(r'\s+')
    # regex: searching for optional (== non-positional) args:
    rgx_minus       = make_regex_opt_arg_minus()         # regex vs. >('-f',<
    rgx_minus_minus = make_regex_opt_arg_minus_minus()   # regex vs. >('--foo',<
    # regex: searching for optional (== non-positional) args:
    rgx_pos_arg     = make_regex_pos_arg()               # regex vs. >('bar',<

    # in conf_file search for (non comment) lines with positional / optional args
    with open(conf_file_fn, 'r') as infile:
        for line in infile:
            line.lstrip()
            if not line.startswith('#'):
                # remove whitespace lines:
                line_test = re.sub(rgx_whitespace, '', line)
                if line_test:
                    match_minus_minus = rgx_minus_minus.search(line)
                    match_minus       = rgx_minus.search(line)
                    match_pos_arg     = rgx_pos_arg.search(line)
                    if match_minus_minus:
                        group_0 = match_minus_minus.group(0)[:-1].lstrip()
                        if len (group_0) > 2:
                            # p_glbls.opt_arg_vars.append(group_0[3:])
                            opt_args.append(group_0[1:])
                        opt_arg_lines.append(line)
                    elif match_minus:
                        group_0 = match_minus.group(0)[:-1].lstrip()
                        if len (group_0) > 1:
                            # p_glbls.opt_arg_vars.append(group_0[2:])
                            opt_args.append(group_0[1:])
                        opt_arg_lines.append(line)
                    elif match_pos_arg:
                        group_0 = match_pos_arg.group(0)[:-1].lstrip()
                        if len (group_0) > 2:
                            # p_glbls.pos_arg_vars.append(group_0[1:])
                            pos_args.append(group_0[1:])
                        pos_arg_lines.append(line)

    # strip '-' or '--' from opt_args and copy them to >p_glbls.opt_arg_vars<
    for arg in opt_args:
        p_glbls.opt_arg_vars.append(arg.lstrip('-'))
    # copy opt_args to >p_glbls.opt_arg_vars<
    for arg in pos_args:
        p_glbls.pos_arg_vars.append(arg)

    # generate lines with pos args like: >parser.add_argument('bar', type=file)<
    txt = ''
    for line in pos_arg_lines:
        txt = txt + '    ' + line # + '\n'
    # generate lines with pos args like: >parser.add_argument('-f', '--foo', ...)<
    for line in opt_arg_lines:
        txt = txt + line # + '\n'

    patterns.CA_Parser[04] = txt

    # log positional and optional arguments
    for arg in pos_args:
        p_log_this('pos. arg: ' + arg)
    for arg in opt_args:
        p_log_this('opt. arg: ' + arg)

    # write y_CAParser.py == ConfArgParser for new program
    CAParser_fn = p_glbls.prefix + 'CAParser.py'
    p_glbls.CAParser_fn = CAParser_fn
    outfile_fn = p_glbls.CAParser_fn
    p_glbls.CAParser_path = os.path.join(p_glbls.dir_lib, CAParser_fn)
    outfile_path = p_glbls.CAParser_path

    code = p_subst_vars_in_patterns (patterns.CA_Parser)
    p_code.p_write_code (code, outfile_fn, outfile_path)




# ------------------------------------

if __name__ == "__main__":
    print 'p_ConfArgParser.py '
else:
    pass
