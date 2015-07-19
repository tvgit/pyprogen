#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'rh'
__date__ = "$18.07.2015 15:55:22$"

import os
import string
import ConfigParser  # read configfile

import p_glbls  # share global values
import p_utils
from   p_log import p_log_this
import p_cfg.patterns as patterns

# may be used in: def p_read_ini():
pyprogen_ini = """
[properties]
prog_name = y_main
"""


def p_read_ini(dir_cfg='.', cfg_fn='pyprogen.ini'):
    """ reads defaults for generated program: name ..."""
    # http://www.karoltomala.com/blog/?p=622
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    print 'p_read_ini: dir_path = ', p_utils.p_act_dir_path()
    print 'p_read_ini: dir_path = ',  dir_path

    p_log_this()
    print p_glbls.my_name()
    # print '>>>>', p_glbls.prog_name
    cfg_path = os.path.join(dir_cfg, cfg_fn)
    cfg_path = os.path.normpath(cfg_path)
    parser = ConfigParser.SafeConfigParser(allow_no_value=True)
    # parser.readfp(io.BytesIO(pyprogen_ini))
    p_log_this('cfg_path: ' + cfg_path)
    cfg_file = parser.read(cfg_path)
    p_log_this('cfg file: ' + str(cfg_file))

    p_glbls.prog_name = parser.get("properties", "prog_name")
    p_log_this('prog_name = ' + p_glbls.prog_name)
    if not p_glbls.prog_name:
        p_glbls.prog_name = 'z_main'
        p_log_this('no >prog_name< in: ' + cfg_path + ' !')
        p_log_this('prog_name -> ' + p_glbls.prog_name)

    if (len(p_glbls.prog_name) < 4):
        p_glbls.prog_name = p_glbls.prog_name + '.py'
        p_log_this('          =>' + p_glbls.prog_name)
    if ((string.lower(p_glbls.prog_name[-3:])) <> '.py'):
        p_glbls.prog_name = p_glbls.prog_name + '.py'
        p_log_this('          =>' + p_glbls.prog_name)

    p_glbls.prog_path = os.path.normpath(p_glbls.prog_name[:-3])
    print 'p_read_ini: p_glbls.prog_path = ', p_glbls.prog_path
    p_log_this("prog_path = " + p_glbls.prog_path)

    p_glbls.prefix = p_glbls.prog_name[0] + '_'  # prefix for generated program

    p_glbls.patterns_fn = parser.get("properties", "patterns")
    p_glbls.patterns_path = os.path.join('.', 'p_cfg', p_glbls.patterns_fn)
    # p_glbls.patterns_path = os.path.normpath(p_glbls.patterns_path)


def p_glbls():
    """ creates y_glbls.py """
    p_log_this()
    outfile_fn = p_glbls.prefix + 'glbls.py'
    outfile_path = os.path.join(p_glbls.dir_lib, outfile_fn)

    y_glbls_02 = patterns.y_glbls_02
    y_glbls_04 = patterns.y_glbls_04
    y_glbls_96 = patterns.y_glbls_96
    y_glbls_98 = patterns.y_glbls_98

    # ??? p_main(): >p_glbls.CAParser_path = outfile_path<

    now_str = p_utils.p_make_act_date_str()
    with open(outfile_path, 'w') as outfile:
        outfile.write('# ' + now_str + ' generated by: >pyprogen.py<')
        y_glbls_02 = y_glbls_02.replace("xx_main", p_glbls.prog_name[:-3])
        y_glbls_02 = y_glbls_02.replace("xx_CAParser", p_glbls.CAParser_fn[:-3])
        y_glbls_02 = y_glbls_02.replace("xx_parser", p_glbls.CAParser_func)
        outfile.write(y_glbls_02)

        y_glbls_98 = y_glbls_98.replace("xx_main", p_glbls.prog_name[:-3])
        outfile.write(y_main_98)

        outfile.write('# ' + now_str)


def p_main():
    """ creates y_main.py """
    p_log_this()
    y_main_02 = patterns.y_main_02
    y_main_04 = patterns.y_main_04
    y_main_96 = patterns.y_main_96
    y_main_98 = patterns.y_main_98

    outfile_fn = p_glbls.prog_name
    outfile_path = os.path.join(p_glbls.dir_main, outfile_fn)
    # p_glbls.prog_path = outfile_path

    now_str = p_utils.p_make_act_date_str()
    with open(outfile_path, 'w') as outfile:
        outfile.write('# ' + now_str + ' generated by: >pyprogen.py<')
        y_main_02 = y_main_02.replace("xx_main", p_glbls.prog_name[:-3])
        y_main_02 = y_main_02.replace("xx_CAParser", p_glbls.CAParser_fn[:-3])
        y_main_02 = y_main_02.replace("xx_parser", p_glbls.CAParser_func)
        outfile.write(y_main_02)

        y_main_98 = y_main_98.replace("xx_main", p_glbls.prog_name[:-3])
        outfile.write(y_main_98)

        outfile.write('# ' + now_str)

if __name__ == "__main__":
    print p_glbls.my_name()
    p_utils.p_exit()
