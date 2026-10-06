"""Realistic apartment planner: the Indian slab-block flat, sized from a room brief.

The previous planners filled a unit envelope by stretching rooms: the Vastu packer cut it
into full-depth columns, so a large flat came out as 3 m x 17 m "bedrooms" and a 50 m²
pooja room. This planner works the other way round. Every room has a target size from the
brief for its BHK tier, scaled to the flat's carpet area within limits, and the flat's
envelope is whatever those rooms add up to. Nothing is stretched to fill space.

The arrangement is the one Indian residential slabs actually use (canonical frame: facade
at y = 0, the corridor/entrance wall at y = H, x running along the facade):

    facade   | balcony | balcony  |balcony | balcony |      habitable rooms on air
    row R1   | KITCHEN | LIVING   |MASTER  | BED 2   |      (balconies cut from the front)
    row R2   |UTIL|STR |POOJA|DIN |ENS|LOB |BATH|LOB |      wet core, dining, door lobbies
    row R3   |SFT|STORE| FOYER |      PASSAGE         |      entrance, circulation, stores
                         ^ main door on the corridor wall

That arrangement satisfies the audit's hard rules by construction: every habitable room
(kitchen included) has a wall on air, the utility snaps to the kitchen, the pooja room
takes its door off the living room and shares no wall with a bathroom, bedrooms open onto a
lobby off the private passage rather than the living room, en-suites are entered only from
their bedroom, common baths open onto the passage, and the rows tile the envelope exactly.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Sequence, Tuple

import vastu

# ---------------------------------------------------------------- the room brief (k = 1)
KITCHEN_W = {1: 2.6, 2: 2.8, 3: 3.0, 4: 3.2, 5: 3.4}
LIVING_W = {1: 3.9, 2: 4.6, 3: 5.4, 4: 6.0, 5: 6.6}
MASTER_W = {1: 3.6, 2: 3.8, 3: 4.0, 4: 4.2, 5: 4.5}
BED_W = {1: 3.3, 2: 3.4, 3: 3.4, 4: 3.5, 5: 3.6}
FAMILY_W = 4.4
OFFICE_W = 3.3
FACADE_ROW = {1: 5.0, 2: 5.4, 3: 5.7, 4: 6.0, 5: 6.3}     # R1 depth incl. balconies
SERVICE_ROW = {1: 2.4, 2: 2.4, 3: 2.6, 4: 2.7, 5: 2.8}    # R2: baths, dining, utility
ENTRY_ROW = {1: 1.5, 2: 1.5, 3: 1.6, 4: 1.6, 5: 1.7}      # R3: foyer, passage, shaft

LIVING_BALCONY = 1.8        # guide: N/E living balcony 1.8-2.4 m
MASTER_BALCONY = 1.2        # guide: exactly 1.2 m
SECONDARY_BALCONY = 1.2     # guide: 1.2-1.5 m
UTILITY_W = 1.35            # guide: 1.2-1.5 m
SHAFT_W = 0.9
POOJA_W = {1: 1.1, 2: 1.4, 3: 1.5, 4: 1.6, 5: 1.8}
BATH_SLOT_W = 2.1           # en-suite / common bath width behind a bedroom
MIN_LOBBY_W = 1.05          # a bedroom door needs a lobby at least a door-and-frame wide
SERVANT_ROOM_W = 2.4
PANTRY_DEPTH = 2.4

GROSS_PER_CARPET = 1.22     # envelope (incl. walls, circulation, balconies) per m² carpet
SCALE_LIMITS = (0.85, 1.35)


def _tier(unit_type: str, carpet: float) -> Tuple[int, bool, Dict[str, Any]]:
    prog = vastu.unit_programme(unit_type, carpet)
    beds = max(1, min(int(prog["beds"]), 5))
    return beds, bool(prog["is_penthouse"]), prog


def _layout_widths(beds: int, penthouse: bool, f: float) -> Dict[str, Any]:
    big = beds >= 5 or penthouse
    tier = min(beds, 5)
    servant = bool(vastu.SCALING_PROTOCOL[tier].get("servant"))
    cols = {
        "kitchen": max(round(KITCHEN_W[tier] * f, 2), 2.6, (UTILITY_W + SERVANT_ROOM_W) if servant else 0.0),
        # Wide enough for the pooja room and a 2.6 m dining area behind it.
        "living": max(round(LIVING_W[tier] * f, 2), POOJA_W[tier] + 2.6),
        "family": round(FAMILY_W * f, 2) if big else 0.0,
        "office": round(OFFICE_W * f, 2) if beds >= 5 else 0.0,
        "beds": [round((MASTER_W[tier] if i == 0 else BED_W[tier]) * f, 2) for i in range(beds)],
    }
    return cols


def _natural_size(beds: int, penthouse: bool, f: float) -> Tuple[float, float, Dict[str, Any]]:
    cols = _layout_widths(beds, penthouse, f)
    tier = min(beds, 5)
    # At least a 3.6 m deep living room behind its 1.8 m balcony.
    d1 = max(round(FACADE_ROW[tier] * min(f, 1.2), 2), LIVING_BALCONY + 3.6)
    width = cols["kitchen"] + cols["living"] + cols["family"] + cols["office"] + sum(cols["beds"])
    depth = d1 + SERVICE_ROW[tier] + ENTRY_ROW[tier]
    return round(width, 2), round(depth, 2), {**cols, "d1": d1}


def scale_for(unit_type: str, carpet: float) -> float:
    beds, penthouse, _ = _tier(unit_type, carpet)
    w0, h0, _ = _natural_size(beds, penthouse, 1.0)
    target = max(float(carpet or 0), 20.0) * GROSS_PER_CARPET
    f = math.sqrt(target / (w0 * h0))
    return max(SCALE_LIMITS[0], min(SCALE_LIMITS[1], f))


def envelope(unit_type: str, carpet: float) -> Tuple[float, float]:
    """(width along the corridor, depth) of the flat this brief produces."""
    beds, penthouse, _ = _tier(unit_type, carpet)
    w, h, _ = _natural_size(beds, penthouse, scale_for(unit_type, carpet))
    return w, h


def _rect(x: float, y: float, w: float, h: float) -> Dict[str, float]:
    return {"x": round(x, 3), "y": round(y, 3), "w": round(w, 3), "h": round(h, 3)}


def _place(rect: Dict[str, float], plan_w: float, plan_h: float, entry_edge: str, mirror: bool) -> Dict[str, float]:
    x, y, w, h = rect["x"], rect["y"], rect["w"], rect["h"]
    if mirror:
        x = plan_w - x - w
    if entry_edge == "S":          # facade north, door south: canonical
        return _rect(x, y, w, h)
    if entry_edge == "N":          # facade south: flip front to back
        return _rect(x, plan_h - y - h, w, h)
    if entry_edge == "E":          # facade west, door east
        return _rect(y, plan_w - x - w, h, w)
    return _rect(plan_h - y - h, x, h, w)   # entry W: facade east


def plan_unit(box: Dict[str, float], unit_type: str, carpet: float, entry_edge: str,
              uid: str, unit_index: int, exterior_edges: Sequence[str],
              mirror: bool = False) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Plan one flat inside `box` (normally sized by `envelope`). Returns (rooms, notes)."""
    beds, penthouse, prog = _tier(unit_type, carpet)
    tier = min(beds, 5)
    big = beds >= 5 or penthouse
    f = scale_for(unit_type, carpet)
    nat_w, nat_h, cols = _natural_size(beds, penthouse, f)

    canonical = entry_edge in ("S", "N")
    plan_w, plan_h = (float(box["w"]), float(box["h"])) if canonical else (float(box["h"]), float(box["w"]))
    x0, y0 = float(box["x"]), float(box["y"])
    if plan_w + 0.05 < nat_w or plan_h + 0.05 < nat_h * 0.98:
        return [], [f"Envelope {plan_w:.1f} x {plan_h:.1f} m is smaller than the {nat_w:.1f} x {nat_h:.1f} m "
                    "the room brief needs."]

    # Any extra envelope (a caller that sized the box differently) goes to the living room
    # and the facade row, never to a strip of leftover space.
    extra_w = plan_w - nat_w
    cols["living"] = round(cols["living"] + extra_w, 3)
    d1 = round(cols["d1"] + (plan_h - nat_h), 3)
    d2, d3 = SERVICE_ROW[tier], ENTRY_ROW[tier]
    y2, y3 = d1, d1 + d2

    rooms: List[Dict[str, Any]] = []

    def emit(key: str, name: str, rtype: str, x: float, y: float, w: float, h: float, **extra: Any):
        if w < 0.3 or h < 0.3:
            return None
        placed = _place(_rect(x, y, w, h), plan_w, plan_h, entry_edge, mirror)
        placed["x"] = round(placed["x"] + x0, 2)
        placed["y"] = round(placed["y"] + y0, 2)
        placed["w"] = round(placed["w"], 2)
        placed["h"] = round(placed["h"], 2)
        room = {"id": f"{uid}-{key}", "name": name, "type": rtype, "unit_id": uid,
                "unit_type": unit_type, "unit_index": unit_index, **placed, **extra}
        rooms.append(room)
        return room

    terrace = "Terrace" if penthouse else "Balcony"

    # ------------------------------------------------------------ R1: the facade row
    x = 0.0
    kw = cols["kitchen"]
    servant = bool(prog.get("servant"))
    back_of_kitchen = big and d1 - PANTRY_DEPTH >= 3.0
    if back_of_kitchen:
        # Utility and pantry side by side behind the kitchen they both serve.
        emit("kitchen", "Kitchen", "kitchen", x, 0, kw, d1 - PANTRY_DEPTH, has_window=True,
             door_to="dining", hob_faces="East")
        emit("utility", "Utility / Wash", "utility", x, d1 - PANTRY_DEPTH, UTILITY_W, PANTRY_DEPTH,
             door_to="kitchen", has_window=False)
        emit("pantry", "Pantry & Dry Store", "pantry", x + UTILITY_W, d1 - PANTRY_DEPTH, kw - UTILITY_W,
             PANTRY_DEPTH, door_to="kitchen")
    else:
        emit("kitchen", "Kitchen", "kitchen", x, 0, kw, d1, has_window=True, door_to="dining", hob_faces="East")
    x_living = x = x + kw
    lw = cols["living"]
    emit("lbalcony", f"Living {terrace}", "terrace" if penthouse else "balcony", x, 0, lw, LIVING_BALCONY,
         has_window=True, projects_from=f"{uid}-living")
    emit("living", "Living Room", "living", x, LIVING_BALCONY, lw, d1 - LIVING_BALCONY,
         has_window=True, door_to="dining")
    x += lw
    if cols["family"]:
        fw = cols["family"]
        emit("fbalcony", f"Family Lounge {terrace}", "terrace" if penthouse else "balcony", x, 0, fw,
             LIVING_BALCONY, has_window=True, projects_from=f"{uid}-family")
        # The lounge takes its column through the service row too, so dining stays a
        # room-shaped space behind the living room instead of a long strip.
        emit("family", "Family Lounge", "living", x, LIVING_BALCONY, fw, d1 + d2 - LIVING_BALCONY,
             has_window=True, door_to="dining")
        x += fw
    x_office = None
    if cols["office"]:
        ow = cols["office"]
        x_office = x
        emit("obalcony", "Office Balcony", "balcony", x, 0, ow, SECONDARY_BALCONY,
             has_window=True, projects_from=f"{uid}-office")
        emit("office", "Home Office", "office", x, SECONDARY_BALCONY, ow, d1 - SECONDARY_BALCONY,
             has_window=True, door_to="passage")
        x += ow
    x_private = x
    bed_xs = []
    for i, bw in enumerate(cols["beds"]):
        key = "mbed" if i == 0 else f"bed{i + 1}"
        name = "Master Bedroom" if i == 0 else f"Bedroom {i + 1}"
        depth = MASTER_BALCONY if i == 0 else SECONDARY_BALCONY
        emit(f"{key}balcony", f"{name} {terrace}", "balcony", x, 0, bw, depth,
             has_window=True, projects_from=f"{uid}-{key}")
        emit(key, name, "bedroom", x, depth, bw, d1 - depth, has_window=True, door_to=f"{key}lobby",
             **({"headboard": "South or West wall"} if i == 0 else {}))
        bed_xs.append((key, name, x, bw))
        x += bw
    plan_end = x

    # ------------------------------------------------------------ R2: the service row
    store_w = kw - UTILITY_W
    if back_of_kitchen:
        if servant:
            emit("servant", "Servant Room", "servant", 0, y2, kw, d2, door_to="utility")
        else:
            emit("store", "Kitchen Store", "storage", 0, y2, kw, d2, door_to="utility")
    elif store_w < 0.8:
        emit("utility", "Utility / Wash", "utility", 0, y2, kw, d2, door_to="kitchen", has_window=False)
    else:
        emit("utility", "Utility / Wash", "utility", 0, y2, UTILITY_W, d2, door_to="kitchen", has_window=False)
        if servant:
            # Staff quarters reached through the utility, never through the living areas.
            emit("servant", "Servant Room", "servant", UTILITY_W, y2, store_w, d2, door_to="utility")
        elif big:
            emit("pantry", "Pantry & Dry Store", "pantry", UTILITY_W, y2, store_w, d2, door_to="kitchen")
        else:
            emit("store", "Kitchen Store", "storage", UTILITY_W, y2, store_w, d2, door_to="kitchen")
    pw = POOJA_W[tier]
    excess = (lw - pw) - 2.2 * d2
    if 0 < excess <= 1.2:
        pw = round(pw + excess, 3)       # a little too long for dining: the pooja room takes it
    emit("pooja", "Pooja Niche" if tier == 1 else "Pooja Room", "pooja", x_living, y2, pw, d2,
         door_to="living", faces="East")
    dining_w = lw - pw
    max_dining = round(2.2 * d2, 3)          # beyond this a dining room reads as a corridor
    if dining_w > max_dining + 1.2:
        emit("dining", "Dining", "dining", x_living + pw, y2, max_dining, d2, has_window=False, door_to="living")
        emit("crockery", "Crockery & Bar", "storage", x_living + pw + max_dining, y2, dining_w - max_dining, d2,
             door_to="dining")
    else:
        emit("dining", "Dining", "dining", x_living + pw, y2, dining_w, d2, has_window=False, door_to="living")
    if x_office is not None:
        # Store on the family-lounge side, powder room on the bedroom side: a powder room
        # may not share a wall with a living space.
        pr_w = min(1.8, cols["office"])
        st_w = cols["office"] - pr_w
        if st_w >= 0.8:
            emit("officestore", "Office Store", "storage", x_office, y2, st_w, d2, door_to="office")
        else:
            pr_w = cols["office"]
            st_w = 0.0
        emit("powder", "Powder Room", "bathroom", x_office + st_w, y2, pr_w, d2, door_to="passage", has_window=False)

    ensuites = int(prog.get("ensuites") or 1)
    common = int(prog.get("common_baths") or 0)
    for i, (key, name, bx, bw) in enumerate(bed_xs):
        slot = round(min(BATH_SLOT_W, bw - MIN_LOBBY_W), 3)
        cx = bx
        if i < ensuites:
            emit(f"{key}bath", f"{name} Ensuite", "bathroom", cx, y2, slot, d2,
                 door_to=key, door_child_of=key, has_window=False)
        elif common > 0:
            common -= 1
            emit(f"{key}cbath", "Common Bathroom", "bathroom", cx, y2, slot, d2,
                 door_to="passage", has_window=False)
        else:
            emit(f"{key}wardrobe", f"{name} Wardrobe", "closet", cx, y2, slot, d2, door_child_of=key)
        cx += slot
        lobby_w = bw - slot
        if i == 0 and big and lobby_w - MIN_LOBBY_W >= 1.4:
            closet_w = round(lobby_w - MIN_LOBBY_W, 3)
            emit("mcloset", "Walk-in Closet", "closet", cx, y2, closet_w, d2, door_child_of=key)
            cx += closet_w
            lobby_w = bw - slot - closet_w
        emit(f"{key}lobby", f"{name} Lobby", "passage", cx, y2, lobby_w, d2, door_to="passage")

    # ------------------------------------------------------------ R3: the entry row
    emit("shaft", "MEP Shaft", "shaft", 0, y3, SHAFT_W, d3, has_window=False)
    x = SHAFT_W
    if servant:
        emit("servantbath", "Servant Bath", "servant", x, y3, kw - SHAFT_W, d3, door_child_of="servant")
    else:
        emit("shoestore", "Shoe & Linen Store", "storage", x, y3, kw - SHAFT_W, d3, door_to="foyer")
    x = kw
    foyer_w = round(min(2.6, max(1.8, (x_private - x) * 0.6)), 3)
    emit("foyer", "Entrance Foyer", "entrance", x, y3, foyer_w, d3, door_to="dining",
         main_entrance=True, entry_edge=entry_edge)
    x += foyer_w
    if beds >= 4 and x_office is None:
        # Guest powder room off the foyer, against the corridor wall.
        emit("powder", "Powder Room", "bathroom", x, y3, 1.8, d3, door_to="foyer", has_window=False)
        x += 1.8
    emit("passage", "Private Passage", "passage", x, y3, plan_end - x, d3, door_to="foyer")

    notes = [
        "Rooms sized from the brief for this BHK tier and scaled to the carpet area "
        f"(x{f:.2f}); the envelope follows the rooms, nothing is stretched to fill space.",
        "Main door -> foyer -> dining and living; bedrooms open onto lobbies off the private passage.",
        "Every habitable room, kitchen included, sits on the facade; wet areas stack behind them.",
    ]
    return rooms, notes


