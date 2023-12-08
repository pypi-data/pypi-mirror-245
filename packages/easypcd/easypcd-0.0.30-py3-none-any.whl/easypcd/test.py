from easypcd import ep
import numpy as np
ep = ep()
points_xyz = np.random.randint(100, size=(100, 3))  # 点云坐标
points_color = np.random.randint(255, size=(100, 3))  # 点云颜色
points_nxyz = np.random.randint(100, size=(100, 3))  # 点云向量
ep_points = np.concatenate((points_xyz, points_color, points_nxyz), axis=1)  # 拼接位置信息和颜色信息
ep.write_pcd(save_name="ep-points.pcd", points=ep_points, color=True, normal=True)  # 写入pcd