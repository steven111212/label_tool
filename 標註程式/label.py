from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import numpy as np
from PyQt5.QtGui import QPixmap,QPainter, QColor, QPainterPathStroker
import sys
from PyQt5.QtWidgets import QApplication,QDialog,QFileDialog, QComboBox, QMainWindow, QMenu, QAction, QLineEdit
from PyQt5.QtCore import Qt
from scipy.spatial import ConvexHull
import json
import base64
import io
import sqlite3
import re
import os.path as osp
import os
import FITiDB
from shapely.geometry import LineString




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("MainWindow")
        MainWindow.resize(1200, 1000)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(30, 70, 800, 600))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)
  
        self.Output_button = QtWidgets.QPushButton(self.centralwidget)
        self.Output_button.setGeometry(QtCore.QRect(200, 20, 51, 31))
        self.Output_button.setText("Output")
        self.Output_button.clicked.connect(self.Output_points)
        self.Output_mask_button = QtWidgets.QPushButton(self.centralwidget)
        self.Output_mask_button.setGeometry(QtCore.QRect(270, 20, 80, 31))
        self.Output_mask_button.setText("Output_mask")
        self.Output_mask_button.clicked.connect(self.Output_mask)
        self.Poly_finish_button = QtWidgets.QPushButton(self.centralwidget)
        self.Poly_finish_button.setGeometry(QtCore.QRect(100, 20, 80, 31))
        self.Poly_finish_button.setText("Poly_finish")
        self.Poly_finish_button.clicked.connect(self.Poly_finish)
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(30, 20, 51, 31))
        self.toolButton.setObjectName("toolButton")
        self.toolButton.setText("Open File")
        self.toolButton.clicked.connect(self.read)   
        self.orient_button = QtWidgets.QPushButton(self.centralwidget)
        self.orient_button.setGeometry(QtCore.QRect(370, 20, 80, 31))
        self.orient_button.setText("回傳定位")
        self.orient_button.clicked.connect(self.Orient_Value)
        # self.input_box = QLineEdit(self)
        # self.input_box.setPlaceholderText("請在此輸入字串")
        # self.input_box.setGeometry(10, 10, 300, 30)  
     
        
        MainWindow.setCentralWidget(self.centralwidget)

        # Connect zoom in/out events
        self.graphicsView.wheelEvent = self.zoom_in_out
        

        # 创建操作
        self.rectangle_action = QAction("Rectangle", self)
        self.polygon_action = QAction("Polygon", self)
        self.frame_action = QAction("Framed",self)
        self.shade_action = QAction("Rectangle",self)
        self.poly_shade =   QAction("Polygon",self)
        self.remove_action = QAction("Remove",self)
        self.size25_action = QAction("Smear25", self)
        self.size50_action = QAction("Smear50", self)
        self.size75_action = QAction("Smear75", self)
        self.size100_action = QAction("Smear100", self)
        self.frame_shade = QAction("Framed",self)
        self.mask_action = QAction("Rectangle",self)
        self.mask_poly_action = QAction("Polygon", self)
        self.orient_action = QAction("Rectangle", self)
        self.orient_poly_action = QAction("Polygon", self)
        self.size50_orient_action = QAction("Smear50", self)
        self.size100_orient_action = QAction("Smear100", self)
        self.size150_orient_action = QAction("Smear150", self)
        self.size200_orient_action = QAction("Smear200", self)

        
        self.rectangle_action.triggered.connect(self.draw_rectangle)
        self.polygon_action.triggered.connect(self.draw_polygon)
        self.frame_action.triggered.connect(self.draw_frame)
        self.shade_action.triggered.connect(self.Shade_Rectangle)
        self.poly_shade.triggered.connect(self.Shade_Polygon)
        self.frame_shade.triggered.connect(self.Shade_Framed)
        self.remove_action.triggered.connect(self.Remove)
        self.mask_action.triggered.connect(self.Mask_Rectangle)
        self.mask_poly_action.triggered.connect(self.Mask_Polygon)
        self.orient_action.triggered.connect(self.Orient_Rectangle)
        self.orient_poly_action.triggered.connect(self.Orient_Polygon)
        

        self.size25_action.triggered.connect(lambda: self.draw_smear(2.5))
        self.size50_action.triggered.connect(lambda: self.draw_smear(5))
        self.size75_action.triggered.connect(lambda: self.draw_smear(7.5))
        self.size100_action.triggered.connect(lambda: self.draw_smear(10))
        
        self.size50_orient_action.triggered.connect(lambda: self.Orient_Smear(5))
        self.size100_orient_action.triggered.connect(lambda: self.Orient_Smear(10))
        self.size150_orient_action.triggered.connect(lambda: self.Orient_Smear(15))
        self.size200_orient_action.triggered.connect(lambda: self.Orient_Smear(20))

        # 添加操作到菜单
        label_menu = self.menuBar().addMenu("Label")
        label_menu.addAction(self.rectangle_action)
        label_menu.addAction(self.polygon_action)
        label_menu.addAction(self.frame_action)
        label_menu.addAction(self.size25_action)
        label_menu.addAction(self.size50_action)
        label_menu.addAction(self.size75_action)
        label_menu.addAction(self.size100_action)
        label_menu.addAction(self.remove_action)

        shade_menu = self.menuBar().addMenu("Shade")
        shade_menu.addAction(self.shade_action)
        shade_menu.addAction(self.poly_shade)
        shade_menu.addAction(self.frame_shade)
        shade_menu.addAction(self.remove_action)

        mask_menu = self.menuBar().addMenu("Mask")
        mask_menu.addAction(self.mask_action)
        mask_menu.addAction(self.mask_poly_action)
        mask_menu.addAction(self.remove_action)
        
        orient_menu = self.menuBar().addMenu("定位")
        orient_menu.addAction(self.orient_action)
        orient_menu.addAction(self.orient_poly_action)
        orient_menu.addAction(self.size50_orient_action)
        orient_menu.addAction(self.size100_orient_action)
        orient_menu.addAction(self.size150_orient_action)
        orient_menu.addAction(self.size200_orient_action)
        orient_menu.addAction(self.remove_action)
       
    
        
