from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from pydantic import BaseModel
import os
import time

app = FastAPI()

# Environment-based CORS configuration for both local and production
def get_cors_origins() -> List[str]:
    default_origins = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8080",
        "http://localhost:8081",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
    ]
    
    cors_origins = os.getenv("CORS_ORIGINS", "")
    if cors_origins:
        production_origins = [origin.strip() for origin in cors_origins.split(",")]
        return production_origins + default_origins
    
    return default_origins

# Apply CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
)

# Pydantic models
class Node(BaseModel):
    id: str
    type: str
    data: dict

class Edge(BaseModel):
    source: str
    target: str

class PipelineData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

# Standardized API response
def build_response(success: bool, message: str, data: dict = {}, start_time: float = None):
    response_time = round((time.time() - start_time) * 1000, 2) if start_time else None
    return {
        "success": success,
        "message": message,
        "data": data,
        "response_time_ms": response_time,
    }

@app.post("/pipelines/parse")
async def parse_pipeline(pipeline: PipelineData):
    start_time = time.time()

    try:
        nodes = pipeline.nodes
        edges = pipeline.edges

        graph = {node.id: [] for node in nodes}
        for edge in edges:
            graph[edge.source].append(edge.target)

        # DAG check
        visited = set()
        rec_stack = set()

        def is_cyclic(v):
            visited.add(v)
            rec_stack.add(v)
            for neighbor in graph.get(v, []):
                if neighbor not in visited:
                    if is_cyclic(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(v)
            return False

        is_dag = True
        for node_id in graph:
            if node_id not in visited:
                if is_cyclic(node_id):
                    is_dag = False
                    break

        return build_response(
            success=True,
            message="Pipeline parsed successfully.",
            data={
                "num_nodes": len(nodes),
                "num_edges": len(edges),
                "is_dag": is_dag,
            },
            start_time=start_time
        )

    except Exception as e:
        return build_response(
            success=False,
            message=f"Error while parsing pipeline: {str(e)}",
            data={},
            start_time=start_time
        )
