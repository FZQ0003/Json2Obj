# -*-coding: utf-8 -*-

import base64
from icon import img
from tkinter import * # pylint: disable=unused-wildcard-import
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from winsound import Beep
import json, time, os


def calculate_relative_path(a, b):
    """
    计算相对路径:
        已知两个绝对路径 a 和 b, 求 b 相对于 a 的相对路径.

	注:
		1. a 和 b 来自于同一个盘符
		2. 路径分隔符用反斜杠 "\\"
    """
    
    a, b = a.split('\\'), b.split('\\')
    # a = 'D:/M/N/O/P/a.py' --> ['D:', 'M', 'N', 'O', 'P', 'a.py']
    # b = 'D:/M/N/Q/b.py' --> ['D:', 'M', 'N', 'Q', 'b.py']
    
    intersection = 0  # 交汇点位置
    
    for index in range(min(len(a), len(b))):
        m, n = a[index], b[index]
        if m != n:
            intersection = index  # --> 3
            break
    
    def backward():  # "溯流而上"
        return (len(a) - intersection - 1) * '../'
    	# (6 - 3 - 1) * '../' --> '../../'
    
    def forward():  # "顺流而下"
        return '/'.join(b[intersection:])
    	# ['D:', 'M', 'N', 'Q', 'b.py'] --> 'Q/b.py'
    
    out = backward() + forward()
    # '../../' + 'Q/b.py' --> '../../Q/b.py'
    return out

def openfile():
    global fn_png

    fn_json = filedialog.askopenfilename(title='选择模型文件', filetypes=[('JSON', '.json'), ('所有文件', '.*')])
    if ':/' in fn_json:
        fn_json = fn_json.replace('/', '\\')
    if fn_json != '' and fn_json != ():
        data_json.set(fn_json)
    else:
        return 0
    
    fn_png = filedialog.askopenfilename(title='选择贴图文件', filetypes=[('PNG', '.png'), ('TGA', '.tga'), ('所有文件', '.*')])
    if ':/' in fn_png:
        fn_png = fn_png.replace('/', '\\')
    if fn_png != '' and fn_png != ():
        data_png.set(fn_png)
        loadjson(fn_json)
        loadpng(fn_png)

def loadjson(fn):
    global json_d
    with open(fn, 'r') as f:
        tx = f.read()
    json_d = json.loads(tx)
    glist = [i for i in list(dict.keys(json_d)) if ':' not in i and 'format_version' not in i]
    data_list.set(glist)

def loadpng(fn):
    global png_d
    png_d = Image.open(fn)

def outputmode():
    if list_model.curselection() == ():
        messagebox.showwarning('提示', '请选择一个模型!')
        return
    filename = filedialog.asksaveasfilename(filetypes=[('Wavefront OBJ', '.obj')])
    if filename == '' or filename == ():
        return
    if ':/' in filename:
        filename = filename.replace('/', '\\')
    if '.obj' in filename:
        filename = filename.replace('.obj', '')
    mode = messagebox.askquestion('提示', '''请选择输出类型\n
  是 - 相对坐标 (可摆动作)
     - 附赠 blender(_bpy) & C4D(_cpy) 脚本
  否 - 默认''')
    configrecord('准备转换...\n\n', 1)
    convertmodel(mode, filename)

def configrecord(text, n):
    text_rec.config(state=NORMAL)
    if n == 1:
        text_rec.delete(1.0, END)
    text_rec.insert('end', text)
    text_rec.config(state=DISABLED)

