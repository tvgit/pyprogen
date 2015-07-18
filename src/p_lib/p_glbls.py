# Sharing program wide information via this module
prog_name    = 'z_main.py'
prog_path    = None

prefix   = None

dir_main = None
dir_cfg  = None
dir_lib  = None
dir_log  = None

cfg_fn   = None
cfg_path = None

CAParser_fn  = None
CAParser_path= None

opt_arg_vars = None
pos_arg_vars = None

patterns_fn  = None
patterns_path= None

def print_p_cfg_vars(print_vars=False):
    print ' prog_name = '     + prog_name
    print ' prefix    = '     + prefix
    print ' dir_main  = '     + dir_main
    print ' dir_cfg   = '     + dir_cfg
    print ' dir_lib   = '     + dir_lib
    print ' dir_log   = '     + dir_log
    print ' CAParser_fn   = ' + CAParser_fn
    print ' CAParser_path = ' + CAParser_path
    print ' patterns_fn  = '  + patterns_fn
    print ' patterns_path= '  + patterns_path
    if print_vars:
        for arg in opt_arg_vars:
            print '  opt. arg var: ' + arg
        for arg in pos_arg_vars:
            print '  pos.-arg var: ' + arg
