import re
import macros


Node = dict
Leaf = str

def term(env, t, heap = int( macros.HEAP_START ) ):
	tag = str( id( t ))
	for label in t:

		if label == "Number":
			value = t[ label ][ 0 ]
			instsNum = [ "set " + str( heap ) + " " + str( value )]
			return (instsNum, heap, heap + 1 )

		if label == "Variable":
			varName = t[ label ][ 0 ]
			varAddr = env[ varName ]
			instsVar = [ 'doc  value of ' + varName + ' addr = ' + str( varAddr )]
			instsVar += macros.copy( varAddr, heap )

			return ( instsVar, heap, heap + 1)

		if label == 'Plus':
 
			f1 = t[ label ][0]
			f2 = t[ label ][1]
			(instsLeft, leftResult, nextHeap) = term( env, f1, heap )
			(instsRight, rightResult, result) = term( env, f2, nextHeap )
			# Increment the heap counter so we store the
			# result of computing Or in a new location.
			heap4 = nextHeap + 1
			# Add instructions that compute the result of the
			# Or operation.

			instsPlus = macros.add( leftResult,  rightResult, result  )

			return (instsLeft + instsRight + instsPlus, result, result+1)


def formula(env, f, heap = int( macros.HEAP_START ) ):
	tag = str( id( f ))
	if type(f) == Leaf:
		if f == 'True':
			# Find a new memory address on the heap.
			heap = heap + 1
			# Generate instruction to store the integer representing True on the heap.
			inst = 'set ' + str(heap) + ' 1'
			# Return the instruction list and top of the heap.
			return ([inst], heap,  heap + 1 )

		if f == 'False':
			# Find a new memory address on the heap.
			heap = heap + 1
			# Generate instruction to store the integer representing False on the heap.
			inst = 'set ' + str(heap) + ' 0'
			# Return the instruction list and top of the heap.
			return ([inst], heap, heap + 1)

	if type(f) == Node:
		for label in f:
			children = f[label]

			if label == "Variable":
				varName = children[ 0 ]
				varAddr = env[ varName ]
				instsVar = [ 'doc  value of ' + varName + ' addr = ' + str( varAddr )]
				instsVar += macros.copy( varAddr, heap )

				return ( instsVar, heap, heap + 1)



			if label == 'Not':
				# Compile the subtree f to obtain the list of
				# instructions that computes the value represented
				# by f.
				f = children[0]
				(insts, heap, nextHeap) = formula( env, f, heap )
				# Generate more instructions to change the memory
				# location in accordance with the definition of the
				# Not operation.
				instsNot = \
					["branch setZero" + tag + " " + str(heap),\
					"set " + str(heap) + " 1",\
					"goto finish" + tag,\
					"label setZero" + tag,\
					"set " + str(heap) + " 0",\
					"label finish" + tag\
					]
				return (insts + instsNot, heap, heap+1)

			if label == 'Or':
				# Compile the two subtrees and get the instructions
				# lists as well as the addresses in which the results
				# of computing the two subtrees would be stored if someone
				# were to run those machine instructions.
				f1 = children[0]
				f2 = children[1]
				(insts1, leftResult, nextHeap) = formula( env, f1, heap )
				(insts2, rightResult, nextHeap) = formula( env, f2, nextHeap )
				# Increment the heap counter so we store the
				# result of computing Or in a new location.
				heap4 = nextHeap + 1
				# Add instructions that compute the result of the
				# Or operation.

				instsOr = macros.add( leftResult, rightResult, macros.ADD_RESULT )

				instsOr += [\
					"branch setOne" + tag + " 0",\
					"goto finish" + tag,\
					"label setOne" + tag,\
					"set " + macros.ADD_RESULT + " 1",\
					"label finish" + tag,\
					]
				instsOr += macros.copy( "0", str( heap4 ) )
				return (insts1 + insts2 + instsOr, heap4, heap4+1)

			if label == 'And':
				# adding left and right results: true == 1 and false == 0
				# false + false == 0  : and -> 0
				# false + true == 1 : and -> 0
				# true + false == 1 : and -> 0
				# true + true == 2 : and -> 1

				# so 0->0, 1->0, 2->1
				# we generate 

				# goto zero
				# goto zero
				# goto one

				# and we jump based on the result of adding the children of And

				# Compile the two subtrees and get the instructions
				# lists as well as the addresses in which the results
				# of computing the two subtrees would be stored if someone
				# were to run those machine instructions.
				f1 = children[0]
				f2 = children[1]
				(insts1, leftResult, nextHeap) = formula( env, f1, heap )
				(insts2, rightResult, nextHeap) = formula( env,f2, nextHeap )
				# Increment the heap counter so we store the
				# result of computing And in a new location.
				heap4 = nextHeap + 1
				heap5 = heap4 + 1
				# Add instructions that compute the result of the
				# Or operation.

				instsAnd = macros.add( leftResult, rightResult, heap4 )
				instsAnd += macros.relativeJump( heap4 )

				instsAnd += [\
					"goto zero" + tag,\
					"goto zero" + tag,\
					"goto one" + tag,\
					"label zero" + tag,\
					"set " + macros.ADD_RESULT + " 0",\
					"goto finish" + tag,\
					"label one" + tag,\
					"set " + macros.ADD_RESULT + " 1",\
					"label finish" + tag,\
					]
				instsAnd += macros.copy( "0", str( heap5 ) )
				return (insts1 + insts2 + instsAnd, heap5, heap5 + 1)

