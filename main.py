# Basic Processor Sim
# Iteration 1
# Start: 3/30/23
# End: ??/??/?? TODO Fill out date at end of iteration
#
# Author: Elliot Bidwell
# mattelliotbidwell@gmail.com
#
# TODO Finish description
# Description:
# The beginning of my attempt at building a computer processor simulator. The current, very rough, plan is to make the
# bitness either 16 or 32-bit, and to devise a very minimalist instruction set most likely made up of quad codes.
# Besides that, the rest of the plan still needs to be fleshed out, specifically the implementation in general.
#
# Plan:
#   3 Classes:
#         TODO Ponder this:
#           - How the hell am I going to implement a multistage pipeline? Maybe take inspiration from QtRVSim as
#               a last resort. I should recall what each stage of the pipeline is responsible for, and when each action
#               performed by each stage is completed. Remember that write-back happens before the read in the decode
#               stage, and that in between each stage is an interstage buffer register (which can probably be
#               implemented in the RegisterFile class, or as separate classes). Maybe I make a method for each buffer
#               that acts as a setter that sets the buffer's contents to the incoming instruction object, while sending
#               its current contents to the next stage in the pipeline, or however its supposed to work.
#           - Calculating jump targets? Probably target + 1 or something akin to that to account for labels. I might
#               need to create something similar to a symbol table for the labels and their addresses but I'm not sure.
#           - Require "HALT"/"END" instruction at end of source file? Sure, why not?
#           - What interfaces should this class have? Getters? Setters? Print to file/console?
#       - ProcessorCore: The primary functional piece of the simulator. Main will only call methods from this class,
#         and calls to any of the other class (probably) will be made by the ProcessorCore itself or by those other
#         classes. The constructor's arguments will include a source file name, and perhaps some booleans to tell the
#         new object whether to print different types of error messages for debugging, or to run in a rudimentary
#         verbose mode. Upon calling this constructor, it will instantiate a CodeGenerator and call its method to read
#         and translate the source file while passing in the file's name (NOTE: The read/translate functionality may
#         end up being built into the CodeGenerator constructor, rather than in its own separate method. Although, if
#         you consider the Single Responsibility Principle, this may not be a good idea). Then, main will call the
#         ProcessorCore's interpret function, which will access the list of instructions in the CodeGenerator object
#         and use a switch statement to execute each of them in sequence. I would like the Processor core to only deal
#         with fully encoded binary instructions, since it lends more to the nature of this being a simulator.
#         It will also use the index of that list as a program counter, and will support fully support conditional
#         branch and unconditional jump instructions.
#               This class will implement a multistage pipelined processor, hopefully with 5 stages: fetch, decode,
#         execute, memory, write-back. This is going to be the most difficult part of this project by far, and
#         at this point I'm really not sure how to implement it, so I need to almost fully implement every other
#         piece first. Something I didn't account for is data memory, which shouldn't be too difficult if I
#         remember how to properly handle memory addressing.
#           * INTERFACES:
#               - Method for printing object code (i.e., binary) to a file
#               - Methods for printing errors/execution results to console/file
#               - Not sure what kind of getters/setters to implement. Maybe one for printing the contents of all the
#                   lists/tables in each of the other objects/classes involved in each of the stages of the pipeline
#
#         TODO Ponder this:
#           - Labels? Word staring and ending in "_", or ending in ":", only letters and maybe numbers, but no symbols.
#           - I think the instruction mnemonics should be case sensitive, but should they be in all caps, all
#               lowercase, or mixed/camelcase/first-letter-caps? Either all caps or all lowercase, since these would
#               probably look the best, and that's all we really care about, am I right? However I'll probably
#               I guess I simply refuse to
#               develop an ugly assembly language, or, at least, one that's any uglier than the others. The bottom line
#               is it's not going to be even slightly uglier than it has to be, because this is my baby and nobody
#               wants an ugly baby.
#           - How are you going to generate the machine code? Maybe use lexical and syntactic analyzers.
#           - Could get away with just implementing lexical under the assumption that each instruction
#               has to be on a separate line that ends in ";" and the contents of each line is a single token.
#               Although, it might need a way to distinguish between which part of a line corresponds with which
#               of the four parts of its corresponding quad code, but this can most likely be circumvented using the
#               magic of offensively bad programming. It'll treat every line pretty much the same, it just needs a
#               reserve table for the instruction mnemonics so it can match and translate the opCode, or print an
#               error if it's an invalid mnemonic. If it catches an error, it should still read the entire line and
#               print it as part of the error message while specifically pointing out which part of the
#               line was invalid.
#           - Should the operands of an instruction being referred to in the assembly source by their mnemonics rather
#               than their numeric designations be optional or mandatory, or should mnemonics in the source code not
#               be supported at all? The first option would be the most difficult, the second would be less so,
#               and the third option would be easiest and least ambitious, but also the least interesting. Making it
#               optional would require me to implement support for the possibility of two different varieties of token
#               for the operands, and I think this would be the best and most interesting exercise of my skills, but
#               it might end up being too much trouble. Making it mandatory would probably be slightly to significantly
#               less difficult, but would likely still be interesting. Both of these would require implementing some
#               way of translating the mnemonics into their corresponding numeric designations (i.e., index in the
#               register file), which I would probably do with another reserve table. The third option, not supporting
#               mnemonics, would definitely be the simplest way to go, and I should consider just doing this for the
#               the first iteration.
#               NOTE: I may have to require either the use of mnemonics or for the operands to start with a specific
#                   character in order to distinguish between register and immediate values. The immediates will
#                   always be the first operand. Actually, maybe if the CodeGenerator recognizes the instruction's
#                   opcode, it can determine whether there is an immediate value in the op1 place in the current
#                   line of code and know what to look for. However, I'm not sure if this will help check whether
#                   the syntax is valid. I suppose if the register operands are written as numerics, accidentally
#                   using an immediate instruction instead of a register operand one would result in the "compiler"
#                   (i.e., the CodeGenerator) treating the numeric designation in the op1 place as an immediate value.
#                   This would obviously be an error, and if I implement all this correctly I can allow the "compiler"
#                   to catch this error and halt to inform the programmer. This would probably require the use of
#                   mnemonics in some way, and if I want to make mnemonics optional, I'd have to require the numeric
#                   designations to start with a specific character. Making mnemonics mandatory is probably the
#                   simplest solution.
#       - CodeGenerator: Reads basic assembly code from a source txt file and translates it into "machine code".
#         It may have to use a lexical and a syntactic analyzer, which may end up being separate classes. Upon
#         translating an instruction, it will create an instruction object and add it to a list which will serve as
#         an abstraction of instruction memory and can be accessed externally through a getter. The processor core
#         will execute this sequence of instructions and use its indexes as a program counter.
#           * INTERFACES:
#               - Getter that returns the instruction located at the passed-in index of the
#                   "instruction memory" list.
#
#         TODO Ponder this:
#           - For branch target back-filling, should the setter method for branch targets do error checking to make
#               sure that the instruction at the designated index is actually a branch? Maybe it could print a console
#               message, but it doesn't seem like any calls should be made to this method that pass in non-branch
#       - RegisterFile: Contains multidimensional list object whose elements each contain the binary encoding of the
#         register's contents, a string to designate the datatype of the data stored, and the value's high-level
#         representation
#           * INTERFACES:
#               - Setter that sets contents of a single register designated by a passed in int to represent
#                   that register's index/numeric name. It will take as arguments the index of the register and the
#                   value it is to be set to
#               - Setter that sets the third operand of
#               - Getter that returns the binary and high-level value stored in the register at the passed-in index.
#
#   Lofty, ambitious stuff to hopefully add later:
#       - Branch predictor
#
#
#
#
# TODO Write at least some pseudocode before jumping in
# Pseudocode:


