import unittest
from Stage import *

class Tests(unittest.TestCase):
    def setUp(self):
        self.IF = Unit('IF',1,True)
        self.EXADD = Unit('EXADD',6,True)

    def test_is_free(self):
        self.assertEquals(self.IF.is_free(),1)
    
    def test_add_new_inst(self):
        self.IF.add_new_inst('ADD.D F4, F6, F2',0)
        self.assertEquals(self.IF.is_free(),0)

    def test_pipeline(self):
        IF = Unit('IF',1,True)
        IF.add_new_inst('GG: L.D F1, 4(R4)',0)
        EXADD = Unit('EXADD',6,True)
        for i in range(1,8):
            print "-------------"+str(i)+"--------------"
            # Find whether there is instruction in last stage
            print IF
            print EXADD
            last_stage_instruction = EXADD.last_stage.instruction
            EXADD.update_unit(IF,i)
            if(EXADD.is_last_stage_free() and last_stage_instruction!=None):
                print last_stage_instruction.operation+" completed at "+str(i)
        IF.update_unit(None,i)



class Unit():
    def __init__(self,name,number_of_stages,is_pipelined):
        self.name = name
        self.number_of_stages = number_of_stages
        self.is_pipelined= is_pipelined
        # Create an array of stages
        self.stages = []
        if(self.is_pipelined==True):
            for i in range(0,number_of_stages):
                s1 = Stage(None,i,1,None)
                self.stages.append(s1)
        else:
            s1 = Stage(None,1,number_of_stages,None)
            self.stages.append(s1)
        
    def is_free(self):
        s1 = self.stages[0]
        if(s1.is_free()):
            return 1
        else:
            return 0
    
    def is_last_stage_free(self):
        return self.last_stage.is_free()
        
    def add_inst(self,prev_unit,clk):
        if(self.is_free()):
            self.stages[0].add_inst(prev_unit.last_stage,clk)
            print "Moving from "+prev_unit.name + " to " + self.name
        else:
            print self.name+" is not free"
    
    @property
    def last_stage(self):
        return self.stages[self.number_of_stages-1]

    def update_unit(self,prev_unit,clk):
        if(self.is_pipelined):
            for i in range(self.number_of_stages-1,-1,-1):
                #print "============="+str(i)+"==========="
                if(i==0):
                    self.stages[i].update_stage(None,clk)
                else:
                    self.stages[i].update_stage(self.stages[i-1],clk)

            if(prev_unit!=None):
                if(self.is_free() and not prev_unit.is_last_stage_free()):
                    self.add_inst(prev_unit,clk)
                    return True
            return False
        else:
             self.stages[0].update_stage(None,clk)
             if(prev_unit!=None):
                 if(self.is_free() and not prev_unit.is_last_stage_free()):
                     self.add_inst(prev_unit,clk)
                     return True
             return False

    def add_new_inst(self,instruction_str,clk):
        if(self.is_free()):
            self.stages[0].add_new_inst(Instruction(instruction_str),clk)
        else:
            print self.name+" is not free"

    def __str__(self):
        unit_state = self.name+"\n"
        if(self.is_pipelined):
            for i in range(self.number_of_stages):
                unit_state += '{:16s}'.format(self.stages[i].__str__())+"|"
        else:
            unit_state += '{:16s}'.format(self.stages[0].__str__())+"|"
        return unit_state+"\n"
        
if __name__ == '__main__':
    #unittest.main()
    IF = Unit('IF',1,True)
    IF.add_new_inst('GG: L.D F1, 4(R4)',0)
    EXADD = Unit('EXADD',6,True)
    for i in range(1,8):
        print "-------------"+str(i)+"--------------"
        # Find whether there is instruction in last stage
        print IF
        print EXADD
        last_stage_instruction = EXADD.last_stage.instruction
        EXADD.update_unit(IF,i)
        if(EXADD.is_last_stage_free() and last_stage_instruction!=None):
            print last_stage_instruction.operation+" completed at "+str(i)
        IF.update_unit(None,i)

