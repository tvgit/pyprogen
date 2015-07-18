# -------------- y_main.py

y_main_02 = """
import xx_CAParser    # substituted by your CAParser
import sys

def m_parser(command = '', cfg_path=''):
    parser = confargparse.ConfArgParser(description='Program: replace_w_program_name')
    # exclude positional args when exporting conf-file
    if (command <> '--export-conf-file'):


if __name__ == "__main__":
    p_log_init(log_dir = 'p_log', log_fn = 'pyprogen')
    p_log_start()
    pyprogen()
    #prog_name = p_glbls.prog_name
    create_main()
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

