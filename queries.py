
# DELETE
DELETE_DB_QUERY = """
MATCH (n)
DETACH DELETE n
"""

DELETE_MOVE = """
MATCH (m:Move {name: $name})
DETACH DELETE m
"""


# QUERIES
QUERY_ALL_POKEMON = """
MATCH (p:Pokemon)
RETURN p
ORDER BY p.num
"""

QUERY_POKEMON_BY_NUMBER = """
MATCH (p: Pokemon {num: $num})
RETURN p
"""

QUERY_POKEMON_BY_WEIGHT = """
MATCH (p:Pokemon)
WHERE p.weightkg >= $min_weight AND p.weightkg <= $max_weight
RETURN p
"""

QUERY_POKEMON_BY_TYPE = """
MATCH (p:Pokemon)-[:IS_TYPE]->(t:Type {name: $type})
RETURN p
"""

QUERY_POKEMON_BY_GENERATION = """
MATCH (p:Pokemon)-[:BELONGS_TO]->(g:Generation {generation: $gen})
RETURN p
ORDER BY p.num
"""

QUERY_POKEMON_BY_ABILITY = """
MATCH (p:Pokemon)-[:HAS_ABILITY]->(a:Ability {name: $ability})
return p
"""

QUERY_POKEMON_BY_MOVE = """
MATCH (p:Pokemon-[:KNOWS]->(m:Move {name: $move}))
return p
"""

QUERY_POKEMON_TYPES = """
MATCH (p:Pokemon {name: $name})-[:IS_TYPE]->(t:Type)
RETURN t
"""

QUERY_TYPES_EFFECTIVITY = """
MATCH (t1:Type {name: $type1}), (t2:Type {name: $type2})
MATCH (t1)-[r:EFFECTIVITY]->(t2)
RETURN r.damage AS damage
"""

QUERY_POKEMON_BY_NAME = """
MATCH (p:Pokemon)
WHERE p.name = $name
RETURN p
"""

QUERY_ALL_TYPES = """
MATCH (t:Type)
RETURN t
"""

QUERY_ALL_MOVES = """
MATCH (m:Move)
RETURN m
"""

QUERY_ALL_ABILITIES_ASOCIATED_TO_POKEMONS = """
MATCH (p:Pokemon)-[:HAS_ABILITY]->(a:Ability)
RETURN DISTINCT a
"""

QUERY_POKEMON_MOVE = """
MATCH (p:Pokemon {name: $name})-[:KNOWS]->(m:Move)
RETURN m
"""

QUERY_POKEMON_MOVE_BY_NUM = """
MATCH (p:Pokemon {num: $num})-[:KNOWS]->(m:Move)
RETURN m
"""

QUERY_MOVE_BY_NAME = """
MATCH(m: Move {name: $name})
RETURN m
"""

QUERY_MOVE_TYPE = """
MATCH (m:Move {name: $name})-[:IS_TYPE]->(t:Type)
RETURN t
"""

QUERY_ABILITY_BY_POKEMON = """
MATCH (p:Pokemon {name: $name})-[:HAS_ABILITY]->(a:Ability)
RETURN a
"""

QUERY_BY_POKEMON_GENERATION = """
MATCH (p:Pokemon {name: $name})-[:BELONGS_TO]->(g:Generation)
RETURN p
"""

QUERY_MOVE_BY_NAME = """
MATCH (m:Move {name: $name})
RETURN m
"""


# UPDATE
UPDATE_MOVEMENT = """
MATCH (m: Move {name: $name})
SET m.name = $new_name, m.accuracy = $accuracy,
m.basePower = $basePower, m.pp = $pp,
m.category = $category, m.description = $description
RETURN m
"""

UPDATE_POKEMON_MOVE = """
MATCH (p: Pokemon {num: $num})-[r:KNOWS]->(m1: Move)
MATCH (m2: Move {name: $newMove})
WHERE EXISTS((p)-[:KNOWS]->(m1))
DELETE r
CREATE (p)-[:KNOWS]->(m2)
"""

# INSERTS
INSERT_POKEMON = """
CREATE (p:Pokemon 
    {
        name: $name, 
        num: $num, 
        heightm: $heightm, 
        weightkg: $weightkg,
        hp: $hp,
        atk: $atk,
        def: $def,
        spa: $spa,
        spd: $spd,
        spe: $spe,
        legendary: $legendary,
        final_evolution: $final_evolution
    }
)
"""

INSERT_ABILITY = """
CREATE (a:Ability {name: $name, description: $description})
"""

INSERT_ABILITY_IF_NOT_EXISTS = """
MERGE (a:Ability {name: $name})
ON CREATE SET a.description = $description
"""

INSERT_TYPE = """
CREATE (t:Type {name: $name})
"""

INSERT_GENERATION = """
CREATE (g:Generation {generation: $gen})
"""

INSERT_POKEMON_TYPE = """
MATCH (p:Pokemon {name: $pokemon}), (t:Type {name: $type})
CREATE (p)-[:IS_TYPE]->(t)
"""

INSERT_POKEMON_GENERATION = """
MATCH (p: Pokemon {name: $pokemon}), (g:Generation {generation: $gen})
CREATE (p)-[:BELONGS_TO]->(g)
"""

INSERT_POKEMON_ABILITY = """
MATCH (p:Pokemon {name: $pokemon}), (a:Ability {name: $ability})
CREATE (p)-[:HAS_ABILITY]->(a)
"""

INSERT_MOVE = """
MERGE (m:Move {name: $name})
ON CREATE SET m += {
    name: $name,
    accuracy: $accuracy,
    basePower: $basePower,
    pp: $pp,
    category: $category,
    description: $description
}
"""

INSERT_POKEMON_MOVES = """
MATCH (p:Pokemon {name: $pokemon}), (m:Move {name: $move})
CREATE (p)-[:KNOWS]->(m)
"""

INSERT_MOVES_TYPE = """
MATCH (m:Move {name: $move}), (t:Type {name: $type})
CREATE (m)-[:IS_TYPE]->(t)
"""

INSERT_TYPE_CHART = """
MATCH (t1:Type {name: $type1}), (t2:Type {name: $type2})
CREATE (t1)-[:EFFECTIVITY {damage: $damage}]->(t2)
"""