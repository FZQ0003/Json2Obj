# -*-coding: utf-8 -*-

import base64
import json
import os
import subprocess

import obj_output
from tkinter import *  # pylint: disable=unused-wildcard-import
from tkinter import messagebox, filedialog

from PIL import Image

from icon import img


data_list = None
data_json = None
data_png = None
list_model = None
text_rec = None
png_d = None
json_d = None
fn_png = None


def calculate_relative_path(path_a, path_b):
    """
    计算相对路径:
        已知两个绝对路径 a 和 b, 求 b 相对于 a 的相对路径.

    注:
        1. a 和 b 来自于同一个盘符
        2. 路径分隔符用反斜杠 "\\"

    :return: 相对路径
    """

    path_a, path_b = path_a.split('\\'), path_b.split('\\')
    # a = 'D:/M/N/O/P/a.py' --> ['D:', 'M', 'N', 'O', 'P', 'a.py']
    # b = 'D:/M/N/Q/b.py' --> ['D:', 'M', 'N', 'Q', 'b.py']

    intersection = 0  # 交汇点位置

    for index in range(min(len(path_a), len(path_b))):
        m, n = path_a[index], path_b[index]
        if m != n:
            intersection = index  # --> 3
            break

    def backward():  # "溯流而上"
        return (len(path_a) - intersection - 1) * '../'

    # (6 - 3 - 1) * '../' --> '../../'

    def forward():  # "顺流而下"
        return '/'.join(path_b[intersection:])

    # ['D:', 'M', 'N', 'Q', 'b.py'] --> 'Q/b.py'

    out = backward() + forward()
    # '../../' + 'Q/b.py' --> '../../Q/b.py'
    return out


def openfile():
    global fn_png, data_json, data_png

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
        load_json(fn_json)
        load_png(fn_png)


def load_json(fn):
    global json_d, data_list
    with open(fn, 'r') as f:
        tx = f.read()
    json_d = json.loads(tx)
    g_list = [i for i in list(dict.keys(json_d)) if ':' not in i and 'format_version' not in i]
    data_list.set(g_list)


def load_png(fn):
    global png_d
    png_d = Image.open(fn)


def output_mode():
    global list_model
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
    config_record('准备转换...\n\n', 1)
    convert_model(mode, filename)


def config_record(text, n):
    global text_rec
    text_rec.config(state=NORMAL)
    if n == 1:
        text_rec.delete(1.0, END)
    text_rec.insert('end', text)
    text_rec.config(state=DISABLED)


