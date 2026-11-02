import os
import json
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "WattWiseCalc"
SITE_TAGLINE = "Precision Solar, Battery & Inverter Sizing Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "7f8a9b2c4d5e6f1a2b3c4d5e6f7a8b9c"

# Auto-detect GitHub Pages URL from environment or fallback
REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/wattwisecalc")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "wattwisecalc")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "Jackery Explorer 1000 v2 Portable Power Station (1070Wh LiFePO4)",
        "category": "Portable Power Station",
        "rating": "4.8 ★ (6,400+ reviews)",
        "badge": " #1 Best Seller in Solar Generators",
        "specs": "1500W AC Output (3000W Surge) | 1-Hr Fast Charge | 4000+ Cycles",
        "keyword": "Jackery+Explorer+1000+v2+Portable+Power+Station+LiFePO4"
    },
    {
        "title": "EcoFlow DELTA 2 LiFePO4 Portable Power Station (1024Wh)",
        "category": "Home Backup & RV",
        "rating": "4.7 ★ (8,100+ reviews)",
        "badge": "Top Rated Backup Power",
        "specs": "1800W Output | Expandable to 3kWh | 80% Charge in 50 Mins",
        "keyword": "EcoFlow+DELTA+2+Portable+Power+Station+LiFePO4"
    },
    {
        "title": "LiTime 12V 100Ah LiFePO4 Lithium Deep Cycle Battery",
        "category": "Deep Cycle Battery",
        "rating": "4.8 ★ (5,900+ reviews)",
        "badge": "Best Value per Watt-Hour",
        "specs": "1280Wh Energy | Built-in 100A BMS | 4000-15000 Deep Cycles",
        "keyword": "LiTime+12V+100Ah+LiFePO4+Battery+Built-in+100A+BMS"
    },
    {
        "title": "BLUETTI EB3A Portable Power Station 268Wh LiFePO4 Backup",
        "category": "Compact Power",
        "rating": "4.6 ★ (11,200+ reviews)",
        "badge": "Most Popular Compact Unit",
        "specs": "600W AC Pure Sine Wave Inverter (1200W Surge) | UPS Function",
        "keyword": "BLUETTI+EB3A+Portable+Power+Station+268Wh+LiFePO4"
    },
    {
        "title": "Renogy 200 Watt 12 Volt Monocrystalline Solar Panel Starter Kit",
        "category": "Solar Panels",
        "rating": "4.7 ★ (9,500+ reviews)",
        "badge": "Top Off-Grid Solar Kit",
        "specs": "High Efficiency Mono Cells | Charge Controller & Cables Included",
        "keyword": "Renogy+200+Watt+12+Volt+Monocrystalline+Solar+Starter+Kit"
    },
    {
        "title": "GIANDEL 2000W Pure Sine Wave Power Inverter 12V DC to 120V AC",
        "category": "Power Inverters",
        "rating": "4.6 ★ (4,300+ reviews)",
        "badge": "Heavy-Duty Inverter Choice",
        "specs": "4000W Peak Surge | Dual AC Outlets | Wired Remote & LED Display",
        "keyword": "GIANDEL+2000W+Pure+Sine+Wave+Inverter+12V+to+120V"
    },
    {
        "title": "APC UPS 1500VA Sine Wave UPS Battery Backup & Surge Protector",
        "category": "Computer & WiFi UPS",
        "rating": "4.8 ★ (19,400+ reviews)",
        "badge": "#1 Uninterruptible Power Supply",
        "specs": "900W Output | Automatic Voltage Regulation (AVR) | Active PFC",
        "keyword": "APC+UPS+1500VA+Sine+Wave+UPS+Battery+Backup+BR1500MS2"
    },
    {
        "title": "Victron Energy SmartSolar MPPT 100/30 Solar Charge Controller",
        "category": "Charge Controllers",
        "rating": "4.9 ★ (7,800+ reviews)",
        "badge": "Pro Installer Choice",
        "specs": "12/24-Volt 30-Amp | Ultra-Fast MPPT Tracking | Built-in Bluetooth",
        "keyword": "Victron+Energy+SmartSolar+MPPT+100+30+Charge+Controller"
    }
]

