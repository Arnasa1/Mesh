> A local-first collaborative workspace with offline support, real-time synchronization, and conflict-free concurrent editing.

Mesh is a collaborative document platform designed around a **local-first architecture**. Users can create and edit documents without an internet connection, while changes are automatically synchronized between devices when connectivity is restored.

The project focuses on distributed systems concepts such as **CRDTs, offline-first applications, event logs, optimistic updates, WebSockets, and conflict resolution**.

---

Installation
Prerequisites

The project requires:

Git
Python 3.13+
uv
Node.js 22+
npm
Docker
Docker Compose



Windows



Install:

Git
Python
Node.js
Docker Desktop

Install uv using PowerShell:

powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

Verify the installation:

git --version
python --version
uv --version
node --version
npm --version
docker --version
docker compose version



macOS



Install Homebrew if it is not already installed.

brew update
brew install git python node uv
brew install --cask docker

Start Docker Desktop, then verify:

git --version
python --version
uv --version
node --version
npm --version
docker --version
docker compose version



Linux



Arch Linux / CachyOS

sudo pacman -Syu
sudo pacman -S --needed git curl base-devel python python-pip nodejs npm docker docker-compose

Enable Docker:

sudo systemctl enable --now docker
sudo usermod -aG docker $USER

Log out and back in for the Docker group change to take effect.

Install uv:

curl -LsSf https://astral.sh/uv/install.sh | sh

Verify:

git --version
python --version
uv --version
node --version
npm --version
docker --version
docker compose version
Ubuntu / Debian
sudo apt update
sudo apt install -y git curl python3 python3-pip nodejs npm docker.io docker-compose-v2

Install uv:

curl -LsSf https://astral.sh/uv/install.sh | sh

Enable Docker:

sudo systemctl enable --now docker
sudo usermod -aG docker $USER

Log out and back in for the Docker group change to take effect.

Verify:

git --version
python3 --version
uv --version
node --version
npm --version
docker --version
docker compose version
Project Setup

Clone the repository and enter the project directory:

git clone <repository-url>
cd mesh
Backend
cd backend


uv python install 3.13
uv python pin 3.13
uv sync

If dependencies have not been configured yet:

uv add fastapi "uvicorn[standard]" pydantic sqlalchemy alembic asyncpg redis
uv add --dev pytest pytest-asyncio httpx
Frontend
cd ../frontend
npm install
Start the Infrastructure

From the project root:

docker compose up -d

Check that PostgreSQL and Redis are running:

docker compose ps
Run the Application
Backend
cd backend
uv run uvicorn app.main:app --reload
Frontend

In a separate terminal:

cd frontend
npm run dev

The Vite development server will display the local URL in the terminal.




Testing
Backend
cd backend
uv run pytest
Frontend
cd frontend
npm run test
End-to-End Tests
cd frontend
npx playwright install
npx playwright test