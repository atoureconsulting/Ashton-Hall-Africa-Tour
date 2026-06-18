#!/usr/bin/env python3
# Generates a branded, self-contained itinerary.html for the Ashton Hall Africa Tour.
import base64, re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
B64 = (HERE / "assets" / "atoure-A-mono.b64").read_text().strip()

# ---- data ---------------------------------------------------------------
legs = [
    dict(idx="01", flag="🇨🇲", name="Cameroon", tag="Arrival", dates="28 to 29 Jun", days=2,
         days_list=[
            dict(n="Day 1", date="28 Jun · Sun", type="arrival", title="Arrival",
                 items=["Flight USA to Cameroon. Arrival airport TBC, likely Douala. Long haul, airline and flight number TBC. Arrive approximately 8 to 9pm.",
                        "Airport pickup on landing, then direct transfer to the hotel. Hotel TBC.",
                        "Check in and rest.",
                        "Full team debrief at the hotel.",
                        "Security handover: head of security meets the Cameroon ground security team and sets the Day 2 protocol. Local contact TBC.",
                        "Overnight at the hotel."]),
            dict(n="Day 2", date="29 Jun · Mon", type="stream", title="Experience and stream",
                 items=["Breakfast and prep in the morning.",
                        "Afternoon: experience and live stream. Content TBC. Approximately 3 to 5 hours.",
                        "Return to the hotel after the stream. Evening rest."]),
         ], nextc="Ghana"),
    dict(idx="02", flag="🇬🇭", name="Ghana", tag="4 days", dates="30 Jun to 3 Jul", days=4,
         days_list=[
            dict(n="Day 1", date="30 Jun · Tue", type="arrival", title="Travel and arrival",
                 items=["Flight Cameroon to Ghana. Airline and flight number TBC. Arrive in the evening.",
                        "Arrival routine: pickup, hotel, team debrief, security handover. Hotel and local security contact TBC.",
                        "Overnight at the hotel."]),
            dict(n="Day 2", date="1 Jul · Wed", type="stream", title="Experience and stream",
                 items=["Breakfast and prep in the morning.",
                        "Afternoon: experience and live stream. Content TBC. Approximately 3 to 5 hours.",
                        "Return to the hotel. Overnight."]),
            dict(n="Day 3", date="2 Jul · Thu", type="tbc", title="Open day",
                 items=["Plan TBC. To decide: second experience and stream, rest day, or secondary activation."]),
            dict(n="Day 4", date="3 Jul · Fri", type="tbc", title="Open day",
                 items=["Plan TBC."]),
         ], nextc="Nigeria"),
    dict(idx="03", flag="🇳🇬", name="Nigeria", tag="4 days", dates="4 to 7 Jul", days=4,
         days_list=[
            dict(n="Day 1", date="4 Jul · Sat", type="arrival", title="Travel and arrival",
                 items=["Flight Ghana to Nigeria. Airline and flight number TBC. Arrive in the evening.",
                        "Arrival routine: pickup, hotel, team debrief, security handover. Hotel and local security contact TBC.",
                        "Overnight at the hotel."]),
            dict(n="Day 2", date="5 Jul · Sun", type="stream", title="Experience and stream",
                 items=["Breakfast and prep in the morning.",
                        "Afternoon: experience and live stream. Content TBC. Approximately 3 to 5 hours.",
                        "Return to the hotel. Overnight."]),
            dict(n="Day 3", date="6 Jul · Mon", type="tbc", title="Open day",
                 items=["Plan TBC. To decide: second experience and stream, rest day, or secondary activation."]),
            dict(n="Day 4", date="7 Jul · Tue", type="tbc", title="Open day",
                 items=["Plan TBC."]),
         ], nextc="Benin"),
    dict(idx="04", flag="🇧🇯", name="Benin", tag="2 days", dates="8 to 9 Jul", days=2,
         days_list=[
            dict(n="Day 1", date="8 Jul · Wed", type="arrival", title="Travel and arrival",
                 items=["Flight Nigeria to Benin. Airline and flight number TBC. Arrive in the evening.",
                        "Arrival routine: pickup, hotel, team debrief, security handover. Hotel and local security contact TBC.",
                        "Overnight at the hotel."]),
            dict(n="Day 2", date="9 Jul · Thu", type="stream", title="Experience and stream",
                 items=["Breakfast and prep in the morning.",
                        "Afternoon: experience and live stream. Content TBC. Approximately 3 to 5 hours.",
                        "Return to the hotel. Overnight."]),
         ], nextc="Ivory Coast"),
    dict(idx="05", flag="🇨🇮", name="Ivory Coast", tag="3 days", dates="10 to 12 Jul", days=3,
         days_list=[
            dict(n="Day 1", date="10 Jul · Fri", type="arrival", title="Travel and arrival",
                 items=["Flight Benin to Ivory Coast. Airline and flight number TBC. Arrive in the evening.",
                        "Arrival routine: pickup, hotel, team debrief, security handover. Hotel and local security contact TBC.",
                        "Overnight at the hotel."]),
            dict(n="Day 2", date="11 Jul · Sat", type="stream", title="Experience and stream",
                 items=["Breakfast and prep in the morning.",
                        "Afternoon: experience and live stream. Content TBC. Approximately 3 to 5 hours.",
                        "Return to the hotel. Overnight."]),
            dict(n="Day 3", date="12 Jul · Sun", type="tbc", title="Open day",
                 items=["Plan TBC. To decide: second experience and stream, rest day, or secondary activation."]),
         ], nextc="Ethiopia"),
    dict(idx="06", flag="🇪🇹", name="Ethiopia", tag="3 days", dates="13 to 15 Jul", days=3,
         days_list=[
            dict(n="Day 1", date="13 Jul · Mon", type="arrival", title="Travel and arrival",
                 items=["Flight Ivory Coast to Ethiopia. Airline and flight number TBC. Arrive in the evening.",
                        "Arrival routine: pickup, hotel, team debrief, security handover. Hotel and local security contact TBC.",
                        "Overnight at the hotel."]),
            dict(n="Day 2", date="14 Jul · Tue", type="stream", title="Experience and stream",
                 items=["Breakfast and prep in the morning.",
                        "Afternoon: experience and live stream. Content TBC. Approximately 3 to 5 hours.",
                        "Return to the hotel. Overnight."]),
            dict(n="Day 3", date="15 Jul · Wed", type="tbc", title="Open day",
                 items=["Plan TBC. To decide: second experience and stream, rest day, or secondary activation."]),
         ], nextc="Cameroon"),
    dict(idx="07", flag="🇨🇲", name="Cameroon", tag="Departure", dates="16 to 17 Jul", days=2,
         days_list=[
            dict(n="Day 1", date="16 Jul · Thu", type="arrival", title="Travel and arrival",
                 items=["Flight Ethiopia to Cameroon. Airline and flight number TBC. Arrive in the evening.",
                        "Arrival routine: pickup, hotel, team debrief, security handover. Hotel and local security contact TBC.",
                        "Overnight at the hotel."]),
            dict(n="Day 2", date="17 Jul · Fri", type="depart", title="Final stream and departure",
                 items=["Breakfast and prep in the morning.",
                        "Afternoon: experience and live stream. Content TBC. Approximately 3 to 5 hours.",
                        "Departure: return flight home. Timing TBC, same evening or the next morning."]),
         ], nextc=None),
]

