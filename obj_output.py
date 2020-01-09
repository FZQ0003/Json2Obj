# -*-coding: utf-8 -*-

from PIL import Image


def obj_v(p, o, s, i):
    ox = (o[0] - p[0] - i) / 16
    oy = (o[1] - p[1] - i) / 16
    oz = (p[2] - o[2] + i) / 16
    sx = str(round(s[0] / 16 + ox + i / 8, 6))
    sy = str(round(s[1] / 16 + oy + i / 8, 6))
    sz = str(round(oz - s[2] / 16 - i / 8, 6))
    ox = str(round(ox, 6))
    oy = str(round(oy, 6))
    oz = str(round(oz, 6))

    v = '\nv ' + sx + ' ' + oy + ' ' + sz
    v += '\nv ' + sx + ' ' + oy + ' ' + oz
    v += '\nv ' + ox + ' ' + oy + ' ' + oz
    v += '\nv ' + ox + ' ' + oy + ' ' + sz
    v += '\nv ' + sx + ' ' + sy + ' ' + sz
    v += '\nv ' + sx + ' ' + sy + ' ' + oz
    v += '\nv ' + ox + ' ' + sy + ' ' + oz
    v += '\nv ' + ox + ' ' + sy + ' ' + sz

    return v


def obj_vt(s, u, tw, th):
    ux0 = u[0] / tw
    ux1 = s[2] / tw + ux0
    ux2 = s[0] / tw + ux1
    ux3 = s[2] / tw + ux2
    ux5 = str(s[0] / tw + ux2)  # v1.2 - Bug Fixed
    ux4 = str(round(s[0] / tw + ux3, 6))
    ux3 = str(round(ux3, 6))
    ux2 = str(round(ux2, 6))
    ux1 = str(round(ux1, 6))
    ux0 = str(round(ux0, 6))

    uy2 = 1 - u[1] / th
    uy1 = uy2 - s[2] / th
    uy0 = str(round(uy1 - s[1] / th, 6))
    uy1 = str(round(uy1, 6))
    uy2 = str(round(uy2, 6))

    vt = '\nvt ' + ux1 + ' ' + uy2
    vt += '\nvt ' + ux2 + ' ' + uy2
    vt += '\nvt ' + ux5 + ' ' + uy2  # v1.2 - Bug Fixed
    vt += '\nvt ' + ux0 + ' ' + uy1
    vt += '\nvt ' + ux1 + ' ' + uy1
    vt += '\nvt ' + ux2 + ' ' + uy1
    vt += '\nvt ' + ux3 + ' ' + uy1
    vt += '\nvt ' + ux4 + ' ' + uy1
    vt += '\nvt ' + ux0 + ' ' + uy0
    vt += '\nvt ' + ux1 + ' ' + uy0
    vt += '\nvt ' + ux2 + ' ' + uy0
    vt += '\nvt ' + ux3 + ' ' + uy0
    vt += '\nvt ' + ux4 + ' ' + uy0
    vt += '\nvt ' + ux5 + ' ' + uy1  # v1.2 - Bug Fixed

    return vt


