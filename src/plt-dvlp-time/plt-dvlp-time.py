4# 2015_08_04-00_46_11 generated by: >pyprogen.py<
# >181cf5ae8600e622f5003fada8e67081< 

# YOUR code resides in THIS module.
# It is respected if changed (modification results from different
# hash code '>xxx...xxx<' in second line of source code of this module).

"""
Evaluate log file pyprogen.log (from pyprogen.py) to plot time of start of pyprogen.py.
Use the gnuplot script from below to draw a plot.
"""

'''
# -------------- gnuplot script -----------------
#
# load it into the gnuplot console by: 'load 'gplt.txt'
#
# gnuplot can not handle different time scales on x and y axis, for example: day vs time of day (i.e. date vs hours:minutes)
# So time has to be treated as numerical data, for example minutes since midnight.
# If so, the tics on the y-Axis have to be modified, to be understandable as hours (an not minutes)
#
# http://psy.swansea.ac.uk/staff/carter/gnuplot/gnuplot_time.htm
#
set terminal windows
set title "development time >pyprogen.py<"
set xlabel "date"
set ylabel "hour: 00:00 to 02:00"
set autoscale
set grid
set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"    # format of data in data file!
set datafile separator ";"
set format x "%Y-%m-%d"            # format of x-axis tics in graphics!
# reformat y tics; see gnuplot manual "xtics" > set xtics { ... ({"<label>"} <pos> {<level>} {,{"<label>"}...) } ...
set ytics ("0" 0, "2" 120, "4" 240, "6" 360, "8" 480, "10" 600, "12" 720, "14" 840, "16" 960, "18" 1080, "20" 1200, "22" 1320, "24" 1440, "26" 1560, "24" 1440, "2" 1560)
# set border lw 3
# colum 1 == 2015-08-03 00:00:00
# colum 4 == Integer range (1 , 24*60 + 2*60) == 24 hours + 2 hours in minutes
plot 'pyprogen.dat' using 1:4
'''

import argparse
import lib.p_utils    as p_utils
from   lib.p_log      import p_log_init, p_log_start, p_log_this, p_log_end
import re
import datetime
import os

args = None   # global fuer module argparse

def arg_parser(command ='', cfg_path_tmp=''):
    # https://martin-thoma.com/how-to-parse-command-line-arguments-in-python/
    print "arg_parser"
    parser = argparse.ArgumentParser(description='Program: plt-dvlp-time.py')
    # 'dest='  == variable that gets the value

    # default_log = "D:\Data_Work\Develop\_Python\_rh\utils\pyprogen\src\plt-dvlp-time\log\d_main.log"
    # parser.add_argument('-i', '--in_file', dest='in_file',
    #                     default = default_log, help = 'name of in_file')
    # parser.add_argument('-o', '--out_file',  dest='out_file',
    #                     default='..\ppg_log\timedata.dat', help = 'name of out_file')

    parser.add_argument('-i', '--in_file', dest='in_file',
                        default='..\ppg_log\pyprogen.log', help='name of in_file')
    parser.add_argument('-o', '--out_file',  dest='out_file',
                        default='..\ppg_log\pyprogen.dat', help = 'name of out_file')

    global args
    args = parser.parse_args()
    print args.in_file
    print args.out_file
    for key, value in vars(args).iteritems():
        print "arg_parser:", key, "=", value


# show command line usage
def usage(exit_status=0):
    msg = '-----------' * 5
    msg += '\n'
    msg += 'Usage: plt-dvlp-time.py [OPTIONS] \n'
    msg += 'Ziel: mit gnuplot eine Graphik erstellen, die Entwicklungszeitpunkte von \n'
    msg += '>pyprogen.py< (Tag/Uhrzeit) anzeigt. Die Daten stammen aus der log-Datei von  \n'
    msg += '>pyprogen.py<. Diese log-Datei  wird mit Hilfe von >plt-dvlp-time.py< aufbereitet: \n'
    msg += 'es werden die Zeitpunkte extrahiert, an denen pyprogen gestartet wurde. \n'
    msg += 'Das Ergebnis wird in die Datei: >pyprogen.out< geschrieben.  \n'
    msg += 'gnuplot kann mit dem oben angegebenen Script aus diesen Daten dann (hoffentlich) den \n'
    msg += 'Plot erstellen. \n'
    msg += ' \n'
    msg += 'Options:\n'
    msg += '  -i input File.   default= >..\p_log\pyprogen.log< \n'
    msg += '  -o output File.  default= >..\p_log\pyprogen.dat< \n'
    msg += '\n'
    msg += '-----------' * 5
    msg += '\n'
    print msg


def eval_arg(arg):
    print 'do something with: ' + str(arg)
    return arg

def rgx_date_time():
    re1='((?:(?:[1]{1}\\d{1}\\d{1}\\d{1})|(?:[2]{1}\\d{3}))[-:\\/.](?:[0]?[1-9]|[1][012])[-:\\/.](?:(?:[0-2]?\\d{1})|(?:[3][01]{1})))(?![\\d])'	# YYYYMMDD 1
    re2='(\\s+)'	# White Space 1
    re3='((?:(?:[0-1][0-9])|(?:[2][0-3])|(?:[0-9])):(?:[0-5][0-9])(?::[0-5][0-9])?(?:\\s?(?:am|AM|pm|PM))?)'	# HourMinuteSec 1

    rgx = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
    return rgx

def get_key(item):
    print type(item)
    print item
    return item.keys()[0]