route = [(l["flag"], l["name"], f'{l["days"]}d') for l in legs]

conventions = [
    "Arrival is always in the evening. Day 1 of each country is a travel and arrival day.",
    "Arrival routine: airport pickup, direct transfer to the hotel, check in, full team debrief, and a security handover where our head of security briefs the local ground security team and sets the next day protocol.",
    "Experience and live stream run in the afternoon, to overlap the US morning with the local afternoon and evening. This holds for both 2 day and 3 day stays.",
    "Each stream runs approximately 3 to 5 hours.",
    "Experience and stream content is TBC while curation is finalised.",
    "Flights are shown for planning. Nothing is booked yet, so all flight details are TBC.",
]

open_items = [
    "Day counts per country (all provisional).",
    "Hotel per country.",
    "Local ground security contact per country.",
    "Experience and stream content per country.",
    "Flight legs: airlines, flight numbers and exact times.",
    "Cameroon arrival airport: Douala or Yaounde.",
    "Plan for the open days in Ghana and Nigeria.",
    "Final Cameroon departure timing.",
    "Re sync the cost proposal to this route: Benin, Ivory Coast and Ethiopia in, Morocco out.",
]

# ---- helpers ------------------------------------------------------------
def tbc(s):  # highlight standalone TBC
    return re.sub(r"\bTBC\b", '<span class="tbc">TBC</span>', s)

