1. Archiitectural Patten
I have implemented an Asynchronous Worker Pattern using FastAPI, Redis and Celery.

Why?
Executing user-submitted code is a resource-intensive and unpredictable task.
- non-blocking API: if we executed code directly within FastAPI request-response cycle, a single long-running script or an infinite loop would hang the entire API server.
- decoupling: by using Redis as a message broker, the API only needs to handoff the task. The actual execution happens in a seperate environment allowing the API to remain responsive to other users.

2.Security and Resource Management
Running untrusted code poses significant risks. This system implements several safety layer:

Time Limiting(Timeout):
- Mechanism: Each execution is wrapped in a subprocess with a strict 5-second timeout.
- Protection: this prevents Denial of Service (DoS) attacks where a user might try to exhaust server CPU by running infinite loops.

Process isolation
- Mechanism: Code is executed using Python's subprocess module.
- Benefit: it seperates the user's execution environment from the main application process. Even if the user's code crashes, the Worker remains alive to handle the next task.

3.Scalability
The choice of Redis and Celery makes the system horizontally scalable:
- Scaling Workers: to handle higher traffic, we can simply increase the number of Worker containers in the docker-compose.yml without changing a single line of code.

4.Error handling strategy
The system categorized execution results into four distinct states:
- QUEUED/RUNNING: Task is waiting or currently being processed.
- COMPLETED: Successful execution -> return stdout
- FAILED: Code contains syntax errors or runtime exceptions -> return stderr
- TIMEOUT: Code exceeded the 5-second limit.
