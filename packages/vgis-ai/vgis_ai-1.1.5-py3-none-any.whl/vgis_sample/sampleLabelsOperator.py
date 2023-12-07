#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
# @Time    :  2021/12/4 14:10
# @Author  : chenxw
# @Email   : gisfanmachel@gmail.com
# @File    : aiSettings.py
# @Descr   : AI样本处理
# @Software: PyChar
import glob
import json
import os
import random
import shutil
import xml.etree.ElementTree as ET
from xml.dom.minidom import Document
import cv2
import imgaug.augmenters as iaa
import numpy as np
from PIL import Image
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
from shapely.geometry import Polygon, MultiPoint
from vgis_aiutils.aiTools import AIHelper
from vgis_utils.vgis_file.fileTools import FileHelper
from vgis_utils.vgis_file.fileTools import JsonHelper
from vgis_utils.vgis_image.imageTools import ImageHelper
from vgis_utils.vgis_string.stringTools import StringHelper


# AI样本格式转换
class FileFormatConverter:
    def __init__(self):
        pass

    # 503样本xml像素坐标转成地理坐标
    def coord_convert_kshxml(self, xml_file_path, tif_minx, tif_miny, tif_maxx, tif_maxy, new_xml_file_path):

        # root = ET.Element('annotation')
        # ET.SubElement(root, 'folder').text = os.path.dirname(output_dir)
        # ET.SubElement(root, 'filename').text = os.path.basename(image_path)
        # size = ET.SubElement(root, 'size')
        # ET.SubElement(size, 'width').text = str(image_width)
        # ET.SubElement(size, 'height').text = str(image_height)
        # ET.SubElement(size, 'depth').text = '3'
        # xml_string = ET.tostring(root, encoding='utf-8')
        # dom = minidom.parseString(xml_string)
        # formatted_xml = dom.toprettyxml(indent='  ')
        # with open(output_dir, 'w') as f:
        #     f.write(formatted_xml)
        #
        print(xml_file_path)
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        auxiliaryInfo = root.find('auxiliaryInfo')
        image_width = auxiliaryInfo.find('image_width').text
        image_height = auxiliaryInfo.find('image_height').text
        items = root.find('items')
        for objinfo in items.findall('objectInfo'):
            pointitems = objinfo.find('points').findall('item')
            for pointitem in pointitems:
                pointx = pointitem.findall('item')[0]
                pointy = pointitem.findall('item')[1]
                pointx.text = str(tif_minx + (tif_maxx - tif_minx) / float(image_width) * float(pointx.text))
                pointy.text = str(tif_maxy - (tif_maxy - tif_miny) / float(image_height) * float(pointy.text))
        # root为修改后的root
        new_tree = ET.ElementTree(root)
        # 保存为xml文件
        new_tree.write(new_xml_file_path, encoding='utf-8')

    # 503样本xml转换为json
    def kshxml2Json1(self, xml_file_path, json_file_path, epsg_code):
        json_file_dict = {}
        json_file_dict["type"] = "FeatureCollection"
        json_file_dict["crs"] = {'type': 'name', 'properties': {'name': 'EPSG:' + str(epsg_code)}}
        featureArray = []
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        items = root.find('items')
        objnum = 0
        for objinfo in items.findall('objectInfo'):
            objnum = objnum + 1
            label1 = objinfo.find('label1')
            label2 = objinfo.find('label2')
            label3 = objinfo.find('label3')
            label4 = objinfo.find('label4')
            label5 = objinfo.find('label5')
            label6 = objinfo.find('label6')
            objname = label6
            if objname == "":
                objname = label5
            if objname == "":
                objname = label4
            if objname == "":
                objname = label3
            if objname == "":
                objname = label2
            if objname == "":
                objname = label1
            pointitems = objinfo.find('points').findall('item')
            coordsArray = []
            point1x = pointitems[0].findall('item')[0].text
            point1y = pointitems[0].findall('item')[1].text
            point2x = pointitems[1].findall('item')[0].text
            point2y = pointitems[1].findall('item')[1].text
            point3x = pointitems[2].findall('item')[0].text
            point3y = pointitems[2].findall('item')[1].text
            point4x = pointitems[3].findall('item')[0].text
            point4y = pointitems[3].findall('item')[1].text
            point1Array = [point1x, point1y]
            point2Array = [point2x, point2y]
            point3Array = [point3x, point3y]
            point4Array = [point4x, point4y]
            pointsArray = []
            pointsArray.append(point1Array)
            pointsArray.append(point2Array)
            pointsArray.append(point3Array)
            pointsArray.append(point4Array)
            pointsArray.append(point1Array)
            coordsArray.append(pointsArray)
            feature_dict = {'type': 'Feature', 'id': objnum,
                            'geometry': {'type': 'Polygon', 'coordinates': coordsArray},
                            'properties': {'FID': objnum, 'Id': 0, 'XH': objname, 'type': ''}}
            featureArray.append(feature_dict)
        json_file_dict["features"] = featureArray
        self.__write_json_file(self, json_file_dict, json_file_path)

    # 503样本xml转换为json
    def kshxml2Json(self, xml_file_path, json_file_path, epsg_code):
        json_file_dict = {}
        json_file_dict["type"] = "FeatureCollection"
        json_file_dict["crs"] = {"type": "name", "properties": {"name": "EPSG:" + str(epsg_code)}}
        featureArray = []
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        items = root.find('items')
        objnum = 0
        for objinfo in items.findall('objectInfo'):
            objnum = objnum + 1
            label1 = objinfo.find('label1')
            label2 = objinfo.find('label2')
            label3 = objinfo.find('label3')
            label4 = objinfo.find('label4')
            label5 = objinfo.find('label5')
            label6 = objinfo.find('label6')
            objname = label6.text
            if objname is None or objname == '':
                objname = label5.text
            if objname is None or objname == '':
                objname = label4.text
            if objname is None or objname == '':
                objname = label3.text
            if objname is None or objname == '':
                objname = label2.text
            if objname is None or objname == '':
                objname = label1.text
            pointitems = objinfo.find('points').findall('item')
            coordsArray = []
            point1x = pointitems[0].findall('item')[0].text
            point1y = pointitems[0].findall('item')[1].text
            point2x = pointitems[1].findall('item')[0].text
            point2y = pointitems[1].findall('item')[1].text
            point3x = pointitems[2].findall('item')[0].text
            point3y = pointitems[2].findall('item')[1].text
            point4x = pointitems[3].findall('item')[0].text
            point4y = pointitems[3].findall('item')[1].text
            point1Array = [point1x, point1y]
            point2Array = [point2x, point2y]
            point3Array = [point3x, point3y]
            point4Array = [point4x, point4y]
            pointsArray = []
            pointsArray.append(point1Array)
            pointsArray.append(point2Array)
            pointsArray.append(point3Array)
            pointsArray.append(point4Array)
            pointsArray.append(point1Array)
            coordsArray.append(pointsArray)
            feature_dict = {"type": "Feature", "id": objnum,
                            "geometry": {"type": "Polygon", "coordinates": coordsArray},
                            "properties": {"FID": objnum, "Id": 0, "XH": objname, "type": ""}}
            featureArray.append(feature_dict)
        json_file_dict["features"] = featureArray

        self.__write_json_file(json_file_dict, json_file_path)

    # pascalVoc转yolo
    def pascalVoc2Yolo(self, xml_file_path, class_file_path, txt_file_path):
        classes_dict = {}
        # class_file_path= "classes.names"
        with open(class_file_path) as f:
            for idx, line in enumerate(f.readlines()):
                class_name = line.strip()
                classes_dict[class_name] = idx

        width, height, objects = self.__pascal_xml_reader(xml_file_path, "ALLClass")

        lines = []
        # 标注内容的类别、归一化后的中心点x坐标，归一化后的中心点y坐标，归一化后的目标框宽度w，归一化后的目标况高度h（此处归一化指的是除以图片宽和高）
        for obj in objects:
            x, y, x2, y2 = obj['bbox']
            class_name = obj['name']
            label = classes_dict[class_name]
            cx = (x2 + x) * 0.5 / width
            cy = (y2 + y) * 0.5 / height
            w = (x2 - x) * 1. / width
            h = (y2 - y) * 1. / height
            line = "%s %.6f %.6f %.6f %.6f\n" % (label, cx, cy, w, h)
            lines.append(line)

        # txt_name = filename.replace(".xml", ".txt").replace("labels_voc", "labels")
        with open(txt_file_path, "w") as f:
            f.writelines(lines)

    # 获取pascal文件中的class类型
    def get_class_name_array_in_pascal(self, file_path):
        class_name_array = []
        tree = ET.parse(file_path)
        for obj in tree.findall('object'):
            class_name = obj.find('name').text
            if class_name not in class_name_array:
                class_name_array.append(class_name)
        return class_name_array

    # 解析pascal文件中的数据,根据指定class
    def __pascal_xml_reader(self, file_path, class_name):
        """ Parse a PASCAL VOC xml file """
        tree = ET.parse(file_path)
        size = tree.find('size')
        width = int(size.find('width').text)
        height = int(size.find('height').text)
        objects = []
        for obj in tree.findall('object'):
            obj_struct = {}
            if class_name == "ALLClass" or class_name == obj.find('name').text:
                obj_struct['name'] = obj.find('name').text
                if obj.find('bndbox') is not None:
                    bbox = obj.find('bndbox')
                    obj_struct['bbox'] = [int(bbox.find('xmin').text),
                                          int(bbox.find('ymin').text),
                                          int(bbox.find('xmax').text),
                                          int(bbox.find('ymax').text)]
                if obj.find('polygon') is not None:
                    points = obj.find('polygon').iter()
                    obj_struct['polygon'] = []
                    for point in points:
                        if point.text != "\n":
                            obj_struct['polygon'].append(point.text)
                objects.append(obj_struct)
        return width, height, objects

    # labelme转yolo
    def labelme2Yolo(self, json_file_path, class_file_path, txt_file_path):
        classes_dict = {}
        # class_file_path= "classes.names"
        with open(class_file_path) as f:
            for idx, line in enumerate(f.readlines()):
                class_name = line.strip()
                classes_dict[class_name] = idx
        lines = []
        with open(json_file_path, 'r', encoding='utf8') as fp:
            json_data = json.load(fp)
            image_width = json_data.get("imageWidth")
            image_height = json_data.get("imageHeight")
            shapes_array = json_data.get("shapes")
            # 标注内容的类别、归一化后的中心点x坐标，归一化后的中心点y坐标，归一化后的目标框宽度w，归一化后的目标况高度h（此处归一化指的是除以图片宽和高）
            for shape_obj in shapes_array:
                class_name = shape_obj.get("label")
                # 针对烟囱样本采集时classname不标准的情况
                if class_name == "yc":
                    class_name = "chimney"
                # 针对油罐采集时classname不标准的情况
                if class_name == "oiltank":
                    class_name = "storagetank"
                points_array = shape_obj.get("points")
                x, y, x2, y2 = self.__get_envelop_of_labelme_points(points_array)
                label = classes_dict[class_name]
                cx = (x2 + x) * 0.5 / image_width
                cy = (y2 + y) * 0.5 / image_height
                w = (x2 - x) * 1. / image_width
                h = (y2 - y) * 1. / image_height
                line = "%s %.6f %.6f %.6f %.6f\n" % (label, cx, cy, w, h)
                lines.append(line)
        # txt_name = filename.replace(".xml", ".txt").replace("labels_voc", "labels")
        with open(txt_file_path, "w") as f:
            f.writelines(lines)

    # 实例点labelme转斜外包矩形labelme
    def convert_seg_points_to_obl_rect_of_labelme(self, intput_json_file_path, output_json_file_path):

        json_data = JsonHelper.get_json_obj_by_file(intput_json_file_path)
        shapes_array = json_data.get("shapes")
        for shape_obj in shapes_array:
            points_array = shape_obj.get("points")
            # new_points_array = self.__get_obl_rect_of_labelme_points(points_array)
            new_points_array = self.__get_rect_of_labelme_points(points_array)
            shape_obj["points"] = new_points_array
        JsonHelper.write_json_obj_into_file(json_data, output_json_file_path)

    # 对多边形计算斜矩形---有问题
    # 多边形的坐标  polygon_coords = [(0, 0), (0, 1), (1, 1), (1, 0)]
    def __oriented_bounding_box(self, polygon_coords):
        # 创建Shapely多边形对象
        polygon = Polygon(polygon_coords)
        # 计算最小旋转矩形
        min_rect = polygon.minimum_rotated_rectangle
        # 获取最小旋转矩形的坐标
        obb_coords = list(min_rect.exterior.coords)
        # 获取最小旋转矩形的中心点
        center = MultiPoint(obb_coords).centroid.coords[0]
        # 计算多边形与边界框中心的夹角（逆时针方向为正）
        angle = np.arctan2(center[1] - polygon.centroid.y, center[0] - polygon.centroid.x)
        # 将边界框坐标绕多边形中心旋转
        obb_coords_rotated = [
            (
                np.cos(angle) * (x - center[0]) - np.sin(angle) * (y - center[1]) + center[0],
                np.sin(angle) * (x - center[0]) + np.cos(angle) * (y - center[1]) + center[1]
            )
            for x, y in obb_coords
        ]
        return obb_coords_rotated

    # 内部函数，获取labelme斜外包矩形坐标范围,有问题
    def __get_obl_rect_of_labelme_points(self, points_array):
        # 定义多边形的坐标
        # coordinates = [(0, 0), (0, 1), (1, 1), (1, 0)]
        coordinates = []
        # points_array = [[104.0, 263.0], [104.0, 279.0]]
        for point in points_array:
            tmpx = point[0]
            tmpy = point[1]
            coordinates.append((tmpx, tmpy))
        # 获取多边形的斜矩形的坐标
        rectangle_coordinates = self.__oriented_bounding_box(coordinates)
        new_points_array = []
        # 最后一个点是跟第一个点一样，不用考虑
        for index in range(len(rectangle_coordinates) - 1):
            point = rectangle_coordinates[index]
            tmpx = point[0]
            tmpy = point[1]
            new_points_array.append([tmpx, tmpy])
        return new_points_array

    # 内部函数，获取labelme外包矩形坐标范围
    # points_array = [[104.0, 263.0], [104.0, 279.0]]
    def __get_rect_of_labelme_points(self, points_array):
        # 获取多边形的外包矩形的坐标
        minx, miny, maxx, maxy = self.__get_envelop_of_labelme_points2(points_array)
        new_points_array = [[minx, miny], [minx, maxy], [maxx, maxy], [maxx, miny]]
        return new_points_array

    # 内部函数，获取labelme正矩形坐标范围,效率低
    def __get_envelop_of_labelme_points(self, points_array):
        minx = points_array[0][0]
        miny = points_array[0][1]
        maxx = points_array[0][0]
        maxy = points_array[0][1]
        for point in points_array:
            tmpx = point[0]
            tmpy = point[1]
            if tmpx < minx:
                minx = tmpx
            if tmpy < miny:
                miny = tmpy
            if tmpx > maxx:
                maxx = tmpx
            if tmpy > maxy:
                maxy = tmpy
        return minx, miny, maxx, maxy

    # 内部函数，获取labelme正矩形坐标范围
    def __get_envelop_of_labelme_points2(self, points_array):
        # 定义多边形的坐标
        # coordinates = [(0, 0), (0, 1), (1, 1), (1, 0)]
        coordinates = []
        # points_array = [[104.0, 263.0], [104.0, 279.0]]
        for point in points_array:
            tmpx = point[0]
            tmpy = point[1]
            coordinates.append((tmpx, tmpy))
        # 创建多边形对象
        polygon = Polygon(coordinates)
        # 获取多边形的斜矩形的坐标
        rectangle_coordinates = polygon.envelope.exterior.coords
        x_list = rectangle_coordinates.xy[0]
        y_list = rectangle_coordinates.xy[1]
        minx = min(x_list)
        miny = min(y_list)
        maxx = max(x_list)
        maxy = max(y_list)
        return minx, miny, maxx, maxy

    # 加载自己的数据集，只需要所有 labelme 标注出来的 json 文件即可
    def load_dataset(self, path):
        dataset = []
        for json_file_path in glob.glob("{}/*json".format(path)):
            with open(json_file_path, 'r', encoding='utf8') as fp:
                json_data = json.load(fp)
                image_width = json_data.get("imageWidth")
                image_height = json_data.get("imageHeight")
                shapes_array = json_data.get("shapes")
                for shape_obj in shapes_array:
                    points_array = shape_obj.get("points")
                    xmin, ymin, xmax, ymax = self.__get_envelop_of_labelme_points(points_array)
                    # 偏移量
                    xmin = int(xmin) / image_width
                    ymin = int(ymin) / image_height
                    xmax = int(xmax) / image_width
                    ymax = int(ymax) / image_height
                    xmin = np.float64(xmin)
                    ymin = np.float64(ymin)
                    xmax = np.float64(xmax)
                    ymax = np.float64(ymax)
                    # 将Anchor的宽和高放入dateset，运行kmeans获得Anchor
                    dataset.append([xmax - xmin, ymax - ymin])
        return np.array(dataset)

    # yolo转pascalVOC
    def yolo2pascalVoc(self, txt_file_path, xml_file_path, pic_file_path, class_file_path):
        classes_dict = {}
        # class_file_path= "classes.names"
        with open(class_file_path) as f:
            for idx, line in enumerate(f.readlines()):
                class_name = line.strip()
                classes_dict[idx] = class_name
        file_name = FileHelper.get_file_name(txt_file_path)
        xmlBuilder = Document()
        annotation = xmlBuilder.createElement("annotation")  # 创建annotation标签
        xmlBuilder.appendChild(annotation)
        txtFile = open(txt_file_path)
        txtList = txtFile.readlines()
        img = cv2.imread(pic_file_path)
        Pheight, Pwidth, Pdepth = img.shape

        folder = xmlBuilder.createElement("folder")  # folder标签
        foldercontent = xmlBuilder.createTextNode("driving_annotation_dataset")
        folder.appendChild(foldercontent)
        annotation.appendChild(folder)  # folder标签结束

        filename = xmlBuilder.createElement("filename")  # filename标签
        filenamecontent = xmlBuilder.createTextNode(file_name)
        filename.appendChild(filenamecontent)
        annotation.appendChild(filename)  # filename标签结束

        filename = xmlBuilder.createElement("path")  # path标签
        filenamecontent = xmlBuilder.createTextNode(pic_file_path)
        filename.appendChild(filenamecontent)
        annotation.appendChild(filename)  # path标签结束

        size = xmlBuilder.createElement("size")  # size标签
        width = xmlBuilder.createElement("width")  # size子标签width
        widthcontent = xmlBuilder.createTextNode(str(Pwidth))
        width.appendChild(widthcontent)
        size.appendChild(width)  # size子标签width结束

        height = xmlBuilder.createElement("height")  # size子标签height
        heightcontent = xmlBuilder.createTextNode(str(Pheight))
        height.appendChild(heightcontent)
        size.appendChild(height)  # size子标签height结束

        depth = xmlBuilder.createElement("depth")  # size子标签depth
        depthcontent = xmlBuilder.createTextNode(str(Pdepth))
        depth.appendChild(depthcontent)
        size.appendChild(depth)  # size子标签depth结束

        annotation.appendChild(size)  # size标签结束

        for j in txtList:
            oneline = j.strip().split(" ")
            object = xmlBuilder.createElement("object")  # object 标签
            picname = xmlBuilder.createElement("name")  # name标签
            namecontent = xmlBuilder.createTextNode(classes_dict[oneline[0]])
            picname.appendChild(namecontent)
            object.appendChild(picname)  # name标签结束

            pose = xmlBuilder.createElement("pose")  # pose标签
            posecontent = xmlBuilder.createTextNode("Unspecified")
            pose.appendChild(posecontent)
            object.appendChild(pose)  # pose标签结束

            truncated = xmlBuilder.createElement("truncated")  # truncated标签
            truncatedContent = xmlBuilder.createTextNode("0")
            truncated.appendChild(truncatedContent)
            object.appendChild(truncated)  # truncated标签结束

            difficult = xmlBuilder.createElement("difficult")  # difficult标签
            difficultcontent = xmlBuilder.createTextNode("0")
            difficult.appendChild(difficultcontent)
            object.appendChild(difficult)  # difficult标签结束

            bndbox = xmlBuilder.createElement("bndbox")  # bndbox标签
            xmin = xmlBuilder.createElement("xmin")  # xmin标签
            mathData = int(((float(oneline[1])) * Pwidth + 1) - (float(oneline[3])) * 0.5 * Pwidth)
            xminContent = xmlBuilder.createTextNode(str(mathData))
            xmin.appendChild(xminContent)
            bndbox.appendChild(xmin)  # xmin标签结束

            ymin = xmlBuilder.createElement("ymin")  # ymin标签
            mathData = int(((float(oneline[2])) * Pheight + 1) - (float(oneline[4])) * 0.5 * Pheight)
            yminContent = xmlBuilder.createTextNode(str(mathData))
            ymin.appendChild(yminContent)
            bndbox.appendChild(ymin)  # ymin标签结束

            xmax = xmlBuilder.createElement("xmax")  # xmax标签
            mathData = int(((float(oneline[1])) * Pwidth + 1) + (float(oneline[3])) * 0.5 * Pwidth)
            xmaxContent = xmlBuilder.createTextNode(str(mathData))
            xmax.appendChild(xmaxContent)
            bndbox.appendChild(xmax)  # xmax标签结束

            ymax = xmlBuilder.createElement("ymax")  # ymax标签
            mathData = int(((float(oneline[2])) * Pheight + 1) + (float(oneline[4])) * 0.5 * Pheight)
            ymaxContent = xmlBuilder.createTextNode(str(mathData))
            ymax.appendChild(ymaxContent)
            bndbox.appendChild(ymax)  # ymax标签结束

            object.appendChild(bndbox)  # bndbox标签结束

            annotation.appendChild(object)  # object标签结束

        f = open(xml_file_path, 'w')
        xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
        f.close()

    # pascalVoc转labelme
    # class_name为AllClass表示全部class,否则按指定class类型类转换
    def pascalVoc2Labelme(self, xml_file_path, pic_file_path, json_file_path, class_name):
        width, height, objects = self.__pascal_xml_reader(xml_file_path, class_name)
        shapes_array = []
        if len(objects) > 0:
            for obj in objects:
                class_name = obj['name']
                shape_dict = {}
                shape_dict["label"] = class_name
                points_array = []
                if "bbox" in obj:
                    x, y, x2, y2 = obj['bbox']
                    points_array = [[float(x), float(y)], [float(x2), float(y)], [float(x2), float(y2)],
                                    [float(x), float(y2)]]
                if "polygon" in obj:
                    for index in range(len(obj["polygon"])):
                        if index % 2 == 0:
                            points_array.append([float(obj["polygon"][index])] + [float(obj["polygon"][index + 1])])
                shape_dict["points"] = points_array
                shape_dict["group_id"] = None
                shape_dict["shape_type"] = "polygon"
                shape_dict["flags"] = {}
                shapes_array.append(shape_dict)
            json_file_dict = self.__build_lableme_json_dict(shapes_array, pic_file_path)
            self.__write_json_file(json_file_dict, json_file_path)
        else:
            print("当前图片的标签数据为空")

    # 内部函数，构建labelme的json字典数据
    def __build_lableme_json_dict(self, shapes_array, pic_file_path):

        json_file_dict = {}
        json_file_dict["version"] = "4.6.0"
        json_file_dict["flags"] = {}
        json_file_dict["shapes"] = shapes_array
        json_file_dict["imagePath"] = FileHelper.get_file_name(pic_file_path)
        # 图像的base64取值有问题
        # json_file_dict["imageData"] = imageOperator.convert2Base64(pic_file_path)
        json_file_dict["imageData"] = None
        img = Image.open(pic_file_path)
        json_file_dict["imageHeight"] = img.height
        json_file_dict["imageWidth"] = img.width
        return json_file_dict

    # 内部函数，将字典对象写入json文件
    def __write_json_file(self, json_file_dict, json_file_path):
        json_str = json.dumps(json_file_dict, indent=4)
        with open(json_file_path, 'w') as json_file:
            json_file.write(json_str)

    # 得到DOTA标签文件里的类型
    def get_class_name_array_in_dota_txt(self, txt_file_path):
        class_name_array = []
        txtFile = open(txt_file_path)
        txtList = txtFile.readlines()
        # 前两行不读
        for j in txtList[2:]:
            oneline = j.strip().split(" ")
            class_name = oneline[8]
            if class_name not in class_name_array:
                class_name_array.append(class_name)
        return class_name_array

    # DOTA转labelme,指定class，或者是全部类型(ALLClass)
    def DOTA2Labelme(self, txt_file_path, pic_file_path, json_file_path, class_name):
        txtFile = open(txt_file_path)
        txtList = txtFile.readlines()
        shapes_array = []
        # 前两行不读
        for j in txtList[2:]:
            oneline = j.strip().split(" ")
            label = oneline[8]
            shape_dict = {}
            shape_dict["label"] = label
            if class_name == "ALLClass" or class_name == label:
                points_array = [[float(oneline[0]), float(oneline[1])], [float(oneline[2]), float(oneline[3])],
                                [float(oneline[4]), float(oneline[5])], [float(oneline[6]), float(oneline[7])]]
                shape_dict["points"] = points_array
                shape_dict["group_id"] = None
                shape_dict["shape_type"] = "polygon"
                shape_dict["flags"] = {}
                shapes_array.append(shape_dict)
        if len(shapes_array) > 0:
            json_file_dict = self.__build_lableme_json_dict(shapes_array, pic_file_path)
            self.__write_json_file(json_file_dict, json_file_path)
        else:
            print("当前图片的标签数据为空")

    # 得到LEVIR标签文件里的类型
    def get_class_name_array_in_levir_txt(self, txt_file_path):
        class_name_array = []
        txtFile = open(txt_file_path)
        txtList = txtFile.readlines()
        for j in txtList:
            oneline = j.strip().split(" ")
            class_name = oneline[0]
            if class_name not in class_name_array:
                class_name_array.append(class_name)
        return class_name_array

    # LEVIR转labelme,指定class，或者是全部类型(ALLClass)
    def LEVIR2Labelme(self, txt_file_path, pic_file_path, json_file_path, class_name):
        txtFile = open(txt_file_path)
        txtList = txtFile.readlines()
        shapes_array = []
        for j in txtList:
            oneline = j.strip().split(" ")
            label = oneline[0]
            shape_dict = {}
            shape_dict["label"] = label
            # class left top right bottom
            if class_name == "ALLClass" or class_name == label:
                if float(oneline[1]) > 0 and float(oneline[2]) > 0 and float(oneline[3]) > 0 and float(oneline[4]) > 0:
                    points_array = [[float(oneline[1]), float(oneline[2])], [float(oneline[3]), float(oneline[2])],
                                    [float(oneline[3]), float(oneline[4])], [float(oneline[1]), float(oneline[4])]]
                    shape_dict["points"] = points_array
                    shape_dict["group_id"] = None
                    shape_dict["shape_type"] = "polygon"
                    shape_dict["flags"] = {}
                    shapes_array.append(shape_dict)
        if len(shapes_array) > 0:
            json_file_dict = self.__build_lableme_json_dict(shapes_array, pic_file_path)
            self.__write_json_file(json_file_dict, json_file_path)
        else:
            print("当前图片的标签数据为空")

    # UCAS转labelme
    def UCAS2Labelme(self, txt_file_path, pic_file_path, json_file_path, label_name):
        txtFile = open(txt_file_path)
        txtList = txtFile.readlines()
        shapes_array = []
        for j in txtList:
            oneline = j.strip().split("\t")
            shape_dict = {}
            shape_dict["label"] = label_name
            # 校正前的范围,不是矩形
            points_array = [[float(oneline[0]), float(oneline[1])], [float(oneline[2]), float(oneline[3])],
                            [float(oneline[4]), float(oneline[5])], [float(oneline[6]), float(oneline[7])]]
            # 校正后的范围
            # minx = float(oneline[9])
            # miny = float(oneline[10])
            # maxx = minx+float(oneline[11])
            # maxy = miny+float(oneline[12])
            # points_array = [[minx, miny], [maxx, miny],
            #                 [maxx, maxy], [minx, maxy]]
            shape_dict["points"] = points_array
            shape_dict["group_id"] = None
            shape_dict["shape_type"] = "polygon"
            shape_dict["flags"] = {}
            shapes_array.append(shape_dict)
        json_file_dict = self.__build_lableme_json_dict(shapes_array, pic_file_path)
        self.__write_json_file(json_file_dict, json_file_path)

    # NWPU转labelme
    def NWPU2Labelme(self, txt_file_path, class_file_path, pic_file_path, json_file_path):
        classes_dict = {}
        # class_file_path= "classes.names"
        with open(class_file_path) as f:
            for idx, line in enumerate(f.readlines()):
                class_name = line.strip()
                classes_dict[idx] = class_name
        txtFile = open(txt_file_path)
        txtList = txtFile.readlines()
        shapes_array = []
        for j in txtList:
            oneline = j.strip().split(",")
            class_id = oneline[2]
            shape_dict = {}
            shape_dict["label"] = classes_dict[class_id]
            minx_str = StringHelper.get_number_in_str(oneline[0].split(",").replace(" ", ""))
            miny_str = StringHelper.get_number_in_str(oneline[1].split(",").replace(" ", ""))
            maxx_str = StringHelper.get_number_in_str(oneline[2].split(",").replace(" ", ""))
            maxy_str = StringHelper.get_number_in_str(oneline[3].split(",").replace(" ", ""))
            minx = float(minx_str)
            miny = float(miny_str)
            maxx = float(maxx_str)
            maxy = float(maxy_str)
            points_array = [[minx, miny], [maxx, miny],
                            [maxx, maxy], [minx, maxy]]
            shape_dict["points"] = points_array
            shape_dict["group_id"] = None
            shape_dict["shape_type"] = "polygon"
            shape_dict["flags"] = {}
            shapes_array.append(shape_dict)
        json_file_dict = self.__build_lableme_json_dict(shapes_array, pic_file_path)
        self.__write_json_file(json_file_dict, json_file_path)

    # HRSC转为labelme
    def HRSC2Labelme(self, xml_file_path, pic_file_path, json_file_path, label_name):
        tree = ET.parse(xml_file_path)
        shapes_array = []
        HRSC_Objects = tree.find('HRSC_Objects')
        if len(HRSC_Objects.findall('HRSC_Object')) > 0:
            for obj in HRSC_Objects.findall('HRSC_Object'):
                shape_dict = {}
                shape_dict["label"] = label_name
                minx_str = obj.find('box_xmin').text
                miny_str = obj.find('box_ymin').text
                maxx_str = obj.find('box_xmax').text
                maxy_str = obj.find('box_ymax').text
                minx = float(minx_str)
                miny = float(miny_str)
                maxx = float(maxx_str)
                maxy = float(maxy_str)
                points_array = [[minx, miny], [maxx, miny],
                                [maxx, maxy], [minx, maxy]]
                shape_dict["points"] = points_array
                shape_dict["group_id"] = None
                shape_dict["shape_type"] = "polygon"
                shape_dict["flags"] = {}
                shapes_array.append(shape_dict)
            json_file_dict = self.__build_lableme_json_dict(shapes_array, pic_file_path)
            self.__write_json_file(json_file_dict, json_file_path)
        else:
            print("当前图片的标签数据为空")

    # 根据labelme标签数据生成二值图
    def build_binary_image_by_lableme(self, input_pic_file_path, result_pic_file_path, json_file_path):
        while_region_array = []
        with open(json_file_path, 'r', encoding='utf8') as fp:
            json_data = json.load(fp)
            shapes_array = json_data.get("shapes")
            for shape_obj in shapes_array:
                points_array = shape_obj.get("points")
                region_data = []
                for each_point in points_array:
                    region_data.append(int(each_point[0]))
                    region_data.append(int(each_point[1]))
                while_region_array.append(region_data)
        ImageHelper.build_binary_image(input_pic_file_path, result_pic_file_path, while_region_array)

    # 将二值图mask图片转成labelme标签文件
    # 有个问题，如果mask是连着的，生成的json也是连接的，没法分成一个一个单独的标注目标
    def build_labelme_json_by_binary_image(self, label_name, mask_pic_file_path, labelme_json_file_path):
        # [[(x1,y1),(x2,y2)...(xn,yn)],[...]]
        polygons = AIHelper.mask_to_polygon(mask_pic_file_path)
        shapes_array = []
        for polygon in polygons:
            shape_dict = {}
            shape_dict["label"] = label_name
            shape_dict["points"] = polygon
            shape_dict["group_id"] = None
            shape_dict["shape_type"] = "polygon"
            shape_dict["flags"] = {}
            shapes_array.append(shape_dict)
        if len(shapes_array) > 0:
            json_file_dict = self.__build_lableme_json_dict(shapes_array, mask_pic_file_path)
            self.__write_json_file(json_file_dict, labelme_json_file_path)
        else:
            print("当前二值图的标签数据为空")

    # 将mask二值图转换为shp文件
    def convert_mask_pic_to_shape_file(self, mask_pic_file_path, gdal_transform, shp_path):
        AIHelper.convert_mask_to_shape(mask_pic_file_path, gdal_transform, None, shp_path, None)

    # 得到VEDAI标签文件里的类型
    def get_class_name_array_in_VEDAI_txt(self, txt_file_path):
        class_name_array = []
        txtFile = open(txt_file_path)
        txtList = txtFile.readlines()
        for j in txtList:
            oneline = j.strip().split(" ")
            class_name = oneline[3]
            if class_name not in class_name_array:
                class_name_array.append(class_name)
        return class_name_array

    # VEDAI转换为pascalVoc
    def vedai2PascalVoc(self, txt_file_path, xml_file_path, pic_file_path, class_name):
        # img_data = cv2.imread(pic_file_path)
        img_data = cv2.imdecode(np.fromfile(pic_file_path, dtype=np.uint8), -1)
        txt_data = open(txt_file_path, 'r').readlines()
        boxes_all = self.__format_vedai_label(txt_data, class_name)
        if len(boxes_all) > 0:
            self.__vedai_save_to_pascal_xml(xml_file_path, img_data.shape[0], img_data.shape[1], boxes_all)
        else:
            print("当前图片标签数据为空")

    # 内部函数，转换为pascalvoc
    def __vedai_save_to_pascal_xml(self, save_path, im_height, im_width, objects_axis):
        im_depth = 0
        object_num = len(objects_axis)
        doc = Document()

        annotation = doc.createElement('annotation')
        doc.appendChild(annotation)

        folder = doc.createElement('folder')
        folder_name = doc.createTextNode('VOC2007')
        folder.appendChild(folder_name)
        annotation.appendChild(folder)

        filename = doc.createElement('filename')
        filename_name = doc.createTextNode(save_path.split('\\')[-1])
        filename.appendChild(filename_name)
        annotation.appendChild(filename)

        source = doc.createElement('source')
        annotation.appendChild(source)

        database = doc.createElement('database')
        database.appendChild(doc.createTextNode('The VOC2007 Database'))
        source.appendChild(database)

        annotation_s = doc.createElement('annotation')
        annotation_s.appendChild(doc.createTextNode('PASCAL VOC2007'))
        source.appendChild(annotation_s)

        image = doc.createElement('image')
        image.appendChild(doc.createTextNode('flickr'))
        source.appendChild(image)

        flickrid = doc.createElement('flickrid')
        flickrid.appendChild(doc.createTextNode('322409915'))
        source.appendChild(flickrid)

        owner = doc.createElement('owner')
        annotation.appendChild(owner)

        flickrid_o = doc.createElement('flickrid')
        flickrid_o.appendChild(doc.createTextNode('knautia'))
        owner.appendChild(flickrid_o)

        name_o = doc.createElement('name')
        name_o.appendChild(doc.createTextNode('dear_jing'))
        owner.appendChild(name_o)

        size = doc.createElement('size')
        annotation.appendChild(size)
        width = doc.createElement('width')
        width.appendChild(doc.createTextNode(str(im_width)))
        height = doc.createElement('height')
        height.appendChild(doc.createTextNode(str(im_height)))
        depth = doc.createElement('depth')
        depth.appendChild(doc.createTextNode(str(im_depth)))
        size.appendChild(width)
        size.appendChild(height)
        size.appendChild(depth)
        segmented = doc.createElement('segmented')
        segmented.appendChild(doc.createTextNode('0'))
        annotation.appendChild(segmented)
        for i in range(object_num):
            objects = doc.createElement('object')
            annotation.appendChild(objects)
            object_name = doc.createElement('name')
            object_name.appendChild(doc.createTextNode(str(int(objects_axis[i][-1]))))
            objects.appendChild(object_name)
            pose = doc.createElement('pose')
            pose.appendChild(doc.createTextNode('Unspecified'))
            objects.appendChild(pose)
            truncated = doc.createElement('truncated')
            truncated.appendChild(doc.createTextNode(str(int(objects_axis[i][9]))))
            objects.appendChild(truncated)
            difficult = doc.createElement('difficult')
            difficult.appendChild(doc.createTextNode(str(int(objects_axis[i][8]))))
            objects.appendChild(difficult)
            polygon = doc.createElement('polygon')
            objects.appendChild(polygon)

            x0 = doc.createElement('x0')
            x0.appendChild(doc.createTextNode(str(int(objects_axis[i][0]))))
            polygon.appendChild(x0)
            y0 = doc.createElement('y0')
            y0.appendChild(doc.createTextNode(str(int(objects_axis[i][4]))))
            polygon.appendChild(y0)

            x1 = doc.createElement('x1')
            x1.appendChild(doc.createTextNode(str(int(objects_axis[i][1]))))
            polygon.appendChild(x1)
            y1 = doc.createElement('y1')
            y1.appendChild(doc.createTextNode(str(int(objects_axis[i][5]))))
            polygon.appendChild(y1)

            x2 = doc.createElement('x2')
            x2.appendChild(doc.createTextNode(str(int(objects_axis[i][2]))))
            polygon.appendChild(x2)
            y2 = doc.createElement('y2')
            y2.appendChild(doc.createTextNode(str(int(objects_axis[i][6]))))
            polygon.appendChild(y2)

            x3 = doc.createElement('x3')
            x3.appendChild(doc.createTextNode(str(int(objects_axis[i][3]))))
            polygon.appendChild(x3)
            y3 = doc.createElement('y3')
            y3.appendChild(doc.createTextNode(str(int(objects_axis[i][7]))))
            polygon.appendChild(y3)

        f = open(save_path, 'w')
        f.write(doc.toprettyxml(indent=''))
        f.close()

    # 内部函数，格式化vedai
    def __format_vedai_label(self, txt_list, class_name):
        # class_list = ['plane', 'boat', 'camping_car', 'car', 'pick-up', 'tractor', 'truck', 'van', 'vehicle']
        class_list = {'plane': 31, 'boat': 23, 'camping_car': 5, 'car': 1, 'pick-up': 11, 'tractor': 4, 'truck': 2,
                      'van': 9,
                      'vehicle': 10, 'others': 0}
        format_data = []

        for i in txt_list:
            if len(i.split(' ')) < 14:
                continue
            flag = False
            for k, v in class_list.items():
                if v == int(i.split(' ')[3].split('\n')[0]):
                    if class_name == "AllClass" or i.split(' ')[3].split('\n')[0] == class_name:
                        format_data.append(
                            [float(xy) for xy in i.split(' ')[6:14]] + [int(x) for x in i.split(' ')[4:6]] + [v]
                        )
                        flag = True
            # if not flag:
            #     format_data.append(
            #         [float(xy) for xy in i.split(' ')[6:14]] + [int(x) for x in i.split(' ')[4:6]] + ['others']
            #     )

        return np.array(format_data)

    def sample_and_label_augment(self, image_path, json_path, image_augment_path, json_augment_path, label_name,
                                 image_file_suffix):

        # 读取图像和LabelMe格式的JSON标注数据
        with open(json_path, 'r') as f:
            labelme_data = json.load(f)

        # 读取图像
        image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)

        # 提取LabelMe格式的标注信息
        shapes = labelme_data['shapes']

        # 提取标注框
        bbs = []
        for shape in shapes:
            points = shape['points']
            x, y, w, h = cv2.boundingRect(np.array(points).astype(int))
            bbs.append(BoundingBox(x1=x, y1=y, x2=x + w, y2=y + h))

        # 创建BoundingBoxesOnImage对象
        bbs_on_image = BoundingBoxesOnImage(bbs, shape=image.shape)

        # 定义图像增广器
        augmenter = iaa.Sequential([
            iaa.Fliplr(0.5),  # 左右翻转
            iaa.Flipud(0.5),  # 上下翻转
            iaa.Affine(rotate=(-45, 45)),  # 旋转
            iaa.GaussianBlur(sigma=(0, 0.6)),  # 高斯模糊
            iaa.Multiply((0.5, 1.5), per_channel=0.5),  # 亮度调整
        ])

        # 进行图像和标注数据增广
        augmented_image, augmented_bbs_on_image = augmenter(image=image, bounding_boxes=bbs_on_image)
        augmented_bbs_on_image = augmented_bbs_on_image.clip_out_of_image()

        cv2.imencode(image_file_suffix, augmented_image)[1].tofile(image_augment_path)

        augmented_shapes = []
        for bb in augmented_bbs_on_image.bounding_boxes:
            x, y, w, h = bb.x1, bb.y1, bb.x2 - bb.x1, bb.y2 - bb.y1
            points = [[float(x), float(y)], [float(x + w), float(y)], [float(x + w), float(y + h)],
                      [float(x), float(y + h)]]
            augmented_shapes.append({'label': label_name, 'points': points, 'shape_type': 'polygon'})

        # 更新LabelMe格式的标注数据
        labelme_data['shapes'] = augmented_shapes
        labelme_data['imagePath'] = os.path.split(image_augment_path)[1]

        # 将增广后的标注数据保存
        with open(json_augment_path, 'w') as f:
            json.dump(labelme_data, f, default=lambda x: x.tolist() if isinstance(x, np.ndarray) else x)

    # 图像增广（上下翻转、左右翻转、旋转、模糊、增亮等）
    # 包括原始图片和标签二值图图片
    def samples_augmentation2(self, input_image_folder, input_label_folder, output_image_folder,
                              label_name, output_label_folder, image_aug_suffix):

        # 遍历原始图片文件夹
        # 对采集影像和二值图标注影像进行增广
        for filename in os.listdir(input_image_folder):
            file_suffix = os.path.splitext(filename)[1]
            if file_suffix.lower() in [".jpg", ".jpep", ".png", ".bmp"]:
                print("对{}图片进行增广处理".format(filename))
                # 构建原始图片文件路径和标签文件路径
                image_path = os.path.join(input_image_folder, filename)
                json_path = os.path.join(input_label_folder, os.path.splitext(filename)[0] + ".json")
                # 保存增强后的原始图片和标签文件
                if not os.path.exists(output_image_folder):
                    os.makedirs(output_image_folder)
                if not os.path.exists(output_label_folder):
                    os.makedirs(output_label_folder)
                image_aug_path = os.path.join(output_image_folder,
                                              os.path.splitext(filename)[0] + image_aug_suffix + file_suffix)
                json_aug_path = os.path.join(output_label_folder,
                                             os.path.splitext(filename)[0] + image_aug_suffix + ".json")
                self.sample_and_label_augment(image_path, json_path, image_aug_path, json_aug_path, label_name,
                                              file_suffix)

        print("数据增强完成")

    # 图像增广（上下翻转、左右翻转、随机旋转）
    # 包括原始图片和标签二值图图片
    def samples_augmentation(self, input_image_folder, input_mask_folder, output_image_folder,
                             output_mask_folder, label_name, output_label_folder):

        # 定义增强函数
        def apply_augmentation(image, mask, augmentation):
            augmented_image = augmentation(image)
            augmented_mask = augmentation(mask)
            return augmented_image, augmented_mask

        # 增强操作函数
        def flip_horizontal(image):
            return image.transpose(Image.FLIP_LEFT_RIGHT)

        def flip_vertical(image):
            return image.transpose(Image.FLIP_TOP_BOTTOM)

        def random_rotation(image, max_angle=30):
            angle = random.uniform(-max_angle, max_angle)
            return image.rotate(angle)

        # 遍历原始图片文件夹
        # 对采集影像和二值图标注影像进行增广
        for filename in os.listdir(input_image_folder):
            if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg") or filename.lower().endswith(
                    ".png") or filename.lower().endswith(".bmp"):
                print("对{}图片进行增广处理".format(filename))
                # 构建原始图片文件路径和标签文件路径
                image_path = os.path.join(input_image_folder, filename)
                mask_filename = filename
                mask_path = os.path.join(input_mask_folder, mask_filename)

                # 打开原始图片和标签文件
                original_image = Image.open(image_path)
                binary_mask = Image.open(mask_path)

                # 随机选择一种增强方式
                # 返回函数名
                augmentation = random.choice([flip_horizontal, flip_vertical, random_rotation])

                # 应用增强
                augmented_image, augmented_mask = apply_augmentation(original_image, binary_mask, augmentation)

                # 保存增强后的原始图片和标签文件
                if not os.path.exists(output_mask_folder):
                    os.makedirs(output_mask_folder)
                if not os.path.exists(output_image_folder):
                    os.makedirs(output_image_folder)
                out_image_path = os.path.join(output_image_folder, filename)
                out_mask_path = os.path.join(output_mask_folder, mask_filename)
                augmented_image.save(out_image_path)
                augmented_mask.save(out_mask_path)

        # 基于增广后的二值图标注生成labelme json文件
        # 如果二值图是成片的（比如船舶）那json文件可能就会把好几个目标合成一个了
        for out_mask_filename in os.listdir(output_mask_folder):
            if out_mask_filename.lower().endswith(".jpg") or out_mask_filename.lower().endswith(
                    ".jpeg") or out_mask_filename.lower().endswith(
                ".png") or out_mask_filename.lower().endswith(".bmp"):
                print("对增广后的二值图图片{}转换为labelme json文件".format(out_mask_filename))
                out_mask_filepath = os.path.join(output_mask_folder, out_mask_filename)
                # 构建原始图片文件路径和标签文件路径
                json_path = os.path.join(output_label_folder, os.path.splitext(out_mask_filename)[0] + ".json")
                self.build_labelme_json_by_binary_image(label_name, out_mask_filepath, json_path)
        print("数据增强完成")