phase_glyph = {"arrival":"✈", "stream":"●", "tbc":"○", "depart":"⌂"}
phase_word  = {"arrival":"Arrival", "stream":"Stream", "tbc":"Open", "depart":"Departure"}

def render_day(d):
    items = "".join(f"<li>{tbc(x)}</li>" for x in d["items"])
    return f"""
      <div class="day {d['type']}">
        <div class="dot"></div>
        <div class="day-body">
          <div class="day-top">
            <span class="day-label">{d['n']} &middot; {d['date']}</span>
            <span class="chip chip-{d['type']}">{phase_glyph[d['type']]} {phase_word[d['type']]}</span>
          </div>
          <div class="day-title">{d['title']}</div>
          <ul class="day-items">{items}</ul>
        </div>
      </div>"""

def render_leg(l):
    days = "".join(render_day(d) for d in l["days_list"])
    nxt = f'<div class="leg-foot">&#8594; Travel to {l["nextc"]}, arriving in the evening</div>' if l["nextc"] else \
          '<div class="leg-foot">&#9873; Tour ends &middot; return flight home</div>'
    return f"""
    <section class="leg">
      <div class="leg-head">
        <div class="leg-id">{l['idx']}</div>
        <div class="leg-title"><span class="leg-flag">{l['flag']}</span>{l['name']}</div>
        <div class="leg-meta"><div class="leg-dates">{l['dates']}</div><div class="leg-days">{l['tag']}</div></div>
      </div>
      <div class="timeline">{days}</div>
      {nxt}
    </section>"""

route_html = ""
for i,(fl,nm,dd) in enumerate(route):
    route_html += f'<div class="stop"><div class="stop-flag">{fl}</div><div class="stop-name">{nm}</div><div class="stop-days">{dd}</div></div>'
    if i < len(route)-1:
        route_html += '<div class="stop-arr">&#8594;</div>'

conv_html = "".join(f"<li>{tbc(c)}</li>" for c in conventions)
open_html = "".join(f"<li>{tbc(c)}</li>" for c in open_items)
legs_html = "".join(render_leg(l) for l in legs)

