import unittest

import numpy as np
import pandas as pd
from numpy import testing as nptest

from operational_analysis.toolkits import unit_conversion

class SimpleUnitConversionTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_convert_power_to_energy(self):
        np.random.seed(42)
        power = np.random.random(100)*100
        time_interval=[10,30,60] # Minutes
        df=pd.DataFrame(data={'power_kw':power})
        
        for t in time_interval:
            energy = power * t / 60
            energy_test = unit_conversion.convert_power_to_energy(df['power_kw'],t)
            nptest.assert_almost_equal(energy, energy_test, err_msg="Convert power to energy is broken") 
            
    def test_convert_power_to_energy(self):
        # Set some test values
        net = np.array([[1, 1, 1],
                       [0, 1, 1],
                       [1, 1, 1]])
        avail = np.array([[0.05, 0.08, 0.2],
                         [0.05, .9, 0.2],
                         [0.05, .9, 0]])
        curt = np.array([[0.05, 0.05, 0.05],
                        [0.05, 0.2, 0.05],
                        [0.05, -0.1, 0.05]])
       
        # Make sure different combinations of 'frac' and 'energy' based measurements work out
        nptest.assert_almost_equal(unit_conversion.compute_gross_energy(net[0,:], avail[0,:], curt[0,:], 'frac', 'frac'), 
                                   [1.1111, 1.1494, 1.3333],
                                   decimal = 4)
        nptest.assert_almost_equal(unit_conversion.compute_gross_energy(net[0,:], avail[0,:], curt[0,:], 'energy', 'frac'), 
                                   [1.1026, 1.1326, 1.2526],
                                   decimal = 4)
        nptest.assert_almost_equal(unit_conversion.compute_gross_energy(net[0,:], avail[0,:], curt[0,:], 'frac', 'energy'), 
                                   [1.1026, 1.1370, 1.3000],
                                   decimal = 4)
        nptest.assert_almost_equal(unit_conversion.compute_gross_energy(net[0,:], avail[0,:], curt[0,:], 'energy', 'energy'), 
                                   [1.1000, 1.1300, 1.2500],
                                   decimal = 4)
       
        # Make sure exceptions are thrown when bad input data is identified
        def func(): # Function to return exception
            unit_conversion.compute_gross_energy(net[1,:], avail[1,:], curt[1,:], 'frac', 'frac')
        with self.assertRaises(Exception): func()
        
        def func(): # Function to return exception
            unit_conversion.compute_gross_energy(net[2,:], avail[2,:], curt[2,:], 'frac', 'frac')
        with self.assertRaises(Exception): func()
     
    def tearDown(self):
        pass

if __name__ == '__main__':

    unittest.main()
