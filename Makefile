SHELL := /bin/bash
DEPENDENCIES = python3
.DEFAULT_GOAL := help

# Tmux session ID store
tmuxSessionIDStore=".tmux-session-id"

# Define runtime environment.
ENV_FILEPATH="config.py"
ENV_TEMPLATE="config.py.example"

# File walkthrough and detect current env values.
envHostPort="$$(sed -n -e "s/^.*PORT.*=//p" $(ENV_FILEPATH) | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
envHostIP="$$(sed -n -e "s/^.*IP_ADDRESS.*=//p" $(ENV_FILEPATH) | tr -d \'\" | head -n 1 | xargs)"
envDebugModeEnabled="$$(sed -n -e "s/^.*DEBUG.*=//p" $(ENV_FILEPATH) | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
envDBNameDetected="$$(sed -n -e "s/^.*PSQL_DATABASE.*=//p" $(ENV_FILEPATH) | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"

# Before anything else, check if the above commands are installed and available, if not throw error and abort.
K := $(foreach exec,$(DEPENDENCIES), $(if $(shell which "$(exec)"),dependencies_ok,$(error ENVIRONMENT DEPENDENCIES CHECK FAILING: Could not find this command: "$(exec)", Cannot proceed)))

# Default target executed on error.
error:
	@printf "\nUnknown or unhandled target (Makefile error).\n\nAbort.\n\n"
	@exit 2

# Probes if Pip3 is installed in Crapbuntu systems and pulls the barrage of dependencies if missing.
# Compat: Debian jessie+/Ubuntu 12+.
.PHONY: probe-pip3
probe-pip3: ## Meta target to check pip's availability
	@python3 -m pip --version >/dev/null 2>&1 && echo "[Info] pip3 is available...OK" || { echo "pip3 is not installed, installing now..."; sudo apt install -y python3-pip; }

# Probes the existince of Pipenv and installs it if missing.
.PHONY: probe-pipenv
probe-pipenv: | probe-pip3; @python3 -m pipenv --version >/dev/null 2>&1 && echo "[Info] pipenv is available...OK" || { echo "pipenv is not installed, installing now..."; python3 -m pip install --user pipenv; } ## Meta target to check Pipenv's availability


# Fork wsgi server into background and generate a tmux store ID on disk for re-attaching later.
# TODO: abandon and exit tmux sessions when kill-server is invoked.
.PHONY: daemonize
daemonize: kill-server ## Fork server into background
	@newbg() { session_name="new_$$(tmux ls 2>/dev/null | wc -l)"; tmux new-session -d -s "$$session_name" > /dev/null 2>&1; tmux send-keys "$$1" C-m; tmux detach -s "$$session_name" > /dev/null 2>&1; printf "\n\n[Info] Success. started server process in background. You can run 'make attach-bg' from anywhere to activate it again.\n\n"; }; \
	newbg "make run-gunicorn-server"; \
	$$(> $(tmuxSessionIDStore) && echo "$$session_name" > $(tmuxSessionIDStore));

# Look up to read what daemonize does.
.PHONY: reload-server
reload-server:
	@make --no-print-directory daemonize

# Attach to the daemonized session (with set Y-axis mouse scrolling ON).
.PHONY: attach-bg
attach-bg: ## Attach to the daemonized session (tmux is required)
	@[ ! -f "$(tmuxSessionIDStore)" ] && { printf "\nNo background sessions found. Try running \"make daemonize\" to initiate one.\n\n"; exit 0; }; \
	tmuxConfig="$$HOME/.tmux.conf"; \
	$$(grep -Fxq "set -g mouse on" $$tmuxConfig || { echo "set -g mouse on" >> $$tmuxConfig; }); \
	tmux source-file $$tmuxConfig >/dev/null 2>&1; \
	tmux attach -t $$(cat $(tmuxSessionIDStore) | xargs);