def obj_f(m, x):
    v = x * 8
    v1 = str(v + 1)
    v2 = str(v + 2)
    v3 = str(v + 3)
    v4 = str(v + 4)
    v5 = str(v + 5)
    v6 = str(v + 6)
    v7 = str(v + 7)
    v8 = str(v + 8)

    vt = x * 14
    vt01 = str(vt + 1)
    vt02 = str(vt + 2)
    vt03 = str(vt + 3)
    vt04 = str(vt + 4)
    vt05 = str(vt + 5)
    vt06 = str(vt + 6)
    vt07 = str(vt + 7)
    vt08 = str(vt + 8)
    vt09 = str(vt + 9)
    vt10 = str(vt + 10)
    vt11 = str(vt + 11)
    vt12 = str(vt + 12)
    vt13 = str(vt + 13)
    vt14 = str(vt + 14)  # v1.2 - Bug Fixed

    # v1.3 - Bug Fixed (Turn [v1, v2, v3, v4] into [v3, v4, v1, v2], in line 1)
    # v1.3 - Bug Fixed (Exchange [vt**] from line 3 with line 5, if m is True)
    if m is True:
        f = '\nf ' + v3 + '/' + vt03 + ' ' + v4 + '/' + vt14 + ' ' + v1 + '/' + vt06 + ' ' + v2 + '/' + vt02
        f += '\nf ' + v5 + '/' + vt06 + ' ' + v8 + '/' + vt05 + ' ' + v7 + '/' + vt01 + ' ' + v6 + '/' + vt02
        f += '\nf ' + v1 + '/' + vt09 + ' ' + v5 + '/' + vt04 + ' ' + v6 + '/' + vt05 + ' ' + v2 + '/' + vt10
        f += '\nf ' + v2 + '/' + vt10 + ' ' + v6 + '/' + vt05 + ' ' + v7 + '/' + vt06 + ' ' + v3 + '/' + vt11
        f += '\nf ' + v3 + '/' + vt11 + ' ' + v7 + '/' + vt06 + ' ' + v8 + '/' + vt07 + ' ' + v4 + '/' + vt12
        f += '\nf ' + v5 + '/' + vt08 + ' ' + v1 + '/' + vt13 + ' ' + v4 + '/' + vt12 + ' ' + v8 + '/' + vt07
    else:
        f = '\nf ' + v3 + '/' + vt02 + ' ' + v4 + '/' + vt06 + ' ' + v1 + '/' + vt14 + ' ' + v2 + '/' + vt03
        f += '\nf ' + v5 + '/' + vt02 + ' ' + v8 + '/' + vt01 + ' ' + v7 + '/' + vt05 + ' ' + v6 + '/' + vt06
        f += '\nf ' + v1 + '/' + vt12 + ' ' + v5 + '/' + vt07 + ' ' + v6 + '/' + vt06 + ' ' + v2 + '/' + vt11
        f += '\nf ' + v2 + '/' + vt11 + ' ' + v6 + '/' + vt06 + ' ' + v7 + '/' + vt05 + ' ' + v3 + '/' + vt10
        f += '\nf ' + v3 + '/' + vt10 + ' ' + v7 + '/' + vt05 + ' ' + v8 + '/' + vt04 + ' ' + v4 + '/' + vt09
        f += '\nf ' + v5 + '/' + vt07 + ' ' + v1 + '/' + vt12 + ' ' + v4 + '/' + vt13 + ' ' + v8 + '/' + vt08

    return f


