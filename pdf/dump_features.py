import json

data = json.load(open("built_features_list.json", encoding="utf-8"))
with open("feature_names_by_cat.txt", "w", encoding="utf-8") as f:
    for cat in data:
        cat_name = cat["category"]
        count = len(cat["features"])
        f.write(f"=== {cat_name} ({count}) ===\n")
        for feat in cat["features"]:
            f.write(f"  - {feat}\n")
        f.write("\n")
print("Done writing feature_names_by_cat.txt")