# Show whether server is running or not (basically check if host port has an active listener).
.PHONY: show-status
show-status: ## Show the running status of the current server instance
	@port="$(envHostPort)"; \
	lsof -ti tcp:$$port >/dev/null 2>&1 && printf "\n\n[Info] Server is running. Try \"make attach-bg\" to launch the background process interactive shell.\n\n" || printf "\n\nServer isn't running. Nothing to do.\n\n";

# Parse the current env settings file and spit out a few config values of common interest to STDOUT.
# (WARNING: terrible choice of parsing config via sed, more so when the config keeps changing. Maybe find a better structure --schema like?).
.PHONY: print-env-settings
print-env-settings: probe-env-settings ## Parse and display current environment settings
	@printf "\n\n===================================\nCurrent server environment settings\n===================================\n\n"; \
	echo -e "Active settings file: \"$(ENV_FILEPATH)\""; \
	echo -e "\nServer listening on host address: \"$(envHostIP)\""; \
	echo -e "\nServer listening on TCP port: \"$(envHostPort)\""; \
	echo -e "\nDebug mode enabled? $(envDebugModeEnabled)";


# Opens up the env file in your default text editor, preference invariably set to $$EDITOR.
.PHONY: edit-config-file
edit-config-file: ## Open the environment file invariably in the default editor (nano is fallback)
	@envFileNameRel="$$(sed -n -e 's/^.*ENV_FILEPATH.*=//p' "./Makefile" | head -n 1 | tr -d ',' | xargs)" && \
	configFilePath="./$$envFileNameRel" && \
	$${EDITOR:-$${VISUAL:-nano}} $$configFilePath

# Find the PID associated to a current listener port and SIGKILL it. (read warning below).
# (WARNING: terrible choice, yet again, of finding the pid of a port listener and force killing it. 10/10 not recommended.)
# Possible TODOs: 1. Graceful termination of server via SIGTERM and SIGKILL if not responded within alert time (<5s).
.PHONY: kill-server
kill-server: ## Send SIGKILL to current dev server instance
	@port="$(envHostPort)"; \
	printf "\n[Task] Find and attempt to stop any running server instances on port $$port..."; \
	pid=$$(lsof -ti tcp:$$port); \
	kill -9 $$pid >/dev/null 2>&1 \
	&& { printf "\n[Info] Found and successfully stopped running server instances.\n"; } \
	|| { printf "\n[Info] No running instances found for current server. Nothing to do.\n"; }


# Installs the dependencies listed in Pipfile via Pipenv.
.PHONY: install
install: | probe-pipenv; @python3 -m pipenv install; ## Installs project dependencies into a virtualenv --fully managed by Pipenv

# Drops you into a virtualenv shell handled by pipenv
.PHONY: shell
shell: | probe-pipenv; @python3 -m pipenv shell; ## Activate virtualenv shell

# Meta target to ask user confirmation before invoking a target.
ask-confirmation:
	@printf "\n\nAre you sure? [y/N] " && read ans && [ $${ans:-N} = y ]

# Force kills the active database connections to a particular PSQL db.
# Not recommended. TODO: find better alternative of gracefully "sql commit"ing and closing sessions.
.PHONY: kill-active-db-connections
kill-active-db-connections: ask-confirmation ## Force kills active connections made to the current postgres database
	@db_name=$(envDBNameDetected); \
	printf "\nDatabase Name: $$db_name\n\n"; \
	printf "\nForce killing active client connections to the postgresql database...\n\n"; \
	sudo -u postgres psql -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '$$db_name';" && \
	{ printf "\n\nKilled all client connections successfully.\n\n"; } \
	|| { printf "\n\nFailed to kill client connections to selected database.\n\n"; exit 1; };

# This drops the lockfile in-case user wants to manually regenerate it.
# This is especailly a terrible idea as you invariably destroy the reproducible environment your team has built, applies if version pinning isn't done in Pipfile.
# if you need to run this target, don't. seek help.
.PHONY: drop-lockfile
drop-lockfile: ask-confirmation ## Remove Pipenv's lockfile (rarely a good idea)
	@rm -rf Pipfile.lock;

