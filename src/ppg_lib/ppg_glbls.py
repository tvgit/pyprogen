# Sharing program wide information about >y_main.py<,
#  its dirs and cfg-, log-, util-files etc via this module
#
import os.path
import string

main_name         = 'def_y_main.py' # default name of (new) main program, configure in: >new_prog.ini<
main_dir          = ''              # default dir
main_path         = ''              # default path
main_changed      = False           # y_main.py changed?
main_new_name     = ''              # name of new version: >y_main.py< or >y_main_TIMESTAMP.py<
main_new_path     = ''              # corresponding path

# function in >y_main.py< which evals cmd-line args and/or conf-file args (always read by ConfArgParser)
confarg_name      = 'eval_confargs.py' # function >eval_confargs() in separate file: >eval_confargs.py<
confarg_dir       = main_dir        # default dir
confarg_path      = ''              # default path
confarg_changed   = False           # file: >eval_confargs.py< changed?
confarg_new_name  = ''              # name of new version: >eval_confargs_TIMESTAMP<
confarg_new_path  = ''              # corresponding path

# name of file with new code: >y_main.py< or >eval_confargs.py< or >eval_confargs_TIMESTAMP.py<
code_new_name     = ''              #
code_new_path     = ''              #

prefix    = None     # common prefix of y_main-specific dirs, paths, modules, functions, vars ...
arg_prefix= None     # common prefix of vars storing values of cmd-line args

main_dir  = None     # main dir: >./y_main<, where >y_main.py< and >eval_confargs.py< are living
cfg_dir   = None     # subdir  : >./y_main/cfg<, config files for >y_main.py<
lib_dir   = None     # subdir  : >./y_main/lib<, utilities for >y_main.py<
log_dir   = None     # subdir  : >./y_main/log<, log-files for >y_main.py<

cfg_fn       = None  # filename of cfg-file for 'y_main.py'; usually: >y_main.py<
cfg_path     = None  # path     of cfg-file for 'y_main.py'; usually: >./y_mainy/cfg/y_main.cfg<
cfg_exists   = False # y_main.cfg exists?
cfg_changed  = False # y_main.cfg changed?

cfg_fn_new   = None  # filename of new cfg-file for for 'y_main.py'; usually: >y_main_timestamp.py<
cfg_path_new = None  # path     of new cfg-file for for 'y_main.py'; usually: >./y_mainy/cfg/y_main_timestamp.cfg<

cfg_fn_tmp   = None  # filename of tmp cfg-file for for 'y_main.py': >y_main_tmp.cfg<
cfg_path_tmp = None  # path     of mpw cfg-file for for 'y_main.py': >./y_mainy/cfg/y_main_tmp.cfg<

CAParser_fn  = None  # filename of arg-parser of 'y_main.py'  (>y_ConfArgParser.py<)
CAParser_path= None  # path     of arg-parser of 'y_main.py'  (>./y_main/lib/y_ConfArgParser.py<)
CAParser_func= None  # function name  (>def y_parser(): ...<)

pos_arg_vars = None  # positional args
opt_arg_vars = None  # optional args

dir_DataIn   = None   # subdir  : >./y_main/DataIn<, DataIn-files for >y_main.py<
dir_DataOut  = None   # subdir  : >./y_main/DataOut<, DataOut-files for >y_main.py<

date_time_str= None  # Date & Time

# headline     = ('-' * 10 + ' ' + main_new_name + ' ' + '-' * 10 + '\n')

def print_headline():
    print ('-' * 10 + ' ' + code_new_name + ' ' + '-' * 10 + '\n')

def print_p_cfg_and_args(print_args=True):
    print ' main_name     =   ' + main_name
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
    # print
    # print ' cfg_file_new  = '     + ' '*len_cfg_dir + os.path.basename(cfg_path_tmp)
    # print ' cfg_path_tmp  = ' + cfg_path_tmp
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
    # print

    if print_args:
        print
        cnt = 0
        for arg in sorted(opt_arg_vars):
            cnt += 1
            print string.rjust(str(cnt), 2, ' ') + '  Opt. command line variable: ' + arg
        cnt = 0
        for arg in sorted(pos_arg_vars):
            cnt += 1
            print string.rjust(str(cnt), 2, ' ') + '  Opt. positional arguments variable: ' + arg

    print
    print_headline()


