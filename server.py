#!/usr/bin/env python3
"""
VilaDesk Server (Production Pilot Ready)
Features:
- Dual-Mode Gatekeeping (Guard Lite PWA + Guardless Night QR Kiosk)
- Meta WhatsApp Business Cloud API Webhook Integration (Verification & Interactive Button Listener)
- Outbound Interactive WhatsApp Dispatch (via Meta Cloud API)
- Fallback Internal Simulation for testing
- JSON REST API for Plots, Visitors, Passes, and Logs
"""

import http.server
import socketserver
import json
import sqlite3
import os
import uuid
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

PORT = int(os.environ.get("PORT", 8080))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
DB_PATH = os.path.join(BASE_DIR, "viladesk.db")
STATIC_DIR = os.path.join(BASE_DIR, "static")

def load_config():
    cfg = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                cfg = json.load(f)
        except Exception as e:
            print(f"Error loading config.json: {e}")
    if not cfg:
        cfg = {
            "society_name": "Defined World City",
            "locality": "Narsinghpura, Ajmer Road, NH-8, Jaipur, 302026",
            "public_base_url": "http://localhost:8080",
            "guard_contact": {
                "phone": "8947051629",
                "name": "Gate 1 Guard Cabin",
                "alternate_phone": ""
            },
            "whatsapp": {
                "enabled": False,
                "api_version": "v18.0",
                "phone_number_id": "",
                "access_token": "",
                "verify_token": "viladesk_secret_verify_token_2026"
            }
        }
    # Auto-detect Cloud host URL (Render, Railway, Fly.io, etc.)
    env_url = os.environ.get("RENDER_EXTERNAL_URL") or os.environ.get("RAILWAY_STATIC_URL") or os.environ.get("PUBLIC_URL")
    if env_url:
        if not env_url.startswith("http"):
            env_url = f"https://{env_url}"
        cfg["public_base_url"] = env_url.rstrip("/")
    if os.environ.get("WHATSAPP_ACCESS_TOKEN"):
        cfg.setdefault("whatsapp", {})["access_token"] = os.environ.get("WHATSAPP_ACCESS_TOKEN")
        cfg["whatsapp"]["enabled"] = True
    if os.environ.get("WHATSAPP_PHONE_NUMBER_ID"):
        cfg.setdefault("whatsapp", {})["phone_number_id"] = os.environ.get("WHATSAPP_PHONE_NUMBER_ID")
    if os.environ.get("WHATSAPP_VERIFY_TOKEN"):
        cfg.setdefault("whatsapp", {})["verify_token"] = os.environ.get("WHATSAPP_VERIFY_TOKEN")
    return cfg

def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)

def ensure_db():
    if not os.path.exists(DB_PATH) or os.path.getsize(DB_PATH) == 0:
        print("[Database] Initializing fresh database from schema.sql...")
        conn = sqlite3.connect(DB_PATH)
        schema_file = os.path.join(BASE_DIR, "schema.sql")
        if os.path.exists(schema_file):
            with open(schema_file, "r") as f:
                conn.executescript(f.read())
        conn.close()
        try:
            import seed_data
            seed_data.seed_database()
        except Exception as e:
            print(f"[Database Seed Error] {e}")

