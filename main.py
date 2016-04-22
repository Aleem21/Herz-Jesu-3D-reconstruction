from Camera import *
from StereoPair import *
from PointsCloud import *

folder, image_extension, camera_extension, projection_matrix_extension = 'herzjesu_dense/', '.png', '.camera', '.P'

def main():
    try:
        image_0 = cv2.imread(filename=folder+'0000'+image_extension)
        image_1 = cv2.imread(filename=folder+'0001'+image_extension)
        image_2 = cv2.imread(filename=folder+'0002'+image_extension)
        image_3 = cv2.imread(filename=folder+'0003'+image_extension)
        image_4 = cv2.imread(filename=folder+'0004'+image_extension)
        image_5 = cv2.imread(filename=folder+'0005'+image_extension)
        image_6 = cv2.imread(filename=folder+'0006'+image_extension)
        image_7 = cv2.imread(filename=folder+'0007'+image_extension)
    except cv2.error as error:
        print error.message

    try:
        camera_0 = Camera(filename='0000')
        camera_1 = Camera(filename='0001')
        camera_2 = Camera(filename='0002')
        camera_3 = Camera(filename='0003')
        camera_4 = Camera(filename='0004')
        camera_5 = Camera(filename='0005')
        camera_6 = Camera(filename='0006')
        camera_7 = Camera(filename='0007')
    except IOError as error:
        print error.strerror

    try:
        data = \
            {
                0: (image_0, camera_0),
                1: (image_1, camera_1),
                2: (image_2, camera_2),
                3: (image_3, camera_3),
                4: (image_4, camera_4),
                5: (image_5, camera_5),
                6: (image_6, camera_6),
                7: (image_7, camera_7)
            }

        # reconstruct(pair_1=data[0], pair_2=data[2], filename='pair_1',
        #             params={'min_disp':976, 'max_disp':1264},
        #             limits={'X':(0,10), 'Y':(-5,3), 'Z':(5,15)})

        reconstruct(pair_1=data[1], pair_2=data[2], filename='pair_2',
                    params={'min_disp':864, 'max_disp':1360},
                    limits={'X':(-10,0), 'Y':(-3,3), 'Z':(5,10)})
        #
        # reconstruct(pair_1=data[2], pair_2=data[3], filename='pair_3',
        #             params={'min_disp':544, 'max_disp':768},
        #             limits={'X':(-50,50), 'Y':(-50,50), 'Z':(-50,50)})
        #
        # reconstruct(pair_1=data[2], pair_2=data[4], filename='pair_4',
        #             params={'min_disp':480, 'max_disp':1184},
        #             limits={'X':(-50,50), 'Y':(-50,50), 'Z':(-50,50)})

        # reconstruct(pair_1=data[3], pair_2=data[4], filename='pair_5',
        #             params={'min_disp':608, 'max_disp':672},
        #             limits={'X':(-5,5), 'Y':(-5,5), 'Z':(10,13)})

        # reconstruct(pair_1=data[3], pair_2=data[5], filename='pair_6',
        #             params={'min_disp':1152, 'max_disp':1408},
        #             limits={'X':(-50,50), 'Y':(-50,50), 'Z':(-50,50)})

        # reconstruct(pair_1=data[4], pair_2=data[5], filename='pair_7',
        #             params={'min_disp':704, 'max_disp':832},
        #             limits={'X':(-11,0), 'Y':(-5,5), 'Z':(10,13)})

        # reconstruct(pair_1=data[5], pair_2=data[6], filename='pair_8',
        #             params={'min_disp':496, 'max_disp':720},
        #             limits={'X':(-50,50), 'Y':(-50,50), 'Z':(-50,50)})
        #
        # reconstruct(pair_1=data[5], pair_2=data[7], filename='pair_9',
        #             params={'min_disp':1008, 'max_disp':1424},
        #             limits={'X':(-50,50), 'Y':(-50,50), 'Z':(-50,50)})
        #
        # reconstruct(pair_1=data[6], pair_2=data[7], filename='pair_10',
        #             params={'min_disp':544, 'max_disp':704},
        #             limits={'X':(-50,50), 'Y':(-50,50), 'Z':(-50,50)})

    except RuntimeError as error:
        print error

def reconstruct(pair_1, pair_2, filename, params, limits):
    print 'PROCESSING OF THE '+filename

    stereo_pair = StereoPair\
        (
            pair_1=pair_1,
            pair_2=pair_2,
            params=params
        )
    stereo_pair.saveData(filename='work materials/'+filename+'/')
    points_cloud = stereo_pair.getPointsCloud(limits=limits)
    # points_cloud.writeToFile(filename='work materials/'+filename+'/out.ply')
    points_cloud = stereo_pair.transformPCtoMainCoordinateSystem(points_cloud)
    points_cloud.writeToFile(filename='work materials/'+filename+'/out.ply')

if __name__ == "__main__":
    main()