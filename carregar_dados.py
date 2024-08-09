import sqlite3
import csv

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('C:/Users/Carlinhos/Ibama/API/animals.db')
cur = conn.cursor()

# Criar a tabela taxa
cur.execute("""
CREATE TABLE IF NOT EXISTS taxa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    taxonID TEXT UNIQUE NOT NULL,
    parentNameUsageID TEXT,
    scientificName TEXT NOT NULL,
    higherClassification TEXT,
    kingdom TEXT,
    phylum TEXT,
    class TEXT,
    "order" TEXT,
    family TEXT,
    genus TEXT,
    subgenus TEXT,
    specificEpithet TEXT,
    infraspecificEpithet TEXT,
    taxonRank TEXT,
    scientificNameAuthorship TEXT,
    FOREIGN KEY (parentNameUsageID) REFERENCES taxa(taxonID)
)
""")

# Carregar dados do arquivo taxon.txt
with open('taxon.txt', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        cur.execute("""
            INSERT OR IGNORE INTO taxa (
                taxonID, parentNameUsageID, scientificName, higherClassification, kingdom, phylum, class, "order", family, genus, subgenus, specificEpithet, infraspecificEpithet, taxonRank, scientificNameAuthorship
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row['taxonID'], row['parentNameUsageID'], row['scientificName'], row['higherClassification'], row['kingdom'], row['phylum'], row['class'], row['order'], row['family'], row['genus'], row['subgenus'], row['specificEpithet'], row['infraspecificEpithet'], row['taxonRank'], row['scientificNameAuthorship']
        ))

# Confirmar as mudanças e fechar a conexão
conn.commit()
cur.close()
conn.close()