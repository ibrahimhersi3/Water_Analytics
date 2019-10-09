# -*- coding: utf-8 -*-
"""
Created on Mon feb 18 11:01:20 2019

@author: Ibrahim
"""
import numpy as np 
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, save
from bokeh.models import HoverTool
import geopandas as gpd
import pandas as pd
import pdb
#from bokeh.tile_providers import get_provider, Vendors
from bokeh.tile_providers import STAMEN_TONER
import osmnx as ox
 
from shapely import wkt
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_colwidth',1000)
pd.set_option('display.width',None)
#pdb.set_trace()
def getXYCoords(geometry, coord_type):

    if coord_type == 'x':
        return geometry.coords.xy[0]
    elif coord_type == 'y':
        return geometry.coords.xy[1]

def getPolyCoords(geometry, coord_type):

    ext = geometry.exterior
    return getXYCoords(ext, coord_type)

def getLineCoords(geometry, coord_type):

    return getXYCoords(geometry, coord_type)

def getPointCoords(geometry, coord_type):

    if coord_type == 'x':
        return geometry.x
    elif coord_type == 'y':
        return geometry.y


def multiGeomHandler(multi_geometry, coord_type, geom_type):


    for i, part in enumerate(multi_geometry):

        if i == 0:
            if geom_type == "MultiPoint":
                coord_arrays = np.append(getPointCoords(part, coord_type), np.nan)
            elif geom_type == "MultiLineString":
                coord_arrays = np.append(getLineCoords(part, coord_type), np.nan)
            elif geom_type == "MultiPolygon":
                coord_arrays = np.append(getPolyCoords(part, coord_type), np.nan)
        else:
            if geom_type == "MultiPoint":
                coord_arrays = np.concatenate([coord_arrays, np.append(getPointCoords(part, coord_type), np.nan)])
            elif geom_type == "MultiLineString":
                coord_arrays = np.concatenate([coord_arrays, np.append(getLineCoords(part, coord_type), np.nan)])
            elif geom_type == "MultiPolygon":
                coord_arrays = np.concatenate([coord_arrays, np.append(getPolyCoords(part, coord_type), np.nan)])

    return coord_arrays

def getCoords(row, geom_col, coord_type):


    geom = row[geom_col]


    gtype = geom.geom_type


    if gtype == "Point":
        return getPointCoords(geom, coord_type)
    elif gtype == "LineString":
        return list( getLineCoords(geom, coord_type) )
    elif gtype == "Polygon":
        return list( getPolyCoords(geom, coord_type) )


    else:
        return list( multiGeomHandler(geom, coord_type, gtype) )
#pdb.set_trace()
#url1 = r"C:\Users\Ibrahim Hersi\.spyder-py3\unlabeled_data_ml4.csv"
url1 = r"C:\Users\Ibrahim Hersi\.spyder-py3\unlabeled_dataKnn.csv"

unlabeled = pd.read_csv(url1)
unlabeled['geometry'] = unlabeled['geometry'].apply(wkt.loads)
df2 = gpd.GeoDataFrame(unlabeled, geometry = 'geometry')


url = r"C:\Users\Ibrahim Hersi\Desktop\docs\docs\labeled_data.csv"


labeled = pd.read_csv(url)
labeled['geometry'] = labeled['geometry'].apply(wkt.loads)
df1 = gpd.GeoDataFrame(labeled, geometry = 'geometry')
 
indus = r"C:\Users\Ibrahim Hersi\Desktop\docs\docs\industrail.csv"
induss = pd.read_csv(indus)
induss['geometry'] = induss['geometry'].apply(wkt.loads)
induss1 = gpd.GeoDataFrame(induss, geometry = 'geometry')
#ml = r"C:\Users\Ibrahim Hersi\.spyder-py3\unlabeled_data_ml2.csv"
#ml = pd.read_csv(ml)
 
place= "Uppsala, Uppsala County"


#uni_amenities = ['university']
#uni = ox.pois_from_address(place, distance =2000,amenities=uni_amenities)[['geometry',
#                                                                              'name',
#                                                                              'element_type',
#                                                                           ]]

#restaurant_amenities = ['restaurant','cafe', 'fast_food']
#restaurants = ox.pois_from_address(place, distance =20000,
#                                 amenities=restaurant_amenities)[['geometry',
#                                                                  'name',
#                                                                  'amenity',
#                                                                  'cuisine',
#                                                                 'element_type']]


