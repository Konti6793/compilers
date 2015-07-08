import tkinter


exec(open("parse.py").read())
exec(open("interpret.py").read())
exec(open("optimize.py").read())
exec(open("compile.py").read())


class Machine:


    def __init__( self ):
        pass

    def setView( self, gui  ):
        self.gui = gui
        self.gui.setMC( self )
         
    def setInstructions( self, s ):
        self.mem = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: -1, 6: 0, 7:0}
        self.instructions = s
        self.instructions = s if type( s ) == list else s.split( "\n" )
        self.instructions = [l.strip().split(" ") for l in self.instructions]
        self.control = 0
        self.outputs = []
        if self.gui is None:
            return
        else:
            self.gui.setInstructions( self.instructions )
            self.gui.setMemory( self.mem )


    def next( self ):
        if self.control < len( self.instructions):
            self.mem[6] = self.control
            self.mem[5] = -1

			# Retrieve the current instruction.
            inst = self.instructions[self.control]

			# Handle the instruction.
            if inst[0] == 'assert':
                assert self.mem[int( inst[1] )] == int( inst[2] )
            if inst[0] == 'doc':
                pass
            if inst[0] == 'label':
                pass
            if inst[0] == 'goto':
                self.control = self.instructions.index(['label', inst[1]])
            if inst[0] == 'branch' and self.mem[int(inst[2])]:
                self.control = self.instructions.index(['label', inst[1]])
            if inst[0] == 'jump':
                self.control = self.mem[int(inst[1])]
                return True
            if inst[0] == 'set':
                if self.mem.get( int(inst[1]) ) is None:
                    self.mem[ int(inst[1])] = 0
                self.mem[int(inst[1])] = int(inst[2])
                if int(inst[1]) == 6:
                    self.control = self.mem[6]
            if inst[0] == 'copy':
                if self.mem.get( self.mem[4] ) is None:
                    self.mem[ self.mem[4]] = 0
                if self.mem.get( self.mem[3] ) is None:
                    self.mem[ self.mem[3]] = 0
                self.mem[self.mem[4]] = self.mem[self.mem[3]]
                if self.mem[4] == 6:
                    self.control = self.mem[6]
            #if self.mem[4] == 6:
            #   control = self.mem[6] - 1 
            if inst[0] == 'add':
                self.mem[0] = self.mem[1] + self.mem[2]

            # Push the output address's content to the output.
            if self.mem[5] > -1:
                self.outputs.append(self.mem[5])

            # Move control to the next instruction.
            #print( control, inst, str( mem ) )

            self.control = self.control + 1

            if self.gui is None:
                return False
            else:
                self.gui.setMemory( self.mem )
                return True
        else:
                return False

