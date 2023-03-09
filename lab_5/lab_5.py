from AggDict import AggDict as agg
from AggDict import StateDef as sdef
import os
import requests
import pandas as pd
import plotly.express as plex
import plotly.graph_objects as go
import plotly.io as io

# First, I gathered the relevant functionality from Lab 3 into a
# package called AggDict. The modules from the package are imported
# above. AggDict already includes generic plotting functionality using
# matPlotLib, illustrated below.

# Set working directory
os.chdir("/home/ian/Documents/geocomp_1/lab_5")

# Import the data
url = "https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_050_00_5m.json"

with requests.get(url) as response:
    data = response.json()

counties_props: list = []

for county in data["features"]:
    counties_props.append(county["properties"])

# Define state codes dictionary
state_dict = agg.aggDict(counties_props, "STATE")
state_codes_dict = sdef.stateCodesDict()

print("Complete.")

# Plot of five most frequent county names using AggDict functions from
# Lab 3
county_dict = agg.aggDict(counties_props, "NAME")
print(agg.frequentValues(county_dict, 5))

agg.aggDictPlot(county_dict, "County name")

# Next, I added a new generic pie chart function to AggDict that uses
# Plotly. See AggDict.py for the function definition.

counties_by_state_pie = agg.aggDictPie(state_dict, lambda code: state_codes_dict[code])

# Use graph_objects to modify the graph created by aggDictPie
counties_by_state_pie = go.Figure(counties_by_state_pie)
counties_by_state_pie.update_layout(
    title=go.layout.Title(text="Share of total US counties by state", x=0.5)
)
counties_by_state_pie.show()

# The pie chart above shows that Texas has by far the most counties of
# any US state, accounting for almost 8% of the country's counties.
# Texas is, of course, huge. This raises the question of whether Texas
# has the most counties just because it is a big state or because it
# has more counties than one would expect for its area.

# First, to get a general idea of how the areas of the counties in
# each state are distributed, we can make a factored boxplot showing
# the distribution of the counties by area for each state. Since
# boxplots don't show how many data points they describe, we'll also
# include the number of counties parenthetically in the x-axis labels
# for each state.

# Initiate the lists that will be used for each column of the dataframe
names: list = []
areas: list = []
states: list = []
num_in_state: list = []
state_with_num: list = []

# Fill the lists
for county in counties_props:
    names.append(county["NAME"])
    areas.append(county["CENSUSAREA"])
    states.append(state_codes_dict[county["STATE"]])
    num_in_state.append(len(state_dict[county["STATE"]]))

# Create a dict from which the data frame will be constructed
state_with_num = [f"{name} ({num})" for name, num in zip(states, num_in_state)]

county_areas = {
    "Counties": names,
    "Area": areas,
    "State (number of counties)": state_with_num,
    "State": states,
    "Counties in state": num_in_state,
}

# Construct the dataframe
df_counties = pd.DataFrame(county_areas)
areas_by_state = plex.box(
    df_counties, x="State (number of counties)", y="Area", template="simple_white"
)
areas_by_state.show()

# This plot is a good start, but the two largest counties in Alaska
# are so big that they compress the rest of the states. To deal with
# this, we'll treat Alaska as an outlier and plot the other states.

df_counties_no_AK = df_counties[df_counties.State != "Alaska"]
areas_by_state_no_AK = plex.box(
    df_counties_no_AK, x="State (number of counties)", y="Area", template="simple_white"
)

areas_by_state_no_AK.show()

# This plot is clearer. For one thing, it shows that Western states
# like Nevada, Arizona, and New Mexico tend to have relatively few
# counties and that these counties are usually very large. Other
# states, like Iowa and Mississippi, have a lot of uniformly sized,
# small counties.

# However, it's not so clear what this plot tells us about Texas.
# Texas has a lot of outliers, which suggests that it has a fairly
# wide range of county sizes. To some extent, the plot suggests that
# Texas is in its own class, as most other states with a high number
# of counties have only small counties.

# However, we can get a clearer picture of these relationships with a
# scatterplot. Let's make a scatterplot of number of each state's
# total area vs. its number of counties.

state_scatter_data: dict = {}
state_areas: list = []
state_names: list = []
county_nums: list = []
mean_county_size: list = []

for state_code in state_dict:
    state_area = 0
    for county in state_dict[state_code]:
        state_area += county["CENSUSAREA"]
    state_areas.append(state_area)
    state_names.append(state_codes_dict[state_code])
    county_nums.append(len(state_dict[state_code]))

mean_county_size = [round(area / n, 2) for area, n in zip(state_areas, county_nums)]

state_scatter_data = {
    "State": state_names,
    "Area": state_areas,
    "Counties": county_nums,
    "Mean county size": mean_county_size,
}

df = pd.DataFrame(state_scatter_data)

# We'll use a lowess smoother since the data does not have a clear
# linear pattern.
state_scatter = plex.scatter(
    df,
    x="Area",
    y="Counties",
    hover_name="State",
    size="Mean county size",
    template="simple_white",
    trendline="lowess",
    trendline_options=dict(frac=0.8),
)

state_scatter.show()

# This plot is promising, Alaska is such an outlier again. Noting
# that Alaska is an extremely large state with very few counties,
# let's exclude it from the analysis and re-create the graph.

df = df[df.State != "Alaska"]

state_scatter_no_AK = plex.scatter(
    df,
    x="Area",
    y="Counties",
    hover_name="State",
    size="Mean county size",
    template="simple_white",
    trendline="lowess",
    trendline_options=dict(frac=0.8),
)

# We can use Plotly graph_objects to make the plot easier to read.
state_scatter_no_AK = go.Figure(state_scatter_no_AK)

state_scatter_no_AK.update_layout(
    title=go.layout.Title(
        text="Number of counties by state area (excluding Alaska)",
        x=0.5,
        font=dict(size=28),
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(text="Number of counties", font=dict(size=22))
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            # HTML can be used within the string because plotly passes
            # the string as HTML; this produces a caption below the x title
            text="Area of state (sq mi)<br><br><sup>Dot sizes indicate average county size for each state. State areas calculated as sum of county areas.<sup>",
            font=dict(size=22),
        )
    ),
)

state_scatter_no_AK.write_image("output/state_scatter_no_AK.png")
state_scatter_no_AK.write_html("output/state_scatter_no_AK.html")
state_scatter_no_AK.show()

# This plot shows more clearly that Texas is in a class
# of its own when it comes to county size and number. Other than Texas
# and Alaska, there are basically three groups: states with just a few small
# counties; states with many small counties; and states with a few
# very large counties (Alaska is an extreme version of this latter
# group). Texas is uniqu in that it has a very high number of
# counties, and these counties are moderately sized--smaller than
# average for a big state, but larger than average for a state with
# many counties.


