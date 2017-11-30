import re
import Parser
import os

Sp = "SP"
Local = "LCL"
Argument = "ARG"
This = "THIS"
That = "THAT"
Temp = "5"
Static = "16"

class Translator():
    """
    generates asm file from vm files
    """

    def __init__(self, files, output_path):
        self.lables_counter = 0
        self.vm_lines = []
        for path in files:
            self.vm_lines += Parser.path_to_lines(path)
        self.output_path = output_path


    def translate(self):
        """
        creat new .asm file and write into it the translated .vm lines
        :return:
        """
        out_file = open(self.output_path, "w+")
        for i in range(len(self.vm_lines)):
            translated = self.vm_to_asm(self.vm_lines[i])
            out_file.write(translated)
        out_file.close()

    def vm_to_asm(self, line):
        """
        translates vm line to asm lines
        """
        as_list = line.split(' ')
        if as_list[0] == 'lable':
            return self.lable_command(as_list[1])
        if as_list[0] == 'goto':
            return self.goto_command(as_list[1])
        if as_list[0] == 'if-goto':
            return self.if_goto_command(as_list[1])





        if (len(as_list)) == 1:

            return self.aritmetics_commands(line.strip())
        command, segment, i = as_list[0], as_list[1], as_list[2]
        if segment == 'this' or segment == 'that':
            return self.this_that_command(command,segment,i)
        if segment == 'constant':
            return self.constant_command(i)
        if segment == "local" or segment == "argument":
            return self.local_argument_command(command, segment, i)
        if segment == 'temp':
            return self.temp_command(command, i)
        if segment == 'pointer':
            return self.pointer_command(command, i)
        if segment == 'static':
            return self.static_command(command, i)

    def this_that_command(self, command , segment , i):
        """
        generates asm code for vm command
        :return: string  of asm code for the vm command
        """
        line = ["// " + command + " " + segment + " " + i]
        ram = That
        if segment == 'this':
            ram = This
        line.append("@" + ram)
        line.append("D=M")
        line.append("@"+i)
        if command == 'push':
            line.append("A=D+A")
            line.append("D=M")
            line.append("@SP")
            line.append("A=M")
            line.append("M=D")
            line.append("@SP")
            line.append("M=M+1")
            return Parser.line_lst_2_str(line)
        if command == 'pop':
            line.append("D=D+A")
            line.append("@R13")
            line.append("M=D")
            line.append("@SP")
            line.append("AM=M-1")
            line.append("D=M")
            line.append("@R13")
            line.append("A=M")
            line.append("M=D")
            return Parser.line_lst_2_str(line)

    def constant_command(self,i):
        """
        generates asm code for vm command
        :return: string  of asm code for the vm command
        """
        line = ["// push constant " + i]
        line.append("@" + i)
        line.append("D=A")
        line.append("@SP")
        line.append("A=M")
        line.append("M=D")
        line.append("@SP")
        line.append("M=M+1")
        return Parser.line_lst_2_str(line)

    def local_argument_command(self, command , segment , i):
        """
        generates asm code for vm command
        :return: string  of asm code for the vm command
        """
        line = ["// " + command + " " + segment + " " + i]
        line.append("@" + self.ram_for_segment(segment))
        line.append("D=M")
        line.append("@" + i)
        if command == 'push':
            line.append("A=D+A")
            line.append("D=M")
            line.append("@SP")
            line.append("A=M")
            line.append("M=D")
            line.append("@SP")
            line.append("M=M+1")
            return Parser.line_lst_2_str(line)
        if command == 'pop':
            line.append("D=D+A")
            line.append("@R13")
            line.append("M=D")
            line.append("@SP")
            line.append("AM=M-1")
            line.append("D=M")
            line.append("@R13")
            line.append("A=M")
            line.append("M=D")
            return Parser.line_lst_2_str(line)

    def temp_command(self, command , i):
        """
        generates asm code for vm command
        :return: string  of asm code for the vm command
        """
        line = ["// " + command + " temp " + i]
        line.append("@" + self.ram_for_segment("temp"))
        line.append("D=M")
        index = int(self.ram_for_segment("temp")) + int(i)
        line.append("@" + str(index))      # D = 5 + i
        if command == 'push':
            line.append("A=D+A")
            line.append("D=M")
            line.append("@SP")
            line.append("A=M")
            line.append("M=D")
            line.append("@SP")
            line.append("M=M+1")
            return Parser.line_lst_2_str(line)
        if command == 'pop':
            line.append("D=D+A")
            line.append("@R13")
            line.append("M=D")
            line.append("@SP")
            line.append("AM=M-1")
            line.append("D=M")
            line.append("@R13")
            line.append("A=M")
            line.append("M=D")
            return Parser.line_lst_2_str(line)

    def pointer_command(self, command, i):
        """
        generates asm code for vm command
        :return: string  of asm code for the vm command
        """
        ram = That
        if i == "0":
            ram = This
        line = ["// " + command + " pointer " + i]
        line.append("@" + ram)
        if command == 'push':
            line.append("D=M")
            line.append("@SP")
            line.append("A=M")
            line.append("M=D")
            line.append("@SP")
            line.append("M=M+1")
            return Parser.line_lst_2_str(line)
        if command == 'pop':
            line.append("D=A")
            line.append("@R13")
            line.append("M=D")
            line.append("@SP")
            line.append("AM=M-1")
            line.append("D=M")
            line.append("@R13")
            line.append("A=M")
            line.append("M=D")
            return Parser.line_lst_2_str(line)

    def static_command(self,command, i):
        """
        generates asm code for vm command
        :return: string  of asm code for the vm command
        """
        line = ["//" + command + "static" + i]
        index = 16 + int(i)
        line.append("@" + str(index))
        if command == 'pop':
            line.append("D=A")
            line.append("@R13")
            line.append("M=D")
            line.append("@SP")
            line.append("AM=M-1")
            line.append("D=M")
            line.append("@R13")
            line.append("A=M")
            line.append("M=D")
            return Parser.line_lst_2_str(line)
        if command == 'push':
            line.append("D=M")
            line.append("@SP")
            line.append("A=M")
            line.append("M=D")
            line.append("@SP")
            line.append("M=M+1")
            return Parser.line_lst_2_str(line)

    def aritmetics_commands(self, command):
        """
        generates asm code for vm command
        :return: string  of asm code for the vm command
        """
        line = ["// " + command]
        if command == "neg":
            line.append("D=0")
            line.append("@SP")
            line.append("A=M-1")
            line.append("M=D-M")
            return Parser.line_lst_2_str(line)
        if command == "not":
            line.append("@SP")
            line.append("A=M-1")
            line.append("M=!M")
            return Parser.line_lst_2_str(line)
        if command in ["eq","lt","gt"]:
            return self.compare_command(command)
        operator = "+"
        if command == "sub":
            operator = "-"
        if command == "and":
            operator = "&"
        if command == "or":
            operator = "|"
        line.append("@SP")
        line.append("A=M-1")
        line.append("D=M")
        line.append("A=A-1")
        line.append("M=M"+operator+"D")
        line.append("D=A+1")
        line.append("@SP")
        line.append("M=D")
        return Parser.line_lst_2_str(line)

    def ram_for_segment(self, segment):
        if segment == 'temp':
            return Temp
        if segment == 'local':
            return Local
        if segment == 'argument':
            return Argument
        if segment == 'this':
            return This
        if segment == 'that':
            return That
        if segment == 'static':
            return Static

    def compare_command(self, command):
        """
        generates asm code for vm command
        :return: string  of asm code for the vm command
        """
        line = ["// "+command]
        true = command.upper() + str(self.lables_counter)
        end = "END" + str(self.lables_counter)
        condition = "JEQ"
        if command == "gt":
            condition = "JGT"
        if command == "lt":
            condition = "JLT"

        self.lables_counter +=1
        line +=[
        '@SP',
        'M=M-1',
        'A=M',
        'D=M',
        '@R13',
        'M=D',
        '@SP',
        'M=M-1',
        'A=M',
        'D=M-D',
        '@'+true,
        'D;'+condition,
        '@SP',
        'A=M',
        'M=0',
        '@'+end,
        '0;JMP',
        '('+true+')',
        '@SP',
        'A=M',
        'M=-1',
        '@'+end,
        '0;JMP',
        '('+end+')',
        '@SP',
        'M=M+1']
        return Parser.line_lst_2_str(line)