class Debugger(tkinter.Tk):

    testProg = '''

    a := 100;
    a := 100;
    print a;
    a := 200;
    print a;
    b := not( true or false );
    print b;
    
    '''
    testProg = '''
assign a := [ 100, 200, 300 ];
print @a[0];
print @a[1];
print @a[2];
print 2+2;
    
    '''

    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
 
    def initialize(self):
        self.grid()
 
        self.pc = 1
 
       
        self.lists = {}
 
        
        Button =    lambda name, cb: tkinter.Button( self, command=cb, text = name )
        Label =     lambda name: tkinter.Label( self, fg = '#999999999', text = name, font=('Helvetica', 16, 'bold' ),  anchor=tkinter.W)
        Reg  =      lambda :  Label( '' )
        IMem  =     lambda :  tkinter.Button( self )
        RegLabel =  lambda name: tkinter.Label( self, text = name, anchor=tkinter.W, justify=tkinter.LEFT)
        Listbox  =  lambda : tkinter.Listbox( self, height = 20, selectmode = tkinter.SINGLE, exportselection = False, highlightthickness = 2 )
 
        self.regs = [ Reg(), Reg(), Reg(), Reg(), Reg(), Reg(), Reg(), Reg()]
 
        self.prog = Listbox()
        self.mem = Listbox()
        self.stack = Listbox()
 
        IMem1 = IMem()
        IMem2 = IMem()
        IMem3 = IMem()
        self.instrMems = [ IMem1, IMem2, IMem3 ]
 
 
        widgets  = []
        widgets += [[None,                  Button( 'Step', self.OnStep),          None]]
        widgets += [[Label( 'Register'),    Label( 'Name'),                        Label( 'Value')]]
        widgets += [[RegLabel( '0'),        RegLabel( 'ADD_RESULT'),               self.regs[0]]]
        widgets += [[RegLabel( '1'),        RegLabel( 'ADD_LEFT'),                 self.regs[1]]]
        widgets += [[RegLabel( '2'),        RegLabel( 'ADD_RIGHT'),                self.regs[2]]]
        widgets += [[RegLabel( '3'),        RegLabel( 'COPY_FROM'),                self.regs[3]]]
        widgets += [[RegLabel( '4'),        RegLabel( 'COPY_TO'),                  self.regs[4]]]
        widgets += [[RegLabel( '5'),        RegLabel( 'OUTPUT'),                   self.regs[5]]]
        widgets += [[RegLabel( '6'),        RegLabel( 'PC'),                       self.regs[6]]]
        widgets += [[RegLabel( '7'),        RegLabel( 'STACK'),                    self.regs[7]]]
        widgets += [[None,                  Label( 'Executed instruction'),        None]]
        widgets += [[IMem1,                 IMem2,                                 IMem3]]
        widgets += [[Label( 'Instructions'),Label( 'Heap'),                        Label( 'Stack')]]
        widgets += [[self.prog,             self.mem,                              self.stack]]
 
        rowNum = 0
        colNum = 0


 
        for row in widgets:
            for col in row:
                if col is not None:
                    col.grid( column = colNum, row = rowNum )
                colNum = colNum  + 1
 
            colNum = 0
            rowNum = rowNum + 1  


        b = Button( 'Compile', self.OnCompile )
        b.grid( column = 3, row = 0 )
        b = Button( 'Print', self.OnPrint)
        b.grid( column = 4, row = 0 )
        b = Button( 'Cont', self.OnContinue)
        b.grid( column = 5, row = 0 )
        self.source = tkinter.Text( self , height = 40, width = 60 )
        self.source.insert( 1.0, self.testProg )
        self.source.grid( column = 4, row = 3, rowspan = 40 )    
         
        r = Label( 'Result:')
        r.grid( row = 500, column = 0 )

        r = Label( 'expect the result here')
        r.grid( row = 500, column = 1, columnspan = 10 )

        self.result = r        
         
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())    
 
    def assign( self, name, value ):
        self.lists[ name ]  = value
 
    def setMC( self, m = None ):
        self.mc = m
 
    def setInstructions( self, instrs ):
        self.prog.delete( 0, tkinter.END )
        index = 0
        instructions = []
        for instr in instrs:
            stri = ''
            for x in instr:
                stri = stri + str( x ) + ' '
            s = str( index ) + ' : ' + str( stri )
            self.prog.insert( index, s )
            instructions += [ instr ]
            index = index + 1
        self.instructions = instructions
 
    def diplayInstr( self, progCounter ):
        comps = self.instructions[ progCounter ]
        for i in range( 0, 3 ):
            self.instrMems[ i ].config( text = "" )
 
        for i in range( 0, 3 ):
            if i >= len( comps ):
                break
            else:
                self.instrMems[ i ].config( text = comps[ i ] )
 
    def setMemory( self, mem ):

        self.stack.delete( 0, tkinter.END )
        self.mem.delete( 0, tkinter.END )
        for i in range( 0, 8 ):
            v = self.regs[ i ]
            nv = mem[ i ]
            if i == 6:
                self.prog.see( nv + 1)
                self.prog.selection_clear( first = nv, last = nv )
                self.prog.selection_set( first = nv+1, last = nv+1 )
                self.diplayInstr( nv )
            ov = 0 if v[ "text"] == "" else int( v[ "text"] )
            if nv != ov:
                v.config( fg = '#CCC000000')
            else:
                v.config( fg = '#000000000')
            v["text"] = str( nv )
        akeys = mem.keys()
        keys = sorted( akeys )
        index = 0
        for i in keys:
            if( i >=0 ):
                break
            else:
                s = str( i ) + ':' + str( mem[ i ])
                self.stack.insert( index, s )
                index = index + 1
        index = 0
        for i in keys:
            if( i < 10 ):
                continue
            else:
                s = str( i ) + ':' + str( mem[ i ])
                self.mem.insert( index, s )
                index = index + 1
 
    def OnStep( self ):

        if self.mc is None:
            return
        else:
            if not self.mc.next():
                self.result[ "text"] = "Done" + str( self.mc.outputs )
            else:
                self.result[ "text"] = str( self.mc.outputs )

    def OnContinue( self ):

        if self.mc is None:
            return
        else:
            while self.mc.next():
                continue
            self.result[ "text"] = "Done" + str( self.mc.outputs )



    def OnCompile( self ):

        s = self.source.get( 1.0, tkinter.END )
        code = compile( s )
        self.mc.setInstructions( code )

    def OnPrint( self ):

        s = self.source.get( 1.0, tkinter.END )
        code = compile( s )
        index = 0
        for i in code:
            print( str( index ) + ':\t' + str( i ) )
            index = index + 1        

  
    
 
if __name__ == "__main__":
    app = Debugger(None)
    app.title('Debugger')
    mc = Machine()
    mc.setView( app )
    app.mainloop()

