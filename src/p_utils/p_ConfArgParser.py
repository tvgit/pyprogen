#! /usr/bin/python
# -*- coding: utf-8 -*-

# https://parezcoydigo.wordpress.com/2012/08/04/from-argparse-to-dictionary-in-python-2-7/
# http://stackoverflow.com/questions/16878315/what-is-the-right-way-to-treat-python-argparse-namespace-as-a-dictionary

__author__ = "rh"
__date__ = "$02.07.2015 21:55:22$"

import StringIO
import re
import os
import sys

import p_glbls
import p_utils
from   p_log   import p_log_this

#cfg_path = os.path.abspath(os.path.join('..', 'p_cfg'))
cfg_path = os.path.join('.', 'p_cfg')
cfg_path = os.path.normpath(cfg_path)
cfg_path = os.path.abspath(cfg_path)
sys.path.append(cfg_path)
print '>>>>>>>>>'
print cfg_path
loc_path = os.getcwd()
print loc_path

import patterns

# CA_Parser_02 = """
# import confargparse
# import argparse
# import sys
#
# def m_parser(command = '', cfg_path=''):
#     parser = confargparse.ConfArgParser(description='Program: replace_w_program_name')
#     # exclude positional args when exporting conf-file
#     if (command <> '--export-conf-file'):
# """
#
# CA_Parser_04 = """
#     if (command == '--export-conf-file'):
#         parser.parse_args(['--export-conf-file', cfg_path])
#         # ConfArgParser obviously exits? Why?
# # http://stackoverflow.com/questions/16878315/what-is-the-right-way-to-treat-python-argparse-namespace-as-a-dictionary
# # https://parezcoydigo.wordpress.com/2012/08/04/from-argparse-to-dictionary-in-python-2-7/
# """
#
# CA_Parser_96 = """
# """
#
# CA_Parser_98 = """
# if __name__ == "__main__":
#     print '-' * 20
#     print '| xx_CAParser: running'
#     cfg_path = sys.argv[1]
#     if not cfg_path:
#         print '| xx_CAParser: No config path?? '
#         cfg_path = os.path.join('.', 'main\cfg', 'conf.ini')
#         print ('| xx_CAParser: Setting config path to: ' + cfg_path)
#     else:
#         print '| conf_path= ', cfg_path
#     m_parser('--export-conf-file', cfg_path)
#     print '| xx_CAParser: end'
#     print '-' * 20
# else:
#     pass
# """

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


def p_read_pattern():
    """ gets patterns fpr CA_Parser (from ./p_cfg/patterns.py<) """
    CA_Parser_02 = patterns.CA_Parser_02
    CA_Parser_04 = patterns.CA_Parser_04
    CA_Parser_96 = patterns.CA_Parser_96
    CA_Parser_98 = patterns.CA_Parser_98


def p_ConfArgParser(conf_file_fn='./pyprogen.conf'):
    p_log_this()
    # p_read_pattern()
    CA_Parser_02 = patterns.CA_Parser_02
    CA_Parser_04 = patterns.CA_Parser_04
    CA_Parser_96 = patterns.CA_Parser_96
    CA_Parser_98 = patterns.CA_Parser_98

    opt_args             = []  # local list of opt-args
    pos_args             = []  # local list of pos-args
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

    with open(conf_file_fn, 'r') as infile:
        for line in infile:
            line.lstrip()
            if not line.startswith('#'):
                # remove whitespace lines:
                line_test = re.sub(rgx_whitespace, '', line)
                if line_test:
                    # virt_file.write(line)
                    match_minus_minus = rgx_minus_minus.search(line)
                    match_minus       = rgx_minus.search(line)
                    match_pos_arg     = rgx_pos_arg.search(line)
                    if match_minus_minus:
                        group_0 = match_minus_minus.group(0)[:-1].lstrip()
                        if len (group_0) > 2:
                            p_glbls.opt_arg_vars.append(group_0[3:])
                            opt_args.append(group_0[1:])
                        opt_arg_lines.append(line)
                    elif match_minus:
                        group_0 = match_minus.group(0)[:-1].lstrip()
                        if len (group_0) > 1:
                            p_glbls.opt_arg_vars.append(group_0[2:])
                            opt_args.append(group_0[1:])
                        opt_arg_lines.append(line)
                    elif match_pos_arg:
                        group_0 = match_pos_arg.group(0)[:-1].lstrip()
                        if len (group_0) > 2:
                            p_glbls.pos_arg_vars.append(group_0[1:])
                            pos_args.append(group_0[1:])
                        pos_arg_lines.append(line)

    virt_file = StringIO.StringIO()
    virt_file.write(CA_Parser_02.replace("replace_w_program_name", p_glbls.prog_name))

    for line in pos_arg_lines:
        virt_file.write('    ' + line)
    for line in opt_arg_lines:
        virt_file.write(line)

    virt_file.write(CA_Parser_04)
    # virt_file.write(CA_Parser_98)
    outfile_fn   = p_glbls.prefix + 'CAParser.py'
    virt_file.write(CA_Parser_98.replace("xx_CAParser", outfile_fn))

    # log positional and optional arguments
    for arg in pos_args:
        p_log_this('pos. arg: ' + arg)
    for arg in opt_args:
        p_log_this('opt. arg: ' + arg)


    # write __CAParser.py == ConfArgParser for new program
    outfile_path = os.path.join(p_utils.p_glbls.dir_lib, outfile_fn)
    p_glbls.CAParser_path = outfile_path

    now_str = p_utils.make_act_date_str()
    with open(outfile_path, 'w') as outfile:
        outfile.write('# generated by: >p_ConfArgParser.py< (' + now_str + ')')
        for line in virt_file.getvalue():
            outfile.write(line)
        outfile.write('# ' + now_str)

if __name__ == "__main__":
    print 'p_ConfArgParser.py '
    print p_utils.p_glbls.dir_cfg
    print p_utils.p_glbls.dir_lib
else:
    pass
