from openmdao.main.api import Assembly
from openmdao.lib.drivers.api import MDASolver, SLSQPdriver
from openmdao.lib.casehandlers.api import CSVCaseRecorder

from sellar import (Discipline1, Discipline2,
    Discipline1_WithDerivatives, Discipline2_WithDerivatives)

class Opt(Assembly): 

    def configure(self): 

        #d1 = self.add('d1',Discipline1())
        #d2 = self.add('d2',Discipline2())
        d1 = self.add('d1',Discipline1_WithDerivatives())
        d2 = self.add('d2',Discipline2_WithDerivatives())

        self.d1.y1 = 1.0

        self.connect('d1.y1','d2.y1')
        self.connect('d2.y2','d1.y2')

        #Driver that knows how to automatically configure
        #   the MDA based on the dataflow graph. 
        mda = self.add('mda', MDASolver())
        mda.workflow.add(['d1','d2'])
        mda.recorders = [CSVCaseRecorder('mda_cases.csv'),]
        mda.newton=True

        driver = self.add('driver',SLSQPdriver())
        driver.add_parameter('d1.x1',low=0,high=10, start=1.0)
        driver.add_parameter(['d1.z1','d2.z1'],low=-10,high=10, start=5.0)
        driver.add_parameter(['d1.z2','d2.z2'],low=0,high=10, start=2.0)
        driver.add_objective('d1.x1**2+d1.z2+d1.y1+exp(-d2.y2)')
        driver.add_constraint('3.16 < d1.y1')
        driver.add_constraint('d2.y2 < 24.0')
        driver.recorders = [CSVCaseRecorder('opt_cases.csv'),]
        driver.workflow.add('mda')

if __name__ == "__main__": 

    o = Opt()
    o.run()
    print "x1: %3.2f, z1:%3.2f, z2:%3.2f, y1:%3.2f, y2:%3.2f"%(o.d1.x1, o.d1.z1, o.d1.z2, o.d1.y1, o.d1.y2)
    print "function calls: %d, derivative calls: %d"%(o.d1.exec_count, o.d1.derivative_exec_count)



