import cv2
import numpy as np
from skimage.measure import ransac
from skimage.transform import FundamentalMatrixTransform
from skimage.transform import EssentialMatrixTransform


def add_ones(x):
    return np.concatenate([x,np.ones((x.shape[0],1))],axis=1)
def extractRt(E):
   W = np.mat([[0,-1,0],[1,0,0],[0,0,1]], dtype=float)
   U,w,Vt = np.linalg.svd(E)
   assert np.linalg.det(U) > 0
   if np.linalg.det(U)<0:
       Vt *= -1
   R = np.dot(np.dot(U,W), Vt)

   if np.sum(R.diagonal()) < 0:
       Vt  *= -1
   R = np.dot(np.dot(U,W.T), Vt)
   t = U[:,2]
   return np.concatenate([R, t.reshape(3,1)],axis=1)

def normalize(Kinv,pts):
    return np.dot(Kinv, add_ones(pts).T).T[:,0:2]

def denormalize(K,pt):
    ret = np.dot(K, np.array([pt[0],pt[1], 1.0]))
    ret /= ret[2]
    return int(round(ret[0])), int(round(ret[1]))

def match(f1,f2):
    bf=cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(f1.des, f2.des, k = 2)

    ret = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            p1 = f1.pts[m.queryIdx]
            p2 =  f2.pts[m.trainIdx]
            ret.append((p1,p2))

    assert len(ret) >= 8
    ret = np.array(ret)

    #fit matrix
    model, inliers = ransac((ret[:,0], ret[:,1]),
                             #FundamentalMatrixTransform,
                             EssentialMatrixTransform,
                             min_samples=8,
                             residual_threshold=0.005,
                             max_trials=100)
    #ignore outliers
    ret = ret[inliers]
    Rt  = extractRt(model.params)

    #return
    return ret, Rt


class Frame(object):
    def __init__(self,img,K):

        self.K = K
        self.Kinv = np.linalg.inv(self.K)

        pts, self.des  = extract(img)
        self.pts = normalize(self.Kinv,pts)


def extract(img):
    orb = cv2.ORB_create(1000)
    pts = cv2.goodFeaturesToTrack(np.mean(img,axis=2).astype(np.uint8),3000,qualityLevel=0.01,minDistance=3)

    kps = [cv2.KeyPoint(x=f[0][0], y=f[0][1], _size=20) for f in pts]
    kps, des = orb.compute(img,kps)
    return np.array([(kp.pt[0],kp.pt[1]) for kp in kps]),des
