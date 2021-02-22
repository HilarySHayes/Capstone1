import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def capitalize_titles(string):
    return ' '.join([x.capitalize() for x in string.split('-')])

class CrimeDataFrame():

    def __init__(self, filename, dt_cols, format, date_col):
        self.df = pd.read_csv(filename)
        self.convert_to_datetime(dt_cols, format)
        self.add_month_day_year(date_col)

    def convert_to_datetime(self, dt_cols, format):
        for col in dt_cols:
            self.df[col] = pd.to_datetime(self.df[col], format = format)

    def add_month_day_year(self, date_col):
        self.df['year'] = self.df[date_col].dt.year
        self.df['month'] = self.df[date_col].dt.month
        self.df['week'] = self.df[date_col].dt.week

    def plot_specific_category_over_time(self, ax, specific_category, offense_category_id, first_offense_date, incident_id):
        cat_df = self.df[self.df[offense_category_id] == specific_category].copy()
        cat_df = cat_df.groupby(['year', 'month']).agg({incident_id: 'count'}).rename(columns={incident_id:'incident_count'}).reset_index()
        
        n =  max(cat_df.year) - min(cat_df.year) + 1
        ax.set_prop_cycle('color',[plt.cm.bone(i) for i in np.linspace(0, 0.8, n)][::-1])
        
        for year in range(min(cat_df.year), max(cat_df.year)+1):  
            tmp = cat_df[cat_df.year==year]
            if year != 2020:
                ax.plot(tmp.month, tmp.incident_count, 'o-', label=f'{year}')
            else:
                ax.plot(tmp.month, tmp.incident_count, 'o-', color='red', label=f'{year}',lw=2)

        ax.set_title(f'Number of {capitalize_titles(specific_category)} Incidents By Month', fontsize=25)
        ax.set_xlabel('Month', fontsize=20)
        ax.set_ylabel('Number of Incidents', fontsize=20)
        ax.set_xticks(range(1,13))
        ax.xaxis.set_tick_params(labelsize=18)
        ax.yaxis.set_tick_params(labelsize=18)
        ax.legend(title='year')

    def plot_all_cats_over_time(self, offense_category_id, first_offense_date, incident_id, city):
        categories = self.df[offense_category_id].unique()
        num_rows = int(np.ceil(len(categories)/2))
        fig, axes = plt.subplots(num_rows, 2, figsize=(24, num_rows*6))
        for category, ax in zip(categories, axes.flatten()):
            self.plot_specific_category_over_time(ax, category, offense_category_id, first_offense_date, incident_id)
        if len(categories) != num_rows * 2:
            axes.flatten()[-1].axis('off')
        fig.suptitle(f'{city} Crime over Time', x=0.5, y=1.01, fontsize=35, fontweight='bold')
        plt.tight_layout()
        fig.savefig(f'../images/{city}_Crime_over_Time.png')     

    def boxplots_by_cat(self, offense_category_id):
        box_df = self.df[self.df.year != 2021].copy()

        categories = box_df[offense_category_id].unique()
        fig, axes = plt.subplots(len(categories), 1, figsize=(12, 3*len(categories)))
        for category, ax in zip(categories, axes.flatten()):
            gtmp = box_df[box_df[offense_category_id] == category].groupby(['year', 'week']).agg({'INCIDENT_ID':'count'}).rename(columns={'INCIDENT_ID': 'num_of_incidents'}).reset_index()
            f = sns.boxplot(x='year', y='num_of_incidents', data=gtmp, boxprops=dict(alpha=0.25), ax=ax)
            f = sns.swarmplot(x='year', y='num_of_incidents', data=gtmp, size=4, ax=ax)
            f.set(xlabel='Year',ylabel='Number of Incidents Per Week')
            f.set_title(f'Distribution of {capitalize_titles(category)} Per Week From 2016 - 2020')
            plt.tight_layout()
            fig.savefig('../images/Denver_Boxswarm_By_Cat.png')

    def kdeplots_by_cat(self, offense_category_id):
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
        fig.savefig('../images/Denver_KDEplots_By_Cat.png')

if __name__ == '__main__':
    Denver = CrimeDataFrame('../data/denver_crime.csv', ['FIRST_OCCURRENCE_DATE', 'LAST_OCCURRENCE_DATE', 'REPORTED_DATE'], "%m/%d/%Y %I:%M:%S %p", 'FIRST_OCCURRENCE_DATE')
    print(Denver.df.info())
    #Denver.plot_all_cats_over_time('OFFENSE_CATEGORY_ID','FIRST_OCCURRENCE_DATE', 'INCIDENT_ID', 'Denver')
    #Denver.boxplots_by_cat('OFFENSE_CATEGORY_ID')
    Denver.kdeplots_by_cat('OFFENSE_CATEGORY_ID')