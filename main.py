from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from pydantic import BaseModel
import os

app = FastAPI()

# Environment-based CORS configuration for both local and production
def get_cors_origins() -> List[str]:
    # Default origins for local development
    default_origins = [
        "http://localhost:3000",      # React default
        "http://localhost:3001",      # Alternative React port
        "http://localhost:8080",      # Vue default
        "http://localhost:8081",      # Alternative Vue port
        "http://127.0.0.1:3000",      # Local IP
        "http://127.0.0.1:8080",      # Local IP alternative
    ]
    
    # Get production origins from environment variable
    cors_origins = os.getenv("CORS_ORIGINS", "")
    if cors_origins:
        # Split comma-separated origins and clean them
        production_origins = [origin.strip() for origin in cors_origins.split(",")]
        # Combine production and development origins
        return production_origins + default_origins
    
    # Return only development origins if no env var is set
    return default_origins

# Apply CORS middleware with dynamic origins
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

@app.post("/pipelines/parse")
async def parse_pipeline(pipeline: PipelineData):
    nodes = pipeline.nodes
    edges = pipeline.edges

    num_nodes = len(nodes)
    num_edges = len(edges)

    # Build adjacency list
    graph = {node.id: [] for node in nodes}
    for edge in edges:
        graph[edge.source].append(edge.target)

    # DAG check using DFS
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
    for node in graph:
        if node not in visited:
            if is_cyclic(node):
                is_dag = False
                break

    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "is_dag": is_dag
    }