def make_time_stamp_list(in_file):
    time_stamp_list = []
    old_time_stamp = ''
    cnt = 0
    rgx = rgx_date_time()
    for line in in_file.xreadlines():
        if not 'p_log_start' in line:
            continue
        match = rgx.search(line)
        if match:
            yyyymmdd = match.group(1)
            ws = match.group(2)
            time = match.group(3)
            time_stamp = yyyymmdd + ws + time
            if (time_stamp <> old_time_stamp):
                old_time_stamp = time_stamp
                time_stamp_list.append(time_stamp)
                cnt += 1
    return time_stamp_list, cnt


def make_day_ts_list(time_stamp_list):
    days_cnt = 0
    times_cnt = 0
    day_str = ''
    day_ts_list  = []    # list of day
    day   = dict() # day == dict{day:[time_1, time_2, time_3 ...]}
    times = []     # Zeitpunkte am gleichen Tag
    for time_stamp in sorted(time_stamp_list):
        new_day_str  = time_stamp[:10]
        time_str     = time_stamp[11:]
        if new_day_str <> day_str:
            # print new_day_str, time_str, time_str
            if day_str:
                day[day_str] = times    # Zeitpunkte an dict {altes Datum : [Zeitpunkte]} anfuegen
                day_ts_list.append(day) # Alten Tag an Liste der Tage
            #
            days_cnt  += 1
            # print ; print days_cnt, new_day_str , ; print time_str ,
            day = dict()            # Neuer Tag
            day_str = new_day_str
            times = []              # Liste der Zeitpunkte leeren
            times.append(time_str)  # ersten Zeitpunkt an Liste ZEitpunkte
            times_cnt += 1
        else:
            # print time_str ,
            times.append(time_str)
            times_cnt += 1

    day[day_str] = times    # Zeitpunkte an dict {altes Datum : [Zeitpunkte]} anfuegen
    day_ts_list.append(day) # Letzten Tag an Liste der Tage
    return day_ts_list, days_cnt, times_cnt


def print_day_ts_list(day_ts_list):
    days_cnt = 0
    # for day in sorted (day_ts_list, key = get_key):
    for day in day_ts_list:
        for dy, tms in day.iteritems():
            days_cnt  += 1
            print days_cnt, '#', dy,
            for t in tms:
                print t ,
            print


def make_data_str(day_ts, mins):
    data_str = (day_ts [:10] + ' 00:00:00 ; ' + day_ts )
    data_str = data_str + ' ; ' + day_ts [-8:-6] + day_ts [-5:-3]
    data_str = data_str + ' ; ' + str(mins) + '\n'
    return data_str

def evaluate_opt_args():
    p_log_this()
    fn_in_file  = args.in_file
    fn_out_file = args.out_file

    if p_utils.p_file_exists (fn_in_file, print_message = False):
        f_in_file = p_utils.p_file_open(fn_in_file, mode = 'r')
        time_stamp_list, runs_cnt = make_time_stamp_list(f_in_file)
        # print 'runs = ', runs_cnt; # print time_stamp_list
        day_ts_list, days_cnt, times_cnt = make_day_ts_list(time_stamp_list)
        print '\nday_ts_list = ', days_cnt, 'times = ', times_cnt
        f_out_file = p_utils.p_file_open(fn_out_file, mode = 'w')

        day_act        = None
        day_before     = None
        day_act_str    = ''
        day_before_str = ''
        one_day = datetime.timedelta(days=1)
        for day_ts in sorted(time_stamp_list):
            Y_a = int(day_ts [:4])
            M_a = int(day_ts [5:7])
            D_a = int(day_ts [8:10])
            day_act = datetime.date(Y_a, M_a, D_a)
            day_act_str = day_ts [:10]
            # print Y_a, M_a, D_a,
            if not day_before:
                day_before     = day_act
                day_before_str = day_act_str

            mins = int(day_ts [-8:-6])*60 + int(day_ts [-5:-3])
            if (day_act == day_before):
                # data_str = (day_ts [:10] + ' 00:00:00 ; ' + day_ts )
                # data_str = data_str + ' ; ' + day_ts [-8:-6] + day_ts [-5:-3]
                # data_str = data_str + ' ; ' + str(mins) + '\n'
                data_str = make_data_str(day_ts, mins)
            else:
                if (((day_act - day_before) == one_day) and (mins < 600)):
                    # Tage an denen ich nach Mitternacht noch programmiert habe
                    data_str = (day_before_str [:10] + ' 00:00:00 ; ' + day_ts )
                    data_str = data_str + ' ; ' + day_ts [-8:-6] + day_ts [-5:-3]
                    data_str = data_str + ' ; ' + str(mins + (24 * 60)) + ' ; +\n'
                else:
                    day_before     = day_act
                    day_before_str = day_act_str
                    print
                    data_str = make_data_str(day_ts, mins)
            f_out_file.write(data_str) # python will convert \n to os.linesep
            print data_str,
        f_out_file.close()
    else:
        print fn_in_file + ' does not exist'

def main():
    p_log_this()
    arg_parser()
    evaluate_opt_args()

def prog_name():
    prog_info = p_utils.scriptinfo()
    prog_name = prog_info['name']
    print '--------\n' + prog_name + '\n--------'
    return prog_name

if __name__ == "__main__":
    # print_prog_name()
    usage()
    log_fn = prog_name()[:-2]  + 'log'
    p_log_init(log_dir = 'log', log_fn = log_fn)
    p_log_start()

    # Here YOUR code is called.
    main()

    p_log_end()
    p_utils.p_exit()
# 2015_08_04-00_46_11
