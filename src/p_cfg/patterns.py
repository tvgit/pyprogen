# -------------- y_main.py
# INFO       2015-07-18 20:36:05  p_log_start:  y_main.py Logging started (first time!)
# INFO       2015-07-18 20:36:05  p_log_end:  y_main.py Logging end

y_main = dict()
y_main[02] = """
import lib.xx_CAParser as xx_CAParser
import lib.xx_glbls    as xx_glbls
import lib.xx_my_code  as xx_my_code

import lib.p_utils as p_utils
from   lib.p_log   import p_log_init, p_log_start, p_log_this, p_log_end

import sys
"""

y_main[04] = """
def use_args():
    pass
"""

y_main[10] = """
"""

y_main[96] = """
"""

y_main[98] = """
if __name__ == "__main__":
    prog_info = p_utils.scriptinfo()
    prog_name = prog_info['name']
    print '--------\\n' + prog_name + '\\n--------'

    p_log_init(log_dir = 'log', log_fn = 'xx_main.log')
    p_log_start()

    # xx_CAParser.xx_parser('ignore_pos_args', '')
    xx_CAParser.xx_parser()

    # Here YOUR code is called.
    xx_my_code.main()

    p_log_end()
    p_utils.p_exit()
"""

# -------------- y_my_code.py

y_my_code = dict()

y_my_code[02] = """# -

# YOUR code resides in THIS module. Imported to >xx_main.py<.
# Is respected if changed (modification results from differnet hash code >nnn< above).

import lib.xx_glbls as xx_glbls
import lib.p_utils as p_utils
from   lib.p_log   import p_log_init, p_log_start, p_log_this, p_log_end
"""

y_my_code[04] = """
def eval_arg(arg):
    print 'do something with: ' + str(arg)
    return arg

def evaluate_opt_args():
    p_log_this()
    print '- xx_my_code > evaluate_args(): '
    xx_glbls.print_arg_ns()
"""

y_my_code[10] = """
"""

y_my_code[96] = """
def main():
    p_log_this()
    evaluate_opt_args()

"""

y_my_code[98] = """
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
    args = Args('xx_glbls.py')
    arg_ns = make_arg_ns('xx_glbls.py')
    print_arg_ns()
else:
    arg_ns = make_arg_ns('xx_glbls.py')
    pass
"""

# -------------- y_CAParser.py

CA_Parser = dict()

CA_Parser[02] = """
import confargparse
import argparse
import sys
try:
    from   lib.p_log   import p_log_init, p_log_start, p_log_this, p_log_end
except:
    pass

args = None

def xx_parser(command = '', cfg_path=''):
    # p_log_this()
    parser = confargparse.ConfArgParser(description='Program: xx_program_name')
    # exclude positional args when exporting conf-file
    if (command <> '--export-conf-file') and (command <> 'ignore_pos_args'):
"""

CA_Parser[04] = """
"""


CA_Parser[10] = """
    global args
    # export conf-file:
    if (command == '--export-conf-file'):
        print '| xx_CAParser.py: generating: ', cfg_path
        print '| xx_CAParser.py: generating & writing: ', cfg_path
        print '-' * 20
        parser.parse_args(['--export-conf-file', cfg_path])
        print '| xx_CAParser.py: end'
        # ConfArgParser obviously exits? Here! Why? ? ? ?
    else:
        # read +/- conf-file +- pos.args +/- opt.args
        args = parser.parse_args()
        # set values in >xx_glbls.arg_ns<
        for key, value in vars(args).iteritems():
            if hasattr(xx_glbls.arg_ns, key):
                setattr(xx_glbls.arg_ns, key, value)
"""


CA_Parser[96] = """
"""

CA_Parser[98] = """
if __name__ == "__main__":
    from   p_log   import p_log_init, p_log_start, p_log_this, p_log_end
    print '-' * 20
    print '| xx_CAParser: running'
    print '|',
    p_log_init(log_dir = 'xx_dir_log', log_fn = 'xx_CAParser')
    p_log_start()
    p_log_this('| generating cfg-file')
    cfg_path = sys.argv[1]
    if not cfg_path:
        print '| xx_CAParser: No output path for cfg-file?? '
        cfg_path = os.path.join('.', 'main\cfg', 'conf.ini')
        print ('| xx_CAParser: Setting output path to: ' + cfg_path)
    else:
        print '| output path for cfg-file = ', cfg_path
    xx_parser('--export-conf-file', cfg_path)
    print '| xx_CAParser: end'
    print '-' * 20
    p_log_end()
else:
    import lib.xx_glbls as xx_glbls
    pass
"""

