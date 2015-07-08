





ADD_RESULT 		= "0"
ADD_LEFT 		= "1"
ADD_RIGHT 		= "2"
COPY_FROM 		= "3"
COPY_TO 		= "4"
OUTPUT_REG 		= "5"
PROGRAM_COUNTER = "6"
STACK_TOP 		= "7"
PC2 			= "8"
HEAP_START 		= "10"


def copy( aFrom, aTo  ):
	if str( aFrom ) == str( aTo ):
		return [ 'doc skiping_copy_same_' + str( aFrom ) ]
	return [\
		'set ' + COPY_FROM + ' ' + str( aFrom ), \
		'set ' + COPY_TO + ' ' + str( aTo ), \
		'copy'
	]

def arrayRead( aFrom, index,  aTo  ):

	return [\
		'doc arrayRead_aFrom:('+ str(aFrom ) + '+index:' + str(index) + ')_aTo' + str( aTo), \
		'set ' + COPY_FROM + ' ' + str(index), \
		'set ' + COPY_TO + ' ' + ADD_RIGHT, \
		'copy ',\
		'set ' + ADD_LEFT + ' ' + str( aFrom ), \
		'add ', \
		'set ' + COPY_FROM + ' ' + ADD_RESULT, \
		'set ' + COPY_TO + ' ' + COPY_FROM, \
		'copy', \
		'set ' + COPY_TO + ' ' + str( aTo ), \
		'copy',\
		'doc DONE arrayRead_aFrom:('+ str(aFrom ) + '+index:' + str(index) + ')_aTo' + str( aTo)
	]

def arrayWrite( aFrom,  aTo, index  ):

	return [\
		'doc arrayWrite_aFrom:('+ str(aFrom ) + '+index:' + str(index) + ')_aTo' + str( aTo), \
		'set ' + ADD_LEFT + ' ' + str( aTo ), \
		'set ' + ADD_RIGHT + ' ' + str( index ), \
		'add ', \
		'set ' + COPY_FROM + ' ' + ADD_RESULT, \
		'set ' + COPY_TO + ' ' + COPY_TO, \
		'copy', \
		'set ' + COPY_FROM + ' ' + str( aFrom ), \
		'copy', \
		'doc DONE arrayWrite_aFrom:('+ str(aFrom ) + '+index:' + str(index) + ')_aTo' + str( aTo)
	]

def clear( reg ):
	return [ 'set ' + reg + ' 0']

def clearRegisters() :
	r =  clear( ADD_RESULT )
	r += clear( ADD_LEFT )
	r += clear( ADD_RIGHT )
	r += clear( COPY_TO)
	r += clear( COPY_FROM )
	return r

def convertLogical( aFrom, aTo, Tag ): # 0->0 (non zero)->1
	r =  [ 'doc convertLogical_form_' + str( aFrom ) + '_to_' + str( aTo )]
	r += [ 'branch ' + 'setOne_' + str( Tag ) + ' ' + str( aFrom )]
	r += [ 'set ' + str( aTo ) + ' 0' ]
	r += [ 'goto ' + 'continue_' + str( Tag ) ]
	r += [ 'label setOne_' + str( Tag )]
	r += [ 'set ' + str( aTo ) + ' 1' ]
	r += [ 'label continue_' + str( Tag )]
	return r

def add( aLeft, aRight, aResult ):
	r =  [ 'doc ' + 'add_' + str( aLeft ) + '_' + str( aRight ) + '_to_' + str( aResult )]
	r += copy( aLeft, ADD_LEFT )
	r += copy( aRight, ADD_RIGHT )
	r += [ 'add']
	r += copy( ADD_RESULT, aResult )
	return r

def logicalAdd( aLeft, aRight, aResult, tag ):
	r =  [ 'doc ' + 'logicalAdd_' + str( aLeft ) + '_' + str( aRight ) + '_to_' + str( aResult )]
	r += convertLogical( aLeft, ADD_LEFT, str(tag) + "1" )
	r += convertLogical( aRight, ADD_RIGHT, str(tag) + "2"  )
	r += [ 'add']
	r += copy( ADD_RESULT, aResult )
	return r

def incrementBy( aLoc, lVal ):
	r =  [ 'doc ' + 'incrementBy_' + str( aLoc ) + '_by_' + str( lVal )]
	r += copy( aLoc, ADD_LEFT )
	r += [ 'set ' + ADD_RIGHT + ' ' + str( lVal )]
	r += [ 'add' ]
	r += copy( ADD_RESULT, aLoc )
	r +=  clearRegisters()
	return r
 
def increment( aLoc ):
	return incrementBy( aloc, 1 )

def decrement( aLoc ):
	return incrementBy( aloc, -1 )

