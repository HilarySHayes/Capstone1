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

def count_by_category_and_year(df, shape_df, category, years = [2020]):
    count_df = (df[(df['OFFENSE_CATEGORY_ID']==category) & (df['YEAR'].isin(years))]
                            .groupby('NEIGHBORHOOD_ID')['INCIDENT_ID'].count().reset_index()
                              .rename(columns={'INCIDENT_ID': 'Count', 'NEIGHBORHOOD_ID' :'Neighborhood'}))
    
    merged_count = pd.merge(left=shape_df, right=count_df, left_on='NBHD_NAME', right_on='Neighborhood').rename(columns = {'NBHD_ID': 'id'})
    merged_count.drop(['NBHD_NAME'], axis=1, inplace=True)
    return merged_count

def choropleth_plot(data, myscale, category, years):
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

def prepare_shapefile_dataframe():
    shape_df = gpd.read_file("../data/statistical_neighborhoods/statistical_neighborhoods.shp")
    shape_df.drop(['TYPOLOGY', 'NOTES'], axis=1, inplace=True)
    shape_df = shape_df[~(shape_df.NBHD_NAME == 'CBD')]
    shape_df['NBHD_NAME'] = shape_df['NBHD_NAME'].map(clean_shape_names)
    return shape_df

def create_denver_geodataframe(crime_df, shape_df):
    crime = crime_df[['INCIDENT_ID', 'OFFENSE_CATEGORY_ID', 'YEAR', 'NEIGHBORHOOD_ID']].copy()
    crime['NEIGHBORHOOD_ID'] = crime['NEIGHBORHOOD_ID'].map(clean_neighborhood_names, na_action='ignore')
    crime = crime[~((crime['NEIGHBORHOOD_ID'].isin(['cbd', 'Cbd'])) | (crime['NEIGHBORHOOD_ID'].isnull()))]

    geo_df = pd.merge(left=crime, right=shape_df, left_on='NEIGHBORHOOD_ID', right_on='NBHD_NAME')
    return geo_df

def create_double_choropleth_plots(denver_crime_df, category):
    shape_df = prepare_shapefile_dataframe()
    geo_df = create_denver_geodataframe(denver_crime_df, shape_df)
    
    data2020 = count_by_category_and_year(geo_df, shape_df, category, [2020])
    data2019 = count_by_category_and_year(geo_df, shape_df, category, [2019])
    
    myscale = (pd.concat([data2020, data2019]).Count.quantile((0,0.1,0.75,0.9,0.98,1))).tolist()
    
    m2020 = choropleth_plot(data2020, myscale, category, 2020)
    m2019 = choropleth_plot(data2019, myscale, category, 2019)
    
    m2020.save(f'../html/Denver_{category}_choropleth_2020.html')
    m2019.save(f'../html/Denver_{category}_choropleth_2019.html')
