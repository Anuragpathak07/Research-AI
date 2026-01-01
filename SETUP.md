# Setup Instructions

## Prerequisites

1. **Python 3.8+** installed
2. **Node.js 18+** and npm installed
3. **Ollama** installed and running (for LLM functionality)

## Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up Ollama (if not already installed):
   - Download from https://ollama.ai
   - Install and start Ollama
   - Pull a model (e.g., `ollama pull llama3.2`)

6. Set environment variables (optional):
   ```bash
   # Windows PowerShell
   $env:OLLAMA_BASE_URL="http://localhost:11434"
   $env:OLLAMA_MODEL="llama3.2"
   
   # macOS/Linux
   export OLLAMA_BASE_URL="http://localhost:11434"
   export OLLAMA_MODEL="llama3.2"
   ```

7. Run the backend server:
   ```bash
   python app.py
   ```
   
   The backend will run on **http://localhost:5005**

## Frontend Setup

1. Navigate to the project root:
   ```bash
   cd research-synthesis-suite
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   
   The frontend will run on **http://localhost:8080**

## Running the Application

1. **Start Ollama** (if using LLM features):
   ```bash
   ollama serve
   ```

2. **Start the backend** (in one terminal):
   ```bash
   cd backend
   python app.py
   ```

3. **Start the frontend** (in another terminal):
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to **http://localhost:8080**

## API Endpoints

The backend provides the following API endpoints:

- `POST /api/discover/` - Discover research papers from arXiv
- `POST /api/clusters/` - Cluster papers by topic
- `POST /api/synthesis/` - Generate literature synthesis
- `POST /api/gaps/` - Identify research gaps
- `POST /api/experiments/` - Generate experiment proposals

All endpoints are accessible via the Vite proxy at `/api/*` which routes to `http://localhost:5005/api/*`

## Troubleshooting

- **Backend not connecting**: Ensure the backend is running on port 5005
- **CORS errors**: The backend has CORS enabled for all origins in development
- **Ollama errors**: Make sure Ollama is running and the model is pulled
- **Frontend proxy issues**: Check that Vite is configured to proxy `/api` to `http://localhost:5005`

