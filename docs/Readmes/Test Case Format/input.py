import builtins


# this entire file is run once during okpy's setup
pos = 0 # line number to read currently
test = 0 # test number we're on currently
def input(user_in=None):

    # print optional argument
    if user_in:
        print(user_in, end="")

    global filenames, pos, test
    
    # no more files to read
    if test >= len(filenames):
        return ""
    
    with open(filenames[test], 'r') as f:
        f.seek(pos)
        input_line = f.readline()
        if input_line == '': # end of input file, next test
            test += 1
            pos = 0
            f.close()
            return input()
        elif input_line[-1] == '\n':
            input_line = input_line[:-1]
        pos = f.tell()

        # print input and return it
        print(input_line)
        return input_line

builtins.input = input