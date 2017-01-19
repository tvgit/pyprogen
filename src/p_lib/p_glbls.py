# Sharing program wide information about >y_main.py<,
#  its dirs and cfg-, log-, util-files etc via this module
#
import os.path

prog_name         = 'def_y_main.py' # default name of (new) program, configure in: >new_prog.ini<
prog_path         = None            # default path: >./y_main/y_main.py<
prog_changed      = False # x_main.py changed?
prog_name_new_cfg = prog_name       # name of program with new config version

prefix    = None     # common prefix of y_main-specific dirs, paths, modules, functions, vars ...
arg_prefix= None     # common prefix of vars storing values of cmd-line args

dir_main  = None     # main dir: >./y_main<, where >y_main.py< lives in
dir_cfg   = None     # subdir  : >./y_main/cfg<, config files for >y_main.py<
dir_lib   = None     # subdir  : >./y_main/lib<, utilities for >y_main.py<
dir_log   = None     # subdir  : >./y_main/log<, log-files for >y_main.py<

dir_DataIn  = None   # subdir  : >./y_main/DataIn<, DataIn-files for >y_main.py<
dir_DataOut = None   # subdir  : >./y_main/DataOut<, DataOut-files for >y_main.py<

cfg_fn    = None     # filename of cfg-file for for 'y_main.py'; usually: >y_main.py<
cfg_path  = None     # path     of cfg-file for for 'y_main.py'; usually: >y_mainy/cfg/y_main.cfg<

cfg_fn_tmp   = None  # filename of temporary cfg-file for for 'y_main.py'; usually: >y_main_timestamp.py<
cfg_path_tmp = None  # path     of temporary cfg-file for for 'y_main.py'; usually: >y_mainy/cfg/y_main_timestamp.cfg<

CAParser_fn  = None  # filename of arg-parser of 'y_main.py'  (>.y_ConfArgParser.py<)
CAParser_path= None  # path     of arg-parser of 'y_main.py'  (>./y_main/lib/...<)
CAParser_func= None  # function name  (>def y_parser(): ...<)

glbls_fn     = None  # name of globals file (OF NEW PROGRAM!); usually: >y_glbls.py<

my_code_fn   = None  # name of your code; usually: >y_my_code.py<

pos_arg_vars = None  # positional args
opt_arg_vars = None  # optional args

date_time_str= None  # Date & Time

def print_p_cfg_and_args(print_args=False):
    print ' prog_name     =   '   + prog_name
    print ' prefix        =   '   + prefix
    print
    print ' dir_main      = '     + dir_main
    print ' dir_lib       = '     + dir_lib
    print ' dir_log       = '     + dir_log
    print
    print ' dir_cfg       = '     + dir_cfg
    len_cfg_dir_cfg = len(dir_cfg) + 1
    print ' cfg_path      = '   + os.path.join(dir_cfg,cfg_fn)
    print ' cfg_file      = '   + ' '*len_cfg_dir_cfg + cfg_fn
    print ' cfg_path_tmp  = '     + cfg_path_tmp
    print ' cfg_file_tmp  = '     + ' '*len_cfg_dir_cfg + os.path.basename(cfg_path_tmp)
    print
    print ' dir_DataIn    = '     + dir_DataIn
    print ' dir_DataOut   = '     + dir_DataOut
    print
    print ' CAParser_path = '     + CAParser_path
    len_CAParser_dir = len(os.path.basename(CAParser_path))
    print ' CAParser_fn   = '   + ' '*len_CAParser_dir + CAParser_fn
    print ' CAParser_func =   '   + CAParser_func
    print
    print ' glbls_fn      =   '   + glbls_fn
    print ' date_time_str = '     + date_time_str
    print

    if print_args:
        for arg in opt_arg_vars:
            print '  opt. arg var: ' + arg
        for arg in pos_arg_vars:
            print '  pos.-arg var: ' + arg

    print '-'*10 + ' ' + prog_name + ' ' + '-' *60 + '\n'