def convertmodel(mode, name):
    global fn_png, json_d, png_d
    txv = ''
    txvt = ''
    txf = ''
    x = 0
    bpym = ''
    bpyg = ''
    cpy = ''
    gn = list_model.get(list_model.curselection())
    geo = json_d[gn]
    tw = geo.get('texturewidth', png_d.size[0])
    th = geo.get('textureheight', png_d.size[1])
    bones = geo['bones']

    for bone in bones:
        bn = bone['name']
        configrecord('正在处理: ' + bn + '\n', 0)
        nr = bone.get('neverRender', False)
        if nr != True:
            f = ""
            if mode == True or mode == 'yes':
                p = bone.get('pivot', [0, 0, 0])
                pa = bone.get('parent', None)
                bpym += "m('" + bn + "', " + str(p[0]) + ", " + str(p[1]) + ", " + str(p[2]) + ")\n"
                cpy += "    editobj('" + bn + "', " + str(p[0]) + ", " + str(p[1]) + ", " + str(p[2])
                if pa != None:
                    bpyg += "g('" + bn + "', '" + pa + "')\n"
                    cpy += ", '" + pa + "')\n"
                else:
                    cpy += ", None)\n"
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
    mtl_png_name = calculate_relative_path(name + '.obj', fn_png)
    output = '''# Made with MCJSON: Json2Obj (Python Edition) by F_Qilin.
# Model Name: ''' + gn + '''

mtllib ''' + os.path.basename(name) + '''.mtl
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
map_Kd ''' + mtl_png_name + '''
map_d ''' + mtl_png_name + '''

# END'''
    if mode == True or mode == 'yes':
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
        cpy = '''# Made with MCJSON by F_Qilin.
# Fix the model of *.obj file
# Only for Cimema 4D
# Verson 1.0
# Model Name: ''' + gn + '''


import c4d


def searchobj(objlist, name):
    for obj in objlist:
        if name in obj.GetName():
            return obj
    return None

def editobj(name, x, y, z, pa):
    global group, objs
    obj = searchobj(objs, name)
    if pa == None:
        pa = group
    else:
        pa = searchobj(objs, pa)
    obj.InsertUnder(pa)
    obj[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(float(x)/16, 
                                                     float(y)/16, 
                                                     float(z)/16)

def datainit(name):
    global group, objs
    objlist = doc.GetObjects()
    group = searchobj(objlist, name)
    if group == None:
        group = c4d.BaseObject(5140)
        group.SetName(name)
        doc.InsertObject(group)
        objs = objlist
    else:
        objs = group.GetChildren()
    group[c4d.NULLOBJECT_DISPLAY] = 9
    group[c4d.NULLOBJECT_RADIUS] = 2
    group[c4d.NULLOBJECT_ORIENTATION] = 3

def main():
    datainit(''' + "'" + os.path.basename(name) + "'" + ''')
    
''' + cpy + '''    
    c4d.EventAdd()

if __name__ == '__main__':
    main()
'''
        with open(name + '_bpy.py', 'w') as f:
            f.write(bpy)
        with open(name + '_cpy.py', 'w') as f:
            f.write(cpy)

    with open(name + '.obj', 'w') as f:
        f.write(output)
    with open(name + '.mtl', 'w') as f:
        f.write(mtl)

    configrecord('\n输出成功!', 0)
    os.system('start explorer ' + os.path.dirname(name + '.obj'))


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
    ux5 = str(s[0] / tw + ux2) # v1.2 - Bug Fixed
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
    vt += '\nvt ' + ux5 + ' ' + uy2 # v1.2 - Bug Fixed
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
    vt += '\nvt ' + ux5 + ' ' + uy1 # v1.2 - Bug Fixed
    
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
    vt14 = str(vt + 14) # v1.2 - Bug Fixed
    
    if m == True:
        f = '\nf ' + v1 + '/' + vt03 + ' ' + v2 + '/' + vt14 + ' ' + v3 + '/' + vt06 + ' ' + v4 + '/' + vt02
        f += '\nf ' + v5 + '/' + vt06 + ' ' + v8 + '/' + vt05 + ' ' + v7 + '/' + vt01 + ' ' + v6 + '/' + vt02
        f += '\nf ' + v1 + '/' + vt11 + ' ' + v5 + '/' + vt06 + ' ' + v6 + '/' + vt07 + ' ' + v2 + '/' + vt12
        f += '\nf ' + v2 + '/' + vt10 + ' ' + v6 + '/' + vt05 + ' ' + v7 + '/' + vt06 + ' ' + v3 + '/' + vt11
        f += '\nf ' + v3 + '/' + vt09 + ' ' + v7 + '/' + vt04 + ' ' + v8 + '/' + vt05 + ' ' + v4 + '/' + vt10
        f += '\nf ' + v5 + '/' + vt08 + ' ' + v1 + '/' + vt13 + ' ' + v4 + '/' + vt12 + ' ' + v8 + '/' + vt07
    else:
        f = '\nf ' + v1 + '/' + vt02 + ' ' + v2 + '/' + vt06 + ' ' + v3 + '/' + vt14 + ' ' + v4 + '/' + vt03
        f += '\nf ' + v5 + '/' + vt02 + ' ' + v8 + '/' + vt01 + ' ' + v7 + '/' + vt05 + ' ' + v6 + '/' + vt06
        f += '\nf ' + v1 + '/' + vt12 + ' ' + v5 + '/' + vt07 + ' ' + v6 + '/' + vt06 + ' ' + v2 + '/' + vt11
        f += '\nf ' + v2 + '/' + vt11 + ' ' + v6 + '/' + vt06 + ' ' + v7 + '/' + vt05 + ' ' + v3 + '/' + vt10
        f += '\nf ' + v3 + '/' + vt10 + ' ' + v7 + '/' + vt05 + ' ' + v8 + '/' + vt04 + ' ' + v4 + '/' + vt09
        f += '\nf ' + v5 + '/' + vt07 + ' ' + v1 + '/' + vt12 + ' ' + v4 + '/' + vt13 + ' ' + v8 + '/' + vt08
    
    return f

