import numpy as np, cv2, main
from PointsCloud import *

class StereoPair:

    def __init__(self, pair_1, pair_2, params):
        self.image_1 = pair_1[0] # image_1
        self.camera_1 = pair_1[1] # camera_1
        self.image_2 = pair_2[0] # image_2
        self.camera_2 = pair_2[1] # camera_2
        self.params = params

        K1, distCoeffs1, R1, t1 = (self.camera_1).getParams()
        K2, distCoeffs2, R2, t2 = (self.camera_2).getParams()

        R = R2.dot(R1.transpose())
        t = -R.dot(t1) + t2
        self.R1, R2, P1, P2, self.Q, validPixROI1, validPixROI2 = \
            cv2.stereoRectify\
                (
                    cameraMatrix1=K1,
                    distCoeffs1=distCoeffs1,
                    cameraMatrix2=K2,
                    distCoeffs2=distCoeffs2,
                    imageSize=(self.image_1).shape[:2],
                    R=R,
                    T=t
                )

        self.imgL = createRectifiedFrame(image=self.image_1, K=K1, distCoeffs=distCoeffs1, R=self.R1, P=P1)

        self.imgR = createRectifiedFrame(image=self.image_2, K=K2, distCoeffs=distCoeffs2, R=R2, P=P2)

        self.depth_map = createDepthMap(imgL=self.imgL, imgR=self.imgR, params=params)

    def saveData(self, filename):
        cv2.imwrite(filename=filename+'imgL'+main.image_extension, img=self.imgL)

        cv2.imwrite(filename=filename+'imgR'+main.image_extension, img=self.imgR)

        cv2.imwrite(filename=filename+'depth_map'+main.image_extension, img=self.depth_map - self.params['min_disp'])

    def getPointsCloud(self, limits):
        mask = self.depth_map > (self.depth_map).min()

        points = cv2.reprojectImageTo3D(self.depth_map, self.Q)

        colors = cv2.cvtColor(self.imgL, cv2.COLOR_BGR2RGB)

        points_cloud = PointsCloud(points=points[mask], colors=colors[mask])

        return points_cloud.makeBoundingBox(limits)

    def transformPCtoMainCoordinateSystem(self, cloud):
        print 'the transformation of the point cloud to the main coordinate system'

        points_cloud = PointsCloud()

        R, t = (self.camera_1).R, ((self.camera_1).t).reshape((3,1))

        for i in range(cloud.size()):
            X = (cloud.points[i]).reshape((3,1))
            X_new = np.linalg.inv(R).dot(np.linalg.inv(self.R1).dot(X) - t)

            color = cloud.colors[i]

            points_cloud.append(set=(X_new.reshape((1,3)), color))

        return points_cloud

def createRectifiedFrame(image, K, distCoeffs, R, P):
    map1, map2 = cv2.initUndistortRectifyMap\
        (
            cameraMatrix=K,
            distCoeffs=distCoeffs,
            R=R,
            newCameraMatrix=P[:3,:3],
            size=image.shape[:2],
            m1type=0
        )

    rectified_frame = cv2.remap(src=image, map1=map1, map2=map2, interpolation=cv2.INTER_LINEAR)

    return rectified_frame

def createDepthMap(imgL, imgR, params):
    print 'creation of the depth map'

    min_disp = params['min_disp']
    window_size = 11
    stereo = cv2.StereoSGBM\
        (
            minDisparity=min_disp,
            numDisparities=params['max_disp'] - min_disp,
            SADWindowSize=window_size,
            uniquenessRatio=10,
            speckleWindowSize=100,
            speckleRange=1,
            disp12MaxDiff=1,
            P1=8*3*(window_size**2),
            P2=32*3*(window_size**2),
            fullDP=False
         )

    depth_map = stereo.compute(imgL, imgR).astype(np.float32) / 16.0

    return depth_map