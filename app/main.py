from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
from typing import Dict

# Import files
from .worker import execute_code_task, celery_app
from .schemas import CodeUpdate, ExecutionResponse, ExecutionResult

app = FastAPI(title="Edtronaut Code Execution API")

# Cors used for allowing frontend to call backend api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# in-memory database to store code sessions
session_db = {}

@app.post("/code-sessions", response_model=ExecutionResponse)
async def create_session():
    session_id = str(uuid.uuid4())
    session_db[session_id] = {
        "language": "python",
        "source_code": ""
    }
    # demonstrate session creation
    return {"session_id": session_id, "status": "ACTIVE"}

@app.patch("/code-sessions/{session_id}")
async def autosave_code(session_id: str, data: CodeUpdate):
    if session_id not in session_db:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_db[session_id].update({
        "source_code": data.source_code,
        "language": data.language
    })
    return {"session_id": session_id, "status": "SAVED"}

@app.post("/code-sessions/{session_id}/run")
async def run_code(session_id: str):
    if session_id not in session_db:
        raise HTTPException(status_code=404, detail="Session not found")

    code = session_db[session_id]["source_code"]
    execution_id = str(uuid.uuid4())

    # store execution_id in session_db for later retrieval
    # use celery to execute code asynchronously
    execute_code_task.apply_async(args=[execution_id, code], task_id=execution_id)

    return {"execution_id": execution_id, "status": "QUEUED"}

@app.get("/executions/{execution_id}", response_model=ExecutionResult)
async def get_result(execution_id: str):
    # use celery's AsyncResult to check the status of the task
    res = celery_app.AsyncResult(execution_id)
    
    if res.state == "PENDING" or res.state == "STARTED":
        return {
            "execution_id": execution_id, 
            "status": "RUNNING", 
            "stdout": "", 
            "stderr": "", 
            "execution_time_ms": 0
        }
    elif res.state == "SUCCESS":
        # return the result of the execution
        return res.result
    else:
        # state is either FAILURE or something else, return error response
        return {
            "execution_id": execution_id, 
            "status": "FAILED", 
            "stdout": "", 
            "stderr": "An error occurred during execution.", 
            "execution_time_ms": 0
        }