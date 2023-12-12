# Kaken local db
Local sqlite database for thing objects


## How to use

```
from kraken_local_Db import kraken_local_db

db = Kraken_local_db('data/localdb.db')

db.post(record)

db.get(record_type, record_id)

db.search(key, value.value)

db.drop()

```

