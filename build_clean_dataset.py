import json

with open("structured_features.json", "r", encoding="utf-8") as f:
    raw_pages = json.load(f)

# Clean up any non-section entries and build final data
pages_data = {}

for p_str, sects in raw_pages.items():
    p_num = int(p_str)
    clean_sects = []
    for s in sects:
        name = s["name"].strip()
        feats = s["features"]
        # filter out empty trailing objective fragments
        if not feats or name.endswith("calculations.") or "stated confidence" in name:
            continue
        clean_feats = []
        for f in feats:
            fn = f["name"].strip()
            st = f["status"].strip()
            clean_feats.append({"name": fn, "status": st})
        clean_sects.append({"name": name, "features": clean_feats})
    pages_data[p_num] = clean_sects

# Apply our updates:
# Page 5 (V1 - Reports): Add 2 built features
reports_sec = None
for s in pages_data[5]:
    if s["name"] == "Reports":
        reports_sec = s
        break
if reports_sec:
    reports_sec["features"].extend([
        {"name": "Tower Floor Plans PDF Report", "status": "built"},
        {"name": "Floor Plan Image & ZIP Export", "status": "built"}
    ])

# Page 8 (V2.5 - 3D & Visualisation): Add 2 built features
vis_sec = None
for s in pages_data[8]:
    if s["name"] == "3D & Visualisation":
        vis_sec = s
        break
if vis_sec:
    vis_sec["features"].extend([
        {"name": "Presentation-Grade Furnished 2D Blueprint Engine", "status": "built"},
        {"name": "Structural Wall Poché & Dimension Badges", "status": "built"}
    ])

# Page 15 (X+ - Generative Design): Mark AI-Generated 2D Floor Plans and 3D Concepts as Built!
gen_sec = None
for s in pages_data[15]:
    if s["name"] == "Generative Design":
        gen_sec = s
        break
if gen_sec:
    for f in gen_sec["features"]:
        if f["name"] == "AI-Generated 2D Floor Plans":
            f["status"] = "built"
        elif f["name"] == "AI-Generated 3D Building Concepts":
            f["status"] = "built"

# Write out feature_data.py
with open("feature_data.py", "w", encoding="utf-8") as f:
    f.write("# Cleaned and updated feature database for Aptimizer Complete Feature List\n\n")
    f.write("PAGES_DATA = " + json.dumps(pages_data, indent=2) + "\n")

print("Successfully generated feature_data.py")
