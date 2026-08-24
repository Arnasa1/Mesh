# Mesh

##‼️ The project is curently in early development ‼️

##**Mesh** is a local-first collaborative document platform that lets users work offline and automatically sync changes across devices once they reconnect.

##**Features**:
- ###CRDTs and conflict resolution
- ###Offline-first applications
- ###Event logs
- ###Optimistic updates
- ###WebSockets
- ###Automatic synchronization between devices

##**Installation Prerequisites**:
### 1. Windows installation:
- #### [Git](https://git-scm.com/)
- #### [Python](https://www.python.org/)
- #### [Node.js](https://nodejs.org/en)
- #### [Docker Desktop](https://nodejs.org/en)
- #### Install uv using PowerShell: ```powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" ```

### 2. MacOS installation:
- #### [Homebrew](https://brew.sh/)
- #### insall using Homebrew ``` brew update brew install git python node uv brew install --cask docker ```

### 3. Arch based linux
- #### bash ```sudo pacman -Syu --needed git curl base-devel python python-pip nodejs npm docker docker-compose```

- #### bash ```yay install uv ```

## Clone the repository and enter the project directory:
####git clone cd mesh Backend cd backend

####uv python install 3.13 uv python pin 3.13 uv sync

###If dependencies have not been configured yet:

####uv add fastapi "uvicorn[standard]" pydantic sqlalchemy alembic asyncpg redis uv add --dev pytest pytest-asyncio httpx Frontend cd ../frontend npm install Start the Infrastructure

###From the project root:

####docker compose up -d

###Check that PostgreSQL and Redis are running:

####docker compose ps Run the Application Backend cd backend uv run uvicorn app.main:app --reload Frontend

###In a separate terminal:

####cd frontend npm run dev

###The Vite development server will display the local URL in the terminal.

####Testing Backend cd backend uv run pytest Frontend cd frontend npm run test End-to-End Tests cd frontend npx playwright install npx playwright test


