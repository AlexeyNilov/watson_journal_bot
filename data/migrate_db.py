from data.fastlite_db import prepare_db, DB


prepare_db()

for t in DB.tables:
    print(t.name, len(t()))
