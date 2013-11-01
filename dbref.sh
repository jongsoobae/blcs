rm current.sqlite.db
echo 'delete db'
python manage.py syncdb
echo 'syncdb'
python manage.py loaddata info.json
echo 'insert info data'
python manage.py loaddata auth.user.json
echo 'insert auth data'