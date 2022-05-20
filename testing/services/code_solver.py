import os
from subprocess import PIPE, Popen


SEPARATOR = '!'


def inp_out_cmd(code, file_in, file_out):
    test_file = 'solution.py'
    open(test_file, 'w').write(code)

    try:
        file_outputs = open(file_out.path, 'r').read().split('\n')
        tests = open(file_in.path, 'r').readlines()
        code_out = []
        for line in tests:
            file_inputs = line.rstrip().split(SEPARATOR)
            command = ['python3 ' + test_file]
            p = Popen(command, stdin=PIPE, stdout=PIPE, shell=True)
            buffer = p.communicate(input=bytes('\n'.join(file_inputs), encoding='utf-8'))[0]
            code_out.append(buffer.rstrip().decode('utf-8').split('\n'))

        result_arr = [co[0] == fo for co, fo in zip(code_out, file_outputs)]
        score = result_arr.count(True) / len(result_arr)
    except Exception as e:
        score = 0

    os.remove(test_file)
    return score
