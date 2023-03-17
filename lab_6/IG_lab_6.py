import geopandas as gp
import requests
import matplotlib.pyplot as plt

# First, I developed a tool to take URLs corrresponding to NYC Open
# Data's API and return a geopackage with each dataset as a layer.


def json_response(url, limit=500000):
    # Limit will determine how many rows are read
    my_params = {"$limit": limit}
    with requests.get(url, params=my_params) as response:
        return response.json()


def gdf_from_url(url, limit=500000):
    response = json_response(url, limit)
    gdf = gp.GeoDataFrame.from_features(response)
    return gdf


def gdf_dict(url_dict, max_size=500000):
    ans = {}
    for key in url_dict:
        ans[key] = gdf_from_url(url_dict[key], max_size)
    return ans


def gdf_dict_to_gpkg(gdf_dict, path, max_size=500000):
    for key in gdf_dict:
        gdf_dict[key].to_file(path, layer=key, driver="GPKG")


def urls_to_gpkg(url_dict, path, max_size=500000):
    my_gdf_dict = gdf_dict(url_dict, max_size)
    gdf_dict_to_gpkg(my_gdf_dict, path)
    return my_gdf_dict

my_urls = {
    "vision_zero": "https://data.cityofnewyork.us/resource/h9gi-nx95.geojson",
    "bike_routes": "https://data.cityofnewyork.us/resource/s5uu-3ajy.geojson",
    "street_centerline": "https://data.cityofnewyork.us/resource/8rma-cm9c.geojson",
    "bikes_in_buildings": "https://data.cityofnewyork.us/resource/scjj-6yaf.geojson",
    "priority_bike_districts": "https://data.cityofnewyork.us/resource/h6b2-3v9f.geojson",
    "census": "https://data.cityofnewyork.us/resource/63ge-mke6.geojson",
}

my_gdf_dict = urls_to_gpkg(my_urls, "my_bike_map.gpkg")

# This geopackage can be opened in QGIS, and the datasets
# corresponding to the API requests will automatically be imported as
# layers. 

# We can also use some of the functions defined above to explore what
# kind of data a GeoDataFrame contains.

# First, we can make a dict of GeoDataFrames that corresponds to the
# layer names and URLs above.
print(my_gdf_dict['census'])

# We can see that the census GeoDataFrame contains multipolygons
# associated with 13 other columns of data.

# But is this the only type of geometry in the data frame? We can
# check this with the following function.

# Return a list of all the unique geometry types in a GeoDataFrame.
def gdf_geo_types(gdf):
    return {geom.geom_type for geom in gdf.geometry}


# We can see that the census GeoDataFrame only contains MultiPolygons.
print(gdf_geo_types(my_gdf_dict['census']))

# Meanwhile, the bike routes GeoDataFrame only contains
# MultiLineStrings.

print(gdf_geo_types(my_gdf_dict['bike_routes']))

# Next, I made a function for quickly plotting some layers from a
# GeoDataFrame.

# The idea is to provide a quick verification that the data looks
# right rather than a finished map product.
def quickplot_gdf_dict(gdfs: dict, to_plot: list, colors: list):
    """Plots the GeoDataFrames within gdfs that are named in to_plot."""

    fig, ax = plt.subplots()
    ax.set_aspect("equal")

    i = 0
    
    # Plot each GeoDataFrame, cycling through the colors.
    # Colors are reused if there are more GeoDataFrames than colors.
    for key in to_plot:
        gdfs[key].plot(ax=ax, color=colors[i % len(colors)], edgecolor='black', linewidth=.4)

        # Reuse colors if there are more layers than colors
        i += 1

# Here, we'll make a plot using the census data, priority bike
# districts, and bike route.

# Note that the order of to_plot corresponds to the plot's drawing
# order, so we want the lower layers first.
my_colors = ["#e6e6e6", "#fcecc0", "#3b3b3b", "#e80c0c"]
to_plot = ["census", "priority_bike_districts", "street_centerline", "bike_routes"]

plt.close()
quickplot_gdf_dict(my_gdf_dict, to_plot, my_colors)

plt.show()
plt.savefig('my_quick_bike_plot.png', format='png')
