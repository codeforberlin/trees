# Trees

## Set up

``` bash
$ git clone https://github.com/jochenklar/trees

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

$ ./manage.py ingest GMLFILE

$ ./manage.py runserver
```

go to http://localhost:8000/admin/ or http://localhost:8000/api/


## Making Queries

### REST style object retrieval

```
http://localhost:8000/api/trees/
http://localhost:8000/api/trees/1
```

### Location queries

#### Distance to point:

http://localhost:8000/api/location/?dist=40&point=13.20887016004902,52.42724780253829

#### On TMS tile

http://localhost:8000/api/location/?tile=16/35172/21520

#### In bounding box

http://localhost:8000/api/location/?in_bbox=13.20,52.427,13.21,52.428
