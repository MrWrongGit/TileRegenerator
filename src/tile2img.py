import json
import cv2
import numpy as np
import os
import sys

tile_root_path = './'
config_file_path = './config.json'
output_dir = './'

def help():
    print('用法: python tile2img.py 瓦片地图根目录 /xx路径/config.json /xx输出目录')
    print('参数1：存放多级瓦片的根目录')
    print('参数2：瓦片配置文件')
    print('参数3：层级文件输出目录')

def argParser():
    global tile_root_path
    global config_file_path
    global output_dir

    if len(sys.argv) < 3:
        help()
        exit(-1)

    if len(sys.argv) > 3:
        output_dir = sys.argv[3]
    else:
        output_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]

    if os.path.exists(sys.argv[1])==False or os.path.isdir(sys.argv[1])==False:
        print("瓦片根目录路径不正确！")
        exit(-2)
    if os.path.exists(sys.argv[2])==False or os.path.isfile(sys.argv[2])==False:
        print("配置文件路径不正确！")
        exit(-2)
    if os.path.exists(output_dir)==False or os.path.isdir(output_dir)==False:
        print("输出目录不正确")
        exit(-2)

    tile_root_path = sys.argv[1]
    config_file_path = sys.argv[2]

    print("瓦片根目录：",tile_root_path)
    print("配置文件：",config_file_path)
    print("输出目录：",output_dir)

# parse args
argParser()

with open(config_file_path, 'r') as f:
    tile_json = json.load(f)
    layer_cnt = tile_json['LayerCount']
    col_cnt = tile_json['Layers'][layer_cnt - 1]['ColCount']
    row_cnt = tile_json['Layers'][layer_cnt - 1]['RowCount']
    tile_max_root = os.path.join(tile_root_path, str(layer_cnt-1))

    col_imgs = []
    for r in range(row_cnt):
        row_imgs = ()
        for c in range(col_cnt):
            tile_name = c * row_cnt + r
            tile_path = os.path.join(tile_max_root, str(tile_name) + '.png')
            row_imgs += (cv2.imread(tile_path, cv2.IMREAD_UNCHANGED),)
        col_imgs += (np.hstack(row_imgs),)

    layer_img = np.vstack(col_imgs)
    cv2.imwrite(os.path.join(output_dir, 'layer_'+str(layer_cnt - 1)+'.png'), layer_img)