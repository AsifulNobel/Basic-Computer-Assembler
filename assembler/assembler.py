# TODO
# Bad input handling
# Error handling

import re
import copy
import time
import os
from collections import OrderedDict

mri = {}
rri = {}
io = {}

def one_switcher(num):
    address = ''

    for val in xrange(11, -1, -1):
        if val == num:
            address += '1'
        else:
            address += '0'

    return address

def command_dict_fill(commands_list, command_type):
    command_dict = {}

    for index, command in enumerate(commands_list):
        command_dict[command] = index

    if command_type == 'mri':
        global mri
        mri = copy.deepcopy(command_dict)
    elif command_type == 'rri':
        global rri
        rri = copy.deepcopy(command_dict)
    elif command_type == 'io':
        global io
        io = copy.deepcopy(command_dict)

def first_pass(code):
    location_counter = -2
    label_pattern = re.compile(r'^(\w)+\s*,')
    label_dictionary = OrderedDict()

    for line in code:
        location_counter += 1

        if label_pattern.match(line):
            label_dictionary[label_pattern.match(line).group()[:-1]] = location_counter
        elif re.match(r'^\s*ORG', line):
            if re.match(r'\s*[0-9]+\s*', line):
                location_counter = int(re.match(r'\s*[0-9]+\s*', line).group())
        elif re.match(r'^\s*END\s*$', line):
            return label_dictionary


def second_pass(code, label_table):
    location_counter = -1
    label_pattern = re.compile(r'\s*(-{0,1}\w+)\s*')
    code_pattern = re.compile(r'^([^/]*)')
    machine_code = OrderedDict()
    global mri
    global rri
    global io

    try:
        for line_of_code in code:
            op_code = '000'
            i_bit = '0'
            address = ''.zfill(12)
            label_flag_dec = False
            label_flag_hex = False
            machine_code_set = False
            label_org = False
            location_counter += 1

            line = code_pattern.match(line_of_code).group()

            if line == '':
                break

            if label_pattern.match(line):
                words = label_pattern.findall(line)

                for word in words:
                    if word == 'ORG':
                        label_org = True
                    elif label_org:
                        location_counter = int(word) - 1
                        machine_code_set = True
                    elif word == 'END':
                        return machine_code
                    else:
                        if word in mri.keys():
                            op_code = bin(mri[word])[2:].zfill(3)
                        elif word in rri.keys() or word in io.keys():
                            op_code = '111'

                            if word in rri.keys():
                                address = one_switcher(int(rri[word]))
                            else:
                                i_bit = '1'
                                address = one_switcher(int(io[word]))
                        elif word == 'DEC':
                            label_flag_dec = True
                        elif word == 'HEX':
                            label_flag_hex = True
                        elif re.match(r'-*[0-9]+', word):
                            if label_flag_hex:
                                machine_code[str(location_counter)] = (bin(int(word, 16))[2:]).zfill(16)

                                machine_code_set = True

                            elif label_flag_dec:
                                if int(word) < 0:
                                    machine_code[str(location_counter)] = (bin((1 << 16) - int(word[1:]))[2:]).zfill(16)
                                else:
                                    machine_code[str(location_counter)] = (bin(int(word))[2:]).zfill(16)

                                machine_code_set = True

                        elif word == 'I':
                            i_bit = '1'
                        elif word in label_table:
                            address = (bin(int(label_table[word]))[2:]).zfill(12)
                        else:
                            raise Exception('Unknown command')
                else:
                    if not machine_code_set:
                        machine_code[str(location_counter)] = (i_bit + op_code + address)
    except Exception:
        machine_code = None
        return machine_code

    return machine_code

def assembler_main(code_string):
    mri_commands = ['AND', 'ADD', 'LDA', 'STA', 'BUN', 'BSA', 'ISZ']
    rri_commands = ['HLT', 'SZE', 'SZA', 'SNA', 'SPA', 'INC', 'CIL', 'CIR', 'CME', 'CMA', 'CLE', 'CLA']
    io_commands = ['IOF', 'ION', 'SKO', 'SKI', 'OUT', 'INP']

    command_dict_fill(mri_commands, 'mri')
    command_dict_fill(rri_commands, 'rri')
    command_dict_fill(io_commands, 'io')

    code = code_string.split('\n')

    label_dictionary = first_pass(code)
    machine_code = second_pass(code, label_dictionary)

    return label_dictionary, machine_code

def handle_uploaded_file(f):
    file_name = str(int(time.time()*1000000))
    file_content = None
    lb_dict = None
    mac_cod = None

    with open('assembler/media/inputs/'+file_name, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    if os.path.getsize('assembler/media/inputs/'+file_name) < 10000001:
        with open('assembler/media/inputs/'+file_name, 'rb') as source:
            file_content = source.read()
            lb_dict, mac_cod = assembler_main(file_content)

    if os.path.isfile('assembler/media/inputs/'+file_name):
        os.remove('assembler/media/inputs/'+file_name)

    return file_content, lb_dict, mac_cod
