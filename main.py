#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json, time, os


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
    vt += '\nvt ' + ux3 + ' ' + uy2
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
    
    vt = x * 13
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
    
    if m == True:
        f = '\nf ' + v1 + '/' + vt03 + ' ' + v2 + '/' + vt07 + ' ' + v3 + '/' + vt06 + ' ' + v4 + '/' + vt02
        f += '\nf ' + v5 + '/' + vt06 + ' ' + v8 + '/' + vt05 + ' ' + v7 + '/' + vt01 + ' ' + v6 + '/' + vt02
        f += '\nf ' + v1 + '/' + vt11 + ' ' + v5 + '/' + vt06 + ' ' + v6 + '/' + vt07 + ' ' + v2 + '/' + vt12
        f += '\nf ' + v2 + '/' + vt10 + ' ' + v6 + '/' + vt05 + ' ' + v7 + '/' + vt06 + ' ' + v3 + '/' + vt11
        f += '\nf ' + v3 + '/' + vt09 + ' ' + v7 + '/' + vt04 + ' ' + v8 + '/' + vt05 + ' ' + v4 + '/' + vt10
        f += '\nf ' + v5 + '/' + vt08 + ' ' + v1 + '/' + vt13 + ' ' + v4 + '/' + vt12 + ' ' + v8 + '/' + vt07
    else:
        f = '\nf ' + v1 + '/' + vt02 + ' ' + v2 + '/' + vt06 + ' ' + v3 + '/' + vt07 + ' ' + v4 + '/' + vt03
        f += '\nf ' + v5 + '/' + vt02 + ' ' + v8 + '/' + vt01 + ' ' + v7 + '/' + vt05 + ' ' + v6 + '/' + vt06
        f += '\nf ' + v1 + '/' + vt12 + ' ' + v5 + '/' + vt07 + ' ' + v6 + '/' + vt06 + ' ' + v2 + '/' + vt11
        f += '\nf ' + v2 + '/' + vt11 + ' ' + v6 + '/' + vt06 + ' ' + v7 + '/' + vt05 + ' ' + v3 + '/' + vt10
        f += '\nf ' + v3 + '/' + vt10 + ' ' + v7 + '/' + vt05 + ' ' + v8 + '/' + vt04 + ' ' + v4 + '/' + vt09
        f += '\nf ' + v5 + '/' + vt07 + ' ' + v1 + '/' + vt12 + ' ' + v4 + '/' + vt13 + ' ' + v8 + '/' + vt08
    
    return f


def a(egg):
    if '726' in egg or 'voxel' in egg or 'arcade' in egg:
        time.sleep(1)
        os.system('cls')
        time.sleep(1)
        print('WARNING - SPECIAL CODE DETECTED!!!')
        time.sleep(1.5)
        print('''
    00        00  
  0000        0000
  000000    000000
  0000000000000000
  00    0000    00
  0000  0000  0000
    000000000000  
    000000000000  
        0000      
''')
        time.sleep(1.5)
        print('Preparing to exit...')
        time.sleep(1)
        exit()


# loc = '/sdcard/Android/data/com.zyn.dwshbsq/files/'

print('''
MCJSON: Json2Obj (Python Edition)
Version: 1.1.1 (20190722)

注意事项: 
* 确保模型json文件路径与脚本路径相同
* 确保json与展开图同名
* 别输错了嗷
* 目前生成的obj导入后不能摆动作
* 贴图自己导 不用肝uv
* 不要试图抓虫子 出错别找我
''')
time.sleep(3)
print('请确认无误后按回车键继续......')
egg = input()
a(egg)

name = input('请输入json文件名 不许加拓展名嗷: ')
print('检测中......')

txv = ''
txvt = ''
txf = ''
x = 0
bpym = ''
bpyg = ''

if '.json' in name:
    fn = name
else:
    fn = name + '.json'
with open(fn, 'r') as f:
    tx = f.read()

json = json.loads(tx)
glist = list(dict.keys(json))
glen = len(glist)
if glen > 1:
    gname = '检测到 ' + str(glen) + ' 个模型!'
    for gni in glist:
        gname += '\n' + gni
    print(gname)
    gn = input('请输入模型名称: ')
else:
    gn = glist[0]

mode = input('''
请选择输出模式:

1 - 相对坐标 附赠blender脚本 (可摆动作)
其它字符 - 默认

''')
a(mode)

print('正在输出obj, 请稍候......')
geo = json[gn]
tw = geo.get('texturewidth', 64)
th = geo.get('textureheight', 64)
bones = geo['bones']

for bone in bones:
    bn = bone['name']
    print('正在处理: ' + bn)
    nr = bone.get('neverRender', False)
    if nr != True:
        f = ""
        if mode == '1':
            p = bone.get('pivot', [0, 0, 0])
            pa = bone.get('parent', None)
            bpym += "m('" + bn + "', " + str(p[0]) + ", " + str(p[1]) + ", " + str(p[2]) + ")\n"
            if pa != None:
                bpyg += "g('" + bn + "', '" + pa + "')\n"
        else:
            p = [0, 0, 0]
        m = bone.get('mirror', False)
        cubes = bone['cubes']
        for cube in cubes:
            o = cube['origin']
            s = cube['size']
            u = cube['uv']
            i = cube.get('inflate', 0)
            txv += obj_v(p, o, s, i)
            txvt += obj_vt(s, u, tw, th)
            f += obj_f(m, x)
            x += 1
        txf += "\n\ng " + bn + f

obj = txv + '\n' + txvt + txf
output = '''# Made with MCJSON: Json2Obj (Python Edition) by F_Qilin.
# Model Name: ''' + gn + '''

mtllib ''' + name + '''.mtl
o _''' + gn + '''_
usemtl Skin
''' + obj + '''

# END'''
mtl = '''Wavefront OBJ material file
# Made with MCJSON: Json2Obj (Python Edition) by F_Qilin.

newmtl Skin
Kd 1 1 1
Ks 0 0 0
interpolateMode NEAREST_MAGNIFICATION_TRILINEAR_MIPMAP_MINIFICATION
map_Kd ''' + name + '''.png
map_d ''' + name + '''.png

# END'''
if mode == '1':
    bpy = '''# Made with MCJSON by F_Qilin.
# Fix the model of *.obj file
# Only for Blender
# Verson 0.1.1
# Model Name: ''' + gn + '''


import bpy

from bpy import data as d
from bpy import context as c
from bpy import ops as o

from mathutils import *
from math import *


def m(bone, px, pz, py):
    d.objects[bone].location[0] = float(px)/16
    d.objects[bone].location[1] = float(py)/16
    d.objects[bone].location[2] = float(pz)/16


def cg(gn):
    o.object.empty_add(type='PLAIN_AXES', radius=2, location=(0, 0, 0))
    c.object.name = gn


def g(bone, gn):
    d.objects[bone].parent = d.objects[gn]


# 以上为核心代码, 勿动
# 以下为模型修改代码, 根据json文件生成


''' + "cg('" + gn + "')\n\n" + bpym + "\n" + bpyg
    with open(name + '_bpy.py', 'w') as f:
        f.write(bpy)

with open(name + '.obj', 'w') as f:
    f.write(output)
with open(name + '.mtl', 'w') as f:
    f.write(mtl)

print('输出成功! 即将自动关闭......')
time.sleep(2)
exit()
