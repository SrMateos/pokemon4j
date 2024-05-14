# Pokemon y sus movimientos
MATCH(p:Pokemon)-[:KNOWS]->(m:Move) RETURN p, m

# Movimiento y su tipo
MATCH(m:Move)-[:IS_TYPE]->(t:Type) RETURN m, t

