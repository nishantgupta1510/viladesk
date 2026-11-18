-- ============================================================================
-- VilaDesk Phase 1: Horizontal Micro-Township & Villa Database Schema
-- Designed for low-density villa communities (10-200 units) in Tier-2 cities.
-- ============================================================================

-- 1. Township / Society Metadata
CREATE TABLE IF NOT EXISTS societies (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    locality TEXT NOT NULL, -- e.g., 'Jagatpura', 'Sirsi Road', 'Ajmer Road'
    city TEXT NOT NULL DEFAULT 'Jaipur',
    state TEXT NOT NULL DEFAULT 'Rajasthan',
    total_plots INTEGER NOT NULL DEFAULT 0,
    gate_mode TEXT NOT NULL DEFAULT 'assisted', -- 'assisted' (guard) or 'unstaffed' (night kiosk)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Horizontal Plot / Villa Assets
-- Diverges from apartment schemas (no Tower/Floor). Tracks vacant and construction plots.
CREATE TABLE IF NOT EXISTS plots (
    id TEXT PRIMARY KEY,
    society_id TEXT NOT NULL,
    plot_number TEXT NOT NULL, -- e.g., '14', 'A-05', 'Villa Rose'
    street_name TEXT NOT NULL, -- e.g., 'Lane 1', 'North Boulevard'
    plot_type TEXT NOT NULL, -- 'occupied_villa', 'vacant_plot', 'under_construction'
    plot_area_sq_yd REAL NOT NULL DEFAULT 200.0, -- Yardage for differential maintenance billing
    
    -- Resident / Occupancy Details
    occupancy_status TEXT NOT NULL DEFAULT 'owner_staying', -- 'owner_staying', 'tenant_rented', 'unoccupied'
    owner_name TEXT NOT NULL,
    owner_phone TEXT NOT NULL,
    tenant_name TEXT,
    tenant_phone TEXT,
    active_contact TEXT NOT NULL DEFAULT 'owner', -- Who receives gate alerts: 'owner' or 'tenant'
    
    -- Construction details (if under_construction)
    contractor_name TEXT,
    contractor_phone TEXT,
    labor_count INTEGER DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (society_id) REFERENCES societies(id)
);

-- 3. Visitors & Gate Entry/Exit Logs
CREATE TABLE IF NOT EXISTS visitors (
    id TEXT PRIMARY KEY,
    society_id TEXT NOT NULL,
    plot_id TEXT NOT NULL,
    visitor_name TEXT NOT NULL,
    visitor_phone TEXT,
    vehicle_number TEXT,
    visitor_type TEXT NOT NULL, -- 'guest', 'delivery', 'cab', 'service', 'construction_labor'
    service_company TEXT, -- e.g., 'Swiggy', 'Zomato', 'Amazon', 'Uber', 'Urban Company'
    
    -- Security & Approval Status
    entry_channel TEXT NOT NULL, -- 'guard_app', 'night_qr_kiosk', 'pre_approved'
    status TEXT NOT NULL DEFAULT 'pending', -- 'pending', 'approved', 'denied', 'inside', 'exited'
    approval_source TEXT, -- 'whatsapp_button', 'guard_override', 'pass_code'
    pass_code TEXT, -- 4-digit pre-approved code if applicable
    photo_url TEXT,
    
    -- Timestamps
    entry_time TIMESTAMP,
    exit_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (society_id) REFERENCES societies(id),
    FOREIGN KEY (plot_id) REFERENCES plots(id)
);

-- 4. Pre-Approved Fast-Track Guest Passes
CREATE TABLE IF NOT EXISTS gate_passes (
    id TEXT PRIMARY KEY,
    society_id TEXT NOT NULL,
    plot_id TEXT NOT NULL,
    pass_code TEXT NOT NULL, -- 4-digit entry PIN
    guest_name TEXT,
    guest_phone TEXT,
    pass_type TEXT NOT NULL DEFAULT 'one_time', -- 'one_time', 'multi_day', 'daily_maid'
    valid_from TIMESTAMP NOT NULL,
    valid_until TIMESTAMP NOT NULL,
    is_active INTEGER DEFAULT 1,
    used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (society_id) REFERENCES societies(id),
    FOREIGN KEY (plot_id) REFERENCES plots(id)
);

-- 5. Physical Infrastructure & Street Asset Mapping
-- Maps common shared assets (streetlights, common borewell, gate barrier)
CREATE TABLE IF NOT EXISTS street_assets (
    id TEXT PRIMARY KEY,
    society_id TEXT NOT NULL,
    asset_type TEXT NOT NULL, -- 'borewell_pump', 'streetlight_pole', 'dg_inverter', 'boom_barrier'
    asset_tag TEXT NOT NULL, -- e.g., 'Pole #04', 'Main Borewell'
    location_near_plot TEXT, -- e.g., 'Opposite Plot 12'
    status TEXT NOT NULL DEFAULT 'working', -- 'working', 'maintenance_needed', 'broken'
    last_serviced_at TIMESTAMP,
    FOREIGN KEY (society_id) REFERENCES societies(id)
);

-- 6. Audit & WhatsApp Event Log
CREATE TABLE IF NOT EXISTS event_logs (
    id TEXT PRIMARY KEY,
    society_id TEXT NOT NULL,
    event_type TEXT NOT NULL, -- 'visitor_request', 'whatsapp_approved', 'gate_relay_opened', 'exit_logged'
    description TEXT NOT NULL,
    metadata_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
