import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # =========================================================================
    # LIGHT & POSITIVE VIBE PALETTE
    # =========================================================================
    C_BG_PAGE = RGBColor(250, 252, 250)      # Luminous soft off-white
    C_WHITE = RGBColor(255, 255, 255)        # Pure white card
    C_HERO_BG = RGBColor(236, 253, 245)      # Soft fresh mint / emerald tint
    C_TEXT_DARK = RGBColor(15, 23, 42)       # Deep slate navy (crisp & readable)
    C_TEXT_MUTED = RGBColor(71, 85, 105)     # Warm slate gray
    C_EMERALD = RGBColor(16, 185, 129)       # Vibrant emerald green (optimism, growth)
    C_TEAL = RGBColor(13, 148, 136)          # Vibrant teal
    C_AMBER = RGBColor(217, 119, 6)          # Warm sunshine amber (energy & friendliness)
    C_SKY = RGBColor(2, 132, 199)            # Bright sky blue (trust & clarity)
    C_INDIGO = RGBColor(79, 70, 229)         # Modern indigo
    C_CARD_BORDER = RGBColor(226, 232, 240)  # Clean subtle border
    C_BORDER_EMERALD = RGBColor(167, 243, 208) # Mint border

    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide, color=C_BG_PAGE):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="VILADESK • SMART TOWNSHIP OS", accent_color=C_TEAL):
        # Decorative top sunshine bar
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.35), Inches(0.6), Inches(0.08))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = accent_color
        top_bar.line.fill.background()

        # Category Pill / Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.48), Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = accent_color

        # Slide Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.75))
        tf = t_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 1: Title Slide (Fresh, Light, Welcoming & High-Vibe)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, C_WHITE)

    # Hero Banner Card (Soft Mint/Emerald Wash)
    hero = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    hero.fill.solid()
    hero.fill.fore_color.rgb = C_HERO_BG
    hero.line.color.rgb = C_BORDER_EMERALD
    hero.line.width = Pt(2)

    # Decorative sunshine pill
    spill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(1.3), Inches(5.8), Inches(0.45))
    spill.fill.solid()
    spill.fill.fore_color.rgb = C_WHITE
    spill.line.color.rgb = C_EMERALD
    spill.line.width = Pt(1.5)
    tf_sp = spill.text_frame
    p_sp = tf_sp.paragraphs[0]
    p_sp.text = "☀️ NEXT-GEN TOWNSHIP OPERATING SYSTEM"
    p_sp.font.size = Pt(11)
    p_sp.font.bold = True
    p_sp.font.color.rgb = C_EMERALD

    # Title box
    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(1.85), Inches(10.8), Inches(4.5))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p_title = tf1.paragraphs[0]
    p_title.text = "VilaDesk"
    p_title.font.size = Pt(60)
    p_title.font.bold = True
    p_title.font.color.rgb = C_TEXT_DARK

    p_sub = tf1.add_paragraph()
    p_sub.text = "Gate Security, WhatsApp Approvals & Plotted Khata OS"
    p_sub.font.size = Pt(24)
    p_sub.font.bold = True
    p_sub.font.color.rgb = C_TEAL

    p_desc = tf1.add_paragraph()
    p_desc.text = "\nPurpose-built for Villa Societies, Micro-Townships & Plotted Developments (10–200 Units).\nDelight your residents with 100% WhatsApp-native approvals: Zero app downloads, zero capex hardware."
    p_desc.font.size = Pt(14)
    p_desc.font.color.rgb = C_TEXT_MUTED

    p_meta = tf1.add_paragraph()
    p_meta.text = "\n🌱 Confidential Proposal Deck • Defined World City & Jaipur Tier-2 Townships • November 2026"
    p_meta.font.size = Pt(11)
    p_meta.font.bold = True
    p_meta.font.color.rgb = RGBColor(100, 116, 139)

    # =========================================================================
    # SLIDE 2: The Plotted Township Problem (Why Apartment Apps Fail)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, C_BG_PAGE)
    add_header(s2, "The Plotted Township Paradox: Why Apartment Apps Fail", "MARKET GAP & PROBLEM STATEMENT", C_AMBER)

    cards_data = [
        ("Horizontal Layout", "Legacy apps (MyGate / NoBrokerHood) are engineered for 500+ unit high-rise towers. They fail completely in horizontal layouts with low density and wide avenues.", "🏢 ➡️ 🏡", C_SKY),
        ("Vacant Plot Owners", "In plotted developments, 40%–60% are vacant investor plots. An investor living elsewhere will NEVER download a bulky 120MB app for land they visit twice a year.", "🌱 40-60% Vacant", C_AMBER),
        ("High Capex & Attrition", "Motorized boom barriers & complex hardware cost ₹3–5 Lakhs upfront + heavy AMC. Gate guards change frequently and struggle with complicated English apps.", "💸 ₹3-5L Barrier", C_INDIGO),
        ("Construction Traffic", "Townships face 3–5 years of active villa construction. Cement trucks, sand dumpers, and daily labor enter without verification, leading to material theft.", "🚛 Construction", C_TEAL)
    ]

    left_margin = Inches(0.8)
    card_width = Inches(2.7)
    gap = Inches(0.3)
    top_pos = Inches(1.8)
    card_height = Inches(4.8)

    for i, (ctitle, cdesc, ctag, ccolor) in enumerate(cards_data):
        c_left = left_margin + i * (card_width + gap)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, top_pos, card_width, card_height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_CARD_BORDER
        card.line.width = Pt(1.5)

        # Top colored accent strip on card
        strip = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, top_pos, card_width, Inches(0.12))
        strip.fill.solid()
        strip.fill.fore_color.rgb = ccolor
        strip.line.fill.background()

        tb = s2.shapes.add_textbox(c_left + Inches(0.15), top_pos + Inches(0.25), card_width - Inches(0.3), card_height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = ctag
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = ccolor

        p2 = tf.add_paragraph()
        p2.text = ctitle
        p2.font.size = Pt(18)
        p2.font.bold = True
        p2.font.color.rgb = C_TEXT_DARK

        p3 = tf.add_paragraph()
        p3.text = f"\n{cdesc}"
        p3.font.size = Pt(13)
        p3.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 3: The VilaDesk Breakthrough (Zero-App WhatsApp Architecture)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, C_BG_PAGE)
    add_header(s3, "The VilaDesk Breakthrough: Zero-App, WhatsApp-Native OS", "CORE VALUE PROPOSITION", C_EMERALD)

    features = [
        ("100% Resident & Investor Adoption on Day 1", "Zero app download required! 100% of residents and plot owners already use WhatsApp every day. Interactive gate approval cards arrive directly in their personal WhatsApp chat with 1-tap buttons: [Allow Entry] / [Deny] / [Leave at Gate].", C_EMERALD, "📲"),
        ("Dual-Mode Gate Operations (Day & Night)", "Operates smoothly in two flexible modes: (1) Guard-Assisted Mode for day hours with 2-tap delivery logging & Hindi speech recognition ('Plot 79 Courier'), and (2) Unguarded Self-Service QR Kiosk for night shifts and budget gates.", C_TEAL, "☀️🌙"),
        ("Zero Capex Hardware & 24-Hour Deployment", "Requires NO expensive boom barriers, NO server racks, and NO RFID tags. Runs on any existing ₹6,000 Android smartphone or tablet in the guard cabin. Completely configured and live in under 24 hours.", C_AMBER, "⚡")
    ]

    for i, (ftitle, fdesc, color, ficon) in enumerate(features):
        y_pos = Inches(1.8) + i * Inches(1.7)
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y_pos, Inches(11.733), Inches(1.4))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = color
        box.line.width = Pt(2)

        tb = s3.shapes.add_textbox(Inches(1.1), y_pos + Inches(0.15), Inches(11.1), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = f"{ficon} {ftitle}"
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.text = fdesc
        p2.font.size = Pt(13)
        p2.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 4: Phase 1 — Instant 24-Hour Gate Security (Ready for Immediate Rollout)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, C_BG_PAGE)
    add_header(s4, "Phase 1: Instant Gate Security (Quickly Deployable in < 24 Hours)", "PHASE 1 IMPLEMENTATION", C_TEAL)

    grid_w = Inches(5.7)
    grid_h = Inches(2.3)
    coords = [
        (Inches(0.8), Inches(1.8)),
        (Inches(6.8), Inches(1.8)),
        (Inches(0.8), Inches(4.5)),
        (Inches(6.8), Inches(4.5))
    ]

    p1_items = [
        ("Guard Lite PWA (Hindi / Voice)", [
            "• 2-Tap fast selector for Swiggy, Zomato, Amazon, Uber & Guests",
            "• Web Speech API: Guard speaks 'Plot 79 Courier' in Hindi to auto-fill",
            "• Audio chime + Text-to-Speech spoken feedback ('Plot 79 Approved')",
            "• 'Currently Inside' carousel with 1-tap exit checkout"
        ], C_EMERALD, "👮"),
        ("Interactive WhatsApp Dispatch", [
            "• Instant interactive cards delivered via Meta WhatsApp Cloud API",
            "• 3 Action Buttons: [✅ Allow Entry]  [❌ Deny]  [📦 Leave at Gate]",
            "• Multi-family simultaneous dispatch (Owner + Spouse + Family)",
            "• Direct '📞 Call Guard Cabin' link embedded in message"
        ], C_TEAL, "💬"),
        ("Night QR Kiosk (Guardless)", [
            "• Self-service visitor check-in when guard is away or off-duty",
            "• Strict 10-digit OTP & resident verification",
            "• Real-time approval polling with full-screen green clearance pass",
            "• Physical weatherproof QR gate board ready for printing"
        ], C_AMBER, "🌙"),
        ("Digital Passes & Fast-Track", [
            "• 4-Digit fast-track guest passcodes generated by residents",
            "• 2-Second guard passcode verification",
            "• 1-Tap '📞 Call Resident' button for guards if resident is away",
            "• Live audit feed and historical gate event logs exportable to Excel"
        ], C_SKY, "🔑")
    ]

    for i, (title, bullets, color, icon) in enumerate(p1_items):
        gx, gy = coords[i]
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, gx, gy, grid_w, grid_h)
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_CARD_BORDER
        card.line.width = Pt(1.5)

        # Colored left accent
        laccent = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, gx, gy, Inches(0.12), grid_h)
        laccent.fill.solid()
        laccent.fill.fore_color.rgb = color
        laccent.line.fill.background()

        tb = s4.shapes.add_textbox(gx + Inches(0.25), gy + Inches(0.12), grid_w - Inches(0.4), grid_h - Inches(0.25))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = f"{icon} {title}"
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = C_TEXT_DARK

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = b
            pb.font.size = Pt(11.5)
            pb.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 5: Requirements From Builder for Phase 1 Deployment (CRITICAL SLIDE)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, C_BG_PAGE)
    add_header(s5, "What We Need From Builder to Deploy Phase 1 (Checklist)", "BUILDER PREREQUISITES & ONBOARDING", C_AMBER)

    reqs = [
        ("1. Plot Layout & Master Plan", "Excel / CAD / PDF of township layout", [
            "• Plot numbers (e.g. 1 to 200) and plot sizes in sq. yards",
            "• Current status (Occupied Villa / Vacant Plot / Under Construction)",
            "• Primary owner name & 10-digit mobile number for WhatsApp alerts"
        ], C_TEAL, "📋"),
        ("2. Gate Cabin Hardware", "1 Budget Smartphone or Tablet", [
            "• 1 Android phone (Android 10+, screen >= 6.0\") or 8\"–10\" budget tablet",
            "• 1 Basic 4G SIM connection (Jio/Airtel ₹150/mo, data usage < 1 GB/mo)",
            "• Continuous 5V charging cable/socket in guard cabin"
        ], C_EMERALD, "📱"),
        ("3. Gate Physical Access Setup", "Manual Gate or ₹2,500 Latch Retrofit", [
            "• Option A (Zero-Hardware): Guard checks full-screen green clearance token",
            "• Option B (Electric Rim Lock Retrofit): ₹2,500 12V latch on pedestrian wicket gate triggered automatically when resident clicks [Allow]",
            "• Physical laminated A4/Sunboard QR sign mounted at entry gate"
        ], C_AMBER, "🚪"),
        ("4. Builder / RWA Site SPOC", "Single Point of Contact for 30-min Setup", [
            "• 1 Site supervisor or manager for initial WhatsApp group creation",
            "• 30-Minute guard training session conducted in Hindi by VilaDesk team",
            "• Official gate mobile number for caller ID (can be society SIM)"
        ], C_SKY, "🤝")
    ]

    for i, (rtitle, rsub, rbullets, rcolor, ricon) in enumerate(reqs):
        rx, ry = coords[i]
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, ry, grid_w, grid_h)
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = rcolor
        card.line.width = Pt(2)

        tb = s5.shapes.add_textbox(rx + Inches(0.2), ry + Inches(0.12), grid_w - Inches(0.4), grid_h - Inches(0.25))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = f"{ricon} {rtitle}"
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = rcolor

        p_sub = tf.add_paragraph()
        p_sub.text = rsub
        p_sub.font.size = Pt(11)
        p_sub.font.italic = True
        p_sub.font.color.rgb = C_TEXT_DARK

        for b in rbullets:
            pb = tf.add_paragraph()
            pb.text = b
            pb.font.size = Pt(11.5)
            pb.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 6: Phase 2 — Plotted Khata & Maintenance Billing (Month 2–3)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, C_BG_PAGE)
    add_header(s6, "Phase 2: Plotted Khata & Automated Maintenance Billing", "FUTURE ROADMAP • MONTH 2–3", C_TEAL)

    p2_cards = [
        ("Per-Sq-Yard Billing Engine", [
            "• Horizontal townships cannot charge flat flat-rates",
            "• Automated differential CAM pricing:",
            "   - Occupied Villas: ₹2.50 / sq.yd (Full services)",
            "   - Vacant Investor Plots: ₹1.00 / sq.yd (Security/road upkeep)",
            "   - Under-Construction: ₹3.50 / sq.yd (Road wear & tear surcharge)"
        ], C_EMERALD, "📐"),
        ("1-Click WhatsApp UPI Payments", [
            "• Automated monthly PDF bills generated and sent directly on WhatsApp",
            "• Embedded Dynamic UPI Payment QR (Google Pay, PhonePe, Paytm)",
            "• Zero convenience fees via direct bank account settlement",
            "• Instant WhatsApp digital receipt & automated reconciliation"
        ], C_TEAL, "💳"),
        ("Public Transparency Cashbook", [
            "• Live financial transparency dashboard for RWA & Builder",
            "• Real-time tracking of collections vs outstanding dues",
            "• Digitized expenditure vouchers (Guard salary, DG diesel, gardener)",
            "• Eliminates resident suspicion during builder-to-RWA handover"
        ], C_AMBER, "📊"),
        ("Construction & Material Gate Passes", [
            "• Digital gate passes for cement, sand, brick & marble trucks",
            "• Daily contractor labor headcount logging (Contractor ID + photo)",
            "• Stops material theft, unauthorized dumping & construction encroachment",
            "• Auto-alerts plot owner when trucks enter their plot"
        ], C_SKY, "🚛")
    ]

    for i, (title, bullets, color, icon) in enumerate(p2_cards):
        gx, gy = coords[i]
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, gx, gy, grid_w, grid_h)
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_CARD_BORDER
        card.line.width = Pt(1.5)

        tb = s6.shapes.add_textbox(gx + Inches(0.2), gy + Inches(0.15), grid_w - Inches(0.4), grid_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = f"{icon} {title}"
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = C_TEXT_DARK

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = b
            pb.font.size = Pt(11.5)
            pb.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 7: Phase 3 — Cluster Utility & Handyman Pooling (Month 3–6)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, C_BG_PAGE)
    add_header(s7, "Phase 3: Cluster Utility Ecosystem & Amenity OS", "FUTURE ROADMAP • MONTH 3–6", C_INDIGO)

    p3_cards = [
        ("Ajmer Road Handyman Pooling", [
            "• Individual 20-50 villa societies cannot afford full-time electricians or plumbers",
            "• Shared on-demand service pool across 3-4 neighboring micro-townships",
            "• Verified technicians dispatched via WhatsApp with tracked gate entry",
            "• 40% lower maintenance cost for residents"
        ], C_EMERALD, "🛠️"),
        ("Water Tanker Delivery Tracking", [
            "• Plotted townships on Ajmer Road / NH-8 rely heavily on private tankers",
            "• Digital tanker logger: Tanker capacity (5,000L / 10,000L) & vendor verification",
            "• TDS water quality testing records logged at gate before tanker discharges",
            "• Transparent billing ledger prevents phantom tanker deliveries"
        ], C_SKY, "💧"),
        ("Clubhouse & Amenity Access", [
            "• QR-based digital access for swimming pool, gym, tennis court & community hall",
            "• Pre-booking of clubhouse for resident family events & birthday parties",
            "• Guest amenity pass generation with built-in time limits",
            "• Maintenance defaulters automatically restricted from amenity booking"
        ], C_AMBER, "🏊"),
        ("Optional IoT & ANPR Camera Integration", [
            "• Automatic Number Plate Recognition (ANPR) camera retrofit at main gate",
            "• Pre-registered resident cars recognized in 1.5 seconds without RFID sticker",
            "• Automatic solar street lighting schedule manager",
            "• Peripheral boundary wall motion sensor alert integration"
        ], C_INDIGO, "📷")
    ]

    for i, (title, bullets, color, icon) in enumerate(p3_cards):
        gx, gy = coords[i]
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, gx, gy, grid_w, grid_h)
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_CARD_BORDER
        card.line.width = Pt(1.5)

        tb = s7.shapes.add_textbox(gx + Inches(0.2), gy + Inches(0.15), grid_w - Inches(0.4), grid_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = f"{icon} {title}"
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = C_TEXT_DARK

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = b
            pb.font.size = Pt(11.5)
            pb.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 8: Builder ROI & Value Creation (Light, Bright & Inspiring)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, C_BG_PAGE)
    add_header(s8, "Builder ROI: Premium Township Branding & Effortless Handover", "BUSINESS IMPACT & VALUE CREATION", C_EMERALD)

    roi_items = [
        ("₹150–₹300 / sq.yd Sales Premium", "Marketing your project as a 'Next-Gen Smart Gated Township' attracts NRI buyers, tech professionals, and premium investors. Plot sales velocity increases by 35% compared to ungated developments.", C_EMERALD, "📈"),
        ("Dispute-Free RWA Handover", "The #1 cause of builder-buyer friction in Jaipur is maintenance fund disputes. VilaDesk's automated Khata and digital audit trail provide 100% transparent records for seamless transition.", C_TEAL, "🤝"),
        ("Eliminates Guard Attrition Woes", "Guards in Jaipur quit every 2-3 months. Because VilaDesk features an ultra-simple 2-tap Hindi voice interface, a brand new guard learns the entire system in under 5 minutes without English proficiency.", C_AMBER, "🛡️"),
        ("Zero Capex & Ultra-Low TCO", "No ₹3-5 Lakh boom barriers to maintain. No recurring AMC contracts. Fraction of legacy high-rise app fees. Less than the cost of one guard's monthly chai expenses.", C_SKY, "💡")
    ]

    for i, (rtitle, rdesc, color, icon) in enumerate(roi_items):
        y_pos = Inches(1.8) + i * Inches(1.25)
        box = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y_pos, Inches(11.733), Inches(1.05))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = color
        box.line.width = Pt(1.5)

        # Left color bar
        cbar = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y_pos, Inches(0.12), Inches(1.05))
        cbar.fill.solid()
        cbar.fill.fore_color.rgb = color
        cbar.line.fill.background()

        tb = s8.shapes.add_textbox(Inches(1.1), y_pos + Inches(0.1), Inches(11.1), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = f"{icon} {rtitle}"
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.text = rdesc
        p2.font.size = Pt(12)
        p2.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 9: Commercials & 30-Day Zero-Risk Pilot Offer
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, C_BG_PAGE)
    add_header(s9, "Commercials & 30-Day Zero-Risk Live Pilot", "PILOT ENGAGEMENT MODEL", C_EMERALD)

    # Left: Pilot Offer Card (Soft Green Card)
    c_left = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = RGBColor(240, 253, 244) # soft mint green
    c_left.line.color.rgb = C_EMERALD
    c_left.line.width = Pt(2)

    tb_l = s9.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.4))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p1 = tf_l.paragraphs[0]
    p1.text = "🎯 30-Day Zero-Risk Live Pilot"
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(6, 95, 70)

    pilot_bullets = [
        "\n• 100% Free 30-Day Live Trial at your main entry gate",
        "• Complete Phase 1 setup deployed within 24 hours",
        "• On-site guard training in Hindi conducted by our team",
        "• Laminated weatherproof QR gate boards provided free",
        "• Zero upfront investment, zero software license fee",
        "• Test with actual residents & plot owners with zero risk"
    ]
    for b in pilot_bullets:
        p = tf_l.add_paragraph()
        p.text = b
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(4, 120, 87)

    # Right: Commercial Model Card
    c_right = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = C_WHITE
    c_right.line.color.rgb = C_CARD_BORDER
    c_right.line.width = Pt(1.5)

    tb_r = s9.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.4))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p1_r = tf_r.paragraphs[0]
    p1_r.text = "💼 Post-Pilot Transparent Pricing"
    p1_r.font.size = Pt(22)
    p1_r.font.bold = True
    p1_r.font.color.rgb = C_TEXT_DARK

    comm_bullets = [
        "\n• Simple, predictable per-plot subscription model",
        "• Discounted rate for vacant investor plots (protects builder holding costs)",
        "• All-inclusive pricing: covers cloud servers, Meta WhatsApp API costs, updates & local support",
        "• Flexible billing: Can be billed directly to Builder or transitioned to RWA",
        "• No hardware lock-in: cancel anytime with 1-click data export in Excel"
    ]
    for b in comm_bullets:
        p = tf_r.add_paragraph()
        p.text = b
        p.font.size = Pt(13)
        p.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 10: 24x7 Live Demo & Next Steps (Light, Cheerful & High-Vibe)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, C_BG_PAGE)
    add_header(s10, "Experience the 24x7 Live Interactive Demo", "GET STARTED IN 24 HOURS", C_EMERALD)

    demo_box = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8))
    demo_box.fill.solid()
    demo_box.fill.fore_color.rgb = C_WHITE
    demo_box.line.color.rgb = C_EMERALD
    demo_box.line.width = Pt(2)

    tb_d = s10.shapes.add_textbox(Inches(1.2), Inches(2.1), Inches(10.9), Inches(4.2))
    tf_d = tb_d.text_frame
    tf_d.word_wrap = True

    p_d1 = tf_d.paragraphs[0]
    p_d1.text = "Try the Live Platform Right Now on Your Laptop or Phone:"
    p_d1.font.size = Pt(22)
    p_d1.font.bold = True
    p_d1.font.color.rgb = C_TEXT_DARK

    demo_links = [
        ("\n📱 Interactive Demo Showcase (Dual Phone Simulator):", "https://viladesk.onrender.com/demo"),
        ("👮 Live Guard Cabin PWA (Hindi / Voice / 2-Tap):", "https://viladesk.onrender.com/guard"),
        ("💬 Live Resident WhatsApp Experience:", "https://viladesk.onrender.com/whatsapp"),
        ("🌙 Live Unguarded Gate QR Kiosk:", "https://viladesk.onrender.com/kiosk"),
        ("🗺️ Live Township Map & Master Khata Admin:", "https://viladesk.onrender.com/admin")
    ]

    for label, url in demo_links:
        p = tf_d.add_paragraph()
        p.text = f"{label} {url}"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_TEAL

    p_action = tf_d.add_paragraph()
    p_action.text = "\n🚀 Rollout Next Step: Share your township plot layout Excel sheet, and we will configure your gate within 24 hours!"
    p_action.font.size = Pt(14)
    p_action.font.bold = True
    p_action.font.color.rgb = C_EMERALD

    # Save presentation
    prs.save(output_path)
    print(f"✓ Successfully generated light & positive vibe proposal deck at: {output_path}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "VilaDesk_Builder_Proposal_Deck.pptx"
    create_deck(out)
