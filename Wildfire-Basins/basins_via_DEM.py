#DESCRIPTION:  Build drainage basins around a wildfire from DEM. Overlay burn severity and extract burn extent by drainage.
#AUTHOR: dnormous
#STATUS: Active development - non-functional
#LAST REVISED: May 7, 2016

#NOTES: 


#Startup code for running script in QGIS console
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


#####################
#Start of QGIS Work
#####################

#Variable list - Input parameters for each individual wildfire analysis 
FIRE_NAME = "Hayman"
DEM = "P:/QGIS/WildfireChem Project/Hayman_py/DEM/USGS_NED_1_n40w106_IMG.img"
FIRE_SHAPE = "P:/QGIS/WildfireChem Project/Hayman_py/Shapes/Hayman_shape.shp" 
#SEVRT =
Stream_size = 10000
Fire_buffer = 10000


#Load full size DEM - Download 1/3 arc second from USGS
fileInfo = QFileInfo(DEM)
baseName = fileInfo.baseName()
rlayer = QgsRasterLayer(DEM, baseName)
if not rlayer.isValid():
  print "Layer failed to load!"

  #Project to UTM for USA


#Load wildfire shapefile
  #Project to UTM for USA
  #Create "square" buffer from fire shape

#Load wildfire burn severity layer

#Clip DEM by buffer

#Run r.watershed on clipped DEM
  #Save files
  #Convert stream layer to vector
  #Convert basin layer to vector
  
#Union basins and burn severity
  #Add layer to map with style

#Data table analysis...
  



  

