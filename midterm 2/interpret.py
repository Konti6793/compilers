#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# interpret.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #2. ***************
#  ****************************************************************
#

exec(open("parse.py").read())

Node = dict
Leaf = str

OUTPUT = 1
ENV = 2

def evaluate(env, e):

    if e == 'True':
        return True

    if e == 'False':
        return False

    for label in e:
        if label == "Number":
            return e[label][ 0 ]

        if label == "Variable":
            return  env[ e[label][ 0 ]]

        if label == "Plus":
            return evaluate( env, e[label][ 0 ] ) + evaluate( env, e[label][ 1 ] )

        if label == "Array":
            exp = e[ label ]
            varName = exp[ 0 ][ "Variable"][ 0 ]
            varIndex = evaluate( env, exp[ 1 ])
            return env[ varName ][ varIndex ]


def execute(env, s):

    for label in s:


        if label == 'End':
            return

        if label == 'Assign':
            node = s[ label ]
            varName = node[0]["Variable"][ 0 ]
            v0 = evaluate( env, node[1])
            v1 = evaluate( env, node[2])
            v2 = evaluate( env, node[3])
            env[ varName ] = [ v0, v1, v2 ]
            execute( env, node[ 4 ])
            return

        if label == 'Print':
            node = s[ label ]
            val = evaluate( env, node[ 0 ])
            env[ OUTPUT ].append( val )
            execute( env, node[ 1 ])
            return

        if label == 'For':
            node = s[ label ]
            progNode = node[ 1 ]
            restNode = node[ 2 ]
            varNode = node[ 0 ]
            varName = varNode[ "Variable"][ 0 ]
            varValue = env[ varName ]
            for ithVal in [0, 1, 2]:
                env[ varName ] = ithVal
                execute( env, progNode )
            env[ varName ] = varValue
            execute( env, restNode )

def interpret(s):
    env = {OUTPUT:[]}
    parseTree = tokenizeAndParse( s )
    execute( env, parseTree )
    return env[ OUTPUT ]

#eof
