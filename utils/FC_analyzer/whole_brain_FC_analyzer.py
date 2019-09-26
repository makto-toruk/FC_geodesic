import numpy as np
import os
import pickle
import sys
import random
from glob import glob
from concurrent.futures import ThreadPoolExecutor, wait, as_completed

'''
when using LR from condition 1 as test, and RL from condition 2 as train
matrix transpose (by symmetry) also provides distance matrix for
RL from condition 2 as test and LR from condition 1 as test
- reduces computation by half
'''

class distance_matrix_requestor(object):
    def __init__(self, condition1, condition2,
                 DIR, trim_method, max_workers,
                 N=20, kROI=300,
                 tau_list=[0, 0.001, 0.01, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20]):
        
        self.condition1 = condition1
        self.condition2 = condition2
        self.N = N
        self.kROI = kROI
        self.max_workers = max_workers
        '''
        trim_method: 'full' or 'trim' or 'truncated'
        '''
        self.trim_method = trim_method
        self.tau_list = tau_list
        
        self.DATA_DIR = DIR + '/data'
        self.SAVE_DIR = DIR + '/results/%s/N_%d_kROI_%d/whole_brain/distance_matrix' %(
                        self.trim_method, self.N, self.kROI)
        self.TEMP_DIR = DIR + '/z_temp'

        if not os.path.exists(self.SAVE_DIR):
            os.makedirs(self.SAVE_DIR)
        if not os.path.exists(self.TEMP_DIR):
            os.makedirs(self.TEMP_DIR)

        # is rank of the matrix a concern?
        self.rank_flag = False
        # load distance_FC class
        UTILS_DIR = DIR + '/utils/distance_FC'
        sys.path.insert(0, UTILS_DIR)
        from distance_FC import distance_FC
        self.distance_FC = distance_FC

    def _info(self, s):
        print('INFO: %s' %(s))

    def _get_save_path(self, tau, distance):

        base_file = '%s_test_%s_%s_train_%s_%s_tau_%s.pkl' %(distance, self.condition1, self.p1,
                                                             self.condition2, self.p2, tau)
        dist_path = self.SAVE_DIR + '/' + base_file

        return base_file, dist_path

    def _get_save_path_symmetric(self, tau, distance):
        base_file = '%s_test_%s_%s_train_%s_%s_tau_%s.pkl' %(distance, self.condition2, self.p2,
                                                             self.condition1, self.p1, tau)
        dist_path = self.SAVE_DIR + '/' + base_file
        return base_file, dist_path
        

    def _save_dist(self, D, tau, distance):
        
        base_file, dist_path = self._get_save_path(tau, distance)
        
        # save in TEMP_DIR
        temp_path = '%s/%s' %(self.TEMP_DIR, base_file)
        with open(temp_path, 'wb') as f:
            pickle.dump(D, f)

        # move to SAVE_DIR
        move_file = 'mv %s/%s %s' %(self.TEMP_DIR, base_file, dist_path)
        os.system(move_file)

        '''
        distances are symmetric
        the transpose of the distance matrices are for
        test data = condition2, train data = condition1
        '''
        base_file, dist_path = self._get_save_path_symmetric(tau, distance)

        # if they don't exist, save
        if not os.path.isfile(dist_path):
            
            # save in TEMP_DIR
            temp_path = '%s/%s' %(self.TEMP_DIR, base_file)
            with open(temp_path, 'wb') as f:
                # transpose must be saved here
                pickle.dump(np.transpose(D), f)

            # move to SAVE_DIR
            move_file = 'mv %s/%s %s' %(self.TEMP_DIR, base_file, dist_path)
            os.system(move_file)
    
    def _compute_dist_matrix(self, tau, distance):
        
        base_file, dist_path = self._get_save_path(tau, distance)
        # SVD will not always converge,
        # continue if it doesn't
        try:                
            # if they don't exist, save
            if not os.path.isfile(dist_path):
                self._info('%s: condition 1 %s condition 2 %s tau %s' %(distance,
                            self.condition1, self.condition2, tau))            
                D = []
                for FC1 in self.FC_list1:
                    d = [] # argmin(d) is nearest neighbor of FC1 (test)
                    for FC2 in self.FC_list2:
                        dist = self.distance_FC(FC1 + tau*np.identity(self.kROI),
                                                FC2 + tau*np.identity(self.kROI))
                        if distance == 'geodesic':
                            d.append(dist.geodesic())
                        elif distance == 'pearson':
                            d.append(dist.pearson())
                    D.append(d)

                self._save_dist(np.array(D), tau, distance)

            else:
                self._info('Skipping %s: condition 1 %s condition 2 %s tau %s' %(distance,
                            self.condition1, self.condition2, tau))    
        except np.linalg.LinAlgError:
            self._info('SVD fail %s: condition 1 %s condition 2 %s tau %s' %(distance,
                        self.condition1, self.condition2, tau))
            self._save_dist([], tau, distance)

    
    def _get_dist_matrix(self):
        '''
        input: FC_list1, FC_list2 - list of FCs of equal size
        output: save distance matrices (geodesic and pearson)
                of size NxN
        '''

        tau = 0 # this case is run irresepctive of rank flag
        '''
        pearson
        '''
        distance = 'pearson'
        self._compute_dist_matrix(tau, distance)
        
        '''
        geodesic
        '''
        distance = 'geodesic'
        
        if self.rank_flag:
            # this case is applicable only to geodesic distance 
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [executor.submit(self._compute_dist_matrix, tau, distance) 
                           for tau in self.tau_list]
                results = [r.result() for r in as_completed(futures)]
            # for tau in self.tau_list:
            #     self._compute_dist_matrix(tau, distance)
        else:
            tau = 0
            self._compute_dist_matrix(tau, distance)
            
    def make_distance_requests(self):
        '''
        for a given pair of conditions, get distance matrices
        '''

        file = '%s/%s/FC_N_%d_kROI_%d_%s_blocks.pkl' %(
                self.DATA_DIR, self.condition1, self.N, self.kROI, self.trim_method)
        with open(file, 'rb') as f:
            data1 = pickle.load(f)
            
        file = '%s/%s/FC_N_%d_kROI_%d_%s_blocks.pkl' %(
                self.DATA_DIR, self.condition2, self.N, self.kROI, self.trim_method)
        with open(file, 'rb') as f:
            data2 = pickle.load(f)

        # fixed
        self.p1 = 'LR1'
        self.p2 = 'RL1'
        '''
        due to symmetry of the distance measure, RL1 for test and
        LR1 for train will occur when the conditions are reversed
        '''

        self.FC_list1 = [FC[self.p1] for FC in data1]
        self.FC_list2 = [FC[self.p2] for FC in data2]
        self._get_dist_matrix()

