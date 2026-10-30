"""Generate a clean, error-free Excalidraw UML Class Diagram for BlueAgent (slide-ready).

Exact 11 classes from user specification:
1. LockRegistry
2. TwoTierLock
3. HostNetworkManager
4. WireGuardManager
5. CommandRunner (<<interface>>)
6. OVNVerifier
7. ContainerEngine (<<abstract>>)
8. IncusEngine
9. LifecycleManager
10. ImageService
11. ImageBuilder

Style: Minimalist class boxes (stereotype + class name), standard UML notation:
- Generalization: solid line + hollow triangle (IncusEngine -> ContainerEngine, no multiplicities)
- Composition: filled diamond at composite end + arrow at part end (LockRegistry 1 *--> 0..* TwoTierLock)
- Directed Associations: solid arrow + explicit multiplicities (1, 0..*) + concise role/verb
"""
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_TESI = Path("/home/davidel/appunti/tesi/blueagent_class_diagram.excalidraw")
OUT_HOME = Path("/home/davidel/blueagent_class_diagram.excalidraw")
PREVIEW_PNG = Path("/home/davidel/.gemini/antigravity/brain/0c7fb467-238e-486e-aebe-55869fcb1806/scratch/class_diagram_preview.png")

elements = []
_seed = 2000
_idx = 1


def _next_meta():
    global _seed, _idx
    _seed += 19
    _idx += 1
    return _seed, f"c{_idx:03d}"


def add_rect(
    el_id, x, y, w, h, stroke="#1e293b", bg="#ffffff",
    stroke_w=2, stroke_style="solid", roundness=8, opacity=100
):
    seed, idx = _next_meta()
    elements.append({
        "type": "rectangle",
        "version": 1,
        "versionNonce": seed,
        "index": idx,
        "isDeleted": False,
        "id": el_id,
        "fillStyle": "solid",
        "strokeWidth": stroke_w,
        "strokeStyle": stroke_style,
        "roughness": 0,
        "opacity": opacity,
        "angle": 0,
        "x": float(x),
        "y": float(y),
        "strokeColor": stroke,
        "backgroundColor": bg,
        "width": float(w),
        "height": float(h),
        "seed": seed,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 3, "value": roundness} if roundness else None,
        "boundElements": [],
        "updated": 1793196000000,
        "link": None,
        "locked": False,
        "created": 1793196000000,
    })


def add_polygon(el_id, points, stroke="#1e293b", bg="#ffffff", stroke_w=2):
    """Closed polygon (used for UML hollow triangle and filled composition diamond)."""
    seed, idx = _next_meta()
    x0, y0 = points[0]
    rel = [[float(px - x0), float(py - y0)] for px, py in points]
    if rel[-1] != [0.0, 0.0]:
        rel.append([0.0, 0.0])
    xs = [p[0] for p in rel]
    ys = [p[1] for p in rel]
    elements.append({
        "id": el_id,
        "type": "line",
        "x": float(x0),
        "y": float(y0),
        "width": float(max(xs) - min(xs)),
        "height": float(max(ys) - min(ys)),
        "angle": 0,
        "strokeColor": stroke,
        "backgroundColor": bg,
        "fillStyle": "solid",
        "strokeWidth": stroke_w,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "index": idx,
        "roundness": None,
        "seed": seed,
        "version": 1,
        "versionNonce": seed + 1,
        "isDeleted": False,
        "boundElements": [],
        "updated": 1793196000000,
        "created": 1793196000000,
        "link": None,
        "locked": False,
        "points": rel,
        "startBinding": None,
        "endBinding": None,
        "lastCommittedPoint": None,
        "startArrowhead": None,
        "endArrowhead": None,
    })


def add_arrow(el_id, points, stroke="#1e293b", stroke_w=2, stroke_style="solid", end_arrow="arrow"):
    seed, idx = _next_meta()
    x0, y0 = points[0]
    rel = [[float(px - x0), float(py - y0)] for px, py in points]
    xs = [p[0] for p in rel]
    ys = [p[1] for p in rel]
    elements.append({
        "id": el_id,
        "type": "arrow",
        "x": float(x0),
        "y": float(y0),
        "width": float(max(xs) - min(xs)),
        "height": float(max(ys) - min(ys)),
        "angle": 0,
        "strokeColor": stroke,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": stroke_w,
        "strokeStyle": stroke_style,
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "index": idx,
        "roundness": None,
        "seed": seed,
        "version": 1,
        "versionNonce": seed + 2,
        "isDeleted": False,
        "boundElements": [],
        "updated": 1793196000000,
        "created": 1793196000000,
        "link": None,
        "locked": False,
        "points": rel,
        "startBinding": None,
        "endBinding": None,
        "lastCommittedPoint": None,
        "startArrowhead": None,
        "endArrowhead": end_arrow,
        "elbowed": False,
    })


