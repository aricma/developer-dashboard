# --- constants ----------------------------------------------------------------

static_folder_name = ".static"
tasks_dummy_data_file_path = "./dummy_data/tasks_dummy_data.json"

# --- shortcuts ----------------------------------------------------------------

ci: lint tests

dev: build server

build: reset statics $(tasks_dummy_data_file_path)

# ------------------------------------------------------------------------------

lint:
	ruff --fix
	mypy business_logic
	mypy web_interface
	mypy server

tests:
	pytest business_logic --noconftest

.PHONY: server
server:
	STATIC_FOLDER_NAME=$(static_folder_name) \
	VELOCITY_DUMMY_DATA_FILE_PATH=$(tasks_dummy_data_file_path) \
	uvicorn server.__main__:app --reload

$(tasks_dummy_data_file_path):
	python dummy_data/make_random_tasks.py > $(tasks_dummy_data_file_path)

# --- make static web interface html, css and js files -------------------------

statics: all-css-files all-js-files all-data-files all-images

$(static_folder_name):
	mkdir $(static_folder_name)

all-css-files: $(static_folder_name)
	cp web_interface/private/__css_components__/* $(static_folder_name)/

all-js-files: $(static_folder_name)
	cp web_interface/private/__js_files__/* $(static_folder_name)/

all-images: $(static_folder_name)
	@echo "No images in __images__ folder"
	#cp web_interface/private/__images__/* $(static_folder_name)/

all-data-files: $(static_folder_name)
	cp web_interface/private/__data_files__/* $(static_folder_name)/

# --- reset repo ---------------------------------------------------------------

reset: reset-statics reset-dummy-data

reset-statics:
	rm -rf $(static_folder_name)

reset-dummy-data:
	rm -rf $(tasks_dummy_data_file_path)

# --- functions ----------------------------------------------------------------

# "build" will run the given 1 and pipe the stdout of 1 into 2 if 1 finishes without errors
# this prevents the building of empty html files in the static folder, when errors occur
define build
	@echo "$(strip $(1)) > $(strip $(2))"
	@out=$$($(1)) && \
    echo "$$out" > $(2)
endef
