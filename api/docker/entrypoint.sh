#!/bin/sh
set -e

export STOCKAZIO_SPA_HTML_ROOT=/front/dist/index.html
export STOCKAZIO_SPA_CSS_ROOT=/front/dist/css/
export STOCKAZIO_SPA_JS_ROOT=/front/dist/js/

exec "$@"