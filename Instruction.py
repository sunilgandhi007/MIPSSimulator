#Test Cases : 'GG: L.D F1, 4(R4)'
#           : 'L.D F2, 8(R5)'
#           : 'ADD.D F4, F6, F2'
#           : 'HLT'
#           : J LABEL 
#           : BNE R3, R4, Label 
#           : DADDI R1, R2, 43 


import unittest

class Tests(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_create_instruction(self):
        i1 = Instruction('GG: L.D F1, 4(R4)',0)
        self.assertEquals(i1.label,'GG')
        self.assertEquals(i1.operation,'L.D')
        self.assertEquals(i1.dest,'F1')
        self.assertEquals(i1.op1,'4(R4)')
        self.assertEquals(i1.op2,None)

        i2 = Instruction('L.D F2, 8(R5)',1)
        self.assertEquals(i2.label,None)
        self.assertEquals(i2.operation,'L.D')
        self.assertEquals(i2.dest,'F2')
        self.assertEquals(i2.op1,'8(R5)')
        self.assertEquals(i2.op2,None)
        
        i3 = Instruction('ADD.D F4, F6, F2',2)
        self.assertEquals(i3.label,None)
        self.assertEquals(i3.operation,'ADD.D')
        self.assertEquals(i3.dest,'F4')
        self.assertEquals(i3.op1,'F6')
        self.assertEquals(i3.op2,'F2')

        i4 = Instruction('HLT',3)
        self.assertEquals(i4.label,None)
        self.assertEquals(i4.operation,'HLT')
        self.assertEquals(i4.dest,None)
        self.assertEquals(i4.op1,None)
        self.assertEquals(i4.op2,None)

        i5 = Instruction('J LABEL',4)
        self.assertEquals(i5.label,None)
        self.assertEquals(i5.operation,'J')
        self.assertEquals(i5.dest,'LABEL')
        self.assertEquals(i5.op1,None)
        self.assertEquals(i5.op2,None)

        i6 = Instruction('BNE R3, R4, Label',5)
        self.assertEquals(i6.label,None)
        self.assertEquals(i6.operation,'BNE')
        self.assertEquals(i6.dest,'R3')
        self.assertEquals(i6.op1,'R4')
        self.assertEquals(i6.op2,'LABEL')

        i7 = Instruction('DADDI R1, R2, 43 ',6)
        self.assertEquals(i7.label,None)
        self.assertEquals(i7.operation,'DADDI')
        self.assertEquals(i7.dest,'R1')
        self.assertEquals(i7.op1,'R2')
        self.assertEquals(i7.op2,'43')

        i8 = Instruction('GG: DSUBI R1,R1,2 ',6)
        self.assertEquals(i8.label,'GG')
        self.assertEquals(i8.operation,'DSUBI')
        self.assertEquals(i8.dest,'R1')
        self.assertEquals(i8.op1,'R1')
        self.assertEquals(i8.op2,'2')

class Instruction():
    def __init__(self,operation,op1,op2,dest,label):
        self.op1 = op1
        self.op2 = op2
        self.dest = dest
        self.label = label
        self.operation = operation
    
    #Process the Instruction and store class variables
    def __init__(self,instruction_str,inst_addr):
        self.inst_addr = inst_addr
        instruction_str = instruction_str.upper()
        self.instruction_str = instruction_str
        seperate_label = instruction_str.split(':')
        if(len(seperate_label)==2):
            self.label = seperate_label[0]
            instruction_str = seperate_label[1]
        else:
            self.label = None
        instruction_str = instruction_str.strip()
        
        seperate_operation = instruction_str.split(None,1)
        self.operation = seperate_operation[0].strip()
        
        if (self.operation == 'HLT'):
            self.dest = None
            self.op1 = None
            self.op2 = None
            self.exunit = 'None'
            return
        
        operands = seperate_operation[1].split(',')
        if (len(operands)==1):
            self.dest = operands[0].strip()
            self.op1 = None
            self.op2 = None
        elif (len(operands)==2):
            self.dest = operands[0].replace(',','').strip()
            self.op1 = operands[1].replace(',','').strip()
            self.op2 = None
        elif(len(operands)==3):
            self.dest = operands[0].replace(',','').strip()
            self.op1 = operands[1].replace(',','').strip()
            self.op2 = operands[2].replace(',','').strip()
        else:
            print "Something is wrong with instruction: "+instruction_str

        # Get Execution Unit required
        f = open('executionUnit')
        lines = f.readlines()
        inst_exunit = {line.split(':')[0].strip():line.split(':')[1].strip() for line in lines}
        self.exunit = inst_exunit[self.operation]

if __name__ == '__main__':
    unittest.main()
    
