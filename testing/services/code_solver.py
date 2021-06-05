import os
from subprocess import PIPE, Popen


SEPARATOR = '!'


def inp_out_cmd(code, file_in, file_out):
    test_file = 'solution.py'
    open(test_file, 'w').write(code)

    file_outputs = open(file_out, 'r').read().split('\n')

    tests = open(file_in, 'r').readlines()
    buffer = ''
    for line in tests:
        file_inputs = line.rstrip().split(SEPARATOR)

        command = ['python3 ' + test_file]
        p = Popen(command, stdin=PIPE, stdout=PIPE, shell=True)
        buffer = p.communicate(input=bytes('\n'.join(file_inputs), encoding='utf-8'))[0]

    code_out = buffer.rstrip().decode('utf-8').split('\n')
    result_arr = [co == fo for co, fo in zip(code_out, file_outputs)]
    score = round(100 * result_arr.count(True) / len(result_arr), 2)

    return score
