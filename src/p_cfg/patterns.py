# -------------- y_main.py
# (first time run of y_main.py)
# INFO       2015-07-18 20:36:05  p_log_start:  y_main.py Logging started
# INFO       2015-07-18 20:36:05  p_log_end:  y_main.py Logging end

y_main = dict()
y_main[02] = """
# YOUR code resides in THIS module.
# It is respected if changed (modification results from different
# hash code '>xxx...xxx<' in third line of source code of this module).

import lib.xx_CAParser as xx_CAParser
import lib.p_utils     as p_utils
from   lib.p_log       import p_log_init, p_log_start, p_log_this, p_log_end
import lib.xx_glbls
import copy


# 'confargs' are your configuration parameters / cmdline arguments
confargs = lib.xx_glbls.arg_ns

def print_prog_name():
    prog_name = p_utils.p_get_prog_name()
    prog_dir  = p_utils.p_get_prog_dir()
    print '-' * 8
    print 'script name:' + prog_name
    print 'script dir :' + prog_dir
    print '-' * 8

"""

y_main[04] = """
def eval_arg(arg):
    print 'do something with: ' + str(arg)
    return arg

def evaluate_opt_args():
    p_log_this()
    # xx_glbls.print_arg_ns()
"""

y_main[10] = """ """

y_main[60] = """
def main():
    p_log_this('begin')
    evaluate_opt_args()
    p_log_this('end')
"""

y_main[80] = r"""
if __name__ == "__main__":
    print_prog_name()
    p_log_init(log_dir = 'log', log_fn = r'xx_main.log')
    p_log_start()

    # http://stackoverflow.com/questions/16878315/what-is-the-right-way-to-treat-python-argparse-namespace-as-a-dictionary
    # http://stackoverflow.com/questions/2799064/how-do-i-merge-dictionaries-together-in-python

    # read commandline arguments:
    xx_CAParser.xx_parser()
    # confargs_cmd_line = copy.deepcopy(confargs)
    # print 'cmd_line: ' + str(vars(confargs_cmd_line))
    # print sorted(vars(confargs_cmd_line).items())

"""

y_main[84] = """ """


y_main[86] = """
    # confargs_cfg_file = confargs
    # print vars(confargs_cfg_file)
    # print 'cfg_file: ' + str(vars(confargs_cfg_file))
    # vars(confargs_cfg_file).update(vars(confargs_cmd_line))
    # print 'confargs: ' + str(vars(confargs_cfg_file))

    # Here YOUR 'main()' is called:
    main()

    p_log_end()
    p_utils.p_exit()
"""

# -------------- y_glbls.py

y_glbls = dict()
y_glbls[02] = """
# Sharing information via this module across >xx_main.py< and its modules
# http://stackoverflow.com/questions/13034496/using-global-variables-between-files-in-python
#
import argparse

def make_arg_ns(origin = 'unknown !?'):
    global arg_ns

    arg_ns = argparse.Namespace()
    arg_ns.__origin__ =  str(origin)
"""

y_glbls[04] = """
"""

y_glbls[10] = """

def print_arg_ns():
    global arg_ns
    for key, value in sorted (vars(arg_ns).iteritems()):
        #print "key / value =  " + key, ' * ' , value
        print "arg_ns." + str(key) + ' = ' + str(value)
"""

y_glbls[96] = """
"""

y_glbls[98] = """
if __name__ == "__main__":
    arg_ns = make_arg_ns(r'xx_glbls.py')
    print_arg_ns()
else:
    arg_ns = make_arg_ns(r'xx_glbls.py')
    pass
"""

# -------------- y_CAParser.py

CA_Parser = dict()
# import argparse

CA_Parser[02] = """
# Ad ConfArgParse
# https://pypi.python.org/pypi/ConfArgParse

import confargparse
import sys
try:
    from lib.p_log   import p_log_init, p_log_start, p_log_this, p_log_end
    from lib.p_utils import p_file_exists
except:
    pass

args = None

def args_to_glbls (args):
    # Copy args name-space to xx_glbls.arg_ns
    for key, value in vars(args).iteritems():
        if hasattr(xx_glbls.arg_ns, key):
            setattr(xx_glbls.arg_ns, key, value)
            p_log_this(str(key) + ' = ' + str(value))
"""

CA_Parser[40] = """
def xx_parser(command = '', cfg_path_tmp=''):
    # p_log_this()
    parser = confargparse.ConfArgParser(description='Program: xx_program_name')
    # exclude positional args when exporting conf-file
    # if (command <> '--export-conf-file') and (command <> 'ignore_pos_args'):
    #     pass
"""

CA_Parser[44] = """
"""


CA_Parser[48] = """
    global args
    # export conf-file:
    if (command == '--export-conf-file'):
        mssge = '| xx_CAParser.py: generating & writing: ' + cfg_path_tmp
        print mssge ; print '-' * 20 ; p_log_this(mssge)
        # NOTE: >parser.parse_args('--export-conf-file' ...) will EXIT!<
        parser.parse_args(['--export-conf-file', cfg_path_tmp])
        # xx_CAParser has written cfg-file
        # nota: parser.parse_args(['--export-conf-file', cfg_path_tmp]) exits module!
    elif ((command == '--conf-file') and str(cfg_path_tmp != '')):
        # read conf-file:
        param_list = [command, cfg_path_tmp]
        p_log_this('Trying to read from:' + str(cfg_path_tmp))
        args = parser.parse_args(param_list)
        args_to_glbls (args)  # set values in >xx_glbls.arg_ns<
    else:
        # cmdline pos.args / opt.args
        param_list = None
        p_log_this('No parameters:')
        args = parser.parse_args(param_list)
        args_to_glbls (args)  # set values in >xx_glbls.arg_ns<
"""


CA_Parser[96] = """
"""

CA_Parser[98] = """
if __name__ == "__main__":
    # This branch should have been called by >pyprogen.py<
    from   p_log   import p_log_init, p_log_start, p_log_this, p_log_end
    print '-' * 20
    print '| xx_CAParser.py: running'
    print '|',
    p_log_init(log_dir = r'xx_dir_log', log_fn = r'xx_CAParser')
    p_log_start()
    p_log_this(' generating cfg-file')
    cfg_path_tmp = sys.argv[1]
    if not cfg_path_tmp:
        mssge =   '| xx_CAParser: No output path for cfg-file?? '
        print mssge ; p_log_this(mssge)
        cfg_path_tmp = os.path.join('.', 'main\cfg', 'conf.ini')
        mssge = '| xx_CAParser: Setting output path to: ' + str(cfg_path_tmp)
        print mssge ; p_log_this(mssge)
    else:
        mssge = '| output path for cfg-file = ' + str(cfg_path_tmp)
        print mssge ; p_log_this(mssge)
    xx_parser('--export-conf-file', cfg_path_tmp)
    # NOTE: in func >xx_parser()<
    # calling >parser.parse_args('--export-conf-file' ...)
    # will EXIT!
else:
    import lib.xx_glbls as xx_glbls
    pass
"""

