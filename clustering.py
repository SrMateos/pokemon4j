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

def get_stats_list_by_number():
    records, summary, keys = exec_query(QUERY_ALL_POKEMON, {})
    stats = []
    for record in records:
        stats.append([record['p']['hp'], record['p']['atk'], record['p']['def'], record['p']['spa'], record['p']['spd'], record['p']['spe']])
    return stats


# trasnform the data into a df to see the correlation between the features
def correlation_matrix(X):
    X = np.array(X)
    X = X.astype(float)
    X = pd.DataFrame(X, columns=cols)
    sns.heatmap(X.corr(),cmap="YlGnBu", annot=True)
    plt.title("Feature Correlation Map")
    plt.show()

def elbow_method():
    # Create a KMeans model
    score = []
    for i in range(4, 100): 
        model = KMeans(n_clusters=i, random_state=42)
        model.fit(X)
        score.append(model.inertia_)
    
    plt.plot(range(4, 100), score)
    plt.title('Elbow method')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    n = 33
    plt.annotate(f"Number of clusters = {n}", xy=(n, score[n]), xytext=(n-3, score[n]*0.8), arrowprops=dict(arrowstyle="->"))
    plt.show()


cols = ['hp', 'atk', 'def', 'spa', 'spd', 'spe']

# We will scale the data
X = get_stats_list_by_number()

correlation_matrix(X)

scaler = StandardScaler()
X = scaler.fit_transform(X)

elbow_method()

model = KMeans(n_clusters=33, random_state=42)
model.fit(X)

# transform the data into a df
X = pd.DataFrame(X, columns=cols)
X['Clusters'] = model.labels_

Centroids = pd.DataFrame(scaler.inverse_transform(model.cluster_centers_))
Centroids.columns = cols
Centroids["Clusters"] = range(33)

sns.pairplot(X, hue="Clusters", palette="viridis")
plt.show()


# Apply PCA to reduce the dimensionality of the data
# pca = PCA(n_components=2)
# X_pca = pca.fit_transform(X)

# Plot the results
# plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y)
# plt.title('Pokemon clustering')
# plt.xlabel('PCA 1')
# plt.ylabel('PCA 2')
# plt.show()


# Now we will print the pokemons in each cluster

# Get the pokemons in each cluster
