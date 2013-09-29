"""
Two discipline components.
From Sellar's analytic problem.

    Sellar, R. S., Batill, S. M., and Renaud, J. E., "Response Surface Based, Concurrent Subspace
    Optimization for Multidisciplinary System Design," Proceedings References 79 of the 34th AIAA
    Aerospace Sciences Meeting and Exhibit, Reno, NV, January 1996.
"""

import numpy

from openmdao.main.api import Component
from openmdao.main.problem_formulation import OptProblem
from openmdao.lib.datatypes.api import Float

class Discipline1(Component):
    """Component containing Discipline 1."""
    
    # pylint: disable-msg=E1101
    z1 = Float(0.0, iotype='in', desc='Global Design Variable.')
    z2 = Float(0.0, iotype='in', desc='Global Design Variable.')
    x1 = Float(1.0, iotype='in', desc='Local Design Variable.')
    y2 = Float(1.0, iotype='in', desc='Disciplinary Coupling.')

    y1 = Float(iotype='out', desc='Output of this Discipline.')        

        
    def execute(self):
        """Evaluates the equation  
        y1 = z1**2 + z2 + x1 - 0.2*y2"""
                
        z1 = self.z1
        z2 = self.z2
        x1 = self.x1
        y2 = self.y2
        
        self.y1 = z1**2 + z2 + x1 - 0.2*y2
        #print "Dis 1 (%f, %f, %f, %f, out = %f)" % (z1, z2, x1, y2, self.y1)
        
        
class Discipline1_WithDerivatives(Component):
    """Component containing Discipline 1."""
    
    # pylint: disable-msg=E1101
    z1 = Float(0.0, iotype='in', desc='Global Design Variable.')
    z2 = Float(0.0, iotype='in', desc='Global Design Variable.')
    x1 = Float(0.0, iotype='in', desc='Local Design Variable.')
    y2 = Float(1.0, iotype='in', desc='Disciplinary Coupling.')

    y1 = Float(iotype='out', desc='Output of this Discipline.')        
   
    def execute(self):
        """Evaluates the equation  
        y1 = z1**2 + z2 + x1 - 0.2*y2."""
                
        z1 = self.z1
        z2 = self.z2
        x1 = self.x1
        y2 = self.y2
        
        self.y1 = z1**2 + z2 + x1 - 0.2*y2
        #print "Dis 1 (%f, %f, %f, %f, out = %f)" % (z1, z2, x1, y2, self.y1)

    def linearize(self):
        """ Calculate the Jacobian """
        
        self.J = numpy.zeros([1, 4])
        
        self.J[0, 0] = 1.0
        self.J[0, 1] = -0.2
        self.J[0, 2] = 2.0*self.z1
        self.J[0, 3] = 1.0
        
    def provideJ(self):
        """Alternative specification."""
        
        input_keys = ('x1', 'y2', 'z1', 'z2')
        output_keys = ('y1',)
        
        return input_keys, output_keys, self.J
                

class Discipline2(Component):
    """Component containing Discipline 2."""
    
    # pylint: disable-msg=E1101
    z1 = Float(0.0, iotype='in', desc='Global Design Variable.')
    z2 = Float(0.0, iotype='in', desc='Global Design Variable.')
    y1 = Float(1.0, iotype='in', desc='Disciplinary Coupling.')

    y2 = Float(iotype='out', desc='Output of this Discipline.')        

        
    def execute(self):
        """Evaluates the equation  
        y2 = y1**(.5) + z1 + z2"""
                
        z1 = self.z1
        z2 = self.z2
        
        # Note: this may cause some issues. However, y1 is constrained to be
        # above 3.16, so lets just let it converge, and the optimizer will 
        # throw it out
        y1 = abs(self.y1)
        
        self.y2 = y1**(.5) + z1 + z2
        #print "Dis 2 (%f, %f, %f, out = %f)" % (z1, z2, y1, self.y2)        
        
    
class Discipline2_WithDerivatives(Component):
    """Component containing Discipline 2."""
    
    # pylint: disable-msg=E1101
    z1 = Float(0.0, iotype='in', desc='Global Design Variable.')
    z2 = Float(0.0, iotype='in', desc='Global Design Variable.')
    y1 = Float(1.0, iotype='in', desc='Disciplinary Coupling.')

    y2 = Float(iotype='out', desc='Output of this Discipline.') 
    
    def execute(self):
        """Evaluates the equation  
        y2 = y1**(.5) + z1 + z2."""
                
        z1 = self.z1
        z2 = self.z2
        
        # Note: this may cause some issues. However, y1 is constrained to be
        # above 3.16, so lets just let it converge, and the optimizer will 
        # throw it out
        y1 = abs(self.y1)
        
        self.y2 = y1**(.5) + z1 + z2         
        #print "Dis 2 (%f, %f, %f, out = %f)" % (z1, z2, y1, self.y2)        
        
    def linearize(self):
        """ Calculate the Jacobian """
        
        self.J = numpy.zeros([1, 3])
        
        self.J[0, 0] = .5*(abs(self.y1))**-0.5
        self.J[0, 1] = 1.0
        self.J[0, 2] = 1.0

    def provideJ(self):
        """Alternative specification."""
        
        input_keys = ('y1', 'z1', 'z2')
        output_keys = ('y2',)
        
        return input_keys, output_keys, self.J

           
            

        
