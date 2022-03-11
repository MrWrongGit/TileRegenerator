#coding=utf-8

import json
import cv2
import numpy as np
import sys
import os
import shutil

input_img_path = './'
img_layer = 0
config_file_path = './config.json'
output_dir = './'

def help():
    print('用法: python layer2tile.py /xx路径/xx图片.png 图片层级 /xx路径/config.json /xx输出目录')
    print('参数1：待切片的图片')
    print('参数2：图片所属层级(数字0-n)')
    print('参数3：切片配置文件')
    print('参数4：可选参数，未指定则为当前目录')

def argParser():
    global input_img_path
    global img_layer
    global config_file_path
    global output_dir

    if len(sys.argv) < 4:
        help()
        exit(-1)

    if len(sys.argv) > 4:
        output_dir = sys.argv[4]
    else:
        output_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]

    if os.path.exists(sys.argv[1])==False or os.path.isfile(sys.argv[1])==False:
        print("图片路径不正确！")
        exit(-2)
    if os.path.exists(sys.argv[3])==False or os.path.isfile(sys.argv[3])==False:
        print("配置文件路径不正确！")
        exit(-2)
    if os.path.exists(output_dir)==False or os.path.isdir(output_dir)==False:
        print("输出目录不正确")
        exit(-2)

    input_img_path = sys.argv[1]
    img_layer = int(sys.argv[2])
    config_file_path = sys.argv[3]

    print("输入图片：",input_img_path)
    print("图片层级：",img_layer)
    print("配置文件：",config_file_path)
    print("输出目录：",output_dir)


# parse args
argParser()
# prepare
if os.path.exists(os.path.join(output_dir, 'tilemap')) == False:
    os.mkdir(os.path.join(output_dir, 'tilemap'))

with open(config_file_path, 'r') as f:
    config_json = json.load(f)
    layer_cnt = config_json['LayerCount']

    # check and prepare
    if img_layer >= layer_cnt:
        print("图片层级超出范围！")
        exit(-3)
    if os.path.exists(os.path.join(output_dir, 'tilemap', str(img_layer))):
        shutil.rmtree(os.path.join(output_dir, 'tilemap', str(img_layer)))
    os.mkdir(os.path.join(output_dir, 'tilemap', str(img_layer)))

    img = cv2.imread(input_img_path,  cv2.IMREAD_UNCHANGED)
    h = img.shape[0]
    w = img.shape[1]
    col_cnt = config_json['Layers'][img_layer]['ColCount']
    row_cnt = config_json['Layers'][img_layer]['RowCount']
    tile_folder_path = os.path.join(output_dir, 'tilemap', str(img_layer))

    # start from down-left corner, blank area in up-side and right-side will be abandoned!
    col_imgs = []
    for r in range(row_cnt - 1, -1, -1): # down to up
        row_imgs = ()
        for c in range(col_cnt): # left to right
            # calculate tile file name
            tile_name = str(c * row_cnt + r)
            tile_path = os.path.join(tile_folder_path, tile_name + '.png')
            # get ROI
            start_h = h - (row_cnt - r) * 256
            end_h = start_h+256
            if start_h < 0: # this may happen
                start_h = 0
            start_w = c * 256
            tile = img[start_h: end_h, start_w: start_w+256]

            # tile may not 256x256
            # hight not enough, epand to 256
            if tile.shape[0] < 256:
                expand_h = np.zeros(shape=(256-tile.shape[0], tile.shape[1], 4), dtype=np.uint8)
                tile = np.vstack((expand_h, tile)) # expand to top!!
            # widht not enough, epand to 256
            if tile.shape[1] < 256:
                expand_w = np.zeros(shape=(tile.shape[0], 256-tile.shape[1], 4), dtype=np.uint8)
                tile = np.hstack((tile, expand_w)) # expand to right!
            # save tile to file
            cv2.imwrite(tile_path, tile)

            # setup and save layer picture
            row_imgs += (tile,)
        col_imgs += (np.hstack(row_imgs),)
    col_imgs.reverse()
    img = np.vstack(col_imgs)
    cv2.imwrite(os.path.join(output_dir, 'tilemap', 'layer_'+str(img_layer)+'.png'), img)

shutil.copyfile(config_file_path, os.path.join(output_dir, 'tilemap', 'config.json'))