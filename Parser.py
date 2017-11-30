
def path_to_lines(file_path):
    """
    This function returns a list of string, each string is a line from vm file.
    :param file_path
    :return: vm_lines
    """
    file = open(file_path)
    lines = []
    file_length = file_number_of_lines(file_path)
    for i in range(file_length):
        line = file.readline()
        lines.append(line)
    file.close()
    return clean_lines(lines)

def file_number_of_lines(file_name):
    """
    This function return the lenght (of rows) of vm file
    :param file_name:
    :return: line_number
    """
    vm_file = open(file_name)
    line_number = 0
    while vm_file.readline():
        line_number += 1
    vm_file.close()
    return line_number

def clean_lines(vm_lines):
    """
    This function cleans all comments ("//") from lines
    :param vm_lines:
    :return: new_lines: cleaned list of vm lines
    """
    new_lines = []
    for i in range(len(vm_lines)):
        line = vm_lines[i].strip()
        comment_start = line.find("//")
        if line == "" or comment_start == 0:
            continue
        elif comment_start > 0:
            line = line[:comment_start]
        new_lines.append(line)
    return new_lines

def line_lst_2_str(line):
    str = ""
    for l in line:
        str += l
        str += "\n"
    return str

