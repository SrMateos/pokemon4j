# Pokedex4j
Pokemon4j es un proyecto para aprender sobre bases de datos NoSQL, en este caso Neo4j, y sobre minería de datos, en este caso haciendo una regresión lineal sobre estadísticas de pokemon y un clustering con KMeans.

# Requirements.txt
Para instalar las dependencias necesarias ejecute el siguiente comando:
```bash
pip install -r requirements.txt
```

# Base de datos
Para ejecutar la base de datos de Neo4j en Docker, ejecute el siguiente comando:
```bash
docker-compose -f neo4j.yaml up -d
```

El archivo neo4j.yaml contiene la configuración necesaria para ejecutar la base de datos de Neo4j en Docker.

# Importar datos
Para importar los datos de los pokemons a la base de datos de Neo4j, puede ejecutar el archivo main.py, el cual le preguntará si desea importar los datos de los pokemons a la base de datos. También puede ejecutar directamente el archivo dump_data.py.

# Ejecución de los scripts
## Aplicación
Ejecuta la aplicación de comparador de pokemons con la Base de datos Neo4j

## Linear regresión
Ejecute el archivo lin_regression.py

## Clustering con KMeans
Ejecute el archivo clustering.py o visualce el archivo clustering.ipynb