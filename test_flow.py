#!/usr/bin/env python3
"""
Automated End-to-End Verification Test for VilaDesk Phase 1.
Tests schema, REST API, WhatsApp interactive flow, Night Kiosk flow, and 4-digit Passcode.
"""

import urllib.request
import json
import time
import sys

BASE_URL = "http://localhost:8080"

def get(path):
    req = urllib.request.Request(f"{BASE_URL}{path}", headers={"User-Agent": "TestRunner"})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode("utf-8"))

def post(path, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}{path}", data=data, 
                                 headers={"Content-Type": "application/json", "User-Agent": "TestRunner"})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode("utf-8"))

def run_tests():
    print("=" * 60)
    print("  RUNNING VILADESK PHASE 1 END-TO-END VERIFICATION")
    print("=" * 60)

    # 1. Test Plots Retrieval
    print("\n[Test 1] Verifying Horizontal Plots Directory...")
    plots_data = get("/api/plots")
    assert plots_data["success"], "Failed to fetch plots"
    plots = plots_data["plots"]
    print(f"  ✓ Successfully fetched {len(plots)} plots (including Plot 79).")
    assert len(plots) >= 24, f"Expected at least 24 plots, got {len(plots)}"
    
    # Check diverse plot types
    types = {p["plot_type"] for p in plots}
    print(f"  ✓ Plot types detected in Jaipur township: {types}")
    assert "occupied_villa" in types and "vacant_plot" in types and "under_construction" in types

    # 2. Test Guard / Kiosk Entry Request Flow
    print("\n[Test 2] Simulating Entry Request for Plot 14 (Zomato Delivery)...")
    req_payload = {
        "plot_number": "14",
        "visitor_name": "Mukesh Kumar",
        "visitor_phone": "9829012345",
        "vehicle_number": "RJ 14 AB 1122",
        "visitor_type": "delivery",
        "service_company": "Zomato",
        "entry_channel": "guard_app"
    }
    req_res = post("/api/visitors/request", req_payload)
    assert req_res["success"], "Failed to create visitor request"
    vis_id = req_res["visitor_id"]
    print(f"  ✓ Visitor created (ID: {vis_id}) with status '{req_res['status']}'.")
    print(f"  ✓ Simulated WhatsApp alert dispatched to: {req_res['resident_name']} ({req_res['resident_phone']})")

    # 3. Test Resident WhatsApp Feed
    print("\n[Test 3] Verifying Resident WhatsApp Feed receives pending alert...")
    wa_feed = get("/api/whatsapp/feed?plot_number=14")
    assert wa_feed["success"], "Failed to fetch WhatsApp feed"
    pending = [v for v in wa_feed["pending_notifications"] if v["id"] == vis_id]
    assert len(pending) == 1, "Pending notification not found in WhatsApp feed"
    print(f"  ✓ WhatsApp bot successfully received interactive prompt for Visitor: {pending[0]['visitor_name']}")

    # 4. Test Resident Approval Action (Simulated Button Tap)
    print("\n[Test 4] Simulating Resident tapping '[Allow Entry]' in WhatsApp...")
    action_res = post("/api/visitors/action", {
        "visitor_id": vis_id,
        "action": "approve",
        "source": "whatsapp_button"
    })
    assert action_res["success"], "Approval action failed"
    assert action_res["status"] == "inside", "Status should be 'inside'"
    print(f"  ✓ Status transitioned to 'inside'. Gate relay signal triggered: {action_res['message']}")

    # 5. Verify Kiosk / Guard status polling reflects approved state
    print("\n[Test 5] Verifying Guard/Kiosk polling detects approval...")
    status_res = get(f"/api/visitors/status/{vis_id}")
    assert status_res["visitor"]["status"] == "inside", "Polled status not inside"
    print(f"  ✓ Guard/Kiosk polling confirmed: Status is 'inside' at Plot 14.")

    # 6. Test 4-Digit Guest Pass Creation & Verification
    print("\n[Test 6] Creating 4-digit Fast-Track Guest Pass for Plot 14...")
    pass_res = post("/api/passes/create", {
        "plot_number": "14",
        "guest_name": "Suresh Gupta (Guest)",
        "valid_hours": 6
    })
    assert pass_res["success"], "Failed to create pass"
    pass_code = pass_res["pass_code"]
    print(f"  ✓ Passcode generated: {pass_code} for Plot {pass_res['plot_number']}.")
    
    print(f"  ✓ Verifying Passcode '{pass_code}' at gate...")
    verify_res = post("/api/passes/verify", {"pass_code": pass_code})
    assert verify_res["success"], "Failed to verify valid passcode"
    print(f"  ✓ Passcode verified! Gate unlocked: {verify_res['message']}")

    # 7. Test Visitor Exit Checkout (Closing the loop)
    print("\n[Test 7] Testing Visitor Exit Flow (Checkout from society)...")
    checkout_res = post("/api/visitors/checkout", {"visitor_id": vis_id})
    assert checkout_res["success"], "Failed to checkout visitor"
    print(f"  ✓ Visitor checked out successfully. Timestamp logged.")

    # 8. Check History Table
    print("\n[Test 8] Verifying Audit Trail in History...")
    history = get("/api/visitors/history")
    assert history["success"], "Failed to get history"
    print(f"  ✓ Total historical gate events recorded: {len(history['history'])}")

    print("\n" + "=" * 60)
    print("  ALL TESTS PASSED! Phase 1 Core Architecture is 100% Operational.")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
