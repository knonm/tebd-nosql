NEO4J_HOME="/opt/neo4j-community-3.0.6"
PY_VIR_HOME="/home/mcanon/virtualenv/TEBD"

NEO4J_STATUS=$(${NEO4J_HOME}/bin/neo4j status)

if [[ "${NEO4J_STATUS}" = "Neo4j is not running" ]]; then
  ${NEO4J_HOME}/bin/neo4j start
else
  ${NEO4J_HOME}/bin/neo4j stop
fi

. ${PY_VIR_HOME}/bin/activate

