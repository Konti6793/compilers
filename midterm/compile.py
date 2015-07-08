#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# compile.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #3. ***************
#  ****************************************************************
#



from random import randint
exec(open('parse.py').read())
exec(open('interpret.py').read())
exec(open('optimize.py').read())
exec(open('machine.py').read())







ADD_RESULT      = "0"
ADD_LEFT        = "1"
ADD_RIGHT       = "2"
COPY_FROM       = "3"
COPY_TO         = "4"
OUTPUT_REG      = "5"
PROGRAM_COUNTER = "6"
STACK_TOP       = "7"
PC2             = "8"
HEAP_START      = "10"


def copy( aFrom, aTo  ):
    if str( aFrom ) == str( aTo ):
        return [ 'doc skiping_copy_same_' + str( aFrom ) ]
    return [\
        'set ' + COPY_FROM + ' ' + str( aFrom ), \
        'set ' + COPY_TO + ' ' + str( aTo ), \
        'copy'
    ]

def arrayRead( aFrom, index,  aTo  ):

    return [\
        'doc arrayRead_aFrom:('+ str(aFrom ) + '+index:' + str(index) + ')_aTo' + str( aTo), \
        'set ' + COPY_FROM + ' ' + str(index), \
        'set ' + COPY_TO + ' ' + ADD_RIGHT, \
        'copy ',\
        'set ' + ADD_LEFT + ' ' + str( aFrom ), \
        'add ', \
        'set ' + COPY_FROM + ' ' + ADD_RESULT, \
        'set ' + COPY_TO + ' ' + COPY_FROM, \
        'copy', \
        'set ' + COPY_TO + ' ' + str( aTo ), \
        'copy',\
        'doc DONE arrayRead_aFrom:('+ str(aFrom ) + '+index:' + str(index) + ')_aTo' + str( aTo)
    ]

def arrayWrite( aFrom,  aTo, index  ):

    return [\
        'doc arrayWrite_aFrom:('+ str(aFrom ) + '+index:' + str(index) + ')_aTo' + str( aTo), \
        'set ' + ADD_LEFT + ' ' + str( aTo ), \
        'set ' + ADD_RIGHT + ' ' + str( index ), \
        'add ', \
        'set ' + COPY_FROM + ' ' + ADD_RESULT, \
        'set ' + COPY_TO + ' ' + COPY_TO, \
        'copy', \
        'set ' + COPY_FROM + ' ' + str( aFrom ), \
        'copy', \
        'doc DONE arrayWrite_aFrom:('+ str(aFrom ) + '+index:' + str(index) + ')_aTo' + str( aTo)
    ]

def add( aLeft, aRight, aResult ):
    r =  [ 'doc ' + 'add_' + str( aLeft ) + '_' + str( aRight ) + '_to_' + str( aResult )]
    r += copy( aLeft, ADD_LEFT )
    r += copy( aRight, ADD_RIGHT )
    r += [ 'add']
    r += copy( ADD_RESULT, aResult )
    return r


Leaf = str
Node = dict

def freshStr():
    return str(randint(0,10000000))

def compileExpression(env, e, heap):
    if e == "True":
        heap = heap + 1
        return (['set ' + str(heap) + ' ' + str(1)], heap, heap)

    if e == "False":
        heap = heap + 1
        return (['set ' + str(heap) + ' ' + str(0)], heap, heap)

    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                n = children[0]
                heap = heap + 1
                return (['set ' + str(heap) + ' ' + str(n)], heap, heap)

            if label == 'Plus':
                leftNode = children[ 0 ]
                rightNode = children[ 1 ]
                ( leftInstrs, leftResult, nextHeap ) = compileExpression( env, leftNode, heap )
                ( rightInstrs,  rightResult, nextHeap ) = compileExpression( env, rightNode, nextHeap )
                result = nextHeap + 1

                instsPlus = add( leftResult,  rightResult, result  )
                return (leftInstrs + rightInstrs + instsPlus, result, result+1)

            if label == "Array":
                exp = e[ label ]
                varName = exp[ 0 ][ "Variable"][ 0 ]
                indexNode = exp[ 1 ]
                varAddress = env[ varName ]
                ( indexInstrs, indexResult, nextHeap ) = compileExpression( env, indexNode, heap )
                result = nextHeap + 1

                arrayInstrs = arrayRead( varAddress, indexResult, result )

                return ( indexInstrs + arrayInstrs, result, result + 1 )



def compileProgram(env, s, heap = 10): # Set initial heap default address.
    if type(s) == Leaf:
        if s == 'End':
            return (env, [], heap)

    if type(s) == Node:
        for label in s:
            children = s[label]
            if label == 'Print':
                [e, p] = children
                (instsE, addr, heap) = compileExpression(env, e, heap)
                (env, instsP, heap) = compileProgram(env, p, heap)
                return (env, instsE + copy(addr, 5) + instsP, heap)

            if label == 'Assign':
                ( v0Instrs, v0Result, nextHeap ) = compileExpression(env, children[ 1 ], heap)
                ( v1Instrs, v1Result, nextHeap ) = compileExpression(env, children[ 2 ], nextHeap)
                ( v2Instrs, v2Result, nextHeap ) = compileExpression(env, children[ 3 ], nextHeap)
                result = nextHeap + 1
                varName = children[0]["Variable"][ 0 ]
                env[ varName ] = result
                assignInstrs  = arrayWrite( v0Result, result, 0 ) # should be optimized to copy
                assignInstrs += arrayWrite( v1Result, result, 1 )
                assignInstrs += arrayWrite( v2Result, result, 2 )
                heap = heap + 6
                (env, instsP, heap) = compileProgram(env, children[ 4 ], heap)
                return (env, v0Instrs + v1Instrs + v2Instrs +  assignInstrs + instsP, heap)



def compile(s):
    p = tokenizeAndParse(s)

    # Add call to type checking algorithm for Problem #4.
    # Add calls to optimization algorithms for Problem #3.

    p = foldConstants( p )
    p = unrollLoops( p )
    (env, insts, heap) = compileProgram({}, p)
    return insts

def compileAndSimulate(s):
    return simulate(compile(s))

#eof
