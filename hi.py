
self.init_ram_num()

line = [ "// call " + name + " " +n]
ret = "RET" + str(self.return_address_counter)
# push return_address:
line = ["// push return_address:"]
line.append("@" + ret)
line.append("D=A")
line.append("@SP")
line.append("A=M")
line.append("M=D")
line.append("@SP")
line.append("M=M+1")



# push LCL