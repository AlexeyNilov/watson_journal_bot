from data.fastlite_db import DB, prepare_db
from fastcore.utils import hl_md


prepare_db()

t = DB.t.event
print(hl_md(t.schema, "sql"))

for e in DB.t.event():
    print(e)
    break