def add_text(el_id, x, y, text, font_size=16, color="#0f172a", align="center"):
    seed, idx = _next_meta()
    lines = text.split("\n")
    f = ImageFont.truetype("/usr/share/fonts/liberation/LiberationSans-Regular.ttf", int(font_size))
    w = max(f.getlength(line) for line in lines) + 8
    h = len(lines) * font_size * 1.25
    tx = x - w / 2 if align == "center" else (x - w if align == "right" else x)
    elements.append({
        "id": el_id,
        "type": "text",
        "x": float(tx),
        "y": float(y),
        "width": float(w),
        "height": float(h),
        "angle": 0,
        "strokeColor": color,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "index": idx,
        "roundness": None,
        "seed": seed,
        "version": 1,
        "versionNonce": seed + 3,
        "isDeleted": False,
        "boundElements": [],
        "updated": 1793196000000,
        "created": 1793196000000,
        "link": None,
        "locked": False,
        "text": text,
        "fontSize": font_size,
        "baseFontSize": font_size,
        "fontFamily": 2,
        "textAlign": align,
        "verticalAlign": "top",
        "containerId": None,
        "originalText": text,
        "autoResize": True,
        "lineHeight": 1.25,
        "labelPosition": None,
    })


def build_diagram():
    # Title
    add_text(
        "title", 890, 22,
        "BlueAgent — Architettura delle Classi Principali (UML Class Diagram)",
        font_size=24, color="#0f172a", align="center"
    )
    add_text(
        "subtitle", 890, 56,
        "Runtime Container, Verifica OVN, Compilazione Immagini, Riconciliazione, Lock a Due Livelli e Rete Host",
        font_size=15, color="#475569", align="center"
    )

    # Subsystem background containers (subtle dashed grouping boxes)
    add_rect(
        "grp_core", 45, 98, 1275, 650,
        stroke="#93c5fd", bg="#f8fafc", stroke_w=1, stroke_style="dashed", roundness=12, opacity=55
    )
    add_text("grp_core_lbl", 65, 108, "Orchestrazione Container, Sandbox OVN, Immagini & Sincronizzazione", font_size=13, color="#1e40af", align="left")

    add_rect(
        "grp_net", 1355, 98, 380, 650,
        stroke="#6ee7b7", bg="#f0fdf4", stroke_w=1, stroke_style="dashed", roundness=12, opacity=45
    )
    add_text("grp_net_lbl", 1375, 108, "Sottosistema Rete Host (Bridge & VPN)", font_size=13, color="#15803d", align="left")

    # Class Box Geometry: 5 columns x 3 rows
    BOX_W = 230
    BOX_H = 74

    # Center coordinates (cx, cy) of the 11 classes
    classes = {
        # Row 1 (y_center = 195)
        "ImageService":       (515,  195, None,            "#1e40af", "#dbeafe"),
        "ImageBuilder":       (855,  195, None,            "#1e40af", "#dbeafe"),
        "HostNetworkManager": (1545, 195, None,            "#15803d", "#dcfce7"),

        # Row 2 (y_center = 430)
        "OVNVerifier":        (175,  430, "<<RAII>>",      "#0284c7", "#e0f2fe"),
        "ContainerEngine":    (515,  430, "<<abstract>>",  "#0f766e", "#ccfbf1"),
        "LifecycleManager":   (855,  430, None,            "#c2410c", "#ffedd5"),
        "LockRegistry":       (1185, 430, None,            "#6d28d9", "#ede9fe"),
        "CommandRunner":      (1545, 430, "<<interface>>", "#0f766e", "#ccfbf1"),

        # Row 3 (y_center = 665)
        "IncusEngine":        (515,  665, None,            "#0f766e", "#f0fdfa"),
        "TwoTierLock":        (1185, 665, None,            "#6d28d9", "#f5f3ff"),
        "WireGuardManager":   (1545, 665, None,            "#15803d", "#dcfce7"),
    }

    for name, (cx, cy, stereo, stroke, bg) in classes.items():
        x0 = cx - BOX_W / 2
        y0 = cy - BOX_H / 2
        add_rect(f"cls_{name}", x0, y0, BOX_W, BOX_H, stroke=stroke, bg=bg, stroke_w=2, roundness=8)
        if stereo:
            add_text(f"st_{name}", cx, y0 + 12, stereo, font_size=13, color=stroke, align="center")
            add_text(f"nm_{name}", cx, y0 + 34, name, font_size=18, color="#0f172a", align="center")
        else:
            add_text(f"nm_{name}", cx, y0 + 25, name, font_size=18, color="#0f172a", align="center")

    def box_edge(name, side):
        cx, cy, *_ = classes[name]
        if side == "top":
            return cx, cy - BOX_H / 2
        if side == "bottom":
            return cx, cy + BOX_H / 2
        if side == "left":
            return cx - BOX_W / 2, cy
        if side == "right":
            return cx + BOX_W / 2, cy
        raise ValueError(side)

    # 1. Generalization: IncusEngine --|> ContainerEngine (hollow triangle at ContainerEngine bottom)
    ix, iy = box_edge("IncusEngine", "top")
    cx, cy = box_edge("ContainerEngine", "bottom")
    tri_h = 16
    tri_w = 11
    # Shaft from IncusEngine top up to base of hollow triangle
    add_arrow("gen_incus", [[ix, iy], [cx, cy + tri_h]], stroke="#0f766e", stroke_w=2, end_arrow=None)
    # Hollow triangle pointing up to (cx, cy)
    add_polygon(
        "gen_tri",
        [[cx, cy], [cx - tri_w, cy + tri_h], [cx + tri_w, cy + tri_h], [cx, cy]],
        stroke="#0f766e", bg="#ffffff", stroke_w=2
    )
    add_text("gen_lbl", cx + 14, (iy + cy) / 2 - 10, "extends", font_size=13, color="#0f766e", align="left")

    # 2. Composition: LockRegistry 1 *--> 0..* TwoTierLock (filled diamond at LockRegistry bottom)
    lx, ly = box_edge("LockRegistry", "bottom")
    tx, ty = box_edge("TwoTierLock", "top")
    dm_h = 20
    dm_w = 7
    add_polygon(
        "comp_dm",
        [[lx, ly], [lx - dm_w, ly + dm_h / 2], [lx, ly + dm_h], [lx + dm_w, ly + dm_h / 2], [lx, ly]],
        stroke="#6d28d9", bg="#6d28d9", stroke_w=2
    )
    add_arrow("comp_arr", [[lx, ly + dm_h], [tx, ty]], stroke="#6d28d9", stroke_w=2, end_arrow="arrow")
    add_text("comp_m1", lx - 14, ly + 6, "1", font_size=13, color="#6d28d9", align="right")
    add_text("comp_m2", tx - 14, ty - 24, "0..*", font_size=13, color="#6d28d9", align="right")
    add_text("comp_lbl", lx + 14, (ly + ty) / 2 - 10, "manages", font_size=13, color="#6d28d9", align="left")

    # Helper for straight horizontal association
    def assoc_h(aid, src, dst, label, m_src="1", m_dst="1", color="#334155"):
        going_right = classes[dst][0] > classes[src][0]
        x1, y1 = box_edge(src, "right" if going_right else "left")
        x2, y2 = box_edge(dst, "left" if going_right else "right")
        add_arrow(f"arr_{aid}", [[x1, y1], [x2, y2]], stroke=color, stroke_w=2, end_arrow="arrow")
        mid_x = (x1 + x2) / 2
        add_text(f"lbl_{aid}", mid_x, y1 - 22, label, font_size=13, color=color, align="center")
        if going_right:
            add_text(f"ms_{aid}", x1 + 8, y1 + 6, m_src, font_size=13, color=color, align="left")
            add_text(f"md_{aid}", x2 - 8, y2 + 6, m_dst, font_size=13, color=color, align="right")
        else:
            add_text(f"ms_{aid}", x1 - 8, y1 + 6, m_src, font_size=13, color=color, align="right")
            add_text(f"md_{aid}", x2 + 8, y2 + 6, m_dst, font_size=13, color=color, align="left")

    # Helper for straight vertical association
    def assoc_v(aid, src, dst, label, m_src="1", m_dst="1", color="#334155"):
        going_down = classes[dst][1] > classes[src][1]
        x1, y1 = box_edge(src, "bottom" if going_down else "top")
        x2, y2 = box_edge(dst, "top" if going_down else "bottom")
        add_arrow(f"arr_{aid}", [[x1, y1], [x2, y2]], stroke=color, stroke_w=2, end_arrow="arrow")
        mid_y = (y1 + y2) / 2
        add_text(f"lbl_{aid}", x1 + 12, mid_y - 10, label, font_size=13, color=color, align="left")
        if going_down:
            add_text(f"ms_{aid}", x1 - 12, y1 + 6, m_src, font_size=13, color=color, align="right")
            add_text(f"md_{aid}", x2 - 12, y2 - 24, m_dst, font_size=13, color=color, align="right")
        else:
            add_text(f"ms_{aid}", x1 - 12, y1 - 24, m_src, font_size=13, color=color, align="right")
            add_text(f"md_{aid}", x2 - 12, y2 + 6, m_dst, font_size=13, color=color, align="right")

    # 3. Straight horizontal associations
    assoc_h("img_svc_bld", "ImageService", "ImageBuilder", "triggers", m_src="1", m_dst="1", color="#1e40af")
    assoc_h("ovn_eng", "OVNVerifier", "ContainerEngine", "uses", m_src="0..*", m_dst="1", color="#0284c7")
    assoc_h("lc_eng", "LifecycleManager", "ContainerEngine", "sweeps", m_src="1", m_dst="1", color="#c2410c")
    assoc_h("lc_lock", "LifecycleManager", "LockRegistry", "checks locks", m_src="1", m_dst="1", color="#c2410c")

    # 4. Straight vertical associations
    assoc_v("img_svc_eng", "ImageService", "ContainerEngine", "uses", m_src="1", m_dst="1", color="#1e40af")
    assoc_v("hnet_cmd", "HostNetworkManager", "CommandRunner", "uses", m_src="1", m_dst="1", color="#15803d")
    assoc_v("wg_cmd", "WireGuardManager", "CommandRunner", "uses", m_src="1", m_dst="1", color="#15803d")

    # 5. Two non-crossing L-shaped associations from ImageBuilder:
    # 5a. ImageBuilder (bottom-left) -> ContainerEngine (top-right)
    bx_l = classes["ImageBuilder"][0] - 55
    by_b = classes["ImageBuilder"][1] + BOX_H / 2
    ex_r = classes["ContainerEngine"][0] + 65
    ey_t = classes["ContainerEngine"][1] - BOX_H / 2
    mid_y_elbow = 305
    add_arrow(
        "arr_bld_eng",
        [[bx_l, by_b], [bx_l, mid_y_elbow], [ex_r, mid_y_elbow], [ex_r, ey_t]],
        stroke="#1e40af", stroke_w=2, end_arrow="arrow"
    )
    add_text("ms_bld_eng", bx_l - 10, by_b + 4, "1", font_size=13, color="#1e40af", align="right")
    add_text("md_bld_eng", ex_r + 10, ey_t - 22, "1", font_size=13, color="#1e40af", align="left")
    add_text("lbl_bld_eng", (bx_l + ex_r) / 2, mid_y_elbow - 20, "imports into", font_size=13, color="#1e40af", align="center")

    # 5b. ImageBuilder (right) -> LockRegistry (top)
    bx_r, by_rm = box_edge("ImageBuilder", "right")
    lx_t, ly_t = box_edge("LockRegistry", "top")
    add_arrow(
        "arr_bld_lock",
        [[bx_r, by_rm], [lx_t, by_rm], [lx_t, ly_t]],
        stroke="#6d28d9", stroke_w=2, end_arrow="arrow"
    )
    add_text("ms_bld_lock", bx_r + 8, by_rm + 6, "1", font_size=13, color="#6d28d9", align="left")
    add_text("md_bld_lock", lx_t + 10, ly_t - 22, "1", font_size=13, color="#6d28d9", align="left")
    add_text("lbl_bld_lock", (bx_r + lx_t) / 2, by_rm - 22, "acquires lock", font_size=13, color="#6d28d9", align="center")

    # Legend at the bottom for slide clarity (drawn with vector UML symbols + text)
    LEG_Y = 770
    cy_leg = LEG_Y + 26
    add_rect("leg_box", 45, LEG_Y, 1690, 52, stroke="#cbd5e1", bg="#f8fafc", stroke_w=1, roundness=8)
    add_text("leg_hdr", 185, LEG_Y + 17, "Notazione UML:", font_size=14, color="#0f172a", align="left")

    # Legend 1: Generalization (line + hollow triangle)
    add_arrow("leg_gen_ln", [[325, cy_leg], [363, cy_leg]], stroke="#0f766e", stroke_w=2, end_arrow=None)
    add_polygon("leg_gen_tri", [[377, cy_leg], [363, cy_leg - 8], [363, cy_leg + 8], [377, cy_leg]], stroke="#0f766e", bg="#ffffff", stroke_w=2)
    add_text("leg_gen_txt", 390, LEG_Y + 17, "Generalizzazione (ereditarietà)", font_size=14, color="#334155", align="left")

    # Legend 2: Composition (filled diamond + arrow)
    add_polygon("leg_cmp_dm", [[660, cy_leg], [669, cy_leg - 6], [678, cy_leg], [669, cy_leg + 6], [660, cy_leg]], stroke="#6d28d9", bg="#6d28d9", stroke_w=2)
    add_arrow("leg_cmp_arr", [[678, cy_leg], [718, cy_leg]], stroke="#6d28d9", stroke_w=2, end_arrow="arrow")
    add_text("leg_cmp_txt", 730, LEG_Y + 17, "Composizione (ciclo di vita vincolato)", font_size=14, color="#334155", align="left")

    # Legend 3: Directed association (arrow + multiplicities)
    add_arrow("leg_asc_arr", [[1055, cy_leg], [1105, cy_leg]], stroke="#1e40af", stroke_w=2, end_arrow="arrow")
    add_text("leg_asc_txt", 1118, LEG_Y + 17, "Associazione navigabile con molteplicità (1, 0..*)", font_size=14, color="#334155", align="left")

    doc = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {
            "gridSize": 20,
            "gridStep": 5,
            "gridModeEnabled": False,
            "viewBackgroundColor": "#ffffff",
        },
        "files": {},
    }
    raw = json.dumps(doc, indent=2, ensure_ascii=False)
    OUT_TESI.write_text(raw, encoding="utf-8")
    OUT_HOME.write_text(raw, encoding="utf-8")
    print(f"[+] Saved {OUT_TESI} and {OUT_HOME} ({len(elements)} elements)")