class B:

    def __init__(self, texturewidth=64, textureheight=64, pic=None):
        """
        Json2Obj 核心算法 ver.2

        :param texturewidth: Texture Width
        :param textureheight: Texture Height
        :param pic: Pic
        """

        self.p = [0, 0, 0]
        self.o = [-4, -4, -4]
        self.s = [8, 8, 8]
        self.u = [0, 0]
        self.inf = 0.0
        self.mir = False
        self.tw = texturewidth
        self.th = textureheight
        self.pic = pic

        self.tx_v = ''
        self.tx_vt = ''
        self.tx_f = ''
        self.vs = 0
        self.vts = 0

        self.__f_vt = 0
        self.__f_v = []
        self.__v_list = []
        self.__vt_list = []
        self.__pic = pic.copy()
        self.__pix = self.__pic.convert('LA').load()

    def cal_i(self, v):
        """
        计算由inflate影响的顶点位置
            v: 位置

        :return: v参数序号
        """

        tmp = '\nv'
        for _ in range(3):
            tmp_v = (v[_] * (self.s[_] + 2 * self.inf) / self.s[_] - self.inf + self.o[_]) / 16
            if _ == 2:
                tmp += ' ' + str(round(0 - tmp_v, 6))
            else:
                tmp += ' ' + str(round(tmp_v, 6))
        self.vs += 1
        self.tx_v += tmp
        return str(self.vs)

    def cal_i2(self):
        """
        补全挤压面f参数

        :return: f参数
        """

        if self.inf > 0:
            f_list = [
                [7, 6, 2, 3],
                [0, 4, 7, 3],
                [0, 1, 5, 4],
                [5, 1, 2, 6]
            ]
            tmp = ''
            for __ in f_list:
                tmp += '\nf'
                for _ in range(4):
                    if int(__[_] / 4):
                        tmp += ' ' + str(self.vs + __[_] % 4 - 3)
                    else:
                        tmp += ' ' + str(self.__f_v[__[_]])
                    tmp += '/' + str(self.__f_vt + __[_] % 4 - 3)
            return tmp
        else:
            return ''

    def cal_vt(self, x, y):
        """
        计算贴图顶点位置
            x, y: 坐标

        :return: vt参数
        """

        x = round((self.u[0] + x) / self.tw, 6)
        y = round((self.th - y - self.u[1]) / self.th, 6)
        return '\nvt ' + str(x) + ' ' + str(y)

    def cal_f(self, a, b, ux, uy, mode):
        """
        计算f参数, 将面与对应贴图一一对应
            a, b: 顶点位置数据
            ux, uy: uv坐标
            mode: 模式列表, 前三位确定双方向, 后一位确定计算顺序

        :return: f参数
        """

        self.__f_vt = self.__vt_list[ux][uy] * 4
        self.__f_v = [0, 0, 0, 0]
        if self.__f_vt == 0:
            return ''
        else:
            tmp = '\nf'
            tmp += self.cal_f2(a, b, mode, [0, 0, -3])
            tmp += self.cal_f2(a, b, mode, [1, 0, -2])
            tmp += self.cal_f2(a, b, mode, [1, 1, -1])
            tmp += self.cal_f2(a, b, mode, [0, 1, 0])
            tmp += self.cal_i2()
            return tmp

    def cal_f2(self, a, b, li, ty):
        """
        将两个数据按顺序写入并替换列表中的-1元素, 然后输出参数
            a, b: 数据
            li: 四元素列表, 前三位控制写入位置, 第四位控制偏移方向
            ty: 三元素列表, 前两位数据偏移量, 后一位计数

        :return: f参数单项数据
        """

        if li[3] == 1:
            ty[li == [-1, 0, -1, 1]] *= -1
        if li[1] == -1 and li[2] == -1:
            a += ty[1]
            b += ty[0]
        else:
            a += ty[0]
            b += ty[1]
        v = [0, 0, 0]
        tmp_li = [a, b]
        __ = 0
        for _ in range(3):
            if li[_] == -1 and __ < 2:
                v[_] = tmp_li[__]
                __ += 1
            else:
                v[_] = li[_]
        self.__f_v[ty[2] + 3] = self.__v_list[v[0]][v[1]][v[2]]
        if self.inf > 0:
            return ' ' + self.cal_i(v) + '/' + str(self.__f_vt + ty[2])
        else:
            return ' ' + str(self.__f_v[ty[2] + 3]) + '/' + str(self.__f_vt + ty[2])

    def cal_m(self, x=-1, y=-1):
        """
        计算受mirror参数影响的X坐标
            x, y: 贴图坐标

        :return: X坐标
        """
        tmp_x = self.s[0] + 2 * self.s[2]
        if x == -1 or y == -1:
            mir_list = [
                [self.s[2], 0, self.s[0], self.s[2]],
                [self.s[0] + self.s[2], 0, self.s[0], self.s[2]],
                [0, self.s[2], tmp_x, self.s[1]],
                [tmp_x, self.s[2], self.s[0], self.s[1]]
            ]
            for _ in mir_list:
                _[0] += self.u[0]
                _[1] += self.u[1]
                _[2] += _[0]
                _[3] += _[1]
                size = tuple(_)
                self.__pic.paste(self.__pic.crop(size).transpose(Image.FLIP_LEFT_RIGHT), size)
            return self.__pic
        else:
            if x >= tmp_x and y >= self.s[2]:
                x = tmp_x * 2 + self.s[0] - x
            elif x >= self.s[0] + self.s[2] and y < self.s[2]:
                x = tmp_x + 2 * self.s[0] - x
            else:
                x = tmp_x - x
            return x - 1

    def main(self):
        """
        主函数, 计算相关数据

        :return: 单方块obj文件
        """

        li_x = range(self.s[0] + 1)
        li_y = range(self.s[1] + 1)
        li_z = range(self.s[2] + 1)

        self.__v_list = [[[0] * (self.s[2] + 1) for _ in li_y] for _ in li_x]

        for i in li_x:
            for j in li_y:
                for k in li_z:
                    if (i % self.s[0]) * (j % self.s[1]) * (k % self.s[2]) == 0:
                        self.tx_v += '\nv ' \
                                     + str((self.o[0] + i) / 16) \
                                     + ' ' + str((self.o[1] + j) / 16) \
                                     + ' ' + str(-(self.o[2] + k) / 16)
                        self.vs += 1
                        self.__v_list[i][j][k] = self.vs

        li_ux = range(2 * (self.s[0] + self.s[2]))
        li_uy = range(self.s[1] + self.s[2])

        self.__vt_list = [[0] * (self.s[1] + self.s[2]) for _ in li_ux]

        for i in li_ux:
            if i < self.s[2] or i > 2 * self.s[0] + self.s[2]:
                li_uy2 = range(self.s[2], self.s[1] + self.s[2])
            else:
                li_uy2 = li_uy
            for j in li_uy2:
                if self.__pix[i + self.u[0], j + self.u[1]][1] > 0:
                    if self.mir:
                        _i = self.cal_m(i, j)
                        self.tx_vt += self.cal_vt(_i + 0.75, j + 0.75)
                        self.tx_vt += self.cal_vt(_i + 0.25, j + 0.75)
                        self.tx_vt += self.cal_vt(_i + 0.25, j + 0.25)
                        self.tx_vt += self.cal_vt(_i + 0.75, j + 0.25)
                    else:
                        self.tx_vt += self.cal_vt(i + 0.25, j + 0.75)
                        self.tx_vt += self.cal_vt(i + 0.75, j + 0.75)
                        self.tx_vt += self.cal_vt(i + 0.75, j + 0.25)
                        self.tx_vt += self.cal_vt(i + 0.25, j + 0.25)
                    self.vts += 1
                    self.__vt_list[i][j] = self.vts

        li_x = range(self.s[0])
        li_y = range(self.s[1])
        li_z = range(self.s[2])

        for i in li_x:
            for j in li_y:
                self.tx_f += self.cal_f(i, j,
                                        i + self.s[2],
                                        self.s[1] + self.s[2] - j - 1,
                                        [-1, -1, 0, 0])
                self.tx_f += self.cal_f(self.s[0] - i, j,
                                        i + self.s[0] + 2 * self.s[2],
                                        self.s[1] + self.s[2] - j - 1,
                                        [-1, -1, self.s[2], 1])
        for j in li_y:
            for k in li_z:
                self.tx_f += self.cal_f(j, k,
                                        k + self.s[0] + self.s[2],
                                        self.s[1] + self.s[2] - j - 1,
                                        [self.s[0], -1, -1, 0])
                self.tx_f += self.cal_f(j, self.s[2] - k, k,
                                        self.s[1] + self.s[2] - j - 1,
                                        [0, -1, -1, 1])
        for i in li_x:
            for k in li_z:
                self.tx_f += self.cal_f(i, k, i + self.s[2],
                                        self.s[2] - k - 1,
                                        [-1, self.s[1], -1, 0])
                self.tx_f += self.cal_f(i, self.s[2] - k,
                                        i + self.s[0] + self.s[2],
                                        self.s[2] - k - 1,
                                        [-1, 0, -1, 1])

        return self.tx_v + '\n' + self.tx_vt + '\n' + self.tx_f

    def input(self, origin, size, uv, inflate=0.0):
        """
        输入相关参数

        :param origin: Origin
        :param size: Size
        :param uv: UV
        :param inflate: Inflate
        """

        self.o = origin
        self.s = size
        self.u = uv
        self.inf = inflate
        for _ in range(3):
            self.o[_] -= self.p[_]
        self.__pic = self.pic.copy()
        if self.mir:
            self.cal_m(-1, -1)
        self.__pix = self.__pic.convert('LA').load()

    def reset(self, bone, pivot=None, mirror=False):
        """
        重置Bone, 并进行部件分割

        :param bone: Bone Name
        :param pivot: Pivot
        :param mirror: Mirror
        """
        if pivot is None:
            self.p = [0, 0, 0]
        else:
            self.p = pivot
        self.mir = mirror
        self.tx_f += '\ng ' + bone

    def print(self):
        return self.tx_v + '\n' + self.tx_vt + '\n' + self.tx_f


'''
test = B()
test.reset('test_mir', mirror=True)
print(test.main())
'''
