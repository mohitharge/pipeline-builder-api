# Pipeline Backend API

A FastAPI backend service for parsing and analyzing pipeline data structures. This service validates pipeline configurations by checking for Directed Acyclic Graph (DAG) properties and provides basic statistics about the pipeline structure.

## Features

- **Pipeline Validation**: Validates that pipeline configurations form a valid DAG
- **Cycle Detection**: Uses depth-first search (DFS) to detect cycles in the pipeline
- **Pipeline Statistics**: Returns basic metrics about nodes and edges
- **CORS Support**: Configured for cross-origin requests during development

## API Endpoints

### POST `/pipelines/parse`

Parses and validates a pipeline configuration.

**Request Body:**
```json
{
  "nodes": [
    {
      "id": "node1",
      "type": "input",
      "data": {"name": "Input Node"}
    },
    {
      "id": "node2",
      "type": "process",
      "data": {"name": "Process Node"}
    }
  ],
  "edges": [
    {
      "source": "node1",
      "target": "node2"
    }
  ]
}
```

**Response:**
```json
{
  "num_nodes": 2,
  "num_edges": 1,
  "is_dag": true
}
```

## Data Models

### Node
- `id` (string): Unique identifier for the node
- `type` (string): Type/category of the node
- `data` (dict): Additional node configuration data

### Edge
- `source` (string): ID of the source node
- `target` (string): ID of the target node

### PipelineData
- `nodes` (List[Node]): List of all nodes in the pipeline
- `edges` (List[Edge]): List of all edges connecting nodes

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd pipeline-backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn pydantic
   ```

## Usage

### Development Server

Run the development server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, you can access:
- **Interactive API docs (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative API docs (ReDoc)**: `http://localhost:8000/redoc`

## Example Usage

### Using curl

```bash
curl -X POST "http://localhost:8000/pipelines/parse" \
  -H "Content-Type: application/json" \
  -d '{
    "nodes": [
      {"id": "start", "type": "input", "data": {"name": "Start"}},
      {"id": "process", "type": "transform", "data": {"name": "Process"}},
      {"id": "end", "type": "output", "data": {"name": "End"}}
    ],
    "edges": [
      {"source": "start", "target": "process"},
      {"source": "process", "target": "end"}
    ]
  }'
```

### Using Python requests

```python
import requests
import json

pipeline_data = {
    "nodes": [
        {"id": "start", "type": "input", "data": {"name": "Start"}},
        {"id": "process", "type": "transform", "data": {"name": "Process"}},
        {"id": "end", "type": "output", "data": {"name": "End"}}
    ],
    "edges": [
        {"source": "start", "target": "process"},
        {"source": "process", "target": "end"}
    ]
}

response = requests.post(
    "http://localhost:8000/pipelines/parse",
    json=pipeline_data
)

print(response.json())
```

## Algorithm Details

### DAG Validation

The service uses a depth-first search (DFS) algorithm with a recursion stack to detect cycles:

1. **Graph Construction**: Builds an adjacency list representation from the edges
2. **Cycle Detection**: For each unvisited node, performs DFS to detect back edges
3. **Recursion Stack**: Tracks nodes in the current recursion path to identify cycles

A pipeline is considered a valid DAG if no cycles are detected.

## Configuration

### CORS Settings

The current configuration allows all origins for development:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**⚠️ Production Warning**: Update `allow_origins` to specific domains in production for security.

## Production Deployment

### Environment Variables

Consider using environment variables for production configuration:
```python
import os

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
```

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Requirements File

Create `requirements.txt`:
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
```

## Testing

### Manual Testing

Test with a cyclic pipeline to verify cycle detection:
```json
{
  "nodes": [
    {"id": "a", "type": "node", "data": {}},
    {"id": "b", "type": "node", "data": {}},
    {"id": "c", "type": "node", "data": {}}
  ],
  "edges": [
    {"source": "a", "target": "b"},
    {"source": "b", "target": "c"},
    {"source": "c", "target": "a"}
  ]
}
```

Expected response: `{"num_nodes": 3, "num_edges": 3, "is_dag": false}`
