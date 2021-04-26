
Releasing clld/ldh
==================

- add new uploads from Zenodo's [ldh community](https://zenodo.org/communities/ldh):
```shell script
ldh crawl
```
- recreate the database:
```bash
clld initdb development.ini
```

- Create downloads:
```
clld-create-downloads development.ini 
```

- Upload the downloads to CDSTAR:
```
clldmpg dl2cdstar --version=<version>
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