def render_preview():
    img = Image.new("RGB", (1790, 850), "white")
    dr = ImageDraw.Draw(img)
    for el in elements:
        t = el["type"]
        if t == "rectangle":
            x1, y1 = el["x"], el["y"]
            x2, y2 = x1 + el["width"], y1 + el["height"]
            bg = None if el["backgroundColor"] == "transparent" else el["backgroundColor"]
            dr.rounded_rectangle([x1, y1, x2, y2], radius=8, fill=bg, outline=el["strokeColor"], width=el["strokeWidth"])
        elif t == "line":
            x0, y0 = el["x"], el["y"]
            pts = [(x0 + px, y0 + py) for px, py in el["points"]]
            bg = None if el["backgroundColor"] == "transparent" else el["backgroundColor"]
            if len(pts) >= 3 and pts[0] == pts[-1]:
                dr.polygon(pts, fill=bg, outline=el["strokeColor"], width=el["strokeWidth"])
            else:
                dr.line(pts, fill=el["strokeColor"], width=el["strokeWidth"])
        elif t == "arrow":
            x0, y0 = el["x"], el["y"]
            pts = [(x0 + px, y0 + py) for px, py in el["points"]]
            dr.line(pts, fill=el["strokeColor"], width=el["strokeWidth"])
            if el.get("endArrowhead") == "arrow":
                ex, ey = pts[-1]
                sx, sy = pts[-2]
                ang = math.atan2(ey - sy, ex - sx)
                L = 10
                p1 = (ex - L * math.cos(ang - 0.5), ey - L * math.sin(ang - 0.5))
                p2 = (ex - L * math.cos(ang + 0.5), ey - L * math.sin(ang + 0.5))
                dr.polygon([(ex, ey), p1, p2], fill=el["strokeColor"])
        elif t == "text":
            is_bold = el["fontSize"] >= 17 or el["id"].startswith("ms_") or el["id"].startswith("md_")
            f = ImageFont.truetype(
                "/usr/share/fonts/liberation/LiberationSans-Bold.ttf" if is_bold else "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
                int(el["fontSize"])
            )
            dr.text((el["x"], el["y"]), el["text"], fill=el["strokeColor"], font=f)
    img.save(PREVIEW_PNG)
    print(f"[+] Preview saved to {PREVIEW_PNG}")


if __name__ == "__main__":
    build_diagram()
    render_preview()
