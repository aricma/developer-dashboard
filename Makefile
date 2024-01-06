# --- constants ----------------------------------------------------------------

static_folder_name = ".static"

# --- shortcuts ----------------------------------------------------------------

ci: lint

dev: server

build: reset statics

# ------------------------------------------------------------------------------

lint:
	ruff --fix
	mypy business_logic
	mypy web_interface
	mypy server

.PHONY: server
server:
	STATIC_FOLDER_NAME=$(static_folder_name) uvicorn server.__main__:app --reload

start-web-dashboard-locally:
	open ./static/index.html

# --- make static web interface html, css and js files -------------------------

statics: all-css-files all-js-files all-data-files all-images

static:
	mkdir $(static_folder_name)

all-css-files: static
	cp web_interface/private/__css_components__/* $(static_folder_name)/

all-js-files: static
	cp web_interface/private/__js_files__/* $(static_folder_name)/

all-images: static
	cp web_interface/private/__images__/* $(static_folder_name)/

all-data-files: static
	cp web_interface/private/__data_files__/* $(static_folder_name)/

# --- reset repo ---------------------------------------------------------------

reset:
	rm -rf $(static_folder_name)

# --- functions ----------------------------------------------------------------

# "build" will run the given 1 and pipe the stdout of 1 into 2 if 1 finishes without errors
# this prevents the building of empty html files in the static folder, when errors occur
define build
	@echo "$(strip $(1)) > $(strip $(2))"
	@out=$$($(1)) && \
    echo "$$out" > $(2)
endef
