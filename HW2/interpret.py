import parse

def accumVariablesInTerm( accum, term ):

    if term == "True":
        return 

    if term == "False":
        return

    if type( term ) == type( "" ):
        return accum.add( term )

    if type( term ) == type( 1 ):
        return 

    for label in term:

        if label == "Plus":
            left = term[ label ][0]
            accumVariablesInTerm( accum, left )
            right = term[ label ][1]
            accumVariablesInTerm( accum, right )
            return  

        if label == "Mult":
            left = term[ label ][0]
            accumVariablesInTerm( accum, left )
            right = term[ label ][1]
            accumVariablesInTerm( accum, right )
            return  


        if label == "Log":
            e = term[ label ][0]
            accumVariablesInTerm( accum, e )
            return  

        if label == "Parens":
            accumVariablesInTerm( accum, term[ label ][ 0 ] )
            return


def evalTerm( env, term ):

    if term == "True":
        return None

    if term == "False":
        return None

    if type( term ) == type( "" ):
        return env[ term ]

    if type( term ) == type( 1 ):
        return term

    for label in term:

        if label == "Plus":
            left = term[ label ][0]
            leftv = evalTerm( env, left )
            right = term[ label ][1]
            rightv = evalTerm( env, right )
            return leftv + rightv

        if label == "Mult":
            left = term[ label ][0]
            leftv = evalTerm( env, left )
            right = term[ label ][1]
            rightv = evalTerm( env, right )
            return leftv * rightv


        if label == "Log":
            e = term[ label ][0]
            ev = evalTerm( env, e )
            return math.log( ev )

        if label == "Parens":
            return evalTerm( env, term[ label ][0])

def evalTermStr( str ):
    ( e, tokens ) = parse.term( parse.tokenize( str ))
    print( parse.pp( e ))
    r = evalTerm( { "pi": 3.14, "a": 1 }, e )
    print( "Term : " + str + " yields : ", r )


def accumVariablesInFormula( accum, exp ):
    if exp == "True":
        return

    if exp == "False":
        return 

    if type( exp ) == type( "" ):
        return accum.add( exp )

    if type( exp ) == type( 1 ):
        return  
    for label in exp:

        if label == 'Xor':
            left = term[ label ][0]
            accumVariablesInFormula( accum, left )
            right = term[ label ][1]
            accumVariablesInFormula( accum, left )
            return  

        if label == 'Equals':
            left = term[ label ][0]
            accumVariablesInFormula( accum, left )
            right = term[ label ][1]
            accumVariablesInFormula( accum, left )
            return  

        if label == 'Greater':
            left = term[ label ][0]
            accumVariablesInFormula( accum, left )
            right = term[ label ][1]
            accumVariablesInFormula( accum, left )
            return  

        if label == 'Not':
            e = term[ label ][0]
            accumVariablesInFormula( accum, e )
            return 

        if label == "Parens":
            accumVariablesInFormula( accum, exp[ label ][ 0 ] )
            return


def evalFormula( env, exp ):

    if exp == "True":
        return True

    if exp == "False":
        return False

    if type( exp ) == type( "" ):
        return env[ exp ]

    if type( exp ) == type( 1 ):
        return  
    for label in exp:

        if label == 'Xor':
            left = term[ label ][0]
            leftv = evalFormula( env, left )
            right = term[ label ][1]
            rightv = evalFormula( env, right )
            return leftv ^ rightv

        if label == 'Equals':
            left = term[ label ][0]
            leftv = evalFormula( env, left )
            right = term[ label ][1]
            rightv = evalFormula( env, right )
            return leftv == rightv

        if label == 'Greater':
            left = term[ label ][0]
            leftv = evalFormula( env, left )
            right = term[ label ][1]
            rightv = evalFormula( env, right )
            return leftv > rightv

        if label == 'Not':
            e = term[ label ][0]
            ev = evalFormula( env, e )
            return not( ev )

        if label == "Parens":
            return evalFormula( env, exp[ label ][ 0 ])


def evalFormulaStr( str ):
    ( e, tokens ) = evalFormula( parse.tokenize( str ))
    r = evalTerm( { "pi": 3.14 }, e )
    print( "Formula : " + str + " yields : ", r )


def evalExpression( env, exp ):
    r = evalTerm( env, exp )
    if r is None:
        r = evalFormula( env, exp )
    return r

