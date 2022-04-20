import os

import arcpy

import sys

arcpy.env.overwriteOutput = True

arcpy.env.workspace = "C:/Users/GSandersfeld/OneDrive/Documents/21-22/Spring/GEOG 3050 Geospatial Programming/airports"

print(arcpy.env.workspace)

fc = "airports.shp"

inFeatures = 'airports'
fieldName = 'BUFF_DIST'
fieldPrecision = 9
fieldAlias = 'bufferdistance'

try:
    arcpy.AddField_management(inFeatures, fieldName, "TEXT", fieldPrecision, field_alias=fieldAlias, field_is_nullable="NULLABLE")
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])
    arcpy.AddError(e.args[0])

myFields = ['FEATURE', 'BUFF_DIST']

with arcpy.da.UpdateCursor(fc, myFields) as cursor:
    for row in cursor:
        if row[0] == 'Seaplane Base':
            row[1] = '7500 Meters'
        elif row[0] == 'Airport':
            row[1] = '15000 Meters'
        else: continue
        cursor.updateRow(row)

try:
    arcpy.Buffer_analysis(fc, 'buffer_airports', 'BUFF_DIST')
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])
    arcpy.AddError(e.args[0])