# ---- template -----------------------------------------------------------
html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,500&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--ink:#0d0c0a;--paper:#FEFCF8;--cream:#FAF6EE;--sand:#F5EDD6;--gold:#C8A951;--gold-lt:#E0C47A;--gold-dk:#9A7D30;--muted:#9A8870;--line:#e7ddc7;--text:#5C5040;}}
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{background:#e9e0cf;font-family:'Jost',sans-serif;color:var(--text);padding:40px 0;-webkit-font-smoothing:antialiased;}}
.sheet{{width:900px;margin:0 auto;background:var(--paper);box-shadow:0 24px 70px rgba(40,30,10,.22);overflow:hidden;}}
.serif{{font-family:'Cormorant Garamond',serif;}}
/* header */
header{{position:relative;background:linear-gradient(160deg,#16130c,#0d0c0a);padding:46px 56px 40px;text-align:center;}}
.logo-mono{{position:absolute;top:50%;left:46px;transform:translateY(-50%);height:74px;}}
.eyebrow{{font-size:13px;letter-spacing:.46em;color:var(--gold);text-transform:uppercase;font-weight:500;}}
header h1{{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:62px;color:var(--paper);line-height:1.02;margin:8px 0 6px;letter-spacing:.5px;}}
.sub{{font-size:12.5px;letter-spacing:.34em;text-transform:uppercase;color:#cbb888;}}
.rule{{width:62px;height:2px;background:var(--gold);margin:20px auto 0;}}
/* stats */
.stats{{display:flex;border-bottom:1px solid var(--line);background:var(--cream);}}
.stat{{flex:1;text-align:center;padding:18px 8px;border-right:1px solid var(--line);}}
.stat:last-child{{border-right:none;}}
.stat .v{{font-family:'Cormorant Garamond',serif;font-size:26px;font-weight:600;color:var(--ink);line-height:1;}}
.stat .l{{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-top:6px;}}
/* body wrap */
.wrap{{padding:34px 56px 12px;}}
.seclabel{{font-size:11px;letter-spacing:.34em;text-transform:uppercase;color:var(--gold-dk);font-weight:600;margin-bottom:14px;}}
/* route strip */
.route{{display:flex;align-items:center;justify-content:space-between;background:var(--cream);border:1px solid var(--line);border-radius:4px;padding:16px 14px;margin-bottom:30px;}}
.stop{{text-align:center;flex:0 0 auto;width:84px;}}
.stop-flag{{font-size:24px;line-height:1;}}
.stop-name{{font-family:'Cormorant Garamond',serif;font-size:16px;font-weight:600;color:var(--ink);margin-top:3px;line-height:1.05;}}
.stop-days{{font-size:10px;letter-spacing:.14em;color:var(--muted);text-transform:uppercase;margin-top:2px;}}
.stop-arr{{color:var(--gold);font-size:15px;flex:1;text-align:center;}}
/* conventions */
.callout{{background:var(--sand);border-left:3px solid var(--gold);border-radius:3px;padding:18px 22px 18px 24px;margin-bottom:36px;}}
.callout ul{{list-style:none;}}
.callout li{{position:relative;padding-left:20px;font-size:13px;line-height:1.5;color:#5a4f3c;margin:7px 0;}}
.callout li::before{{content:"";position:absolute;left:0;top:8px;width:7px;height:7px;background:var(--gold);transform:rotate(45deg);}}
/* legs */
.leg{{margin-bottom:34px;}}
.leg-head{{position:relative;display:flex;align-items:flex-end;gap:14px;border-bottom:2px solid var(--gold);padding-bottom:10px;margin-bottom:20px;}}
.leg-id{{font-family:'Cormorant Garamond',serif;font-size:46px;font-weight:600;color:var(--gold-lt);line-height:.8;}}
.leg-title{{font-family:'Cormorant Garamond',serif;font-size:32px;font-weight:600;color:var(--ink);line-height:1;display:flex;align-items:center;gap:11px;}}
.leg-flag{{font-size:27px;}}
.leg-meta{{margin-left:auto;text-align:right;}}
.leg-dates{{font-size:14px;letter-spacing:.05em;color:var(--text);}}
.leg-days{{font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--gold-dk);margin-top:3px;font-weight:500;}}
/* timeline */
.timeline{{position:relative;margin-left:9px;border-left:2px solid var(--line);padding-left:30px;}}
.day{{position:relative;padding-bottom:22px;}}
.day:last-child{{padding-bottom:4px;}}
.dot{{position:absolute;left:-39px;top:2px;width:15px;height:15px;border-radius:50%;background:var(--paper);border:2px solid var(--gold);}}
.day.stream .dot{{background:var(--gold);}}
.day.depart .dot{{background:var(--gold-dk);border-color:var(--gold-dk);box-shadow:0 0 0 3px var(--sand);}}
.day.tbc .dot{{border-color:var(--muted);width:12px;height:12px;left:-37px;top:4px;}}
.day-top{{display:flex;align-items:center;gap:12px;margin-bottom:4px;}}
.day-label{{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);font-weight:500;}}
.chip{{font-size:9.5px;letter-spacing:.13em;text-transform:uppercase;font-weight:600;padding:3px 9px;border-radius:20px;}}
.chip-arrival{{background:var(--sand);color:var(--gold-dk);}}
.chip-stream{{background:var(--gold);color:#241d08;}}
.chip-tbc{{background:transparent;color:var(--muted);border:1px dashed var(--muted);}}
.chip-depart{{background:var(--ink);color:var(--gold);}}
.day-title{{font-family:'Cormorant Garamond',serif;font-size:21px;font-weight:600;color:var(--ink);line-height:1.1;margin-bottom:6px;}}
.day-items{{list-style:none;}}
.day-items li{{position:relative;padding-left:16px;font-size:13px;line-height:1.5;color:var(--text);margin:4px 0;}}
.day-items li::before{{content:"";position:absolute;left:0;top:8px;width:5px;height:5px;border-radius:50%;background:var(--gold-lt);}}
.tbc{{display:inline-block;background:#efe2bd;color:var(--gold-dk);font-size:10.5px;font-weight:600;letter-spacing:.06em;padding:1px 6px;border-radius:3px;vertical-align:1px;}}
.leg-foot{{margin:14px 0 0 39px;font-size:12px;letter-spacing:.05em;color:var(--gold-dk);font-style:italic;font-family:'Cormorant Garamond',serif;font-size:15px;}}
/* open items */
.open{{background:var(--cream);border:1px solid var(--line);border-radius:4px;padding:24px 28px;margin:8px 0 6px;}}
.open ol{{margin-left:0;padding-left:0;list-style:none;counter-reset:oi;columns:2;column-gap:34px;}}
.open li{{counter-increment:oi;position:relative;padding-left:26px;font-size:12.5px;line-height:1.45;margin:6px 0;break-inside:avoid;color:#5a4f3c;}}
.open li::before{{content:counter(oi);position:absolute;left:0;top:0;font-family:'Cormorant Garamond',serif;font-weight:600;font-size:14px;color:var(--gold-dk);width:18px;height:18px;border:1px solid var(--gold);border-radius:50%;text-align:center;line-height:17px;}}
/* footer */
footer{{background:linear-gradient(160deg,#16130c,#0d0c0a);color:#8a7d5f;display:flex;justify-content:space-between;padding:18px 56px;margin-top:30px;font-size:10.5px;letter-spacing:.26em;text-transform:uppercase;}}
footer .g{{color:var(--gold);}}
</style></head>
<body>
  <div class="sheet">
    <header>
      <img class="logo-mono" src="data:image/png;base64,{B64}" alt="Atoure">
      <div class="eyebrow">Atoure Consulting</div>
      <h1>Itinerary</h1>
      <div class="sub">Day by Day &middot; Ashton Hall Africa Tour</div>
      <div class="rule"></div>
    </header>

    <div class="stats">
      <div class="stat"><div class="v">11</div><div class="l">Travellers</div></div>
      <div class="stat"><div class="v">7</div><div class="l">Countries</div></div>
      <div class="stat"><div class="v">20</div><div class="l">Days</div></div>
      <div class="stat"><div class="v serif">28 Jun &ndash; 17 Jul</div><div class="l">2026</div></div>
    </div>

    <div class="wrap">
      <div class="seclabel">The Route</div>
      <div class="route">{route_html}</div>

      <div class="seclabel">How Each Day Runs</div>
      <div class="callout"><ul>{conv_html}</ul></div>

      <div class="seclabel">Day by Day</div>
      {legs_html}

      <div class="seclabel">Open Items to Confirm</div>
      <div class="open"><ol>{open_html}</ol></div>
    </div>

    <footer><span>Atoure Consulting</span><span class="g">Working Draft &middot; Figures Indicative</span></footer>
  </div>
</body></html>"""

out = HERE / "itinerary.html"
out.write_text(html, encoding="utf-8")
print("wrote", out, len(html), "bytes")
