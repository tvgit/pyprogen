# -------------- y_main.py
# INFO       2015-07-18 20:36:05  p_log_start:  y_main.py Logging started (first time!)
# INFO       2015-07-18 20:36:05  p_log_end:  y_main.py Logging end


y_main = dict()
y_main[02] = """
from   lib.xx_CAParser  import  xx_parser
import lib.xx_glbls as xx_glbls
# import lib.xx_my_code as my_code

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
        print mssge_1 + '\\n' + mssge_2
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

    parse_args('no_pos_args', cfg_path='./cfg/xx_main.cfg')

    p_log_end()
    p_utils.p_exit()
"""

# -------------- y_my_code.py

y_my_code = dict()
y_my_code[02] = """
# In this module resides our code. Imported to >xx_main.py<. Is respected if changed.'
import lib.xx_glbls as xx_glbls
# import lib.xx_my_code as my_code

import lib.p_utils as p_utils
from   lib.p_log   import p_log_init, p_log_start, p_log_this, p_log_end
"""

y_my_code[04] = """
"""

y_my_code[96] = """
"""

y_my_code[98] = """
"""

# -------------- y_glbls.py

y_glbls = dict()
y_glbls[02] = """
# Sharing information via this module across >xx_main.py< and its modules
#
"""

y_glbls[04] = """
"""

y_glbls[96] = """
"""

y_glbls[98] = """
"""

# -------------- y_CAParser.py

CA_Parser_02 = """
import confargparse
import argparse
import sys
try:
    from   lib.p_log   import p_log_init, p_log_start, p_log_this, p_log_end
except:
    pass
# from   p_log   import p_log_this

def xx_parser(command = '', cfg_path=''):
    # p_log_this()
    parser = confargparse.ConfArgParser(description='Program: xx_program_name')
    # exclude positional args when exporting conf-file
    if (command <> '--export-conf-file') and (command <> 'no_pos_args'):
"""

CA_Parser_04 = """
    if (command == '--export-conf-file'):
        print '| xx_CAParser: generating: ', cfg_path
        print '| xx_CAParser: end'
        print '-' * 20
        # ConfArgParser obviously exits? Here! Why?
        parser.parse_args(['--export-conf-file', cfg_path])
        # ConfArgParser obviously exits? Here! Why?
    elif cfg_path:
        print '++++++++ read from: ', cfg_path
        args = parser.parse_args(['--conf-file', cfg_path])
    else:
        args = parser.parse_args()

    args = vars(args)
    for key, value in sorted(args.iteritems()):
        print "%s  =  %s " % (key, value)

    #print 'args: ' , args
# http://stackoverflow.com/questions/16878315/what-is-the-right-way-to-treat-python-argparse-namespace-as-a-dictionary
# https://parezcoydigo.wordpress.com/2012/08/04/from-argparse-to-dictionary-in-python-2-7/
"""

CA_Parser_96 = """
"""

CA_Parser_98 = """
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
    pass
"""

