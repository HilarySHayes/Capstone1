import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium_functions

def capitalize_titles(string):
    return ' '.join([x.capitalize() for x in string.split('-')])

class CrimeDataFrame():

    def __init__(self, filename, dt_cols, format, date_col):
        self.df = pd.read_csv(filename)
        self.convert_to_datetime(dt_cols, format)
        self.add_month_week_year(date_col)

    def convert_to_datetime(self, dt_cols, format):
        for col in dt_cols:
            self.df[col] = pd.to_datetime(self.df[col], format = format)

    def add_month_week_year(self, date_col):
        self.df['year'] = self.df[date_col].dt.year
        self.df['month'] = self.df[date_col].dt.month
        self.df['week'] = self.df[date_col].dt.week

    def barplot_city_crime_by_category(self, offense_category_id, incident_id, city, palette):
        """ Barplot of # of incidents by category by yeear
            Args:
                offense_category_id: the name of the column that categorizes the offense
                incident_id: the name of the column where the incident identifier is 
                city: the name of the city
                palette: seaborn color palette for plot
        """
        fig, ax = plt.subplots(figsize=(18,10))
        sns.set_palette(palette)
        cat_by_year = self.df.groupby(['year', offense_category_id]).agg({incident_id:'count'}).reset_index()
        ax = sns.barplot(x=offense_category_id, y=incident_id, hue='year', data=cat_by_year[cat_by_year.year!=2021].sort_values(incident_id, ascending=False), saturation=0.7, alpha=0.9, edgecolor='black')
        ax.set_yticklabels([int(x) for x in ax.get_yticks()], size=20)
        plt.ylabel('# of Occurences Per Year', size=22)
        plt.xlabel('')
        plt.setp(ax.patches, linewidth=1)
        plt.title(f'{city} Crime By Category', fontsize=30)
        plt.xticks(rotation = 30, ha='right', fontsize=18)
        plt.tight_layout()
        plt.legend(fontsize='xx-large')
        fig.savefig(f'../images/{city}/{city}CrimeByCategoryBarplot.png')

    def plot_specific_category_over_time(self, ax, specific_category, offense_category_id, first_offense_date, incident_id):
        """ Lineplot of # of incidents per month over time for specified category
            Args:
                ax: axis object
                specific_category: the name of the specific offense category you are plotting over time
                offense_category_id: the name of the column that categorizes the offense
                first_offense_date: the name of the column where the date of first offense is
                incident_id: the name of the column where the incident identifier is 
        """
        cat_df = self.df[self.df[offense_category_id] == specific_category].copy()
        cat_df = cat_df[cat_df.year != 2021]
        cat_df = cat_df.groupby(['year', 'month']).agg({incident_id: 'count'}).rename(columns={incident_id:'incident_count'}).reset_index()
        
        n =  max(cat_df.year) - min(cat_df.year) + 1
        ax.set_prop_cycle('color',[plt.cm.bone(i) for i in np.linspace(0, 0.8, n)][::-1])
        
        for year in range(min(cat_df.year), max(cat_df.year)+1):  
            tmp = cat_df[cat_df.year==year]
            if year != 2020:
                ax.plot(tmp.month, tmp.incident_count, 'o-', label=f'{year}')
            else:
                ax.plot(tmp.month, tmp.incident_count, 'o-', color='red', label=f'{year}',lw=2)

        ax.set_title(f'Number of {capitalize_titles(specific_category)} Incidents By Month', fontsize=18)
        ax.set_xlabel('Month', fontsize=18)
        ax.set_ylabel('Number of Incidents', fontsize=18)
        ax.set_xticks(range(1,13))
        ax.xaxis.set_tick_params(labelsize=18)
        ax.yaxis.set_tick_params(labelsize=18)
        ax.legend(title='year')

    def plot_all_cats_over_time(self, offense_category_id, first_offense_date, incident_id, city):
        """ Lineplots of # of incidents per month over time by category
            Args:
                offense_category_id: the name of the column that categorizes the offense
                first_offense_date: the name of the column where the date of first offense is
                incident_id: the name of the column where the incident identifier is 
                city: the name of the city
        """
        categories = self.df[offense_category_id].unique()
        num_rows = int(np.ceil(len(categories)/2))
        fig, axes = plt.subplots(num_rows, 2, figsize=(18, num_rows*8))
        for category, ax in zip(categories, axes.flatten()):
            self.plot_specific_category_over_time(ax, category, offense_category_id, first_offense_date, incident_id)
        if len(categories) != num_rows * 2:
            axes.flatten()[-1].axis('off')
        fig.suptitle(f'{city} Crime over Time', x=0.5, y=1.01, fontsize=35, fontweight='bold')
        plt.tight_layout()
        fig.savefig(f'../images/{city}/{city}_Crime_over_Time.png', bbox_inches='tight')     

    def boxplots_by_cat(self, offense_category_id, city):
        """ Plots a swarmplot overlaying boxplot showing the distribution across time for each unique category 
            in the columns passed as offense_category_id
            Args:
                offense_category_id: the name of the column that categorizes the offense
                city: the name of the city
        """
        box_df = self.df[self.df.year != 2021].copy()
        categories = box_df[offense_category_id].unique()
        fig, axes = plt.subplots(len(categories), 1, figsize=(12, 4*len(categories)))
        for category, ax in zip(categories, axes.flatten()):
            gtmp = box_df[box_df[offense_category_id] == category].groupby(['year', 'week']).agg({'INCIDENT_ID':'count'}).rename(columns={'INCIDENT_ID': 'num_of_incidents'}).reset_index()
            f = sns.boxplot(x='year', y='num_of_incidents', data=gtmp, boxprops=dict(alpha=0.25), ax=ax)
            f = sns.swarmplot(x='year', y='num_of_incidents', data=gtmp, size=4, ax=ax)
            f.set(xlabel='Year',ylabel='Number of Incidents Per Week')
            f.set_title(f'Distribution of {capitalize_titles(category)} Per Week From {min(box_df.year)} - {max(box_df.year)}')
            plt.tight_layout()
            fig.savefig(f'../images/{city}/{city}_Boxswarm_By_Cat.png')

    def kdeplots_by_cat(self, offense_category_id, city):
        """ On the same graph, for each year, a kernel density estimate plot of the distribution of the number incidents for a category is plotted. 
            One such graph is generated for each unique category in the offense_category_id column.
            Args:
                offense_category_id: the name of the column that categorizes the offense
                city: the name of the city
        """
        df = self.df[self.df.year != 2021].copy()
        palette = sns.color_palette("rocket_r", as_cmap=True)
        categories = df[offense_category_id].unique()
        fig, axes = plt.subplots(len(categories), 1, figsize=(12, 3*len(categories)))
        for category, ax in zip(categories, axes.flatten()):
            gtmp = df[df[offense_category_id] == category].groupby(['year', 'week']).agg({'INCIDENT_ID':'count'}).rename(columns={'INCIDENT_ID': 'num_of_incidents'}).reset_index()
            g = sns.kdeplot(data=gtmp, x='num_of_incidents', hue='year', fill=True, palette=palette, ax=ax)
            g.set_title(f'KDE of the Number of {capitalize_titles(category)} Per Week')
            g.set_xlabel(f'Number of {capitalize_titles(category)} Per Week')
        plt.tight_layout()
        fig.savefig(f'../images/{city}/{city}_KDEplots_By_Cat.png')

    def top_crime_neighborhoods(self, n, neighborhood_id, city):
        """ A barchart of the top n neighborhoods ranked by highest crime counts
            Args:
                n: the number of neighborhoods to include in plot
                neighborhood_id: the name of the column identifying the neighborhood
                city: the name of the city
        """
        fig, ax = plt.subplots(figsize=(9, max(n//3, 1)))
        tmp = self.df[(self.df.year != 2021) & (self.df[neighborhood_id] != 'cbd')]
        neighborhood = tmp.groupby(neighborhood_id).size().sort_values(ascending=False).reset_index()
        neighborhood.rename(columns={neighborhood_id:'Neighborhood', 0:'Count'}, inplace=True)
        top_n = neighborhood[:n]
        g = sns.barplot(x='Count', y='Neighborhood', data=top_n, palette='mako', edgecolor='black')
        g.axes.set_title(f"Neighborhoods in {city} with Most Crime From {min(tmp.year)}-{max(tmp.year)}",fontsize=16)
        g.set_xlabel("Number of Crime Occurrences",fontsize=12)
        g.set_ylabel("")
        g.set_yticklabels([capitalize_titles(y.get_text()) for y in g.get_yticklabels()])
        g.tick_params(labelsize=11)
        plt.tight_layout()
        fig.savefig(f'../images/{city}/{city}TopNCrimeNeighborhoods.png')


if __name__ == '__main__':

    """ Creates class with Denver dataset attribute
        Makes numerous plots
        Makes folium cluster map By category for crime in Denver for 2020 
        Left for ease of generating graphics
    """
    Denver = CrimeDataFrame('../data/denver_crime.csv', ['FIRST_OCCURRENCE_DATE', 'LAST_OCCURRENCE_DATE', 'REPORTED_DATE'], "%m/%d/%Y %I:%M:%S %p", 'FIRST_OCCURRENCE_DATE')
    print(Denver.df.info())
    #Denver.plot_all_cats_over_time('OFFENSE_CATEGORY_ID','FIRST_OCCURRENCE_DATE', 'INCIDENT_ID', 'Denver')
    #Denver.barplot_city_crime_by_category('OFFENSE_CATEGORY_ID', 'INCIDENT_ID', 'Denver', ["#1D3557","#457B9D","#A8DADC","#F3C6C6","#E63946"])    
    #Denver.boxplots_by_cat('OFFENSE_CATEGORY_ID', 'Denver')
    #Denver.kdeplots_by_cat('OFFENSE_CATEGORY_ID', 'Denver')
    Denver.top_crime_neighborhoods(15, 'NEIGHBORHOOD_ID', 'Denver')
    
    #categories = sorted(Denver.df.OFFENSE_CATEGORY_ID.unique())
    #categories.remove('sexual-assault')
    #folium_functions.make_layered_clustered_map(Denver.df, [39.7177, -104.9208], categories, 'OFFENSE_CATEGORY_ID', 'GEO_LAT', 'GEO_LON', 'Denver')
    
    
    """ Creates class with Seattle dataset attribute
        Makes top 10 crime neighborhoods plot
        Makes folium cluster map by category for crime in Seattle for 2020 
    """
    #Seattle = CrimeDataFrame('../data/Seattle_crime.csv', ['Offense Start DateTime'], '%m/%d/%Y %I:%M:%S %p', 'Offense Start DateTime')
    
    #Seattle.top_crime_neighborhoods(10, 'MCPP', 'Seattle')

    #tmp = Seattle.df[Seattle.df.year == 2020][['Latitude','Longitude','Offense Parent Group']].dropna(axis=0)
    #categories = sorted(tmp['Offense Parent Group'].unique())
    #folium_functions.make_layered_clustered_map(Seattle.df, [47.608013, -122.335167], categories, 'Offense Parent Group', 'Latitude', 'Longitude', 'Seattle')
    