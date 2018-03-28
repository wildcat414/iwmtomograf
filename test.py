import numpy as np
R = np.zeros((5, 5), dtype='float64')
R[:,0] = [1,1,1,1,1]
R[:,1] = 2
R[:,2] = 3
R[:,3] = 4
R[:,4] = 5
R1 = sum(R)
print(R[:,2])
print(R)
print(R1)