# ==========================================
# PROGRAMMATIC SEO CALCULATOR PRESETS
# ==========================================
APPLIANCE_PRESETS = [
    {"slug": "cpap-machine-battery-calculator", "name": "CPAP Machine", "watts": 45, "hours": 8, "surge": 90, "voltage": 12, "desc": "Calculate exact battery capacity (Wh & Ah) and portable power station size needed to run a CPAP machine overnight during camping or power outages."},
    {"slug": "refrigerator-solar-battery-calculator", "name": "Full-Size Refrigerator", "watts": 180, "hours": 10, "surge": 1200, "voltage": 12, "desc": "Estimate the exact solar generator, LiFePO4 battery bank, and pure sine wave inverter needed to keep your refrigerator running during a blackout."},
    {"slug": "starlink-power-consumption-calculator", "name": "Starlink Satellite Internet", "watts": 65, "hours": 12, "surge": 150, "voltage": 12, "desc": "Calculate off-grid solar panel wattage and battery runtime required to power Starlink Gen 2 / Gen 3 dishes continuously for RV and remote work."},
    {"slug": "sump-pump-battery-backup-calculator", "name": "Basement Sump Pump (1/2 HP)", "watts": 800, "hours": 3, "surge": 2100, "voltage": 12, "desc": "Size the right inverter surge rating and deep cycle backup battery capacity to prevent basement flooding during severe storm outages."},
    {"slug": "chest-freezer-solar-generator-calculator", "name": "Deep Chest Freezer", "watts": 100, "hours": 8, "surge": 900, "voltage": 12, "desc": "Find out how many watt-hours and solar panels are required to protect frozen food in a chest freezer during extended grid failures."},
    {"slug": "gaming-pc-ups-battery-calculator", "name": "High-End Gaming PC & Monitor", "watts": 550, "hours": 4, "surge": 750, "voltage": 12, "desc": "Calculate UPS battery backup runtime and portable power station sizing for gaming rigs, workstations, and dual monitor setups."},
    {"slug": "portable-air-conditioner-solar-calculator", "name": "Portable / Window Air Conditioner", "watts": 950, "hours": 5, "surge": 2200, "voltage": 24, "desc": "Determine the battery bank (24V/48V), solar array wattage, and high-surge inverter required to run an air conditioner off-grid."},
    {"slug": "rv-12v-fridge-battery-calculator", "name": "RV 12V Compressor Fridge", "watts": 55, "hours": 14, "surge": 180, "voltage": 12, "desc": "Calculate boondocking battery amp-hours (Ah) and rooftop solar wattage required to run a 12V DC RV refrigerator 24/7."},
    {"slug": "oxygen-concentrator-battery-backup-calculator", "name": "Home Oxygen Concentrator", "watts": 320, "hours": 8, "surge": 600, "voltage": 12, "desc": "Calculate emergency battery backup capacity and solar generator runtime for medical oxygen concentrators during power outages."},
    {"slug": "pellet-stove-battery-backup-calculator", "name": "Pellet Stove Heating System", "watts": 130, "hours": 10, "surge": 450, "voltage": 12, "desc": "Size a pure sine wave battery backup system to keep your pellet stove auger and blower fans heating your home when the grid goes down."},
    {"slug": "well-pump-solar-inverter-calculator", "name": "Submersible Well Pump (3/4 HP)", "watts": 1100, "hours": 2, "surge": 3000, "voltage": 24, "desc": "Calculate high-surge inverter requirements and solar battery bank capacity to maintain running water from a deep well pump off-grid."},
    {"slug": "microwave-inverter-battery-calculator", "name": "Countertop Microwave Oven", "watts": 1200, "hours": 0.5, "surge": 2000, "voltage": 12, "desc": "Determine the exact inverter continuous/surge rating and LiFePO4 battery discharge capacity needed to run a microwave in a camper or van."},
    {"slug": "space-heater-battery-runtime-calculator", "name": "Electric Space Heater (Low/High)", "watts": 1500, "hours": 3, "surge": 1600, "voltage": 24, "desc": "See exact watt-hour consumption and heavy-duty solar generator requirements for running an electric heater off battery power."},
    {"slug": "wifi-router-modem-ups-calculator", "name": "WiFi Router & Fiber Modem", "watts": 20, "hours": 24, "surge": 40, "voltage": 12, "desc": "Calculate how long a mini UPS or portable power station will keep your home internet router and modem online during a power cut."},
    {"slug": "electric-blanket-camping-battery-calculator", "name": "Heated Electric Blanket", "watts": 110, "hours": 8, "surge": 120, "voltage": 12, "desc": "Calculate exact portable power station watt-hours required to stay warm with an electric blanket all night while tent or car camping."},
    {"slug": "coffee-maker-solar-generator-calculator", "name": "Drip & Espresso Coffee Maker", "watts": 1000, "hours": 0.5, "surge": 1200, "voltage": 12, "desc": "Find the minimum inverter wattage and battery capacity needed to brew coffee off-grid in your RV, van, or campsite."},
    {"slug": "tv-home-theater-battery-backup-calculator", "name": "65-Inch LED TV & Soundbar", "watts": 140, "hours": 6, "surge": 250, "voltage": 12, "desc": "Calculate battery backup runtime and portable power station sizing to run your television and entertainment system during blackouts."},
    {"slug": "washing-machine-solar-power-calculator", "name": "Clothes Washing Machine", "watts": 500, "hours": 1.5, "surge": 1500, "voltage": 12, "desc": "Calculate off-grid solar generator and inverter sizing required to run a standard or high-efficiency washing machine."},
    {"slug": "diesel-heater-12v-battery-calculator", "name": "12V Chinese Diesel Air Heater", "watts": 40, "hours": 10, "surge": 150, "voltage": 12, "desc": "Calculate glow-plug startup amp draw and overnight 12V battery amp-hour capacity required for van life and ice fishing diesel heaters."},
    {"slug": "aquarium-filter-heater-battery-backup-calculator", "name": "Aquarium Heater, Pump & Filter", "watts": 220, "hours": 12, "surge": 350, "voltage": 12, "desc": "Protect fish and reef tanks during power outages by calculating exact UPS and LiFePO4 battery backup capacity for heaters and air pumps."},
    {"slug": "induction-cooktop-battery-solar-calculator", "name": "Portable Induction Cooktop", "watts": 1400, "hours": 1, "surge": 1800, "voltage": 24, "desc": "Size the battery bank, BMS amp rating, and solar panels required for flameless electric cooking in a camper van or tiny home."},
    {"slug": "laptop-mobile-workstation-solar-calculator", "name": "Laptop & Portable Monitor Setup", "watts": 85, "hours": 8, "surge": 130, "voltage": 12, "desc": "Calculate portable solar panel and power bank watt-hour requirements for digital nomads working remotely off-grid."},
    {"slug": "ev-level-1-portable-charger-calculator", "name": "Level 1 Portable EV Charger", "watts": 1440, "hours": 4, "surge": 1800, "voltage": 48, "desc": "Calculate expandable home backup battery capacity and solar array output required for emergency off-grid electric vehicle range extension."},
    {"slug": "furnace-blower-fan-battery-backup-calculator", "name": "Gas Furnace Blower Motor", "watts": 600, "hours": 8, "surge": 1800, "voltage": 12, "desc": "Calculate how to power your central gas furnace blower fan using a portable power station or inverter during winter power outages."}
]