# To be used when the user suspects the virtualenv is crippled and needs to go.
# Start a new virtualenv afresh via pipenv with the "pipenv install" command.
.PHONY: drop-virtualenv
drop-virtualenv: | ask-confirmation probe-pipenv; @python3 -m pipenv --rm; ## Removes the active virtualenv created by Pipenv

# Overwrites (if existing) the current env settings file with a configuration template.
# Use only if you suspect the config file has gone bad and/or is missing values you want to override from envfilepath
.PHONY: reset-local-settings
reset-local-settings: ## Overwrites current environemnt file (if any) with a configuration template
	@envSettingsPath=$(ENV_FILEPATH); \
	exampleEnvFilePath=$(ENV_TEMPLATE); \
	[ ! -f "$$envSettingsPath" ] && { cp $$exampleEnvFilePath $$envSettingsPath && printf "\nDone!\n" || printf "\n\nError: failed to reset local settings.\n\n"; } || { printf "\n\nLocal env settings object exists. Nothing to do.\n\n"; }

# This probes environment settings with a fail and bail on error approach.
.PHONY: probe-env-settings
probe-env-settings: ## Check environment settings file's existence (and create if missing)
	@envSettingsPath=$(ENV_FILEPATH); \
	[ ! -f "$$envSettingsPath" ] && { make reset-local-settings; } || { printf "[Info] successfully loaded environment from \"$$envSettingsPath\"...OK"; }

# This target drops the existing database fully, recreatces it,
# finally generates and applies all migrations.
.PHONY: reinstate-db
reinstate-db: | probe-pipenv probe-env-settings kill-active-db-connections ## Drops and recreates current psql database, regenerates all migrations and applies them
	@db_name=$(envDBNameDetected); \
	printf "\n\n[Info] Using database with name: $$db_name\n\n"; \
    sudo -u postgres psql -c "drop database $$db_name;"; \
    sudo -u postgres psql -c "create database $$db_name;" && \
	python3 -m pipenv run flask db init && \
	make --no-print-directory run-migrations && \
	printf "\n\nSuccessfuly reinstated database and applied migrations!\n\n" \
	|| { printf "\nSomething went wrong with reinstating database. abort\n\n"; exit 1; };


.PHONY: create-migrations
create-migrations: | probe-pipenv probe-env-settings ## Invokes Django's makemigrations command for specified inline apps
	@printf "\n\nCreating database migrations...\n\n"; \
	python3 -m pipenv run  flask db migrate;

.PHONY: apply-migrations
apply-migrations: | probe-pipenv probe-env-settings ## Attempts to apply any unapplied django database migrations
	@printf "\n\nApplying database migrations...\n\n"; \
	python3 -m pipenv run flask db upgrade;

.PHONY: run-migrations
run-migrations: | probe-pipenv probe-env-settings ## Bursts python cache, generates django db migrations freshly, and applies them
	@make create-migrations && make apply-migrations;


# This target starts the in-built wsgi server based on env settings.
.PHONY: run
run: | probe-pipenv probe-env-settings kill-server ## Spawn dev server
	@printf "\nStarting Ground Truth microservice...\n\n"; \
	python3 -m pipenv run python ground_truth.py;

.PHONY: run-gunicorn-server
run-gunicorn-server: | probe-pipenv probe-env-settings kill-server ## Spawn dev server
	@printf "\nStarting Ground Truth microservice...\n\n"; \
	python3 -m pipenv run gunicorn --bind 0.0.0.0:8040 ground_truth:app;

.PHONY: list
list: ## Parse the Make database and display available targets
	@printf "\nAvailable Makefile commands:\n\n" && $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' && printf "\n\n"

.PHONY: help
help:
	@printf "\nAvailable Makefile targets:\n---------------------------\n\n" && grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
