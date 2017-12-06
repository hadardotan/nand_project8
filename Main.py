import sys
import os
import Translator
import re

def main(path):
    """
    This fucntion classify the two options: .asm file path or directory path.
    """
    files = []
    if os.path.isfile(path):
        abs_path = os.path.abspath(path)
        files.append(abs_path)
        output_path = re.sub(r'(\.vm)$', '', abs_path) + ".asm"
    else:
        dir_path = os.path.abspath(path)
        for f in os.listdir(path):
            f_path = ''.join([path,"/",f])
            if os.path.isfile(f_path):
                if str(f).split('.')[-1] == "vm":
                    files.append(f_path)

        file_name = dir_path.split('/')[-1]
        output_path = ''.join([dir_path,"/",file_name,".asm"])

    lines = Translator.Translator(files,output_path)
    lines.translate()


# if __name__ == "__main__":
#     if len(sys.argv) == 2:
#         main(sys.argv[1])

example_path = r"C:\Users\mika\Desktop\nand2tetris\nand2tetris\projects\08\FunctionCalls\SimpleFunction\SimpleFunction.vm"
main(example_path)