
Releasing clld/ldh
==================

- add new uploads from Zenodo's [ldh community](https://zenodo.org/communities/ldh):
```shell
ldh crawl
```
- recreate the database:
```shell
clld initdb development.ini
```

- Create downloads:
```shell
clld create_downloads development.ini ldh.clld.org 
```

- Upload the downloads to CDSTAR:
```shell
clldmpg dl2cdstar --version=<version>
```

- Make sure the tests pass
```shell
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
