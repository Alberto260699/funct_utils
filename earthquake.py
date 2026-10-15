import gmaps
import gmaps.datasets

#Use google maps api
gmaps.configure(api_key=api_key) #Fill in with your API key

#Get the dataset
earthquake_df=gmaps.datasets.load_dataset_as_df('earthquakes')

#Get the locations from data set
locations=earthquake_df[['latitude','longitude']]
#Get the magnitude from the data
weights=earthquake_df['magnitude']

#Set up your map
fig=gmaps.figure()
fig.add_layer(gmap.heatmap_layer(locations, weights=weights))
fig