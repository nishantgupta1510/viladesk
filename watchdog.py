#!/usr/bin/env python3
"""
VilaDesk 24x7 Persistent Supervisor & Tunnel Watchdog
Ensures:
 1. VilaDesk python server (localhost:8080) is ALWAYS running.
 2. Cloudflare tunnel is ALWAYS connected.
 3. Automatically detects server crashes or Cloudflare tunnel expirations,
    restarts them, captures the live public HTTPS URL, and syncs config.json.
 4. Writes the current active URL to LIVE_DEMO_URL.txt.
"""

import os
import sys
import time
import json
import re
import subprocess
import signal
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
URL_FILE = os.path.join(BASE_DIR, "LIVE_DEMO_URL.txt")
LOG_FILE = os.path.join(BASE_DIR, "watchdog.log")

CLOUDFLARED_BIN = "/opt/homebrew/bin/cloudflared"
if not os.path.exists(CLOUDFLARED_BIN):
    CLOUDFLARED_BIN = "cloudflared"

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted, flush=True)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

def update_config_url(public_url):
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                cfg = json.load(f)
            cfg["public_base_url"] = public_url
            with open(CONFIG_FILE, "w") as f:
                json.dump(cfg, f, indent=2)
            log(f"Updated config.json with public_base_url: {public_url}")
        
        with open(URL_FILE, "w") as f:
            f.write(public_url.strip() + "\n")
    except Exception as e:
        log(f"Error updating config URL: {e}")

class Supervisor:
    def __init__(self):
        self.server_proc = None
        self.tunnel_proc = None
        self.public_url = None
        self.server_fail_count = 0
        self.running = True

    def is_server_healthy(self):
        try:
            req = urllib.request.Request("http://localhost:8080/api/config", headers={"User-Agent": "Watchdog/1.0"})
            with urllib.request.urlopen(req, timeout=10) as res:
                return res.status == 200
        except Exception:
            return False

    def start_server(self):
        log("Starting VilaDesk Python Server (port 8080)...")
        # Kill any orphan process on 8080
        os.system("lsof -ti:8080 | xargs kill -9 2>/dev/null")
        time.sleep(1)
        self.server_proc = subprocess.Popen(
            [sys.executable, os.path.join(BASE_DIR, "server.py")],
            cwd=BASE_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        time.sleep(1.5)
        if self.is_server_healthy():
            log("✓ VilaDesk Server is healthy and running on localhost:8080")
        else:
            log("⚠️ VilaDesk Server started, waiting for health check...")

    def start_tunnel(self):
        log("Starting Cloudflare 24x7 Public Tunnel...")
        # Kill existing cloudflared
        os.system("pkill -9 -f 'cloudflared tunnel' 2>/dev/null")
        time.sleep(1)

        self.tunnel_proc = subprocess.Popen(
            [CLOUDFLARED_BIN, "tunnel", "--url", "http://localhost:8080"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        # Read output line-by-line until public URL is captured
        url_found = None
        start_t = time.time()
        while time.time() - start_t < 25:
            line = self.tunnel_proc.stdout.readline()
            if not line:
                break
            # Match trycloudflare.com URL
            match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
            if match:
                url_found = match.group(0)
                break
            if "ERR" in line or "error" in line.lower():
                log(f"[Tunnel Log] {line.strip()}")

        if url_found:
            self.public_url = url_found
            log(f"============================================================")
            log(f"🎉 24x7 PUBLIC DEMO URL ESTABLISHED: {self.public_url}")
            log(f"   • Interactive Demo Hub: {self.public_url}/demo")
            log(f"   • Builder Proposal PPT: {self.public_url}/proposal")
            log(f"   • Guard Cabin App:      {self.public_url}/guard")
            log(f"   • Resident WhatsApp:    {self.public_url}/whatsapp")
            log(f"   • Night QR Kiosk:       {self.public_url}/kiosk")
            log(f"   • Master Map & Khata:   {self.public_url}/admin")
            log(f"============================================================")
            update_config_url(self.public_url)
        else:
            log("⚠️ Could not parse public URL within 25 seconds. Will retry in loop.")

    def run(self):
        log("VilaDesk 24x7 Watchdog Supervisor starting up...")
        self.start_server()
        self.start_tunnel()

        loop_count = 0
        while self.running:
            time.sleep(5)
            loop_count += 1

            # 1. Check Python Server with consecutive failure tolerance
            if not self.is_server_healthy():
                self.server_fail_count += 1
                log(f"⚠️ Health check missed ({self.server_fail_count}/3)...")
                if self.server_fail_count >= 3:
                    log("⚠️ VilaDesk Server failed 3 consecutive health checks! Restarting server...")
                    self.start_server()
                    self.server_fail_count = 0
            else:
                self.server_fail_count = 0

            # 2. Check Tunnel Process (ONLY restart if cloudflared actually died)
            if self.tunnel_proc is None or self.tunnel_proc.poll() is not None:
                log("⚠️ Cloudflare Tunnel process exited! Re-establishing tunnel...")
                self.start_tunnel()

            # Periodic status log every 60 seconds
            if loop_count % 12 == 0:
                log(f"✓ Health Check OK | Active Demo URL: {self.public_url or 'Connecting...'}")

if __name__ == "__main__":
    sup = Supervisor()
    try:
        sup.run()
    except KeyboardInterrupt:
        log("Watchdog stopped by user.")
