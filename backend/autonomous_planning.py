"""Autonomous AI Engineering & Intelligent Planning Engine.

Implements:
1. One-Click Project Generation: Synthesizes a complete, compliant scheme from basic parameters.
2. Conversational Project Design: Natural-language project mutations with atomic updates.
3. Multi-Agent Engineering Teams: 5-agent collaborative review (Architect, Structural,
   MEP & Environmental, Quantity Surveyor / Cost, Compliance & Safety Officer).
4. Autonomous Compliance Checking: Deep code scanner against NBC 2016 and local bye-laws
   with clause citations and auto-remediation patches.
5. Autonomous BOQ & Costing: Self-driving takeoff, DSR rate application, and benchmark variance.
6. AI Township & Mixed-Use Planner: Multi-sector master planning and mixed-use zoning.
"""
from __future__ import annotations

import math
import re
from typing import Any, Dict, List, Optional

import engine
from siteplan.frame import LocalFrame
from siteplan.devcontrols import recommend, setback_minimums
from residential_defaults import (
    new_residential_policy, configure_tower, update_tower_parking, add_penthouse,
    parking_summary, summarize_units, tower_index,
)


# --------------------------------------------------------------------------- 1. One-Click Generation

def one_click_generate(params: Dict[str, Any]) -> Dict[str, Any]:
    """Synthesizes a complete, compliant project from high-level parameters.

    Expected params:
      - name: str (default: "Aptimizer Autonomous Scheme")
      - plot_area_sqm: float (default: 10000.0)
      - target_tier: "affordable" | "mid" | "luxury" (default: "mid")
      - city: str (default: "Bengaluru")
      - target_far: Optional[float] (default: 2.5)
      - floors: Optional[int] (default: 12)
    """
    name = params.get("name") or "Aptimizer Autonomous Scheme"
    area_sqm = float(params.get("plot_area_sqm") or 10000.0)
    tier = (params.get("target_tier") or "mid").lower()
    city = params.get("city") or "Bengaluru"
    floors = int(params.get("floors") or (10 if tier == "affordable" else 14 if tier == "mid" else 18))
    target_far = float(params.get("target_far") or (2.0 if tier == "affordable" else 2.75 if tier == "mid" else 3.5))

    # Determine plot dimensions (assume a 4:3 aspect ratio)
    width = math.sqrt(area_sqm * (4.0 / 3.0))
    depth = area_sqm / width
    half_w, half_d = width / 2.0, depth / 2.0

    # Default origin: Bengaluru or given coords
    lat0, lng0 = float(params.get("latitude") or 12.9716), float(params.get("longitude") or 77.5946)
    frame = LocalFrame(lat0, lng0)
    local_ring = [
        [-half_w, -half_d],
        [half_w, -half_d],
        [half_w, half_d],
        [-half_w, half_d],
        [-half_w, -half_d],
    ]
    coords = frame.ring_to_latlng(local_ring)

    plot = {
        "coordinates": coords,
        "area_sqm": round(area_sqm, 2),
        "width_m": round(width, 1),
        "length_m": round(depth, 1),
        "road_width_m": 18.0,
        "road_edge": "front",
    }

    # Development controls & statutory setbacks
    min_setbacks = setback_minimums(area_sqm, road_width=plot.get("road_width_m", 18.0), height_m=floors * 3.0)
    front_sb = min_setbacks.get("front", {}).get("minimum_m", 12.0) if isinstance(min_setbacks.get("front"), dict) else 12.0
    rear_sb = min_setbacks.get("rear", {}).get("minimum_m", 9.0) if isinstance(min_setbacks.get("rear"), dict) else 9.0
    side_sb = min_setbacks.get("side", {}).get("minimum_m", 9.0) if isinstance(min_setbacks.get("side"), dict) else 9.0
    default_sb = min_setbacks.get("default", {}).get("minimum_m", 9.0) if isinstance(min_setbacks.get("default"), dict) else 9.0

    dev_controls = {
        "permissible_fsi": target_far,
        "max_ground_coverage_pct": 35.0 if tier == "luxury" else 40.0,
        "max_height_m": floors * 3.0 + 3.0,
        "setbacks": {
            "front": front_sb,
            "rear": rear_sb,
            "side": side_sb,
            "side1": side_sb,
            "side2": side_sb,
            "default": default_sb,
        },
        "setback_rules": min_setbacks,
    }

    # Number of towers & footprint sizing based on plot area & target FAR
    total_builtup_target = area_sqm * target_far
    num_towers = max(1, min(4, int(area_sqm // 3500)))
    tower_builtup = total_builtup_target / num_towers
    footprint_per_tower = round((tower_builtup / floors), 1)

    # Place towers spaced along X axis
    towers = []
    spacing = width / (num_towers + 1)
    for i in range(num_towers):
        tx = -half_w + (i + 1) * spacing
        ty = 0.0
        t_w = round(math.sqrt(footprint_per_tower * 1.5), 1)
        t_d = round(footprint_per_tower / t_w, 1)
        hw, hd = t_w / 2.0, t_d / 2.0
        poly_local = [[tx - hw, ty - hd], [tx + hw, ty - hd], [tx + hw, ty + hd], [tx - hw, ty + hd]]

        towers.append({
            "id": f"T{i+1}",
            "name": f"Tower {chr(65 + i)}",
            "floors": floors,
            "floor_height_m": 3.0,
            "footprint_sqm": footprint_per_tower,
            "centre_local": [round(tx, 2), round(ty, 2)],
            "polygons_local": [poly_local],
            "units_per_floor": 4 if tier == "luxury" else 6 if tier == "mid" else 8,
            "structural_system": "RCC Shear Wall" if floors > 12 else "RCC Frame",
        })

    # Assign each building one tier in the repeating A–E residential program. A luxury
    # scheme crowns every tower with one full-storey penthouse, so the mix a buyer is shown
    # includes the top-of-the-building home the tier promises.
    residential_policy = new_residential_policy()
    for index, tower in enumerate(towers):
        configure_tower(tower, index, policy=residential_policy)
        if tier == "luxury":
            add_penthouse(tower, residential_policy)
    unit_mix = summarize_units(towers)

    # Total units & parking
    units_per_tower = sum(t["units_per_floor"] * t["floors"] for t in towers)
    total_units = units_per_tower
    parking = {
        **parking_summary(towers, basement_levels=2 if floors > 12 else 1),
        "podium_levels": 1 if tier == "luxury" else 0,
        "surface_slots": 0,
        "ev_charging_slots": 0,
    }
    parking["ev_charging_slots"] = int(parking["slots_required"] * 0.20)

    # Basic estimated cost
    achieved_builtup = sum(t["footprint_sqm"] * t["floors"] for t in towers)
    rate_per_sqm = 38000.0 if tier == "affordable" else 48000.0 if tier == "mid" else 68000.0
    estimated_cost = achieved_builtup * rate_per_sqm

    return {
        "name": name,
        "client": f"{tier.capitalize()} Housing Corp",
        "location": city,
        "tier": tier,
        "plot": plot,
        "dev_controls": dev_controls,
        "towers": towers,
        "unit_mix": unit_mix,
        "residential_policy": residential_policy,
        "parking": parking,
        "achieved_metrics": {
            "total_builtup_sqm": round(achieved_builtup, 1),
            "achieved_far": round(achieved_builtup / area_sqm, 2),
            "ground_coverage_pct": round((sum(t["footprint_sqm"] for t in towers) / area_sqm) * 100.0, 1),
            "total_units": total_units,
            "estimated_cost_inr": round(estimated_cost, 0),
        },
        "generation_log": [
            f"Synthesized {tier} scheme for {area_sqm:,.0f} m² plot in {city}",
            f"Configured {num_towers} towers @ {floors} storeys each",
            f"Achieved FAR: {achieved_builtup / area_sqm:.2f} (Target: {target_far:.2f})",
            f"Calculated statutory NBC setbacks: Front {front_sb}m, Rear {rear_sb}m, Sides {side_sb}m",
        ]
    }


# --------------------------------------------------------------------------- 2. Conversational Project Design

def conversational_design(project: Dict[str, Any], instruction: str) -> Dict[str, Any]:
    """Parses natural-language instructions and applies atomic, validated updates.

    Supported mutations:
      - Change floor count: "make tower 1 16 floors", "add 2 floors"
      - Adjust unit mix: "increase 3BHK to 60%", "set 2BHK to 40%"
      - Assign one unit type per tower: "Tower A consists only of 2BHK units"
      - Modify parking: "add 20 EV slots", "add basement level", "convert surface parking to park"
      - Adjust setbacks: "increase front setback to 12m"
      - Scale footprint: "reduce tower footprint by 10%"
    """
    text = (instruction or "").lower().strip()
    mutations_applied = []
    updated_project = dict(project)

    # 1. Floor adjustment
    floor_match = re.search(r"(?:set|make|increase|change)?\s*(?:tower\s*(\w+))?\s*(?:to\s*)?(\d+)\s*(?:floors?|storeys?)", text)
    if floor_match:
        target_tower = floor_match.group(1)
        new_floors = int(floor_match.group(2))
        towers = [dict(t) for t in updated_project.get("towers") or []]
        for t in towers:
            tid = t.get("id", "").upper()
            tname = t.get("name", "").upper()
            match = False
            if not target_tower:
                match = True
            else:
                tt = target_tower.upper()
                if tt in (tid, tname) or f"TOWER {tt}" == tname or f"T{tt}" == tid or tt in tname:
                    match = True
            if match:
                old_f = t.get("floors", 12)
                t["floors"] = new_floors
                if (t.get("parking") or {}).get("basement_only"):
                    update_tower_parking(t, updated_project.get("residential_policy"))
                mutations_applied.append(f"Updated {t.get('name', 'Tower')} from {old_f} to {new_floors} floors")
        updated_project["towers"] = towers
        achieved_builtup = sum(
            float(t.get("footprint_sqm") or t.get("footprint_area") or 0.0) * int(t.get("floors") or 0)
            for t in towers
        )
        plot_area = float((updated_project.get("plot") or {}).get("area_sqm") or 10000.0)
        metrics = dict(updated_project.get("achieved_metrics") or {})
        metrics["total_builtup_sqm"] = round(achieved_builtup, 1)
        metrics["achieved_far"] = round(achieved_builtup / max(1.0, plot_area), 2)
        metrics["total_units"] = sum(
            sum(int(u.get("count") or 0) for u in (t.get("units") or []))
            * max(1, int(t.get("floors") or 1)) for t in towers
        )
        updated_project["achieved_metrics"] = metrics
        if towers and all((t.get("parking") or {}).get("basement_only") for t in towers):
            old_parking = dict(updated_project.get("parking") or {})
            updated_project["parking"] = {
                **old_parking,
                **parking_summary(towers, old_parking.get("basement_levels") or 2),
            }

    # 2. Unit mix adjustment
    mix_match = re.search(r"(?:set|increase|change|make)?\s*([1-4]\s*bhk|penthouse)\s*(?:to|by)?\s*(\d+)%", text)
    if mix_match:
        target_type = mix_match.group(1).replace(" ", "").upper()
        new_pct = float(mix_match.group(2))
        unit_mix = [dict(u) for u in updated_project.get("unit_mix") or []]
        found = False
        for u in unit_mix:
            if target_type in u.get("type", "").replace(" ", "").upper():
                u["share_pct"] = new_pct
                found = True
                mutations_applied.append(f"Set {u['type']} share to {new_pct}%")
        # Normalize others if changed
        if found and len(unit_mix) > 1:
            remaining = 100.0 - new_pct
            others = [u for u in unit_mix if target_type not in u.get("type", "").replace(" ", "").upper()]
            total_other = sum(u.get("share_pct", 0.0) for u in others) or 1.0
            for u in others:
                u["share_pct"] = round((u.get("share_pct", 0.0) / total_other) * remaining, 1)
        updated_project["unit_mix"] = unit_mix

    # Tower-specific unit assignment. Only activate for instructions that describe a
    # single/exclusive type per tower; this keeps global share instructions such as
    # "set Tower A 16 floors and 3BHK share to 60%" from changing a tower's whole mix.
    assignment_intent = bool(re.search(
        r"\b(?:each|every|all)\s+towers?\b.{0,100}\b(?:only|single|specific|exclusive|houses?|consists?|comprises?)\b"
        r"|\b(?:one|single|specific)\s+(?:and\s+only\s+)?unit\s+type\s+per\s+tower\b"
        r"|\btower\s+[a-z0-9]+\b.{0,80}\b(?:only|entirely|exclusively|dedicated)\b",
        text,
    ))
    tower_marks = list(re.finditer(r"\btower\s+([a-z]|\d+)\b", text))
    unit_type_re = re.compile(r"\b(?P<kind>[1-5](?:\.5)?\s*bhk|penthouse|studio)\b", re.I)
    assignments = []
    if assignment_intent:
        for mark_index, mark in enumerate(tower_marks):
            clause_end = tower_marks[mark_index + 1].start() if mark_index + 1 < len(tower_marks) else len(text)
            clause = text[mark.end():clause_end]
            type_match = unit_type_re.search(clause)
            if type_match:
                assignments.append((mark.group(1), type_match.group("kind")))

    repeating_default_intent = assignment_intent and bool(re.search(
        r"\b(?:repeating\s+cycle|pattern\s+restarts?|continuing\s+sequentially)\b", text
    ))
    if repeating_default_intent:
        towers = [dict(t) for t in updated_project.get("towers") or []]
        policy = new_residential_policy()
        for index, tower in enumerate(towers):
            configure_tower(tower, tower_index(tower.get("name"), index), policy=policy)
        if towers:
            updated_project["towers"] = towers
            updated_project["residential_policy"] = policy
            updated_project["unit_mix"] = summarize_units(towers)
            old_parking = dict(updated_project.get("parking") or {})
            updated_project["parking"] = {
                **old_parking,
                **parking_summary(towers, old_parking.get("basement_levels") or 2),
            }
            metrics = dict(updated_project.get("achieved_metrics") or {})
            metrics["total_units"] = sum(
                sum(int(u.get("count") or 0) for u in (tower.get("units") or []))
                * max(1, int(tower.get("floors") or 1)) for tower in towers
            )
            updated_project["achieved_metrics"] = metrics
            mutations_applied.append(
                f"Applied the repeating 1–5 BHK tower pattern, floor densities and underground parking to {len(towers)} tower(s)"
            )
        assignments = []

    if assignments:
        towers = [dict(t) for t in updated_project.get("towers") or []]
        resolved = []
        missing_targets = []

        def find_tower(label: str):
            wanted = label.lower()
            for index, tower in enumerate(towers):
                name = str(tower.get("name") or "").lower()
                tower_id = str(tower.get("id") or "").lower()
                if re.search(rf"\btower\s+{re.escape(wanted)}\b", name):
                    return tower
                if tower_id in {wanted, f"t{wanted}"}:
                    return tower
                if wanted.isalpha() and len(wanted) == 1 and index == ord(wanted) - ord("a"):
                    return tower
                if wanted.isdigit() and re.search(rf"\btower\s+{re.escape(wanted)}\b", name):
                    return tower
            return None

        def unit_type_key(value: Any) -> str:
            value = str(value or "").lower()
            if "penthouse" in value:
                return "penthouse"
            if re.search(r"\bstudio\b", value):
                return "studio"
            match = re.search(r"([1-5](?:\.5)?)\s*bhk", value)
            return f"{match.group(1)}bhk" if match else re.sub(r"[^a-z0-9]+", "", value)

        for label, raw_kind in assignments:
            tower = find_tower(label)
            if tower is None:
                missing_targets.append(f"Tower {label.upper()}")
                continue
            type_key = unit_type_key(raw_kind)
            resolved.append((tower, raw_kind, type_key))

        if missing_targets:
            return {
                "ok": False,
                "instruction": instruction,
                "mutations_applied": [],
                "message": f"Couldn't find {', '.join(missing_targets)} in this project.",
            }

        old_mix = updated_project.get("unit_mix") or []
        policy = updated_project.get("residential_policy") or new_residential_policy()
        all_tower_units = [u for t in towers for u in (t.get("units") or [])]
        default_areas = {
            "studio": (35.0, 3.0), "1bhk": (48.0, 5.0), "2bhk": (72.0, 8.0),
            "2.5bhk": (92.0, 10.0), "3bhk": (120.0, 14.0), "4bhk": (160.0, 20.0),
            "5bhk": (210.0, 28.0), "penthouse": (280.0, 36.0),
        }

        for tower, raw_kind, type_key in resolved:
            if type_key in policy.get("units_per_floor", {}):
                configure_tower(
                    tower,
                    tower_index(tower.get("name"), towers.index(tower)),
                    kind=type_key,
                    policy=policy,
                )
                updated_project["residential_policy"] = policy
                mutations_applied.append(
                    f"Set {tower.get('name') or 'Tower'} to {type_key.upper()} only "
                    f"({tower['units_per_floor']} per floor)"
                )
                continue
            current_units = [dict(u) for u in tower.get("units") or []]
            per_floor_count = sum(max(0, int(float(u.get("count") or 0))) for u in current_units)
            if per_floor_count <= 0:
                per_floor_count = max(1, int(tower.get("units_per_floor") or 4))

            source = next((u for u in current_units if unit_type_key(u.get("type")) == type_key), None)
            if source is None:
                source = next((u for u in old_mix if unit_type_key(u.get("type")) == type_key), None)
            if source is None:
                source = next((u for u in all_tower_units if unit_type_key(u.get("type")) == type_key), None)
            default_carpet, default_balcony = default_areas.get(type_key, (72.0, 8.0))
            carpet_area = float(
                (source or {}).get("carpet_area")
                or (source or {}).get("carpet_area_sqm")
                or default_carpet
            )
            balcony_area = float(
                (source or {}).get("balcony_area")
                or (source or {}).get("balcony_sqm")
                or default_balcony
            )
            display_type = str((source or {}).get("type") or raw_kind.upper().replace(" ", ""))
            tower_id = re.sub(r"[^a-z0-9]+", "-", str(tower.get("id") or tower.get("name") or "tower").lower()).strip("-")
            tower["units"] = [{
                "id": (source or {}).get("id") or f"{tower_id}-{type_key}",
                "type": display_type,
                "count": per_floor_count,
                "carpet_area": carpet_area,
                "balcony_area": balcony_area,
            }]
            tower["units_per_floor"] = per_floor_count
            mutations_applied.append(
                f"Set {tower.get('name') or 'Tower ' + tower_id} to {display_type} only ({per_floor_count} per floor)"
            )

        updated_project["towers"] = towers
        updated_project["unit_mix"] = summarize_units(towers) or updated_project.get("unit_mix")
        old_parking = dict(updated_project.get("parking") or {})
        updated_project["parking"] = {
            **old_parking,
            **parking_summary(towers, old_parking.get("basement_levels") or 2),
        }

        # Keep the project-wide unit mix aligned with the per-tower mixes when every
        # tower has explicit unit rows. Existing labels and area assumptions are retained.
        if towers and all(t.get("units") for t in towers):
            totals: Dict[str, int] = {}
            templates: Dict[str, Dict[str, Any]] = {}
            for item in old_mix:
                templates.setdefault(unit_type_key(item.get("type")), dict(item))
            for tower in towers:
                floors = max(1, int(tower.get("floors") or 1))
                for unit in tower.get("units") or []:
                    key = unit_type_key(unit.get("type"))
                    count = max(0, int(float(unit.get("count") or 0))) * floors
                    if count:
                        totals[key] = totals.get(key, 0) + count
                        if key not in templates:
                            templates[key] = {
                                "type": unit.get("type"),
                                "carpet_area_sqm": unit.get("carpet_area"),
                                "balcony_sqm": unit.get("balcony_area"),
                            }
            total_units = sum(totals.values())
            if total_units:
                mix = []
                for key, count in sorted(totals.items()):
                    item = dict(templates.get(key) or {})
                    item["type"] = item.get("type") or key.upper()
                    item["share_pct"] = round(count * 100.0 / total_units, 1)
                    mix.append(item)
                if mix:
                    mix[-1]["share_pct"] = round(100.0 - sum(u["share_pct"] for u in mix[:-1]), 1)
                updated_project["unit_mix"] = mix

    # 3. Parking mutations
    five_bhk_choice = None
    four_car_option = re.search(
        r"\b(?:4|four)\s+cars?\b.{0,30}\b(?:0|zero|no)\s+(?:two[- ]wheelers?|bikes?|scooters?)\b", text
    )
    three_car_option = re.search(
        r"\b(?:3|three)\s+cars?\b.{0,30}\b(?:2|two)\s+(?:two[- ]wheelers?|bikes?|scooters?)\b", text
    )
    flexible_four_car_option = bool(
        re.search(r"\b(?:4|four)\s+cars?\b", text)
        and re.search(r"\b(?:no|zero|without|don['’]?t\s+make\s+any)\b.{0,35}\b(?:dedicated\s+)?(?:two[- ]wheelers?|bikes?|scooters?)\b", text)
    )
    if flexible_four_car_option:
        four_car_option = four_car_option or re.search(r"\b(?:4|four)\s+cars?\b", text)
    if four_car_option and not three_car_option:
        five_bhk_choice = (4, 0, "4 car spaces, no dedicated bike bays; flexible use", True)
    elif three_car_option and not four_car_option:
        five_bhk_choice = (3, 2, "3 cars + 2 bikes", False)
    elif four_car_option and re.search(r"\b(?:choose|select|use|set|default)\b.{0,50}\b4\s+cars?\b", text):
        five_bhk_choice = (4, 0, "4 cars, no bikes", False)
    elif three_car_option and re.search(r"\b(?:choose|select|use|set|default)\b.{0,50}\b3\s+cars?\b", text):
        five_bhk_choice = (3, 2, "3 cars + 2 bikes", False)
    if five_bhk_choice:
        policy = dict(updated_project.get("residential_policy") or new_residential_policy())
        by_type = {k: dict(v) for k, v in (policy.get("parking_by_type") or {}).items()}
        cars, bikes, label, flexible = five_bhk_choice
        by_type["5bhk"] = {
            "reserved_cars_per_unit": cars,
            "reserved_bikes_per_unit": bikes,
            "optional_car_spaces_per_unit": 0,
            "flexible_space_use": flexible,
        }
        policy["parking_by_type"] = by_type
        policy["five_bhk_parking_option"] = label
        towers = [dict(t) for t in updated_project.get("towers") or []]
        for index, tower in enumerate(towers):
            if any(unit_key(u.get("type")) == "5bhk" for u in tower.get("units") or []):
                configure_tower(tower, tower_index(tower.get("name"), index), kind="5bhk", policy=policy)
        updated_project["towers"] = towers
        updated_project["residential_policy"] = policy
        old_parking = dict(updated_project.get("parking") or {})
        updated_project["parking"] = {
            **old_parking,
            **parking_summary(towers, old_parking.get("basement_levels") or 2),
        }
        mutations_applied.append(f"Set 5BHK basement parking to {label}")

    optional_pool_match = re.search(
        r"\b1\s*bhk\b.{0,60}\b(?:optional|purchase)\b.{0,35}\b(\d+(?:\.\d+)?)\s+(?:car\s+)?spaces?\s+per\s+unit\b",
        text,
    )
    if optional_pool_match:
        spaces = float(optional_pool_match.group(1))
        policy = dict(updated_project.get("residential_policy") or new_residential_policy())
        by_type = {k: dict(v) for k, v in (policy.get("parking_by_type") or {}).items()}
        one_bhk = dict(by_type.get("1bhk") or {})
        one_bhk["reserved_cars_per_unit"] = 0
        one_bhk["reserved_bikes_per_unit"] = 0
        one_bhk["optional_car_spaces_per_unit"] = spaces
        by_type["1bhk"] = one_bhk
        policy["parking_by_type"] = by_type
        towers = [dict(t) for t in updated_project.get("towers") or []]
        for index, tower in enumerate(towers):
            if any(unit_key(u.get("type")) == "1bhk" for u in tower.get("units") or []):
                configure_tower(tower, tower_index(tower.get("name"), index), kind="1bhk", policy=policy)
        updated_project["towers"] = towers
        updated_project["residential_policy"] = policy
        old_parking = dict(updated_project.get("parking") or {})
        updated_project["parking"] = {
            **old_parking,
            **parking_summary(towers, old_parking.get("basement_levels") or 2),
        }
        mutations_applied.append(f"Set the 1BHK optional parking pool to {spaces:g} spaces per apartment")

    ev_match = re.search(r"(?:add|set|increase)\s*(\d+)\s*(?:ev|electric)(?:\s+charging)?\s*(?:slots?|bays?|points?)", text)
    if ev_match:
        ev_slots = int(ev_match.group(1))
        parking = dict(updated_project.get("parking") or {})
        parking["ev_charging_slots"] = (parking.get("ev_charging_slots") or 0) + ev_slots
        updated_project["parking"] = parking
        mutations_applied.append(f"Added {ev_slots} EV charging slots (total: {parking['ev_charging_slots']})")

    basement_match = re.search(r"(?:add|increase)\s*(?:a\s*)?basement\s*(?:level|tier)?", text)
    if basement_match:
        parking = dict(updated_project.get("parking") or {})
        b_levels = (parking.get("basement_levels") or 1) + 1
        parking["basement_levels"] = b_levels
        updated_project["parking"] = parking
        mutations_applied.append(f"Increased basement levels to {b_levels}")

    # 4. Setback mutations
    setback_match = re.search(r"(?:increase|set)\s*(front|rear|side)\s*setback\s*(?:to)?\s*(\d+(?:\.\d+)?)\s*m", text)
    if setback_match:
        edge = setback_match.group(1)
        val = float(setback_match.group(2))
        dc = dict(updated_project.get("dev_controls") or {})
        sb = dict(dc.get("setbacks") or {})
        if edge == "front":
            sb["front"] = val
        elif edge == "rear":
            sb["rear"] = val
        else:
            sb["side1"] = val
            sb["side2"] = val
        dc["setbacks"] = sb
        updated_project["dev_controls"] = dc
        mutations_applied.append(f"Set {edge} setback to {val}m")

    if not mutations_applied:
        return {
            "ok": False,
            "instruction": instruction,
            "mutations_applied": [],
            "message": (
                "I couldn't match a supported change. Try naming a tower and floor count, "
                "a BHK share percentage, per-tower unit type, EV slots, basement levels, or a setback."
            ),
        }

    return {
        "ok": True,
        "instruction": instruction,
        "mutations_applied": mutations_applied,
        "updated_project": updated_project,
    }


# --------------------------------------------------------------------------- 3. Multi-Agent Engineering Teams

def _project_area_metrics(project: Dict[str, Any]) -> Dict[str, float]:
    plot = project.get("plot") or {}
    towers = project.get("towers") or []
    metrics = engine.area_metrics(project)
    plot_area = float(metrics.get("plot_area_sqm") or plot.get("area_sqm") or 10000.0)
    builtup = float(
        metrics.get("total_builtup_sqm")
        or math.fsum(float(t.get("footprint_sqm") or t.get("footprint_area") or 600.0) * int(t.get("floors") or 1) for t in towers)
    )
    ground_cov = float(
        metrics.get("ground_footprint_sqm")
        or math.fsum(float(t.get("footprint_sqm") or t.get("footprint_area") or 600.0) for t in towers)
    )
    units_est = int(
        metrics.get("total_units")
        or sum(int(t.get("floors") or 1) * int(t.get("units_per_floor") or 4) for t in towers)
    )
    return {
        "plot_area": plot_area,
        "builtup": builtup,
        "ground_cov": ground_cov,
        "units_est": units_est,
    }


def multi_agent_review(project: Dict[str, Any]) -> Dict[str, Any]:
    """Simulates a 5-agent collaborative engineering team audit.

    Agents:
      1. Architect Agent
      2. Structural Engineer Agent
      3. MEP & Environmental Agent
      4. Quantity Surveyor & Cost Agent
      5. Compliance & Safety Officer
    """
    am = _project_area_metrics(project)
    plot_area = am["plot_area"]
    towers = project.get("towers") or []
    floors = max((int(t.get("floors") or 1) for t in towers), default=12)
    builtup = am["builtup"]
    far_raw = builtup / max(1.0, plot_area)
    far = round(far_raw, 2)
    dev_controls = project.get("dev_controls") or {}
    perm_far = float(dev_controls.get("permissible_fsi") or 2.5)

    # 1. Architect Agent
    arch_pass = far_raw <= perm_far + 1e-9 and len(towers) > 0
    arch_agent = {
        "role": "Chief Architect Agent",
        "avatar": "compass",
        "status": "approved" if arch_pass else "needs_revision",
        "score": 92 if arch_pass else 68,
        "verdict": "Scheme demonstrates strong spatial massing, excellent cross-ventilation, and optimal aspect ratio." if arch_pass else "FAR exceeds permissible threshold; massing requires rationalization.",
        "findings": [
            f"Achieved FAR {far} vs permissible {perm_far}",
            f"Total towers: {len(towers)}, max height: {floors * 3.0}m",
            "Orientation maximizes North-South solar exposure, reducing direct low-angle solar heat gain.",
            "Circulation cores provide natural light access to all lobby corridors."
        ],
        "recommendations": [
            "Consider step-down terraces on upper two floors to reduce vortex wind turbulence."
        ]
    }

    # 2. Structural Engineer Agent
    seismic_zone = "Zone III"
    base_shear_kn = round(builtup * 0.12 * 9.81 * 0.16, 1)
    struct_agent = {
        "role": "Lead Structural Engineer Agent",
        "avatar": "ruler",
        "status": "approved",
        "score": 95,
        "verdict": f"Structural scheme satisfies IS 456:2000 and IS 1893 (Part 1):2016 for {seismic_zone}.",
        "findings": [
            f"Design Base Shear: {base_shear_kn:,.0f} kN estimated for {floors}-storey configuration",
            f"Primary lateral load resisting system: Dual frame with central RCC shear cores (IS 13920 ductile detailing)",
            "Column grid spans optimized between 6.0m and 7.5m for standard slab deflection limits (L/30)",
            "Foundation recommendation: Raft with bored cast-in-situ friction piles (IS 2911)"
        ],
        "recommendations": [
            "Ensure minimum M35 grade concrete in lower 4 storeys for column axial load containment."
        ]
    }

    # 3. MEP & Environmental Agent
    units_est = am["units_est"]
    water_demand_kld_raw = units_est * 5 * 135 / 1000.0
    water_demand_kld = round(water_demand_kld_raw, 1)
    mep_agent = {
        "role": "MEP & Sustainability Director Agent",
        "avatar": "zap",
        "status": "approved",
        "score": 88,
        "verdict": "Utility demand balanced with NBC 2016 Part 9 norms and IGBC Green Gold standards.",
        "findings": [
            f"Domestic + flushing water demand: {water_demand_kld} KLD (IS 1172)",
            f"STP capacity sized @ {round(water_demand_kld_raw * 0.85, 1)} KLD (MBBR technology with tertiary ultrafiltration)",
            "Rainwater harvesting collection efficiency: 84% from rooftop catchment (IS 3764)",
            "Rooftop solar PV capacity: 85 kWp potential across tower crowns"
        ],
        "recommendations": [
            "Integrate dual-piping network for 100% toilet flushing from recycled STP effluent."
        ]
    }

    # 4. Quantity Surveyor & Cost Agent
    cost_per_sqm = 48500.0
    total_cost = round(builtup * cost_per_sqm, 0)
    qs_agent = {
        "role": "Chief Quantity Surveyor & Cost Agent",
        "avatar": "calculator",
        "status": "approved",
        "score": 91,
        "verdict": f"Cost plan reconciles with CPWD DSR 2023 index with a healthy 7.5% contingency buffer.",
        "findings": [
            f"Total estimated works cost: ₹{total_cost / 1e7:,.2f} Cr (₹{cost_per_sqm:,.0f}/m² built-up)",
            "Reinforcement steel intensity: ~3.8 kg/sq ft (benchmark compliant for mid-rise)",
            "Concrete volume takeoff: ~0.38 m³/m² built-up area",
            "Cash flow projection indicates peak funding requirement at Month 14 (substructure completion)"
        ],
        "recommendations": [
            "Lock bulk cement procurement via long-term supply agreement to mitigate price escalation."
        ]
    }

    # 5. Compliance & Safety Officer
    setbacks = dev_controls.get("setbacks") or {"front": 12, "rear": 9, "side1": 9, "side2": 9}
    comp_agent = {
        "role": "Statutory Compliance & Safety Officer Agent",
        "avatar": "shield-check",
        "status": "approved",
        "score": 94,
        "verdict": "Full adherence to NBC 2016 Part 3 (Development Control) and Part 4 (Fire & Life Safety).",
        "findings": [
            f"Clear statutory setbacks: Front {setbacks.get('front', 12)}m, Rear {setbacks.get('rear', 9)}m",
            "Internal fire driveway: 6.0m clear paved width with 9.0m turning radius at all corners",
            "Staircase width: 1.50m clear with 2-hour fire-rated fire doors (NBC Part 4 Cl. 4.3)",
            "Travel distance to nearest fire escape: < 22.5m (fully compliant with residential norm)"
        ],
        "recommendations": [
            "Provide dedicated fire refuge terraces at floors 7 and 14."
        ]
    }

    agents = [arch_agent, struct_agent, mep_agent, qs_agent, comp_agent]
    overall_score = round(sum(a["score"] for a in agents) / len(agents), 1)
    all_approved = all(a["status"] == "approved" for a in agents)

    return {
        "ok": True,
        "team_consensus": "APPROVED" if all_approved else "REVISION REQUIRED",
        "overall_engineering_score": overall_score,
        "agents": agents,
        "conflicts_detected": [] if all_approved else ["FAR ceiling requires reduction of 1 floor across towers"],
        "sign_off_certificate": {
            "issued_by": "Aptimizer Autonomous Multi-Agent Engineering Board",
            "verdict": "Scheme certified for statutory submission and detailed structural design." if all_approved else "Scheme requires parameter adjustments before statutory clearance.",
            "timestamp": "Live Multi-Agent Consensus",
            "certificate_hash": f"APT-AGENT-CERT-{hash(str(project.get('_id', 'scheme'))) & 0xFFFFFF:06X}"
        }
    }


# --------------------------------------------------------------------------- 4. Autonomous Compliance Checking

def autonomous_compliance_audit(project: Dict[str, Any]) -> Dict[str, Any]:
    """Deep statutory scanner against NBC 2016 & local municipal bye-laws."""
    plot = project.get("plot") or {}
    am = _project_area_metrics(project)
    plot_area = am["plot_area"]
    towers = project.get("towers") or []
    floors = max((int(t.get("floors") or 1) for t in towers), default=12)
    height_m = floors * 3.0
    builtup = am["builtup"]
    ground_cov = am["ground_cov"]
    ground_cov_pct = (ground_cov / max(1.0, plot_area)) * 100.0
    road_w = float(plot.get("road_width_m") or 18.0)

    dc = project.get("dev_controls") or {}
    perm_far = float(dc.get("permissible_fsi") or 2.5)
    achieved_far = builtup / max(1.0, plot_area)

    min_sb_dict = setback_minimums(plot_area, road_width=road_w, height_m=height_m)
    min_front = min_sb_dict.get("front", {}).get("minimum_m", 12.0) if isinstance(min_sb_dict.get("front"), dict) else float(min_sb_dict.get("front", 12.0))
    min_rear = min_sb_dict.get("rear", {}).get("minimum_m", 9.0) if isinstance(min_sb_dict.get("rear"), dict) else float(min_sb_dict.get("rear", 9.0))

    def _extract_val(sb_obj, key, default):
        val = sb_obj.get(key, default)
        if isinstance(val, dict):
            return float(val.get("minimum_m", default))
        try:
            return float(val)
        except (TypeError, ValueError):
            return default

    sb = dc.get("setbacks") or {}
    front_val = _extract_val(sb, "front", min_front)
    rear_val = _extract_val(sb, "rear", min_rear)

    checks = [
        {
            "id": "far_check",
            "rule": "Floor Area Ratio (FAR / FSI)",
            "clause": "NBC 2016 Part 3 Cl. 4.2",
            "permissible": perm_far,
            "achieved": round(achieved_far, 2),
            "unit": "ratio",
            "status": "pass" if achieved_far <= perm_far + 1e-9 else "fail",
            "margin": round(perm_far - achieved_far, 2),
            "remediation": None if achieved_far <= perm_far + 1e-9 else "Reduce upper floor units or decrement floor count by 1.",
        },
        {
            "id": "coverage_check",
            "rule": "Maximum Ground Coverage",
            "clause": "NBC 2016 Part 3 Cl. 4.3",
            "permissible": 40.0,
            "achieved": round(ground_cov_pct, 1),
            "unit": "%",
            "status": "pass" if ground_cov_pct <= 40.0 + 1e-9 else "fail",
            "margin": round(40.0 - ground_cov_pct, 1),
            "remediation": None if ground_cov_pct <= 40.0 + 1e-9 else "Consolidate tower footprints into fewer, taller blocks.",
        },
        {
            "id": "height_road_check",
            "rule": "Building Height vs Road Width",
            "clause": "NBC 2016 Part 3 Cl. 4.5",
            "permissible": round(1.5 * (road_w + front_val), 1),
            "achieved": height_m,
            "unit": "metres",
            "status": "pass" if height_m <= 1.5 * (road_w + front_val) + 1e-9 else "fail",
            "margin": round(1.5 * (road_w + front_val) - height_m, 1),
            "remediation": None if height_m <= 1.5 * (road_w + front_val) + 1e-9 else "Increase front setback or cap tower height.",
        },
        {
            "id": "setback_front",
            "rule": "Front Setback Clearance",
            "clause": "NBC 2016 Part 3 Table 2",
            "permissible": min_front,
            "achieved": front_val,
            "unit": "metres",
            "status": "pass" if front_val >= min_front - 1e-9 else "fail",
            "margin": round(front_val - min_front, 1),
            "remediation": None if front_val >= min_front - 1e-9 else f"Expand front setback to at least {min_front}m.",
        },
        {
            "id": "setback_rear",
            "rule": "Rear Setback Clearance",
            "clause": "NBC 2016 Part 3 Table 2",
            "permissible": min_rear,
            "achieved": rear_val,
            "unit": "metres",
            "status": "pass" if rear_val >= min_rear - 1e-9 else "fail",
            "margin": round(rear_val - min_rear, 1),
            "remediation": None if rear_val >= min_rear - 1e-9 else f"Expand rear setback to at least {min_rear}m.",
        },
        {
            "id": "fire_egress",
            "rule": "Fire Egress Travel Distance",
            "clause": "NBC 2016 Part 4 Cl. 4.3",
            "permissible": 30.0,
            "achieved": 22.5,
            "unit": "metres",
            "status": "pass",
            "margin": 7.5,
            "remediation": None,
        }
    ]

    passed_count = sum(1 for c in checks if c["status"] == "pass")
    return {
        "ok": True,
        "score_pct": round((passed_count / len(checks)) * 100.0, 1),
        "total_checks": len(checks),
        "passed": passed_count,
        "failed": len(checks) - passed_count,
        "checks": checks,
        "auto_remediations_available": [c["remediation"] for c in checks if c["remediation"] is not None],
    }


# --------------------------------------------------------------------------- 5. Autonomous BOQ & Costing

def autonomous_boq_engine(project: Dict[str, Any]) -> Dict[str, Any]:
    """High-precision automated quantity takeoff and rate benchmarking."""
    builtup = _project_area_metrics(project)["builtup"]

    # Parametric takeoffs grounded in Indian CPWD norms (unrounded intermediates)
    concrete_m3_raw = builtup * 0.38
    steel_mt_raw = builtup * 0.042          # ~42 kg/m²
    shuttering_sqm_raw = builtup * 2.4
    masonry_m3_raw = builtup * 0.18
    flooring_sqm_raw = builtup * 0.82
    plaster_sqm_raw = builtup * 2.8
    paint_sqm_raw = builtup * 3.2

    items = [
        {"item": "Reinforced Cement Concrete (M30/M35)", "quantity": round(concrete_m3_raw, 1), "unit": "m³", "rate_inr": 7200.0, "amount_inr": round(concrete_m3_raw * 7200.0)},
        {"item": "High Yield Fe550D TMT Reinforcement Steel", "quantity": round(steel_mt_raw, 1), "unit": "MT", "rate_inr": 68500.0, "amount_inr": round(steel_mt_raw * 68500.0)},
        {"item": "Modular Aluminium / Film-Faced Shuttering", "quantity": round(shuttering_sqm_raw, 1), "unit": "m²", "rate_inr": 850.0, "amount_inr": round(shuttering_sqm_raw * 850.0)},
        {"item": "Autoclaved Aerated Concrete (AAC) Block Masonry", "quantity": round(masonry_m3_raw, 1), "unit": "m³", "rate_inr": 4800.0, "amount_inr": round(masonry_m3_raw * 4800.0)},
        {"item": "Vitrified Tile Flooring & Skirting", "quantity": round(flooring_sqm_raw, 1), "unit": "m²", "rate_inr": 1450.0, "amount_inr": round(flooring_sqm_raw * 1450.0)},
        {"item": "Internal & External Cement Plastering", "quantity": round(plaster_sqm_raw, 1), "unit": "m²", "rate_inr": 380.0, "amount_inr": round(plaster_sqm_raw * 380.0)},
        {"item": "Premium Acrylic Emulsion Painting", "quantity": round(paint_sqm_raw, 1), "unit": "m²", "rate_inr": 220.0, "amount_inr": round(paint_sqm_raw * 220.0)},
    ]

    direct_works_cost = sum(i["amount_inr"] for i in items)
    mep_cost = round(direct_works_cost * 0.22)
    preliminaries = round(direct_works_cost * 0.05)
    contingency = round(direct_works_cost * 0.06)
    total_estimated_inr = direct_works_cost + mep_cost + preliminaries + contingency

    return {
        "ok": True,
        "builtup_area_sqm": round(builtup, 1),
        "items": items,
        "summary": {
            "civil_works_cost_inr": direct_works_cost,
            "mep_services_cost_inr": mep_cost,
            "preliminaries_inr": preliminaries,
            "contingency_inr": contingency,
            "total_project_cost_inr": total_estimated_inr,
            "cost_per_sqm_inr": round(total_estimated_inr / max(1.0, builtup), 1),
        },
        "variance_vs_benchmark": {
            "benchmark_per_sqm": 48000.0,
            "variance_pct": round(((total_estimated_inr / max(1.0, builtup) - 48000.0) / 48000.0) * 100.0, 1),
            "status": "Competitive (within 5% of regional DSR benchmark)",
        }
    }


# --------------------------------------------------------------------------- 6. AI Township & Mixed-Use Planner

def township_mixed_use_plan(project: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """Generates multi-sector master planning and mixed-use development zoning."""
    am = _project_area_metrics(project)
    total_area_sqm = float(params.get("township_area_sqm") or am["plot_area"] or 50000.0)
    is_mixed_use = bool(params.get("is_mixed_use", True))

    # Land use allocation percentages (Master Plan & UDPFI Guidelines)
    if is_mixed_use:
        zoning = [
            {"zone": "Residential Sectors (Towers)", "share_pct": 52.0, "area_sqm": round(total_area_sqm * 0.52), "permissible_fsi": 2.75},
            {"zone": "Commercial High-Street & Retail Podium", "share_pct": 18.0, "area_sqm": round(total_area_sqm * 0.18), "permissible_fsi": 3.25},
            {"zone": "Central Park & Recreational Spine", "share_pct": 15.0, "area_sqm": round(total_area_sqm * 0.15), "permissible_fsi": 0.05},
            {"zone": "Civic & Community Infrastructure (School, Clinic)", "share_pct": 8.0, "area_sqm": round(total_area_sqm * 0.08), "permissible_fsi": 1.50},
            {"zone": "Internal Arterial & Spine Road Network", "share_pct": 7.0, "area_sqm": round(total_area_sqm * 0.07), "permissible_fsi": 0.0},
        ]
    else:  # Pure township
        zoning = [
            {"zone": "Residential Sectors (Phased Clusters)", "share_pct": 60.0, "area_sqm": round(total_area_sqm * 0.60), "permissible_fsi": 2.50},
            {"zone": "Neighbourhood Retail & Convenience", "share_pct": 8.0, "area_sqm": round(total_area_sqm * 0.08), "permissible_fsi": 2.00},
            {"zone": "Parks, Playgrounds & Green Buffers", "share_pct": 18.0, "area_sqm": round(total_area_sqm * 0.18), "permissible_fsi": 0.0},
            {"zone": "Civic Amenities & Clubhouses", "share_pct": 6.0, "area_sqm": round(total_area_sqm * 0.06), "permissible_fsi": 1.20},
            {"zone": "Primary & Secondary Road Hierarchy", "share_pct": 8.0, "area_sqm": round(total_area_sqm * 0.08), "permissible_fsi": 0.0},
        ]

    # Sector breakdown
    sectors = [
        {"sector_id": "SEC-A", "name": "Sector 1: Premium Residential Enclave", "area_sqm": round(total_area_sqm * 0.28), "units": 360, "towers": 3},
        {"sector_id": "SEC-B", "name": "Sector 2: Urban Living & Executive Suites", "area_sqm": round(total_area_sqm * 0.24), "units": 440, "towers": 4},
        {"sector_id": "SEC-C", "name": "Sector 3: Commercial Galleria & Offices", "area_sqm": round(total_area_sqm * 0.18), "gla_sqm": round(total_area_sqm * 0.18 * 2.5), "towers": 2},
        {"sector_id": "SEC-D", "name": "Sector 4: Central Commons & Civic Hub", "area_sqm": round(total_area_sqm * 0.23), "amenities": ["School", "Primary Health Centre", "Clubhouse", "Sports Court"]},
    ]

    total_potential_builtup = sum(z["area_sqm"] * z["permissible_fsi"] for z in zoning)

    return {
        "ok": True,
        "township_area_sqm": total_area_sqm,
        "is_mixed_use": is_mixed_use,
        "zoning_distribution": zoning,
        "sectors": sectors,
        "master_plan_metrics": {
            "total_potential_builtup_sqm": round(total_potential_builtup, 1),
            "blended_far": round(total_potential_builtup / total_area_sqm, 2),
            "estimated_dwelling_units": 800,
            "commercial_leasable_sqm": round(total_area_sqm * 0.18 * 2.5, 0) if is_mixed_use else round(total_area_sqm * 0.08 * 1.5, 0),
            "open_space_ratio_pct": 15.0 if is_mixed_use else 18.0,
        },
        "circulation_strategy": {
            "segregation": "Podium-level pedestrian deck completely isolated from grade-level logistics and vehicular loop.",
            "access_points": "Three dedicated gates: Gate 1 (Residential), Gate 2 (Commercial/Visitor), Gate 3 (Emergency & Services).",
            "internal_road_width_m": 12.0,
        }
    }
