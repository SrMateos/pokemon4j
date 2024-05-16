# lets create a linear regression of the statistics of a pokemon and the generation
# in order to see if the pokemons are getting stronger with each generation
# To see if there is correlation between the generation and the statistics of the pokemons
# we will use index of correlation of pearson

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr
from sklearn.model_selection import train_test_split

from utils import exec_query
from queries import QUERY_ALL_POKEMON

def get_stats_list_by_number():
    records, summary, keys = exec_query(QUERY_ALL_POKEMON, {})
    stats = []
    names = []
    for record in records:
        if record['p']['legendary'] == 0:
            stats.append([record['p']['num'], sum([record['p']['hp'], record['p']['atk'], record['p']['def'], record['p']['spa'], record['p']['spd'], record['p']['spe']])])
            names.append(record['p']['name'])
    return stats, names
    
number_statistics, names = get_stats_list_by_number()

# Now we will have to create the X and y values for the linear regression
# The x will be the generation and the y will be the statistics of the pokemons
# Consider that we have a list of 6 statistics for each pokemon for each pokemon in each generation
X = [i[0] for i in number_statistics]
y = [i[1] for i in number_statistics]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a linear regression model
model = LinearRegression()
model.fit(np.array(X_train).reshape(-1, 1), np.array(y_train).reshape(-1, 1))   
y_pred = model.predict(np.array(X_test).reshape(-1, 1))

# Calculate confusion matrix of the estimation for each generation given the statistics of the pokemons


# Calculate the correlation between the generation and the statistics of the pokemons
correlation = pearsonr(X, y)
print(correlation)

# Plot the results
plt.scatter(X, y, color='blue')
plt.plot(X_test, y_pred, color='red')
plt.title('Pokemon statistics by generation')
plt.xlabel('Generation')
plt.ylabel('Statistics')
for i, name in enumerate(names):
    plt.annotate(name, (X[i], y[i]))
plt.show()
