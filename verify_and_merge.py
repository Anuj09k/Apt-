import json

# Load official built_features_list.json
official = json.load(open("built_features_list.json", encoding="utf-8"))

# Load all 7 groups
merged = {}
for g in [1, 2, 3, 4, 5, 6, 7]:
    data = json.load(open(f"plain_english_group{g}.json", encoding="utf-8"))
    merged.update(data)

print(f"Total categories in merged dictionary: {len(merged)}")
total_entries = sum(len(features) for features in merged.values())
print(f"Total feature entries in merged dictionary: {total_entries}")

# Verification against official list
missing_cats = []
missing_feats = []
verified_data = []

total_official_features = 0

for cat_obj in official:
    cat_name = cat_obj["category"]
    features = cat_obj["features"]
    total_official_features += len(features)
    
    if cat_name not in merged:
        missing_cats.append(cat_name)
        continue
    
    cat_dict = merged[cat_name]
    cat_result = {
        "category": cat_name,
        "page": cat_obj.get("page", "1"),
        "features": []
    }
    
    for feat in features:
        if feat not in cat_dict:
            missing_feats.append((cat_name, feat))
        else:
            anchor, meaning = cat_dict[feat]
            cat_result["features"].append({
                "name": feat,
                "status": "built",
                "memory_anchor": anchor,
                "human_meaning": meaning
            })
    
    verified_data.append(cat_result)

print(f"Official total features: {total_official_features}")
if missing_cats:
    print(f"ERROR: Missing categories: {missing_cats}")
if missing_feats:
    print(f"ERROR: Missing features: {missing_feats}")

if not missing_cats and not missing_feats:
    print("SUCCESS: 100% of all 417 built features matched perfectly!")
    with open("built_features_complete_dictionary.json", "w", encoding="utf-8") as f:
        json.dump(verified_data, f, indent=2)
    print("Saved verified data to built_features_complete_dictionary.json")
