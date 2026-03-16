import subprocess
import time
from celery import Celery

# Cấu hình Celery kết nối tới Redis container
celery_app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@celery_app.task(bind=True)
def execute_code_task(self, execution_id, code):
    start_time = time.time()
    
    try:
        # Quan trọng: Đảm bảo các dòng dưới đây thụt lề 8 dấu cách (hoặc 2 lần tab)
        process = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=5,
            shell=False 
        )
        
        execution_time = int((time.time() - start_time) * 1000)
        
        return {
            "execution_id": execution_id,
            "status": "COMPLETED",
            "stdout": process.stdout,
            "stderr": process.stderr,
            "execution_time_ms": execution_time
        }

    except subprocess.TimeoutExpired:
        # Thụt lề phải khớp với khối try
        return {
            "execution_id": execution_id,
            "status": "TIMEOUT",
            "stderr": "Error: Execution exceeded time limit (5s).",
            "execution_time_ms": 5000
        }
    except Exception as e:
        return {
            "execution_id": execution_id,
            "status": "FAILED",
            "stderr": str(e)
        }