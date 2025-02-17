import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches

# ---------------------------------------------------------------------------------------------------------------------
# in this section, write the script to load the data and complete the main part of the analysis.
# try to print the results to the screen using the format method demonstrated in the workbook

# load the necessary data here and transform to a UTM projection
# Load the counties and ward data
wards = gpd.read_file('data_files/NI_Wards.shp')
counties = gpd.read_file('data_files/Counties.shp')

# Transform the CRS to EPSG 2157 for both wards and counties
wards = wards.to_crs(epsg=2157)
counties = counties.to_crs(epsg=2157)

# check if CRS is the same
print(counties.crs == wards.crs)

# Using a spatial join, summarize the total population by county. What county has the highest population? What about the lowest?
join = gpd.sjoin(counties, wards, how='inner', lsuffix='left', rsuffix='right') # perform the spatial join

# Summarise the total population by county
pop_by_county = join.groupby('CountyName')['Population'].sum()

# Find the counties with the highest and lowest population
max_pop_county = pop_by_county.idxmax()
min_pop_county = pop_by_county.idxmin()

# Print the total population by county and the counties with the highest and lowest population
print("Total Population by County:")
print(pop_by_county)
print("County with the Highest Population:", max_pop_county)
print("County with the Lowest Population:", min_pop_county)

# ADDITIONAL EXERCISE QUESTION NO.2
# Summarise the total population by ward
pop_by_ward = join.groupby('Ward')['Population'].sum()

# Find the wards with the highest and lowest population
max_pop_ward = pop_by_ward.idxmax()
min_pop_ward = pop_by_ward.idxmin()

# Print obtained values
print("Total Population by Ward:")
print(pop_by_ward)
print("Ward with the Highest Population:", max_pop_ward)
print("Ward with the Lowest Population:", min_pop_ward)
# ---------------------------------------------------------------------------------------------------------------------
# below here, you may need to modify the script somewhat to create your map.
# create a crs using ccrs.UTM() that corresponds to our CRS
myCRS = ccrs.UTM(29)
# create a figure of size 10x10 (representing the page size in inches
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=myCRS))

# add gridlines below
gridlines = ax.gridlines(draw_labels=True,
                         xlocs=[-8, -7.5, -7, -6.5, -6, -5.5],
                         ylocs=[54, 54.5, 55, 55.5])
gridlines.right_labels = False
gridlines.bottom_labels = False

# to make a nice colorbar that stays in line with our map, use these lines:
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

# plot the ward data into our axis, using
ward_plot = wards.plot(column='Population', ax=ax, vmin=1000, vmax=8000, cmap='viridis',
                       legend=True, cax=cax, legend_kwds={'label': 'Resident Population per Ward'})

county_outlines = ShapelyFeature(counties['geometry'], myCRS, edgecolor='r', facecolor='none')

ax.add_feature(county_outlines)
county_handles = [mpatches.Rectangle((0, 0), 1, 1, facecolor='none', edgecolor='r')]

ax.legend(county_handles, ['County Boundaries'], fontsize=12, loc='upper left', framealpha=1)

# save the figure
fig.savefig('sample_map.png', dpi=300, bbox_inches='tight')
plt.show()