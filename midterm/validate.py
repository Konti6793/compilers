#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# validate.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #5. ***************
#  ****************************************************************
#

exec(open('interpret.py').read())
exec(open('compile.py').read())

 

def expressions(n):

    if n <= 0:
        []
    elif n == 1:
        return [   { 'Number': [ 2 ]} ] #'Variable': [ 'a' ]},

    else:

        exps = expressions( n - 1 )
        expsN  = []

        expsN += [ { 'Array': [ { 'Variable': [ 'a' ]}, e  ] } for e in exps ]
        return exps + expsN

 

def programs(n):

    if n <= 0:

        []

    elif n == 1:

        return ['End']

    else:

        ps = programs(n-1)
        es = expressions(n-1)
        psN = []
        psN += [{'Assign':[{'Variable':['a']}, e, e, e, p]} for p in ps for e in es]
        psN += [{'Print':[ e, p]} for p in ps for e in es]



        pass # Add more nodes to psN for Problem #5.

        return  psN + ps

 

# We always add a default assignment to the program in case
# there are variables in the parse tree returned from programs().

 

def defaultAssigns(p):
    return \
      {'Assign':[\
        {'Variable':['a']}, {'Number':[1]}, {'Number':[1]}, {'Number':[1]}, p\
      ]}

 

def interpretTree( parseTree  ):
    env = {OUTPUT:[]}
    execute( env, parseTree )
    return env[ OUTPUT ]
 

# Compute the formula that defines correct behavior for the
# compiler for all program parse trees of depth at most 4.
# Any outputs indicate that the behavior of the compiled
# program does not match the behavior of the interpreted
# program.

 

 

for p in [defaultAssigns(p) for p in programs(4)]:   
    try:
        print(p)
        if simulate( compileProgram({}, p)[ 1 ] ) != interpretTree( p ):
            print('\nIncorrect behavior on: ' + str(p))
    except:
        print('\nError on: ' + str(p))

#eof