def expression( env, f, heap = int( macros.HEAP_START )  ):
	r = formula( env, f, heap )
	if r is None:
		r = term( env, f, heap )
	return r

def program(env, p, heap = int( macros.HEAP_START ) ):

	if p == "End":
		return ( [], 0, heap )

	Tag = str( id( p ))
	for label in p:

		if label == "Print":
			exp = p[ label ][ 0 ]
			doc = [ "doc print " + str( exp )]
			(insts, heap, nextHeap) = expression( env, exp, heap )
			insts += macros.copy( heap, macros.OUTPUT_REG )
			( contInsts, resultLoc, nextHeap ) = program( env, p[ label ][ 1 ], nextHeap )
			return ( doc + insts + contInsts , resultLoc, nextHeap )

		if label == "Assign":
			a = p[ label ]
			varExp = a[ 1 ]
			varName = a[0][ "Variable"][ 0 ]
			if env.get( varName ) == None:
				heap = heap + 1
				varAddr = str( heap )
				env[ varName ] = varAddr
			else:
				varAddr = int( env[ varName ])
			(insts, resultAddr, nextHeap) = expression( env, varExp, heap )
			code = [ "doc assign "  + varName + str( varExp )]
			code += insts
			code += macros.copy( resultAddr, varAddr )
			(cont, resultAddr, nextHeap) = program( env, a[2], heap + 1 )
			return ( code + cont , resultAddr, nextHeap )

		if label == "Call":
			call = p[ label ]
			procName = call[0][ "Variable"][ 0 ]
			callCode = macros.call( procName, Tag)
			(rest_insts, rest_resultAddr, rest_nextHeap ) = program( env, call[ 1 ], heap )
			return ( callCode + rest_insts , rest_resultAddr, rest_nextHeap+1 )

		if label == "Procedure":
			proc = p[ label ]
			procName = proc[0][ "Variable"][ 0 ]
			(proc_insts, ignore, nextHeap ) = program( env, proc[ 1 ], heap )
			procCode = macros.procedure( procName, proc_insts )
			(rest_insts, rest_resultAddr, rest_nextHeap ) = program( env, proc[ 2 ], nextHeap )
			return ( procCode + rest_insts , rest_resultAddr, nextHeap+1 )

		if label == "If":
			ifs = p[ label ]
			
			(cond_insts, cond_resultAddr, cond_nextHeap ) = expression( env, ifs[ 0 ], heap )
			(ifTrue_insts, ifTrue_resultAddr, ifTrue_nextHeap ) = program( env, ifs[ 1 ], cond_nextHeap )
			(rest_insts, rest_resultAddr, rest_nextHeap ) = program( env, ifs[ 2 ], ifTrue_nextHeap )

			insts = [ 'doc ' + 'if (' + str( ifs[ 0 ]) + ' ... ']
			insts += cond_insts
			insts += macros.copy( cond_resultAddr, macros.ADD_RESULT )
			insts += [ 'branch ' + 'ifTrue_' + Tag + ' ' + macros.ADD_RESULT ]
			insts += [ 'goto ' + 'ifFalse_' + Tag ]
			insts += [ 'label ' + 'ifTrue_' + Tag ]
			insts += ifTrue_insts
			insts += [ 'label ' + 'ifFalse_' + Tag ]
			insts += rest_insts

			return ( insts, rest_resultAddr, rest_nextHeap + 1 )










