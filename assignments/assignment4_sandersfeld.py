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
# Problem 1 (20 points)
# 
# Given an input point feature class (e.g., facilities or hospitals) and a polyline feature class, i.e., bike_routes:
# Calculate the distance of each facility to the closest bike route and append the value to a new field.
#        
###################################################################### 
def calculateDistanceFromPointsToPolylines(input_geodatabase, fcPoint, fcPolyline):
    import os
    import arcpy
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = input_geodatabase
    try:
        arcpy.analysis.Near(fcPoint, fcPolyline, None, "NO_LOCATION", "NO_ANGLE", "GEODESIC", "NEAR_FID NEAR_FID;NEAR_DIST NEAR_DIST") # writes nearest distances to a new field NEAR_DIST

    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2)) 

######################################################################
# Problem 2 (30 points)
# 
# Given an input point feature class, i.e., facilities, with a field name (FACILITY) and a value ('NURSING HOME'), and a polygon feature class, i.e., block_groups:
# Count the number of the given type of point features (NURSING HOME) within each polygon and append the counts as a new field in the polygon feature class
#
######################################################################
def countPointsByTypeWithinPolygon(input_geodatabase, fcPoint, pointFieldName, pointFieldValue, fcPolygon):
    try:
        arcpy.env.workspace = input_geodatabase
        where = pointFieldName + " = " + "'" + pointFieldValue + "'" # SQL statement from variables
        arcpy.management.SelectLayerByAttribute(fcPoint, "NEW_SELECTION", where, None) # select the point features by values
        arcpy.analysis.SpatialJoin(fcPolygon, fcPoint, pointFieldValue.replace(' ', '') + "_ptsInP","JOIN_ONE_TO_MANY", "KEEP_ALL", None, "CONTAINS") # count of points with input values is found in "Join_Count" attribute of ptsInPolygon.shp
        arcpy.management.SelectLayerByAttribute(fcPoint, "CLEAR_SELECTION", '', None) # clear the selection

    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))

######################################################################
# Problem 3 (50 points)
# 
# Given a polygon feature class, i.e., block_groups, and a point feature class, i.e., facilities,
# with a field name within point feature class that can distinguish categories of points (i.e., FACILITY);
# count the number of points for every type of point features (NURSING HOME, LIBRARY, HEALTH CENTER, etc.) within each polygon and
# append the counts to a new field with an abbreviation of the feature type (e.g., nursinghome, healthcenter) into the polygon feature class 

# HINT: If you find an easier solution to the problem than the steps below, feel free to implement.
# Below steps are not necessarily explaining all the code parts, but rather a logical workflow for you to get started.
# Therefore, you may have to write more code in between these steps.

# 1- Extract all distinct values of the attribute (e.g., FACILITY) from the point feature class and save it into a list
# 2- Go through the list of values:
#    a) Generate a shortened name for the point type using the value in the list by removing the white spaces and taking the first 13 characters of the values.
#    b) Create a field in polygon feature class using the shortened name of the point type value.
#    c) Perform a spatial join between polygon features and point features using the specific point type value on the attribute (e.g., FACILITY)
#    d) Join the counts back to the original polygon feature class, then calculate the field for the point type with the value of using the join count field.
#    e) Delete uncessary files and the fields that you generated through the process, including the spatial join outputs.  
######################################################################
def countCategoricalPointTypesWithinPolygons(fcPoint, pointFieldName, fcPolygon, fcPolyJoinField, workspace):
    # This function might cause ArcGIS Pro to hang - call it with caution. I couldn't figure out the full solution to this problem past the joins. But I came close:
    try:
        arcpy.env.workspace = workspace
        # Extract attribute values
        myList = [row[0] for row in arcpy.da.SearchCursor(fcPoint, pointFieldName)]
        # Convert list to a set to remove duplicates and convert back to a list
        pointAttbSet = set(myList)
        pointAttbList = list(pointAttbSet)

        # remove spaces in the list items
        myListNoSpace = [x.replace(' ', '') for x in pointAttbList]

        # remove characters after the 13th in each item
        allPointFieldValues = [elem[:13] for elem in myListNoSpace]

        # add as many fields to the polygon fc as there are types of points
        for i in range(0, len(allPointFieldValues)):
            arcpy.management.AddField(fcPolygon, allPointFieldValues[i], "DOUBLE")
        # run the function from problem 2 for each attribute and join the counts to original polygon FC
        for x in range(0,len(pointAttbList)):
            countPointsByTypeWithinPolygon("", fcPoint, pointFieldName, pointAttbList[x], fcPolygon)
            arcpy.management.AddJoin(fcPolygon, fcPolyJoinField, pointAttbList[x].replace(' ', '') + "_ptsInP", fcPolyJoinField, "KEEP_ALL", "NO_INDEX_JOIN_FIELDS")
    
    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))


######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
