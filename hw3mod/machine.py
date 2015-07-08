#####################################################################
#
# CAS CS 320, Fall 2014
# Assignment 3 (skeleton code)
# machine.py
#

def simulate(s, report = "" ):
    instructions = s if type(s) == list else s.split("\n")
    instructions = [l.strip().split(" ") for l in instructions]
    mem = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: -1, 6: 0, 7: 0 }
    control = 0
    outputs = []
    index = 0
    for ins in instructions:
        #print( str(index) + '   '  + str( ins ))
        index = index + 1
    while control < len(instructions):
        # Update the memory address for control.
        mem[6] = control 
        # Retrieve the current instruction.
        inst = instructions[control]

        #print( control, inst, str( mem ) )
        #input( "cont:")

        # Handle the instruction.
        if inst[0] == 'assert':
            assert mem[int( inst[1] )] == int( inst[2] )
        if inst[0] == 'doc':
            pass
        if inst[0] == 'label':
            pass
        if inst[0] == 'goto':
            control = instructions.index(['label', inst[1]])
            continue
        if inst[0] == 'branch' and mem[int(inst[2])]:
            control = instructions.index(['label', inst[1]])
            continue
        if inst[0] == 'jump':
            control = mem[int(inst[1])]
            continue
        if inst[0] == 'set':
            if mem.get( int(inst[1]) ) is None:
                mem[ int(inst[1])] = 0
            mem[int(inst[1])] = int(inst[2])
        if inst[0] == 'copy':
            if mem.get( mem[4] ) is None:
                mem[ mem[4]] = 0
            if mem.get( mem[3] ) is None:
                mem[ mem[3]] = 0
            mem[mem[4]] = mem[mem[3]]
            if mem[4] == 6:
                control = mem[6] 
            #print( str( mem[3] ) + "(" + str( mem[ mem[ 3 ]]) + ") -> " + str( mem[ 4 ]) )
        if inst[0] == 'add':
            mem[0] = mem[1] + mem[2]
            #print( str( mem[ 1] ) + "+" + str( mem[ 2 ]) + "=" + str( mem[ 0 ]))

        # Push the output address's content to the output.
        if mem[5] > -1:
            outputs.append(mem[5])
            mem[5] = -1

        # Move control to the next instruction.
        #print( control, inst, str( mem ) )

        control = control + 1



    if report == "":
      pass # print("memory: "+str(mem))
    else:
      pass #print("result mem["+ report + "]=" + str( mem[ int( report )]) )

    return outputs

# Examples of useful helper functions from lecture.    



 
# eof
