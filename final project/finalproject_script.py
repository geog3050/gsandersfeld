##########################################################
### HABITAT CONNECTIVITY MODEL FOR URBAN PARKS USING PATCHES AND SEARCH DISTANCE
### Graham Sandersfeld 
### University of Iowa
### Geospatial Programming Spring 2022 
### Dr. Caglar Koylu 
##########################################################

# import necessary modules
import os
import arcpy

arcpy.env.overwriteOutput = True


### USER INPUT - ENTER PARAMETERS AS ASSIGNMENTS FOR THE VARIABLES BELOW ###

# Enter your workspace path. Move/copy Parks shapefile, NLCD 2016 land cover raster, and study bounds into this folder:
workspace = "C:/Users/GSandersfeld/Documents/ArcGIS/Projects/3050FinalProj/3050FinalProj.gdb"

# Choose your study area boundary shapefile:
studyArea = "PolkBoundary"

# Choose your Parks shapefile:
parksFC = "public_lands_conservationt"

# The field in Parks to be used for joining results and exporting final layer of the model (MUST CONTAIN UNIQUE VALUES FOR EACH ROW):
joinfield = "OBJECTID_12"

# Choose how far outside of your bounding study area to search for parks and land cover:
studyAreaBuffer = "4 Miles"

# Choose the buffer length to use around parks (species colonization distance):
parksBuffer = "1 Miles"

# Land cover raster:
lcRaster = "nlcd2016_ia"

### Choose suitable land cover types as habitat
lcExtractArg = "NLCD_LAND = 'Deciduous Forest' Or NLCD_LAND = 'Evergreen Forest' Or NLCD_LAND = 'Mixed Forest'" # SQL statement. Select multiple using OR, AND, NOT, etc. 
### Ex: "NLCD_Land = 'Deciduous Forest' OR NLCD_Land = 'Mixed Forest'"
### All Land Cover types:
# "Open Water"
# "Developed, Open Space"
# "Developed, Low Intensity"
# "Developed, Medium Intensity"
# "Developed, High Intensity"
# "Barren Land"
# "Deciduous Forest"
# "Evergreen Forest"
# "Mixed Forest"
# "Shrub/Scrub"
# "Herbaceuous"
# "Hay/Pasture"
# "Cultivated Crops"
# "Woody Wetlands"
# "Emergent Herbaceuous Wetlands"
###

### END USER INPUT - MODEL SCRIPT IS BELOW, DO NOT MODIFY WITHOUT BACKING UP ###

# Create buffer layer around study area:
try:
    arcpy.analysis.PairwiseBuffer(studyArea, "sa_buffer", studyAreaBuffer, "NONE", None, "PLANAR", "0 Meters")
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))

# Select parks that intersect with study area buffer:
arcpy.management.SelectLayerByLocation(parksFC, "INTERSECT", "sa_buffer", None, "NEW_SELECTION", "NOT_INVERT")

# Export selected intersecting parks:
arcpy.conversion.FeatureClassToFeatureClass(parksFC, workspace, "sa_parks")

# Extract the land cover image by the study area buffer and save it to workspace:
try:
    out_raster = arcpy.sa.ExtractByMask(lcRaster, "sa_buffer")
    out_raster.save(workspace + "/sa_landcover")
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))

# Saved raster is a parameter for extract by attributes:
inRaster = "sa_landcover"

# Extract the suitable land cover types from the extracted raster and save to workspace:
try:
    attExtract = arcpy.sa.ExtractByAttributes(inRaster, lcExtractArg)
    attExtract.save(workspace + "/sa_coverclass")
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))

# Convert raster to polygon (multi-part feature):
try:
    with arcpy.EnvManager(outputZFlag="Disabled", outputMFlag="Disabled"):
        arcpy.conversion.RasterToPolygon("sa_coverclass", "sa_cover_polygon", "SIMPLIFY", "NLCD_LAND", "MULTIPLE_OUTER_PART", None)
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))

# Buffer the parks according to specified search/colonization distance:
arcpy.analysis.PairwiseBuffer("sa_parks", "sa_parks_Buffer", parksBuffer, "NONE", None, "PLANAR", "0 Meters")

# Calculate the total suitable land cover within each park's buffer:
arcpy.analysis.SummarizeWithin("sa_parks_Buffer", "sa_cover_polygon", "sa_ParksPatches", "KEEP_ALL", None, "ADD_SHAPE_SUM", "SQUAREMILES", None, "NO_MIN_MAJ", "NO_PERCENT", None)

# Create new field and calculate total area within each park's buffer 
try:
    arcpy.management.CalculateGeometryAttributes("sa_ParksPatches", "totalarea AREA_GEODESIC", '', "SQUARE_MILES_US")
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))

# Create new field and calculate connectScore (ratio of suitable to unsuitable habitat within parks buffers):
try:
    arcpy.management.CalculateField("sa_ParksPatches", "connectScore", "!sum_Area_SQUAREMILES! / !totalarea!", "PYTHON3", '', "DOUBLE", "NO_ENFORCE_DOMAINS")
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))

# Validate the joining of connectScore to study area parks features:
try:
    arcpy.env.workspace = workspace
    arcpy.ValidateJoin_management("sa_parks", joinfield, "sa_ParksPatches", joinfield)
    print(arcpy.GetMessages()) # prints output about the join
    arcpy.management.AddJoin("sa_parks", joinfield, "sa_ParksPatches", joinfield, "KEEP_ALL", "NO_INDEX_JOIN_FIELDS") # if join is valid, perform the join
    arcpy.conversion.FeatureClassToFeatureClass("sa_parks", workspace, "connectScore") # and export to a new feature class "connectScore"
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))

# Symbolize connectScore field with graduated colors to finish the model

# Delete intermediate products of the model:

arcpy.Delete_management("sa_buffer")
print("deleted sa_buffer.shp")

arcpy.Delete_management("sa_parks")
print("deleted sa_parks.shp")

arcpy.Delete_management("sa_parks_Buffer")
print("deleted sa_parks_Buffer.shp")

arcpy.Delete_management("sa_parksPatches")
print("deleted sa_parksPatches.shp")

arcpy.Delete_management("sa_cover_polygon")
print("deleted sa_cover_polygon.shp")

arcpy.Delete_management("sa_landcover")
print("deleted sa_landcover image")

arcpy.Delete_management("sa_coverclass")
print("deleted sa_coverclass image")

print("Model finished. It is recommended to symbolize the connectScore field with graduated colors")

### END
### Graham Sandersfeld 
### University of Iowa
### Geospatial Programming Spring 2022 
### Dr. Caglar Koylu 