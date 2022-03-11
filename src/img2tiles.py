#coding=utf-8

import json
import cv2
import numpy as np
import sys
import os
import shutil

input_img_path = './'
config_file_path = './config.json'
output_dir = './'

def help():
    print('用法: python img2tiles.py /xx路径/xx图片.png /xx路径/config.json /xx输出目录')
    print('参数1：待切片的图片')
    print('参数2：切片配置文件')
    print('参数3：可选参数，未指定则为当前目录')

def argParser():
    global input_img_path
    global config_file_path
    global output_dir

    if len(sys.argv) < 3:
        help()
        exit(-1)

    if len(sys.argv) > 3:
        output_dir = sys.argv[3]
    else:
        output_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]

    if os.path.exists(sys.argv[1])==False or os.path.isfile(sys.argv[1])==False:
        print("图片路径不正确！")
        exit(-2)
    if os.path.exists(sys.argv[2])==False or os.path.isfile(sys.argv[2])==False:
        print("配置文件路径不正确！")
        exit(-2)
    if os.path.exists(output_dir)==False or os.path.isdir(output_dir)==False:
        print("输出目录不正确")
        exit(-2)

    input_img_path = sys.argv[1]
    config_file_path = sys.argv[2]

    print("输入图片：",sys.argv[1])
    print("配置文件：",sys.argv[2])
    print("输出目录：",output_dir)


# parse args
argParser()
# prepare
if os.path.exists(os.path.join(output_dir, 'tilemap')):
    shutil.rmtree(os.path.join(output_dir, 'tilemap'))
os.mkdir(os.path.join(output_dir, 'tilemap'))

with open(config_file_path, 'r') as f:
    config_json = json.load(f)
    layer_cnt = config_json['LayerCount']

    # input image is the highest resolution layer picture
    img = cv2.imread(input_img_path,  cv2.IMREAD_UNCHANGED)

    for layer in range(layer_cnt-1, -1, -1):
        # the highest layer no need 512x522 -> 256x256 convertion, just split to 256x256 tile
        # ROI_size used just for reducing duplicate code
        if layer == layer_cnt-1:
            ROI_size = 256
        else:
            ROI_size = 512

        # folder for tile
        tile_folder_path = os.path.join(output_dir, 'tilemap', str(layer))
        os.mkdir(tile_folder_path)
        # basic info
        h = img.shape[0]
        w = img.shape[1]
        col_cnt = config_json['Layers'][layer]['ColCount']
        row_cnt = config_json['Layers'][layer]['RowCount']

        # start from down-left corner, blank area in up-side and right-side will be abandoned!
        # high layer image -> get 512*512 -> down to 256*256 -> merge to low layer image
        col_imgs = []
        for r in range(row_cnt - 1, -1, -1): # down to up
            row_imgs = ()
            for c in range(col_cnt): # left to right
                # calculate tile file name
                tile_name = str(c * row_cnt + r)
                tile_path = os.path.join(tile_folder_path, tile_name + '.png')
                # get ROI
                start_h = h - (row_cnt - r) * ROI_size
                end_h = start_h+ROI_size
                if start_h < 0: # this may happen
                    start_h = 0
                start_w = c * ROI_size
                tile = img[start_h: end_h, start_w: start_w+ROI_size]

                # tile may not 512x512
                # hight not enough, epand to 512
                if tile.shape[0] < ROI_size:
                    expand_h = np.zeros(shape=(ROI_size-tile.shape[0], tile.shape[1], 4), dtype=np.uint8)
                    tile = np.vstack((expand_h, tile)) # expand to top!!
                # widht not enough, epand to 512
                if tile.shape[1] < ROI_size:
                    expand_w = np.zeros(shape=(tile.shape[0], ROI_size-tile.shape[1], 4), dtype=np.uint8)
                    tile = np.hstack((tile, expand_w)) # expand to right!
                # down to 256 * 256
                if ROI_size == 512:
                    tile = cv2.pyrDown(tile)
                # save tile to file
                cv2.imwrite(tile_path, tile)

                # setup and save layer picture
                row_imgs += (tile,)
            col_imgs += (np.hstack(row_imgs),)
        col_imgs.reverse()
        img = np.vstack(col_imgs)
        cv2.imwrite(os.path.join(output_dir, 'tilemap', 'layer_'+str(layer)+'.png'), img)

shutil.copyfile(config_file_path, os.path.join(output_dir, 'tilemap', 'config.json'))