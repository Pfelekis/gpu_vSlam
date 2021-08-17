
import numpy as np
import cv2
import time
from skimage.measure import ransac
from skimage.transform import FundamentalMatrixTransform, EssentialMatrixTransform


#return cv2.triangulatePoints(pose1[:3], pose2[:3], pts1.T, pts2.T).T
def triangulate(pose1, pose2, pts1, pts2):
    # linear triangulation method
    ret = np.zeros((pts1.shape[0], 4))
    pose1 = np.linalg.inv(pose1)
    pose2 = np.linalg.inv(pose2)
    for i, p in enumerate(zip(pts1, pts2)):
        A = np.zeros((4, 4))
        A[0] = p[0][0] * pose1[2] - pose1[0]
        A[1] = p[0][1] * pose1[2] - pose1[1]
        A[2] = p[1][0] * pose2[2] - pose2[0]
        A[3] = p[1][1] * pose2[2] - pose2[1]
        _, _, vt = np.linalg.svd(A)
        ret[i] = vt[3]
    
    return ret

def add_ones(x):
    return np.concatenate([x, np.ones((x.shape[0], 1))], axis=1)
 


def extractRt(E):
    # E -> Essential Matrix
    # F -> Fundamental Matrix
    W = np.mat([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=float)
    U, d, Vt = np.linalg.svd(E)

    #assert np.linalg.det(U) > 0

    if np.linalg.det(Vt) < 0:
        Vt *= -1.0
    R = np.dot(np.dot(U, W), Vt)
    if np.sum(R.diagonal()) < 0:
        R = np.dot(np.dot(U, W.T), Vt)
    t = U[:, 2]
    ret = np.eye(4)
    ret[:3, :3] = R
    ret[:3, 3] = t
    Rt = np.concatenate([R, t.reshape(3, 1)], axis=1)
    return ret




def normalise(Kinv, pts):
    return np.dot(Kinv, add_ones(pts).T).T[:, 0:2]
 
def denormalise(K, pt):
    ret = np.dot(K, np.array([pt[0], pt[1], 1.0]))
    ret /= ret[2]
    return int(ret[0]), int(ret[1])



def match_frames(f1, f2):

    
   # print(f1.g_des,f2.g_des)
    g_bf=cv2.cuda_DescriptorMatcher.createBFMatcher(cv2.NORM_HAMMING)
    g_matches= g_bf.knnMatchAsync(f1.g_des, f2.g_des, k=2)

    matches=g_bf.knnMatchConvert(g_matches)


    #print(match)
   # bf = cv2.BFMatcher(cv2.NORM_HAMMING)
   # matches = bf.knnMatch(f1.des, f2.des, k=2)
    
    
    
    # Lowe's Ratio Test
    ret = []
    idx1, idx2 = [], []
    
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            '''
            # keep indices
            idx1.append(m.queryIdx)
            idx2.append(m.trainIdx)
            
            p1 = f1.features[m.queryIdx]
            p2 = f2.features[m.trainIdx]

            ret.append((p1, p2))
            '''
            p1 = f1.kps[m.queryIdx]
            p2 = f2.kps[m.trainIdx]
            # fix error
            # travel less than 10% of diagonal and be within orb distance 32
            if np.linalg.norm((p1 - p2)) < 0.1 * np.linalg.norm([f1.w, f1.h]) and m.distance < 32:
                # keep indices
                idx1.append(m.queryIdx)
                idx2.append(m.trainIdx)
                
                ret.append((p1, p2))

    assert len(ret) >= 8
    ret = np.array(ret)
    idx1 = np.array(idx1)
    idx2 = np.array(idx2)
    
    # Fit matrix
    model, inliers = ransac((ret[:, 0], ret[:, 1]),
                            FundamentalMatrixTransform,
                            #EssentialMatrixTransform,
                            min_samples=8,
                            #residual_threshold=0.01,
                            residual_threshold=0.001,
                            max_trials=100)
    Rt = extractRt(model.params)
    
    return idx1[inliers], idx2[inliers], Rt