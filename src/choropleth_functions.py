import numpy as np
import pandas as pd
import geopandas as gpd
import folium

def clean_shape_names(string):
    return string.replace('- ', '')

def clean_neighborhood_names(string):
    name =  ' '.join([x.capitalize() for x in string.split('-')])
    if name == 'Dia':
        return 'DIA'
    return name

def prepare_shapefile_dataframe():
    """ Returns a cleaned pandas dataframe from .shp file provided on 
        https://www.denvergov.org/opendata/dataset/city-and-county-of-denver-statistical-neighborhoods
        
        Dataframe has columns 'NBHD_ID' (neighborhood id)
                               'NBHD_NAME' (neighborhood name)
                               'geometry' (polygons for neighborhood boundaries)
    """
    shape_df = gpd.read_file("../data/statistical_neighborhoods/statistical_neighborhoods.shp")
    shape_df.drop(['TYPOLOGY', 'NOTES'], axis=1, inplace=True)
    shape_df = shape_df[~(shape_df.NBHD_NAME == 'CBD')]
    shape_df['NBHD_NAME'] = shape_df['NBHD_NAME'].map(clean_shape_names)
    return shape_df

def create_denver_geodataframe(crime_df, shape_df):
    """ Args: 
            crime_df: pandas crime data frame
            shape_df: pandas shape data frame for same location as crime_df
        Returns a pandas dataframe merging crime_df and shape_df by neighborhoods
        (Removes rows where NEIGHBORHOOD_ID is null or cannot be determined.)
    """
    crime = crime_df[['INCIDENT_ID', 'OFFENSE_CATEGORY_ID', 'year', 'NEIGHBORHOOD_ID']].copy()
    crime['NEIGHBORHOOD_ID'] = crime['NEIGHBORHOOD_ID'].map(clean_neighborhood_names, na_action='ignore')
    crime = crime[~((crime['NEIGHBORHOOD_ID'].isin(['cbd', 'Cbd'])) | (crime['NEIGHBORHOOD_ID'].isnull()))]

    geo_df = pd.merge(left=crime, right=shape_df, left_on='NEIGHBORHOOD_ID', right_on='NBHD_NAME')
    return geo_df

def count_by_category_and_year(df, shape_df, category, years = [2020]):
    """ Finds the counts for the specified category for each neighborhood (NEIGHBORHOOD_ID) for specified years
        Returns dataframe with columns 'id', 'geometry', 'neighborhood', 'Count'
        Args:
            df: pandas crime dataframe 
            shape_df: pandas dataframe of cleaned .shp (see prepare_shapefile_dataframe function above)
            category: a string - the category your finding the counts for 
            years: list of years included in count
    """
    count_df = (df[(df['OFFENSE_CATEGORY_ID']==category) & (df['year'].isin(years))]
                            .groupby('NEIGHBORHOOD_ID')['INCIDENT_ID'].count().reset_index()
                              .rename(columns={'INCIDENT_ID': 'Count', 'NEIGHBORHOOD_ID' :'Neighborhood'}))
    
    merged_count = pd.merge(left=shape_df, right=count_df, left_on='NBHD_NAME', right_on='Neighborhood').rename(columns = {'NBHD_ID': 'id'})
    merged_count.drop(['NBHD_NAME'], axis=1, inplace=True)
    return merged_count

def choropleth_plot(data, myscale, category, years):
    """ Returns a folium choropleth map 
        Args: 
            data: a pandas dataframe with geodata
            myscale: the scale you are specifying for folium Choropleth threshold_scale
            category: a string, the crime category you are filtering for
            years: a list of years to be included in the plot
    """
    mapa = folium.Map(location=[39.7807, -104.8208], 
               tiles="CartoDB positron", 
               zoom_start=11.25)

    folium.Choropleth(
        geo_data=data,
        name='choropleth',
        data=data,
        columns=['Neighborhood','Count'], 
        key_on='feature.properties.Neighborhood',
        fill_color='OrRd',
        threshold_scale=myscale,
        fill_opacity=0.5,
        line_opacity=0.75,
        legend_name=f'{category} in {years}'
    ).add_to(mapa)

    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}

    hover_feature = folium.features.GeoJson(
        data,
        style_function=style_function, 
        tooltip=folium.features.GeoJsonTooltip(
            fields=['Neighborhood','Count'], 
            aliases=['Neighborhood: ', f'Count of {category} incidences: '],
        )
    )

    mapa.add_child(hover_feature)
    return mapa

def choropleth_compare_two_years(denver_crime_df, category, year1, year2):
    """ Saves two choropleth maps as html files for the category and years specified
        Creates a consistent threshold_scale across both years for comparison
        Args:
            denver_crime_df: a pandas dataframe for denver crime
            category: a string, the crime category you are filtering for
            year1: a integer specifying the first year you'd like to make a map for in format YYYY
            year2: a integer specifying the second year you'd like to make a map for in format YYYY
    """
    shape_df = prepare_shapefile_dataframe()
    geo_df = create_denver_geodataframe(denver_crime_df, shape_df)
    
    year1_data = count_by_category_and_year(geo_df, shape_df, category, [year1])
    year2_data = count_by_category_and_year(geo_df, shape_df, category, [year2])
    
    myscale = (pd.concat([year1_data, year2_data]).Count.quantile((0,0.1,0.75,0.9,0.98,1))).tolist()
    
    m1 = choropleth_plot(year1_data, myscale, category, [year1])
    m2 = choropleth_plot(year2_data, myscale, category, [year2])
    
    m1.save(f'../html/Denver_{category}_choropleth_{year1}.html')
    m2.save(f'../html/Denver_{category}_choropleth_{year2}.html')
