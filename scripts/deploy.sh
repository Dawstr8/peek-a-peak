#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.yaml}"

log() {
	printf "\n[deploy] %s\n" "$*"
}

warn() {
	printf "\n[deploy][warn] %s\n" "$*" >&2
}

require_command() {
	if ! command -v "$1" >/dev/null 2>&1; then
		echo "Required command '$1' not found on PATH" >&2
		exit 1
	fi
}

ensure_clean_worktree() {
	if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
		echo "This script must be run inside a git repository" >&2
		exit 1
	fi

	if [[ -n $(git status --porcelain) ]]; then
		echo "Working tree has uncommitted changes. Please stash or commit before deploying." >&2
		exit 1
	fi
}

pull_latest_main() {
	log "Fetching latest changes from origin/main"
	git fetch origin main

	local current_branch
	current_branch="$(git rev-parse --abbrev-ref HEAD)"
	if [[ "$current_branch" != "main" ]]; then
		log "Checking out main branch"
		git checkout main
	fi

	git pull --ff-only origin main
}

find_volume() {
	local override="$1"
	local suffix="$2"
	local project_name
	project_name="${COMPOSE_PROJECT_NAME:-$(basename "$REPO_ROOT")}"

	if [[ -n "$override" ]]; then
		if docker volume inspect "$override" >/dev/null 2>&1; then
			printf '%s' "$override"
			return 0
		fi
		warn "Volume '$override' not found"
		return 1
	fi

	for candidate in "${project_name}_${suffix}" "$suffix"; do
		if docker volume inspect "$candidate" >/dev/null 2>&1; then
			printf '%s' "$candidate"
			return 0
		fi
	done

	return 1
}

backup_volume() {
	local volume_name="$1"
	local archive_name="$2"

	if [[ -z "$volume_name" ]]; then
		warn "Skipping backup for '$archive_name' – volume not found"
		return
	fi

	log "Backing up volume '$volume_name' to ${archive_name}"
	docker run --rm \
		-v "${volume_name}:/data" \
		-v "${BACKUP_DIR}:/backup" \
		alpine:3 sh -c "cd /data && tar -czf /backup/${archive_name} ."
}

build_and_start_stack() {
	log "Building and starting containers"
	docker compose -f "$COMPOSE_FILE" up -d --build
}

run_migrations() {
	log "Running Alembic migrations"
	docker compose -f "$COMPOSE_FILE" exec -T backend alembic upgrade head
}

run_seed() {
	log "Running database seed"
	docker compose -f "$COMPOSE_FILE" exec -T backend python -m src.database.seed.run_seed
}

main() {
	require_command git
	require_command docker
	docker compose version >/dev/null 2>&1 || {
		echo "docker compose plugin is required" >&2
		exit 1
	}

	if [[ ! -f "$COMPOSE_FILE" ]]; then
		echo "Compose file '$COMPOSE_FILE' not found" >&2
		exit 1
	fi

	ensure_clean_worktree
	pull_latest_main

	local timestamp
	timestamp="$(date +%Y%m%d-%H%M%S)"
	BACKUP_DIR="$REPO_ROOT/backups/$timestamp"
	mkdir -p "$BACKUP_DIR"

	log "Creating backups in $BACKUP_DIR"
	local postgres_volume
	local minio_volume
	postgres_volume="$(find_volume "${POSTGRES_VOLUME_NAME:-}" "postgresdata" || true)"
	minio_volume="$(find_volume "${MINIO_VOLUME_NAME:-}" "miniodata" || true)"

	backup_volume "$postgres_volume" "postgres-$timestamp.tar.gz"
	backup_volume "$minio_volume" "minio-$timestamp.tar.gz"

	build_and_start_stack
	run_migrations
	run_seed

	log "Deployment complete"
	log "Backups stored in $BACKUP_DIR"
}

main "$@"
