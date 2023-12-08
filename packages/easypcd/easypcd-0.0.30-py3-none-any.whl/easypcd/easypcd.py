# -*- coding: UTF-8 -*-
'''
@Project ：easypcd
@File    ：easypcd.py
@Author  ：王泽辉
@Date    ：2023-12-08 15:49
'''
import numpy as np


class DotDict(dict):
    def __init__(self, *args, **kwargs):
        super(DotDict, self).__init__(*args, **kwargs)

    def __getattr__(self, key):
        value = self[key]
        if isinstance(value, dict):
            value = DotDict(value)
        return value


class ep():
    def __init__(self):
        self.format_dic = {0: 'pcd', 1: "txt"}
        self.pcd_head = '# .PCD v0.7 - Point Cloud Data file format'
        self.VERSION = 'VERSION 0.7'

    def processing_str(self, input, s, length):
        """功能：输入一个字符、将其增加到length长度"""
        for i in range(length):
            input += " "
            input += str(s)
        return input

    def read_pcd(self, pcd_file):
        """功能：读取pcd文件
        pcd_file：输入读取pcd文件的路径
        """
        format_type = {"I": np.int32, "U": np.uint, "F": np.float32}
        pcd_data = []
        pcd_information = {}
        with open(pcd_file, 'r') as f:
            lines = f.readlines()
            for i in lines[1:11]:
                info = list(i.strip('\n').split(' '))
                if len(info) > 2:
                    info_line = [info[0], ' '.join(info[1:])]
                else:
                    info_line = info
                pcd_information.update({info_line[0]: info_line[1]})
            pcd_type = pcd_information['TYPE'].split(" ")
            for line in lines[11:]:
                line = list(line.strip('\n').split(' '))
                if line == ['']:
                    pass
                else:
                    tmp = []
                    for i in range(len(line)):
                        tmp.append(format_type[pcd_type[i]](line[i]))
                    pcd_data.append(tmp)
            points = np.array(pcd_data)

            pcd_information.update({"points": points})
        return DotDict(pcd_information)

    def contract_point_list(self, point_list):
        """
        将如下的数组进行拼接
        [array([[-710.34927002, -237.10757877,  215.2757621 ],
                [-709.46899019, -236.99056383,  214.81596639]]),
        array([[-708.6379193 , -238.05448845,  219.71073159],
               [-706.88288009, -237.81858778,  218.7811006 ]]),
        array([[-707.06327968, -239.84758949,  222.8262728 ],
               [-706.18809347, -239.72758696,  222.35760756]])]
        返回：
        [array(
                [-710.34927002, -237.10757877,  215.2757621 ],
                [-709.46899019, -236.99056383,  214.81596639],
                [-708.6379193 , -238.05448845,  219.71073159],
                [-706.88288009, -237.81858778,  218.7811006 ],
                [-707.06327968, -239.84758949,  222.8262728 ],
                [-706.18809347, -239.72758696,  222.35760756]
                )]
        """
        points_tmp = point_list[0]
        for i in range(1, len(point_list)):
            points_tmp = np.concatenate((points_tmp, point_list[i]), axis=0)
        return points_tmp

    def write_pcd(self, save_name, points, color=False, normal=False, _SIZE=4,
                  _TYPE="F", _COUNT=1, _HEIGHT=1, _VIEWPOINT='0 0 0 1 0 0 0', _DATA='ascii'):
        """功能：写入pcd文件
            必要参数：
                save_name:保存的文件名
                points：需要保存的点云数据

            可选参数
                color：是否有颜色信息（True/False），默认False
                normal：是否有向量信息（True/False），默认False
                _SIZE：字节数量，默认为4
                _TYPE：字符类型，默认为F
                _DATA：编码格式
        """
        if color == True and normal == False:
            length = 4
            TYPE = self.processing_str("TYPE", _TYPE, length - 1) + ' U'
            FIELDS = "FIELDS x y z rgb"
            points = self.encode_rgb(length, points)

        if color == False and normal == False:
            length = 3
            TYPE = self.processing_str("TYPE", _TYPE, length)
            FIELDS = "FIELDS x y z"
        if color == False and normal == True:
            length = 6
            TYPE = self.processing_str("TYPE", _TYPE, length)
            FIELDS = "FIELDS x y z nx ny nz"
        if color == True and normal == True:
            length = 7
            TYPE = self.processing_str("TYPE", _TYPE, length - 4) + " U" + self.processing_str("", _TYPE,
                                                                                               length - 4)
            FIELDS = "FIELDS x y z rgb nx ny nz"
            points = self.encode_rgb(length, points)
        pcd_init = {
            "pcd_head": self.pcd_head,
            "VERSION": self.VERSION,
            "FIELDS": FIELDS,
            "SIZE": self.processing_str("SIZE", _SIZE, length),
            "TYPE": TYPE,
            "COUNT": self.processing_str("COUNT", _COUNT, length),
            "WIDTH": "WIDTH " + str(len(points)),
            "HEIGHT": 'HEIGHT ' + str(_HEIGHT),
            "VIEWPOINT": 'VIEWPOINT ' + str(_VIEWPOINT),
            "POINTS": "POINTS " + str(len(points)),
            "DATA": 'DATA ' + str(_DATA)
        }
        try:
            with open(save_name, mode='w') as f:
                for i in pcd_init:
                    f.write(pcd_init[i] + '\n')
                np.savetxt(f, points, delimiter=' ', fmt='%.8e')
            # if isinstance(data, list):
            #     if points.ndim == 3:
            #         for i in pcd_init:
            #             f.write(pcd_init[i] + '\n')
            #         points_tmp = points[0, :, :]
            #         for i in range(1, points.shape[0]):
            #             points_tmp.concatenate(points[i, :, :], axis=0)
            #         np.savetxt(f, points, delimiter=' ', fmt='%d')

        except:
            assert "一个未知的错误！"

    def write_txt(self, save_name, points):
        """功能：写入txt文件
            save_name:保存的文件名
            points：需要保存的点云数据
        """
        with open(save_name, mode='w') as f:
            for line in points:
                for p in line:
                    p = str(int(p))
                    f.write(p)
                    f.write(" ")
                f.write("\n")

    def encode_rgb(self, length, points):
        # rgb编码
        xyz = points[:, :3]  # 位置
        color = points[:, 3:6]  # 颜色
        color_tmp = []
        for i in range(color.shape[0]):
            color_tmp.append([int(color[i, 0]) << 16 | int(color[i, 1]) << 8 | int(color[i, 2])])  # 颜色重新编码
        if length == 4:
            ep_points = np.concatenate((xyz, np.asarray(color_tmp)), axis=1)  # 拼接位置信息和颜色信息

        if length == 7:
            nxyz = points[:, 6:]
            ep_points = np.concatenate((xyz, np.asarray(color_tmp), nxyz), axis=1)  # 拼接位置信息和颜色信息
        return ep_points

    def decode_rgb(self, rgb):
        r = (rgb >> 16) & 0x0000ff
        g = (rgb >> 8) & 0x0000ff
        b = (rgb) & 0x0000ff
        return [r, g, b]
