import numpy as np

ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

class PointsCloud:
    def __init__(self, points=None, colors=None):
        if points is None and colors is None:
            self.points, self.colors = [], []
        else:
            self.points = points
            self.colors = colors

    def size(self):
        return len(self.points)

    def append(self, set):
        (self.points).append(set[0])
        (self.colors).append(set[1])

    def makeBoundingBox(self, limits):
        print 'making of the bounding box'

        points_cloud = PointsCloud()

        for i in range(self.size()):
            point, color = self.points[i], self.colors[i]

            if point[0] > limits['X'][0] and point[0] < limits['X'][1] and \
               point[1] > limits['Y'][0] and point[1] < limits['Y'][1] and \
               point[2] > limits['Z'][0] and point[2] < limits['Z'][1]:
                points_cloud.append(set=(point, color))

        return points_cloud

    def writeToFile(self, filename):
        print "writing into '.ply' file"

        self.points = np.array(self.points, dtype=np.float32)
        self.colors = np.array(self.colors, dtype=np.float32)

        verts = (self.points).reshape(-1, 3)
        colors = (self.colors).reshape(-1, 3)
        verts = np.hstack([verts, colors])

        with open(filename, 'w') as f:
            f.write(ply_header % dict(vert_num=len(verts)))
            np.savetxt(f, verts, '%f %f %f %d %d %d')