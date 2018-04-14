# Trees

An API for Berlin's street trees.
Based on Django and PostgreSQL/PostGIS.

Trees are extracted from [Baumbestand Berlin](http://fbinter.stadt-berlin.de/fb/index.jsp?loginkey=zoomStart&mapId=k_wfs_baumbestand@senstadt).

## Overview

- Data source: [Baumbestand Berlin](http://fbinter.stadt-berlin.de/fb/index.jsp?loginkey=zoomStart&mapId=k_wfs_baumbestand@senstadt)
- Data extraction via [codeforberlin/wfs-downloader](https://github.com/codeforberlin/wfs-downloader)
- This is the API
- Map for [trees.codefor.de](https://trees.codefor.de) via [codeforberlin/trees-map](https://github.com/codeforberlin/trees-map)
- The map tiles and also the tree tiles are generated using [codeforberlin/trees-mapnik](https://github.com/codeforberlin/trees-mapnik)

### Somewhat related

- [codeforberlin/treemeta](https://github.com/codeforberlin/treemeta) collects botanical names which might be integrated in the API or by a client application.
- [codeforberlin/tree-column-names](https://github.com/codeforberlin/tree-column-names) is not directly used in this project but the basis for the [column-names.json](https://trees.codefor.de/names/column-names.json) that is used.


## Roadmap / features

- [x] Command to import GML file
- [x] API endpoint to filter by properties
- [x] API endpoint to filter by distance from point
- [x] API endpoint to filter by bounding box
- [ ] Filter combining by properties, distance from point, bounding box (Django filters, DRF-GIS)
- [ ] Advanced filtering such as greater then year, fuzzy search on strings
- [ ] Server-side clustering

tbc.


## Set up

``` bash
$ git clone https://github.com/codeforberlin/trees-api
$ cd trees
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ cp trees/settings/sample.local.py trees/settings/local.py
```

edit *trees/settings/local.py* for your database connection

``` python
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'trees',
        'USER': 'postgres',
        'PASSWORD': 'secret',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```


``` bash
$ ./manage.py migrate
$ ./manage.py createsuperuser
$ ./manage.py ingest GMLFILE 2016-02-29T13:00Z
$ ./manage.py runserver
```

go to http://localhost:8000/admin/ or http://localhost:8000


## Making Queries

### REST style object retrieval

```
http://localhost:8000/trees/
http://localhost:8000/trees/1
```

### Location queries

#### Distance to point

```
http://localhost:8000/trees/?dist=100&point=13.381018,52.498606
```

#### On TMS tile

```
http://localhost:8000/trees/?tile=15/17602/10749
```

#### In bounding box

```
http://localhost:8000/trees/?in_bbox=13.20,52.427,13.21,52.428
```

#### Properties

```
http://localhost:8000/trees/?art_dtsch=LINDE&bezirk=Spandau
```
