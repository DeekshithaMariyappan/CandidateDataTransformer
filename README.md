# Candidate Data Transformer

A full-stack application that intelligently extracts and merges candidate data from structured sources (CSV) and unstructured sources (PDF Resumes) using Ollama and Llama 3.2.

## Features

- **Multi-Source Extraction**: Parses CSV data and extracts information from unstructured PDF resumes using a local LLM.
- **Intelligent Merging & Conflict Resolution**: Automatically merges data from both sources based on priority rules and tracks conflict resolution decisions.
- **Provenance & Confidence Tracking**: Maintains a record of where each data point came from and calculates a confidence score.
- **Configurable Projection Layer**: Easily map the internal canonical profile to a custom JSON structure.
- **Modern React Dashboard**: A stunning, glassmorphism-inspired UI to visualize the transformation process.

## Prerequisites

1. **Python 3.8+**
2. **Node.js & npm**
3. **Ollama**: Installed and running locally.
   - Run `ollama pull llama3.2` to download the required model.

## Setup Instructions

### Backend (FastAPI)

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

### Frontend (React/Vite)

1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   The UI will be available at `http://localhost:5173`.

## Usage

1. Open the frontend in your browser.
2. Upload a recruiter CSV file (see `sample_data/recruiter.csv` for an example).
3. Upload a PDF resume.
4. (Optional) Upload a projection configuration JSON (see `configs/projection.json`).
5. Click **Generate Canonical Profile** and view the extracted data, conflict resolutions, and confidence scores!
