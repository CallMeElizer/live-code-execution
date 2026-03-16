from fastapi import FastAPI, HTTPException
from app.worker import execute_code_task, celery_app
from app.schemas import CodeUpdate, ExecutionResponse, ExecutionResult
import uuid

app = FastAPI(title="Code Execution API")

#gia lap databse trong bo nho
session_db= {}

@app.post("/code-sessions", response_model=ExecutionResponse)
async def create_session():
    session_id = str(uuid.uuid4())
    session_db[session_id] = {
        "language": "python",
        "source_code": ""
    }
    return {"session_id": session_id, "status": "ACTIVE"}

@app.patch("/code-sessions/{session_id}")
async def autosave_code(session_id: str, data: CodeUpdate):
    if session_id not in session_db:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_db[session_id].update({
        "source_code": data.source_code,
        "language": data.language
        })
    return{"session_id": session_id, "status": "ACTIVE"}

@app.post("/code-sessions/{session_id}/run")
async def run_code(session_id: str):
    if session_id not in session_db:
        raise HTTPException(status_code=404, detail="Session not found")

    code = session_db[session_id]["source_code"]
    lang = session_db[session_id]["language"]
    execution_id=str(uuid.uuid4())

    #gui task vao celery de thuc thi code
    execute_code_task.apply_async(args=[execution_id, code], task_id=execution_id)

    return{"execution_id": execution_id, "status": "QUEUED"}

@app.get("/executions/{execution_id}", response_model=ExecutionResult)
async def get_result(execution_id:str):
    res = celery_app.AsyncResult(execution_id)
    if res.state == "PENDING":
        return{"execution_id": execution_id, "status": "QUEUED"}
    elif res.state == "SUCCESS":
        return res.result
    elif res.state == "FAILURE":
        return{"execution_id": execution_id, "status": "FAILED", "stderr": "An error occurred during execution."}