class QuadReserve:

    def __init__(self):
        self.quad_tablelist = [
            # For all except branches, op3 is the destination register
            # For immediate instructions, op1 is the immediate
            # For single operand instructions, only op1 is used
            # For nops, the syntax doesn't allow anything but ";" to follow the "nop", so no operands used

            # ***LITTLE ENDIAN***
            #["halt",    "00000000"], # 0    all operands ignored
            #["add",     "10000000"], # 1
            #["addi",    "01000000"], # 2
            #["sub",     "11000000"], # 3
            #["subi",    "00100000"], # 4
            #["mult",    "10100000"], # 5
            #["multi",   "01100000"], # 6
            #["div",     "11100000"], # 7
            #["divi",    "00010000"], # 8
            #["and",     "10010000"], # 9
            #["andi",    "01010000"], # 10
            #["or",      "11010000"], # 11
            #["ori",     "00110000"], # 12
            #["not",     "10110000"], # 13   single operand
            #"noti",    "01110000"], # 14
            #["xor",     "11110000"], # 15
            #["xori",    "00001000"], # 16
            #["sll",     "10001000"], # 17   single operand
            #["slli",    "01001000"], # 18   single operand
            #["srl",     "11001000"], # 19   single operand
            #["srli",    "00101000"], # 20   single operand
            #["mov",     "10101000"], # 21   single operand
            #["movi",    "01101000"], # 22   single operand

            # For branches, op3 is the target
            #["jump",    "11101000"], # 23  branch unconditional, value of op3 is the target
            #["bz",      "00011000"], # 24  branch zero, if op1 = 0, two used operands: op1, op3
            #["bpos",    "10011000"], # 25  branch positive, if op1 > 0,
            #["bneg",    "01011000"], # 26  branch negative, if op1 < 0
            #["bnz",     "11011000"], # 27  branch not zero, if op1 != 0
            #["bnp",     "00111000"], # 28  branch not positive, if op1 <= 0
            #["bnn",     "10111000"], # 29  branch not negative, if op1 >= 0
            #["jmpr",    "01111000"], # 30  branch unconditional (register), value op3 is index of a register
            # TODO For print instruction, figure out how to determine what datatype op1 should be printed as.
            #   Not sure if current implementation will work well
            #["prnti",   "11111000"], # 31  prints contents of op1 to console as signed int
            #["prntu",   "00000100"], # 32  prints contents of op1 to console as unsigned int
            #["prntc",   "10000100"], # 33  prints contents of op1 to console as char
            #["nop",     "01000100"], # 34  NO OP, processor does nothing, no operands

            # ***BIG ENDIAN***
            #["halt", "00000000"],  # 0    all operands ignored
            #["add", "00000001"],  # 1
            #["addi", "00000010"],  # 2
            #["sub", "00000011"],  # 3
            #["subi", "00000100"],  # 4
            #["mult", "00000101"],  # 5
            #["multi", "00000110"],  # 6
            #["div", "00000111"],  # 7
            #["divi", "00001000"],  # 8
            #["and", "00001001"],  # 9
            #["andi", "00001010"],  # 10
            #["or", "00001011"],  # 11
            #["ori", "00001100"],  # 12
            #["not", "00001101"],  # 13   single operand
            #["noti", "00001110"],  # 14
            #["xor", "00001111"],  # 15
            #["xori", "00010000"],  # 16
            #["sll", "00010001"],  # 17   single operand
            #["slli", "00010010"],  # 18   single operand
            #["srl", "00010011"],  # 19   single operand
            #["srli", "00010100"],  # 20   single operand
            #["mov", "00010101"],  # 21   single operand
            #["movi", "00010110"],  # 22   single operand

            # For branches, op3 is the target
            #["jump", "00010111"],  # 23  branch unconditional, value of op3 is the target
            #["bz", "00011000"],  # 24  branch zero, if op1 = 0, two used operands: op1, op3
            #["bpos", "00011001"],  # 25  branch positive, if op1 > 0,
            #["bneg", "00011010"],  # 26  branch negative, if op1 < 0
            #["bnz", "00011011"],  # 27  branch not zero, if op1 != 0
            #["bnp", "00011100"],  # 28  branch not positive, if op1 <= 0
            #["bnn", "00011101"],  # 29  branch not negative, if op1 >= 0
            #["jmpr", "00011110"],  # 30  branch unconditional (register), value op3 is index of a register
            # TODO For print instruction, figure out how to determine what datatype op1 should be printed as.
            #   Not sure if current implementation will work well
            #["prnti", "00011111"],  # 31  prints contents of op1 to console as signed int
            #["prntu", "00100000"],  # 32  prints contents of op1 to console as unsigned int
            #["prntc", "00100001"],  # 33  prints contents of op1 to console as char
            #["nop", "00100010"],  # 34  NO OP, processor does nothing, no operands

            ["halt", 0b00000000],  # 0    all operands ignored
            ["add",  0b00000001],  # 1
            ["addi", "00000010"],  # 2
            ["sub", "00000011"],  # 3
            ["subi", "00000100"],  # 4
            ["mult", "00000101"],  # 5
            ["multi", "00000110"],  # 6
            ["div", "00000111"],  # 7
            ["divi", "00001000"],  # 8
            ["and", "00001001"],  # 9
            ["andi", "00001010"],  # 10
            ["or", "00001011"],  # 11
            ["ori", "00001100"],  # 12
            ["not", "00001101"],  # 13   single operand
            ["noti", "00001110"],  # 14
            ["xor", "00001111"],  # 15
            ["xori", "00010000"],  # 16
            ["sll", "00010001"],  # 17   single operand
            ["slli", "00010010"],  # 18   single operand
            ["srl", "00010011"],  # 19   single operand
            ["srli", "00010100"],  # 20   single operand
            ["mov",   "00010101"],  # 21   single operand
            ["movi", 0b00010110],  # 22   single operand

            # For branches, op3 is the target
            ["jump", "00010111"],  # 23  branch unconditional, value of op3 is the target
            ["bz", "00011000"],  # 24  branch zero, if op1 = 0, two used operands: op1, op3
            ["bpos", "00011001"],  # 25  branch positive, if op1 > 0,
            ["bneg", "00011010"],  # 26  branch negative, if op1 < 0
            ["bnz", "00011011"],  # 27  branch not zero, if op1 != 0
            ["bnp", 0b00011100],  # 28  branch not positive, if op1 <= 0
            ["bnn", "00011101"],  # 29  branch not negative, if op1 >= 0
            ["jmpr", "00011110"],  # 30  branch unconditional (register), value op3 is index of a register
            # TODO For print instruction, figure out how to determine what datatype op1 should be printed as.
            #   Not sure if current implementation will work well
            ["prnti", "00011111"],  # 31  prints contents of op1 to console as signed int
            ["prntu", "00100000"],  # 32  prints contents of op1 to console as unsigned int
            ["prntc", 0b00100001],  # 33  prints contents of op1 to console as char
            ["nop", 0b00100010],  # 34  NO OP, processor does nothing, no operands
        ]

    def get_index(self, mnem_or_code):
        for i in range(0, len(self.quad_tablelist)):
            if (self.quad_tablelist[i][0] == mnem_or_code) or (self.quad_tablelist[i][1] == mnem_or_code):
                return i

    def get_opcode(self, mnem_or_index):

        opcode = "undef"

        if isinstance(mnem_or_index, int):
            return self.quad_tablelist[mnem_or_index][1]

        elif isinstance(mnem_or_index, str):
            for quad in self.quad_tablelist:

                if quad[0] == mnem_or_index:
                    opcode = quad[1]

        return opcode

    def get_halt(self):
        print(f'halt {int(self.quad_tablelist[0][1])}')
        return self.quad_tablelist[0][1]

    def get_mnem(self, code_or_index):
        mnemonic = "undef"

        if isinstance(code_or_index, int):
            return self.quad_tablelist[code_or_index][0]

        elif isinstance(code_or_index, str):
            for quad in self.quad_tablelist:

                if quad[1] == code_or_index:
                    mnemonic = quad[0]

        return mnemonic