def plan_unit_mirrored(box, unit_type, carpet, entry_edge, uid, unit_index, exterior_edges):
    return plan_unit(box, unit_type, carpet, entry_edge, uid, unit_index, exterior_edges, mirror=True)


# ---------------------------------------------------------------- livability score
HABITABLE = {"bedroom", "living", "kitchen", "dining", "office", "family", "study"}


def livability_defects(rooms: Sequence[Dict[str, Any]]) -> List[str]:
    """Rooms no-one could furnish: corridor-shaped or too narrow. Ranked ahead of the
    soft Vastu placements when choosing between planners."""
    out = []
    for r in rooms:
        w, h = float(r.get("w") or 0), float(r.get("h") or 0)
        if w <= 0 or h <= 0:
            continue
        short, long_ = min(w, h), max(w, h)
        rtype = str(r.get("type"))
        if rtype in HABITABLE:
            min_short = 2.2 if rtype == "kitchen" else 2.4
            if short < min_short:
                out.append(f"{r.get('id')}: {short:.2f} m wide is too narrow for a {rtype}")
            if long_ / short > 2.3:
                out.append(f"{r.get('id')}: {long_:.1f} x {short:.1f} m is corridor-shaped")
        elif rtype in ("bathroom", "pooja", "servant", "storage", "pantry", "closet") and long_ / short > 3.2:
            out.append(f"{r.get('id')}: {long_:.1f} x {short:.1f} m is a strip, not a room")
    return out
