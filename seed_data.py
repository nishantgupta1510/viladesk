#!/usr/bin/env python3
"""
Seed script for VilaDesk: Initializes database with realistic Jaipur villa township data.
Township: "Defined World City, Narsinghpura, Ajmer Road, NH-8, Jaipur, 302026"
"""

import sqlite3
import json
import uuid
from datetime import datetime, timedelta

DB_PATH = "viladesk.db"
SCHEMA_PATH = "schema.sql"

def seed_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Load and execute schema
    with open(SCHEMA_PATH, "r") as f:
        cursor.executescript(f.read())

    # Check if already seeded
    cursor.execute("SELECT COUNT(*) FROM societies")
    if cursor.fetchone()[0] > 0:
        print("Database already seeded. Skipping.")
        conn.close()
        return

    society_id = "soc_jaipur_01"
    
    # 1. Insert Society
    cursor.execute("""
        INSERT INTO societies (id, name, address, locality, city, state, total_plots, gate_mode)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        society_id,
        "Defined World City",
        "Narsinghpura, Ajmer Road, NH-8, Jaipur, 302026",
        "Ajmer Road",
        "Jaipur",
        "Rajasthan",
        25,
        "assisted"
    ))

    # 2. Insert Horizontal Plots (North Lane: 1-12, South Lane: 13-24, Main Avenue: 79)
    plots_data = [
        # North Lane (Plots 1-12)
        ("1", "North Lane", "occupied_villa", 250, "owner_staying", "Rajesh Sharma", "9829011001", None, None, "owner", "[]"),
        ("2", "North Lane", "occupied_villa", 200, "owner_staying", "Vikram Rathore", "9829011002", None, None, "owner", "[]"),
        ("3", "North Lane", "vacant_plot", 200, "unoccupied", "Manoj Agarwal (NRI)", "9829011003", None, None, "owner", "[]"),
        ("4", "North Lane", "occupied_villa", 200, "tenant_rented", "Sunil Mehta (Owner)", "9829011004", "Amit Verma (Tenant)", "9829099004", "tenant", "[]"),
        ("5", "North Lane", "occupied_villa", 300, "owner_staying", "Col. H.S. Shekhawat", "9829011005", None, None, "owner", "[]"),
        ("6", "North Lane", "under_construction", 250, "unoccupied", "Kailash Choudhary", "9829011006", None, None, "owner", "[]"),
        ("7", "North Lane", "occupied_villa", 200, "owner_staying", "Dr. Neha Khandelwal", "9829011007", None, None, "owner", "[]"),
        ("8", "North Lane", "vacant_plot", 200, "unoccupied", "Pramod Soni", "9829011008", None, None, "owner", "[]"),
        ("9", "North Lane", "occupied_villa", 250, "owner_staying", "Mahesh Gupta", "9829011009", None, None, "owner", "[]"),
        ("10", "North Lane", "occupied_villa", 200, "tenant_rented", "Deepak Jain (Owner)", "9829011010", "Rahul Tiwari (Tenant)", "9829099010", "tenant", "[]"),
        ("11", "North Lane", "under_construction", 300, "unoccupied", "Suresh Godara", "9829011011", None, None, "owner", "[]"),
        ("12", "North Lane", "occupied_villa", 250, "owner_staying", "Bhagwan Singh", "9829011012", None, None, "owner", "[]"),

        # South Lane (Plots 13-24)
        ("13", "South Lane", "occupied_villa", 200, "owner_staying", "Rameshwar Prasad", "9829011013", None, None, "owner", "[]"),
        ("14", "South Lane", "occupied_villa", 250, "owner_staying", "Saurabh Agarwal", "9829011014", None, None, "owner", "[]"),
        ("15", "South Lane", "vacant_plot", 200, "unoccupied", "Ashok Singhal", "9829011015", None, None, "owner", "[]"),
        ("16", "South Lane", "occupied_villa", 200, "owner_staying", "Gopal Pareek", "9829011016", None, None, "owner", "[]"),
        ("17", "South Lane", "occupied_villa", 300, "tenant_rented", "Pradeep Joshi (Owner)", "9829011017", "Karan Malhotra (Tenant)", "9829099017", "tenant", "[]"),
        ("18", "South Lane", "under_construction", 250, "unoccupied", "Dinesh Bhati", "9829011018", None, None, "owner", "[]"),
        ("19", "South Lane", "occupied_villa", 200, "owner_staying", "Virendra Yadav", "9829011019", None, None, "owner", "[]"),
        ("20", "South Lane", "vacant_plot", 200, "unoccupied", "Ravi Mathur", "9829011020", None, None, "owner", "[]"),
        ("21", "South Lane", "occupied_villa", 250, "owner_staying", "Hemant Somani", "9829011021", None, None, "owner", "[]"),
        ("22", "South Lane", "occupied_villa", 200, "owner_staying", "Anita Meena", "9829011022", None, None, "owner", "[]"),
        ("23", "South Lane", "vacant_plot", 200, "unoccupied", "Satish Mittal", "9829011023", None, None, "owner", "[]"),
        ("24", "South Lane", "occupied_villa", 300, "owner_staying", "Bhawani Singh", "9829011024", None, None, "owner", "[]"),

        # Main Avenue (Plot 79 - User Villa)
        ("79", "Main Avenue", "occupied_villa", 250, "owner_staying", "Nishant Gupta", "8947051629", None, None, "owner", json.dumps([{"name": "Shweta", "phone": "8104947078", "relation": "Spouse"}]))
    ]

    for p in plots_data:
        plot_id = f"plot_{p[0]}"
        cursor.execute("""
            INSERT INTO plots (id, society_id, plot_number, street_name, plot_type, plot_area_sq_yd, 
                               occupancy_status, owner_name, owner_phone, tenant_name, tenant_phone, active_contact, family_members_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (plot_id, society_id, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10]))

    # 3. Insert Street Assets
    assets = [
        (str(uuid.uuid4()), society_id, "borewell_pump", "Main Society Borewell", "Corner of Plot 1", "working"),
        (str(uuid.uuid4()), society_id, "boom_barrier", "Main Entrance Barrier", "Main Gate", "working"),
        (str(uuid.uuid4()), society_id, "dg_inverter", "Security & Gate Power Backup", "Guard Cabin", "working"),
        (str(uuid.uuid4()), society_id, "streetlight_pole", "Pole #01 (Gate)", "Main Gate", "working"),
        (str(uuid.uuid4()), society_id, "streetlight_pole", "Pole #04 (North Lane)", "Opposite Plot 4", "working"),
        (str(uuid.uuid4()), society_id, "streetlight_pole", "Pole #08 (North End)", "Near Plot 12", "working"),
        (str(uuid.uuid4()), society_id, "streetlight_pole", "Pole #12 (South Lane)", "Opposite Plot 18", "working"),
    ]
    for a in assets:
        cursor.execute("INSERT INTO street_assets VALUES (?, ?, ?, ?, ?, ?, ?)", (a[0], a[1], a[2], a[3], a[4], a[5], None))

    # 4. Insert active sample pre-approved pass for Plot 14
    now = datetime.now()
    cursor.execute("""
        INSERT INTO gate_passes (id, society_id, plot_id, pass_code, guest_name, guest_phone, pass_type, valid_from, valid_until, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "pass_demo_01",
        society_id,
        "plot_14",
        "4821",
        "Aakash Saxena",
        "9829055443",
        "one_time",
        now - timedelta(hours=1),
        now + timedelta(hours=6),
        1
    ))

    # 5. Insert one active visitor currently inside (Plot 7 Delivery)
    cursor.execute("""
        INSERT INTO visitors (id, society_id, plot_id, visitor_name, visitor_phone, vehicle_number, 
                              visitor_type, service_company, entry_channel, status, approval_source, 
                              entry_time, exit_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "vis_init_01",
        society_id,
        "plot_7",
        "Mukesh Kumar",
        "9876543210",
        "RJ 14 SK 2201",
        "delivery",
        "Swiggy",
        "guard_app",
        "inside",
        "whatsapp_button",
        (now - timedelta(minutes=14)).strftime("%Y-%m-%d %H:%M:%S"),
        None
    ))

    conn.commit()
    conn.close()
    print("Database seeded successfully with 24 Jaipur township plots, street assets, and sample state.")

if __name__ == "__main__":
    seed_database()
