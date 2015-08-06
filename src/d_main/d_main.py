# 2015_08_04-00_46_11 generated by: >pyprogen.py<
# >181cf5ae8600e622f5003fada8e67081< 

# YOUR code resides in THIS module.
# It is respected if changed (modification results from different
# hash code '>xxx...xxx<' in second line of source code of this module).

import lib.d_glbls    as d_glbls
import lib.d_CAParser as d_CAParser
import lib.p_utils    as p_utils
from   lib.p_log      import p_log_init, p_log_start, p_log_this, p_log_end
import re
import datetime
import os

# http://psy.swansea.ac.uk/staff/carter/gnuplot/gnuplot_time.htm

def eval_arg(arg):
    print 'do something with: ' + str(arg)

    return arg

def rgx_date_time():
    re1='((?:(?:[1]{1}\\d{1}\\d{1}\\d{1})|(?:[2]{1}\\d{3}))[-:\\/.](?:[0]?[1-9]|[1][012])[-:\\/.](?:(?:[0-2]?\\d{1})|(?:[3][01]{1})))(?![\\d])'	# YYYYMMDD 1
    re2='(\\s+)'	# White Space 1
    re3='((?:(?:[0-1][0-9])|(?:[2][0-3])|(?:[0-9])):(?:[0-5][0-9])(?::[0-5][0-9])?(?:\\s?(?:am|AM|pm|PM))?)'	# HourMinuteSec 1

    rgx = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
    # txt = ''
    # m = rgx.search(txt)
    # if m:
    #     yyyymmdd1=m.group(1)
    #     ws1=m.group(2)
    #     time1=m.group(3)
    #     print "("+yyyymmdd1+")"+"("+ws1+")"+"("+time1+")"+"\n"
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
            print days_cnt, '#',
            print dy,
            for t in tms:
                print t ,
            print


def evaluate_opt_args():
    p_log_this()
    # d_glbls.print_arg_ns()
    # optional args(ConfArgParser):
    if d_glbls.arg_ns.in_file == d_glbls.arg_ns.in_file:
        fn_in_file = d_glbls.arg_ns.in_file

        if p_utils.p_file_exists (fn_in_file, print_message = False):
            f_in_file = p_utils.p_file_open(fn_in_file, mode = 'r')
            time_stamp_list, runs_cnt = make_time_stamp_list(f_in_file)
            # print 'runs = ', runs_cnt; # print time_stamp_list
            day_ts_list, days_cnt, times_cnt = make_day_ts_list(time_stamp_list)
            print '\nday_ts_list = ', days_cnt, 'times = ', times_cnt
            fn_out_file = d_glbls.arg_ns.out_file
            f_out_file = p_utils.p_file_open(fn_out_file, mode = 'w')
            # for day_ts in sorted(time_stamp_list):
            #     data_str = (day_ts [:10] + ' 00:00:00 ; ' + day_ts )
            #     data_str = data_str + ' ; ' + day_ts [-8:-6] + day_ts [-5:-3]
            #     data_str = data_str + ' ; ' + str(int(day_ts [-8:-6])*60 + int(day_ts [-5:-3])) + '\n'
            #     f_out_file.write(data_str) # python will convert \n to os.linesep
            #     print data_str,
            # f_out_file.close()


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
                if (day_act != day_before):
                    if ((day_act - day_before) == one_day):
                        if (mins < 600):
                            #print ; print '!! ', day_act, day_before, mins
                        # else:
                        #     day_before     = day_act
                        #     day_before_str = day_act_str
                            data_str = (day_before_str [:10] + ' 00:00:00 ; ' + day_ts )
                            data_str = data_str + ' ; ' + day_ts [-8:-6] + day_ts [-5:-3]
                            data_str = data_str + ' ; ' + str(mins + 24 * 60) + ' +\n'
                    else:
                        day_before     = day_act
                        day_before_str = day_act_str
                        print
                        data_str = (day_ts [:10] + ' 00:00:00 ; ' + day_ts )
                        data_str = data_str + ' ; ' + day_ts [-8:-6] + day_ts [-5:-3]
                        data_str = data_str + ' ; ' + str(mins) + '\n'

                else:
                    data_str = (day_ts [:10] + ' 00:00:00 ; ' + day_ts )
                    data_str = data_str + ' ; ' + day_ts [-8:-6] + day_ts [-5:-3]
                    data_str = data_str + ' ; ' + str(mins) + '\n'
                f_out_file.write(data_str) # python will convert \n to os.linesep
                print data_str,
            f_out_file.close()
        else:
            print fn_in_file + ' does not exist'


def main():
    p_log_this()
    evaluate_opt_args()


def print_prog_name():
    prog_info = p_utils.scriptinfo()
    prog_name = prog_info['name']
    print '--------\n' + prog_name + '\n--------'

if __name__ == "__main__":
    print_prog_name()
    p_log_init(log_dir = 'log', log_fn = 'd_main.log')
    p_log_start()

    # d_CAParser.d_parser('ignore_pos_args', '')
    d_CAParser.d_parser()

    # Here YOUR code is called.
    main()

    p_log_end()
    p_utils.p_exit()
# 2015_08_04-00_46_11