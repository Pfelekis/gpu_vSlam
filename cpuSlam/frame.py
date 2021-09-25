import cv2
import numpy as np
from skimage.measure import ransac
from skimage.transform import FundamentalMatrixTransform, EssentialMatrixTransform
from utilities import normalise
# Colors
magenta = (255, 0, 255)
cyan = (255, 255, 0)

# Global Variables
IRt = np.eye(4)
 


def extract(frame):
    orb = cv2.ORB_create(nfeatures=500)
    
    # Detection
    #features = cv2.goodFeaturesToTrack(np.mean(frame, axis=2).astype(np.uint8),
    #        maxCorners=500, qualityLevel=0.01, minDistance=7)
    #print('heeeyyy')

    # Extraction
    #kp = [cv2.KeyPoint(x = f[0][0], y = f[0][1], size=20) for f in features]
    kp, des = orb.detectAndCompute(frame,None)
    
    # return points of interest
    return np.array([(k.pt[0], k.pt[1]) for k in kp]).reshape(-1, 2), des
    
class Frame(object):
    def __init__(self, mapp, image, K):
        self.pose = IRt
        self.K = K
        self.Kinv = np.linalg.inv(self.K)
        self.scale = 2

        self.w, self.h = image.shape[0:2]
    
        kps, self.des = extract(image)
        self.kps = normalise(self.Kinv, kps)
        self.pts = [None] * len(self.kps)
    
        self.id = len(mapp.frames)
        mapp.frames.append(self)
 
 

