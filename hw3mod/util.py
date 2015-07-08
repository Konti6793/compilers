import re


defaultEnv = { "tasos": 'True', "alex" : 'False', "daph": {'Number': [100]}, "helen":{'Number': [1000]} }

# instructions pretty print
def ipp( s ):
	c = 0;
	for i in s:
		print( str( c ) + ":\t" + str( i ) )
		c = c + 1

# tokenize the string s, parse the tokens with function f, return the parse tree
def parse( s, f ):
	tokens = re.split(r"(\s+|assign|:=|print|\+|if|while|{|}|;|true|false|call|procedure|not|and|or|\(|\))", s)
	tokens = [t for t in tokens if not t.isspace() and not t == ""]
	(p, tokens) = f(tokens)
	return p

# compile a string given a parser function pF and an a compiler function cF
def compile( s, pF, cF ):
	pt = parse( s, pF )
	code = cF( defaultEnv, pt )
	return code

# compile and execute a string given a parser function pF and an a compiler function cF
def compileAndExec( s, pF, cF ):
    code = compile( s, pF, cF )
    #ipp( code[ 0 ])
   
    return machine.simulate( code[0] )
