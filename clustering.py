# we are going to do now a clustering of the data base on the statistics of the pokemons
# we will use the KMeans algorithm from sklearn
#
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from utils import exec_query
from queries import QUERY_ALL_POKEMON
from sklearn.decomposition import PCA
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


N_MAX_CLUSTERS = 50
n_choosed_clusters = 3
random_state = 42
cols = ['hp', 'atk', 'def', 'spa', 'spd', 'spe']

def get_stats_list_by_number():
    records, summary, keys = exec_query(QUERY_ALL_POKEMON, {})
    stats = []
    names = []
    for record in records:
        stats.append([record['p']['hp'], record['p']['atk'], record['p']['def'], record['p']['spa'], record['p']['spd'], record['p']['spe']])
        names.append(record['p']['name'])
    return stats, names

def elbow_method():
    inertia = []
    for i in range(1, N_MAX_CLUSTERS): 
        model = KMeans(n_clusters=i, random_state=random_state)
        model.fit(X)
        inertia.append(model.inertia_)
    
    plt.plot(range(1, N_MAX_CLUSTERS), inertia)
    plt.title('Elbow method')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.show()


X, names = get_stats_list_by_number()

# We will use the StandardScaler to scale the data
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Elbow method to choose the number of clusters
elbow_method()

# Kmeans with the number of clusters choosed
model = KMeans(n_clusters=n_choosed_clusters, init='k-means++', random_state=random_state)
model.fit(X)

# Visualize the clusters
X = pd.DataFrame(X, columns=cols)
X['Clusters'] = model.labels_

centroides = pd.DataFrame(scaler.inverse_transform(model.cluster_centers_))
centroides.columns = cols
centroides["Clusters"] = range(n_choosed_clusters)

sns.pairplot(X, hue="Clusters", palette="bright")
plt.show()

clustered_pokemons = X.groupby(["Clusters"])
centroides.astype(int)

# Radar chart splited by cluster
rows = 3
columns = n_choosed_clusters // 2

fig = make_subplots(
    rows=rows,
    cols=columns,
    specs=[
        [{"type": "polar"} for i in range(columns)] for j in range(rows)
    ],
    subplot_titles=[f"Cluster {i}" for i in range(n_choosed_clusters)],
)
for i in range(rows):
    for j in range(columns):
        if i * columns + j >= n_choosed_clusters:
            break
        fig.add_trace(
            go.Scatterpolar(
                r=centroides.iloc[i].values,
                theta=cols,
                fill="toself",
                name=f"Cluster {i}",
            ),
            row=i + 1,
            col=j + 1
        )
        
fig.update_polars(
    radialaxis=dict(visible=True, range=[0, 150]),
    angularaxis=dict(showline=True, showticklabels=True),
)

fig.show()


# Radar chart with all clusters in the same plot
fig = go.Figure()

for i in range(rows):
    fig.add_trace(
        go.Scatterpolar(
            r=centroides.iloc[i].values,
            theta=cols,
            fill="toself",
            name=f"Cluster {i}",
        ),
    )
        
fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 150]),
        angularaxis=dict(showline=True, showticklabels=True),
    )
)

fig.show()

# which pokemons are in each cluster
for cluster, pokemons in clustered_pokemons:
    print(f"Cluster {cluster}")
    for i in pokemons.index:
        print(names[i], end=", ")
    print()