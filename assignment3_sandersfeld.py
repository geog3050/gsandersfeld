###################################################################### 
# Edit the following function definition, replacing the words
# 'name' with your name and 'hawkid' with your hawkid.
# 
# Note: Your hawkid is the login name you use to access ICON, and not
# your firsname-lastname@uiowa.edu email address.
# 
# def hawkid():
#     return(["Caglar Koylu", "ckoylu"])
###################################################################### 
def hawkid():
    return(["Graham Sandersfeld", "gsandersfeld"])

###################################################################### 
# Problem 1 (10 Points)
#
# This function reads all the feature classes in a workspace (folder or geodatabase) and
# prints the name of each feature class and the geometry type of that feature class in the following format:
# 'states is a point feature class'

###################################################################### 
import arcpy
import os

arcpy.env.overwriteOutput = True

def printFeatureClassNames(workspace):
    try: 
        arcpy.env.workspace = workspace
        featureclasses = arcpy.ListFeatureClasses()
        for fc in featureclasses:
            describe_fc = arcpy.Describe(fc)
            if describe_fc.shapeType == "Polygon":
                print(fc + " is a polygon feature class")
            elif describe_fc.shapeType == "Polyline":
                print(fc + " is a polyline feature class")
            elif describe_fc.shapeType == "Point":
                print(fc + " is a point feature class")
            else:
                print("Type unknown")

    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))

###################################################################### 
# Problem 2 (20 Points)
#
# This function reads all the attribute names in a feature class or shape file and
# prints the name of each attribute name and its type (e.g., integer, float, double)
# only if it is a numerical type

###################################################################### 
def printNumericalFieldNames(inputFc, workspace):
    try:
        arcpy.env.workspace = workspace
        fields = arcpy.ListFields(inputFc)
        for field in fields:
            if field.type in ("Integer", "SmallInteger", "Double", "Single"):
                print("{0} is a type of {1} with length {2}" .format(field.name, field.type, field.length))

    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))
                
###################################################################### 
# Problem 3 (30 Points)
#
# Given a geodatabase with feature classes, and shape type (point, line or polygon) and an output geodatabase:
# this function creates a new geodatabase and copying only the feature classes with the given shape type into the new geodatabase

###################################################################### 
def exportFeatureClassesByShapeType(input_geodatabase, shapeType, output_geodatabase):
    if shapeType not in ("Polygon", "Polyline", "Point", "Multipoint", "MultiPatch"):
        print("shapeType must be Polygon, Polyline, Point, Multipoint, or MultiPatch [with quotes]") # only the accepted shape types should be given as arguments
    try:
        arcpy.env.workspace = input_geodatabase
        featureclasses = arcpy.ListFeatureClasses()
        mygdb = output_geodatabase
        dir_path = os.path.dirname(os.path.realpath(mygdb))
        outgdb = os.path.basename(mygdb)
        print("directory:   ", dir_path)
        print("output workspace:   ", outgdb)
        arcpy.CreateFileGDB_management(dir_path, outgdb)
        print(outgdb, " successfully created")
        for fc in featureclasses:
            descObject = arcpy.Describe(fc)
            if descObject.shapeType == shapeType:
                out_featureclass = os.path.join(mygdb, os.path.splitext(fc)[0])
                arcpy.CopyFeatures_management(fc, out_featureclass)

    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))

###################################################################### 
# Problem 4 (40 Points)
#
# Given an input feature class or a shape file and a table in a geodatabase or a folder workspace,
# join the table to the feature class using one-to-one and export to a new feature class.
# Print the results of the joined output to show how many records matched and unmatched in the join operation. 

###################################################################### 
def exportAttributeJoin(inputFc, outputFc, idFieldInputFc, inputTable, idFieldTable, workspace):
    try:
        arcpy.env.workspace = workspace
        val_res = arcpy.ValidateJoin_management(inputFc, idFieldInputFc, inputTable, idFieldTable)
        matched = int(val_res[0]) 
        row_count = int(val_res[1]) # information about this join

        print(arcpy.GetMessages()) # prints ArcGIS output about the join

        if matched >= 1:
            fc_joined_table = arcpy.AddJoin_management(inputFc, idFieldInputFc, inputTable, idFieldTable) # if join is valid, perform the join
            arcpy.CopyFeatures_management(fc_joined_table, outputFc) # and export to a new feature class

        print(f"Output Features: {outputFc} had matches {matched} and created {row_count} records")

    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
