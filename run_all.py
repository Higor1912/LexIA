import subprocess
import time

# Inicia o backend (FastAPI)
backend = subprocess.Popen(["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "3001"])

# Aguarda o backend subir antes de iniciar o frontend
time.sleep(2)

# Inicia o frontend (Flet Web)
frontend = subprocess.Popen(["python", "frontend/main.py"])

try:
    backend.wait()
    frontend.wait()
except KeyboardInterrupt:
    backend.terminate()
    frontend.terminate()