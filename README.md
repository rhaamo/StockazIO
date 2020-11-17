# StockazIO

Manage your inventory of electronic stuff

# V2 Caveats

The following is not implemented and needs to be accessed through django admin `/admin`:
- Edition of:
  - Footprints
  - Storages
  - Categories

# Requirements
- Python 3.8 (minimum !)
- A pretty decent NodeJS + Yarn
- Nginx
- PostgreSQL

# Install

We assume in here you are installing under the `stockazio` user with default home directory `/home/stockazio`, like by doing:
```
useradd -m -s /bin/bash stockazio
```

## API Backend

```shell
sudo su - stockazio
git clone https://github.com/rhaamo/StockazIO/ stockazio
cd stockazio
python3.8 -m virtualenv -p python3.8 venv
source venv/bin/activate
pip install --requirement api/requirements.txt
# For production environment
cp deploy/env.prod.sample .env
$EDITOR .env
# For local development see the other section
cd api
python manage.py collectstatic
# edit config, uses a gunicorn, whatever
# eg.: pip install gunicorn uvicorn
python manage.py migrate
# don't forget to run migrations and then
python manage.py seeds_database
# create a superuser
python manage.py createsuperuser
```

You can uses `deploy/stockazio-server.service` for your systemd service. 

## Frontend
```shell
sudo su - stockazio
cd stockazio/front
yarn install
yarn build
```

## Nginx
See the file `deploy/stockazio-nginx.conf` for a sample, don't forget you need all the `location /xxx` as the example to make it works.

## Development

For local development, you always needs to export `DJANGO_SETTINGS_MODULE=config.settings.local` to have the right config:
```
cp deploy/env.dev.sample .env
$EDITOR .env
cd api
export DJANGO_SETTINGS_MODULE=config.settings.local
python manage.py ...
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
- Can import orders from vendors (Mouser for now) and selective import into inventory with category matching through regexpes

# Orders importer
- Current vendors supported: Mouser
- Set the required values in the `.env` file for Mouser
- Run one time everyday a cron uder the user running the app with:
```
/path/to/app/venv/bin/python /path/to/app/api/manage.py import_orders
```

It will by default import from 'ThisMonth', you can use `--filter=LastMonth` to fetch previous orders.

Available realistic and useful values for filtering: Today, ThisWeek, ThisMonth, LastMonth, ThisYear, LastYear and All.

You then will have to navigate to 'View - Order importer' in the web ui to manage orders: set a default vendor matching the ones in the db, set categories, manage the categories matchers, etc.

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

# Contact
- Fedivers: dashie at pleroma.otter.sh
- Email: stockazio at squeaky dot tech

# License
AGPL v3
