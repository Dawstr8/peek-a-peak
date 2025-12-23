# 🏔️ Peek-a-Peak - Development Container

Full-stack FastAPI + Next.js project with a batteries-included Dev Container that boots the entire docker-compose stack automatically - no manual setup required.

## 🚀 Quick Start

1. **Install Prerequisites**

   - [VS Code](https://code.visualstudio.com/)
   - [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
   - [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker Engine)

2. **Open in Dev Container**

   ```bash
   git clone https://github.com/dawstr8/peek-a-peak.git
   cd peek-a-peak
   code .  # Opens VS Code
   ```

   Then: `Ctrl+Shift+P` → **Dev Containers: Reopen in Container**

3. **Wait for Auto-Setup**

   - Dev container builds (installs Python, Node.js, extensions)
   - Docker Compose stack starts automatically (backend, frontend, Postgres, MinIO)
   - All services are ready when the terminal shows `Container started`

4. **Start Coding!**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🧱 Running Services

| Service           | Description                 | URL / Port                        | Credentials                                |
| ----------------- | --------------------------- | --------------------------------- | ------------------------------------------ |
| Frontend          | Next.js 15.5.4 dev server   | http://localhost:3000             | —                                          |
| Backend API       | FastAPI (Python 3.11)       | http://localhost:8000             | —                                          |
| API Docs          | Swagger UI                  | http://localhost:8000/docs        | —                                          |
| PostgreSQL        | Primary database            | `localhost:5432` → `peek_a_peak`  | `postgres` / `postgres`                    |
| MinIO Console     | Object storage UI           | http://localhost:9001             | `minioadmin` / `minioadmin`                |
| MinIO S3 Endpoint | S3-compatible bucket access | http://localhost:9000/peek-a-peak | Access: `minioadmin`, Secret: `minioadmin` |

Volumes defined in `docker-compose.dev.yaml` persist Postgres (`postgresdata`) and MinIO (`miniodata`) data between restarts.

## 🛠️ Development Workflow

### Docker Compose Commands

```bash
# View running containers
docker compose -f docker-compose.dev.yaml ps

# View logs (all services)
docker compose -f docker-compose.dev.yaml logs -f

# View logs (specific service)
docker compose -f docker-compose.dev.yaml logs -f backend

# Restart a service
docker compose -f docker-compose.dev.yaml restart frontend

# Stop all services
docker compose -f docker-compose.dev.yaml down

# Stop and remove volumes (full reset)
docker compose -f docker-compose.dev.yaml down -v
```

## 🐛 Troubleshooting

### Port conflicts

If ports 3000, 8000, 5432, or 9000 are already in use:

1. Stop conflicting services on host machine
2. Or modify ports in `docker-compose.dev.yaml`
3. Restart the stack: `docker compose -f docker-compose.dev.yaml down && docker compose -f docker-compose.dev.yaml up`

### Dev container won't rebuild

```bash
# From VS Code Command Palette (Ctrl+Shift+P)
Dev Containers: Rebuild Container Without Cache

# Or manually from terminal
docker compose -f docker-compose.dev.yaml down
docker system prune -a  # Warning: removes all unused images
```

### Hot reload not working

- **Backend**: FastAPI dev server watches `.py` files automatically
- **Frontend**: Next.js Turbopack watches all `src/` files
- If changes aren't reflected, try restarting the service or rebuilding the container

## 📚 Additional Resources

- [Backend README](../backend/README.md) – API details, testing, migrations
- [Frontend README](../frontend/README.md) – Component patterns, state management
- [Main README](../README.md) – Project overview, architecture
- [Docker Compose docs](https://docs.docker.com/compose/)
- [Dev Containers docs](https://code.visualstudio.com/docs/devcontainers/containers)

Happy building! 🧗
