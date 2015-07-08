
import parse
import util
import compiler
import machine
import macros

def toStr( a ):
	r = ""
	for x in a:
		r = r + x + '\n'
	return r

def test( str ):
	#print( str )
	return machine.simulate( str )


def testTerm( s, expectedValue ):
	( code, result, nextHeap ) = util.compile( s, parse.term, compiler.term )
	code += [ 'assert ' + str( result ) + ' ' + str( expectedValue )]
	test( code )

def testformula( s, expectedValue ):
	( code, result, nextHeap ) = util.compile( s, parse.formula, compiler.formula )
	code += [ 'assert ' + str( result ) + ' ' + str( expectedValue )]
	test( code )

def testProgram( s, outputValues ):
	( code, result, nextHeap ) = util.compile( s, parse.program, compiler.program )
	o = test( code )
	assert o == outputValues

def termTests():
	testTerm( '1 + 2', 3)
	testTerm( '1 + 2 + 3 + 4', 10)


 

termTests()

def termFormulas():
	testformula( 'not ( true )',  0)
	testformula( 'true', 1 )
	testformula( 'false', 0 )
	testformula( 'not( false )', 1 )
	testformula( 'false and false', 0 )
	testformula( 'false and true', 0 )
	testformula( 'true and false', 0 )
	testformula( 'true and true', 1 )
	testformula( 'false or false', 0 )
	testformula( 'false or true', 1 )
	testformula( 'true or false', 1 )
	testformula( 'true or true', 1 )
	testformula( 'not( true or false )', 0 )
	testformula( 'not( true or true )', 0 )
	testformula( 'not( false or false )', 1 )

termFormulas()

def testPrograms():
	p = '''
	print 1;
	print 1+2;
	print 3;
	print not( false or false );
	'''
	testProgram( p, [ 1, 3, 3, 1 ])

	p = '''
	a := 100;
	print a;
	a := 200;
	print a;
	b := not( true or false );
	print b;
	'''
	testProgram( p, [ 100, 200, 0 ])


	p = '''
	if true 
	{
		print 10;
	}
	print 20;
	'''
	testProgram( p, [ 10, 20])

	p = '''
	if false 
	{
		print 10;
	}
	print 20;
	'''
	testProgram( p, [ 20 ])
	

	p = '''
	a := 10;
	if true 
	{
		print a;
	}
	print 20;
	'''
	testProgram( p, [ 10, 20 ])
	
	p = '''
	procedure foo
	{
		print 10;
	}
	print 20;
	'''
	testProgram( p, [ 20 ])


	p = '''
	procedure foo
	{
		print 10;
	}
	call foo;
	'''
	testProgram( p, [ 10 ])

testPrograms()

def macroTests():

	testRelJump = '''
	set 200 0
	set 100 3
	''' + toStr( macros.relativeJump( 100 ) ) + '''
	set 200 1
	goto finish
	set 200 2
	goto finish
	set 200 3
	goto finish
	label finish
	assert 200 2
	'''
	test( testRelJump )


	testCopy = '''
	set 100 1
	''' + toStr( macros.copy( 100, 200 ) ) + '''
	assert 200 1
	'''
	test( testCopy )

	testAdd = '''
	set 100 1000
	set 101 2000
	''' + toStr( macros.add( 100, 101, 102 ) ) + '''
	assert 102 3000
	'''

	test( testAdd )

	testIncr = '''
	set 100 2000
	set 200 2000
	''' + toStr( macros.incrementBy( 100, 1 ) ) + '''
	''' + toStr( macros.incrementBy( 200, -1 ) ) + '''
	assert 100 2001
	assert 200 1999
	'''
	test( testIncr )

	testDeref = '''
	set 100 200
	set 200 1000
	set 300 0 
	''' + toStr( macros.deref( 100, 300 ) ) + '''
	assert 300 1000
	'''
	test( testDeref )

	testIndirectSet = '''
	set 100 101
	set 101 1000
	set 200 201
	set 201 0
	''' + toStr( macros.indirectSet( 100, 200 ) ) + '''
	assert 201 1000
	'''
	test( testIndirectSet )

	testIndirectSetLiteral = '''
	set 100 200
	set 200 0
	''' + toStr( macros.indirectSetLiteral( 100, 123 ) ) + '''
	assert 200 123
	'''
	test( testIndirectSet )

	testIndirectIncrement = '''
	set 100 101
	set 101 1000
	''' + toStr( macros.indirectIncrement( 100, 50 ) ) + '''
	assert 101 1050
	'''
	test( testIndirectIncrement )


	testIndirectIncrement = '''
	set 100 101
	set 101 1000
	''' + toStr( macros.indirectIncrement( 100, 50 ) ) + '''
	assert 101 1050
	'''
	test( testIndirectIncrement )

	testStack = '''
	set 100 2222
	set 200 0
	''' + toStr( macros.push( 100 ) ) + '''
	assert -1 2222
	''' + toStr( macros.pop( 200 ) ) + '''
	doc assert 200 2222
	''' + toStr( macros.pushLiteral( 10 ) ) + '''
	assert -1 10
	'''+ toStr( macros.pushLiteral( 4 ) ) + '''
	assert -2 4
	'''+ toStr( macros.pop( 100 ) ) + '''
	assert 100 4
	'''+ toStr( macros.pop( 200 ) ) + '''
	assert 200 10
	'''
	test( testStack )

	pcall = '''
	''' + toStr( macros.procedure( "foo", [ 'set 300 1 ', 'set 301 2'])) + '''
	''' + toStr( macros.call( "foo", "blah" ) ) + '''
	assert 300 1
	assert 301 2
	'''
	test( pcall )

macroTests()


testIndirectIncrement = '''
set 100 101
set 101 1000
''' + toStr( macros.indirectIncrement( 100, 50 ) ) + '''
assert 101 1050
'''
test( testIndirectIncrement )

