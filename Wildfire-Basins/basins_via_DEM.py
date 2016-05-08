#DESCRIPTION:  Build drainage basins around a wildfire from DEM. Overlay burn severity and extract burn extent by drainage.
#AUTHOR: dnormous
#STATUS: Active development - non-functional
#LAST REVISED: May 7, 2016

#NOTES: 

#Startup code for running script in QGIS console

Paste here



#Parameter list
  #Set work path
  #Fire name
  #DEM path
  #Wildfire shape path
  #Wildfire burn severity path
  #Stream network size
  #Fire buffer size


#Load DEM
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
  



  

