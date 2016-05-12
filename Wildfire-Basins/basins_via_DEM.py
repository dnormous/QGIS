#DESCRIPTION:  Build drainage basins around a wildfire from DEM. Overlay burn severity and extract burn extent by drainage.
#AUTHOR: dnormous
#STATUS: Active development - non-functional
#LAST REVISED: May 7, 2016

#NOTES: 


#Startup code for running script in QGIS console
import os
from PyQt4.QtCore import * 
from qgis.core import *
from qgis.analysis import *
import processing

settings = QSettings()
settings.setValue("pythonConsole/lastDirPath", QDir.homePath())

# supply path to where is your qgis installed
#QgsApplication.setPrefixPath("E:/Program Files/QGIS Essen/bin", True)
print "Current working dir : %s" % os.getcwd()

# load providers
QgsApplication.initQgis()

#Set project projection (aka "crs")
mycrs = QgsCoordinateReferenceSystem(32613)  #32613 = WGS84 UTM Zone 13N
iface.mapCanvas().mapRenderer().setDestinationCrs(mycrs)  # set CRS to canvas
#vlayer.setCrs(mycrs,True)#set CRS to vector layer. I'm not sure True param. is neccesary
#QgsMapLayerRegistry.instance().addMapLayer(vlayer)
print "QGIS CRS ID:", mycrs.srsid()
print "Description:", mycrs.description()
print "Projection Acronym:", mycrs.projectionAcronym()
print "Ellipsoid Acronym:", mycrs.ellipsoidAcronym()
# check whether it's geographic or projected coordinate system
print "Is geographic:", mycrs.geographicFlag()
# check type of map units in this CRS (values defined in QGis::units enum)
print "Map units:", mycrs.mapUnits() # meters = 0, degrees = 2


#####################
#Useful Functions
#####################









#####################
#Start of QGIS Work
#####################

#Variable list - Input parameters for each individual wildfire analysis 
#Change to user input after ALPHA
FIRE_NAME = "Hayman"
USER_PATH = "P:/QGIS/WildfireChem Project/"
DEM = "P:/QGIS/WildfireChem Project/Hayman_py/DEM/Hayman_UTM_DEM.tif"
FIRE_SHAPE = "P:/QGIS/WildfireChem Project/Hayman_py/Shapes/Hayman_UTM_shape.shp" 
#SEVRT =
Stream_size = 10000  
Fire_buffer = 10000

#Create folders in USER_PATH
PARENT_PATH = USER_PATH+FIRE_NAME+"_py/"
if not os.path.exists(PARENT_PATH):
    os.makedirs(PARENT_PATH)

DEM_PATH = PARENT_PATH+"DEM/"
if not os.path.exists(DEM_PATH):
    os.makedirs(DEM_PATH)

SHAPE_PATH = PARENT_PATH+"Shapes/"
if not os.path.exists(SHAPE_PATH):
    os.makedirs(SHAPE_PATH)

WSOUT_PATH = PARENT_PATH+"Watershed Output/"
if not os.path.exists(WSOUT_PATH):
    os.makedirs(WSOUT_PATH)


#Load full size DEM - Download 1/3 arc second from USGS
DEM_layer = QgsRasterLayer(DEM, FIRE_NAME+"_DEM")

if DEM_layer.isValid():
  print "DEM loaded successfully!"
else:
    print "Layer failed to load!"

#??? How to project raster from NAD83 to UTM Zone 13N

#Add rastor layer to interface
DEM_add = iface.addRasterLayer(DEM, FIRE_NAME + "_DEM")
if DEM_add.isValid():
  print "DEM Raster added to canvas successfully!"
else:
    print "DEM Raster failed to load to canvas!"


#Load wildfire shapefile
#Import vector layer from file
fire_layer = QgsVectorLayer(FIRE_SHAPE, FIRE_NAME + "_Shape", "ogr")
if fire_layer.isValid():
  print "Fire shape layer loaded successfully!"
else:
  print "Fire shape failed to load!" 

#Set fire layer crs
#fire_layer.setCrs(mycrs,True)

