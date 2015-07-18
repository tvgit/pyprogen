# -------------- y_main.py
# INFO       2015-07-18 20:36:05  p_log_start:  y_main.py Logging started (first time!)
# INFO       2015-07-18 20:36:05  p_log_end:  y_main.py Logging end

y_main_02 = """
import lib.xx_CAParser    # substituted by your CAParser
import lib.p_utils as p_utils
from   lib.p_log   import p_log_init, p_log_start, p_log_this, p_log_end

import sys

def m_parser(command = '', cfg_path=''):
    parser = confargparse.ConfArgParser(description='Program: replace_w_program_name')
    # exclude positional args when exporting conf-file
    if (command <> '--export-conf-file'):
        pass


if __name__ == "__main__":
    p_log_init(log_dir = 'log', log_fn = 'xx_main.log')
    p_log_start()

    prog_info = p_utils.scriptinfo()
    prog_name = prog_info['name']
    print '\\n' + '__main__ : ' + prog_name + '\\n'

    p_log_end()
    p_utils.p_exit()
"""

y_main_04 = """
"""

y_main_96 = """
"""

y_main_98 = """
if __name__ == "__main__":
    print '-' * 20
    print '| xx_main: running'
    print '| xx_CAParser: end'
    print '-' * 20
else:
    pass
"""



# -------------- y_CAParser.py

CA_Parser_02 = """
import confargparse
import argparse
import sys

def m_parser(command = '', cfg_path=''):
    parser = confargparse.ConfArgParser(description='Program: replace_w_program_name')
    # exclude positional args when exporting conf-file
    if (command <> '--export-conf-file'):
"""

CA_Parser_04 = """
    if (command == '--export-conf-file'):
        parser.parse_args(['--export-conf-file', cfg_path])
        # ConfArgParser obviously exits? Why?
# http://stackoverflow.com/questions/16878315/what-is-the-right-way-to-treat-python-argparse-namespace-as-a-dictionary
# https://parezcoydigo.wordpress.com/2012/08/04/from-argparse-to-dictionary-in-python-2-7/
"""

CA_Parser_96 = """
"""

CA_Parser_98 = """
if __name__ == "__main__":
    print '-' * 20
    print '| xx_CAParser: running'
    cfg_path = sys.argv[1]
    if not cfg_path:
        print '| xx_CAParser: No config path?? '
        cfg_path = os.path.join('.', 'main\cfg', 'conf.ini')
        print ('| xx_CAParser: Setting config path to: ' + cfg_path)
    else:
        print '| conf_path= ', cfg_path
    m_parser('--export-conf-file', cfg_path)
    print '| xx_CAParser: end'
    print '-' * 20
else:
    pass
"""