# aTo = *aFrom
def deref( aFrom, aTo ):
	r =  [ 'doc deref_' + str( aFrom ) + '_' + str( aTo ) ]
	r += [ 'set ' + COPY_FROM + ' ' + str( aFrom )]
	r += [ 'set ' + COPY_TO + ' ' + COPY_FROM ]
	r += [ 'copy ']
	r += [ 'set ' + COPY_TO + ' ' + str( aTo )]
	r += [ 'copy']
	return r

# *to = v
def indirectSetLiteral( aTo, lVal ):
	r =  [ 'doc indirectSetLiteral_' + str( aTo ) + '_' + str( lVal)]
	r += [ 'set ' + COPY_FROM + ' ' + str( aTo )]
	r += [ 'set ' + COPY_TO + ' ' + COPY_TO ]
	r += [ 'copy ']
	r += [ 'set ' + ADD_RESULT + ' ' + str( lVal )]
	r += [ 'set ' + COPY_FROM + ' ' + ADD_RESULT ]
	r += [ 'copy ']
	return r;

# *to = *from
def indirectSet( aFrom, aTo ):
	r =  [ 'doc indirectSet_' + str( aFrom ) + '_' + str( aTo )]
	r += deref( aFrom, ADD_RESULT )
	r += [ 'set ' + COPY_FROM + ' ' + str( aTo )]
	r += [ 'set ' + COPY_TO + ' ' + COPY_TO ]
	r += [ 'copy ']
	r += [ 'set ' + COPY_FROM + ' ' + ADD_RESULT ]
	r += [ 'copy ']
	return r;


# *loc = *loc + v
def indirectIncrement( aLoc, lVal ):
	r =  [ 'doc indirectIncrement_' + str( aLoc ) + '_' + str( lVal ) ]
	r += deref( aLoc, ADD_LEFT )
	r += [ 'set ' + ADD_RIGHT + ' ' + str( lVal ) ]
	r += [ 'add' ]
	r += [ 'set ' + COPY_FROM + ' ' + str( aLoc )]
	r += [ 'set ' + COPY_TO + ' ' + COPY_TO ]
	r += [ 'copy ']	
	r += [ 'set ' + COPY_FROM + ' ' + ADD_RESULT ]
	r += [ 'copy ']	
	return r

def pushLiteral( lVal ):
	r =   [ 'doc pushLiteral_' + str( lVal ) ]
	r =  incrementBy( STACK_TOP, -1 )
	r += indirectSetLiteral( STACK_TOP, lVal )
	return r

def push( aLoc ):
	r =   [ 'doc pushing_' + str( aLoc ) ]
	r +=  incrementBy( STACK_TOP, -1 )
	r +=  [ 'doc indirectSet_STACK_TOP_' + str( aLoc ) ]
	r +=  [ 'set ' + COPY_FROM + ' ' + STACK_TOP ]
	r +=  [ 'set ' + COPY_TO + ' ' + COPY_TO ]
	r +=  [ 'copy' ]
	r +=  [ 'set ' + COPY_FROM + ' ' + str( aLoc ) ]
	r +=  [ 'copy' ]

	return r

def pop( aTo ):
	r =  [ 'doc pop_to_' + str( aTo )]
	r += deref( STACK_TOP, ADD_RESULT )
	r += copy( ADD_RESULT, aTo )
	r += incrementBy( STACK_TOP, 1 )
	return r

def relativeJump( incrLoc ):
	r = add( incrLoc, PROGRAM_COUNTER, ADD_RIGHT )
	r += [ "set " + ADD_LEFT + " 8" ] # 8 is magic adjustement to jump to correct program counter
	r += [ "add" ]
	r += [ "jump " + ADD_RESULT ]
	return r



def call( name, tag ):
	r =  [ 'doc call_' + str( name )]
	r += push( PROGRAM_COUNTER )
	r += indirectIncrement( STACK_TOP, 15 ) # 15 is a 'magic' displacement number of instructions - it depends on the current coding: len( indirectIncrement( STACK_TOP, 15 ) ) + 1
	r += [ 'goto procedure_begin_' + str(name) ]
	r += [ 'label procedure_rest_' + str(name) + '_' + str( tag )]

	return r



def procedure( name, body ):

	r =  [ 'doc procedure_' + str( name )]
	r += [ 'goto procedure_end_' + str( name )]
	r += [ 'label procedure_begin_' + str( name )]
	r += body
	r += [ 'doc poping_to_PC2']
	r += pop( PC2 )
	r += [ 'doc done_poping_to_PC2']
	r += copy( PC2, PROGRAM_COUNTER )
	r += [ 'doc done_poping_to_PC']
	r += [ 'label procedure_end_' + str( name )]
	return r








