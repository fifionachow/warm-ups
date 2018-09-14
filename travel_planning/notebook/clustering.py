import random

from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering, MeanShift, estimate_bandwidth

from color_maps import colors

def create_color_stops(df, field_property):
    unique_values = df[field_property].unique()
    return [[unique_values[e], c[1].hex_format()] for e, c in enumerate(random.sample(colors.items(), len(unique_values)))]
