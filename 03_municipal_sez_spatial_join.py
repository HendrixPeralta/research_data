# %%
import numpy as np
import pandas as pd
import geopandas as gpd
from geopandas import points_from_xy
import matplotlib as plt
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap
import plotly.express as px

# %%
# Reads all the shp map and the aggregated sez data 

hoods = gpd.read_file("/Users/hendrixperalta/Desktop/Research Data Manipulation/research_data/adm2/map_files/adm2_shp.shp")

sez = pd.read_csv("sez_aggregated.csv")
sez = sez[sez['latitude'] != 0]

sez.info()

# %%
sez

# %%
sample_sez.dtypes.head(10)

# %%
sample_sez = sez.sample(frac=1)
sample_sez["close"] = sample_sez['close'].replace(0, 2019)
sample_sez['start'] = pd.to_datetime(sample_sez['start'].astype(int).astype(str), format='%Y')
sample_sez['close'] = pd.to_datetime(sample_sez['close'].astype(int).astype(str), format='%Y')
sample_sez

# %%

fig = px.timeline(sample_sez, x_start="start", x_end="close", y="name")
fig.update_yaxes(autorange="reversed")
fig.xlim()
fig.show()


# %%
# Creates a variable len, this variable keep track of the length of operation of the sez 

year_list = list(range(2000, 2017))

for year in year_list:
    conditions = (sez["ent"+str(year)])
    # Calculate operation years only if conditions are met
    sez["len" + str(year)] = np.where(conditions, year - sez['start'], 0)

# Export DataFrame to CSV
#joined.to_csv("joined.csv", index=False)

# %%
# Shows the position of the sez 

sez.plot(
    kind='scatter', x="longitude", y="latitude"
)


# %%
# Converts the sez points using the coordinate references in the shp map 

hoods.crs

sez_gdf = gpd.GeoDataFrame(
    sez, crs = hoods.crs,
    geometry = points_from_xy(
        sez["longitude"], sez["latitude"]
    )
)

sez_gdf.head()

# %%
#sez_gdf.to_csv("sez_gdf.csv")

# Shows the  location of the sez in a 2d map 

sez_gdf.explore(
    titles = "CartoDB positron",
    cmap = "plasma", 
    style_kwds=dict(color = "black")
)

# %%
# Spatial joins the sez data into their respective municipality 

#%%timeit
joined = gpd.sjoin(
    sez_gdf,
    hoods,
    how="right",
    predicate="within"
)

# %%
# Creates the aggregation/reduction function

joined.fillna(0, inplace = True)
joined["id"] = pd.to_numeric(joined["id"], errors = "coerce")

agg_func = {col: "sum" for col in joined.columns}
del agg_func['geometry']
mean_columns = joined.columns[joined.columns.str.contains('sal|id|len', regex=True)]
for col in mean_columns:
    if col in agg_func:
        agg_func[col] = "mean"

# %%
types = joined[joined.columns[joined.columns.str.contains('sal|id|len')]].dtypes
#types.to_csv("types.csv")

# %%
# Reduces the variables for each municipalities using the agg_func

res_dissolve = joined.dissolve(by="id", aggfunc=agg_func)
#res_dissolve

# %%
import matplotlib.pyplot as plt

cmap = LinearSegmentedColormap.from_list("custom_blue_red", ["blue", "red"])
fig, ax = plt.subplots(figsize=(20, 8))
joined.plot(ax=ax, color="lightgrey", alpha=0.5)           
joined.plot(ax=ax, alpha=0.5, markersize=2, column="ent2015", 
            legend=True, vmin=1, vmax=30)
plt.title("Pickups Colored by Neighborhood", fontsize=20);


# %%
joined.drop(columns = 'geometry').to_csv("joined.csv")

# %%
res_nogeo = res_dissolve.drop(columns = "geometry")
res_nogeo.to_csv("joined_sez_map.csv")

# %%


# %%



