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

import macros

from random import randint
exec(open('parse.py').read())
exec(open('interpret.py').read())
exec(open('optimize.py').read())
exec(open('machine.py').read())

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

                instsPlus = macros.add( leftResult,  rightResult, result  )
                return (leftInstrs + rightInstrs + instsPlus, result, result+1)

            if label == "Array":
                exp = e[ label ]
                varName = exp[ 0 ][ "Variable"][ 0 ]
                indexNode = exp[ 1 ]
                varAddress = env[ varName ]
                ( indexInstrs, indexResult, nextHeap ) = compileExpression( env, indexNode, heap )
                result = nextHeap + 1

                arrayInstrs = macros.arrayRead( varAddress, indexResult, result )

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
                assignInstrs  = macros.arrayWrite( v0Result, result, 0 ) # should be optimized to copy
                assignInstrs += macros.arrayWrite( v1Result, result, 1 )
                assignInstrs += macros.arrayWrite( v2Result, result, 2 )
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
