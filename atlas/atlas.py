from collections import defaultdict

import psycopg2
import psycopg2.extras
from jinja2 import Environment, FileSystemLoader

def get_color_class(obs_nbr):
    color = "black"
    if obs_nbr < 1000:
        color = "#DAF7A6"
    elif obs_nbr > 1000 and obs_nbr < 2500:
        color = "#FFC300"
    elif obs_nbr > 2500 and obs_nbr < 5000:
        color = "#FF5733"
    elif obs_nbr > 5000 and obs_nbr < 7500:
        color = "#C70039"
    elif obs_nbr > 7500 and obs_nbr < 10000:
        color = "#900C3F"
    elif obs_nbr > 10000:
        color = "#581845"
    else:
        color = "grey"
    return color

# Connect to your postgres DB
connection = psycopg2.connect(
    database="***REMOVED***",
    user="***REMOVED***",
    password="***REMOVED***",
    host="***REMOVED***",
    port="5432",
)

# Open a cursor to perform database operations
db = connection.cursor(
    cursor_factory = psycopg2.extras.DictCursor,
)

depts = ('01', '04', '05', '26', '38', '73', '74')

query_cd_ref = """SELECT DISTINCT ON (o.cd_ref)
	o.cd_ref AS code,
	t.lib_nom AS "name"
FROM flore.observation AS o
	JOIN referentiels.taxref AS t
		ON o.cd_ref = t.cd_ref
	JOIN flore.releve AS r
		ON o.id_releve = r.id_releve
WHERE r.insee_dept IN %(depts)s AND o.cd_ref > 79000
LIMIT 10 ;
"""

db.execute(query_cd_ref, {"depts": depts})
records = db.fetchall()
taxons = []
for record in records:
    taxons.append({
        "code": record["code"],
        "name": record["name"],
    })

for taxon in taxons:
    print(f"{taxon['name']}:")
    query_obs = """SELECT
        r.insee_dept AS dept,
        COUNT(*) AS obs_nbr
    FROM flore.observation AS o
        JOIN flore.releve AS r
            ON o.id_releve = r.id_releve
    WHERE cd_ref = %(cd_ref)s
        AND r.insee_dept IN %(depts)s
    GROUP BY r.insee_dept ;
    """

    # Execute a query
    db.execute(query_obs, {"cd_ref": taxon["code"], "depts": depts})
    # Retrieve query results
    records = db.fetchall()

    colors = {}
    colors = defaultdict(lambda:[], colors)
    for record in records:
        color = get_color_class(record["obs_nbr"])
        colors[color].append(f"#dep{record['dept']}")

    styles = []
    for color, depts_codes in colors.items():
        styles.append({"selector": ', '.join(depts_codes), "color": color})

    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("depts.jinja.svg")
    content = template.render({"styles":styles})
    taxon_name = taxon["name"].lower().replace(' ', '_')
    filename = f"output/depts_{taxon_name}.svg"
    with open(filename, mode="w", encoding="utf-8") as svg:
        svg.write(content)
        print(f"... wrote {filename}")
