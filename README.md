# Capstone1

# Background & Motivation

Optimally allocating respources to make the biggest dent in crime we need to start by examining how crime as changed.  

# Data

The dataset includes the last five years of criminal offenses in the City and County of Denver, Colorado. Based on the National Incident Based Reporting System, the dataset is available publically online [here](https://www.denvergov.org/opendata/dataset/city-and-county-of-denver-crime). The data includes more than 451,400 reported crimes from 2016-2020. Each crime is classified by offense type, includes the date of occurence, and reporting date. Most reported crimes also include the neighborhood and geographical location coordinates. In accordance with legal protections against identifying sexual assault victims, addresses are not included. Child abuse cases and all crimes involving juveniles are not reported in this dataset at all. It should be noted that in August 2020, Stapleton changed its name to Central Park. The name change was adjusted for all years for consistency. 

# Exploratory Data Analysis

One of my first goals after preparing the dataframe was to assess if crime in Denver had changed in 2020. To examine this question, I plotted number of incidents for each of the major crime categories in the dataset by year. There appears to be a considerable decline in traffic accidents and drug/alcohol incidents in 2020. There also is an increase in theft from motor vehicles and auto theft in 2020.


![Barplot of Crime in Denver By Crime Category](./images/Denver/DenverCrimeByCategoryBarplot.png)

To further investigate the changes in auto theft, I plotted the total number of incidents each month over time.  We can see the number of auto theft incidents per month increase steadily across the year.  

![Distribution of Auto Theft in Denver Over Time](./images/Denver/Denver_auto-theft_Over_Time.png)

Looking at the total number of traffic accidents over time there is a sharp drop as Covid measures were enacted. Over time the number of accidents increased but did not ever reach the previous levels. More people working from home is likely contributing to this change.

![Distribution of Traffic Accidents in Denver Over Time](./images/Denver/Denver_traffic-accident_Over_Time.png)

Reviewing theft from motor vehicles we also see an upward trend over 2020. 

![Distribution of Theft From Motor Vehicles in Denver Over Time](./images/Denver/Denver_theft-from-motor-vehicle_Over_Time.png)

While the number of aggravated assaults seem to be trending upward over the years there is an interesting cyclical component with more incidents occuring in the summer in general with a dip sometimes in August.

![Distribution of Aggravated Assault in Denver Over Time](./images/Denver/Denver_aggravated-assault_Over_Time.png)

## Where do most crimes occur?

Grouping by neighborhood, we can see the top 15 neighborhoods where crimes occur. Central Park, was formerly known as Stapleton. For the purposed of the analysis it was renamed for all years. 

![Denver Neighborhoods Ranked by Crime Counts](./images/Denver/DenverTopNCrimeNeighborhoods.png)

In order to be able to drill down for a close up on crime in Denver neighborhoods, I made a folium map with different crime categories as layers.  The map includes only crimes from 2020.  Due to the large number of incidents I used clusters to allow for easier viewing. Below is a gif of the map. An html file containing the map is located in the html folder of this repo and can be downloaded and run from your local machine. There are 622 incidents from 2020 in the dataset that are not represented geographically on the map. All but one are sexual crimes for which location data is withheld.

![Gif of a layered folium map of Denver for crime in 2020](./images/Denver/Map_Demos.gif)


# Future directions

I