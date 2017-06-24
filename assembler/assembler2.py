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
FILE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def one_switcher(num):
    address = ''

    for val in xrange(11, -1, -1):
        if val == num:
            address += '1'
        else:
            address += '0'

    return address

def command_dict_fill(commands_list, command_type, begin=0):
    command_dict = {}

    for index, command in enumerate(commands_list, start=begin):
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


def split_str(seq):
    length = 2
    dummy = []

    for i in range(0, len(seq), length):
        try:
            if seq[i + 1]:
                dummy.append(seq[i:i + length])
        except IndexError:
            dummy.append(seq[i] + ' ')

    return dummy


def split_int(seq):
    dummy = str(seq)
    length = len(dummy)

    if length % 2 != 0:
        dummy = str(seq).zfill(length + 1)

    if len(dummy) != 4:
        dummy = '00' + dummy

    return split_list(dummy.upper())


def split_list(seq):
    length = 2

    return [seq[i:i + length] for i in range(0, len(seq), length)]


def hex_substr(seq):
    dummy = []

    for x in seq:
        dummy.append(x[2:].upper())

    return dummy

def ascii_val(seq):
    return [map(ord, x) for x in seq]


def hex_val(seq):
    return [map(hex, val) for val in ascii_val(seq)]


def hex_to_bin(seq):
    dummy = []

    for x in seq:
        for y in x:
            dummy.append(str(bin(int(y, 16))[2:]).zfill(4))

    return dummy


def list_to_str(seq, option):
    dummy = ''

    if option == 0:
        for elem in seq:
            dummy += elem + ' '

    elif option == 1:
        for bin_list in seq:
            for elem in bin_list:
                dummy += elem + ' '

    return dummy


def adr_sym_repr(label_dictionary):
    adr_sym_dict = []

    for key, value in label_dictionary.iteritems():
        adr_sym_key_list = split_str(key + ',')

        hex_list = split_list(hex_val(adr_sym_key_list))[0]
        hex_list = map(hex_substr, hex_list)
        bin_trans = map(hex_to_bin, hex_list)
        hex_location = split_int(hex(label_dictionary[key])[2:])
        bin_location = map(hex_to_bin, hex_location)

        for index, label_key in enumerate(adr_sym_key_list):
            adr_sym_dict.append([label_key, hex_list[index], bin_trans, hex_location,
                                 bin_location])

    return adr_sym_dict


def first_pass(code):
    location_counter = -2
    label_pattern = re.compile(r'^(\w)+\s*,')
    label_dictionary = OrderedDict()

    for line in code:
        location_counter += 1

        if label_pattern.match(line):
            label_dictionary[label_pattern.match(line).group()[:-1]] = location_counter
        elif re.match(r'^\s*ORG', line):

            org_point_location = re.findall(r'[0-9a-fA-F]+', line)
            try:
                if len(org_point_location) > 0 and int(org_point_location[0], 16):
                    location_counter = int(org_point_location[0], 16) - 1
            except Exception as e:
                pass
        elif re.match(r'^\s*END\s*$', line):
            return label_dictionary

    return label_dictionary


def second_pass(code, label_table):
    location_counter = -2
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
                    elif label_org and int(word, 16):
                        location_counter = int(word, 16) - 1
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
                                if int(word, 16) < 0:
                                    machine_code[hex(location_counter)[2:].upper()] = (bin((1 << 16) - int(word[1:], 16))[2:]).zfill(16)
                                else:
                                    machine_code[hex(location_counter)[2:].upper()] = (bin(int(word, 16))[2:]).zfill(16)

                                machine_code_set = True

                            elif label_flag_dec:
                                if int(word) < 0:
                                    machine_code[hex(location_counter)[2:].upper()] = (bin((1 << 16) - int(word[1:]))[2:]).zfill(16)

                                else:
                                    machine_code[hex(location_counter)[2:].upper()] = (bin(int(word))[2:]).zfill(16)

                                machine_code_set = True

                        elif word == 'I':
                            i_bit = '1'
                        elif word in label_table:
                            label_location = hex(label_table[word])[2:]
                            bin_list = []
                            address = ''

                            if len(label_location) <= 3:
                                for num in label_location:
                                    bin_list.append((bin(int(num, 16))[2:]).zfill(4))
                                address = ''.join(bin_list).zfill(12)
                            else:
                                raise Exception('Label Location Error')
                        else:
                            raise Exception('Unknown command')
                else:
                    if not machine_code_set and not label_org:
                        machine_code[hex(location_counter)[2:].upper()] = (i_bit + op_code + address)

    except Exception as e:
        print e
        machine_code = None
        return machine_code

    return machine_code


def assembler_main(code_string):
    mri_commands = ['AND', 'ADD', 'LDA', 'STA', 'BUN', 'BSA', 'ISZ']
    rri_commands = ['HLT', 'SZE', 'SZA', 'SNA', 'SPA', 'INC', 'CIL', 'CIR', 'CME', 'CMA', 'CLE', 'CLA']
    io_commands = ['IOF', 'ION', 'SKO', 'SKI', 'OUT', 'INP']

    command_dict_fill(mri_commands, 'mri')
    command_dict_fill(rri_commands, 'rri')
    command_dict_fill(io_commands, 'io', 6)

    code = code_string.split('\n')

    label_dictionary = first_pass(code)
    machine_code = second_pass(code, label_dictionary)
    adr_sym_dict = adr_sym_repr(label_dictionary)

    return adr_sym_dict, machine_code

def handle_uploaded_file(f):
    file_name = str(int(time.time()*1000000))
    file_path = os.getcwd()+'/Basic-Computer-Assembler/assembler/media/inputs/'+file_name
    file_content = None
    adr_dict = None
    mac_cod = None

    with open(file_path, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    if os.path.getsize(file_path) < 10000001:
        with open(file_path, 'rb') as source:
            file_content = source.read()
            adr_dict, mac_cod = assembler_main(file_content)

    if os.path.isfile(file_path):
        os.remove(file_path)

    return file_content, adr_dict, mac_cod

def handle_local_file(file_name):
    # file_path = os.getcwd()+'/Basic-Computer-Assembler/assembler/media/inputs/'+file_name
    file_path = os.path.join(FILE_DIR, 'assembler/media/inputs/', file_name)

    with open(file_path, 'rb') as source:
        file_content = source.read()
        adr_dict, mac_cod = assembler_main(file_content)

    return file_content, adr_dict, mac_cod
