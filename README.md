# StockazIO

Manage your inventory of electronic stuff

# Install

```
git clone this repository
cd StockazIO
python3 -m virtualenv venv
source venv/bin/activate
pip install --requirements api/requirements.txt
edit config, uses a gunicorn, whatever
don't forget to run migrations and then
python manage.py database_seeds
```

# Features

- yummy bugs
- partkeepr import from CSV (fixed fields)
