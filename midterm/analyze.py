#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# analyze.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #4. ***************
#  ****************************************************************
#

exec(open("parse.py").read())

Node = dict
Leaf = str

def typeExpression(env, e):
    if type(e) == Leaf:
        if e == 'True' or e == 'False':
            return 'Boolean'
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                return 'Number'

            if label == 'Variable':
                return env[ e[label][ 0 ]]

            elif label == 'Array':
                [x, e] = children
                x = x['Variable'][0]
                if x in env and env[x] == 'Array' and typeExpression(env, e) == 'Number':
                    return 'Number'

            elif label == 'Plus':
                if typeExpression( env, e[label][ 0 ] ) == 'Number' and typeExpression( env, e[label][ 1 ] ) == 'Number':
                    return 'Number'
                else:
                    return None


def typeProgram(env, s):
    if type(s) == Leaf:
        if s == 'End':
            return 'Void'
    elif type(s) == Node:
        for label in s:
            if label == 'Print':
                [e, p] = s[label]
                pType = typeProgram( env, p)
                eType = typeExpression( env, e )
                if pType == 'Void' and ( eType == 'Boolean' or eType == 'Number'):
                    return 'Void'
                else:
                    return None
                

            if label == 'Assign':
                [x, e0, e1, e2, p] = s[label]
                x = x['Variable'][0]
                if typeExpression(env, e0) == 'Number' and\
                   typeExpression(env, e1) == 'Number' and\
                   typeExpression(env, e2) == 'Number':
                     env[x] = 'Array'
                     if typeProgram(env, p) == 'Void':
                           return 'Void'

            if label == 'For':
                [x, p1, p2] = s[label]
                x = x['Variable'][0]
                prevType = None
                if x in env:
                    prevType = env[ x ]
                env[ x ] = 'Number'
                pType1 = typeProgram( env, p1)
                if not prevType is None:
                    env[ x ] = prevType
                else:
                    del env[ x ]
                pType2 = typeProgram( env, p2)
                if pType1 == 'Void' and pType2 == 'Void': 
                    return 'Void'
                


#eof
