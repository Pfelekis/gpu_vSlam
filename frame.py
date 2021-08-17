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
 

#cuda
def extract(frame):


    
   # frame=frame.astype(np.uint8)
    #print (frame)
    #cv2.waitKey(0)
    #allocate
    gpu_frame=cv2.cuda_GpuMat()
    #upload to gpu
    gpu_frame.upload(frame)
    
    g_orb = cv2.cuda_ORB.create(nfeatures=1000,blurForDescriptor= True)

    gpu_frame = cv2.cuda.cvtColor(gpu_frame, cv2.COLOR_RGB2GRAY)

    #detector=cv2.cuda.createGoodFeaturesToTrackDetector(cv2.CV_8UC1,maxCorners=1500, qualityLevel=0.01, minDistance=7)
    
    #kp= detector.detect(gpu_frame)
    

   # g_kps, g_des= g_orb.detectAndComputeAsync(gpu_frame,None,keypoints=kp)

    g_kps, g_des= g_orb.detectAndComputeAsync(gpu_frame,None)

    #convert keypoints to cpu

    kp = [cv2.KeyPoint() for i in range(1000)]
    kp=g_orb.convert(g_kps)
    
    #print(g_des)
    des= g_des.download()
    
    #print(g_des)
   
    # return points of interest
    return np.array([(k.pt[0], k.pt[1]) for k in kp]).reshape(-1, 2), des, g_des
    
class Frame(object):
    def __init__(self, mapp, image, K):
        self.pose = IRt
        self.K = K
        self.Kinv = np.linalg.inv(self.K)
        self.scale = 2

        self.w, self.h = image.shape[0:2]
        
        kps, self.des, self.g_des = extract(image) 
        
        self.kps = normalise(self.Kinv, kps)
        self.pts = [None] * len(self.kps)
    
        self.id = len(mapp.frames)

        mapp.frames.append(self)
        
        
 

