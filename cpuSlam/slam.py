# Optimising the built map abcd
import time
import cv2
import numpy as np
from skimage.measure import ransac
from skimage.transform import FundamentalMatrixTransform, EssentialMatrixTransform
from frame import Frame
from display import Map, Point
from utilities import triangulate, denormalise, match_frames
from variables import IRt, K, W, H, Kinv, magenta, cyan
from benchmark import Timer
 

def process(image,fps):

    #start timer
    
    num_matches = 0

    #image = cv2.resize(image, (W, H))
    programTimer.extractionTimer(True)
    frame = Frame(mapp, image, K)
    programTimer.extractionTimer(False)
    if frame.id == 0:       # i.e just the start frame
        old_time=0
        return num_matches
    
    # Match frame keypoints

    f1 = mapp.frames[-1]
    f2 = mapp.frames[-2]

    programTimer.matchTimer(True)
    idx1, idx2, Rt = match_frames(f1, f2)
    programTimer.matchTimer(False)
    f1.pose = np.dot(Rt, f2.pose)

    for i, idx in enumerate(idx2):
        if f2.pts[idx] is not None:
            f2.pts[idx].add_observation(f1, idx1[i])

    # Homogeneous 3D coords
    programTimer.triangulateTimer(True)
    pts4d = triangulate(f1.pose, f2.pose,
            f1.kps[idx1], f2.kps[idx2])
    pts4d /= pts4d[:, 3:]
    

    programTimer.triangulateTimer(False)

    # Reject some points without enough parallax
    unmatched_points = np.array([f1.pts[i] is None for i in idx1])
    good_pts4d = (np.abs(pts4d[:, 3]) > 0.005) & (pts4d[:, 2] > 0) & unmatched_points
    
    for i, p in enumerate(pts4d):
        if not good_pts4d[i]:
            continue
        pt = Point(mapp, p)
        pt.add_observation(f1, idx1[i])
        pt.add_observation(f2, idx2[i])
    
   
    for pt1, pt2 in zip(f1.kps[idx1], f2.kps[idx2]):
        num_matches += 1
        u1, v1 = denormalise(K, pt1)
        u2, v2 = denormalise(K, pt2)
        cv2.circle(image, (u1, v1), color=magenta, radius=3)
        cv2.line(image, (u1, v1), (u2, v2), color=cyan, thickness=1)
        cv2.putText(image, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
    #print('Matches : ', num_matches)
    #2D display
    
    cv2.imshow('frames', image)
    
    
    # 3D display
    mapp.display_map()
    return num_matches

# Main classes    
mapp = Map()
mapp.create_viewer()



total_matches=0

old_time=0
new_time=0
fps=0  
nframeproc=0
font = cv2.FONT_HERSHEY_SIMPLEX


cap = cv2.VideoCapture('Videos/Test2.MP4')
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print( length )
programTimer=  Timer(length)   
programTimer.totalTimer(True)
while(cap.isOpened()):
    ret, frame = cap.read()
    nframeproc+=1
    if not ret or nframeproc==length:
        programTimer.totalTimer(False)
        break
    
    new_time=time.time()
    total_matches += process(frame,fps)
    
    fps=1/(new_time-old_time)
    old_time= new_time
    fps = int(fps)
    fps = str(fps)
    
    #run for 250 frames
    if nframeproc == 700:
        break
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        time.sleep(2)
        programTimer.totalTimer(False)
        break
programTimer.totalTimer(False)
programTimer.printTime()
print('Total frames computed:',nframeproc)
print('Average matches:',total_matches//nframeproc)
cv2.destroyAllWindows()
 
 

