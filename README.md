

# 瓦片生成工具

### 简介

​	如果需要对路网工具生成的瓦片**地图进行美化**，可以通过本工具对美化后的地图重新瓦片化。

### 环境配置

- 下载并安装[python3](https://www.python.org/ftp/python/3.9.10/python-3.9.10-amd64.exe)

- 安装运行依赖(opecv、numpy)

  打开命令行终端，输入如下指令：

  ```shell
  pip3 install opencv-contrib-python -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```

### 前置说明

​	可通过路网工具下载地图工程，解压后根目录下的tilemap目录即为瓦片地图的存储路径。瓦片地图下的文件目录结构如下：

```
tilemap
   |--- 0
        |----x.png
   |----1
        |----x.png
   |----2
        |----x.png
   |----3
        |----x.png
   |----4
        |----x.png
   |----config.json
   |----layer_0.png
   |----layer_1.png
   |----layer_2.png
   |----layer_3.png
   |----layer_4.png
```

​	以上示例为一个包含5个层级的瓦片地图，0至4这五个文件夹分别存放对应层级切片后的地图小瓦片，每个小瓦片为256*256像素的小图片；layer_0.png至layer_4.png这五张图片为对应层级的原始图片，即把layer_4.png切片将得到目录4下面的多张小图片，依此类推；config.json文件描述了从layer_n.png到目录n的转换关系，以及图片到地图坐标系的转换关系。

### 使用说明

#### 使用场景1

​	如果需要对地图进行美化，可以拿到最高清的那张图层图片(上例中为layer_4.png)，然后使用PS或者AI对图片进行处理，然后使用img2tiles.py重新生成所有文件夹以及layer_n.png图片，示例如下：

```shell
python.exe C:\TileRegenerator\src\img2tiles.py C:\TileRegenerator\example\layer_4.png C:\TileRegenerator\example\config.json C:\TileRegenerator\output
```

​	该脚本需要三个参数，分别为：

- 美化后的图片路径，本例为：C:\TileRegenerator\example\layer_4.png
- 原始的配置文件，本例为：C:\TileRegenerator\example\config.json
- 输出目录，本例为：C:\TileRegenerator\output

#### 使用场景2

​	使用场景1会存在一个问题，如果图片上有文字标注信息，那么生成的低层级图片layer_n.png上面的文字就会越来越小，解决办法是使用场景1处理时，图片上面先不要标注文本信息，然后按照使用场景1输出多张图层图片layer_n.png，美工再分别对layer_n.png进行文字标注，一般高层级的标注会比较丰富、比较多，低层级的比较少，位置也会有所不同，需要分别处理。

​	处理完后，使用layer2tile.py分别切片layer_n.png，即该程序的功能是根据layer_n.png图层图片生成对应的n级瓦片目录，示例如下：

```
python.exe C:\TileRegenerator\src\layer2tile.py C:\TileRegenerator\output\tilemap\layer_4.png 4 C:\TileRegenerator\example\config.json C:\TileRegenerator\output

python.exe C:\TileRegenerator\src\layer2tile.py C:\TileRegenerator\output\tilemap\layer_3.png 3 C:\TileRegenerator\example\config.json C:\TileRegenerator\output

python.exe C:\TileRegenerator\src\layer2tile.py C:\TileRegenerator\output\tilemap\layer_2.png 2 C:\TileRegenerator\example\config.json C:\TileRegenerator\output

python.exe C:\TileRegenerator\src\layer2tile.py C:\TileRegenerator\output\tilemap\layer_1.png 1 C:\TileRegenerator\example\config.json C:\TileRegenerator\output

python.exe C:\TileRegenerator\src\layer2tile.py C:\TileRegenerator\output\tilemap\layer_0.png 0 C:\TileRegenerator\example\config.json C:\TileRegenerator\output
```

​	该脚本需要四个参数，分别为：

- 处理后的图层图片，本例子为：C:\TileRegenerator\output\tilemap\layer_n.png
- 图层图片对应的图层，本例子为：4、3、2、1、0
- 原始的配置文件，本例为：C:\TileRegenerator\example\config.json
- 输出目录，本例为：C:\TileRegenerator\output

#### 其他

​	软件还包括一个tile2img.py脚本，这个软件的作用是，如果目录下没有最高层级的图片(本例为layer_4.png)，可以执行该脚本，通过瓦片反向拼接出最高层级的图片。

```
python.exe C:\TileRegenerator\src\tile2img.py C:\TileRegenerator\output\tilemap C:\TileRegenerator\output\tilemap\config.json C:\TileRegenerator\output\tilemap
```

​	该脚本需要三个参数，分别为：

- 瓦片地图根目录，本例子为：C:\TileRegenerator\output\tilemap
- 原始的配置文件，本例为：C:\TileRegenerator\output\tilemap\config.json 
- 输出目录，本例为：C:\TileRegenerator\output\tilemap

执行该脚本，最终会重新生成layer_4.png。

#### 

