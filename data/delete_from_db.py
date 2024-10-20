from data.fastlite_db import DB

t = DB.t.event
query = "SELECT * FROM event WHERE text LIKE '%I feel%';"
events = DB.q(query)
for event in events:
    t.delete(event["id"])
    print(event, "deleted")