class label(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(label,self).__init__()
        self.setupUi(self)
        self.image_loaded = False
        self.rect_start_point = None
        self.rect_item = None
        self.polygon_item = None
        self.smear_item = None
        self.frame_item = None
        self.border_item = None
         
        
    def read(self):

        
        #讀檔
        filename, _ = QFileDialog.getOpenFileName(self, "Open image", "", "Image files (*.jpg *.png *.bmp)")
        arr = filename.split('/')
        self.name = arr[-1].split('.')[0]
        path = ''
        print(arr[-1])
        for i in range(len(arr)-1):
            path = path+arr[i]+'/'
        print(path)
        self.path = path
        path = path + self.name+'.json'
        print(self.name)
    
        
        try:
            #讀圖片檔
            self.img = cv2.imread(filename)
            imageData = self.load_image_file(filename)
            
            #圖片顯示在介面
            self.photo = QPixmap(filename)
            height, width, channel = self.img.shape
            bytesPerLine = 3 * width
            qImg = QtGui.QImage(self.img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()
            self.photo = QPixmap.fromImage(qImg).scaled(self.graphicsView.width(), self.graphicsView.height(), Qt.KeepAspectRatio)
            self.graphicsView.scene = QtWidgets.QGraphicsScene(self)
            self.graphicsView.setScene(self.graphicsView.scene)
            self.graphicsView.scene.clear()
            self.graphicsView.scene.addPixmap(self.photo)
            self.space = (self.photo.width() < self.graphicsView.width() or self.photo.height() < self.graphicsView.height())
            self.fill =  not (self.photo.width() < self.graphicsView.width() or self.photo.height() < self.graphicsView.height())
            self.scaleX = height/self.graphicsView.height()
            self.scaleY = width/self.graphicsView.width()
            self.scalefactor = max(self.scaleX, self.scaleY)
            self.pixmap_item = QtWidgets.QGraphicsPixmapItem()
            self.graphicsView.scene.addItem(self.pixmap_item)
            
            self.image_loaded = True
            self.rectangle = False
            self.polygon = False 
            self.frame = False
            self.smear = False
            self.remove = False
            self.shade_rectangle = False
            self.shade_polygon = False
            self.shade_frame = False
            self.maskk = False
            self.mask_polygon = False
            self.orient = False
            self.orient_polygon = False
            self.graphheight = height
            self.graphwidth = width
            self.graphicsView.mousePressEvent = self.PressEvent
            self.graphicsView.mouseReleaseEvent = self.ReleaseEvent
            self.graphicsView.mouseMoveEvent = self.MoveEvent
            self.dict = {}
            self.dict.setdefault("imagePath", arr[-1])
            self.dict.setdefault("imageHeight", height)
            self.dict.setdefault("imageWidth", width)
            self.dict.setdefault("imageData", imageData)
            self.dict.setdefault("shapes","")
            FITiDB.Labelinfo(arr[-1], height, width).add()
            self.dict_mask = {}
            self.dict_mask.setdefault("imageHeight", height)
            self.dict_mask.setdefault("imageWidth", width)
            self.dict.setdefault("shapes","")
            
            #檢查是否有標註檔，有的話把標註內容添加上去
            if os.path.isfile(path):
                
                print("檔案存在。")
                with open(path, "r") as f:
                    data = json.load(f)

                if self.fill:
                    for shape in data["shapes"]:
                        label = shape["label"]
                        points = shape["points"]
                        shape_type = shape['shape_type']
                        # if shape_type == "rectangle" and label == 'defect':
                        #     rect_start_point = QtCore.QPointF(points[0][0]/self.scaleX, points[0][1]/self.scaleY)
                        #     rect_end_point = QtCore.QPointF(points[2][0]/self.scaleX, points[2][1]/self.scaleY )
                        #     rect_item = QtWidgets.QGraphicsRectItem(QtCore.QRectF(rect_start_point, rect_end_point))
                        #     pen = QtGui.QPen(QtGui.QColor("red"))
                        #     pen.setWidth(2)
                        #     rect_item.setPen(pen)
                        #     self.graphicsView.scene.addItem(rect_item)

                        # elif shape_type == "rectangle" and label == 'shade':
                        #     rect_start_point = QtCore.QPointF(points[0][0]/self.scaleX, points[0][1]/self.scaleY)
                        #     rect_end_point = QtCore.QPointF(points[2][0]/self.scaleX, points[2][1]/self.scaleY )
                        #     rect_item = QtWidgets.QGraphicsRectItem(QtCore.QRectF(rect_start_point, rect_end_point))
                        #     pen = QtGui.QPen(QtGui.QColor("black"))
                        #     pen.setWidth(2)
                        #     rect_item.setPen(pen)
                        #     brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128), QtCore.Qt.DiagCrossPattern)
                        #     rect_item.setBrush(brush)
                        #     self.graphicsView.scene.addItem(rect_item)

                        if shape_type == "polygon" and label == "defect":
                            polygon = QtGui.QPolygonF([QtCore.QPointF(x/self.scaleX, y/self.scaleY) for x, y in points])
                            polygon_item = QtWidgets.QGraphicsPolygonItem(polygon)
                            self.graphicsView.scene.addItem(polygon_item)
                            pen = QtGui.QPen(QtGui.QColor("red"))
                            pen.setWidth(2)
                            polygon_item.setPen(pen)

                        elif shape_type == "polygon" and label == "shade":
                            polygon = QtGui.QPolygonF([QtCore.QPointF(x/self.scaleX, y/self.scaleY) for x, y in points])
                            polygon_item = QtWidgets.QGraphicsPolygonItem(polygon)
                            self.graphicsView.scene.addItem(polygon_item)
                            pen = QtGui.QPen(QtGui.QColor("black"))
                            pen.setWidth(2)
                            polygon_item.setPen(pen)
                            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128), QtCore.Qt.DiagCrossPattern)
                            polygon_item.setBrush(brush)

                        elif shape_type == "frame" and label == "defect":
                            path = QtGui.QPainterPath()
                            path_item = QtWidgets.QGraphicsPathItem()
                            path_item.setPen(QtGui.QPen(QtGui.QColor("red"), 2))
                            self.graphicsView.scene.addItem(path_item)
                            path.moveTo(points[0][0]/self.scaleX, points[0][1]/self.scaleY)
                            for point in points[1:]:
                                path.lineTo(point[0]/self.scaleX, point[1]/self.scaleY)
                            path_item.setPath(path)

                        elif shape_type == "frame" and label == "shade":
                            path = QtGui.QPainterPath()
                            path_item = QtWidgets.QGraphicsPathItem()
                            path_item.setPen(QtGui.QPen(QtGui.QColor("black"), 2))
                            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128), QtCore.Qt.DiagCrossPattern)
                            path_item.setBrush(brush)
                            self.graphicsView.scene.addItem(path_item)
                            path.moveTo(points[0][0]/self.scaleX, points[0][1]/self.scaleY)
                            for point in points[1:]:
                                path.lineTo(point[0]/self.scaleX, point[1]/self.scaleY)
                            path_item.setPath(path)
                        
                elif self.space:
                    for shape in data["shapes"]:
                        label = shape["label"]
                        points = shape["points"]
                        shape_type = shape['shape_type']
                        # if shape_type == "rectangle" and label == 'defect':
                        #     rect_start_point = QtCore.QPointF(points[0][0]/self.scalefactor, points[0][1]/self.scalefactor)
                        #     rect_end_point = QtCore.QPointF(points[2][0]/self.scalefactor, points[2][1]/self.scalefactor )
                        #     rect_item = QtWidgets.QGraphicsRectItem(QtCore.QRectF(rect_start_point, rect_end_point))
                        #     pen = QtGui.QPen(QtGui.QColor("red"))
                        #     pen.setWidth(2)
                        #     rect_item.setPen(pen)
                        #     self.graphicsView.scene.addItem(rect_item)

                        # elif shape_type == "rectangle" and label == 'shade':
                        #     rect_start_point = QtCore.QPointF(points[0][0]/self.scalefactor, points[0][1]/self.scalefactor)
                        #     rect_end_point = QtCore.QPointF(points[2][0]/self.scalefactor, points[2][1]/self.scalefactor )
                        #     rect_item = QtWidgets.QGraphicsRectItem(QtCore.QRectF(rect_start_point, rect_end_point))
                        #     pen = QtGui.QPen(QtGui.QColor("black"))
                        #     pen.setWidth(2)
                        #     rect_item.setPen(pen)
                        #     brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128), QtCore.Qt.DiagCrossPattern)
                        #     rect_item.setBrush(brush)
                        #     self.graphicsView.scene.addItem(rect_item)

                        if shape_type == "polygon"  and label == "defect":
                            polygon = QtGui.QPolygonF([QtCore.QPointF(x/self.scalefactor, y/self.scalefactor) for x, y in points])
                            polygon_item = QtWidgets.QGraphicsPolygonItem(polygon)
                            self.graphicsView.scene.addItem(polygon_item)
                            pen = QtGui.QPen(QtGui.QColor("red"))
                            pen.setWidth(2)
                            polygon_item.setPen(pen)

                        elif shape_type == "polygon" and label == "shade":
                            polygon = QtGui.QPolygonF([QtCore.QPointF(x/self.scalefactor, y/self.scalefactor) for x, y in points])
                            polygon_item = QtWidgets.QGraphicsPolygonItem(polygon)
                            self.graphicsView.scene.addItem(polygon_item)
                            pen = QtGui.QPen(QtGui.QColor("black"))
                            pen.setWidth(2)
                            polygon_item.setPen(pen)
                            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128), QtCore.Qt.DiagCrossPattern)
                            polygon_item.setBrush(brush)

                        elif shape_type == "frame" and label == "defect":
                            path = QtGui.QPainterPath()
                            path_item = QtWidgets.QGraphicsPathItem()
                            path_item.setPen(QtGui.QPen(QtGui.QColor("red"), 2))
                            self.graphicsView.scene.addItem(path_item)
                            path.moveTo(points[0][0]/self.scalefactor, points[0][1]/self.scalefactor)
                            for point in points[1:]:
                                path.lineTo(point[0]/self.scalefactor, point[1]/self.scalefactor)
                            path_item.setPath(path)

                        elif shape_type == "frame" and label == "shade":
                            path = QtGui.QPainterPath()
                            path_item = QtWidgets.QGraphicsPathItem()
                            path_item.setPen(QtGui.QPen(QtGui.QColor("black"), 2))
                            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128), QtCore.Qt.DiagCrossPattern)
                            path_item.setBrush(brush)
                            self.graphicsView.scene.addItem(path_item)
                            path.moveTo(points[0][0]/self.scalefactor, points[0][1]/self.scalefactor)
                            for point in points[1:]:
                                path.lineTo(point[0]/self.scalefactor, point[1]/self.scalefactor)
                            path_item.setPath(path)
            else:
                print("檔案不存在。")
        except:
            print("請確認是否已經讀圖")
            
    #滑鼠滾輪控制圖片大小
    def zoom_in_out(self, event):
        if event.angleDelta().y() > 0:
            # Zoom in
            self.graphicsView.scale(1.2, 1.2)
        else:
            # Zoom out
            self.graphicsView.scale(1/1.2, 1/1.2)

    #矩形標註
    def draw_rectangle(self):
        self.polygon = False
        self.rectangle = True
        self.frame = False
        self.smear = False
        self.remove = False
        self.shade_rectangle = False
        self.shade_polygon = False
        self.shade_frame = False
        self.maskk = False
        self.mask_polygon = False
        self.orient = False
        self.orient_polygon = False
        self.orient_smear = False

        if self.image_loaded:
            print("Draw Rectangle")
            self.graphicsView.mousePressEvent = self.PressEvent
            self.graphicsView.mouseReleaseEvent = self.ReleaseEvent
            self.graphicsView.mouseMoveEvent = self.MoveEvent
        else:
            print("Please load an image first.")

    def PressEvent(self, event):
        if self.rectangle == True and self.image_loaded and event.button() == QtCore.Qt.LeftButton :
            view_pos = event.pos()
            if not self.graphicsView.rect().contains(view_pos):
                return
            scene_pos = self.graphicsView.mapToScene(view_pos)
            self.rect_start_point = scene_pos
            self.rect_item = QtWidgets.QGraphicsRectItem(QtCore.QRectF(self.rect_start_point, self.rect_start_point))
            self.graphicsView.scene.addItem(self.rect_item)
            pen = QtGui.QPen(QtGui.QColor("red"))
            pen.setWidth(2)
            self.rect_item.setPen(pen)
            self.graphicsView.viewport().update()
            event.accept()
        

    def MoveEvent(self, event):
        
        if self.rectangle == True and self.image_loaded and self.rect_start_point is not None and event.buttons() == QtCore.Qt.LeftButton : 
            if self.rect_item is not None:
                self.graphicsView.scene.removeItem(self.rect_item)
            pen = QtGui.QPen(QtGui.QColor("red"))
            pen.setWidth(2)
            view_pos = event.pos()
            scene_pos = self.graphicsView.mapToScene(view_pos)
            rect = QtCore.QRectF(self.rect_start_point, scene_pos).normalized()
            self.rect_item = self.graphicsView.scene.addRect(rect, pen)
            self.graphicsView.viewport().update()


    def ReleaseEvent(self, event):
        
        if self.rectangle == True and self.image_loaded and event.button() == QtCore.Qt.LeftButton and self.rect_item is not None :
            view_pos = event.pos()
            scene_pos = self.graphicsView.mapToScene(view_pos)
            self.rect_end_point = scene_pos
            self.rect_item.setRect(QtCore.QRectF(self.rect_start_point, self.rect_end_point))       
            self.graphicsView.viewport().update()

    #多邊型標註
    def draw_polygon(self):

        self.polygon_item = QtWidgets.QGraphicsPolygonItem() # Create a new QGraphicsPolygonItem object
        self.graphicsView.scene.addItem(self.polygon_item) # Add the polygon item to the scene
        self.smear = False
        self.rectangle = False
        self.polygon = True
        self.frame = False
        self.remove = False
        self.shade = False
        self.shade_rectangle = False
        self.shade_polygon = False
        self.shade_frame = False
        self.maskk = False
        self.mask_polygon = False
        self.orient = False
        self.orient_polygon = False
        self.orient_smear = False
      
        if self.image_loaded:
            print("Draw Polygon")
            self.graphicsView.mousePressEvent = self.PressEventPoly
           
        else:
            print("Please load an image first.")

    def PressEventPoly(self, event):
        if self.polygon == True:
            self.polygon_item.setPen(QtGui.QPen(QtCore.Qt.red, 2))
            sp = self.graphicsView.mapToScene(event.pos())
            lp = self.pixmap_item.mapFromScene(sp)

            poly = self.polygon_item.polygon()
            poly.append(lp)
            
            self.polygon_item.setPolygon(poly)
            self.graphicsView.viewport().update()

    #多邊形完成時觸發這個按鈕才能繪製新的多邊形
    def Poly_finish(self):
        self.polygon_item = None
        self.polygon_item = QtWidgets.QGraphicsPolygonItem() # Create a new QGraphicsPolygonItem object
        self.graphicsView.scene.addItem(self.polygon_item) # Add the polygon item to the scene

    #輸出遮罩檔+寫入DB
    def Output_mask(self):
        self.shapes = []
        if self.image_loaded:
            for item in self.graphicsView.scene.items():
                if isinstance(item, QtWidgets.QGraphicsRectItem) and item.pen().color() == QtGui.QColor("green") and self.fill:
                    dict = {}
                    rect = item.rect()
                    points = []
                    points.append([int(rect.x()*self.scaleX), int(rect.y()*self.scaleY)])
                    points.append([int(rect.x()*self.scaleX), int((rect.y()+rect.height())*self.scaleY)])
                    points.append([int((rect.x()+rect.width())*self.scaleX), int((rect.y()+rect.height())*self.scaleY)])
                    points.append([int((rect.x()+rect.width())*self.scaleX), int(rect.y()*self.scaleY)])     
                    points = self.correction_points(points)
                    print(f"Rectangle: {points}")
                    dict.setdefault("label", "mask")
                    dict.setdefault("points", points)
                    dict.setdefault("shape_type","polygon")
                    self.shapes.append(dict)

                elif isinstance(item, QtWidgets.QGraphicsRectItem) and item.pen().color() == QtGui.QColor("green") and self.space:
                    dict = {}
                    rect = item.rect()
                    points = []
                    points.append([int(rect.x()*self.scalefactor), int(rect.y()*self.scalefactor)])
                    points.append([int(rect.x()*self.scalefactor), int((rect.y()+rect.height())*self.scalefactor)])
                    points.append([int((rect.x()+rect.width())*self.scalefactor), int((rect.y()+rect.height())*self.scalefactor)])
                    points.append([int((rect.x()+rect.width())*self.scalefactor), int(rect.y()*self.scalefactor)]) 
                    points = self.correction_points(points)          
                    print(f"Rectangle: {points}")
                    dict.setdefault("label", "mask")
                    dict.setdefault("points", points)
                    dict.setdefault("shape_type","polygon")
                    self.shapes.append(dict)
                
                elif isinstance(item, QtWidgets.QGraphicsPolygonItem) and item.pen().color() == QtGui.QColor("green") and self.fill:
                    dict = {}
                    poly = item.polygon()
                    points = []
                    for i in range(poly.size()):
                        point = poly.at(i)
                        points.append([int(point.x()*self.scaleX), int(point.y()*self.scaleY)])
                    points = self.correction_points(points)
                    print(f"Polygon: {points}")
                    dict.setdefault("label", "shade")
                    dict.setdefault("points", points)
                    dict.setdefault("shape_type","polygon")
                    self.shapes.append(dict)

                elif isinstance(item, QtWidgets.QGraphicsPolygonItem) and item.pen().color() == QtGui.QColor("green") and self.space:
                    dict = {}
                    poly = item.polygon()
                    points = []
                    for i in range(poly.size()):
                        point = poly.at(i)
                        points.append([int(point.x()*self.scalefactor), int(point.y()*self.scalefactor)])
                    points = self.correction_points(points)
                    print(f"Polygon: {points}")
                    dict.setdefault("label", "defect")
                    dict.setdefault("points", points)
                    dict.setdefault("shape_type","polygon")
                    self.shapes.append(dict)
            self.shapes = self.remove_dicts_with_same_points(self.shapes)
            self.dict_mask['shapes'] = self.shapes
            with open(self.path+"mask.json", "w") as f:
                json.dump(self.dict_mask, f, indent = 4)

            # with open(self.path+"mask.json", "r") as f:
            #     data = json.load(f)

        else:
            print("Please load an image first.")
        

    #輸出標註檔+寫入DB
    def Output_points(self):
        self.shapes = []
        if self.image_loaded:
            for item in self.graphicsView.scene.items():
                if isinstance(item, QtWidgets.QGraphicsRectItem) and item.pen().color() == QtGui.QColor("red") and self.fill:
                    dict = {}
                    rect = item.rect()
                    points = []
                    points.append([int(rect.x()*self.scaleX), int(rect.y()*self.scaleY)])
                    points.append([int(rect.x()*self.scaleX), int((rect.y()+rect.height())*self.scaleY)])
                    points.append([int((rect.x()+rect.width())*self.scaleX), int((rect.y()+rect.height())*self.scaleY)])
                    points.append([int((rect.x()+rect.width())*self.scaleX), int(rect.y()*self.scaleY)])  
                    points = self.correction_points(points)         
                    print(f"Rectangle: {points}")
                    dict.setdefault("label", "defect")
                    dict.setdefault("points", points)
                    dict.setdefault("shape_type","polygon")
                    self.shapes.append(dict)

                elif isinstance(item, QtWidgets.QGraphicsRectItem) and item.pen().color() == QtGui.QColor("black") and self.fill:
                    dict = {}
                    rect = item.rect()
                    points = []
                    points.append([int(rect.x()*self.scaleX), int(rect.y()*self.scaleY)])
                    points.append([int(rect.x()*self.scaleX), int((rect.y()+rect.height())*self.scaleY)])
                    points.append([int((rect.x()+rect.width())*self.scaleX), int((rect.y()+rect.height())*self.scaleY)])
                    points.append([int((rect.x()+rect.width())*self.scaleX), int(rect.y()*self.scaleY)])    
                    points = self.correction_points(points)       
                    print(f"Shade: {points}")
                    dict.setdefault("label", "shade")
                    dict.setdefault("points", points)
                    dict.setdefault("shape_type","polygon")
                    self.shapes.append(dict)
                
                elif isinstance(item, QtWidgets.QGraphicsPolygonItem) and item.pen().color() == QtGui.QColor("red") and self.fill:
                    dict = {}
                    poly = item.polygon()
                    points = []
                    for i in range(poly.size()):
                        point = poly.at(i)
                        points.append([int(point.x()*self.scaleX), int(point.y()*self.scaleY)])
                    points = self.correction_points(points)
                    print(f"Polygon: {points}")
                    dict.setdefault("label", "defect")
                    dict.setdefault("points", points)
                    dict.setdefault("shape_type","polygon")
                    self.shapes.append(dict)

                elif isinstance(item, QtWidgets.QGraphicsPolygonItem) and item.pen().color() == QtGui.QColor("black") and self.fill:
                    dict = {}
                    poly = item.polygon()
                    points = []
                    for i in range(poly.size()):
                        point = poly.at(i)
                        points.append([int(point.x()*self.scaleX), int(point.y()*self.scaleY)])
                    points = self.correction_points(points)
                    print(f"Polygon: {points}")
                    dict.setdefault("label", "shade")
                    dict.setdefault("points", points)
                    dict.setdefault("shape_type","polygon")
                    self.shapes.append(dict)

                elif isinstance(item, QtWidgets.QGraphicsPathItem) and item.pen().color() == QtGui.QColor("red") and self.fill:
                    dict = {}
                    path = item.path()
                    points = []
                    for i in range(path.elementCount()):
                        point = path.elementAt(i)
                        points.append([int(point.x*self.scaleX), int(point.y*self.scaleY)])
                    points = self.correction_points(points)
                    print(f"Frame: {points}")
                    dict.setdefault("label", "defect")
                    dict.setdefault("points", points)
                    dict.setdefault("shape_type","frame")
                    self.shapes.append(dict)

                elif isinstance(item, QtWidgets.QGraphicsPathItem) and item.pen().color() == QtGui.QColor("black") and self.fill:
                    dict = {}
                    path = item.path()
                    points = []
                    for i in range(path.elementCount()):
                        point = path.elementAt(i)
                        points.append([int(point.x*self.scaleX), int(point.y*self.scaleY)])
                    points = self.correction_points(points)
                    print(f"Frame: {points}")
                    dict.setdefault("label", "shade")
                    dict.setdefault("points", points)
                    dict.setdefault("shape_type","frame")
                    self.shapes.append(dict)

                elif isinstance(item, QtWidgets.QGraphicsRectItem) and item.pen().color() == QtGui.QColor("red") and self.space:
                    dict = {}
                    rect = item.rect()
                    points = []
                    points.append([int(rect.x()*self.scalefactor), int(rect.y()*self.scalefactor)])
                    points.append([int(rect.x()*self.scalefactor), int((rect.y()+rect.height())*self.scalefactor)])
                    points.append([int((rect.x()+rect.width())*self.scalefactor), int((rect.y()+rect.height())*self.scalefactor)])
                    points.append([int((rect.x()+rect.width())*self.scalefactor), int(rect.y()*self.scalefactor)])    
                    points = self.correction_points(points)       
                    print(f"Rectangle: {points}")
                    dict.setdefault("label", "defect")
                    dict.setdefault("points", points)
                    dict.setdefault("shape_type","polygon")
                    self.shapes.append(dict)

                elif isinstance(item, QtWidgets.QGraphicsRectItem) and item.pen().color() == QtGui.QColor("black") and self.space:
                    dict = {}
                    rect = item.rect()
                    points = []
                    points.append([int(rect.x()*self.scalefactor), int(rect.y()*self.scalefactor)])
                    points.append([int(rect.x()*self.scalefactor), int((rect.y()+rect.height())*self.scalefactor)])
                    points.append([int((rect.x()+rect.width())*self.scalefactor), int((rect.y()+rect.height())*self.scalefactor)])
                    points.append([int((rect.x()+rect.width())*self.scalefactor), int(rect.y()*self.scalefactor)]) 
                    points = self.correction_points(points)          
                    print(f"Shade: {points}")
                    dict.setdefault("label", "shade")
                    dict.setdefault("points", points)
                    dict.setdefault("shape_type","polygon")
                    self.shapes.append(dict)
                
                elif isinstance(item, QtWidgets.QGraphicsPolygonItem) and item.pen().color() == QtGui.QColor("red") and self.space:
                    dict = {}
                    poly = item.polygon()
                    points = []
                    for i in range(poly.size()):
                        point = poly.at(i)
                        points.append([int(point.x()*self.scalefactor), int(point.y()*self.scalefactor)])
                    points = self.correction_points(points)
                    print(f"Polygon: {points}")
                    dict.setdefault("label", "defect")
                    dict.setdefault("points", points)
                    dict.setdefault("shape_type","polygon")
                    self.shapes.append(dict)

                elif isinstance(item, QtWidgets.QGraphicsPolygonItem) and item.pen().color() == QtGui.QColor("black") and self.space:
                    dict = {}
                    poly = item.polygon()
                    points = []
                    for i in range(poly.size()):
                        point = poly.at(i)
                        points.append([int(point.x()*self.scalefactor), int(point.y()*self.scalefactor)])
                    points = self.correction_points(points)
                    print(f"Polygon: {points}")
                    dict.setdefault("label", "shade")
                    dict.setdefault("points", points)
                    dict.setdefault("shape_type","polygon")
                    self.shapes.append(dict)

                elif isinstance(item, QtWidgets.QGraphicsPathItem) and item.pen().color() == QtGui.QColor("red") and self.space:
                    dict = {}
                    path = item.path()
                    points = []
                    for i in range(path.elementCount()):
                        point = path.elementAt(i)
                        points.append([int(point.x*self.scalefactor), int(point.y*self.scalefactor)])
                    points = self.correction_points(points)
                    print(f"Frame: {points}")
                    dict.setdefault("label", "defect")
                    dict.setdefault("points", points)
                    dict.setdefault("shape_type","frame")
                    self.shapes.append(dict)

                elif isinstance(item, QtWidgets.QGraphicsPathItem) and item.pen().color() == QtGui.QColor("black") and self.space:
                    dict = {}
                    path = item.path()
                    points = []
                    for i in range(path.elementCount()):
                        point = path.elementAt(i)
                        points.append([int(point.x*self.scalefactor), int(point.y*self.scalefactor)])
                    points = self.correction_points(points)
                    print(f"Frame: {points}")
                    dict.setdefault("label", "shade")
                    dict.setdefault("points", points)
                    dict.setdefault("shape_type","frame")
                    self.shapes.append(dict)
            #移除相同點
            # new_shapes = []
            # for shape in self.shapes:
            #     if not all(point == shape['points'][0] for point in shape['points']):
            #         new_shapes.append(shape)
            # self.shapes = new_shapes
            self.shapes = self.remove_dicts_with_same_points(self.shapes)
            print(self.shapes)
            self.dict['shapes'] = self.shapes
            with open(self.path+self.name +".json", "w") as f:
                json.dump(self.dict, f, indent = 4)

            # #JSON檔寫進DB    
            # with open(self.path+self.name +".json", "r") as f:
            #     data = json.load(f)

       
            # filename = re.sub(r'[^\w\s]', '', self.name)
            # filename = re.sub(r'[^\w\s]', '', filename)
            # # Remove whitespace using string methods
            # filename = filename.replace(" ", "")
            # filename = "ID"+filename
 

            # Date = None
            # for shape in data["shapes"]:
            #     image_path = data["imagePath"]
            #     image_height = data["imageHeight"]
            #     image_width = data["imageWidth"]
            #     label = shape["label"]
            #     points = json.dumps(shape["points"])
            #     shape_type = shape["shape_type"]
                
            
        else:
            print("Please load an image first.")
            
    def Orient_Value(self):
        shapes_orient = []
        if self.image_loaded:
            for item in self.graphicsView.scene.items():
                if isinstance(item, QtWidgets.QGraphicsRectItem) and item.pen().color() == QtGui.QColor("blue") and self.fill:
                    dict = {}
                    rect = item.rect()
                    points = []
                    points.append([int(rect.x()*self.scaleX), int(rect.y()*self.scaleY)])
                    points.append([int(rect.x()*self.scaleX), int((rect.y()+rect.height())*self.scaleY)])
                    points.append([int((rect.x()+rect.width())*self.scaleX), int((rect.y()+rect.height())*self.scaleY)])
                    points.append([int((rect.x()+rect.width())*self.scaleX), int(rect.y()*self.scaleY)])     
                    points = self.correction_points(points)
                    print(f"Rectangle: {points}")
                    dict.setdefault("label", "定位座標")
                    dict.setdefault("points", points)
                    shapes_orient.append(dict)

                elif isinstance(item, QtWidgets.QGraphicsRectItem) and item.pen().color() == QtGui.QColor("blue") and self.space:
                    dict = {}
                    rect = item.rect()
                    points = []
                    points.append([int(rect.x()*self.scalefactor), int(rect.y()*self.scalefactor)])
                    points.append([int(rect.x()*self.scalefactor), int((rect.y()+rect.height())*self.scalefactor)])
                    points.append([int((rect.x()+rect.width())*self.scalefactor), int((rect.y()+rect.height())*self.scalefactor)])
                    points.append([int((rect.x()+rect.width())*self.scalefactor), int(rect.y()*self.scalefactor)]) 
                    points = self.correction_points(points)          
                    print(f"Rectangle: {points}")
                    dict.setdefault("label", "定位座標")
                    dict.setdefault("points", points)
                    shapes_orient.append(dict)
                
                elif isinstance(item, QtWidgets.QGraphicsPolygonItem) and item.pen().color() == QtGui.QColor("blue") and self.fill:
                    dict = {}
                    poly = item.polygon()
                    points = []
                    for i in range(poly.size()):
                        point = poly.at(i)
                        points.append([int(point.x()*self.scaleX), int(point.y()*self.scaleY)])
                    points = self.correction_points(points)
                    print(f"Polygon: {points}")
                    dict.setdefault("label", "定位座標")
                    dict.setdefault("points", points)
                    shapes_orient.append(dict)

                elif isinstance(item, QtWidgets.QGraphicsPolygonItem) and item.pen().color() == QtGui.QColor("blue") and self.space:
                    dict = {}
                    poly = item.polygon()
                    points = []
                    for i in range(poly.size()):
                        point = poly.at(i)
                        points.append([int(point.x()*self.scalefactor), int(point.y()*self.scalefactor)])
                    points = self.correction_points(points)
                    print(f"Polygon: {points}")
                    dict.setdefault("label", "定位座標")
                    dict.setdefault("points", points)
                    shapes_orient.append(dict)
                
            shapes_orient = self.remove_dicts_with_same_points(shapes_orient)
            print('Here', shapes_orient)
        return shapes_orient
        
   
    #標註圈選功能
    def draw_frame(self):
        self.rectangle = False
        self.polygon = False
        self.frame = True
        self.smear = False
        self.shade = False
        self.remove = False
        self.shade_rectangle = False
        self.shade_polygon = False
        self.shade_frame = False
        self.maskk = False
        self.mask_polygon = False
        self.orient = False
        self.orient_polygon = False
        self.orient_smear = False

        if self.image_loaded:
            self.graphicsView.mousePressEvent = self.PressEventFrame
            self.graphicsView.mouseReleaseEvent = self.ReleaseEventFrame
            self.graphicsView.mouseMoveEvent = self.MoveEventFrame
            
        else:
            print("Please load an image first.")

    def PressEventFrame(self,event):
        if self.frame == True and self.image_loaded and event.button() == QtCore.Qt.LeftButton :
            view_pos = event.pos()
            if not self.graphicsView.rect().contains(view_pos):
                return
        self.frame_path = QtGui.QPainterPath()
        self.frame_item = QtWidgets.QGraphicsPathItem()
        self.frame_item.setPen(QtGui.QPen(QtGui.QColor("red"), 2))
        self.graphicsView.scene.addItem(self.frame_item)
        scene_pos = self.graphicsView.mapToScene(view_pos)
        self.frame_start_point = scene_pos
        self.frame_path.moveTo(scene_pos)

    def MoveEventFrame(self,event):
        if self.frame == True:
            if not self.graphicsView.rect().contains(event.pos()):
                return
            view_pos = event.pos()
            if not self.graphicsView.rect().contains(view_pos):
                return
            scene_pos = self.graphicsView.mapToScene(view_pos)
            self.frame_path.lineTo(scene_pos)
            self.frame_item.setPath(self.frame_path)


    def ReleaseEventFrame(self, event):
        if self.frame == True and self.image_loaded and event.button() == QtCore.Qt.LeftButton :
            self.frame_path.lineTo(self.frame_start_point) # Connect the final point to the starting point
            self.frame_item.setPath(self.frame_path)

    #標註塗抹功能
    def draw_smear(self, brush_size):
        self.rectangle = False
        self.polygon = False
        self.frame = False
        self.smear = True
        self.remove = False
        self.shade_rectangle = False
        self.shade_polygon = False
        self.shade_frame = False
        self.maskk = False
        self.mask_polygon = False
        self.orient = False
        self.orient_polygon = False
        self.orient_smear = False

        if self.image_loaded:
            self.graphicsView.mousePressEvent = lambda event: self.smear_press_event(event, brush_size)
            self.graphicsView.mouseMoveEvent = self.smear_move_event
            self.graphicsView.mouseReleaseEvent = lambda event: self.smear_release_event(event, brush_size)
        else:
            print("Please load an image first.")

    def smear_press_event(self, event, brush_size):
        if self.smear == True and self.image_loaded and event.button() == QtCore.Qt.LeftButton :
            view_pos = event.pos()
            if not self.graphicsView.rect().contains(view_pos):
                return
        self.smear_path = QtGui.QPainterPath()
        self.smear_item = QtWidgets.QGraphicsPathItem()
        self.smear_item.setPen(QtGui.QPen(QtGui.QColor("red"), brush_size))
        self.graphicsView.scene.addItem(self.smear_item)
        scene_pos = self.graphicsView.mapToScene(view_pos)
        self.smear_start_point = scene_pos
        self.smear_path.moveTo(scene_pos)

    def smear_move_event(self, event):
        if not self.graphicsView.rect().contains(event.pos()):
            return
        view_pos = event.pos()
        if not self.graphicsView.rect().contains(view_pos):
            return
        scene_pos = self.graphicsView.mapToScene(view_pos)
        self.smear_path.lineTo(scene_pos)
        self.smear_item.setPath(self.smear_path)

    def smear_release_event(self, event, brush_size):
        if self.smear == True and self.smear_path is not None:
            points = []
            for i in range(self.smear_path.elementCount()):
                    point = self.smear_path.elementAt(i)
                    points.append([point.x, point.y])
                    points = self.correction_points(points)
            if len(points)>1:
                line = LineString(points)
                buffer_distance = brush_size
                bounding_box = line.buffer(buffer_distance)
                bounding_box_coords = list(bounding_box.exterior.coords)
                polygon = QtGui.QPolygonF([QtCore.QPointF(x, y) for x, y in bounding_box_coords])
                polygon_item = QtWidgets.QGraphicsPolygonItem(polygon)
                self.graphicsView.scene.addItem(polygon_item)
                pen = QtGui.QPen(QtGui.QColor("red"))
                pen.setWidth(2)
                polygon_item.setPen(pen)
                self.graphicsView.scene.removeItem(self.smear_item)
            
    #移除功能
    def Remove(self, event):
        self.rectangle = False
        self.polygon = False
        self.frame = False
        self.smear = False
        self.remove = True
        self.shade_rectangle = False
        self.shade_polygon = False
        self.shade_frame = False
        self.maskk = False
        self.mask_polygon = False
        self.orient = False
        self.orient_polygon = False
        self.orient_smear = False
        
        if self.image_loaded:
            print("Remove")
        self.graphicsView.mousePressEvent = self.Remove_press_event

    def Remove_press_event(self, event):
        # Get the position of the mouse click
        view_pos = event.pos()
        scene_pos = self.graphicsView.mapToScene(view_pos)

        # Iterate through all the items in the scene
        for item in self.graphicsView.scene.items():
            # Check if the item is a QGraphicsPathItem and if the clicked position is within its bounding rectangle
            if isinstance(item, QtWidgets.QGraphicsRectItem) and item.boundingRect().contains(scene_pos):
                # Remove the item from the scene
                self.graphicsView.scene.removeItem(item)
                break
        for item in self.graphicsView.scene.items():
        # Check if the item is a QGraphicsPathItem and if the clicked position is within its bounding rectangle
            if   isinstance(item, QtWidgets.QGraphicsPolygonItem) and item.boundingRect().contains(scene_pos):
                # Remove the item from the scene
                self.graphicsView.scene.removeItem(item)
                break

        for item in self.graphicsView.scene.items():
        # Check if the item is a QGraphicsPathItem and if the clicked position is within its bounding rectangle
            if   isinstance(item, QtWidgets.QGraphicsPathItem) and item.boundingRect().contains(scene_pos):
                # Remove the item from the scene
                self.graphicsView.scene.removeItem(item)
                break
    
    #矩形-遮蔽
    def Shade_Rectangle(self):
        self.polygon = False
        self.rectangle = False
        self.frame = False
        self.smear = False
        self.remove = False
        self.shade_rectangle = True
        self.shade_polygon = False
        self.shade_frame = False
        self.maskk = False
        self.mask_polygon = False
        self.orient = False
        self.orient_polygon = False
        self.orient_smear = False
        
        if self.image_loaded:
            print("Draw Rectangle")
            self.graphicsView.mousePressEvent = self.PressEvent_Shade
            self.graphicsView.mouseReleaseEvent = self.ReleaseEvent_Shade
            self.graphicsView.mouseMoveEvent = self.MoveEvent_Shade
        else:
            print("Please load an image first.")

    def PressEvent_Shade(self, event):
        if self.shade_rectangle == True and self.image_loaded and event.button() == QtCore.Qt.LeftButton :
            view_pos = event.pos()
            if not self.graphicsView.rect().contains(view_pos):
                return
            scene_pos = self.graphicsView.mapToScene(view_pos)
            self.rect_start_point = scene_pos
            self.rect_item = QtWidgets.QGraphicsRectItem(QtCore.QRectF(self.rect_start_point, self.rect_start_point))
           
            self.graphicsView.scene.addItem(self.rect_item)
            pen = QtGui.QPen(QtGui.QColor("red"))
            pen.setWidth(2)
            self.rect_item.setPen(pen)
            self.graphicsView.viewport().update()
            event.accept()
        
    def MoveEvent_Shade(self, event):
        
        if self.shade_rectangle == True and self.image_loaded and self.rect_start_point is not None and event.buttons() == QtCore.Qt.LeftButton : 
            if self.rect_item is not None:
                self.graphicsView.scene.removeItem(self.rect_item)
            pen = QtGui.QPen(QtGui.QColor("black"))
            pen.setWidth(2)
            view_pos = event.pos()
            scene_pos = self.graphicsView.mapToScene(view_pos)
            rect = QtCore.QRectF(self.rect_start_point, scene_pos).normalized()
            self.rect_item = self.graphicsView.scene.addRect(rect, pen)
            self.graphicsView.viewport().update()


    def ReleaseEvent_Shade(self, event):
        
        if self.shade_rectangle == True and self.image_loaded and event.button() == QtCore.Qt.LeftButton and self.rect_item is not None :
            view_pos = event.pos()
            scene_pos = self.graphicsView.mapToScene(view_pos)
            self.rect_end_point = scene_pos
            self.rect_item.setRect(QtCore.QRectF(self.rect_start_point, self.rect_end_point))   
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128), QtCore.Qt.DiagCrossPattern)
            self.rect_item.setBrush(brush)     
            self.graphicsView.viewport().update()

    #多邊型-遮蔽
    def Shade_Polygon(self):

        self.polygon_item = QtWidgets.QGraphicsPolygonItem() # Create a new QGraphicsPolygonItem object
        self.graphicsView.scene.addItem(self.polygon_item) # Add the polygon item to the scene
        self.rectangle = False
        self.polygon = False
        self.frame = False
        self.smear = False
        self.shade = False
        self.remove = False
        self.shade_rectangle = False
        self.shade_polygon = True
        self.shade_frame = False
        self.maskk = False
        self.mask_polygon = False
        self.orient = False
        self.orient_polygon = False
        self.orient_smear = False
        
        if self.image_loaded:
            print("Draw Polygon")
            self.graphicsView.mousePressEvent = self.PressEventPoly_shade
           
        else:
            print("Please load an image first.")

    def PressEventPoly_shade(self, event):
        if self.shade_polygon == True:
            self.polygon_item.setPen(QtGui.QPen(QtCore.Qt.black, 2))
            sp = self.graphicsView.mapToScene(event.pos())
            lp = self.pixmap_item.mapFromScene(sp)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128), QtCore.Qt.DiagCrossPattern)
            self.polygon_item.setBrush(brush)
            poly = self.polygon_item.polygon()
            poly.append(lp)
            self.polygon_item.setPolygon(poly)
            self.graphicsView.viewport().update()

    #圈選-遮蔽
    def Shade_Framed(self):
        self.rectangle = False     
        self.polygon = False
        self.frame = False
        self.smear = False
        self.shade = False
        self.remove = False
        self.shade_rectangle = False
        self.shade_polygon = False
        self.shade_frame = True
        self.maskk = False
        self.mask_polygon = False
        self.orient = False
        self.orient_polygon = False
        self.orient_smear = False

        if self.image_loaded:
            self.graphicsView.mousePressEvent = self.PressEventFrame_shade
            self.graphicsView.mouseReleaseEvent = self.ReleaseEventFrame_shade
            self.graphicsView.mouseMoveEvent = self.MoveEventFrame_shade
            
        else:
            print("Please load an image first.")

    def PressEventFrame_shade(self,event):
        
        if self.shade_frame == True and self.image_loaded and event.button() == QtCore.Qt.LeftButton :
            view_pos = event.pos()
            if not self.graphicsView.rect().contains(view_pos):
                return
        self.frame_path = QtGui.QPainterPath()
        self.frame_item = QtWidgets.QGraphicsPathItem()
        self.frame_item.setPen(QtGui.QPen(QtGui.QColor("black"), 2))
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128), QtCore.Qt.DiagCrossPattern)
        self.frame_item.setBrush(brush)
        self.graphicsView.scene.addItem(self.frame_item)
        scene_pos = self.graphicsView.mapToScene(view_pos)
        self.frame_start_point = scene_pos
        self.frame_path.moveTo(scene_pos)

    def MoveEventFrame_shade(self,event):     
        if self.shade_frame == True:
            if not self.graphicsView.rect().contains(event.pos()):
                return
            view_pos = event.pos()
            if not self.graphicsView.rect().contains(view_pos):
                return
            scene_pos = self.graphicsView.mapToScene(view_pos)
            self.frame_path.lineTo(scene_pos)
            self.frame_item.setPath(self.frame_path)

    def ReleaseEventFrame_shade(self, event):
        if self.shade_frame == True and self.image_loaded and event.button() == QtCore.Qt.LeftButton :
            self.frame_path.lineTo(self.frame_start_point) # Connect the final point to the starting point
            self.frame_item.setPath(self.frame_path)

    #矩形-遮罩
    def Mask_Rectangle(self):
        self.polygon = False
        self.rectangle = False
        self.frame = False
        self.smear = False
        self.remove = False
        self.shade_rectangle = False
        self.shade_polygon = False
        self.shade_frame = False
        self.maskk = True
        self.mask_polygon = False
        self.orient = False
        self.orient_polygon = False
        self.orient_smear = False
       
        if self.image_loaded:
            print("Draw Rectangle")
            self.graphicsView.mousePressEvent = self.PressEventmask
            self.graphicsView.mouseReleaseEvent = self.ReleaseEventmask
            self.graphicsView.mouseMoveEvent = self.MoveEventmask
        else:
            print("Please load an image first.")

    def PressEventmask(self, event):
        if self.maskk == True and self.image_loaded and event.button() == QtCore.Qt.LeftButton :
            view_pos = event.pos()
            if not self.graphicsView.rect().contains(view_pos):
                return
            scene_pos = self.graphicsView.mapToScene(view_pos)
            self.rect_start_point = scene_pos
            self.rect_item = QtWidgets.QGraphicsRectItem(QtCore.QRectF(self.rect_start_point, self.rect_start_point))
            self.graphicsView.scene.addItem(self.rect_item)
            pen = QtGui.QPen(QtGui.QColor("green"))
            pen.setWidth(2)
            self.rect_item.setPen(pen)
            self.graphicsView.viewport().update()
            event.accept()
        
    def MoveEventmask(self, event):
        
        if self.maskk == True and self.image_loaded and self.rect_start_point is not None and event.buttons() == QtCore.Qt.LeftButton : 
            if self.rect_item is not None:
                self.graphicsView.scene.removeItem(self.rect_item)
            pen = QtGui.QPen(QtGui.QColor("green"))
            pen.setWidth(2)
            view_pos = event.pos()
            scene_pos = self.graphicsView.mapToScene(view_pos)
            rect = QtCore.QRectF(self.rect_start_point, scene_pos).normalized()
            self.rect_item = self.graphicsView.scene.addRect(rect, pen)
            self.graphicsView.viewport().update()

    def ReleaseEventmask(self, event):
        
        if self.maskk == True and self.image_loaded and event.button() == QtCore.Qt.LeftButton and self.rect_item is not None :
            view_pos = event.pos()
            scene_pos = self.graphicsView.mapToScene(view_pos)
            self.rect_end_point = scene_pos
            self.rect_item.setRect(QtCore.QRectF(self.rect_start_point, self.rect_end_point))       
            self.graphicsView.viewport().update()

    #多邊型-遮罩
    def Mask_Polygon(self):

        self.polygon_item = QtWidgets.QGraphicsPolygonItem() # Create a new QGraphicsPolygonItem object
        self.graphicsView.scene.addItem(self.polygon_item) # Add the polygon item to the scene
        self.rectangle = False
        self.polygon = False
        self.frame = False
        self.smear = False
        self.shade = False
        self.remove = False
        self.shade_rectangle = False
        self.shade_polygon = False
        self.shade_frame = False
        self.maskk = False
        self.mask_polygon = True
        self.orient = False
        self.orient_polygon = False
        self.orient_smear = False
        
        if self.image_loaded:
            print("Draw Polygon")
            self.graphicsView.mousePressEvent = self.PressEventPoly_mask
           
        else:
            print("Please load an image first.")

    def PressEventPoly_mask(self, event):
        if self.mask_polygon == True:
            pen = QtGui.QPen(QtGui.QColor("green"))
            pen.setWidth(2)
            self.polygon_item.setPen(pen)
            sp = self.graphicsView.mapToScene(event.pos())
            lp = self.pixmap_item.mapFromScene(sp)
            poly = self.polygon_item.polygon()
            poly.append(lp)
            self.polygon_item.setPolygon(poly)
            self.graphicsView.viewport().update()
    
    def load_image_file(self, filename):
        try:
            image_cv2 = cv2.imread(filename)
        except IOError:
            logger.error("Failed opening image file: {}".format(filename))
            return

        with io.BytesIO() as f:
            _, image_data = cv2.imencode(".png", image_cv2)
            b64_imageData = base64.b64encode(image_data).decode('utf-8')
            
            return b64_imageData
        
    def correction_points(self,points):
        for sublist in points:
            sublist[0] = 0 if sublist[0] < 0 else self.graphwidth if sublist[0] > self.graphwidth else sublist[0]
            sublist[1] = 0 if sublist[1] < 0 else self.graphheight if sublist[1] > self.graphheight else sublist[1]
        return points
    
      #矩形-遮罩
    def Orient_Rectangle(self):
        self.polygon = False
        self.rectangle = False
        self.frame = False
        self.smear = False
        self.remove = False
        self.shade_rectangle = False
        self.shade_polygon = False
        self.shade_frame = False
        self.maskk = False
        self.mask_polygon = False
        self.orient = True
        self.orient_polygon = False
        
        
        if self.image_loaded:
            print("Draw Rectangle")
            self.graphicsView.mousePressEvent = self.PressEventorient
            self.graphicsView.mouseReleaseEvent = self.ReleaseEventorient
            self.graphicsView.mouseMoveEvent = self.MoveEventorient
        else:
            print("Please load an image first.")
            
    def PressEventorient(self, event):
        if self.orient == True and self.image_loaded and event.button() == QtCore.Qt.LeftButton :
            view_pos = event.pos()
            if not self.graphicsView.rect().contains(view_pos):
                return
            scene_pos = self.graphicsView.mapToScene(view_pos)
            self.rect_start_point = scene_pos
            self.rect_item = QtWidgets.QGraphicsRectItem(QtCore.QRectF(self.rect_start_point, self.rect_start_point))
            self.graphicsView.scene.addItem(self.rect_item)
            pen = QtGui.QPen(QtGui.QColor("blue"))
            pen.setWidth(2)
            self.rect_item.setPen(pen)
            self.graphicsView.viewport().update()
            event.accept()
        
    def MoveEventorient(self, event):
        
        if self.orient == True and self.image_loaded and self.rect_start_point is not None and event.buttons() == QtCore.Qt.LeftButton : 
            if self.rect_item is not None:
                self.graphicsView.scene.removeItem(self.rect_item)
            pen = QtGui.QPen(QtGui.QColor("blue"))
            pen.setWidth(2)
            view_pos = event.pos()
            scene_pos = self.graphicsView.mapToScene(view_pos)
            rect = QtCore.QRectF(self.rect_start_point, scene_pos).normalized()
            self.rect_item = self.graphicsView.scene.addRect(rect, pen)
            self.graphicsView.viewport().update()

    def ReleaseEventorient(self, event):
        
        if self.orient == True and self.image_loaded and event.button() == QtCore.Qt.LeftButton and self.rect_item is not None :
            view_pos = event.pos()
            scene_pos = self.graphicsView.mapToScene(view_pos)
            self.rect_end_point = scene_pos
            self.rect_item.setRect(QtCore.QRectF(self.rect_start_point, self.rect_end_point))       
            self.graphicsView.viewport().update()
            
    def Orient_Polygon(self):

        self.polygon_item = QtWidgets.QGraphicsPolygonItem() # Create a new QGraphicsPolygonItem object
        self.graphicsView.scene.addItem(self.polygon_item) # Add the polygon item to the scene
        self.rectangle = False
        self.polygon = False
        self.frame = False
        self.smear = False
        self.shade = False
        self.remove = False
        self.shade_rectangle = False
        self.shade_polygon = False
        self.shade_frame = False
        self.maskk = False
        self.mask_polygon = False
        self.orient = False
        self.orient_polygon = True
        
        if self.image_loaded:
            print("Draw Polygon")
            self.graphicsView.mousePressEvent = self.PressEventPoly_orient
           
        else:
            print("Please load an image first.")
            
    def PressEventPoly_orient(self, event):
        if self.orient_polygon == True:
            pen = QtGui.QPen(QtGui.QColor("blue"))
            pen.setWidth(2)
            self.polygon_item.setPen(pen)
            sp = self.graphicsView.mapToScene(event.pos())
            lp = self.pixmap_item.mapFromScene(sp)
            poly = self.polygon_item.polygon()
            poly.append(lp)
            self.polygon_item.setPolygon(poly)
            self.graphicsView.viewport().update()
            
    def Orient_Smear(self, brush_size):
        self.rectangle = False
        self.polygon = False
        self.frame = False
        self.smear = False
        self.remove = False
        self.shade_rectangle = False
        self.shade_polygon = False
        self.shade_frame = False
        self.maskk = False
        self.mask_polygon = False
        self.orient = False
        self.orient_polygon = False
        self.orient_smear = True

        if self.image_loaded:
            self.graphicsView.mousePressEvent = lambda event: self.smear_press_event_orient(event, brush_size)
            self.graphicsView.mouseMoveEvent = self.smear_move_event_orient
            self.graphicsView.mouseReleaseEvent = lambda event:self.smear_release_event_orient(event, brush_size)
        else:
            print("Please load an image first.")
        
            
    def smear_press_event_orient(self, event, brush_size):
        if self.orient_smear == True and self.image_loaded and event.button() == QtCore.Qt.LeftButton :
            view_pos = event.pos()
            if not self.graphicsView.rect().contains(view_pos):
                return
        self.smear_path = QtGui.QPainterPath()
        self.smear_item = QtWidgets.QGraphicsPathItem()
        self.smear_item.setPen(QtGui.QPen(QtGui.QColor("blue"), brush_size))
        self.graphicsView.scene.addItem(self.smear_item)
        scene_pos = self.graphicsView.mapToScene(view_pos)
        self.smear_start_point = scene_pos
        self.smear_path.moveTo(scene_pos)

    def smear_move_event_orient(self, event):
        if not self.graphicsView.rect().contains(event.pos()):
            return
        view_pos = event.pos()
        if not self.graphicsView.rect().contains(view_pos):
            return
        scene_pos = self.graphicsView.mapToScene(view_pos)
        self.smear_path.lineTo(scene_pos)
        self.smear_item.setPath(self.smear_path)

    def smear_release_event_orient(self, event, brush_size):
        if self.orient_smear and self.smear_path is not None:
               
            points = []
            for i in range(self.smear_path.elementCount()):
                    point = self.smear_path.elementAt(i)
                    points.append([point.x, point.y])
                    points = self.correction_points(points)
            if len(points)>1:
                line = LineString(points)
                buffer_distance = brush_size
                bounding_box = line.buffer(buffer_distance)

                bounding_box_coords = list(bounding_box.exterior.coords)
                polygon = QtGui.QPolygonF([QtCore.QPointF(x, y) for x, y in bounding_box_coords])
                polygon_item = QtWidgets.QGraphicsPolygonItem(polygon)
                self.graphicsView.scene.addItem(polygon_item)
                pen = QtGui.QPen(QtGui.QColor("blue"))
                pen.setWidth(2)
                polygon_item.setPen(pen)
                self.graphicsView.scene.removeItem(self.smear_item)
    
    def remove_dicts_with_same_points(self, lst):
        for d in lst[:]:
            points = d['points']
            if all(point[0] == points[0][0] for point in points) or all(point[1] == points[0][1] for point in points):
                lst.remove(d)
        return lst
            

app = QApplication(sys.argv)
w = label()
w.show()
sys.exit(app.exec_())
