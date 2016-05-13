##################
#SCRIPT STARTUP#
##################

import os
from PyQt4.QtCore import * 

settings = QSettings()
settings.setValue("pythonConsole/lastDirPath", QDir.homePath())

from qgis.core import *

# supply path to where is your qgis installed
QgsApplication.setPrefixPath("E:/Program Files/QGIS Essen/bin", True)
print "Current working dir : %s" % os.getcwd()

# load providers
QgsApplication.initQgis()



###################
#START SCRIPT WORK#
###################

#Load active layer
layer = iface.activeLayer()

#Print layer dir
#print dir(layer)

#Import vector layer from file
mylayer = QgsVectorLayer("P:/QGIS/WildfireChem Project/My Layers/West_US_Square.shp", \
  "West_US_Sqr", "ogr")
if not layer.isValid():
  print "Layer failed to load!"

#Load vector layer to interface
ifacelayer = iface.addVectorLayer("P:/QGIS/WildfireChem Project/My Layers/West_US_Square.shp", \
  "West_US_Sqr", "ogr")
if not ifacelayer:
  print "Layer failed to load!"

#Get layer features
for f in mylayer.getFeatures():
  print f
  
#Import raster from file
fileName = "P:/QGIS/WildfireChem Project/DEMs/WestUS.tif"
fileInfo = QFileInfo(fileName)
baseName = fileInfo.baseName()
rlayer = QgsRasterLayer(fileName, baseName)
if not rlayer.isValid():
  print "Layer failed to load!"
  
#Load rastor layer to interface
ifaceraslayer = iface.addRasterLayer("P:/QGIS/WildfireChem Project/DEMs/WestUS.tif", "West_US_DEM")
if not ifaceraslayer:
  print "Layer failed to load!"
  
#Define and set raster crs (untested)
from osgeo import osr, gdal
from gdalconst import *
dataset = gdal.Open('path_to_my_raster/out_pyqgis.tif', GA_Update)
band = dataset.GetRasterBand(1)
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)
dataset.SetProjection( srs.ExportToWkt() )
dataset = None

#Loop over canvas layers example (unknown code)
canvas = qgis.utils.iface.mapCanvas()
allLayers = canvas.layers()
exp_crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
for i in allLayers: 

    if i.type() != 0 :
        print(i.name() + " skipped as it is not a vector layer")
    if i.type() == 0 :
        #exp_crs = QgsCoordinateReferenceSystem(4326,QgsCoordinateReferenceSystem.PostgisCrsId)
        print i.crs()
        print exp_crs
        qgis.core.QgsVectorFileWriter.writeAsVectorFormat(i, i.name() + '.js', 'utf-8', exp_crs, 'GeoJSON')

