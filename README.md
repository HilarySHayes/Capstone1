# Denver Crime Trends

# Background & Motivation

In the last year we have seen a dramatic impact on how people live due to COVID-19. In this report, I explore crime data for the City of Denver to understand how and where crime has changed this last year.  Some types of crime have have decreased, such as the number of traffic accidents,  while other crimes, like automobile theft, have seen a dramatic increase.  Traffic accidents decreased the most in the neighborhood around the Denver International Airport, an area that saw a staggering decrease in traffic this last year.  Part of optimally allocating resources is understanding 
the distribution of crimes, where they are occuring and being able to adapt to changes that are happening.  This report is a first step toward looking at a few of the largest shifts that have happened this year.

# Data

I obtained the last five years of criminal offenses in the City and County of Denver, Colorado, which is based on the National Incident Based Reporting Systems (NIBRS) and is publically available online [here](https://www.denvergov.org/opendata/dataset/city-and-county-of-denver-crime).
 The data includes more than 451,400 reported crimes from 2016-2020. Each crime is classified by offense type, and includes the date of occurence as well as the reporting date. Most reported crimes also include the neighborhood and geographical location coordinates. In accordance with legal protections against identifying sexual assault victims, addresses are not included. Child abuse cases and all crimes involving juveniles are not also reported in this dataset. In August 2020, the Stapleton neighborhood changed its name to Central Park; The new name, Central Park, was replaced in all previous years for consistency. 

# Exploratory Data Analysis

One of my first goals after preparing the dataframe was to assess if crime in Denver had changed in 2020. To examine this question, I plotted the number of incidents for each of the major crime categories in the dataset by year. Looking at the figure below, there is a considerable decline in traffic accidents and drug/alcohol incidents in 2020. There also is an increase in theft from motor vehicles and auto theft in 2020.

<p align="center">
<img src="./images/Denver/DenverCrimeByCategoryBarplot.png" width="700">
</p>

To further investigate the changes in auto theft, I plotted the total number of incidents by year, and for each month over time.  The red line represents the year 2020 and there is a considerable increase in auto theft incidents that starts around March, when the severity of COVID-19 was just being realized in the US.  The box plot on the right shows just how much this has increased compared to other years.

<p align="center">
<img src="./images/Denver/Denver_auto-theft_Over_Time.png" width="800">
</p>

The number of traffic accidents decreased last year.  In the figure below, we can observe a sharp drop as Covid measures were enacted and more people were staying home. Over time the number of accidents increased but it remained well below its previous levels. More people working from home is likely contributing to this change.  The far-right box plot shows the extent of this change when compared with other years.

<p align="center">
<img src="./images/Denver/Denver_traffic-accident_Over_Time.png" width="800">
</p>

Reviewing theft from motor vehicles we also see an upward trend over 2020. In this instance, there has been a upward trend that appears to level off during 2019, before increasing significantly again in 2020.  March and April appear to be the point at where the increase begins.  Like the other two figures, the box-plot on the right shows the distribution over the year for all 5 years and highlights the notable difference in 2020. 

<p align="center">
<img src="./images/Denver/Denver_theft-from-motor-vehicle_Over_Time.png" width="800">
</p>

While the number of aggravated assaults seem to be trending upward over the last few years, there is a cyclical pattern with more incidents occuring in the summer. 

<p align="center">
<img src="./images/Denver/Denver_aggravated-assault_Over_Time.png" width="800">
</p>

## Where do most crimes occur?

Grouping by neighborhood, we can see the top 15 neighborhoods where crimes occur. Central Park, was formerly known as Stapleton and, as previously mentioned, for the purposed of the analysis it was renamed for all years. 

<p align="center">
<img src="./images/Denver/DenverTopNCrimeNeighborhoods.png" width="500">
</p>

In order to be able to drill down for a close up on crime in Denver neighborhoods, I made a folium map with different crime categories as layers.  The map includes only crimes from 2020.  Due to the large number of incidents I used clusters to allow for easier viewing. Below is a gif of the map. An html file containing the map is located in the html folder of this repo and can be downloaded and run from your local machine. There are 622 incidents from 2020 in the dataset that are not represented geographically on the map. All but one are sexual crimes for which location data is withheld.

<p align="center">
<img src="./images/Denver/Map_Demos.gif" width="500">
</p>

In order to be able to see changes in time across neighborhoods for specific categories, I made a function that creates a folium choropleth.  Below you can see the difference neighborhood by neighborhood for auto-theft incidents in 2019 and in 2020. While these static maps offer an insight into the changes 

<p align="center">
<img src="./images/Denver/auto-theft2019.png" width="400">
<img src="./images/Denver/auto-theft2020.png" width="400">
</p>

# Future directions

Are similar changes exhibited in other cities?  Expand the EDA to other cities to compare different trends.
