import numpy as np
from numpy import linalg as LA

class distance_FC(object):
    def __init__(self, FC1, FC2, eig_thresh=10**(-3)):
        self.FC1 = FC1
        self.FC2 = FC2
        self.eig_thresh = eig_thresh

        # ensure symmetric
        self.FC1 = self._ensure_symmetric(self.FC1)
        self.FC2 = self._ensure_symmetric(self.FC2)

    def _info(self, s):
        print('INFO: %s' % s)

    def _ensure_symmetric(self, Q):
        '''
        computation is sometimes not precise (round errors),
        so ensure matrices that are supposed to be
        symmetric are symmetric
        '''
        return (Q + np.transpose(Q))/2

    def _vectorize(self, Q):
        '''
        given a symmetric matrix (FC), return unique
        elements as an array. Ignore diagonal elements
        '''
        # extract lower triangular matrix
        tri = np.tril(Q, -1)

        vec = []
        for ii in range(1, tri.shape[0]):
            for jj in range(ii):
                vec.append(tri[ii, jj])
        
        return np.asarray(vec)

    def geodesic(self):
        '''
        dist = sqrt(trace(log^2(M)))
        M = Q_1^{-1/2}*Q_2*Q_1^{-1/2}
        '''
        # compute Q_1^{-1/2} via eigen value decmposition
        u, s, _ = LA.svd(self.FC1, full_matrices=True)

        ## lift very small eigen values
        for ii, s_ii in enumerate(s):
            if s_ii < self.eig_thresh:
                s[ii] = self.eig_thresh

        '''
        since FC1 is in S+, u = v, u^{-1} = u'
        FC1 = usu^(-1)
        FC1^{1/2} = u[s^{1/2}]u'
        FC1^{-1/2} = u[s^{-1/2}]u'
        '''
        FC1_mod = u @ np.diag(s**(-1/2)) @ np.transpose(u)
        M = FC1_mod @ self.FC2 @ FC1_mod

        '''
        trace = sum of eigenvalues;
        np.logm might have round errors,
        implement using svd instead
        '''
        _, s, _ = LA.svd(M, full_matrices=True)

        return np.sqrt(np.sum(np.log(s)**2))

    def pearson(self):
        '''
        conventional Pearson distance between
        two FC matrices. The matrices are vectorized
        '''
        vec1 = self._vectorize(self.FC1)
        vec2 = self._vectorize(self.FC2)

        return (1 - np.corrcoef(vec1, vec2)[0, 1])/2







    
