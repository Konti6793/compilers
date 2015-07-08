exec(open("parse.py").read())
exec(open("interpret.py").read())
exec(open("optimize.py").read())
exec(open("compile.py").read())
exec(open("analyze.py").read())


def testf( func, s ):
    tokens = tokenize( s )
    r = func( tokens )
    assert r[ 1 ] == []
    #print( 'assert testf( ' + str( func.__name__ ) + ', "' + s + '" ) == ' + str( r[0]) )
    return r[ 0 ]

testf( expression, 'true')
testf( expression, 'false')
testf( expression, '123')
testf( expression, '-123')
testf( expression, 'a')
testf( expression, '@a[2]+@b[3]+3')
testf( expression, '1+2')

 
testf( program, 'assign a:=[ 1,2,3]; print a;')
testf( program, 'for a { print a; print 20; } print 10;')


assert testf( expression, "true" ) == 'True'
assert testf( expression, "false" ) == 'False'
assert testf( expression, "123" ) == {'Number': [123]}
assert testf( expression, "-123" ) == {'Number': [-123]}
assert testf( expression, "a" ) == {'Variable': ['a']}
assert testf( expression, "@a[2]+@b[3]+3" ) == {'Plus': [{'Array': [{'Variable': ['a']}, {'Number': [2]}]}, {'Plus': [{'Array': [{'Variable': ['b']}, {'Number': [3]}]}, {'Number': [3]}]}]}
assert testf( expression, "1+2" ) == {'Plus': [{'Number': [1]}, {'Number': [2]}]}
assert testf( program, "assign a:=[ 1,2,3]; print a;" ) == {'Assign': [{'Variable': ['a']}, {'Number': [1]}, {'Number': [2]}, {'Number': [3]}, {'Print': [{'Variable': ['a']}, 'End']}]}
assert testf( program, "for a { print a; } print 10;" ) == {'For': [{'Variable': ['a']}, {'Print': [{'Variable': ['a']}, 'End']}, {'Print': [{'Number': [10]}, 'End']}]}
assert testf( program, "for a { print a; print 20; } print 10;" ) == {'For': [{'Variable': ['a']}, {'Print': [{'Variable': ['a']}, {'Print': [{'Number': [20]}, 'End']}]}, {'Print': [{'Number': [10]}, 'End']}]}


prog = '''
assign a := [10, 20, 30 ];
for a 
{
    print a;
    print 200;
}
print @a[0] + @a[1] + @a[2];
'''

assert interpret( prog ) == [0, 200, 1, 200, 2, 200, 60]

prog2 = '''

assign a := [10, 20, 30 ];
for a {}
print @a[0] + @a[1] + @a[3];

'''

print(compileAndSimulate( prog ))
print(typeProgram( {}, tokenizeAndParse( prog2 ) ))

