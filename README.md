Live Code Execution System

Project Overview
The Live Code Execution system is built as take-home case for the Edtronaut Job Simulation platform. The system allows user to submit Python source code, execute it safely in an isolated environment, and receive immediate results.

Key features:
- Session Management: initializes unique work sessions for each user.
- AutoSave: automatically stores source code during drafting via the Patch API.
- Asynchronous Execution: Utilized a task queue to process code, ensuring a non-blocking system.
- Security and Safety: Implements a timeout mechanism to prevent inifinte loops and protect system resources.

System architecture:
The system follows a Producer-Consumer model:
- API (FastAPI): handles requests and manages session states.
- Message Broker (Redis): Orchestrates execution tasks.
- Worker (Celery): pulls code from the queue, runs it in a separate process and returns the results.

Installation Instruction:

Prerequistes:
Docker and Docker Compose installed

Setup Steps:
In the root directory of the project, run:

docker-compose up --build

Once the system is running:
API Documentation (Swagger UI): Access at http://localhost:8000/docs
Redis: Running on port 6379.

API Documentation:
- POST /code-sessions: Create a session.
- PATCH /code-sessions/{session_id}: AutoSave source code.
- POST /code-sessions/{session_id}/run: submit source code to the execution queue.
- GET /executions/{execution_id}: Retrieve execution results (stdout, stderr, execution_time).

Design Trade-offs:
- Celery+Redis: Chosen over direcct execution on the API to ensure scalability. As the user base grows, the number of worker containers can be increased.
- Timeout(5s): Limits code execution time to protect the server from DoS attacks or user logic errors.
- In-memory State: Used for rapid prototype demonstration. In a production environment, this would be upgraded to PostgeSQL for persistence.