def convert_model(mode, name):
    global fn_png, json_d, png_d
    # tx_v = ''
    # tx_vt = ''
    # tx_f = ''
    x = 0
    tx_py = ''
    gn = list_model.get(list_model.curselection())
    geo = json_d[gn]
    tw = geo.get('texturewidth', png_d.size[0])
    th = geo.get('textureheight', png_d.size[1])
    bones = geo['bones']

    obj_m = obj_output.B(tw, th, png_d)

    for bone in bones:
        bn = bone['name']
        config_record('正在处理: ' + bn + '\n', 0)
        nr = bone.get('neverRender', False)
        if not nr:
            # f = ''
            if mode is True or mode == 'yes':
                p = bone.get('pivot', [0, 0, 0])
                pa = bone.get('parent', None)
                tx_py += "    edit_obj('" + bn + "', " + str(p[0]) + ", " + str(p[1]) + ", " + str(p[2])
                if pa is not None:
                    tx_py += ", '" + pa + "')\n"
                else:
                    tx_py += ", None)\n"
            else:
                p = [0, 0, 0]
            m = bone.get('mirror', False)
            obj_m.reset(bn, p, m)
            cubes = bone['cubes']
            for cube in cubes:
                o = cube['origin']
                s = cube['size']
                u = cube['uv']
                i = cube.get('inflate', 0)
                # tx_v += obj_v(p, o, s, i)
                # tx_vt += obj_vt(s, u, tw, th)
                # f += obj_f(m, x)
                obj_m.input(o, s, u, i)
                obj_m.main()
                x += 1
            # tx_f += "\n\ng " + bn + f

    # obj = tx_v + '\n' + tx_vt + tx_f
    obj = obj_m.print()
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
    if mode is True or mode == 'yes':
        bpy = '''# Made with MCJSON by F_Qilin.
# Fix the model of *.obj file
# Only for Blender
# Version: 1.0
# Model Name: ''' + gn + '''


import bpy, math

from bpy import data as d
from bpy import context as c
from bpy import ops as o


def search_parent(objects, obj):
    while obj.parent != None and obj.parent != objects:
        obj = obj.parent
    return obj

def edit_obj(name, x, y, z, pa):
    global group
    if pa == None:
        pa = group
    else:
        pa = d.objects[pa]
    obj = d.objects[name]
    pos_pa = search_parent(group, pa).location
    d.objects[name].parent = pa
    pos_obj = obj.location
    rot_obj = obj.rotation_euler
    pos_obj[0] = float(x)/16 - pos_pa[0]
    pos_obj[1] = float(y)/16 - pos_pa[1]
    pos_obj[2] = float(z)/16 - pos_pa[2]
    rot_obj[0] = 0

def data_init(name):
    global group
    group = d.objects.get(name, None)
    if group == None:
        o.object.empty_add(type='PLAIN_AXES', radius=2, location=(0, 0, 0))
        c.object.name = name
        group = d.objects[name]
        group.rotation_euler[0] = math.pi/2

def main():
    data_init(''' + "'" + os.path.basename(name) + ".obj'" + ''')
    
''' + tx_py + '''

if __name__ == '__main__':
    main()
'''
        cpy = '''# Made with MCJSON by F_Qilin.
# Fix the model of *.obj file
# Only for Cinema 4D
# Version: 1.1
# Model Name: ''' + gn + '''


import c4d


def search_obj(obj_list, name, ty):
    global pa_tmp
    if ty == 1:
        pa_tmp = None
    for obj in obj_list:
        if name == obj.GetName():
            return obj
        obj_children = obj.GetChildren()
        if obj_children != []:
            x = search_obj(obj_children, name, 0)
            if x != None:
                if ty == 1:
                    pa_tmp = obj
                return x
    return None

def edit_obj(name, x, y, z, pa):
    global group, objects, pa_tmp
    obj = search_obj(objects, name, 0)
    if pa == None:
        pa = group
        pa_pos = c4d.Vector(0, 0, 0)
    else:
        pa = search_obj(objects, pa, 1)
        if pa_tmp == None:
            pa_tmp = pa
        pa_pos = pa_tmp.GetAbsPos()
    obj[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(float(x)/16 - pa_pos[0], 
                                                     float(y)/16 - pa_pos[1], 
                                                     float(z)/16 - pa_pos[2])
    obj.InsertUnder(pa)

def data_init(name):
    global group, objects
    obj_list = doc.GetObjects()
    group = search_obj(obj_list, name, 0)
    if group == None:
        group = c4d.BaseObject(5140)
        group.SetName(name)
        doc.InsertObject(group)
        objects = obj_list
    else:
        objects = group.GetChildren()
    group[c4d.NULLOBJECT_DISPLAY] = 9
    group[c4d.NULLOBJECT_RADIUS] = 2
    group[c4d.NULLOBJECT_ORIENTATION] = 3

def main():
    data_init(''' + "'" + os.path.basename(name) + ".obj'" + ''')
    
''' + tx_py + '''    
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

    config_record('\n输出成功!', 0)
    # os.system('start explorer ' + os.path.dirname(name + '.obj'))
    subprocess.Popen(['explorer', os.path.dirname(name + '.obj')])


def main():
    global data_json, data_png, data_list, list_model, text_rec
    ft = 'Microsoft YaHei'
    abspath = os.path.abspath('.')
    if ':\\' in abspath:
        abspath += '\\'
    else:
        abspath += '/'
    info = 'Made by F_Qilin (10/22/2019)'

    root = Tk()
    root.title('MCJSON: Json2Obj (Python Edition) v1.3_beta_1')
    root.resizable(False, False)

    tmp = open("tmp.ico", "wb+")
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
    bu_convert = Button(frame_ctrl, text='转换', width=10, height=10, command=output_mode)
    bu_convert.grid(row=3, column=1)

    frame_rec = Frame(root)
    frame_rec.grid(sticky=NW, row=0, column=1, padx=30, pady=20)
    Label(frame_rec, text='输出日志', font=(ft, 16)).grid(sticky=W)
    text_rec = Text(frame_rec, width=24, height=22)
    text_rec.config(state=DISABLED)
    text_rec.grid(pady=15)

    Label(root, text=info).grid(sticky=W)
    config_record('''注意事项: 
* 此为Beta版本，可能会有BUG

提前体验: 
* 自动细分与自动挤压 (inflate>0)
* 修复底部贴图旋转180d的BUG

''', 1)

    root.mainloop()


if __name__ == '__main__':
    main()
