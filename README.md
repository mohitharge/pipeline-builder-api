# Pipeline Backend API

A FastAPI backend service for parsing and analyzing pipeline data structures. This service validates pipeline configurations by checking for Directed Acyclic Graph (DAG) properties and provides detailed statistics about the pipeline structure with standardized responses.

## Features

- **Pipeline Validation**: Validates that pipeline configurations form a valid DAG
- **Cycle Detection**: Uses depth-first search (DFS) to detect cycles in the pipeline
- **Pipeline Statistics**: Returns comprehensive metrics about nodes and edges
- **Standardized Responses**: Consistent API response format with success status and timing
- **Environment-based CORS**: Flexible CORS configuration for development and production
- **Performance Monitoring**: Built-in response time tracking

## Live Deployment

- **Production API**: https://pipeline-builder-api.onrender.com
- **Frontend**: https://pipeline-builder-one.vercel.app

## API Endpoints

### POST `/pipelines/parse`

Parses and validates a pipeline configuration with enhanced response format.

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
  "success": true,
  "message": "Pipeline parsed successfully.",
  "data": {
    "num_nodes": 2,
    "num_edges": 1,
    "is_dag": true
  },
  "response_time_ms": 12.34
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Error while parsing pipeline: [error details]",
  "data": {},
  "response_time_ms": 5.67
}
```

---

## Installation

1. **Clone the repository:**
   ```bash
   git https://github.com/mohitharge/pipeline-builder-api
   cd pipeline-backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
---

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

---

## Usage

### Development Server

Run the development server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Production Server

The production server runs on Render with:
```bash
uvicorn main:app --host 0.0.0.0 --port 10000
```
---

## CORS Configuration

The API supports both development and production environments with automatic CORS configuration:

### Development Origins (Always Allowed)
- `http://localhost:3000` (React default)
- `http://localhost:3001` (Alternative React)
- `http://localhost:8080` (Vue default)
- `http://localhost:8081` (Alternative Vue)
- `http://127.0.0.1:3000` (Local IP)
- `http://127.0.0.1:8080` (Local IP alternative)

### Production Origins (Environment Variable)
Set the `CORS_ORIGINS` environment variable with comma-separated URLs:
```bash
CORS_ORIGINS=https://pipeline-builder-one.vercel.app,https://your-other-domain.com
```

## Example Usage

### Using curl

```bash
curl -X POST "https://pipeline-builder-api.onrender.com//pipelines/parse" \
  -H "Content-Type: application/json" \
  -H "Origin: https://pipeline-builder-one.vercel.app" \
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
    "https://pipeline-builder-api.onrender.com//pipelines/parse",
    json=pipeline_data,
    headers={"Origin": "https://pipeline-builder-one.vercel.app"}
)

result = response.json()
print(f"Success: {result['success']}")
print(f"Message: {result['message']}")
print(f"Data: {result['data']}")
print(f"Response Time: {result['response_time_ms']}ms")
```

### Using JavaScript (Frontend)

```javascript
const API_BASE_URL = 'https://pipeline-builder-api.onrender.com/';

async function parsePipeline(pipelineData) {
  try {
    const response = await fetch(`${API_BASE_URL}/pipelines/parse`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(pipelineData)
    });
    
    const result = await response.json();
    
    if (result.success) {
      console.log('Pipeline Analysis:', result.data);
      console.log(`Processed in ${result.response_time_ms}ms`);
    } else {
      console.error('Error:', result.message);
    }
    
    return result;
  } catch (error) {
    console.error('Network Error:', error);
  }
}

// Example usage
parsePipeline({
  nodes: [
    { id: 'node1', type: 'input', data: { name: 'Input' } },
    { id: 'node2', type: 'output', data: { name: 'Output' } }
  ],
  edges: [
    { source: 'node1', target: 'node2' }
  ]
});
```

## Response Format

All API responses follow a standardized format:

```typescript
interface APIResponse {
  success: boolean;           // Operation success status
  message: string;           // Human-readable message
  data: object;              // Response data (varies by endpoint)
  response_time_ms: number;  // Processing time in milliseconds
}
```

## Algorithm Details

### DAG Validation

The service uses a depth-first search (DFS) algorithm with a recursion stack to detect cycles:

1. **Graph Construction**: Builds an adjacency list representation from the edges
2. **Cycle Detection**: For each unvisited node, performs DFS to detect back edges
3. **Recursion Stack**: Tracks nodes in the current recursion path to identify cycles

A pipeline is considered a valid DAG if no cycles are detected.

### Performance Tracking

Each request includes timing information:
- Start time recorded at request beginning
- End time calculated at response generation
- Response time included in milliseconds

## Production Deployment

### Render Configuration

The service is deployed on Render with the following configuration:
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
- **Port**: `10000`
- **Environment Variables**: `CORS_ORIGINS=https://pipeline-builder-one.vercel.app`

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `CORS_ORIGINS` | Comma-separated list of allowed origins | `https://pipeline-builder-one.vercel.app,https://example.com` |
| `ENVIRONMENT` | Deployment environment | `production` or `development` |

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
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

Test with a valid DAG:
```json
{
  "nodes": [
    {"id": "a", "type": "input", "data": {"name": "Start"}},
    {"id": "b", "type": "process", "data": {"name": "Middle"}},
    {"id": "c", "type": "output", "data": {"name": "End"}}
  ],
  "edges": [
    {"source": "a", "target": "b"},
    {"source": "b", "target": "c"}
  ]
}
```

Test with a cyclic pipeline:
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

Expected response: `{"success": true, "data": {"is_dag": false}, ...}`

### Load Testing

Test API performance:
```bash
# Simple load test
for i in {1..10}; do
  curl -X POST "https://pipeline-builder-api.onrender.com//pipelines/parse" \
    -H "Content-Type: application/json" \
    -d '{"nodes": [{"id": "test", "type": "input", "data": {}}], "edges": []}' &
done
```

## Error Handling

The API includes comprehensive error handling:
- **Validation Errors**: Invalid request format or missing fields
- **Processing Errors**: Issues during pipeline analysis
- **System Errors**: Internal server errors

All errors return the standardized response format with `success: false`.

## Performance Considerations

- **Response Time Tracking**: Each request includes processing time
- **Memory Efficient**: Uses DFS for cycle detection (O(V + E) complexity)
- **Render Free Tier**: Service may sleep after 15 minutes of inactivity