# Dynamic daily expansion: adds Wattage/Battery benchmark pages based on day of year
def get_dynamic_wattage_pages():
    base_wattages = [100, 200, 300, 400, 500, 600, 750, 800, 1000, 1200, 1500, 2000, 2500, 3000]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    # Always include at least 10 + unlock more over time
    active_count = min(len(base_wattages), 8 + (day_of_year % 7))
    pages = []
    for w in base_wattages[:active_count]:
        pages.append({
            "slug": f"{w}-watt-solar-battery-calculator",
            "name": f"{w} Watt Continuous Load",
            "watts": w,
            "hours": 5,
            "surge": int(w * 2),
            "voltage": 12 if w <= 1200 else 24,
            "desc": f"Calculate exact battery amp-hours (Ah), watt-hours (Wh), inverter size, and solar panel array required to run a {w}W continuous electrical load."
        })
    return pages

ALL_PAGES = APPLIANCE_PRESETS + get_dynamic_wattage_pages()

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

def generate_faq_data(preset_name, watts, hours):
    total_wh = int(watts * hours * 1.2)
    ah_12v = round(total_wh / 12.8, 1)
    solar_w = int(total_wh / 4)
    return [
        {
            "q": f"What size battery or solar generator do I need for a {preset_name} ({watts}W)?",
            "a": f"To run a {watts}W {preset_name} for {hours} hours, you need at least {watts * hours} Wh of net energy. Factoring in 85% inverter efficiency and LiFePO4 depth-of-discharge safety, we recommend a battery capacity of at least {total_wh} Wh (or {ah_12v} Ah at 12.8V)."
        },
        {
            "q": f"How many solar panels are needed to recharge a battery running a {watts}W load?",
            "a": f"Assuming 4.5 peak sun hours per day and standard MPPT charge controller efficiency, you need approximately {max(100, solar_w)}W to {max(200, int(solar_w * 1.3))}W of solar panels to fully replenish {total_wh} Wh daily."
        },
        {
            "q": "Should I choose a LiFePO4 battery or Lead-Acid (AGM) for backup power?",
            "a": "LiFePO4 (Lithium Iron Phosphate) batteries provide 80–100% usable capacity and 4,000+ charge cycles, whereas Lead-Acid/AGM batteries only allow 50% depth of discharge and last 300–500 cycles. LiFePO4 costs significantly less per cycle."
        },
        {
            "q": "How do I size a pure sine wave inverter for my appliances?",
            "a": f"Your inverter continuous rating should be at least 25% higher than your running watts ({int(watts * 1.25)}W minimum), and its peak surge rating must exceed the startup motor surge of your appliance."
        },
        {
            "q": "Can I plug my appliance directly into a Portable Power Station (Jackery, EcoFlow, Bluetti)?",
            "a": "Yes. All-in-one portable power stations combine a LiFePO4 battery, MPPT solar charge controller, and pure sine wave AC inverter in a single plug-and-play unit—requiring zero wiring."
        }
    ]