# Tokens:
#   - opCode: letter followed by any amount of letters, followed by space or tab
#   - operand: TODO Define register mnemonics and format of numeric designations, as well as immediate value format
# Edge Cases:
#   - If token halt is read, set operands to 0, add to instruction mem table, and stop parsing source code altogether
#   - Possibly treat labels as nops
class LexicalAnalyzer:

    def __init__(self, source_name, vrbs, quad_table):
        self.source_file = open(source_name, "r")
        self.verbose_mode = vrbs
        self.quad_reserve = quad_table

# class CodeGenerator:
#
#     def __init__(self):
#         self.


class RegFile:
    registerList = []
    reg_file_size = 0

    class Register:
        reg_num = 0
        reg_name = ""
        reg_bin_contents = "0000" + "0000"\
                         + "0000" + "0000"\
                         + "0000" + "0000"\
                         + "0000" + "0000"
        reg_hex_contents = ""
        reg_char_contents = ""
        reg_unsign_contents = 0
        reg_sign_contents = 0
        reg_float_contents = 0.0

        def __int__(self, register_number, register_name):
            self.reg_num = register_number
            self.reg_name = register_name

        def set_contents(self, bin_str):
            self.reg_bin_contents = bin_str

            neg_signed_flag = False



            n = 0
            for bin_dig in self.reg_bin_contents:
                if bin_dig == '1':
                    if n == 31:
                        self.reg_sign_contents += (2 ** n) * -1
                    else:
                        self.reg_sign_contents += (2 ** n)
                    self.reg_unsign_contents += 2 ** n

                if n == 7:
                    self.reg_char_contents = chr(self.reg_unsign_contents)

                n += 1

            self.reg_hex_contents = hex(self.reg_unsign_contents)

    def __init__(self, file_sz, echo):
        self.reg_file_size = file_sz

        for i in self.reg_file_size:
            self.registerList.append(-1)

    def __repr__(self):
        return "Test()"

    def __str__(self):
        return "Register File:\n"\
             + "Size:" + self.reg_file_size\
             + "\n" + self.registerList

    def add_reg(self, reg_name):
        self.registerList.append(reg_name) # TODO FINISH THIS


