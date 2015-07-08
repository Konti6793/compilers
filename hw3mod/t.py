a = '''  ?  
1111
2222
3333
444

666
  7777

'''

print( a )

q = a.split( "\n")

print( q )

index = 0;

for x in q:
	print( index, ' === "' + x +  '"')
	index = index + 1
