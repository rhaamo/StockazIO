# StockazIO

Manage your inventory of electronic stuff

# Install

```
git clone https://github.com/rhaamo/StockazIO/
cd StockazIO
git submodule init
git submodule update
python3 -m virtualenv -p python3 venv
source venv/bin/activate
pip install --requirement api/requirements.txt
cd api
python manage.py collectstatic
# edit config, uses a gunicorn, whatever
# eg.: pip install gunicorn uvicorn
# don't forget to run migrations and then
python manage.py seeds_database
```

# Features

- yummy bugs
- partkeepr import from CSV (fixed fields, see [here](https://github.com/rhaamo/StockazIO/blob/master/api/controllers/part/management/commands/import_partkeepr.py#L14) for them) 
- Categories tree for parts
- Storage categories and Storage Locations (with possible pictures)
- Footprints categories and actual footprint in them (with possible picture)
- Parts can have distributors SKU, manufacturers SKU, parts parameters and file attachments
- Parts and Storage Locations have UUIDs and QRCode (containing a specific URI usuable in the search input)
- Quick add form and a full-featured one

# TODO List
- KISS Project management
- Project BOM state
- Export of project BOM
- Export of all components or a category or search
- ???

# Generated QRCodes format
- StorageLocation: `stockazio://storageLocation/{uuid}`
- Part: `stockazio://part/{uuid}`

# Images sources
- Footprints
    - Unless noted, from https://commons.wikimedia.org/, original names, some have been edited to add a transform for orientation and size.
    - plcc.svg by cpsdqs
    - so8.svg other
    - tqfp.svg other
    - qip-component-package-photo.jpg [here](https://blog.mbedded.ninja/pcb-design/component-packages/qip-component-package/#&gid=1&pid=1)
- Manufacturers
    - \*shrug*
