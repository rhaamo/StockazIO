# StockazIO

Manage your inventory of electronic stuff

# Features

- API first! Everything is done through the backend API, auth via oauth2.
- yummy bugs
- partkeepr import from CSV (fixed fields, see [here](https://github.com/rhaamo/StockazIO/blob/master/api/controllers/part/management/commands/import_partkeepr.py#L14) for them) 
- Categories tree for parts
- Storage categories and Storage Locations (with possible pictures)
- Footprints categories and actual footprint in them (with possible picture)
- Parts can have distributors SKU, manufacturers SKU, parts parameters and file attachments
- Parts and Storage Locations have UUIDs and QRCode (containing a specific URI usuable in the search input)
- Quick add form and a full-featured one
- Can import orders from vendors (Mouser for now) and selective import into inventory with category matching through regexpes
- Project management with BOM with parts from inventory or free-form (with export of BOM to CSV or XLSX)
- PDF Generator for labels printing of Storage Locations (plus bulk-generation) or Parts

# V2 Caveats

The following is not implemented and needs to be accessed through django admin `/admin`:
- Edition of:
  - Footprints
  - Categories

# Requirements
- Python 3.8 (minimum !)
- A pretty decent NodeJS + Yarn
- Nginx
- PostgreSQL

# API Documentation

After installing the backend, Swagger documentation will be accessible at:
- http://backend_url/api/doc/swagger/
- http://backend_url/api/doc/redoc/

# Install - manual

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
# don't forget to run migrations
python manage.py migrate
# and then seed some initial datas (categories, manufacturers, footprints, ...)
python manage.py seeds_database
# create a superuser
python manage.py createsuperuser
```

You can uses `deploy/stockazio-server.service` for your systemd service. 

## NodeJS warning
You might need to uses thoses commands because of weird things in NodeJS and incompatibilities...

If using NodeJS 16.x uses the following commands for the frontend instead of the other ones:
```
CXXFLAGS="--std=c++14" yarn install
do yarn build classic
```

For NodeJS 17.x:
```
CXXFLAGS="--std=c++14" yarn install
NODE_OPTIONS=--openssl-legacy-provider yarn build
```

The build might also fails related to memory (https://github.com/vitejs/vite/issues/2433) so the workaround is:
```
node --max_old_space_size=16384 ./node_modules/vite/bin/vite.js build
```

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

### Docker All-In-One image build
```
docker build -t stockazio-allinone -f Dockerfile-allinone
```

## Updating
Look at release changes first if anything is needed.

```
sudo su - stockazio
cd stockazio
source venv/bin/activate
git pull
cd front
yarn install
yarn build
cd ../api
pip install -r requirements.txt
python manage.py migrate
```

Then restart your `stockazio-server` service.

# Install - docker All In One
You can use the `Dockerfile-allinone` to run StockazIO.

See the file ./deploy/env.prod.sample for the list of ENV variables you can use for the container.

You can copy that env file, edit it, and use `--env-file your-env-file.prod` for `docker run/exec` too.

The volume for uploads is `/uploads`.

To migrate the database:
```
docker exec -it stockazio python manage.py migrate
```

To seed database:
```
docker exec -it stockazio python manage.py seeds_database
```

To create your superuser:
```
docker exec -it stockazio python manage.py createsuperuser
```

Example build & run:
```
docker build -t stockazio-allinone -f Dockerfile-allinone .
docker run --net=host --name stockazio -it --rm --env-file .env -v /local/path/to/uploads:/uploads stockazio-allinone:latest
```

# Install - docker split frontend & backend
TODO

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
- Export of all components or a category or search
- Mobile app / better mobile layout

# Generated QRCodes format
Format changed but both URLs are handled by the search.

- StorageLocation: `web+stockazio:storageLocation,{uuid}` (old format: `stockazio://storageLocation/{uuid}`)
- Part: `web+stockazio:part,{uuid}` (old format: `stockazio://part/{uuid}`)

# Changelog
- Part file attachments split into file and picture, if you had uploads prior to that split, use that command to migrate them: `python3 manage.py migrations_move_from_one_to_two_part_file_fields`

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
