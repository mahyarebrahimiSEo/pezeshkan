# -*- coding: utf-8 -*-
"""
High-Concurrency Production Server Runner & Multi-Worker Cluster
Pezeshkan Medical Ecosystem - Enterprise Performance Layer
Optimized for 3,000+ Concurrent Virtual Users (VUs) and High-Throughput Benchmarking.
Powered by Uvicorn ASGI with Windows IOCP (I/O Completion Ports), Keep-Alive, and SQLite WAL tuning.
"""

import os
import sys
import time
import argparse
import asyncio
import sqlite3
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Ensure settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

DEFAULT_CLUSTER_PORTS = [3000, 3001, 3002, 3003]


# Pre-tune SQLite database for massive concurrency (WAL Mode & 30s busy timeout)
def tune_sqlite():
    db_path = BASE_DIR / "data" / "pezeshkan.sqlite3"
    if db_path.exists():
        try:
            conn = sqlite3.connect(str(db_path), timeout=30.0)
            cur = conn.cursor()
            cur.execute("PRAGMA journal_mode=WAL;")
            cur.execute("PRAGMA synchronous=NORMAL;")
            cur.execute("PRAGMA busy_timeout=30000;")
            cur.execute("PRAGMA cache_size=-64000;")
            cur.execute("PRAGMA temp_store=MEMORY;")
            cur.execute("PRAGMA mmap_size=268435456;")  # 256MB memory-mapped I/O
            conn.commit()
            conn.close()
        except Exception:
            pass


def run_worker_instance(port, host="127.0.0.1"):
    tune_sqlite()

    import django
    django.setup()

    import asgiref.sync
    from concurrent.futures import ThreadPoolExecutor

    # Expand single_thread_executor to 64 parallel threads across CPU cores
    asgiref.sync.SyncToAsync.single_thread_executor = ThreadPoolExecutor(
        max_workers=64,
        thread_name_prefix=f"PezeshkanWorker_{port}"
    )

    # Pre-warm in-memory caches
    from django.core.cache import cache
    from apps.pezeshkan_core.models import Pillar, Doctor, Article, SubscriptionPlan
    from apps.pezeshkan_core.views import serve_static_file, load_site_images
    from django.conf import settings

    load_site_images()
    for name in ['portal/index.html', 'portal/packages.html', 'portal/appointments.html', 'mag/index.html']:
        p = settings.BASE_DIR / name
        if p.exists():
            serve_static_file(p)

    try:
        pillars = [p.to_dict() for p in Pillar.objects.all().order_by('id')]
        cache.set("api_pillars", pillars, 300)

        docs = [d.to_dict() for d in Doctor.objects.all().order_by('id')]
        cache.set("api_doctors", docs, 300)

        directory = {
            "results": [{
                "slug": d.get("customId") or f"doc-{d.get('id')}",
                "name": f"کلینیک {d.get('name')}",
                "doctor_name": d.get("name"),
                "specialty": d.get("dept"),
                "phone": d.get("phone") or "۰۲۱-۶۶۰۲۰۳۰۸",
                "address": d.get("address") or "تهران، ساختمان پزشکان فجر",
                "center_type": "solo" if not d.get("dept") or "کلینیک" not in d.get("dept") else "polyclinic",
            } for d in docs]
        }
        cache.set("api_clinic_directory", directory, 300)

        articles = [a.to_dict() for a in Article.objects.all().order_by('-id')]
        cache.set("api_articles_all", articles, 300)

        plans = list(SubscriptionPlan.objects.all().values())
        cache.set("api_platform_plans", plans, 300)
    except Exception:
        pass

    import uvicorn

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    uvicorn.run(
        "config.asgi:application",
        host=host,
        port=port,
        limit_concurrency=10000,
        backlog=8192,
        timeout_keep_alive=60,
        http="httptools",
        access_log=False,
        log_level="warning",
    )


def run_cluster_supervisor(ports=None, host="127.0.0.1"):
    if ports is None:
        ports = DEFAULT_CLUSTER_PORTS

    tune_sqlite()

    print("==================================================================")
    print(f"[Cluster] Pezeshkan High-Throughput Cluster Starting ({len(ports)} Workers)")
    for i, p in enumerate(ports, 1):
        role = "Primary / Browser" if i == 1 else "Load Balancing Worker"
        print(f"         Worker {i}: http://{host}:{p} ({role})")
    print(f"         Total Concurrency Capacity: {len(ports) * 10000:,} Connections")
    print("==================================================================")

    processes = []
    py_executable = sys.executable

    for p in ports:
        cmd = [py_executable, str(BASE_DIR / "run_server.py"), "--worker", str(p), "--host", host]
        proc = subprocess.Popen(cmd)
        processes.append((p, proc))

    try:
        while True:
            time.sleep(1)
            for p, proc in processes:
                if proc.poll() is not None:
                    print(f"[Warning] Worker on port {p} exited with code {proc.returncode}. Restarting...")
                    new_proc = subprocess.Popen([py_executable, str(BASE_DIR / "run_server.py"), "--worker", str(p), "--host", host])
                    processes.remove((p, proc))
                    processes.append((p, new_proc))
    except KeyboardInterrupt:
        print("\n[Cluster] Shutting down all worker processes gracefully...")
        for _, proc in processes:
            proc.terminate()
        for _, proc in processes:
            proc.wait()
        print("[Cluster] All workers terminated.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pezeshkan Concurrency Runner")
    parser.add_argument("--worker", type=int, default=None, help="Run single worker on given port")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host interface")
    parser.add_argument("--cluster", action="store_true", help="Run multi-worker cluster supervisor")
    args = parser.parse_args()

    if args.worker:
        run_worker_instance(args.worker, args.host)
    else:
        run_cluster_supervisor(host=args.host)
