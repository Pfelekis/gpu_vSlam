import numpy as np
import cv2





# Colors
magenta = (255, 0, 255)
cyan = (255, 255, 0)

# Global Variables
IRt = np.eye(4)


# Colors
magenta = (255, 0, 255)
cyan = (255, 255, 0)

# Camera insintrics
#1080p
W = 1920
H = 1080

#720p
 
#W= 1280  
#H= 720

#480p
#W= 640
#H= 480
# Focal Length
F = 500     # varies for videos, make it a parameter

# Global Variables
K = np.array(([F, 0, W // 2], [0, F, H // 2], [0, 0, 1]))
Kinv = np.linalg.inv(K) 
