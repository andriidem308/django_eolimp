import os
import time
from subprocess import PIPE, Popen


SEPARATOR = '!'


def test_student_solution(code, exec_time, file_in, file_out):
    temporary_file = 'test_solution.py'
    open(temporary_file, 'w').write(code)

    try:
        test_outputs = list(map(lambda x: x.strip(), open(file_out.path, 'r').readlines()))
        test_inputs = list(map(lambda x: x.strip(), open(file_in.path, 'r').readlines()))

        code_outputs = []

        for curr_test_inputs in test_inputs:
            inputs_list = curr_test_inputs.split(SEPARATOR)

            command = [f'python3 {temporary_file}']

            start_time = time.time()
            p = Popen(command, stdin=PIPE, stdout=PIPE, shell=True)
            buffer = p.communicate(input=bytes('\n'.join(inputs_list), encoding='utf-8'))[0]
            end_time = time.time()

            if (end_time - start_time) * 1000 > exec_time:
                code_outputs.append(None)
            else:
                code_outputs.append(buffer.rstrip().decode('utf-8').split('\n'))

        test_success = 0
        test_total = len(test_outputs)

        for code_output, test_output in zip(code_outputs, test_outputs):
            if code_output:
                if code_output[0] == test_output:
                    test_success += 1

        score = test_success / test_total
    except Exception as e:
        # If Student's code return some exception, his score of this problem becomes equal to zero
        score = 0

    os.remove(temporary_file)
    return score
