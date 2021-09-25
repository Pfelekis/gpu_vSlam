import numpy as np



# Colors
magenta = (255, 0, 255)
cyan = (255, 255, 0)

# Global Variables
IRt = np.eye(4)


# Colors
magenta = (255, 0, 255)
cyan = (255, 255, 0)

# Camera insintrics
#W = 1920
#H = 1080


W = 752 
H = 480


# Focal Length
F = 800     # varies for videos, make it a parameter
Fx =3018
Fy = 3016
# Global Variables
K = np.array(([Fx, 0, W // 2], [0, Fy, H // 2], [0, 0, 1]))
Kinv = np.linalg.inv(K) 
