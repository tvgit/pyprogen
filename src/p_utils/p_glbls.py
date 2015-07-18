#
# Sharing program wide information via this module
#

import  p_utils

prog_name    = 'z_main'

prefix   = ''

dir_main = ''
dir_cfg  = ''
dir_lib  = ''
dir_log  = ''

cfg_fn   = ''
cfg_path = ''

CAParser_path= ''

opt_arg_vars = []
pos_arg_vars = []

patterns_fn  = ''
patterns_path= ''

def print_p_cfg_vars(print_vars=False):
    print p_utils.here('', 1)
    print ' prog_name = '     + prog_name
    print ' prefix    = '     + prefix
    print ' dir_main  = '     + dir_main
    print ' dir_cfg   = '     + dir_cfg
    print ' dir_lib   = '     + dir_lib
    print ' dir_log   = '     + dir_log
    print ' CAParser_path = ' + CAParser_path
    print ' patterns_fn  = '  + patterns_fn
    print ' patterns_path= '  + patterns_path
    if print_vars:
        for arg in opt_arg_vars:
            print '  opt. arg var: ' + arg
        for arg in pos_arg_vars:
            print '  pos.-arg var: ' + arg
