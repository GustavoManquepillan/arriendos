#!/usr/bin/env bash

# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

python manage.py loaddata app/fixtures/comunas.json
python manage.py loaddata app/fixtures/regiones.json
python manage.py loaddata app/fixtures/tipo_inmuebles.json
python manage.py loaddata app/fixtures/user.json
python manage.py loaddata app/fixtures/usuarios.json
python manage.py loaddata app/fixtures/inmuebles.json