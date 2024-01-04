# --- shortcuts ----------------------------------------------------------------

dev: start-web-dashboard-locally

.PHONY: server
server:
	uvicorn server.__main__:app --reload

build: reset statics

# ------------------------------------------------------------------------------

start-web-dashboard-locally:
	open ./static/index.html

# --- make static web interface html, css and js files -------------------------

statics: all-css-files all-js-files all-data-files all-images

static:
	mkdir "static"

all-css-files: static
	cp web_interface/private/__css_components__/* static/

all-js-files: static
	cp web_interface/private/__js_files__/* static/

all-images: static
	cp web_interface/private/__images__/* static/

all-data-files: static
	cp web_interface/private/__data_files__/* static/

# --- reset repo ---------------------------------------------------------------

reset:
	rm -rf static

# --- functions ----------------------------------------------------------------

# "build" will run the given 1 and pipe the stdout of 1 into 2 if 1 finishes without errors
# this prevents the building of empty html files in the static folder, when errors occur
define build
	@echo "$(strip $(1)) > $(strip $(2))"
	@out=$$($(1)) && \
    echo "$$out" > $(2)
endef
