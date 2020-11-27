#!/bin/sh
set -e

export STOCKAZIO_SPA_HTML_ROOT=/app/front/index.html
export STOCKAZIO_SPA_CSS_ROOT=/app/front/css/
export STOCKAZIO_SPA_JS_ROOT=/app/front/js/

exec "$@"