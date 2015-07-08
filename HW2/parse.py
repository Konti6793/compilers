


import re
import json
import math
import operator




def pp( tree ):
    return  json.dumps( tree, sort_keys=True, indent=1 )

def tokenize(stringToTokenize):

    # Use a regular expression to split the string into
    # tokens or sequences of zero or more spaces.
    tokens = [t for t in re.split( r"(\s+|-?[1-9][0-9]*|[a-zA-Z]+|,|@|#|:=|;|\(|\)|&&|\|\||==|<|>|\+|\*)", stringToTokenize )]

    # Throw out the spaces and return the result.
    return [t for t in tokens if not t.isspace() and not t == ""]
            
 
Keywords = { "xor", "not", "true", "false", "log", "print", "assign", "if", "while" }

Table = 1
Func  = 2

def TabVal( tab , name ):
    return [ Table, tab, name  ]

def FuncVal( func, name ):
    return [ Func, func, name ]

def number(tokens):
    if re.match(r"^(-?[1-9][0-9]*)$", tokens[0]):
     #   
        return (int(tokens[0]), tokens[1:])

def variable(tokens):
    if re.match(r"^([a-zA-Z]+)$", tokens[0]) and not ( tokens[0] in Keywords ):
        # return ({"Variable": [ tokens[0]]}, tokens[1:])
        return ( tokens[0], tokens[1:])

def end(tokens):
    if len( tokens )  == 0:
        return ({"End": []}, [])
    if tokens[ 0 ] == "}":
        return ({"End": []}, tokens[0:])

def FORMULA():
    return TabVal( FormulaTab, "FORMULA" )

def LFORMULA():
    return TabVal( LFormulaTab, "LFORMULA" )

def TERM():
    return TabVal( TermTab, "TERM" )

def FACTOR():
    return TabVal( FactorTab, "FACTOR" )

def LFACTOR():
    return TabVal( LFactorTab, "L_FACTOR" )

def PROGRAM():
    return TabVal( ProgramTab, "PROGRAM" )

def VARIABLE():
    return FuncVal( variable, "VARIABLE" )

def NUMBER():
    return FuncVal( number, "Number" )

def END():
    return FuncVal( end, "END" )

def EXPRESSION():
    return TabVal( ExpressionTab, "EXPRESSION" )

def PROGRAM():
    return TabVal( ProgramTab, "PROGRAM" )


def FormulaTab():
    tab = [\

        ('Xor',         [  LFORMULA, 'xor', FORMULA ]), \
        ('Equals',      [  LFORMULA, '==', FORMULA ]), \
        ('Greater',     [  LFORMULA, '>', FORMULA ]), \
        ('pass',        [  LFORMULA ]), \
       ]
    return tab


def LFormulaTab():
    tab = [\
        ('Parens',      [ '(', FORMULA, ')']), \
        ('True',        [ 'true']), \
        ('False',       [ 'false']), \
        ('pass',        [ VARIABLE ]), \
        ('Not',         [ 'not', '(', FORMULA, ')']), \
        ]
    return tab


def TermTab():
    tab = [\
        ( 'Plus',       [ FACTOR, '+', TERM ]), \
        ( 'pass',       [ FACTOR ]), \

        ]
    return tab

def FactorTab():
    tab = [\
        ( 'Mult',       [ LFACTOR, '*', FACTOR ]), \
        ( 'pass',       [ LFACTOR ]),
        ]
    return tab

def LFactorTab():
    tab = [\

        ('Parens',      [ '(', FACTOR, ')']), \
        ('Log',         [ 'log', '(', FACTOR, ')']), \
        ('pass',        [ VARIABLE ]), \
        ('pass',        [ NUMBER ]), \
        ]
    return tab


def ExpressionTab():
    tab = [\
        ('pass',      [ TERM ]), \
        ('pass',      [ FORMULA ]), \
        ]
    return tab
 
def ProgramTab():
    tab = [\
        ('pass',        [ END ]), \
        ('Print',       ['print', EXPRESSION, ';', PROGRAM ]), \
        ('Assign',      ['assign', VARIABLE , ':=', EXPRESSION, ';', PROGRAM ] ), \
        ('If',          ['if', EXPRESSION, '{', PROGRAM, '}', PROGRAM ] ), \
        ('While',       ['while', EXPRESSION, '{', PROGRAM, '}', PROGRAM ] ), \
        ]
    return tab


 
def parse(tmp, spec, top = True, level = 0):

    seqs = spec[ 1 ]()
    
    # Try each choice sequence.
    for (label, seq) in seqs:

        tokens = tmp[0:]
        ss = [] # To store matched terminals.
        es = [] # To collect parse trees from recursive calls.
        
        # Walk through the sequence and either
        # match terminals to tokens or make
        # recursive calls depending on whether
        # the sequence entry is a terminal or
        # parsing function.

        for x in seq:
 
            if type(x) == type(""): # Terminal.

                if len( tokens ) > 0 and tokens[0] == x: # Does terminal match token?
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break # Terminal did not match token.

            else: # Parsing function.

                # Call parsing function recursively
                #print( pad + "calling function for label ", label, x  )
                r = None
                x = x()
                if( x[ 0 ] == Table ):
                    r = parse( tokens, x, False, level + 1 )
                else:
                    r = x[1]( tokens )

                #print( pad, "result : ", label, " result = ", r )

                if not r is None:
                    (e, tokens) = r
                    es = es + [e]




        # Check that we got either a matched token
        # or a parse tree for each sequence entry.
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                if label == "pass":
                    return r
                else:
                    return ({label:es} if len(es) > 0 else label, tokens)



 
def term( tmp ):
    return parse( tmp,  TERM() )

def formula( tmp ):
    return parse( tmp, FORMULA() )

def program( tmp ):
    return parse( tmp, PROGRAM() )

def factor( tmp ):
    return parse( tmp, FACTOR() )

def expression( tmp ):
    return parse( tmp, EXPRESSION() )

def process( str, func ):
    return func( tokenize( str ) )


def testFormula( str ):
    r = formula( tokenize(  str ) )
    print( "formula( " + str + " ) ----> " , r )
    r = expression( tokenize(  str ) )
    print( "expression( " + str + " ) ----> " , r )








