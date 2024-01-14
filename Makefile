# --- constants ----------------------------------------------------------------

static_folder_name = .static
path_to_task_dummy_data = ./dummy_data

# --- shortcuts ----------------------------------------------------------------

ci: local-ci

dev: build server

build: reset statics dummy-data

# --- dummy data ---------------------------------------------------------------

dummy-data:
	poetry run python dummy_data/make_random_tasks.py

# --- CI -----------------------------------------------------------------------

local-ci: refactor lint tests

refactor:
	poetry run black .
	poetry run ruff --fix

lint:
	poetry run ruff check
	poetry run mypy business_logic
	poetry run mypy web_interface
	poetry run mypy server

tests:
	poetry run pytest business_logic --noconftest

.PHONY: server
server:
	STATIC_FOLDER_NAME=$(static_folder_name) \
	PATH_TO_TASK_DUMMY_DATA=$(path_to_task_dummy_data) \
	poetry run uvicorn server.__main__:app --reload

# --- make static web interface html, css and js files -------------------------

statics: all-css-files all-js-files all-data-files all-images

$(static_folder_name):
	mkdir $(static_folder_name)

all-css-files: $(static_folder_name)
	cp web_interface/private/__css_components__/* $(static_folder_name)/

all-js-files: $(static_folder_name)
	cp web_interface/private/__js_files__/* $(static_folder_name)/

all-images: $(static_folder_name)
	cp web_interface/private/__images__/* $(static_folder_name)/

all-data-files: $(static_folder_name)
	cp web_interface/private/__data_files__/* $(static_folder_name)/

# --- reset repo ---------------------------------------------------------------

reset: reset-statics

reset-statics:
	rm -rf $(static_folder_name)

# --- functions ----------------------------------------------------------------

# "build" will run the given 1 and pipe the stdout of 1 into 2 if 1 finishes without errors
# this prevents the building of empty html files in the static folder, when errors occur
define build
	@echo "$(strip $(1)) > $(strip $(2))"
	@out=$$($(1)) && \
    echo "$$out" > $(2)
endef
