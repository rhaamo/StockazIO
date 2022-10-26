#!/bin/sh
set -e

export STOCKAZIO_SPA_HTML_ROOT=/app/front/index.html
export STOCKAZIO_SPA_ASSETS_ROOT=/app/front/assets/

export STATIC_ROOT=/statics
export MEDIA_ROOT=/uploads

exec "$@"