#restaurants = restaurants.to_crs(epsg=3857)
#uni = uni.to_crs(epsg=3857)
#ml= ml.to_crs(epsg=3857)
df1.crs = {'init' :'epsg:3857'}
df2.crs = {'init' :'epsg:3857'}
induss1.crs = {'init' :'epsg:3857'}
#ml.crs = {'init' :'epsg:3857'}



#restaurants.name.fillna('', inplace=True)
#uni.name.fillna('campus', inplace=True)
#restaurants.cuisine.fillna('?', inplace=True)

#for item in ['way', 'relation']:
#   restaurants.loc[restaurants.element_type==item, 'geometry'] = \
#   restaurants[restaurants.element_type==item]['geometry'].map(lambda x: x.centroid)

#for item in ['way', 'relation']:
#   uni.loc[uni.element_type==item, 'geometry'] = \
#   uni[uni.element_type==item]['geometry'].map(lambda x: x.centroid)


df1['x'] = df1.apply(getCoords, geom_col='geometry', coord_type='x', axis=1)
df1['y'] = df1.apply(getCoords, geom_col='geometry', coord_type='y', axis=1)

df2['x'] = df2.apply(getCoords, geom_col='geometry', coord_type='x', axis=1)
df2['y'] = df2.apply(getCoords, geom_col='geometry', coord_type='y', axis=1)

induss['x'] = induss.apply(getCoords, geom_col='geometry', coord_type='x', axis=1)
induss['y'] = induss.apply(getCoords, geom_col='geometry', coord_type='y', axis=1)


g_df= df1.drop('geometry', axis=1).copy()
msource = ColumnDataSource(g_df)


#ml = ColumnDataSource(ml)

g_df2= df2.drop('geometry', axis=1).copy()
df2source = ColumnDataSource(g_df2)

indus1= induss.drop('geometry', axis=1).copy()
indus1source = ColumnDataSource(indus1)




#source = ColumnDataSource(data=dict(
#    x=restaurants.geometry.x,
#    y=restaurants.geometry.y,
#    name=restaurants.name.values,
#    cuisine=restaurants.cuisine.values
#    ))

#Psource = ColumnDataSource(data=dict(
#    x=uni.geometry.x,
#    y=uni.geometry.y,
#    name=uni.name.values


#    ))


TOOLS = "pan,wheel_zoom,reset"
p = figure(title="OSM restaurants", tools=TOOLS,
           match_aspect=True, x_axis_location=None, y_axis_location=None,
           active_scroll='wheel_zoom')



#tooltips = [
 #           ('Name', '@name'),('Cuisine', '@cuisine'),('Avg Wtr demand', '21.95539 m3'),
 #          ]
#tooltipss = [
#            ('Name', '@name'),('Avg Wtr demand', '50.658 m3')]
tooltipsss = [
            ('building', '@building'),('Avg Wtr demand', '565 m3'),('Prediction', 'OSM')]

tooltipssss = [('building', '@buildings'),('Avg Wtr demand', '565 m3'),('Prediction', 'Knn Algorithm')]

tooltipsssss = [
            ('building', '@building'),('Avg Wtr demand', '1478 m3'),('Prediction', '@Prediction')]

p.grid.grid_line_color = None
#ibrahim = get_provider(Vendors.CARTODBPOSITRON)
p.add_tile(STAMEN_TONER, alpha=.3)
#p.add_tile(ibrahim)


#r2=p.circle('x', 'y',color='red', source=source, legend='Resturant',fill_alpha=0.6, size=6)
#r3=p.circle('x', 'y', source=Psource, legend='University',fill_alpha=0.6, size=10)
r4=p.patches('x', 'y', color='orange',source=msource,fill_alpha=0.6)
r5=p.patches('x', 'y', color='orange',source=df2source, legend='meadium Water demand',fill_alpha=0.6)
r6=p.patches('x', 'y', color='red',source=indus1source, legend='high Water demand',fill_alpha=0.6)             
#r6=p.patches('x', 'y', color='orange',source=ml, legend='machine learning builings',fill_alpha=0.6)

#p.add_tools(HoverTool(renderers=[r2], tooltips= tooltips ))
#p.add_tools(HoverTool(renderers=[r3], tooltips=tooltipss))
p.add_tools(HoverTool(renderers=[r4], tooltips=tooltipsss))
p.add_tools(HoverTool(renderers=[r5], tooltips=tooltipssss))
p.add_tools(HoverTool(renderers=[r6], tooltips=tooltipsssss))
outfp= r"C:\Users\Ibrahim Hersi\Desktop\omnxRest112.html"
save(obj=p, filename=outfp)
