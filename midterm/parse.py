#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# parse.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #1. ***************
#  ****************************************************************
#

import re

def parse(seqs, tmp, top = True):
    for (label, seq) in seqs:
        tokens = tmp[0:]
        (ss, es) = ([], [])
        for x in seq:
            if type(x) == type(""):
                if tokens[0] == x:
                    tokens = tokens[1:]
                    ss = ss + [x]
                else: break
            else:
                r = x(tokens, False)
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]
        if len(ss) + len(es) == len(seq) and (not top or len(tokens) == 0):
            return ({label:es} if len(es) > 0 else label, tokens)



def number(tokens, top = True):
    if re.compile(r"(-(0|[1-9][0-9]*)|(0|[1-9][0-9]*))").match(tokens[0]):
        return ({"Number": [int(tokens[0])]}, tokens[1:])

def variable(tokens, top = True):
    if re.compile(r"[a-z][A-Za-z0-9]*").match(tokens[0]) and tokens[0] not in ['true', 'false']:
        return ({"Variable": [tokens[0]]}, tokens[1:])

def expression( tmp, top = True ):
    r = leftExpression( tmp, False )
    if not r is None:
        ( lexp, tokens ) = r
        if len( tokens ) > 0 and tokens[ 0 ] == '+':
            r = expression( tokens[ 1: ], False )
            if not r is None:
                ( rexp, tokens ) = r
                return ( { 'Plus': [ lexp, rexp ] }, tokens )
        else:
            return r

def leftExpression( tmp, top = True ):
    tokens = tmp[0:]
    # print( 1, tokens )
    if tokens[0] == '@':
        r = variable(tokens[1:], False)
        # print( 2 )
        if not r is None:
            (var, tokens) = r
            if tokens[0] == '[':
                r = expression( tokens[ 1: ], False )
                if not r is None:
                    ( exp, tokens ) = r
                    if tokens[ 0 ] == ']':
                        return ( { 'Array': [ var, exp ]}, tokens[ 1:])


    tokens = tmp[0:]
    if tokens[0] == 'true':
        return ( 'True', tokens[1:])

    tokens = tmp[0:]
    if tokens[0] == 'false':
        return ( 'False', tokens[1:])

    tokens = tmp[0:]
    r = variable(tokens, False)
    if not r is None:
        return r

    tokens = tmp[0:]
    r = number(tokens, False)
    if not r is None:
        return r
    

def program(tmp, top = True):
    if len(tmp) == 0:
        return ('End', [])
    r = parse([\
        ('Print',   ['print', expression, ';', program]),\
        ('For',     ['for', expression, '{', program, '}', program ]),\
        ('Assign',  ['assign', variable, ':=', '[', expression, ',', expression, ',', expression, ']', ';', program]),\
        ('End',     [])
        ], tmp, top)
    if not r is None:
        return r

def tokenize( s ):
    tokens = re.split(r"(\s+|assign|:=|,|print|\+|for|{|}|;|@|true|false|[a-z][A-Za-z0-9]*|\[|\])", s)
    tokens = [t for t in tokens if not t.isspace() and not t == ""]
    return tokens

def tokenizeAndParse(s):
    tokens = tokenize( s )
    (p, tokens) = program(tokens)
    return p
#eof



