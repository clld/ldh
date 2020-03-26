
Releasing clld/ldh
==================

- add new uploads from Zenodo:
```shell script
ldh crawl
```
- recreate the database:
```bash
ldh initdb --glottolog-version v4.1
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
