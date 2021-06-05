import os
from subprocess import PIPE, Popen


sep_symb = '!'


def inp_out_file(run_str, tests_file_name='tests.txt', res_file_name='results.txt'):
    result_arr = []
    check_arr = []

    run_file = 'solution.py'
    tmp = open(run_file, 'w')
    tmp.write(run_str)
    tmp.close()

    with open(res_file_name, 'r') as results:
        for line in results:
            check_arr.append(line.rstrip())


    with open(tests_file_name, 'r') as tests:
        counter = 0
        for line in tests:
            input_file = open("input.txt", 'w')
            arr_test = line.strip().split(sep_symb)
            test_result_str = '\n'.join(arr_test)
            input_file.write(test_result_str)
            input_file.close()
            cmd = 'python3 ' + run_file
            os.system(cmd)
            output_file = open('output.txt', 'r')
            if output_file.readline() == check_arr[counter]:
                result_arr.append(True)
            else:
                result_arr.append(False)
            output_file.close()
            counter+=1
    true_counter = 0
    for b in result_arr:
        if b:
            true_counter += 1
    percent = round(true_counter / len(result_arr) * 100, 2)
    return percent



def inp_out_cmd(run_str, tests_file_name='tests.txt', res_file_name='results.txt'):
    check_arr = []
    result_arr = []


    run_file = 'solution.py'
    open(run_file,'w').write(run_str)

    if run_file[-1:-4:-1] == 'txt':
        read_data = open(run_file, 'r').read()
        run_file = run_file[:-3] + 'py'
        open(run_file, 'w').write(read_data)

    with open(res_file_name, 'r') as results:
        for line in results:
            check_arr.append(line.rstrip())

    with open(tests_file_name, 'r') as tests:
        counter = 0
        for line in tests:
            arr_test = line.split(sep_symb)
            command = ['python3 ' + run_file]
            p = Popen(command, stdin=PIPE, stdout=PIPE, shell=True)
            out = p.communicate(input=bytes('\n'.join(arr_test), encoding='utf-8'))[0]
            if out.rstrip().decode('utf-8') == check_arr[counter]:
                result_arr.append(True)
            else:
                result_arr.append(False)
            counter += 1

    true_counter = 0
    for b in result_arr:
        if b:
            true_counter += 1
    percent = round(true_counter / len(result_arr) * 100, 2)
    return percent
