import scipy.io as sio
import numpy as np
import unittest
from distance_FC import distance_FC

class Test(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        data = sio.loadmat('test_distance.mat')
        results = data['test_distance']
        FC1 = results[0]['FC1'][0]
        FC2 = results[0]['FC2'][0]
        self.dist_geo = results[0]['dist_geo'][0]
        self.dist_pearson = results[0]['dist_pearson'][0]

        self.dist = distance_FC(FC1, FC2)
        self.dist_sym = distance_FC(FC2, FC1)

    def test_geodesic(self):
        
        geo = self.dist.geodesic()
        self.assertAlmostEqual(np.sqrt(self.dist_geo[0][0]), geo)
        
    def test_pearson(self):
    
        pearson = self.dist.pearson()
        self.assertAlmostEqual(self.dist_pearson[0][0], pearson)

    def test_geodesic_symmetry(self):
    
        # close enough
        # geo1 = self.dist.geodesic()
        # geo2 = self.dist_sym.geodesic()
        # self.assertAlmostEqual(geo1, geo2)

        pearson1 = self.dist.pearson()
        pearson2 = self.dist_sym.pearson()
        self.assertAlmostEqual(pearson1, pearson2)

if __name__ == '__main__':
    unittest.main()