def accumVariableInExpression( accum, exp ):
    accumVariablesInTerm( accum, exp )
    accumVariablesInFormula( accum, exp )

def accumVariablesInProgram( accum, program ):

    print( "Program : ", program )
     
    for label in program:

        if label == "End":
            return

        if label == "Assign":

            p = program[ label ]
            varName = p[0]
            accumVariableInExpression( accum, p[ 1 ])
            accumVariablesInProgram( accum, p[ 2 ])
            return

        if label == "Print":
            p = program[ label ]
            accumVariableInExpression( accum, p[ 0 ])
            accumVariablesInProgram( accum, p[ 1 ])
            return

        if label == "If":
            p = program[ label ]
            accumVariableInExpression( accum, p[ 0 ])
            accumVariablesInProgram( accum, p[ 1 ])
            accumVariablesInProgram( accum, p[ 2 ])
            return
        
        if label == "While":
            p = program[ label ]
            accumVariableInExpression( accum, p[ 0 ])
            accumVariablesInProgram( accum, p[ 1 ])
            return

def liveVariablesInProgram( program ):
    accum = set()
    accumVariablesInProgram( accum, program )
    return accum

STDOUT = 0

def execProgram( env, program ):

    #print( "env = ", env )
    #print( "program = ", program )

    liveVars = liveVariablesInProgram( program )

    for label in program:

        if label == "End":
            return

        if label == "Assign":

            p = program[ label ]
            varName = p[0]
            if varName in liveVars:
                varValue = evalExpression( env, p[ 1 ])
                env[ varName ] = varValue
            else:
                print( "SKIP ", varName, p[ 1 ])
            execProgram( env, p[ 2 ])
            return

        if label == "Print":
            p = program[ label ]
            val = evalExpression( env, p[ 0 ])
            env[ STDOUT ] += str( val ) + "\n"
            execProgram( env, p[ 1 ])
            return

        if label == "If":
            p = program[ label ]
            cond = evalExpression( env, p[ 0 ])
            if cond:
                execProgram( env, p[ 1 ])
            else:
                execProgram( env, p[ 2 ])
            return
        
        if label == "While":
            p = program[ label ]
            cond = evalExpression( env, p[ 0 ])
            while( cond ):
                execProgram( env, p[ 1 ])
                cond = evalExpression( env, p[ 0 ])
            return



def interpret( str ):
    r = parse.program( parse.tokenize( str ))
    if r is None:
        return None
    (  e, tokens ) = r
    if len( tokens ) > 0:
        return None
    accum = set()
    accumVariablesInProgram( accum, e )
    print( "accum = ", accum )
    env = { STDOUT: ""}
    r = execProgram( env, e )
    return env[ STDOUT ]


def testProgram( str ):
    r = parse.program( parse.tokenize(  str ) )
    print( "program( " + str + " ) ----> " , r )


def testTerm( str ):
    r = parse.term( parse.tokenize(  str ) )
    print( "term( " + str + " ) ----> " , r )
    r = parse.expression( parse.tokenize(  str ) )
    print( "expression( " + str + " ) ----> " , r )


'''

testFormula( " true " )
testFormula( " false " )
testFormula( " abc  " )
testFormula( " not ( true )  " )
testFormula( " not ( false )  " )
testFormula( " not ( abc )  " )
testFormula( " ( abc )  " )
testFormula( " ( not( abc ) )  " )
testFormula( " true xor true  " )
testFormula( " a xor v  " )
testFormula( "  true xor false   " )
testFormula( " ( true xor true )  " )
testFormula( " not( true xor true )  " )



testTerm( " 1  ");
testTerm( " a ");
testTerm( " a + 1 ");
testTerm( " a * 1 ");
testTerm( " log( 1 ) ");
testTerm( " ( 1 ) ");



def testProgram( str ):
    r = program( tokenize(  str ) )
    print( "program( " + str + " ) ----> " , r )


testProgram( "" );
testProgram( "print a;" );
testProgram( "if( true ) { print yes; } print no; " );

'''

#testTerm( "  true ")


#testProgram( "assign a := 1 ; print a; if( true ) { print 100; }" );
o = interpret( "assign a := 1 ; assign b := 1; print a; if( true ) { print 100; } " );
print( o )


# sevalTermStr( " a + 20 ");







