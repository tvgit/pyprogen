# Sharing program wide information about >y_main.py< via this module
prog_name= 'default_y_main.py' # default name of new program. Configure in ???
prog_path= None                # default path: >./y_main/y_main.py<

prefix   = None     # common prefix of y_main-specific dirs, paths, modules, functions, vars ...

dir_main = None     # main dir: >./y_main<, where >y_main.py< lives in
dir_cfg  = None     # subdir  : >./y_main/cfg<, config files for >y_main.py<
dir_lib  = None     # subdir  : >./y_main/lib<, utilities for >y_main.py<
dir_log  = None     # subdir  : >./y_main/log<, log-files for >y_main.py<

cfg_fn   = None
cfg_path = None

CAParser_fn  = None  # filename of arg-parser of 'y_main.py'  (y_ConfArgParser.py)
CAParser_path= None  # path     of arg-parser of 'y_main.py'  (>./y_main/lib/...<)
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

