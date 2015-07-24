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
    xx_glbls.print_cfg_args(xx_glbls.args)

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

y_my_code[04] = ("""
def evaluate_args():
    # http://stackoverflow.com/questions/295058/convert-a-string-to-preexisting-variable-names
    # http://stackoverflow.com/questions/16878315/what-is-the-right-way-to-treat-python-argparse-namespace-as-a-dictionary
    # http://stackoverflow.com/questions/1602934/check-if-a-given-key-already-exists-in-a-dictionary?rq=1
    p_log_this()
    print '*' * 30
    print '- y_my_code > evaluate_args(): '
    xx_glbls.print_cfg_args((xx_glbls.args))
    print '*' * 30
""")

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
"""

y_glbls[04] = """
"""

y_glbls[96] = """
"""

y_glbls[98] = """

global args

def make_args(origin = 'xx_glbls.py'):
    args = Args('xx_glbls.py')
    return args

def get_args(origin):
    if args:
        return args
    else:
        args = make_args(origin = 'unknown !?')
        return args

if __name__ == "__main__":
    args = Args('xx_glbls.py')
else:
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

def get_args():
    global args
    return args

def print_args():
    global args
    print '*' * 30
    print 'This is: >xx_CAParser<'
    print 'args are: '
    args = vars(args)
    for key, value in sorted(args.iteritems()):
        print "  %s  =  %s " % (key, value)
    print '*' * 30

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
    if (command == '--export-conf-file'):
        print '| xx_CAParser.py: generating: ', cfg_path
        print '| xx_CAParser.py: end'
        print '-' * 20
        parser.parse_args(['--export-conf-file', cfg_path])
        # ConfArgParser obviously exits? Here! Why? ? ? ?
    elif cfg_path:
        print 'xx_CAParser.py > xx_parser.py: reading config from: >', cfg_path, '<'
        # args = parser.parse_args(['--conf-file', cfg_path], namespace = y_glbls.arg)
        args = parser.parse_args(['--conf-file', cfg_path])
        g_args = y_glbls.make_args()
        y_glbls.args = args
        # print_args(False)
    else:
        # args = parser.parse_args(namespace = y_glbls.arg)
        args = parser.parse_args()

    # print_args()
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

