QUERY_POKEMON_BY_GENERATION = """
MATCH (p:Pokemon)-[:IS_FROM_GENERATION]->(g:Generation {number: $generation})
RETURN p
"""

QUERY_POKEMON_BY_HEIGHT = """
MATCH (p:Pokemon)
WHERE p.heightm >= $min_height AND p.heightm <= $max_height
RETURN p
"""

QUERY_POKEMON_BY_TYPE = """
MATCH (p:Pokemon)-[:IS_OF_TYPE]->(t:Type {name: $type})
RETURN p
"""

QUERY_POKEMON_BY_ABILITY = """
MATCH (p:Pokemon)-[:HAS_ABILITY]->(a:Ability {name: $ability})
return p
"""

QUERY_POKEMON_BY_MOVE = """
MATCH (p:Pokemon-[HAS_MOVE]->(m:Move {name: $move}))
return p
"""

QUERY_POKEMON_BY_NAME = """
MATCH (p:Pokemon)
WHERE p.name == $name
RETURN p
"""

