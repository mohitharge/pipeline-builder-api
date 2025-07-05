from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from pydantic import BaseModel

app = FastAPI()

# Allow frontend requests (dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in prod
    allow_methods=["*"],
    allow_headers=["*"],
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
