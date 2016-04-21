from Camera import *
from StereoPair import *
from PointsCloud import *

folder, image_extension, camera_extension, projection_matrix_extension = 'herzjesu_dense/', '.png', '.camera', '.P'

def main():
    try:
        image_1 = cv2.imread(filename=folder+'0001'+image_extension)
        image_2 = cv2.imread(filename=folder+'0002'+image_extension)
        image_3 = cv2.imread(filename=folder+'0003'+image_extension)
        image_4 = cv2.imread(filename=folder+'0004'+image_extension) # it's the head frame
        image_5 = cv2.imread(filename=folder+'0005'+image_extension)
        image_6 = cv2.imread(filename=folder+'0006'+image_extension)
        image_7 = cv2.imread(filename=folder+'0007'+image_extension)
    except cv2.error as error:
        print error.message

    try:
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
                1: (image_1, camera_1),
                2: (image_2, camera_2),
                3: (image_3, camera_3),
                4: (image_4, camera_4),
                5: (image_5, camera_5),
                6: (image_6, camera_6),
                7: (image_7, camera_7)
            }
        reconstruct(data)
    except RuntimeError as error:
        print error

def reconstruct(data):
    print 'PROCESSING OF THE FIRST PAIR'
    pair_1 = StereoPair\
        (
            pair_1=data[3],
            pair_2=data[4],
            params={'min_disp':608, 'max_disp':672}
        )
    pair_1.saveData(filename='work materials/pair_1/')
    points_cloud = pair_1.getPointsCloud(limits={'X':(-5,5), 'Y':(-5,5), 'Z':(10,13)})
    # points_cloud.writeToFile(filename='work materials/pair_1/out.ply')
    points_cloud = pair_1.transformPCtoMainCoordinateSystem(points_cloud)
    points_cloud.writeToFile(filename='work materials/pair_1/out.ply')

    print 'PROCESSING OF THE SECOND PAIR'
    pair_2 = StereoPair\
        (
            pair_1=data[4],
            pair_2=data[5],
            params={'min_disp':704, 'max_disp':832}
        )
    pair_2.saveData(filename='work materials/pair_2/')
    points_cloud = pair_2.getPointsCloud(limits={'X':(-11,0), 'Y':(-5,5), 'Z':(10,13)})
    # points_cloud.writeToFile(filename='work materials/pair_2/out.ply')
    points_cloud = pair_2.transformPCtoMainCoordinateSystem(points_cloud)
    points_cloud.writeToFile(filename='work materials/pair_2/out.ply')

if __name__ == "__main__":
    main()