ensure_db()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------------------------------------------------------
# Real Meta WhatsApp Cloud API Dispatcher
# -----------------------------------------------------------------------------
def dispatch_real_meta_whatsapp(to_phone, visitor_data):
    cfg = load_config()
    wa = cfg.get("whatsapp", {})
    if not wa.get("enabled") or not wa.get("access_token") or not wa.get("phone_number_id"):
        return {"dispatched": False, "reason": "Meta WhatsApp credentials not configured. Using simulator."}

    # Format phone number with country code (91 for India)
    clean_phone = "".join(filter(str.isdigit, str(to_phone)))
    if len(clean_phone) == 10:
        clean_phone = "91" + clean_phone

    api_url = f"https://graph.facebook.com/{wa.get('api_version', 'v18.0')}/{wa.get('phone_number_id')}/messages"
    
    vis_name = visitor_data.get("visitor_name", "Visitor")
    company = visitor_data.get("service_company") or visitor_data.get("visitor_type", "Guest")
    plot_num = visitor_data.get("plot_number", "--")
    vis_id = visitor_data.get("id")
    guard_phone = cfg.get("guard_contact", {}).get("phone", "8947051629")

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": clean_phone,
        "type": "interactive",
        "interactive": {
            "header": {
                "type": "text",
                "text": f"🔔 गेट सूचना / Gate Alert ({cfg.get('society_name')})"
            },
            "body": {
                "text": f"नमस्कार! आपके विला Plot {plot_num} पर आगंतुक आए हैं:\n\n"
                        f"👤 आगंतुक: {vis_name} ({company})\n"
                        f"⏰ समय: {datetime.now().strftime('%I:%M %p')}\n"
                        f"📍 चैनल: {visitor_data.get('entry_channel', 'gate')}\n"
                        f"📞 गार्ड संपर्क / Guard: +91 {guard_phone}\n\n"
                        f"क्या आप इन्हें प्रवेश की अनुमति देते हैं?"
            },
            "footer": {
                "text": "VilaDesk • Smart Gated Security"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": f"APPROVE_{vis_id}",
                            "title": "✅ Allow Entry"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": f"DENY_{vis_id}",
                            "title": "❌ Deny Entry"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": f"LEAVE_GATE_{vis_id}",
                            "title": "📦 Leave at Gate"
                        }
                    }
                ]
            }
        }
    }

    try:
        req = urllib.request.Request(
            api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {wa.get('access_token')}",
                "Content-Type": "application/json"
            }
        )
        with urllib.request.urlopen(req) as res:
            res_body = json.loads(res.read().decode("utf-8"))
            print(f"[Meta WhatsApp] Outbound message sent to {clean_phone}: {res_body}")
            return {"dispatched": True, "meta_response": res_body}
    except urllib.error.HTTPError as e:
        err_text = e.read().decode("utf-8")
        print(f"[Meta WhatsApp HTTPError {e.code}] Destination {clean_phone}: {err_text}")
        try:
            err_json = json.loads(err_text)
            err_code = err_json.get("error", {}).get("code")
            err_msg = err_json.get("error", {}).get("message")
            if err_code == 190:
                print("[Meta WhatsApp Notice] Temporary Access Token has expired. Please click 'Generate token' on Meta Developer Console.")
            elif err_code == 131030:
                print(f"[Meta WhatsApp Notice] Recipient {clean_phone} is not in Meta Allowed Recipient List. Add number to Step 1 allowed list.")
            return {"dispatched": False, "error_code": err_code, "error_message": err_msg, "details": err_json}
        except Exception:
            return {"dispatched": False, "error": err_text}
    except Exception as e:
        print(f"[Meta WhatsApp Error] Outbound failed: {e}")
        return {"dispatched": False, "error": str(e)}


class VilaDeskHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path
        query = urllib.parse.parse_qs(url.query)

        # 1. Meta Webhook Verification Challenge (GET /api/whatsapp/webhook)
        if path == "/api/whatsapp/webhook":
            mode = query.get("hub.mode", [""])[0]
            token = query.get("hub.verify_token", [""])[0]
            challenge = query.get("hub.challenge", [""])[0]
            cfg = load_config()
            expected_token = cfg.get("whatsapp", {}).get("verify_token", "viladesk_secret_verify_token_2026")

            if mode == "subscribe" and token == expected_token:
                print(f"[Meta Webhook] Successfully verified challenge from Meta!")
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(challenge.encode("utf-8"))
                return
            else:
                print(f"[Meta Webhook Verification FAILED] Received token '{token}', expected '{expected_token}'")
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"Forbidden")
                return

        # 2. Frontend Page Routing
        if path in ["/", "/demo"]:
            return self.serve_file("demo.html")
        elif path == "/proposal":
            return self.serve_file("proposal.html")
        elif path in ["/download/proposal-deck", "/VilaDesk_Builder_Proposal_Deck.pptx"]:
            return self.serve_binary_file("VilaDesk_Builder_Proposal_Deck.pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation")
        elif path == "/admin":
            return self.serve_file("admin.html")
        elif path == "/guard":
            return self.serve_file("guard.html")
        elif path == "/kiosk":
            return self.serve_file("kiosk.html")
        elif path == "/whatsapp":
            return self.serve_file("resident_whatsapp.html")
        elif path == "/print-board":
            return self.serve_file("print_gate_board.html")
        elif path in ["/join", "/register"]:
            return self.serve_file("register.html")
        elif path == "/privacy":
            return self.serve_file("privacy.html")

        # 3. API Endpoints
        if path.startswith("/api/"):
            return self.handle_api_get(path, query)

        # 4. Static files
        super().do_GET()

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path

        # 1. Meta Webhook Incoming Button Reply Listener (POST /api/whatsapp/webhook)
        if path == "/api/whatsapp/webhook":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            try:
                body = json.loads(post_data.decode("utf-8")) if post_data else {}
            except json.JSONDecodeError:
                body = {}
            return self.handle_meta_webhook_post(body)

        # 2. General API POST
        if path.startswith("/api/"):
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            try:
                body = json.loads(post_data.decode("utf-8")) if post_data else {}
            except json.JSONDecodeError:
                body = {}
            return self.handle_api_post(path, body)

        self.send_error(404, "Not Found")

    def serve_file(self, filename):
        file_path = os.path.join(STATIC_DIR, filename)
        if not os.path.exists(file_path):
            self.send_error(404, f"File {filename} not found")
            return
        
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        with open(file_path, "rb") as f:
            self.wfile.write(f.read())

    def serve_binary_file(self, filename, content_type):
        file_path = os.path.join(BASE_DIR, filename)
        if not os.path.exists(file_path):
            file_path = os.path.join(STATIC_DIR, filename)
        if not os.path.exists(file_path):
            self.send_error(404, f"File {filename} not found")
            return
        
        with open(file_path, "rb") as f:
            content = f.read()

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def send_json(self, data, status=200):
        response_bytes = json.dumps(data, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # -------------------------------------------------------------------------
    # Meta Webhook Processor (Handles real button clicks on WhatsApp!)
    # -------------------------------------------------------------------------
    def handle_meta_webhook_post(self, body):
        print(f"[Meta Webhook POST] Received payload: {json.dumps(body)}")
        try:
            entries = body.get("entry", [])
            for entry in entries:
                changes = entry.get("changes", [])
                for change in changes:
                    val = change.get("value", {})
                    messages = val.get("messages", [])
                    for msg in messages:
                        if msg.get("type") == "interactive":
                            btn_reply = msg.get("interactive", {}).get("button_reply", {})
                            btn_id = btn_reply.get("id", "")
                            print(f"[Meta Webhook] Resident tapped button: {btn_id}")

                            # Button IDs formatted as: APPROVE_vis_123, DENY_vis_123, LEAVE_GATE_vis_123
                            if "_" in btn_id:
                                action_part, vis_id = btn_id.split("_", 1)
                                action = "approve" if action_part == "APPROVE" else ("deny" if action_part == "DENY" else "leave_at_gate")
                                
                                conn = get_db()
                                cursor = conn.cursor()
                                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                                if action == "approve":
                                    cursor.execute("UPDATE visitors SET status = 'inside', approval_source = 'meta_whatsapp', entry_time = ? WHERE id = ?", (now_str, vis_id))
                                elif action == "deny":
                                    cursor.execute("UPDATE visitors SET status = 'denied', approval_source = 'meta_whatsapp' WHERE id = ?", (vis_id,))
                                elif action == "leave_at_gate":
                                    cursor.execute("UPDATE visitors SET status = 'leave_at_gate', approval_source = 'meta_leave_gate', exit_time = ? WHERE id = ?", (now_str, vis_id))

                                conn.commit()
                                conn.close()
                                print(f"[Meta Webhook] Visitor {vis_id} successfully updated to status: {action}")

        except Exception as e:
            print(f"[Meta Webhook Error] Failed to parse: {e}")

        # Meta requires an immediate 200 OK
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"EVENT_RECEIVED")

    # -------------------------------------------------------------------------
    # GET API Routes
    # -------------------------------------------------------------------------
    def handle_api_get(self, path, query):
        conn = get_db()
        cursor = conn.cursor()

        try:
            if path == "/api/config":
                cfg = load_config()
                # Mask sensitive token in response
                safe_cfg = json.loads(json.dumps(cfg))
                if safe_cfg.get("whatsapp", {}).get("access_token"):
                    safe_cfg["whatsapp"]["access_token"] = safe_cfg["whatsapp"]["access_token"][:6] + "..." + safe_cfg["whatsapp"]["access_token"][-4:]
                return self.send_json({"success": True, "config": safe_cfg})

            elif path == "/api/plots":
                cursor.execute("""
                    SELECT p.*, s.name as society_name 
                    FROM plots p 
                    JOIN societies s ON p.society_id = s.id 
                    ORDER BY CAST(p.plot_number AS INTEGER) ASC
                """)
                rows = [dict(r) for r in cursor.fetchall()]
                return self.send_json({"success": True, "plots": rows})

            elif path == "/api/visitors/active":
                cursor.execute("""
                    SELECT v.*, p.plot_number, p.street_name, p.owner_name, p.tenant_name, p.active_contact,
                           CASE WHEN p.active_contact = 'tenant' THEN p.tenant_phone ELSE p.owner_phone END as resident_phone,
                           CASE WHEN p.active_contact = 'tenant' THEN p.tenant_name ELSE p.owner_name END as resident_name
                    FROM visitors v
                    JOIN plots p ON v.plot_id = p.id
                    WHERE v.status IN ('pending', 'inside')
                    ORDER BY v.created_at DESC
                """)
                rows = [dict(r) for r in cursor.fetchall()]
                return self.send_json({"success": True, "active_visitors": rows})

            elif path == "/api/visitors/history":
                cursor.execute("""
                    SELECT v.*, p.plot_number, p.street_name,
                           CASE WHEN p.active_contact = 'tenant' THEN p.tenant_name ELSE p.owner_name END as resident_name
                    FROM visitors v
                    JOIN plots p ON v.plot_id = p.id
                    ORDER BY v.created_at DESC LIMIT 50
                """)
                rows = [dict(r) for r in cursor.fetchall()]
                return self.send_json({"success": True, "history": rows})

            elif path.startswith("/api/visitors/status/"):
                visitor_id = path.replace("/api/visitors/status/", "")
                cursor.execute("""
                    SELECT v.*, p.plot_number 
                    FROM visitors v
                    JOIN plots p ON v.plot_id = p.id
                    WHERE v.id = ?
                """, (visitor_id,))
                row = cursor.fetchone()
                if not row:
                    return self.send_json({"success": False, "error": "Visitor not found"}, 404)
                return self.send_json({"success": True, "visitor": dict(row)})

            elif path == "/api/whatsapp/feed":
                target_plot = query.get("plot_number", [None])[0]
                sql = """
                    SELECT v.*, p.plot_number, p.street_name,
                           CASE WHEN p.active_contact = 'tenant' THEN p.tenant_name ELSE p.owner_name END as resident_name,
                           CASE WHEN p.active_contact = 'tenant' THEN p.tenant_phone ELSE p.owner_phone END as resident_phone
                    FROM visitors v
                    JOIN plots p ON v.plot_id = p.id
                    WHERE v.status = 'pending'
                """
                params = []
                if target_plot:
                    sql += " AND p.plot_number = ?"
                    params.append(target_plot)
                sql += " ORDER BY v.created_at DESC"
                cursor.execute(sql, params)
                rows = [dict(r) for r in cursor.fetchall()]
                return self.send_json({"success": True, "pending_notifications": rows})

            else:
                return self.send_json({"error": "Endpoint not found"}, 404)
        finally:
            conn.close()

    # -------------------------------------------------------------------------
    # POST API Routes
    # -------------------------------------------------------------------------
    def handle_api_post(self, path, body):
        conn = get_db()
        cursor = conn.cursor()

        try:
            # POST /api/config/update -> Update Meta WhatsApp credentials & society settings
            if path == "/api/config/update":
                cfg = load_config()
                if "whatsapp" in body:
                    cfg["whatsapp"].update(body["whatsapp"])
                if "public_base_url" in body:
                    cfg["public_base_url"] = body["public_base_url"]
                if "society_name" in body:
                    cfg["society_name"] = body["society_name"]
                if "guard_contact" in body:
                    if "guard_contact" not in cfg:
                        cfg["guard_contact"] = {}
                    cfg["guard_contact"].update(body["guard_contact"])
                save_config(cfg)
                return self.send_json({"success": True, "message": "Configuration updated successfully"})

            # POST /api/plots/register -> Self-service registration by resident
            elif path == "/api/plots/register":
                plot_num = str(body.get("plot_number", "")).strip()
                name = str(body.get("name", "")).strip()
                phone = str(body.get("phone", "")).strip()
                occupancy = str(body.get("occupancy", "owner_staying")).strip()
                street = "Main Avenue"
                area = float(body.get("plot_area_sq_yd", 250))
                family_members = body.get("family_members", [])
                family_json = json.dumps(family_members)
                
                if not plot_num or not name or not phone:
                    return self.send_json({"success": False, "error": "Plot number, Name, and Phone are required"}, 400)

                cursor.execute("SELECT id FROM plots WHERE plot_number = ?", (plot_num,))
                existing = cursor.fetchone()
                
                plot_type = 'vacant_plot' if occupancy == 'vacant_plot' else 'occupied_villa'
                active_contact = 'tenant' if occupancy == 'tenant_rented' else 'owner'
                owner_name = name if occupancy != 'tenant_rented' else (body.get("owner_name") or "Owner")
                owner_phone = phone if occupancy != 'tenant_rented' else (body.get("owner_phone") or "")
                tenant_name = name if occupancy == 'tenant_rented' else None
                tenant_phone = phone if occupancy == 'tenant_rented' else None

                if existing:
                    cursor.execute("""
                        UPDATE plots 
                        SET street_name = ?, plot_type = ?, occupancy_status = ?,
                            owner_name = COALESCE(?, owner_name), owner_phone = COALESCE(?, owner_phone),
                            tenant_name = ?, tenant_phone = ?, active_contact = ?, family_members_json = ?
                        WHERE plot_number = ?
                    """, (street, plot_type, occupancy, owner_name, owner_phone, tenant_name, tenant_phone, active_contact, family_json, plot_num))
                    plot_id = existing["id"]
                else:
                    plot_id = f"plot_{plot_num}"
                    cursor.execute("""
                        INSERT INTO plots (id, society_id, plot_number, street_name, plot_type, plot_area_sq_yd, 
                                           occupancy_status, owner_name, owner_phone, tenant_name, tenant_phone, active_contact, family_members_json)
                        VALUES (?, 'soc_jaipur_01', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (plot_id, plot_num, street, plot_type, area, occupancy, owner_name or name, owner_phone or phone, tenant_name, tenant_phone, active_contact, family_json))

                cursor.execute("SELECT COUNT(*) as count FROM plots")
                total_cnt = cursor.fetchone()["count"]
                cursor.execute("UPDATE societies SET total_plots = ? WHERE id = 'soc_jaipur_01'", (total_cnt,))

                conn.commit()
                return self.send_json({
                    "success": True, 
                    "message": f"Villa Plot {plot_num} registered successfully!",
                    "plot_number": plot_num,
                    "resident_name": name,
                    "phone": phone,
                    "family_members_count": len(family_members)
                })

            # POST /api/plots/delete -> Admin deletes a plot
            elif path == "/api/plots/delete":
                plot_id = body.get("plot_id")
                cursor.execute("DELETE FROM visitors WHERE plot_id = ?", (plot_id,))
                cursor.execute("DELETE FROM gate_passes WHERE plot_id = ?", (plot_id,))
                cursor.execute("DELETE FROM plots WHERE id = ?", (plot_id,))
                conn.commit()
                return self.send_json({"success": True, "message": "Plot deleted successfully"})

            # POST /api/visitors/request -> Create entry request
            elif path == "/api/visitors/request":
                plot_num = str(body.get("plot_number", "")).strip()
                visitor_name = body.get("visitor_name", "Visitor").strip()
                raw_vphone = str(body.get("visitor_phone", "")).strip()
                clean_vphone = "".join(filter(str.isdigit, raw_vphone))
                
                # Strict phone validation (mandatory 10 digits)
                if not clean_vphone or len(clean_vphone) < 10:
                    return self.send_json({
                        "success": False, 
                        "error": "आगंतुक का 10-अंकों का वैध मोबाइल नंबर अनिवार्य है (Valid 10-digit visitor mobile number is mandatory)"
                    }, 400)
                visitor_phone = clean_vphone[-10:]

                visitor_type = body.get("visitor_type", "guest")
                service_company = body.get("service_company", "")
                vehicle_number = body.get("vehicle_number", "")
                entry_channel = body.get("entry_channel", "guard_app")
                
                cursor.execute("SELECT * FROM plots WHERE plot_number = ?", (plot_num,))
                plot = cursor.fetchone()
                if not plot:
                    return self.send_json({"success": False, "error": f"Plot {plot_num} does not exist"}, 400)

                plot_id = plot["id"]
                society_id = plot["society_id"]
                visitor_id = f"vis_{uuid.uuid4().hex[:10]}"

                cursor.execute("""
                    INSERT INTO visitors (id, society_id, plot_id, visitor_name, visitor_phone, 
                                          vehicle_number, visitor_type, service_company, entry_channel, 
                                          status, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', CURRENT_TIMESTAMP)
                """, (visitor_id, society_id, plot_id, visitor_name, visitor_phone, 
                      vehicle_number, visitor_type, service_company, entry_channel))

                cursor.execute("""
                    INSERT INTO event_logs (id, society_id, event_type, description, metadata_json)
                    VALUES (?, ?, 'visitor_requested', ?, ?)
                """, (str(uuid.uuid4()), society_id, 
                      f"New visitor request for Plot {plot_num}: {visitor_name} ({visitor_type})",
                      json.dumps({"visitor_id": visitor_id, "plot": plot_num, "channel": entry_channel})))

                conn.commit()

                # Multi-recipient collection: Primary Resident + All Family Members
                recipients = []
                res_name = plot["tenant_name"] if plot["active_contact"] == "tenant" else plot["owner_name"]
                res_phone = plot["tenant_phone"] if plot["active_contact"] == "tenant" else plot["owner_phone"]
                if res_phone:
                    recipients.append({"name": res_name, "phone": res_phone, "type": "primary"})

                fam_raw = plot["family_members_json"] if ("family_members_json" in plot.keys() and plot["family_members_json"]) else "[]"
                try:
                    fam_list = json.loads(fam_raw)
                    for f in fam_list:
                        f_phone = f.get("phone", "").strip()
                        if f_phone:
                            recipients.append({"name": f.get("name", "Family"), "phone": f_phone, "type": f.get("relation", "family")})
                except Exception as e:
                    pass

                # Dispatch Real Meta WhatsApp Messages to ALL registered family members
                meta_dispatches = []
                for r in recipients:
                    m_res = dispatch_real_meta_whatsapp(r["phone"], {
                        "id": visitor_id,
                        "visitor_name": visitor_name,
                        "visitor_type": visitor_type,
                        "service_company": service_company,
                        "plot_number": plot_num,
                        "entry_channel": entry_channel
                    })
                    meta_dispatches.append({"name": r["name"], "phone": r["phone"], "result": m_res})

                return self.send_json({
                    "success": True,
                    "visitor_id": visitor_id,
                    "status": "pending",
                    "plot_number": plot_num,
                    "primary_resident": res_name,
                    "resident_name": res_name,
                    "resident_phone": res_phone,
                    "dispatched_to_count": len(recipients),
                    "dispatches": meta_dispatches,
                    "message": f"WhatsApp notification dispatched to {len(recipients)} resident(s) for Plot {plot_num}"
                })

            # POST /api/visitors/action -> Manual or Simulated action
            elif path == "/api/visitors/action":
                visitor_id = body.get("visitor_id")
                action = body.get("action")
                source = body.get("source", "whatsapp_button")

                cursor.execute("SELECT v.*, p.plot_number FROM visitors v JOIN plots p ON v.plot_id = p.id WHERE v.id = ?", (visitor_id,))
                visitor = cursor.fetchone()
                if not visitor:
                    return self.send_json({"success": False, "error": "Visitor not found"}, 404)

                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if action == "approve":
                    new_status = "inside"
                    cursor.execute("""
                        UPDATE visitors 
                        SET status = ?, approval_source = ?, entry_time = ?
                        WHERE id = ?
                    """, (new_status, source, now_str, visitor_id))
                    event_desc = f"Visitor {visitor['visitor_name']} approved for Plot {visitor['plot_number']} via {source}."
                elif action == "deny":
                    new_status = "denied"
                    cursor.execute("UPDATE visitors SET status = ?, approval_source = ? WHERE id = ?", (new_status, source, visitor_id))
                    event_desc = f"Visitor {visitor['visitor_name']} denied entry for Plot {visitor['plot_number']}."
                elif action == "leave_at_gate":
                    new_status = "leave_at_gate"
                    cursor.execute("UPDATE visitors SET status = ?, approval_source = ?, exit_time = ? WHERE id = ?", (new_status, "leave_at_gate", now_str, visitor_id))
                    event_desc = f"Parcel for Plot {visitor['plot_number']} marked to leave at guard post."
                else:
                    return self.send_json({"success": False, "error": "Invalid action"}, 400)

                cursor.execute("""
                    INSERT INTO event_logs (id, society_id, event_type, description)
                    VALUES (?, ?, 'visitor_action', ?)
                """, (str(uuid.uuid4()), visitor["society_id"], event_desc))

                conn.commit()
                return self.send_json({"success": True, "visitor_id": visitor_id, "status": new_status, "message": event_desc})

            # POST /api/visitors/checkout -> Visitor departs
            elif path == "/api/visitors/checkout":
                visitor_id = body.get("visitor_id")
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("UPDATE visitors SET status = 'exited', exit_time = ? WHERE id = ?", (now_str, visitor_id))
                conn.commit()
                return self.send_json({"success": True, "message": "Visitor checked out successfully."})

            # POST /api/passes/create -> 4-digit guest pass
            elif path == "/api/passes/create":
                plot_num = str(body.get("plot_number", "14")).strip()
                guest_name = body.get("guest_name", "Guest")
                valid_hours = int(body.get("valid_hours", 8))
                
                cursor.execute("SELECT * FROM plots WHERE plot_number = ?", (plot_num,))
                plot = cursor.fetchone()
                if not plot:
                    return self.send_json({"success": False, "error": "Plot not found"}, 400)

                import random
                pass_code = f"{random.randint(1000, 9999)}"
                pass_id = f"pass_{uuid.uuid4().hex[:8]}"
                now = datetime.now()

                cursor.execute("""
                    INSERT INTO gate_passes (id, society_id, plot_id, pass_code, guest_name, pass_type, valid_from, valid_until, is_active)
                    VALUES (?, ?, ?, ?, ?, 'one_time', ?, ?, 1)
                """, (pass_id, plot["society_id"], plot["id"], pass_code, guest_name, now, now + timedelta(hours=valid_hours)))
                conn.commit()

                cfg = load_config()
                return self.send_json({
                    "success": True,
                    "pass_code": pass_code,
                    "plot_number": plot_num,
                    "guest_name": guest_name,
                    "share_text": f"Namaste! Your guest entry pass for Villa Plot {plot_num} ({cfg.get('society_name')}) is: {pass_code}. Valid for {valid_hours} hours."
                })

            # POST /api/passes/verify
            elif path == "/api/passes/verify":
                code = str(body.get("pass_code", "")).strip()
                cursor.execute("""
                    SELECT gp.*, p.plot_number, p.street_name,
                           CASE WHEN p.active_contact = 'tenant' THEN p.tenant_name ELSE p.owner_name END as resident_name
                    FROM gate_passes gp
                    JOIN plots p ON gp.plot_id = p.id
                    WHERE gp.pass_code = ? AND gp.is_active = 1
                """, (code,))
                pass_entry = cursor.fetchone()
                if not pass_entry:
                    return self.send_json({"success": False, "error": "गलत कोड! Invalid or expired pass code."}, 400)

                vis_id = f"vis_{uuid.uuid4().hex[:10]}"
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute("""
                    INSERT INTO visitors (id, society_id, plot_id, visitor_name, visitor_type, 
                                          entry_channel, status, approval_source, pass_code, entry_time)
                    VALUES (?, ?, ?, ?, 'guest', 'pre_approved', 'inside', 'pass_code', ?, ?)
                """, (vis_id, pass_entry["society_id"], pass_entry["plot_id"], 
                      pass_entry["guest_name"] or "Pre-approved Guest", code, now_str))

                if pass_entry["pass_type"] == "one_time":
                    cursor.execute("UPDATE gate_passes SET is_active = 0, used_at = ? WHERE id = ?", (now_str, pass_entry["id"]))

                conn.commit()
                return self.send_json({
                    "success": True,
                    "plot_number": pass_entry["plot_number"],
                    "guest_name": pass_entry["guest_name"],
                    "resident_name": pass_entry["resident_name"],
                    "message": f"Pass Verified! Gate open for Plot {pass_entry['plot_number']}"
                })

            else:
                return self.send_json({"error": "Endpoint not found"}, 404)
        finally:
            conn.close()

def run_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), VilaDeskHandler) as httpd:
        print(f"============================================================")
        print(f"  VilaDesk Pilot Server Running at: http://localhost:{PORT}")
        print(f"============================================================")
        print(f"  • Guard Lite App (Hindi/Voice):  http://localhost:{PORT}/guard")
        print(f"  • Night QR Kiosk (Guardless):   http://localhost:{PORT}/kiosk")
        print(f"  • Resident WhatsApp Simulator:   http://localhost:{PORT}/whatsapp")
        print(f"  • Society Admin / Plot Map:     http://localhost:{PORT}/admin")
        print(f"  • Gate Sign (Print Ready):       http://localhost:{PORT}/print-board")
        print(f"  • Meta Webhook Endpoint:         http://localhost:{PORT}/api/whatsapp/webhook")
        print(f"============================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run_server()