class SampleHandler:
    def __init__(self):
        pass

    # 从样本中拆分出训练数据和验证数据
    @staticmethod
    def split_train_val_data_of_yolov8(all_image_path, all_label_path, dest_path, class_name, train_radio, valid_radio,
                                       test_radio):
        SampleHandler.init_yolov8_data_dir(dest_path, class_name)
        img_list = os.listdir(all_image_path)
        train_img_list = []
        valid_img_list = []
        test_img_list = []

        # trainImage：训练集的图片
        # - Abyssinian_1.jpg
        # - Abyssinian_10.jpg
        # - Abyssinian_11.jpg
        # 原来的图片是类别名称加后缀数量
        # classes_set = set([i.split("_")[0] for i in img_list])  # 每个类别的名称
        # for cls in classes_set:
        #     cls_list = list(filter(lambda x: x.startswith(cls), img_list))
        #     train_num = int(len(cls_list) * train_radio)
        #     train_img_list += cls_list[:train_num]
        #     valid_img_list += cls_list[train_num:]

        train_num = int(len(img_list) * train_radio)
        valid_num = int(len(img_list) * valid_radio)
        test_num = int(len(img_list) * test_radio)
        train_img_list += img_list[:train_num]
        valid_img_list += img_list[train_num:train_num + valid_num]
        test_img_list += img_list[train_num + valid_num:train_num + valid_num + test_num]

        # 打乱数据
        random.shuffle(train_img_list)
        random.shuffle(valid_img_list)
        random.shuffle(test_img_list)

        print("num of train set is {} ".format(len(train_img_list)))
        print("num of valid set is {} ".format(len(valid_img_list)))
        print("num of test set is {} ".format(len(test_img_list)))
        print(f"total num of dataset is {len(train_img_list) + len(valid_img_list) + len(test_img_list)}")

        yolo_image_dir = os.path.join(dest_path, "datasets", class_name, "images")
        yolo_label_dir = os.path.join(dest_path, "datasets", class_name, "labels")
        SampleHandler.copy_data_to_dest(train_img_list, "train", all_image_path, all_label_path, yolo_image_dir,
                                        yolo_label_dir)
        SampleHandler.copy_data_to_dest(valid_img_list, "val", all_image_path, all_label_path, yolo_image_dir,
                                        yolo_label_dir)
        SampleHandler.copy_data_to_dest(test_img_list, "test", all_image_path, all_label_path, yolo_image_dir,
                                        yolo_label_dir)

        # with open("train.txt", "a+") as f:
        #     for img in train_img_list:
        #         if img.endswith(".jpg"):
        #             f.write("data/custom/images/" + img + "\n")
        # print("train.txt create sucessful!")
        #
        #
        # with open("valid.txt", "a+") as f:
        #     for img in valid_img_list:
        #         if img.endswith(".jpg"):
        #             f.write("data/custom/images/" + img + "\n")
        # print("valid.txt create sucessful!")
        #
        #
        # train_img_dir = "trainImage/"
        # train_img_list = [os.path.join("data/custom/images/", i) for i in sorted(os.listdir(train_img_dir))]
        # train_img_list = list(map(lambda x: x + "\n", train_img_list))
        #
        # val_img_dir = "valImage/"
        # val_img_list = [os.path.join("data/custom/images/", i) for i in sorted(os.listdir(val_img_dir))]
        # val_img_list = list(map(lambda x: x + "\n", val_img_list))
        #
        # with open("train.txt", "w") as f:
        #     f.writelines(train_img_list)
        #
        # with open("val.txt", "w") as f:
        #     f.writelines(val_img_list)

    @staticmethod
    def copy_data_to_dest(img_list, img_usage, all_image_path, all_label_path, yolo_image_dir, yolo_label_dir):
        # 复制数据到指定目录
        for img_name in img_list:
            img_name_prefix = FileHelper.get_file_name_prefix(img_name)
            label_txt_path = os.path.join(all_label_path, img_name_prefix + ".txt")
            img_path = os.path.join(all_image_path, img_name)
            # 复制图片
            copy_dest_image_path = os.path.join(yolo_image_dir, img_usage + "2017")
            shutil.copy(img_path, copy_dest_image_path)
            print("复制图片文件:从{}到{}".format(img_path, copy_dest_image_path))
            copy_dest_label_path = os.path.join(yolo_label_dir, img_usage + "2017")
            # 复制样本
            shutil.copy(label_txt_path, copy_dest_label_path)
            print("复制标注文件：从{}到{}".format(img_path, copy_dest_label_path))

    # 初始化yolov8需要的数据目录
    @staticmethod
    def init_yolov8_data_dir(dest_path, class_name):
        yolo_image_dir = os.path.join(dest_path, "datasets", class_name, "images")
        yolo_train_image_dir = os.path.join(yolo_image_dir, "train2017")
        yolo_val_image_dir = os.path.join(yolo_image_dir, "val2017")
        yolo_test_image_dir = os.path.join(yolo_image_dir, "test2017")
        yolo_label_dir = os.path.join(dest_path, "datasets", class_name, "labels")
        yolo_train_label_dir = os.path.join(yolo_label_dir, "train2017")
        yolo_val_label_dir = os.path.join(yolo_label_dir, "val2017")
        yolo_test_label_dir = os.path.join(yolo_label_dir, "test2017")
        FileHelper.mkdirs(
            [yolo_image_dir, yolo_train_image_dir, yolo_val_image_dir, yolo_test_image_dir, yolo_label_dir,
             yolo_train_label_dir, yolo_val_label_dir, yolo_test_label_dir])


