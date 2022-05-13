import os
import arcpy

arcpy.env.overwriteOutput = True

workspace = "C:/Users/GSandersfeld/Documents/ArcGIS/Projects/3050FinalProj/3050FinalProj.gdb"
studyAreaBuffer = "4 Miles"
parksFC = "public_lands_conservationt"
parksBuffer = "1 Miles"
lcRaster = "nlcd2016_ia"
coverclass = 'Deciduous Forest' # from "NLCD_LAND" field
joinfield = "ShapeSTAre"
studyArea = "PolkBoundary"

arcpy.analysis.PairwiseBuffer(studyArea, "sa_buffer", studyAreaBuffer, "NONE", None, "PLANAR", "0 Meters")

arcpy.management.SelectLayerByLocation(parksFC, "INTERSECT", "sa_buffer", None, "NEW_SELECTION", "NOT_INVERT")

arcpy.conversion.FeatureClassToFeatureClass(parksFC, workspace, "sa_parks")

out_raster = arcpy.sa.ExtractByMask(lcRaster, "sa_buffer")
out_raster.save("C:/Users/GSandersfeld/Documents/ArcGIS/Projects/3050FinalProj/3050FinalProj.gdb/sa_landcover") # modify this path to be general based on workspace path

out_raster = arcpy.sa.ExtractByAttributes("sa_landcover", "NLCD_LAND = coverclass")
out_raster.save("C:/Users/GSandersfeld/Documents/ArcGIS/Projects/3050FinalProj/3050FinalProj.gdb/sa_coverclass")

with arcpy.EnvManager(outputZFlag="Disabled", outputMFlag="Disabled"):
    arcpy.conversion.RasterToPolygon("sa_coverclass", "sa_cover_polygon", "SIMPLIFY", "NLCD_LAND", "MULTIPLE_OUTER_PART", None)

arcpy.analysis.PairwiseBuffer("sa_parks", "sa_parks_Buffer", parksBuffer, "NONE", None, "PLANAR", "0 Meters")

arcpy.analysis.SummarizeWithin("sa_parks_Buffer", "sa_cover_polygon", "sa_ParksPatches", "KEEP_ALL", None, "ADD_SHAPE_SUM", "SQUAREMILES", None, "NO_MIN_MAJ", "NO_PERCENT", None)

arcpy.management.CalculateGeometryAttributes("sa_ParksPatches", "totalarea AREA_GEODESIC", '', "SQUARE_MILES_US")

arcpy.management.CalculateField("sa_ParksPatches", "connectScore", "!sum_Area_SQUAREMILES! / !totalarea!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")

arcpy.management.AddJoin("sa_parks", joinfield, "sa_ParksPatches", joinfield, "KEEP_ALL", "NO_INDEX_JOIN_FIELDS")