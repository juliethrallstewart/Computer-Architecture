"""CPU functionality."""

"""
* R5 is reserved as the interrupt mask (IM)
* R6 is reserved as the interrupt status (IS)
* R7 is reserved as the stack pointer (SP)
"""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.running = True
        self.pc = 0
        self.SP = 7 #stack pointer
        self.fl = [0] * 8
        self.reg = [0] * 8 #R5, R6, R7 is reserved, no slot over 255
        self.ram = [0] * 256

    def load_memory(self, filename):
    
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    # Ignore comments
                    line = line.split("#")[0]
                    line = line.strip()

                    if line == "":
                        continue  # Ignore blank lines

                    value = int(line, 2)   # Base 10, but ls-8 is base 2
            

                    self.ram[address] = value
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)


        if len(sys.argv) != 2:
            print("Usage: file.py filename", file=sys.stderr)
            sys.exit(1)

        print(self.ram)   

    def load(self):
        """Load a program into memory."""
        self.running = True

        address = 0
        
        self.load_memory(sys.argv[1])

        
        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8 set the value of a register to an integer
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0, Print numeric value stored in the given register. (as  a decimal)
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        self.reg[7] = 0xF4


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """


        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # read the memory address that's stored in register `PC`, and store that result in `IR`, the _Instruction Register_
    def run(self):
        """Run the CPU."""
       
        self.trace()
        print(self.ram, "RAM")
        print(self.reg, "REG")

        while self.running == True:
            IR = self.ram_read(self.pc) #IR = Instruction Register
            register_a = self.ram_read(self.pc + 1)
            register_b = self.ram_read(self.pc + 2)

            if IR == 0b10000010: #LDI 0b10000010
                self.reg[register_a] = register_b
                self.pc += 3
                
            elif IR == 0b01000111: #PRN 0b01000111 - Print numeric value stored in the given register.
                value = self.reg[int(str(register_a))]
                print(value)
                self.pc += 2
            elif IR == 0b0000000: #HLT 0b0000000
                self.running = False
                self.pc += 1
            elif IR == 0b10100010:
                self.reg[register_a] *= self.reg[register_b]
                self.pc += 3

            elif IR == 0b01000101: #PUSH
                reg = self.ram[self.pc + 1]
                val = self.reg[reg]
                self.reg[self.SP] -= 1
                self.ram[self.reg[self.SP]] = val
                self.pc += 2
                
            elif IR == 0b01000110: #POP
                reg = self.ram[self.pc + 1]
                val = self.ram[self.reg[self.SP]]
                self.reg[reg] = val
                self.reg[self.SP] += 1
                self.pc += 2
            
            elif IR == 0b10100111: #CMP     Compare the values in two registers.
                val_a = self.reg[register_a]
                val_b = self.reg[register_b]
                if val_a == val_b: #567 = #LGE
                    self.fl[5] = 0
                    self.fl[6] = 0
                    self.fl[7] = 1
                    self.pc += 3
                elif val_a < val_b:
                    self.fl[5] = 1
                    self.fl[6] = 0
                    self.fl[7] = 0
                    self.pc += 3
                elif val_a > val_b:
                    self.fl[5] = 0
                    self.fl[6] = 1
                    self.fl[7] = 0
                    self.pc += 3
            
            elif IR == 0b01010100: #JMP to the address stored in the given register.
                address = self.reg[register_a]
                self.pc = address

            elif IR == 0b01010101: #JEQ
                # print(self.fl[7], "line 205")
                if self.fl[7] == 1:
                    address = self.reg[register_a]
                    # print(address, "line 208")
                    self.pc = address
                else:
                    self.pc += 2
               
            elif IR == 0b01010110: #JNE
                # print(self.fl[7], "libne 212")
                if self.fl[7] == 0:
                    address = self.reg[register_a]
                    # print(address, "ADDRESS")
                    self.pc = address
                else:
                    self.pc += 2

            
                

            else:
                print(f"Error: Unknown IR: {IR}")
                sys.exit(1)

# If `E` flag is clear (false, 0), jump to the address stored in the given
#register.
# Set the `PC` to the address stored in the given register.

    #accept the address to read and return the value stored there.

    # Using `ram_read()`,
# read the bytes at `PC+1` and `PC+2` from RAM into variables `operand_a` and
# `operand_b` in case the instruction needs them.
    def ram_read(self, address): #_Memory Address Register_ 
        return self.ram[address]

      
        
        

    #accept a value to write, and the address to write it to
    def ram_write(self, address, value): #_Memory Data Register_ 
        self.ram[address] = value
    

# print(sys.argv[0], "sys args [0]")

# # cd into src or the file directory itself
# # in terminal $python 03_modules.py
# # in terminal $python 03_modules.py tacos pizza
# args = [arg for arg in sys.argv]
# print(args)

# for arg in sys.argv:
#     print(arg, "arg in sys.argv")