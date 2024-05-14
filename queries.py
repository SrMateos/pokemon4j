delete_db_query = """
MATCH (n)
DETACH DELETE n
"""

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

INSERT_POKEMON = """
CREATE (p:Pokemon 
    {
        name: $name, 
        num: $num, 
        gen: $gen,
        heightm: $heightm, 
        weightkg: $weightkg,
        hp: $hp,
        atk: $atk,
        def: $def,
        spa: $spa,
        spd: $spd,
        spe: $spe
    }
)
"""

INSERT_ABILITY = """
CREATE (a:Ability {name: $name, description: $description})
"""

INSERT_TYPE = """
CREATE (t:Type {name: $name})
"""

INSERT_POKEMON_TYPE = """
MATCH (p:Pokemon {name: $pokemon}), (t:Type {name: $type})
CREATE (p)-[:IS_TYPE]->(t)
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