class accuracy_requestor(object):
    def __init__(self, condition1, condition2,
                 DIR, trim_method, max_workers,
                 N=20, kROI=300):
    
        self.condition1 = condition1
        self.condition2 = condition2
        self.N = N
        self.kROI = kROI
        self.max_workers = max_workers
        self.trim_method = trim_method
        self.LOAD_DIR = DIR + '/results/%s/N_%d_kROI_%d/whole_brain/distance_matrix' %(
                        self.trim_method, self.N, self.kROI)
        self.SAVE_DIR = DIR + '/results/%s/N_%d_kROI_%d/whole_brain/accuracy' %(
                        self.trim_method, self.N, self.kROI)
        self.TEMP_DIR = DIR + '/z_temp'
        
        # get all distance matrices
        files = [y for x in os.walk(self.LOAD_DIR) 
                 for y in glob(os.path.join(x[0], '*.pkl'))]

        self.distance_matrices = []
        for file in files:
            if (self.condition1 in file) and (self.condition2 in file):
                self.distance_matrices.append(file)

        if not os.path.exists(self.SAVE_DIR):
            os.makedirs(self.SAVE_DIR)
        if not os.path.exists(self.TEMP_DIR):
            os.makedirs(self.TEMP_DIR)
        
    def _info(self, s):
        print('INFO: %s' %(s))

    def _compute_accuracy(self, D):
        N_ = D.shape[0]
        labels = D.argmin(1)
        true = [ii for ii in range(N_)]
        accuracy = [1 if y_hat == y else 0 for y_hat, y in zip(labels, true)]
        
        return np.mean(accuracy)

    def _get_accuracy(self, file):

        base_file = os.path.basename(file)
        save_path = '%s/%s' %(self.SAVE_DIR, base_file)

        # if they don't exist, save
        if not os.path.isfile(save_path):
            with open(file, 'rb') as f:
                D = pickle.load(f)
            
            # if SVD failed, D is []
            # use list since np array gets confused by if
            if list(D):
                accuracy = self._compute_accuracy(D)
                self._info('Accuracy for %s = %s' %(base_file, accuracy))  

                # save in TEMP_DIR
                temp_path = '%s/%s' %(self.TEMP_DIR, base_file)
                with open(temp_path, 'wb') as f:
                    pickle.dump(accuracy, f)

                # move to SAVE_DIR
                move_file = 'mv %s/%s %s' %(self.TEMP_DIR, base_file, save_path)
                os.system(move_file)

        else:
            self._info('Skip %s' %(base_file))  
    
    def make_accuracy_requests(self):
        '''
        obtain accuracy based on distance matrix
        if not already found
        '''
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self._get_accuracy, file) 
                        for file in self.distance_matrices]
            results = [r.result() for r in as_completed(futures)]

    def _compute_bootstrap_accuracy(self, D):

        N_ = D.shape[0]
        pool = [ii for ii in range(N_)]

        A = []
        for b in range(self.b_inner):
    
            choice = random.choices(pool, k=N_)
            D_ = D[np.ix_(choice, choice)]
            labels = D_.argmin(1)
            true = [choice.index(jj) for jj in choice] # where it first occurs
            accuracy = [1 if y_hat == y else 0 for y_hat, y in zip(labels, true)]
            A.append(np.mean(accuracy))

        return np.mean(A)

    def _get_bootstrap_accuracy(self, file):

        base_file = os.path.basename(file)
        filename, file_extension = os.path.splitext(base_file)
        base_file = filename + '_B_%d_b_%d' %(self.B_outer, self.b_inner) + file_extension

        save_path = '%s/%s' %(self.SAVE_DIR, base_file)

        # if they don't exist, save
        if not os.path.isfile(save_path):
            with open(file, 'rb') as f:
                D = pickle.load(f)
            
            # if SVD failed, D is []
            # use list since np array gets confused by if
            if list(D):
                '''
                set the seed such that identical random numbers
                are generated for each D
                '''
                random.seed(42)

                accuracy = []
                for B in range(self.B_outer):
                    accuracy.append(self._compute_bootstrap_accuracy(D))
                
                self._info('Accuracy for %s = %s' %(base_file, np.mean(accuracy)))

                # save in TEMP_DIR
                temp_path = '%s/%s' %(self.TEMP_DIR, base_file)
                with open(temp_path, 'wb') as f:
                    pickle.dump(accuracy, f)

                # move to SAVE_DIR
                move_file = 'mv %s/%s %s' %(self.TEMP_DIR, base_file, save_path)
                os.system(move_file)

        else:
            self._info('Skip %s' %(base_file))  
    
    def make_bootstrap_accuracy_requests(self, B_outer, b_inner):
        '''
        obtain accuracy based on distance matrix
        if not already found
        '''
        self.B_outer = B_outer
        self.b_inner = b_inner

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self._get_bootstrap_accuracy, file) 
                        for file in self.distance_matrices]
            results = [r.result() for r in as_completed(futures)]


