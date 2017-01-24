# Sharing program wide information about >y_main.py<,
#  its dirs and cfg-, log-, util-files etc via this module
#
import os.path

prog_name         = 'def_y_main.py' # default name of (new) program, configure in: >new_prog.ini<
prog_dir          = None            # default path
prog_changed      = False           # y_main.py changed?
prog_name_new     = prog_name       # name of program with new config version

prefix    = None     # common prefix of y_main-specific dirs, paths, modules, functions, vars ...
arg_prefix= None     # common prefix of vars storing values of cmd-line args

main_dir  = None     # main dir: >./y_main<, where >y_main.py< lives in
cfg_dir   = None     # subdir  : >./y_main/cfg<, config files for >y_main.py<
lib_dir   = None     # subdir  : >./y_main/lib<, utilities for >y_main.py<
log_dir   = None     # subdir  : >./y_main/log<, log-files for >y_main.py<

cfg_fn       = None  # filename of cfg-file for for 'y_main.py'; usually: >y_main.py<
cfg_path     = None  # path     of cfg-file for for 'y_main.py'; usually: >./y_mainy/cfg/y_main.cfg<
cfg_changed  = False # y_main.cfg changed?

cfg_fn_new   = None  # filename of new cfg-file for for 'y_main.py'; usually: >y_main_timestamp.py<
cfg_path_new = None  # path     of new cfg-file for for 'y_main.py'; usually: >./y_mainy/cfg/y_main_timestamp.cfg<

CAParser_fn  = None  # filename of arg-parser of 'y_main.py'  (>y_ConfArgParser.py<)
CAParser_path= None  # path     of arg-parser of 'y_main.py'  (>./y_main/lib/y_ConfArgParser.py<)
CAParser_func= None  # function name  (>def y_parser(): ...<)

glbls_fn     = None  # name of globals file (OF NEW PROGRAM!); usually: >y_glbls.py<
glbls_path   = None  # path of globals file (OF NEW PROGRAM!); usually: >./y_main/lib/y_glbls.py<;

pos_arg_vars = None  # positional args
opt_arg_vars = None  # optional args

dir_DataIn  = None   # subdir  : >./y_main/DataIn<, DataIn-files for >y_main.py<
dir_DataOut = None   # subdir  : >./y_main/DataOut<, DataOut-files for >y_main.py<

date_time_str= None  # Date & Time

def print_p_cfg_and_args(print_args=True):
    print ' prog_name     =   '   + prog_name
    print ' prefix        =   '   + prefix
    print
    print ' main_dir      = ' + main_dir
    print ' lib_dir       = ' + lib_dir
    print ' log_dir       = ' + log_dir
    print ' cfg_dir       = ' + cfg_dir
    print
    len_cfg_dir = len(cfg_dir) + 1
    print ' cfg_fn        = '   + ' '*len_cfg_dir + cfg_fn
    print ' cfg_path      = '   + os.path.join(cfg_dir, cfg_fn)
    print
    print ' cfg_file_new  = '     + ' '*len_cfg_dir + os.path.basename(cfg_path_new)
    print ' cfg_path_new  = ' + cfg_path_new
    print
    len_lib_dir = len(lib_dir) + 1
    print ' CAParser_fn   = '   + ' '*len_lib_dir + CAParser_fn
    print ' CAParser_path = '     + CAParser_path
    print ' CAParser_func =   >'   + CAParser_func + '()<'
    print
    print ' glbls_fn      = '   + ' '*len_lib_dir + glbls_fn
    print ' glbls_path    = '   + os.path.join(lib_dir, glbls_fn)
    # print ' glbls_path    = '   + glbls_path
    print
    print ' dir_DataIn    = '     + dir_DataIn
    print ' dir_DataOut   = '     + dir_DataOut
    print
    print ' date_time_str = '     + date_time_str
    print

    if print_args:
        print
        for arg in sorted(opt_arg_vars):
            print '  Opt. command line variables: ' + arg
        for arg in sorted(pos_arg_vars):
            print '  Opt. positional arguments variables: ' + arg

    print
    print '-'*10 + ' ' + prog_name_new + ' ' + '-' *60 + '\n'