def render_html_page(page_data, is_home=False):
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} Solar & Battery Sizing Calculator ({page_data['watts']}W) | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(page_data["name"], page_data["watts"], page_data["hours"])

    # Build FAQ JSON-LD Schema for Rich Snippets on Google & Bing
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {"@type": "Answer", "text": item["a"]}
            } for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    # Render Best Sellers Cards HTML
    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm hover:shadow-md transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-amber-100 text-amber-900 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-600">{prod['rating']}</span>
                </div>
                <span class="text-xs text-slate-500 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-slate-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-slate-600 mb-4 bg-slate-50 p-2.5 rounded-lg border border-slate-100">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    # Render Programmatic Directory Links
    preset_links_html = ""
    for p in ALL_PAGES:
        active_cls = "bg-amber-50 border-amber-400 text-amber-900 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-white border-slate-200 text-slate-700 hover:border-amber-400 hover:text-slate-900"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-slate-400 font-mono shrink-0">{p['watts']}W</span>
        </a>
        """

    # Render FAQ HTML
    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-white border border-slate-200 rounded-xl p-5">
            <h3 class="text-base font-bold text-slate-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-slate-600 leading-relaxed">{item['a']}</p>
        </div>
        """

    hero_deal_link = amz_url("Portable+Power+Station+LiFePO4+Solar+Generator+Deal")
    mid_banner_link = amz_url("LiFePO4+12V+100Ah+Battery+Solar+Panel+Kit")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-white text-slate-900 antialiased selection:bg-amber-200 selection:text-slate-900">

    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-slate-900 text-white py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-slate-800">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-slate-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">Live Deals</span>
            <span>Save up to 35% on LiFePO4 Solar Generators, Backup Batteries & Inverters today on Amazon.</span>
            <a href="{hero_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-400 hover:text-amber-300 underline font-bold ml-1">
                View Active Deals &rarr;
            </a>
        </div>
    </div>

    <!-- NAVIGATION HEADER -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-30">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-amber-500 flex items-center justify-center text-slate-950 font-black text-lg shadow-sm">W</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-slate-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-slate-500 font-medium">Solar & Battery Sizing Engine</span>
                </div>
            </a>
            <nav class="flex items-center gap-5 text-sm font-semibold text-slate-700">
                <a href="#calculator" class="hover:text-amber-600 transition">Calculator</a>
                <a href="#product-search" class="hover:text-amber-600 transition">Product Search</a>
                <a href="#best-sellers" class="hover:text-amber-600 transition">Best Sellers</a>
                <a href="#presets" class="hover:text-amber-600 transition">Appliance Guides</a>
                <a href="#faq" class="hover:text-amber-600 transition">FAQ</a>
            </nav>
        </div>
    </header>

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100 border border-slate-200 text-xs font-semibold text-slate-700">
                <span>⚡ 2026 Engineering-Grade Off-Grid & Backup Calculator</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
                { "Solar, Battery & Inverter Sizing Calculator" if is_home else f"{page_data['name']} Power & Battery Calculator ({page_data['watts']}W)" }
            </h1>
            <p class="text-slate-600 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Calculator Inputs (Left 7 Cols) -->
            <div class="lg:col-span-7 bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-slate-100 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-slate-900">1. Enter Your Load Parameters</h2>
                        <p class="text-xs text-slate-500">Adjust values below or pick a quick appliance preset</p>
                    </div>
                    <span class="text-xs font-mono bg-slate-100 text-slate-700 px-2.5 py-1 rounded font-semibold">Real-Time Calc</span>
                </div>

                <!-- Quick Appliance Selector -->
                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-2">Quick Select Appliance Preset</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-2.5 text-sm font-medium text-slate-900 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
                        <option value="{page_data['watts']},{page_data['hours']},{page_data['surge']},{page_data['voltage']}">Current: {page_data['name']} ({page_data['watts']}W)</option>
                        <option value="45,8,90,12">CPAP Machine (45W | 8 hrs)</option>
                        <option value="180,10,1200,12">Full-Size Refrigerator (180W | 10 hrs)</option>
                        <option value="65,12,150,12">Starlink Satellite Dish (65W | 12 hrs)</option>
                        <option value="800,3,2100,12">Sump Pump 1/2 HP (800W | 3 hrs)</option>
                        <option value="550,4,750,12">Gaming PC + Monitor (550W | 4 hrs)</option>
                        <option value="950,5,2200,24">Window / Portable AC (950W | 5 hrs)</option>
                        <option value="1500,2,1600,24">Electric Space Heater (1500W | 2 hrs)</option>
                        <option value="100,8,900,12">Deep Chest Freezer (100W | 8 hrs)</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="wattsInput" class="block text-sm font-bold text-slate-800 mb-1">Running Power (Watts)</label>
                        <input type="number" id="wattsInput" value="{page_data['watts']}" min="1" max="25000" oninput="calculatePower()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
                        <span class="text-[11px] text-slate-500">Continuous wattage drawn by device</span>
                    </div>

                    <div>
                        <label for="hoursInput" class="block text-sm font-bold text-slate-800 mb-1">Daily Runtime (Hours/Day)</label>
                        <input type="number" id="hoursInput" value="{page_data['hours']}" min="0.1" max="24" step="0.5" oninput="calculatePower()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
                        <span class="text-[11px] text-slate-500">Hours per day the device stays on</span>
                    </div>

                    <div>
                        <label for="surgeInput" class="block text-sm font-bold text-slate-800 mb-1">Startup Surge Watts (Peak)</label>
                        <input type="number" id="surgeInput" value="{page_data['surge']}" min="1" max="50000" oninput="calculatePower()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
                        <span class="text-[11px] text-slate-500">Peak startup spike (compressors/motors)</span>
                    </div>

                    <div>
                        <label for="voltageInput" class="block text-sm font-bold text-slate-800 mb-1">Battery System Voltage</label>
                        <select id="voltageInput" onchange="calculatePower()" class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
                            <option value="12" {"selected" if page_data['voltage'] == 12 else ""}>12V System (Standard RV / Portable)</option>
                            <option value="24" {"selected" if page_data['voltage'] == 24 else ""}>24V System (Mid-Size Cabin / 1500W+)</option>
                            <option value="48" {"selected" if page_data['voltage'] == 48 else ""}>48V System (Whole Home / Server Rack)</option>
                        </select>
                        <span class="text-[11px] text-slate-500">DC battery bank nominal voltage</span>
                    </div>

                    <div>
                        <label for="chemInput" class="block text-sm font-bold text-slate-800 mb-1">Battery Chemistry (DoD)</label>
                        <select id="chemInput" onchange="calculatePower()" class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-sm font-semibold text-slate-900 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
                            <option value="0.85" selected>LiFePO4 Lithium (85% Safe DoD + Inverter Loss)</option>
                            <option value="0.50">Lead-Acid / AGM / Gel (50% Max DoD)</option>
                        </select>
                    </div>

                    <div>
                        <label for="sunHoursInput" class="block text-sm font-bold text-slate-800 mb-1">Peak Sun Hours / Day</label>
                        <select id="sunHoursInput" onchange="calculatePower()" class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-sm font-semibold text-slate-900 focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
                            <option value="3.5">3.5 Hours (Winter / Northern Cloudy)</option>
                            <option value="4.5" selected>4.5 Hours (US Average Sun)</option>
                            <option value="5.5">5.5 Hours (Sunny Southwest / Summer)</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Calculator Output + Dynamic Amazon Recommendation (Right 5 Cols) -->
            <div class="lg:col-span-5 bg-white border-2 border-amber-400 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-slate-100 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-amber-600">2. Engineered System Sizing</span>
                    <h2 class="text-xl font-extrabold text-slate-900">Your Required Power Specs</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-500 font-medium block">Daily Energy Used</span>
                        <span id="resNetWh" class="text-2xl font-black text-slate-900">0 Wh</span>
                    </div>
                    <div class="bg-amber-50 border border-amber-200 rounded-xl p-3.5">
                        <span class="text-xs text-amber-900 font-semibold block">Min. Battery Capacity</span>
                        <span id="resRecWh" class="text-2xl font-black text-amber-700">0 Wh</span>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-500 font-medium block">Battery Amp-Hours</span>
                        <span id="resAh" class="text-xl font-extrabold text-slate-900">0 Ah</span>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-500 font-medium block">Recommended Solar</span>
                        <span id="resSolarW" class="text-xl font-extrabold text-emerald-700">0 Watts</span>
                    </div>
                </div>

                <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5 flex items-center justify-between">
                    <span class="text-xs font-bold text-slate-700">Recommended Pure Sine Inverter:</span>
                    <span id="resInverterW" class="text-sm font-black text-slate-900 bg-white px-2.5 py-1 rounded border border-slate-200">0W Continuous</span>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-amber-50/70 border-2 border-amber-300 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-amber-400 text-slate-950 px-2 py-0.5 rounded">Best Match For Your Load</span>
                        <span class="text-xs font-bold text-slate-600">Amazon Verified</span>
                    </div>
                    <h3 id="recProductTitle" class="text-base font-extrabold text-slate-900 leading-snug">Loading Recommendation...</h3>
                    <p id="recProductDesc" class="text-xs text-slate-600"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-amber-500 hover:bg-amber-600 text-slate-950 font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           View Recommended Power Station &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-white hover:bg-slate-100 text-slate-800 border border-slate-300 font-bold text-xs py-3 px-3 rounded-lg transition">
                           Compare DIY LiFePO4 Battery
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-slate-900">Search Solar Generators, Batteries & Inverters</h2>
                <p class="text-sm text-slate-600">Search any wattage, brand (Jackery, EcoFlow, Bluetti, LiTime, Renogy, Victron), or backup component to check real-time Amazon prices and specifications.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. 1000W Portable Power Station, 12V 200Ah LiFePO4 Battery, 2000W Pure Sine Inverter..."
                           class="flex-1 bg-white border-2 border-slate-300 rounded-xl px-4 py-3 text-sm font-medium text-slate-900 focus:outline-none focus:border-amber-500" required>
                    <button type="submit" class="bg-slate-900 hover:bg-slate-800 text-white font-bold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-slate-400 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('LiFePO4 Solar Generator 1000W')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-amber-100 text-slate-700 rounded-full transition">1000W Solar Generator</a>
                    <a href="{amz_url('12V 100Ah LiFePO4 Lithium Battery')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-amber-100 text-slate-700 rounded-full transition">12V 100Ah LiFePO4</a>
                    <a href="{amz_url('200W Portable Folding Solar Panel')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-amber-100 text-slate-700 rounded-full transition">200W Folding Solar Panel</a>
                    <a href="{amz_url('Pure Sine Wave Inverter 2000W 12V')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-amber-100 text-slate-700 rounded-full transition">2000W Sine Wave Inverter</a>
                    <a href="{amz_url('Automatic Transfer Switch UPS Battery Backup')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-amber-100 text-slate-700 rounded-full transition">Home UPS Backup</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-slate-200 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-amber-600">Verified High-Efficiency Hardware</span>
                    <h2 class="text-2xl font-extrabold text-slate-900">Best-Selling Solar Generators, Batteries & Inverters</h2>
                </div>
                <a href="{amz_url('Best Selling Portable Power Stations and Solar Batteries')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-amber-600 hover:text-amber-700">
                    Browse Full Amazon Best Sellers List &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL BANNER -->
        <section class="bg-slate-50 border-2 border-amber-400 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-amber-400 text-slate-950 px-2.5 py-1 rounded">DIY Off-Grid Bundle Guide</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-slate-900">Building a Custom 12V/24V/48V LiFePO4 Solar Bank?</h2>
                <p class="text-sm text-slate-600">Save up to 40% per Watt-Hour by pairing a Grade-A 12V 100Ah/280Ah LiFePO4 deep-cycle battery with an MPPT solar controller and pure sine wave inverter.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-amber-500 hover:bg-amber-600 text-slate-950 font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore DIY Battery & Solar Kits on Amazon &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO APPLIANCE CALCULATOR DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-slate-200 pb-3">
                <h2 class="text-xl font-extrabold text-slate-900">Appliance & Wattage Specific Calculators</h2>
                <p class="text-xs text-slate-500">Select any appliance or wattage load below for pre-configured battery runtime, inverter surge, and solar sizing calculations.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-slate-200 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-amber-600">Technical Knowledge Base</span>
                <h2 class="text-2xl font-extrabold text-slate-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

    </main>

    <!-- FOOTER -->
    <footer class="bg-white border-t border-slate-200 mt-16 py-10 px-4 text-xs text-slate-500">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-slate-800">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex gap-4 font-medium text-slate-600">
                <a href="{BASE_URL}/" class="hover:text-slate-900">Home</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-slate-900">Sitemap</a>
                <a href="#calculator" class="hover:text-slate-900">Calculator</a>
                <a href="#faq" class="hover:text-slate-900">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 4) {{
                document.getElementById("wattsInput").value = parts[0];
                document.getElementById("hoursInput").value = parts[1];
                document.getElementById("surgeInput").value = parts[2];
                document.getElementById("voltageInput").value = parts[3];
                calculatePower();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculatePower() {{
            const watts = parseFloat(document.getElementById("wattsInput").value) || 0;
            const hours = parseFloat(document.getElementById("hoursInput").value) || 0;
            const surge = parseFloat(document.getElementById("surgeInput").value) || 0;
            const voltage = parseFloat(document.getElementById("voltageInput").value) || 12;
            const effFactor = parseFloat(document.getElementById("chemInput").value) || 0.85;
            const sunHours = parseFloat(document.getElementById("sunHoursInput").value) || 4.5;

            const netWh = Math.round(watts * hours);
            const requiredWh = Math.round(netWh / effFactor);
            const nominalV = voltage === 12 ? 12.8 : (voltage === 24 ? 25.6 : 51.2);
            const requiredAh = Math.ceil(requiredWh / nominalV);
            const solarWatts = Math.ceil((requiredWh / sunHours) * 1.25);
            const minInverterContinuous = Math.max(Math.ceil((watts * 1.25) / 100) * 100, Math.ceil(surge / 2));

            document.getElementById("resNetWh").textContent = netWh.toLocaleString() + " Wh";
            document.getElementById("resRecWh").textContent = requiredWh.toLocaleString() + " Wh";
            document.getElementById("resAh").textContent = requiredAh.toLocaleString() + " Ah @ " + voltage + "V";
            document.getElementById("resSolarW").textContent = solarWatts.toLocaleString() + " W";
            document.getElementById("resInverterW").textContent = minInverterContinuous.toLocaleString() + "W (Surge " + surge + "W+)";

            let recTitle = "";
            let recDesc = "";
            let primaryQuery = "";
            let secondaryQuery = "";

            if (requiredWh <= 350 && minInverterContinuous <= 600) {{
                recTitle = "300Wh–500Wh Compact LiFePO4 Portable Power Station (600W Output)";
                recDesc = "Ideal for CPAP machines, laptops, Starlink, WiFi routers, and overnight camping loads.";
                primaryQuery = "Portable Power Station 300Wh 500Wh LiFePO4 Bluetti Jackery EcoFlow";
                secondaryQuery = "12V 50Ah LiFePO4 Lithium Battery Deep Cycle";
            }} else if (requiredWh <= 1250 && minInverterContinuous <= 1800) {{
                recTitle = "1000Wh–1500Wh LiFePO4 Solar Generator (1800W AC Inverter)";
                recDesc = "Best-selling tier for full-size refrigerators, chest freezers, gaming PCs, sump pumps, and home backup.";
                primaryQuery = "1000Wh LiFePO4 Portable Power Station Jackery 1000 v2 EcoFlow Delta 2";
                secondaryQuery = "12V 100Ah LiFePO4 Battery Built-in BMS";
            }} else if (requiredWh <= 2600) {{
                recTitle = "2000Wh–3000Wh Heavy-Duty Expandable Solar Power Station";
                recDesc = "Built for high-draw appliances including portable air conditioners, microwaves, space heaters, and RVs.";
                primaryQuery = "2000Wh 3000Wh LiFePO4 Portable Power Station Solar Generator";
                secondaryQuery = "12V 200Ah LiFePO4 Lithium Battery Plus 2000W Pure Sine Inverter";
            }} else {{
                recTitle = "3600Wh+ Whole-Home Modular LiFePO4 Backup System / 48V Server Rack";
                recDesc = "High-capacity energy storage for extended multi-day blackouts, well pumps, and heavy off-grid loads.";
                primaryQuery = "3600Wh Expandable Home Battery Backup EcoFlow Delta Pro Bluetti";
                secondaryQuery = "48V 100Ah Server Rack LiFePO4 Battery 5.12kWh";
            }}

            document.getElementById("recProductTitle").textContent = recTitle;
            document.getElementById("recProductDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(primaryQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(secondaryQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculatePower);
    </script>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.8"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    # Write IndexNow verification key file
    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        print("Skipping IndexNow ping on template placeholder URL.")
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice (non-fatal): {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage (Defaulting to Refrigerator / General Backup Preset)
    home_preset = {
        "slug": "index",
        "name": "Home & Off-Grid Appliance",
        "watts": 250,
        "hours": 8,
        "surge": 1000,
        "voltage": 12,
        "desc": "Calculate exact battery capacity (Wh & Ah), pure sine wave inverter wattage, and solar panel array size for any appliance—plus compare verified Amazon power stations."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_html_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate All Programmatic SEO Appliance & Wattage Pages
    for page in ALL_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_html_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 3. Generate Sitemap, Robots.txt & IndexNow Key
    generate_sitemap_and_robots(generated_urls)

    # 4. Automatically Ping Search Engines (Bing, Yahoo, DuckDuckGo, Yandex via IndexNow)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} SEO calculator pages in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
