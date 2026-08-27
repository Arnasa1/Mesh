# Mesh

## ‼️ The project is curently in early development ‼️

## **Mesh** is a local-first collaborative document platform that lets users work offline and automatically sync changes across devices once they reconnect.

## **Features**:
- ### CRDTs and conflict resolution
- ### Offline-first applications
- ### Event logs
- ### Optimistic updates
- ### WebSockets
- ### Automatic synchronization between devices

## **Development setup**:
### Windows
<details>
<summary>Windows Installation (For less experienced users)</summary>

#### 1. Install core dependecies:
- #### [Git](https://git-scm.com/)
- #### [Python](https://www.python.org/)
- #### [Node.js](https://nodejs.org/en)
- #### [Docker Desktop](https://nodejs.org/en)
- #### Install uv using PowerShell:
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
 ```
  #### 2. Setup:
``` bash
git clone https://github.com/Arnasa1/Mesh.git
```
#### Backend
``` bash
cd Mesh/backend
uv sync
```
#### Frontend
``` bash
cd ../frontend
npm install
```
</details>

<details>
<summary>Winget (Reccomended)</summary>

#### 1. Install core dependecies:
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
 ```
  #### 2. Setup:
``` bash
git clone https://github.com/Arnasa1/Mesh.git
```
#### Backend
``` bash
cd Mesh/backend
uv sync
```
#### Frontend
``` bash
cd ../frontend
npm install
```
</details>

### MacOS
<details>
<summary>Homebrew</summary>

#### 1. Install core dependecies
- #### [Homebrew](https://brew.sh/)
- #### insall using Homebrew 
``` bash 
brew update brew install git python node uv brew install --cask docker 
 ```
  #### 2. Setup:
``` bash
git clone https://github.com/Arnasa1/Mesh.git
```
#### Backend
``` bash
cd Mesh/backend
uv sync
```
#### Frontend
``` bash
cd ../frontend
npm install
```
</details>

### Linux
<details>
<summary>Arch based installation</summary>

#### 1. Install core dependecies:
- #### bash 
``` bash
sudo pacman -Syu --needed git curl base-devel python python-pip nodejs npm docker docker-compose uv
```
#### 2. Setup:
``` bash
git clone https://github.com/Arnasa1/Mesh.git
```
#### Backend
``` bash
cd Mesh/backend
uv sync
```
#### Frontend
``` bash
cd ../frontend
npm install
```

</details>

<details>
<summary>NixOS installation </summary>

#### 1. Install core dependecies in /etc/nixos/configuration.nix
``` bash
  environment.systemPackages = with pkgs; [
    git
    uv
    python314
  ];
```
#### 2. Setup:
``` bash
git clone https://github.com/Arnasa1/Mesh.git
```
#### Backend
``` bash
cd Mesh
nix develop
cd backend
uv sync
```
#### Frontend
``` bash
cd ../frontend
npm install
```
</details>



## Repository configuration (some these changes are configurated in 'Development setup' section):
#### git clone cd mesh Backend cd backend

#### uv add fastapi "uvicorn[standard]" pydantic sqlalchemy alembic asyncpg redis uv add --dev pytest pytest-asyncio httpx Frontend cd ../frontend npm install Start the Infrastructure

### From the project root:

#### docker compose up -d

### Check that PostgreSQL and Redis are running:

#### docker compose ps Run the Application Backend cd backend uv run uvicorn app.main:app --reload Frontend

### In a separate terminal:

#### cd frontend npm run dev

### The Vite development server will display the local URL in the terminal.

#### Testing Backend cd backend uv run pytest Frontend cd frontend npm run test End-to-End Tests cd frontend npx playwright install npx playwright test


