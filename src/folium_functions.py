import folium
from folium.plugins import MarkerCluster
from crime import capitalize_titles


def crime_marking(x, marker_cluster):
    folium.Circle(location = [x[0], x[1]]).add_to(marker_cluster)

def make_layered_clustered_map(df, center, categories, offense_category_id, geo_lat, geo_lon, city):
    """ Makes an html Folium map with layers for each category 
        Args:
            df: pandas dataframe
            center: [latitude, longitude] for the center of the map
            categories: a list of categories will produce map layer for each category
            offense_category_id: the name of the column that categorizes the offense
            geo_lat: the name of the column with the latitude coordinate
            geo_long: the name of the column with the longitude coordinate
            city: the city 
    """ 
    mapa = folium.Map(center, zoom_start=12)
    for category in categories:
        fg = folium.FeatureGroup(name=capitalize_titles(category), show=False)
        mapa.add_child(fg)
        marker_cluster = folium.plugins.MarkerCluster().add_to(fg)
        loc = df[(df[offense_category_id] == category) & (df.year == 2020)].groupby([geo_lat,geo_lon]).size().reset_index().rename(columns={0:'count'})
        loc[[geo_lat, geo_lon]].apply(lambda x: crime_marking(x, marker_cluster), axis=1)
    folium.TileLayer('openstreetmap').add_to(mapa)
    folium.LayerControl().add_to(mapa)
    mapa.save(f'../html/{city}clustermap.html')

    