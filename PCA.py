#This part is mainly finished by Ma Zhuoyuan.
import open3d as o3d
import numpy as np
from pyntcloud import PyntCloud

def PCA(data, correlation=False, sort=True):
    data_mean = np.mean(data, axis=0)
    data = data - data_mean
    H = np.dot(data.T, data)
    eigenvectors, eigenvalues, eigenvectors_t = np.linalg.svd(H)
    if sort:
        sort = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[sort]
        eigenvectors = eigenvectors[:, sort]
    return eigenvalues, eigenvectors, data_mean


def main():
    point_cloud_pynt = PyntCloud.from_file("C:/Users/jdy/Documents/GitHub/StandTheGrapefruit/Femto/models/test_gemini/after3.ply")
    point_cloud_o3d = point_cloud_pynt.to_instance("open3d", mesh=False)
    o3d.visualization.draw_geometries([point_cloud_o3d],width=800,height=600)  # 显示原始点云
    points = point_cloud_pynt.points
    print('total points number is:', points.shape[0])
    size = points.shape[0]
    w, u, p= PCA(points)
    point_cloud_vector = u[:, 0]
    print('the main orientation of this pointcloud is: ', point_cloud_vector, 'and', w[0])
    print('the second orientation of this pointcloud is:', u[:, 1])
    print('the third orientation of this pointcloud is:', u[:, 2])
    # o3d.visualization.draw_geometries([point_cloud_o3d,point_cloud_vector], width=800, height=600)

    # # 循环计算每个点的法向量
    # pcd_tree = o3d.geometry.KDTreeFlann(point_cloud_o3d)
    # normals = []
    #
    # # 1.选取一个点,搜索１０个邻近点
    # for i in range(size):
    #     [_, idx, _] = pcd_tree.search_knn_vector_3d(point_cloud_o3d.points[i], 10)
    #     k_nearest_point = np.asarray(point_cloud_o3d.points)[idx, :]  # 按照ｉｄｘ取出k个近邻点
    #     # 2.选取改点的一个邻域，计算该邻域内的点的PCA
    #     u_1, v_1 = PCA(k_nearest_point)
    #
    #     # 3.选取出特征值最小对应的特征向量作为法向量方向
    #     normals.append(v_1[:, 2])
    #
    # normals = np.array(normals, dtype=np.float64)


if __name__ == '__main__':
    main()

