from fastapi import FastAPI, Query
import psutil
import asyncio
import os

app = FastAPI()

@app.get("/metrics")
async def get_metrics(limit: int = Query(5, ge=1, le=50)):
    """Return system metrics and top processes.
    limit: number of processes to return (default 5, max 50).
    Honors FAST_TEST env var to skip delay in CI.
    """
    fast_test = os.getenv("FAST_TEST") == "1"
    sleep_time = 0 if fast_test else 0.05  # Reduced from 0.1 for faster responses

    # Prime overall CPU and per-process CPU counters
    cpu_percent = psutil.cpu_percent(interval=None)
    memory_percent = psutil.virtual_memory().percent

    procs = list(psutil.process_iter(['pid', 'name', 'status']))
    # Prime process cpu counters
    for p in procs:
        try:
            p.cpu_percent()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if sleep_time:
        await asyncio.sleep(sleep_time)

    processes = []
    for p in procs:
        try:
            processes.append({
                "pid": p.pid,
                "name": p.info.get('name'),
                "cpu": p.cpu_percent(),
                "memory": p.memory_percent(),
                "status": p.info.get('status')
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    top_processes = sorted(processes, key=lambda p: p['cpu'], reverse=True)[:limit]

    return {"cpu_percent": cpu_percent, "memory_percent": memory_percent, "processes": top_processes}
