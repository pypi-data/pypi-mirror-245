# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 13:57:04 2022

@author: lrussell
"""

import pandas as pd
import numpy as np
from shapely.geometry import Point,LineString,Polygon,MultiPolygon,shape
import geopandas as gpd
import rasterio as rio
from rasterio.mask import mask
from rasterio import features
from pysheds.grid import Grid
from scipy.interpolate import RBFInterpolator
import copy
        

def get_terrain(dem_file):
    grid = Grid.from_raster(dem_file)
    dem = grid.read_raster(dem_file)
    
    with rio.open(dem_file) as src:
        nodata = src.nodata
        crs = src.crs
        
    print('Grid loaded')
    
    # Fill depressions, resolve flats and compute flow directions
    pit_filled_dem = grid.fill_pits(dem)
    print('Pits filled')
    flooded_dem = grid.fill_depressions(pit_filled_dem)
    print('Depressions filled')   
    inflated_dem = grid.resolve_flats(flooded_dem, eps=1e-12, max_iter=1e9)
    print('Flats inflated')
    fdir = grid.flowdir(inflated_dem)
    print('Flow direction computed')
    acc = grid.accumulation(fdir)
    acc = acc
    print('Flow accumulation computed')
    
    return [grid,dem,fdir,acc,crs]
        
def get_WS(terrain, pour_point, streamlines=None, catchment=None, threshold=None, snap_threshold=None):
    grid, fdir, acc, crs = terrain[0],terrain[2],terrain[3],terrain[4]
    grid = copy.deepcopy(grid)
    
    if threshold is None:
        threshold = grid.size/100
    if snap_threshold is None:
        snap_threshold = grid.size/10
    
    # Specify outlet
    if isinstance(pour_point,str):
        pour_point = gpd.read_file(pour_point)
    pour_point = pour_point.to_crs(crs)
    pour_point = pour_point.geometry.values[0]
    x0, y0 = pour_point.x, pour_point.y
    
    # Find nearest flow accumulated cell
    xy = grid.snap_to_mask(acc > snap_threshold, np.column_stack([x0,y0]), return_dist=False)
    x = xy[0,0]
    y = xy[0,1]
    
    # Delineate a catchment
    catch = grid.catchment(x=x, y=y, fdir=fdir, xytype='coordinate')
    
    # Clip the grid to the catchment and create shapefile
    grid.clip_to(catch)
    shapes = grid.polygonize()
    for shape in shapes:
        coords = np.asarray(shape[0]['coordinates'][0])
    cm = gpd.GeoDataFrame([],geometry=[Polygon(coords)],crs=crs)   

    if catchment:         
        cm.to_file(catchment)
    print('Catchment delineated')

    # Extract river network to geodataframe 
    branches = grid.extract_river_network(fdir, acc > threshold)
    file = str(branches)
    
    lines = gpd.read_file(file,crs=crs)
    print('Streamlines delineated')
   
    # get upstream and downstream neighbors for each segment
    # create line ids
    lines['FID'] = np.arange(0,len(lines))
    # then create empty columns to hold neighbor ids
    lines['upstream'] = [[np.nan]]*len(lines)
    lines['downstream'] = [[np.nan]]*len(lines)
    
    # for each line...
    for i in lines.FID:
        ind = lines.loc[lines.FID==i].index[0]
        cl = lines.loc[lines.FID==i, 'geometry'].values[0]
        
        # ...find lines within 1 unit of upstream most point
        us_point = Point(cl.coords[0])
        us_reaches_bool = ((lines.geometry.apply(lambda x: Point(x.coords[-1]).distance(us_point) < 0.01)) & (lines.FID!=i))
        if us_reaches_bool.any() == True:
            us_reaches = lines.loc[us_reaches_bool,'FID'].dropna().values
        else:
            us_reaches = [np.nan]    
        lines.at[ind,'upstream'] = us_reaches
        
        # ...find lines within 1 unit of downstream most point
        ds_point = Point(cl.coords[-1])
        ds_reaches_bool = ((lines.geometry.apply(lambda x: Point(x.coords[0]).distance(ds_point) < 0.01)) & (lines.FID!=i))
        if ds_reaches_bool.any() == True:
            ds_reaches = lines.loc[ds_reaches_bool,'FID'].dropna().values[0]
        else:
            ds_reaches = np.nan 
        lines.at[ind,'downstream'] = ds_reaches
    
    print('Neighbors found')
    
    # recursive function to find total distance to pour point
    def get_dist_to_pour_point(i,lines):
        if np.isnan(i):
            return lines
        for j in lines.loc[lines.FID==i,'upstream'].values[0]:
            lines.loc[lines.FID==j,'dist_to_pour_point'] = lines.loc[lines.FID==i,'dist_to_pour_point'].values[0] + lines.loc[lines.FID==i,'geometry'].values[0].length
            
            lines = get_dist_to_pour_point(j,lines)
        
        return lines
    
    # starting with the pour point assign a total distance 
    # call recursive function from pour point
    pour_point = lines.loc[lines.downstream.isnull(),'FID'].values[0]
    lines.loc[lines.FID==pour_point,'dist_to_pour_point'] = 0
    lines = get_dist_to_pour_point(pour_point,lines)
    lines.crs = crs
    
    # this will find the segments of the longest stream path
    lines['us_dist'] = lines.dist_to_pour_point + lines.geometry.length
    farthest_reaches = lines[lines.us_dist==lines.us_dist.max()]
    if len(farthest_reaches) > 1:
        i = farthest_reaches.loc[farthest_reaches.geometry.length==farthest_reaches.geometry.length.max(), 'FID'].values[0]
    else:
        i = farthest_reaches.FID.values[0]
    print('Distance to pour point computed')
    
    sl = lines.copy()
    del sl['upstream']
    del sl['downstream']
    sl.index = np.arange(len(sl))
    
    if streamlines:
        sl.to_file(streamlines)
        
    return [sl,cm]
        
def get_XS(lines,xs_length,id_col=None,spacing=None):
    if isinstance(lines,str):
        lines = gpd.read_file(lines)

    xs_lines = gpd.GeoDataFrame([],columns=['CSID','Distance','geometry'],crs=lines.crs)
    
    for idx,row in lines.iterrows():
        num_xsecs = int(row.geometry.length/spacing)
        
        for xs in range(1,num_xsecs):
            point = row.geometry.interpolate(xs*spacing)
            pointA = row.geometry.interpolate(xs*spacing-100)
            pointB = row.geometry.interpolate(xs*spacing+100)
            
            deltaX = pointA.x-pointB.x
            deltaY = pointA.y-pointB.y
            if deltaX==0:
                deltaX=0.0000000000001
            slope = deltaY/deltaX
            theta = np.arctan(slope)
            new_theta = (theta + np.pi/2)%np.pi
            
            line_end1 = Point(point.x+xs_length*np.cos(new_theta), point.y+xs_length*np.sin(new_theta))
            line_end2 =  Point(point.x-xs_length*np.cos(new_theta), point.y-xs_length*np.sin(new_theta))
            
            line = LineString([line_end1,line_end2])
            
            xs_lines.loc[len(xs_lines)] = [idx,xs*spacing,line]
    
    xs_lines = gpd.GeoDataFrame(xs_lines,geometry=xs_lines.geometry,crs=xs_lines.crs)
    xs_lines.set_crs(lines.crs, inplace=True)
    return xs_lines

def get_points(lines,spacing,end_point=True,csid_col=None):
    if isinstance(lines,str):
        lines = gpd.read_file(lines)
        
    points = gpd.GeoDataFrame([],columns=['CSID','Station','geometry'],crs=lines.crs)
        
    if not csid_col:
        if end_point:
            for j,l in lines.iterrows():
                intervals = np.arange(0,l.geometry.length,spacing)
                temp = gpd.GeoDataFrame([],columns=['CSID','Station','geometry'],crs=lines.crs)
                temp['Station'] = intervals
                temp['CSID'] = j
                temp['geometry'] = temp['Station'].apply(lambda x: l.geometry.interpolate(x))
                points = gpd.GeoDataFrame(pd.concat([points,temp],ignore_index=True),crs=lines.crs)
                if end_point==True:
                    if l.geometry.geom_type == 'MultiLineString':
                        for ll in l.geometry.geoms:
                            ep = Point(np.array(ll.coords)[-1])
                            points.loc[len(points)] = [j,ll.length,ep]
                            points.crs = lines.crs
                    else:
                        ep = Point(np.array(l.geometry.coords)[-1])
                        points.loc[len(points)] = [j,l.geometry.length,ep]
                        points.crs = lines.crs

        else:
            for j,l in lines.iterrows():
                intervals = np.arange(0,l.geometry.length,spacing)
                temp = gpd.GeoDataFrame([],columns=['CSID','Station','geometry'],crs=lines.crs)
                temp['Station'] = intervals
                temp['CSID'] = j
                temp['geometry'] = temp['Station'].apply(lambda x: l.geometry.interpolate(x))
                points = gpd.GeoDataFrame(pd.concat([points,temp],ignore_index=True),crs=lines.crs)
                if end_point==True:
                    if l.geometry.geom_type == 'MultiLineString':
                        for ll in l.geometry.geoms:
                            ep = Point(ll.coords[-1])
                            points.loc[len(points)] = [j,ll.length,ep]
                            points.crs = lines.crs
                    else:
                        ep = Point(l.geometry.coords[-1])
                        points.loc[len(points)] = [j,l.geometry.length,ep]
                        points.crs = lines.crs
    else:
        if end_point:
            for j,l in lines.iterrows():
                intervals = np.arange(0,l.geometry.length,spacing)
                temp = gpd.GeoDataFrame([],columns=['CSID','Station','geometry'],crs=lines.crs)
                temp.set_crs(lines.crs, inplace=True)
                temp['Station'] = intervals
                temp['CSID'] = l[csid_col]
                temp['geometry'] = temp['Station'].apply(lambda x: l.geometry.interpolate(x))
                points = gpd.GeoDataFrame(pd.concat([points,temp],ignore_index=True),crs=lines.crs)
                if end_point==True:
                    if l.geometry.geom_type == 'MultiLineString':
                        for ll in l.geometry:
                            ep = Point(ll.coords[-1])
                            points.loc[len(points)] = [l[csid_col],ll.length,ep]
                    else:
                        ep = Point(l.geometry.coords[-1])
                        points.loc[len(points)] = [l[csid_col],l.geometry.length,ep]
        else:
            for j,l in lines.iterrows():
                intervals = np.arange(0,l.geometry.length,spacing)
                temp = gpd.GeoDataFrame([],columns=['CSID','Station','geometry'],crs=lines.crs)
                temp.set_crs(lines.crs, inplace=True)
                temp['Station'] = intervals
                temp['CSID'] = l[csid_col]
                temp['geometry'] = temp['Station'].apply(lambda x: l.geometry.interpolate(x))
                points = gpd.GeoDataFrame(pd.concat([points,temp],ignore_index=True),crs=lines.crs)
                if end_point==True:
                    if l.geometry.geom_type == 'MultiLineString':
                        for ll in l.geometry:
                            ep = Point(ll.coords[-1])
                            points.loc[len(points)] = [l[csid_col],ll.length,ep]
                    else:
                        ep = Point(l.geometry.coords[-1])
                        points.loc[len(points)] = [l[csid_col],l.geometry.length,ep]
            
    #points = gpd.GeoDataFrame(points,geometry=points.geometry,crs=lines.crs)
    points.set_crs(lines.crs, inplace=True)
    return points

def sample_raster(raster,points,buff=None,metric='min',multiband=False):
    def _get_metric(buff_geom,src,metric):
        masked_array = mask(src, [buff_geom], crop=True)[0]
        masked_array = np.ma.masked_where(masked_array==src.nodata,masked_array)
        if metric == 'min':
            value = masked_array.min()
        elif metric == 'max':
            value = masked_array.max()
        elif metric == 'mean':
            value = masked_array.mean()
        elif metric == 'mode':
            value = masked_array.mode()
        return value
    
    if isinstance(points,str):
        points = gpd.read_file(points)
    
    with rio.open(raster) as src:
        points = points.to_crs(src.crs)
        if buff:
            points.geometry = points.geometry.buffer(buff)
            sampled_data = points.geometry.apply(lambda buffer_geom: _get_metric(buffer_geom,src,metric))
        else:
            if multiband:
                sampled_data = [x.tolist() for x in src.sample(zip(points.geometry.x,points.geometry.y),masked=True)]
            else:
                sampled_data = [x.tolist()[0] for x in src.sample(zip(points.geometry.x,points.geometry.y),masked=True)]
    
    return sampled_data

def create_REM(dem_file,points,output_file,Z_col='Z',use_blocks=False,limits=[-50,50],surface_file=None):
          
    # before we go any further lets clip the raster to the buffer of the centerline
    with rio.open(dem_file,'r') as src:
       
        if isinstance(points,str):
            points = gpd.read_file(points)
        
        profile = src.profile.copy()
        profile['driver'] = 'GTiff'
        with rio.open(output_file,'w',**profile) as dst:
            # get xyz of all points in preferred input for Rbf interpolator
            points = points.drop_duplicates()
            points = points.dropna()
           
            clr,clc = rio.transform.rowcol(profile['transform'], points.geometry.x, points.geometry.y)
            points['R'] = clr
            points['C'] = clc
            points['temp_Z'] = 1
                        
            rbfi = RBFInterpolator(np.vstack([points.C,points.R]).T, points[Z_col], kernel='linear')
                
            # write HAWS
            if use_blocks == False:
                dem = dst.read(1)
                
                ci,ri = np.meshgrid(np.arange(dem.shape[1]), np.arange(dem.shape[0]))
                wse = rbfi(np.vstack(ci.flatten(),ri.flatten()).T)
                wse = wse.reshape(dem.shape)
                haws = dem - wse
                dst.write(haws,indexes=1)
                
                if surface_file:
                    with rio.open(surface_file,'w',**profile) as wse_dst:
                        wse_dst.write(wse,indexes=1)
                
            else:
                # write HAWS in blocks/windows (slower but works for large files)
                num_blocks = len(list(dst.block_windows(1)))
                for block_index, win in dst.block_windows(1):
                    print('\rWriting block {0} out of {1}'.format(str(block_index[0]),str(num_blocks)),end='')
                    
                    # get block data and transform
                    dem_block = dst.read(1,window=win)
                    win_transform = dst.window_transform(win)
                    
                    # get world coordinates from block array coordinates via window transform
                    ci,ri = np.meshgrid(np.arange(win.width), np.arange(win.height))
                    
                    #get WSE surface for block and subtract from elevation surface
                    wse_block = rbfi(ci,ri)
                    haws_block = dem_block - wse_block
                    haws_block = haws_block.reshape((1,haws_block.shape[0],haws_block.shape[1]))
                    
                    dst.write(haws_block,window=win) 
    
    # this last will set all values above/below the set limits to nodata
    if limits is not None:
        with rio.open(output_file, 'r+') as src:
            array = src.read(1)
            
            array = np.where(array>limits[1],-9999,array)
            array = np.where(array<limits[0],-9999,array)
                        
            src.write(array,indexes=1)
            
    print('\nHAWS created at {0}'.format(output_file))
        
def inundate(raster,rel_wse_list,largest_only=False):
    
    with rio.open(raster) as src:

        array = src.read(1)
        affine = src.transform
        nodata = src.nodata
        crs = src.crs
        masked_array = np.ma.masked_where(array==nodata,array)

        inundated = gpd.GeoDataFrame([],crs=src.crs,geometry=[],columns=['WSE'])
        
        for wse in rel_wse_list:  
            
            inundation_array = np.ma.where(masked_array<=wse,1,0)
            inundation_array = np.ma.masked_where(inundation_array==0,inundation_array)
            #inundation_array = inundation_array.data.astype('int32')
            
            if largest_only==True:
                poly=Polygon([])
                for shapedict, value in features.shapes(inundation_array,transform=affine):
                    if value == 1:
                        if shape(shapedict).area > poly.area:
                            poly = shape(shapedict).buffer(0)
                inundated.loc[len(inundated)] = [wse,poly]
            else:
                polys = []
                for shapedict, value in features.shapes(inundation_array,transform=affine):
                    if value == 1:
                        polys.append(shape(shapedict).buffer(0))
                geom = MultiPolygon(polys)
                inundated.loc[len(inundated)] = [wse,geom]
                
            print('Completed inundation mapping for {0} feet above WSE'.format(wse))
    
    inundated = inundated.set_geometry('geometry')
    inundated.WSE = inundated.WSE.astype(float)
    inundated.crs = crs
    #inundated = gpd.GeoDataFrame(inundated,geometry=inundated.geometry,crs=inundated.crs)
    
    return inundated


