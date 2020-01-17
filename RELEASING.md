
Releasing clld/ldh
==================

- add new uploads from Zenodo:
```bash
ldh crawl_zenodo
```
- recreate the database. This assumes a soft link `data/concepticon-data`.
```bash
dropdb ldh
createdb ldh
python ldh/scripts/initializedb.py development.ini
```

- Create downloads:
```
clld-create-downloads development.ini 
```

- Upload the downloads to CDSTAR:
```
clldmpg --version=<version> dl2cdstar
```

- Make sure the tests pass
```
pytest
```

- Commit and push all changes
```
git commit -a -m"release <version>"
```

- Create a release of ldh/ldh
- Deploy to https://ldh.clld.org
```
(appconfig)$ fab deploy:production
```
