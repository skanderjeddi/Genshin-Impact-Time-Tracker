import psutil
import time
import os.path
import sys

DATA_FILE = 'gi-tracker.dat'
GI_P_NAME = 'GenshinImpact.exe'

def main():
    print('Genshin Impact Time Tracker - by Uberfap (CTRL-C to exit)')
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as data_file:
            create_default(data_file)
    with open(DATA_FILE, 'r') as data_file:
        proc_checks_delay, prog_print_delay, curr_record = read_data(data_file)
    print('Current recorded time: {} minute(s) ({} hour(s))'.format(curr_record, curr_record / 60))
    print('Game process detection will occur every {} minute(s)'.format(proc_checks_delay))
    print('Progress will be printed every {} minute(s)'.format(prog_print_delay))
    start_time = time.time()
    first_idle, first_detection = True, True
    while True:
            p_names = [p.name() for p in psutil.process_iter()]
            if GI_P_NAME not in p_names:
                if first_idle:
                    print('Genshin Impact process not detected - idling...')
                    with open(DATA_FILE, 'r') as data_file:
                        content = data_file.readlines()
                    new_content = []
                    for line in content:
                        if line.startswith('curr_record_mins'):
                            line = 'curr_record_mins = {}'.format(curr_record)
                        new_content.append(line)
                    # print('Writing {}'.format(new_content))
                    with open(DATA_FILE, 'w') as data_file:
                        data_file.write(''.join(new_content))
                    first_idle = False
                    first_detection = True
                time.sleep(proc_checks_delay * 60)
            else:
                if first_detection:
                    print('Genshin Impact process detected!')
                    first_detection = False
                    first_idle = True
                curr_record += 1
                if curr_record % prog_print_delay == 0:
                    print('\t+{} ({})'.format(prog_print_delay, curr_record))
                    if curr_record % 60 == 0:
                        print('\t\t+1 hour!')
                time.sleep(60.0 - ((time.time() - start_time) % 60.0))

def create_default(data_file):
    data_file.write('proc_detect_delay_mins = 1\n')
    data_file.write('prog_print_delay_mins = 15\n')
    data_file.write('curr_record_mins = 0')

def read_data(data_file):
    proc_checks_delay = int(data_file.readline().strip().split("=")[1])
    prog_print_delay = int(data_file.readline().strip().split("=")[1])
    curr_record = int(data_file.readline().strip().split("=")[1])
    return proc_checks_delay, prog_print_delay, curr_record

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting...', end='', flush=True)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)