def a(egg):
    
    x1 = '''
    00        00  
  0000        0000
  000000    000000
  0000000000000000
  00    0000    00
  0000  0000  0000
    000000000000  
    000000000000  
        0000      
'''
    x2 = '''
\033[34m    00        00  
  0000        0000\n");
  0000\033[31m00    00\033[34m0000
  00\033[31m0000\033[34m0000\033[31m0000\033[34m00
  00    0000    00
  00\033[31m00\033[34m  0000  \033[31m00\033[34m00
    00\033[31m00\033[34m0000\033[31m00\033[34m00  
    00\033[31m00\033[34m0000\033[31m00\033[34m00  
        0000      
\033[0m'''
    x3 = '''
  00000000  00        00  00000000
  00                            00
  00          00000000          00
  00      0000  0000  0000      00
        0000            0000
  00    00    00    00    00    00
      00    000000000000    00
      0000      0000      0000
      0000  00  0000  00  0000
      00      00000000      00
  00    00  00  0000  00  00    00
        0000            0000
  00      0000  0000  0000      00
  00          00000000          00
  00                            00
  00000000  00        00  00000000

  0  0  00  000  00   00  000  000
  0  0 0  0 0 0 0  0 0  0 0  0 0
  0  0 0  0 00  0    0  0 0  0 00
   0 0 0000 0 0 0  0 0000 0  0 0
    0  0  0 0 0  00  0  0 000  000
'''
    x4 = '''
\033[34m  00000000  \033[31m00        00\033[34m  00000000
  00                            00
  00          00000000          00
  00      \033[31m0000\033[34m  0000  \033[31m0000\033[34m      00
\033[31m        0000            0000
  00    00    00    00    00    00
\033[34m      00    \033[31m0000\033[34m0000\033[31m0000\033[34m    00
      0000      0000      0000
      0000  \033[31m00\033[34m  0000  \033[31m00\033[34m  0000
      00      \033[31m00\033[34m0000\033[31m00\033[34m      00
\033[31m  00    00\033[34m  00  0000  00  \033[31m00    00
        0000            0000
\033[34m  00      \033[31m0000\033[34m  0000  \033[31m0000\033[34m      00
  00          00000000          00
  00                            00
  00000000  \033[31m00        00\033[34m  00000000
                                  
  0  0 \033[31m 00  000  00 \033[34m  00  000  000
  0  0 \033[31m0  0 0 0 0  0\033[34m 0  0 0  0 0
  0  0 \033[31m0  0 00  0   \033[34m 0  0 0  0 00
   0 0 \033[31m0000 0 0 0  0\033[34m 0000 0  0 0
    0  \033[31m0  0 0 0  00 \033[34m 0  0 000  000
\033[0m'''
    
    egg = str.lower(egg)
    if 'voxel' and 'arcade' in egg:
        time.sleep(0.5)
        os.system('cls')
        time.sleep(0.5)
        print("It seems that you've pressed the name of a studio.")
        time.sleep(2)
        print('"Voxel Arcade"... Nice.')
        time.sleep(1.5)
        print("Well, It's time to show you something.")
        time.sleep(2)
        print('Please wait...')
        b(x3)
    elif '726' in egg or 'voxel' in egg or 'arcade' in egg:
        time.sleep(1)
        os.system('cls')
        time.sleep(1)
        print('WARNING - SPECIAL CODE DETECTED!!!')
        time.sleep(1.5)
        print(x1)
        time.sleep(0.5)
        print('Preparing to exit...')
        time.sleep(1.5)
        exit()

