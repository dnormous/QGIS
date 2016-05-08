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


#####################
#Start of QGIS Work
#####################

#Variable list - Input parameters for each individual wildfire analysis 
FIRE_NAME = "Hayman"
PATH = "P:/QGIS/WildfireChem Project/Hayman_py/"
DEM = "DEM/Hayman_UTM_DEM.tif"
FIRE_SHAPE = "Shapes/Hayman_UTM_shape.shp" 
#SEVRT =
Stream_size = 10000
Fire_buffer = 10000

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


#Load full size DEM - Download 1/3 arc second from USGS
fileInfo = QFileInfo(PATH+DEM)
baseName = fileInfo.baseName()
rlayer = QgsRasterLayer(PATH+DEM, baseName)

if rlayer.isValid():
  print "DEM loaded successfully!"
else:
    print "Layer failed to load!"

#??? How to project raster from NAD83 to UTM Zone 13N

#Add rastor layer to interface
ifaceraslayer = iface.addRasterLayer(PATH+DEM, FIRE_NAME + "_DEM")
if ifaceraslayer.isValid():
  print "Raster added to canvas successfully!"
else:
    print "Raster failed to load to canvas!"


#Load wildfire shapefile
#Import vector layer from file
fire_layer = QgsVectorLayer(PATH+FIRE_SHAPE, FIRE_NAME + "_Shape", "ogr")
if fire_layer.isValid():
  print "Fire shape layer loaded successfully!"
else:
  print "Fire shape failed to load!" 

#Set fire layer crs
#fire_layer.setCrs(mycrs,True)

#Load vector layer to interface
fire_ifacelayer = iface.addVectorLayer(PATH+FIRE_SHAPE, FIRE_NAME + "_Shape", "ogr")
if fire_ifacelayer.isValid():
  print "Fire layer added to canvas successfully!"
else:
    print "Fire layer failed to load to canvas!"


#Create buffer around fire shape
QgsGeometryAnalyzer().buffer(fire_layer, PATH + "Shapes/" + FIRE_NAME + "_Buffer.shp", Fire_buffer, False, False, -1)

#Load newly created fire buffer vector
fire_buffer = QgsVectorLayer(PATH + "Shapes/" + FIRE_NAME + "_Buffer.shp", FIRE_NAME + "_Buffer", "ogr")
if fire_buffer.isValid():
  print "Fire buffer layer loaded successfully!"
else:
  print "Fire buffer failed to load!" 
  
#Load fire buffer vector layer to interface
buffer_ifacelayer = iface.addVectorLayer(PATH + "Shapes/" + FIRE_NAME + "_Buffer.shp", FIRE_NAME + "_Buffer", "ogr")
if fire_ifacelayer.isValid():
  print "Fire buffer layer added to canvas successfully!"
else:
    print "Fire buffer layer failed to load to canvas!"
    

#Clip DEM by fire buffer
#processing.alglist("clip")   #<-- Finds processing algorithms related to "clip"
processing.runalg("gdalogr:cliprasterbymasklayer",
    PATH+DEM,
    PATH + "Shapes/" + FIRE_NAME + "_Buffer.shp",
    "-9999",False,False,False,5,4,75,6,1,False,0,False,"",
    PATH + "DEM/" + FIRE_NAME + "_DEM_BUFFER.tif")

#Find DEM buffer extent (xmin, xmax, ymin, ymax)
ext =rlayer.extent()
    #dir(ext)
DEMBFxmin = ext.xMinimum
DEMBFxmax = ext.xMaximum
DEMBFymin = ext.yMinimum
DEMBFymax = ext.yMaximum

#Run r.watershed on clipped DEM
processing.runalg("grass7:r.watershed",
"P:/QGIS/WildfireChem Project/Hayman_py/DEM/Hayman_DEM_BUFFER.tif",
None,None,None,None,
10000,
0,5,300,False,False,False,False,False,
DEMBFxmin, DEMBFxmax, DEMBFymin, DEMBFymax, 0,
PATH + "Watershed Output/" + "FlowAcc.tif",
PATH + "Watershed Output/" + "FlowDir.tif",
PATH + "Watershed Output/" + "Basins.tif",
PATH + "Watershed Output/" + "Streams.tif",
PATH + "Watershed Output/" + "HalfBasins.tif",
PATH + "Watershed Output/" + "SlopeLSteep.tif",
PATH + "Watershed Output/" + "Steep.tif",
PATH + "Watershed Output/" + "TopoIndex.tif")
 



  #Convert stream layer to vector
  #Convert basin layer to vector
    
    

