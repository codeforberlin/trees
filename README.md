trees
=====

```
git clone https://github.com/jochenklar/trees

cd trees

virtualenv env
source env/bin/activate

pip install -r requirements.txt

cp trees/settings/sample.local.py trees/settings/local.py

# edit trees/settings/local.py for your database connection

./manage.py migrate
./manage.py createsuperuser

./manage.py ingest GMLFILE

./manage.py runserver

# go to http://localhost:8000/admin/
```

more will follow