# 主入口,进行测试
if __name__ == '__main__':

    # pascalxml转labelme成单元测试方法
    def pascalVoc2Labelme_test(file_converter):
        xml_file_path = "G:\\AI\\train_data\\样本\\oiltank\\Annotation\\xml\\oiltank_1.xml"
        # class_file_path = "G:\\AI\\train_data\\样本\\oiltank\\Annotation\\classes.names"
        pic_file_path = "G:\\AI\\train_data\\样本\\oiltank\\JPEGImages\\oiltank_1.jpg"
        json_file_path = "G:\\AI\\train_data\\样本\\oiltank\\Annotation\\labelme\\oiltank_1.json"
        file_converter.pascalVoc2Labelme(xml_file_path, pic_file_path, json_file_path)


    def build_binary_image_by_lableme_test(file_converter):
        input_pic_file_path = "G:\\AI\\train_data\\样本\\oiltank\\JPEGImages\\oiltank_1.jpg"
        result_pic_file_path = "G:\\AI\\train_data\\样本\\oiltank\\BianryImages\\oiltank_1.jpg"
        json_file_path = "G:\\AI\\train_data\\样本\\oiltank\\Annotation\\labelme\\oiltank_1.json"
        file_converter.build_binary_image_by_lableme(input_pic_file_path, result_pic_file_path, json_file_path)


    def UCAS2Labelme_test(file_converter):
        txt_file_path = "G:\\AI\\train_data\\样本\\UCAS_AOD\\中科院大学高清航拍目标数据集合\\CAR\\P0001.txt"
        pic_file_path = "G:\\AI\\train_data\\样本\\UCAS_AOD\\中科院大学高清航拍目标数据集合\\CAR\\P0001.png"
        json_file_path = "G:\\AI\\train_data\\样本\\UCAS_AOD\\中科院大学高清航拍目标数据集合\\CAR\\P0001.json"
        file_converter.UCAS2Labelme(txt_file_path, pic_file_path, json_file_path, "car")


    def HRSC2Labelme_test(file_converter):
        xml_file_path = "G:\\AI\\train_data\\样本\\HRSC2016\\HRSC\\HRSC2016\\FullDataSet\\Annotations\\100000001.xml"
        pic_file_path = "G:\\AI\\train_data\\样本\\HRSC2016\\HRSC\\HRSC2016\\FullDataSet\\AllImages\\100000001.bmp"
        json_file_path = "G:\\AI\\train_data\\样本\\HRSC2016\\HRSC\\HRSC2016\\FullDataSet\\labelme\\100000001.json"
        file_converter.HRSC2Labelme(xml_file_path, pic_file_path, json_file_path, "boat")


    def Labelme2Yolo_test(file_converter):
        json_file_path = "G:\\AI\\train_data\\样本\\send\\火电站\高矮烟囱_汇总\\LabelImages\\00004_3.json"
        class_file_path = "G:\\AI\\train_data\\样本\\send\\火电站\\高矮烟囱_汇总\\Yolo\\classes.names"
        txt_file_path = "G:\\AI\\train_data\\样本\\send\\火电站\\高矮烟囱_汇总\\Yolo\\labels\\00004_3.txt"
        file_converter.labelme2Yolo(json_file_path, class_file_path, txt_file_path)


    def AugmentSample_test(file_converter):
        input_image_folder = "G:\\AI\\train_data\\样本\\send\\车辆\\SampleImages"
        input_mask_folder = "G:\\AI\\train_data\\样本\send\\车辆\\BianryImages"
        input_label_folder = "G:\\AI\\train_data\\样本\send\\车辆\\LabelImages"
        output_image_folder = "G:\\AI\\train_data\\样本\\send\\车辆\\SampleImages_Augment"
        output_mask_folder = "G:\\AI\\train_data\\样本\send\\车辆\\BianryImages_Augment"
        output_label_folder = "G:\\AI\\train_data\\样本\send\\车辆\\LabelImages_Augment"
        label_name = "CAR"
        image_aug_suffix = "_aug"
        # file_converter.samples_augmentation(input_image_folder, input_mask_folder, output_image_folder,
        #                                    output_mask_folder, label_name, output_label_folder)

        file_converter.samples_augmentation2(input_image_folder, input_label_folder, output_image_folder,
                                             label_name, output_label_folder, image_aug_suffix)


    try:

        file_converter = FileFormatConverter()
        # 测试pascalvoc转换labelme
        # pascalVoc2Labelme_test(file_converter)
        # 测试lablme标签生成二值图
        # build_binary_image_by_lableme_test(file_converter)
        # 测试UCAS转labelme
        # UCAS2Labelme_test(file_converter)
        # 测试HRSC转labelme
        # HRSC2Labelme_test(file_converter)
        # 测试labelme转yolo
        # Labelme2Yolo_test(file_converter)

        # 测试样本数据增广
        # AugmentSample_test(file_converter)
        input_json_file = "G:\\AI\\train_data\\样本\\飞机船舶\\AI样本\\船舶\\ship1581.json"
        output_json_file = "G:\\AI\\train_data\\样本\\飞机船舶\\AI样本\\船舶\\ship1581_rect.json"
        file_converter.convert_seg_points_to_obl_rect_of_labelme(input_json_file, output_json_file)




    except Exception as tm_exp:
        print("测试用例失败：{}".format(str(tm_exp)))