#Load vector layer to interface
FIRE_add = iface.addVectorLayer(FIRE_SHAPE, FIRE_NAME + "_Shape", "ogr")
if FIRE_add.isValid():
  print "Fire layer added to canvas successfully!"
else:
    print "Fire layer failed to load to canvas!"


#Create buffer around fire shape
QgsGeometryAnalyzer().buffer(fire_layer, SHAPE_PATH + FIRE_NAME + "_Buffer.shp", Fire_buffer, False, False, -1)

#Load newly created fire buffer vector
fire_buffer = QgsVectorLayer(SHAPE_PATH + FIRE_NAME + "_Buffer.shp", FIRE_NAME + "_Buffer", "ogr")
if fire_buffer.isValid():
  print "Fire buffer layer loaded successfully!"
else:
  print "Fire buffer failed to load!" 
  
#Load fire buffer vector layer to interface
buffer_ifacelayer = iface.addVectorLayer(SHAPE_PATH + FIRE_NAME + "_Buffer.shp", FIRE_NAME + "_Buffer", "ogr")
if buffer_ifacelayer.isValid():
  print "Fire buffer layer added to canvas successfully!"
else:
    print "Fire buffer layer failed to load to canvas!"


#Clip DEM by fire buffer and add buffer DEM to canvas
#processing.alglist("clip")   #<-- Finds processing algorithms related to "clip"
processing.runalg("gdalogr:cliprasterbymasklayer",
    DEM,
    SHAPE_PATH + FIRE_NAME + "_Buffer.shp",
    "-9999",False,False,False,5,4,75,6,1,False,0,False,"",
    DEM_PATH + FIRE_NAME + "_DEM_BUFFER.tif")

DEMBUF_add = iface.addRasterLayer(DEM_PATH + FIRE_NAME + "_DEM_BUFFER.tif", FIRE_NAME + "_DEM_BUFFER")
if DEMBUF_add.isValid():
  print "Buffer DEM Raster added to canvas successfully!"
else:
    print "Buffer DEM Raster failed to load to canvas!"



#Find DEM buffer extent (xmin, xmax, ymin, ymax)
DEMext =DEMBUF_add.extent()
    #dir(DEMext)
DEMBFxmin = DEMext.xMinimum
DEMBFxmax = DEMext.xMaximum
DEMBFymin = DEMext.yMinimum
DEMBFymax = DEMext.yMaximum

#Run r.watershed on clipped DEM
processing.runalg("grass7:r.watershed",
DEM_PATH + FIRE_NAME + "_DEM_BUFFER.tif",
None,None,None,None,
10000,
0,5,300,False,False,False,False,False,
str(DEMBFxmin()) + ',' + str(DEMBFxmax()) + ',' + str(DEMBFymin()) + ',' + str(DEMBFymax()), 0,
WSOUT_PATH + "FlowAcc.tif",
WSOUT_PATH + "FlowDir.tif",
WSOUT_PATH + "Basins.tif",
WSOUT_PATH + "Streams.tif",
WSOUT_PATH + "HalfBasins.tif",
WSOUT_PATH + "SlopeLSteep.tif",
WSOUT_PATH + "Steep.tif",
WSOUT_PATH + "TopoIndex.tif")
 
#Convert basin layer to vector and add to canvas
basinlayer = QgsRasterLayer(WSOUT_PATH + "Basins.tif", "Basins")
BASext =basinlayer.extent()
BASxmin = BASext.xMinimum
BASxmax = BASext.xMaximum
BASymin = BASext.yMinimum
BASymax = BASext.yMaximum

processing.runalg("grass7:r.to.vect",WSOUT_PATH + "Basins.tif",
2,False,str(BASxmin()) + ',' + str(BASxmax()) + ',' + str(BASymin()) + ',' + str(BASymax()),0,
SHAPE_PATH+"Basins.shp")   

#? how to add formatting?
basin_ifacelayer = iface.addVectorLayer(SHAPE_PATH+"Basins.shp", FIRE_NAME + "_Basins", "ogr")
if basin_ifacelayer.isValid():
  print "Basin layer added to canvas successfully!"
else:
    print "Basin layer failed to load to canvas!"


#Convert stream layer to vector



    

