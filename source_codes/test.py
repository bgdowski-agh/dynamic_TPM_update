import time,subprocess,shlex,sys,os,datetime
from paramsK import params

def format_timedelta(td):
    td = td - datetime.timedelta(microseconds=td.microseconds)
    td_str = str(td) 
    if 'day' in td_str:
        days, time_part = td_str.split(', ')
        hours, minutes, seconds = time_part.split(':')
        total_hours = int(days.split()[0]) * 24 + int(hours)
        return f"{total_hours:02}:{minutes}:{seconds}"
    else:
        return td_str

iterate = int(sys.argv[1])
total_start_time = time.time() 
open("estimates.txt", "w").close()
iters=len(params)
for param in params:
    print("*** " + str(iters) + " tests remaining ***" )
    start_time=time.time()
    upd_map = {"0": "hebbian", "1": "anti_hebbian", "2": "random_walk", "3": "dynamic_rows", "4": "dynamic_matrix", "5": "random_eve"}
    upd = upd_map.get(str(param[4]), "unknown")
    if param[4] in [3,4]:
        upd_eve = upd_map.get(str(param[5]), "unknown")
    filename= 'test_' + str(param[0]) + '_' + str(param[1]) + '_' + str(param[2]) + '_qber' + str(param[3]) + '_' + upd + '.txt'
    name= 'K=' + str(param[0]) + ' N=' + str(param[1]) + ' L=' + str(param[2]) + ' qber=' + str(param[3]) + ' ' + upd
    if param[4] in [3,4]:
        filename = filename[:-4] + "_" + upd_eve + ".txt"
        name = name + " " + upd_eve

    if os.path.exists(filename):
        os.system("rm " + filename)

    log = open(filename, 'a+')
    log.write(name + '\n')
    log.flush()
    
    print("*** \n Script is running for " + name + "\n***")

    for i in range(iterate):
        txt="*** " + str(i+1) + " iteration ***" 
        sys.stdout.write('\r' + txt) 
        command = "python3 run.py " + str(param[0]) + ' ' + str(param[1]) + ' ' + str(param[2]) + ' ' + str(param[3]) + ' ' + str(param[4])
        if param[4] in [3,4]:
            command = command + ' ' + str(param[5]) 
        args = shlex.split(command)
        while True:
            process = subprocess.Popen(args, stdout=log, stderr=log)
            try:
                process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                process.kill()
                sys.stdout.write("\r*** " + str(i+1) + " iteration again*** \r")
                continue
            break
    end_time = time.time()
    time_taken = end_time - start_time 
    iter_time=format_timedelta(datetime.timedelta(seconds=time_taken))
    total_elapsed = format_timedelta(datetime.timedelta(seconds=(end_time - total_start_time)))
    iters-=1
    completed_tests = len(params) - iters
    remaining_time = format_timedelta(datetime.timedelta(seconds=int((((end_time-total_start_time)/completed_tests)*iters))))
    estimate = format_timedelta(datetime.timedelta(seconds=((end_time-total_start_time)*(1+iters/completed_tests))))
    with open("estimates.txt", "a") as est_file:
        est_file.write(estimate + "\n")
    print("\n*** \n Script has finished running for " + name + "\n" + "it took " + str(iter_time) + ", total elapsed: " + str(total_elapsed) + ", remaining estimated time: " + str(remaining_time) + ", estimated total time: " + str(estimate) + " ***")
with open("estimates.txt", "a") as est_file:
    est_file.write(total_elapsed + "\n")  

sys.exit()