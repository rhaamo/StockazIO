# StockazIO

Manage your inventory of electronic stuff

# Install

```
git clone this repository
cd StockazIO
git submodule init
git submodule update
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

# Images sources
- Footprints
    - Unless noted, from https://commons.wikimedia.org/, original names, some have been edited to add a transform for orientation and size.
    - plcc.svg by cpsdqs
    - so8.svg other
    - tqfp.svg other
    - qip-component-package-photo.jpg [here](https://blog.mbedded.ninja/pcb-design/component-packages/qip-component-package/#&gid=1&pid=1)
- Manufacturers
    - \*shrug*

# TODO
- All edit/new/delete/etc. should keep the: a) category if any, b) q= if any

