# -------------- y_main.py
# INFO       2015-07-18 20:36:05  p_log_start:  y_main.py Logging started (first time!)
# INFO       2015-07-18 20:36:05  p_log_end:  y_main.py Logging end

y_main = dict()
y_main[02] = """
from   lib.xx_CAParser  import  xx_parser
import lib.xx_glbls as xx_glbls
import lib.xx_my_code as xx_my_code

import lib.p_utils as p_utils
from   lib.p_log   import p_log_init, p_log_start, p_log_this, p_log_end

import sys
"""

y_main[04] = """
def use_args():
    pass
"""

y_main[10] = """
def parse_args(command, cfg_path):
    if command:
        mssge_1 = 'xx_main > parse_args: command  = ' + command
        mssge_2 = 'xx_main > parse_args: cfg_path = ' + cfg_path
        p_log_this(mssge_1)
        p_log_this(mssge_2)
    xx_parser(command, cfg_path)
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

    parse_args('ignore_pos_args', cfg_path='./cfg/xx_main.cfg')

    # Here YOUR code is called.
    xx_my_code.main()

    p_log_end()
    p_utils.p_exit()
"""

# -------------- y_my_code.py

y_my_code = dict()
y_my_code[02] = """
# Hash = xx_hash
# Your code resides in this module. Imported to >xx_main.py<. Is respected if changed.'
#
import lib.xx_glbls as xx_glbls
import lib.xx_CAParser as xx_CAParser

import lib.p_utils as p_utils
from   lib.p_log   import p_log_init, p_log_start, p_log_this, p_log_end
"""

y_my_code[04] = """
def evaluate_args():
    # print '- y_my_code > evaluate_args(): '
    p_log_this()
    xx_glbls.print_arg_ns()
"""

y_my_code[10] = """
def main():
    p_log_this()
    evaluate_args()
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
    # ab hier: p_code ...

"""

y_glbls[04] = """
"""

y_glbls[10] = """
    return arg_ns

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
        print '| y_CAParser.py: generating: ', cfg_path
        print '| y_CAParser.py: generating & writing: ', cfg_path
        print '-' * 20
        parser.parse_args(['--export-conf-file', cfg_path])
        print '| y_CAParser.py: end'
        # ConfArgParser obviously exits? Here! Why? ? ? ?
    # when reading conf-file:
    elif cfg_path:
        print 'xx_CAParser.py > xx_parser.py: reading config from: >', cfg_path, '<'
        args = parser.parse_args(['--conf-file', cfg_path])
        for key, value in vars(args).iteritems():
            if hasattr(y_glbls.arg_ns, key):
                setattr(y_glbls.arg_ns, key, value)
    else:
        args = parser.parse_args()
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
    import lib.y_glbls as y_glbls
    pass
"""