def test_quad_reserve(quad_reserve):
    line_spacing = 15

    print("Index".ljust(line_spacing) + "Mnem/Index".ljust(line_spacing) + "opCode/Mnem".ljust(
        line_spacing) + "opCode/Index".ljust(line_spacing))
    for i in range(0, len(quad_reserve.quad_tablelist)):
        mnem_by_index = quad_reserve.get_mnem(i)
        index = quad_reserve.get_index(mnem_by_index)
        opcode_by_index = quad_reserve.get_opcode(i)
        mnem_by_opcode = quad_reserve.get_mnem(opcode_by_index)
        opcode_by_mnem = quad_reserve.get_opcode(mnem_by_index)

        if opcode_by_mnem != opcode_by_index:
            print(f"\nERROR: Quad Index: {i}: mismatched opCodes: {opcode_by_mnem} != {opcode_by_index}\n")

        # print(f"{mnem_by_index.format(15)} {opcode_by_mnem.format(15)} {opcode_by_index.format(15)}")
        print(f"{index}".ljust(line_spacing) + "" +
              mnem_by_index.ljust(line_spacing) + "" +
              opcode_by_mnem.ljust(line_spacing) + "" +
              opcode_by_index.ljust(line_spacing))


new_reserve = QuadReserve()
print(new_reserve.get_opcode(0))
print(new_reserve.get_opcode(1))
print(new_reserve.get_opcode(22))
print(new_reserve.get_opcode(28))
print(new_reserve.get_opcode(33))
print(new_reserve.get_opcode(34))
#test_quad_reserve(new_reserve)

# print(quad_reserve.get_opCode)

