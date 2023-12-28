# --- shortcuts ----------------------------------------------------------------

dev: start-web-dashboard-locally

.PHONY: server
server:
	uvicorn server.__main__:app --reload

# ------------------------------------------------------------------------------

start-web-dashboard-locally:
	open ./index.html
