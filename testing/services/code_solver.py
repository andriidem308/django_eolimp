import os
from subprocess import PIPE, Popen


SEPARATOR = '!'


def inp_out_cmd(code, file_in, file_out):
    temporary_file = 'test_solution.py'
    open(temporary_file, 'w').write(code)

    try:
        test_outputs = open(file_out.path, 'r').read().split('\n')
        test_inputs = open(file_in.path, 'r').readlines()

        code_outputs = []

        for curr_test_inputs in test_inputs:
            inputs_list = curr_test_inputs.rstrip().split(SEPARATOR)

            command = [f'python3 {temporary_file}']
            p = Popen(command, stdin=PIPE, stdout=PIPE, shell=True)
            buffer = p.communicate(input=bytes('\n'.join(inputs_list), encoding='utf-8'))[0]

            code_outputs.append(buffer.rstrip().decode('utf-8').split('\n'))

        result_arr = [code_output[0] == test_output for code_output, test_output in zip(code_outputs, test_outputs)]

        test_success = result_arr.count(True)
        test_total = len(result_arr)

        score = test_success / test_total
    except Exception as e:
        # If Student's code return some exception, his score of this problem becomes equal to zero
        score = 0

    os.remove(temporary_file)
    return score