def b(x):
    time.sleep(2.5)
    os.system('cls')
    
    Beep(523, 500)
    print("I think you've heard it many times.\n")
    Beep(932, 500)
    Beep(880, 1000)
    Beep(523, 500)
    Beep(932, 500)
    Beep(880, 1000)
    Beep(523, 500)
    print('We all have dreams, though there are tons of difficulties.\n')
    Beep(784, 1000)
    Beep(784, 500)
    Beep(698, 500)
    Beep(880, 1000)
    Beep(784, 500)
    
    Beep(523, 500)
    print("As we're chasing them...\n")
    Beep(932, 500)
    Beep(880, 1000)
    Beep(523, 500)
    Beep(932, 500)
    Beep(880, 1000)
    Beep(523, 500)
    print('WE')
    Beep(784, 1000)
    print('ARE')
    Beep(784, 500)
    
    print('ALL')
    Beep(698, 500)
    print('BECOMING')
    Beep(932, 500)
    print('STRONGER')
    Beep(1046, 500)
    print('AS WELL AS')
    Beep(880, 500)
    print('GROWING')
    Beep(784, 500)
    print('UP...\n')
    Beep(698, 3000)
    print('Yeah, something will never change.\n')
    Beep(659, 1000)
    Beep(784, 1000)
    Beep(784, 1000)
    Beep(698, 1000)
    
    print('Our hearts to...\n')
    Beep(932, 1500)
    Beep(880, 500)
    Beep(784, 1500)
    print('...CRAFT.\n')
    Beep(698, 500)
    Beep(698, 3000)
    
    os.system('cls')
    time.sleep(1.5)
    print(x)
    time.sleep(3)


ft = 'Microsoft YaHei'
abspath = os.path.abspath('.')
if ':\\' in abspath:
    abspath += '\\'
else:
    abspath += '/'
info = 'Made by F_Qilin (09/15/2019)'

root = Tk()
root.title('MCJSON: Json2Obj (Python Edition) v1.2')
root.resizable(False, False)

tmp = open("tmp.ico","wb+")
tmp.write(base64.b64decode(img))
tmp.close()
root.iconbitmap("tmp.ico")
root.iconbitmap('tmp.ico')
os.remove("tmp.ico")

frame_ctrl = Frame(root)
frame_ctrl.grid(padx=20, pady=20)
Label(frame_ctrl, text='请输入路径: ', font=(ft, 20)).grid(sticky=W)

frame_path = Frame(frame_ctrl)
frame_path.grid(sticky=W, pady=10)
Label(frame_path, text='模型 (JSON)', font=(ft, 10)).grid(sticky=W, padx=5)
Label(frame_path, text='贴图 (PNG)', font=(ft, 10)).grid(sticky=W, padx=5)
data_json = StringVar()
data_json.set(abspath)
data_png = StringVar()
data_png.set(abspath)
entry_json = Entry(frame_path, textvariable=data_json, width=50)
entry_json.grid(row=0, column=1, padx=5)
entry_png = Entry(frame_path, textvariable=data_png, width=50)
entry_png.grid(row=1, column=1, padx=5)
bu_search = Button(frame_ctrl, text='浏览...', width=10, height=2, command=openfile)
bu_search.grid(row=1, column=1, padx=10)

Label(frame_ctrl, text='可转换模型列表: ', font=(ft, 16)).grid(sticky=W)
data_list = StringVar()
list_model = Listbox(frame_ctrl, listvariable=data_list, width=62)
list_model.grid(pady=10)
bu_convert = Button(frame_ctrl, text='转换', width=10, height=10, command=outputmode)
bu_convert.grid(row=3, column=1)

frame_rec = Frame(root)
frame_rec.grid(sticky=NW, row=0, column=1, padx=30, pady=20)
Label(frame_rec, text='输出日志', font=(ft, 16)).grid(sticky=W)
text_rec = Text(frame_rec, width=24, height=22)
text_rec.config(state=DISABLED)
text_rec.grid(pady=15)

Label(root, text=info).grid(sticky=W)
configrecord('''注意事项: 
* 目前生成的obj导入后不能摆动作
* 贴图自己导 不用肝uv
* 请确保文件路径无空格
* 尽量将输出路径与贴图路径保持一致
* 不要试图抓虫子 出错别找我

更新日志: 
* 窗口化GUI
* 新增导出C4D脚本
* 修复当方块长宽不同时底部贴图错误的BUG
''', 1)

root.mainloop()

a(input('Thanks for using this software!\nPress Enter to exit...\n'))
