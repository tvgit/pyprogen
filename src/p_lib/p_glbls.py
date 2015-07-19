# Sharing program wide information via this module
prog_name    = 'def_main.py'   # default name of new program. Configure in ???
prog_path    = None          # default path: >./z_main/z_main.py<

prefix   = None     # common prefix of z_main-specific dirs, paths, modules, functions, vars ...

dir_main = None     # main dir: >./z_main<, where >z_main.py< lives in
dir_cfg  = None     # subdir  : >./z_main/cfg<, config files for >z_main.py<
dir_lib  = None     # subdir  : >./z_main/lib<, utilities for >z_main.py<
dir_log  = None     # subdir  : >./z_main/log<, log-files for >z_main.py<

cfg_fn   = None
cfg_path = None

CAParser_fn  = None  # filename of arg-parser of 'z_main.py'  (y_ConfArgParser.py)
CAParser_path= None  # path     of arg-parser of 'z_main.py'  (>./z_main/lib/...<)
CAParser_func= None  # function name  (>def y_parser(): ...<)

pos_arg_vars = None  # positional args
opt_arg_vars = None  # optional args

patterns_fn  = None  # name of pattern file; usually: >patterns.py<
patterns_path= None  # path of pattern file; usually: >./p_cfg/pattern.py<

def print_p_cfg_vars(print_args=False):
    print ' prog_name = '     + prog_name
    print ' prefix    = '     + prefix
    print ' dir_main  = '     + dir_main
    print ' dir_cfg   = '     + dir_cfg
    print ' dir_lib   = '     + dir_lib
    print ' dir_log   = '     + dir_log
    print ' cfg_fn    = '     + cfg_fn
    print ' cfg_path  = '     + cfg_path
    print ' CAParser_fn   = ' + CAParser_fn
    print ' CAParser_path = ' + CAParser_path
    print ' CAParser_func = ' + CAParser_func
    print ' patterns_fn  = '  + patterns_fn
    print ' patterns_path= '  + patterns_path
    if print_args:
        for arg in opt_arg_vars:
            print '  opt. arg var: ' + arg
        for arg in pos_arg_vars:
            print '  pos.-arg var: ' + arg
