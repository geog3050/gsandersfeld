### QUIZ 6
### Graham Sandersfeld
### hawkid: gsandersfeld

# calculates the area of inputfcB that intersects with inputfcA and joins and exports the ratio to the inputfcA shapefile
# the joinfield should also be the grouping field for observations in inputfcA
def calcIntersectArea(workspace, inputfcA, inputfcB, joinfield):
    try:
        import os
        import arcpy
        arcpy.env.overwriteOutput = True

        arcpy.env.workspace = workspace

        arcpy.management.CalculateGeometryAttributes(inputfcA, "areasqmi AREA", "MILES_US", "SQUARE_MILES_US", None, "SAME_AS_INPUT")

        arcpy.analysis.Intersect([inputfcB, inputfcA], "b_a_intersect", "ALL", None, "INPUT") # intersect A and B and create an output layer b_a_intersect

        arcpy.management.CalculateGeometryAttributes("b_a_intersect", "areasqmi AREA", "MILES_US", "SQUARE_MILES_US", None, "SAME_AS_INPUT") # calculate the area of the output features by square miles

        arcpy.analysis.Statistics("parks_BGs_intersect", workspace + "b_a_intersect_stats", "areasqmi SUM", "joinfield") # export table with intersection areas grouped by the join field

        arcpy.management.AddJoin(inputfcA, joinfield, "b_a_intersect_stats", joinfield, "KEEP_ALL") # join the intersecting areas to inputfcA

        arcpy.conversion.FeatureClassToFeatureClass("inputfcA", workspace, "intersect_area") # export join to new feature intersect_area

        arcpy.Delete_management("b_a_intersect")
        print("deleted intermediate product b_a_intersect.shp")

        print(arcpy.GetMessages())

    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))


