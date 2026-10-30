"""Generate slide-optimized Excalidraw UML Sequence Diagram for UC-03 with 24px fonts.

Updates /home/davidel/appunti/tesi/seqdiagram.excalidraw (and synced copies)
with larger, balanced font sizes (24px for messages and lifeline headers,
21px for phase tags, 18px for header subtitles) and a 2.15:1 widescreen layout
that fills the 16:9 presentation slide card without wasted margins.
"""
import json
from pathlib import Path
from PIL import ImageFont

OUT_SEQ = Path("/home/davidel/appunti/tesi/seqdiagram.excalidraw")
OUT_UC03 = Path("/home/davidel/appunti/tesi/uc03_sequence_diagram.excalidraw")
OUT_HOME = Path("/home/davidel/uc03_sequence_diagram.excalidraw")
OUT_DL = Path("/home/davidel/Scaricati/seqdiagram.excalidraw")

FONT_REG = "/usr/share/fonts/liberation/LiberationSans-Regular.ttf"
FONT_BLD = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"

elements = []
_seed = 1000
_idx = 1


def _next_meta():
    global _seed, _idx
    _seed += 17
    _idx += 1
    return _seed, f"b{_idx:03d}"


def add_rect(
    el_id, x, y, w, h, stroke="#1e293b", bg="transparent",
    stroke_w=2, stroke_style="solid", roundness=6, opacity=100
):
    seed, idx = _next_meta()
    elements.append({
        "type": "rectangle",
        "version": 2,
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
        "updated": 1793195000000,
        "link": None,
        "locked": False,
        "created": 1793195000000,
    })


def add_text(
    el_id, x, y, text, font_size=24, color="#0f172a", align="center", bold=False
):
    seed, idx = _next_meta()
    lines = text.split("\n")
    f = ImageFont.truetype(FONT_BLD if bold else FONT_REG, int(font_size))
    w = max(f.getlength(line) for line in lines) + 10
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
        "version": 2,
        "versionNonce": seed + 1,
        "isDeleted": False,
        "boundElements": [],
        "updated": 1793195000000,
        "created": 1793195000000,
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


def add_line(
    el_id, x1, y1, x2, y2, stroke="#64748b", stroke_w=2, stroke_style="dashed"
):
    seed, idx = _next_meta()
    elements.append({
        "id": el_id,
        "type": "line",
        "x": float(x1),
        "y": float(y1),
        "width": float(abs(x2 - x1)),
        "height": float(abs(y2 - y1)),
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
        "version": 2,
        "versionNonce": seed + 2,
        "isDeleted": False,
        "boundElements": [],
        "updated": 1793195000000,
        "created": 1793195000000,
        "link": None,
        "locked": False,
        "points": [[0.0, 0.0], [float(x2 - x1), float(y2 - y1)]],
        "startBinding": None,
        "endBinding": None,
        "lastCommittedPoint": None,
        "startArrowhead": None,
        "endArrowhead": None,
    })


def add_arrow(
    el_id, points, stroke="#1e293b", stroke_w=2,
    stroke_style="solid", end_arrow="arrow"
):
    seed, idx = _next_meta()
    x0, y0 = points[0]
    rel_pts = [[float(px - x0), float(py - y0)] for px, py in points]
    xs = [p[0] for p in rel_pts]
    ys = [p[1] for p in rel_pts]
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
        "version": 2,
        "versionNonce": seed + 3,
        "isDeleted": False,
        "boundElements": [],
        "updated": 1793195000000,
        "created": 1793195000000,
        "link": None,
        "locked": False,
        "points": rel_pts,
        "startBinding": None,
        "endBinding": None,
        "lastCommittedPoint": None,
        "startArrowhead": None,
        "endArrowhead": end_arrow,
        "elbowed": False,
    })


def build_diagram():
    # 5 Lifelines spaced to fit 24px message labels without touching bars (width ~2280px)
    cols = [
        ("ctf", 145,  "CTF Manager",            "(Client / CTFd)",        "#1e40af", "#dbeafe"),
        ("svc", 730,  "API + ChallengeService", "(API)",                  "#1e40af", "#dbeafe"),
        ("ovn", 1255, "OVNVerifier",            "(Context Manager RAII)", "#0284c7", "#e0f2fe"),
        ("eng", 1730, "IncusEngine",            "(ZFS CoW & OVN SDN)",    "#0f766e", "#ccfbf1"),
        ("sbx", 2160, "Sandbox Verify",         "(Cloni + Runner)",       "#15803d", "#dcfce7"),
    ]
    X = {k: cx for k, cx, *_ in cols}

    # Phase background bands (compact vertically for 2.15:1 widescreen ratio)
    BAND_X = 10
    BAND_W = 2295
    phases = [
        ("p1", 214, 462,  "FASE 1 — Setup Sandbox",                 "#eff6ff", "#93c5fd", "#1e40af", 335),
        ("p2", 476, 804,  "FASE 2 — Controlli Readiness & Verifica", "#f0fdf4", "#86efac", "#15803d", 485),
        ("p3", 818, 1024, "FASE 3 — Teardown",                      "#fff7ed", "#fdba74", "#c2410c", 275),
    ]
    for pid, y_top, y_bot, label, bg, border, txt_col, tag_w in phases:
        add_rect(
            f"band_{pid}", BAND_X, y_top, BAND_W, y_bot - y_top,
            stroke=border, bg=bg, stroke_w=1, stroke_style="dashed", roundness=8, opacity=55
        )
        # Placed in the clear gap between CTF Manager lifeline (x=145) and ChallengeService (x=730)
        add_rect(f"tag_{pid}", 170, y_top + 10, tag_w, 38, stroke=border, bg="#ffffff", stroke_w=1, roundness=6, opacity=98)
        add_text(f"txt_{pid}", 186, y_top + 16, label, font_size=21, color=txt_col, align="left", bold=True)

    # Lifeline headers and dashed vertical lines
    TOP_Y = 20
    BOX_W = 290
    BOX_H = 76
    BOT_Y = 1076

    for key, cx, title, sub, stroke, bg in cols:
        line_end = 955 if key == "sbx" else BOT_Y
        add_line(f"ll_{key}", cx, TOP_Y + BOX_H, cx, line_end, stroke="#94a3b8", stroke_w=2, stroke_style="dashed")
        add_rect(f"hdr_{key}", cx - BOX_W / 2, TOP_Y, BOX_W, BOX_H, stroke=stroke, bg=bg, stroke_w=2, roundness=8)
        add_text(f"ht1_{key}", cx, TOP_Y + 11, title, font_size=24, color="#0f172a", align="center", bold=True)
        add_text(f"ht2_{key}", cx, TOP_Y + 44, sub, font_size=18, color=stroke, align="center")

    # Activation bars (width = 18, centered on lifeline X, aligned to exact call/return Y)
    ACT_W = 18
    activations = [
        ("act_svc",    X["svc"], 142, 1054, "#1e40af", "#bfdbfe"),
        ("act_ovn_1",  X["ovn"], 250, 440,  "#0284c7", "#bae6fd"),
        ("act_ovn_2",  X["ovn"], 508, 788,  "#0284c7", "#bae6fd"),
        ("act_ovn_3",  X["ovn"], 852, 1006, "#0284c7", "#bae6fd"),
        ("act_eng_1",  X["eng"], 288, 408,  "#0f766e", "#99f6e4"),
        ("act_eng_2a", X["eng"], 544, 646,  "#0f766e", "#99f6e4"),
        ("act_eng_2b", X["eng"], 690, 772,  "#0f766e", "#99f6e4"),
        ("act_eng_3",  X["eng"], 886, 988,  "#0f766e", "#99f6e4"),
        ("act_sbx",    X["sbx"], 366, 916,  "#15803d", "#bbf7d0"),
    ]
    for aid, cx, y1, y2, stroke, bg in activations:
        add_rect(aid, cx - ACT_W / 2, y1, ACT_W, y2 - y1, stroke=stroke, bg=bg, stroke_w=2, roundness=2)

    # Helper for single-hop message arrows with 24px labels
    FONT_MSG = 24
    f_msg = ImageFont.truetype(FONT_REG, FONT_MSG)

    def msg(mid, c_from, c_to, y, label, dashed=False, color="#1e293b"):
        going_right = X[c_to] > X[c_from]
        x1 = X[c_from] + (ACT_W / 2 if going_right else -ACT_W / 2)
        if c_from == "ctf":
            x1 = X["ctf"]
        x2 = X[c_to] - (ACT_W / 2 if going_right else -ACT_W / 2)
        if c_to == "ctf":
            x2 = X["ctf"]

        tw = f_msg.getlength(label)
        span = abs(x2 - x1)
        assert tw < span - 14, f"Label '{label}' ({tw:.1f}px) exceeds span ({span:.1f}px)"

        add_arrow(
            f"arr_{mid}", [[x1, y], [x2, y]],
            stroke=color, stroke_w=2,
            stroke_style="dashed" if dashed else "solid",
            end_arrow="arrow"
        )
        mid_x = (x1 + x2) / 2
        add_text(f"lbl_{mid}", mid_x, y - 30, label, font_size=FONT_MSG, color=color, align="center")

    def self_msg(mid, col, y1, y2, label, color="#1e40af"):
        x0 = X[col] + ACT_W / 2
        add_arrow(
            f"arr_{mid}",
            [[x0, y1], [x0 + 44, y1], [x0 + 44, y2], [x0, y2]],
            stroke=color, stroke_w=2, stroke_style="solid", end_arrow="arrow"
        )
        ty = (y1 + y2) / 2 - 15
        add_text(f"lbl_{mid}", x0 + 54, ty, label, font_size=FONT_MSG, color=color, align="left")

    # --- INGRESSO & LOCK ---
    msg("m1", "ctf", "svc", 142, "1. POST /teams/{team_k}/verificator", color="#0f172a")
    self_msg("m2", "svc", 162, 198, "2. Interpreta Configurazione YAML", color="#1e40af")

    # --- FASE 1: SETUP SANDBOX ---
    msg("m3",    "svc", "ovn", 250, "3. __aenter__(config, team_k)", color="#0284c7")
    msg("m4",    "ovn", "eng", 288, "4. Crea la rete", color="#0f766e")
    msg("m5",    "ovn", "eng", 336, "5. Clona ed avvia", color="#0f766e")
    msg("m7",    "eng", "sbx", 366, "7. Effettua il boot dei cloni", color="#15803d")
    msg("m7_r1", "eng", "ovn", 408, "Cloni e rete attivi", dashed=True, color="#0f766e")
    msg("m7_r2", "ovn", "svc", 440, "Sandbox pronta, rilascia lock team:{team_k}", dashed=True, color="#0284c7")

    # --- FASE 2: CONTROLLI READINESS & VERIFICA ---
    msg("m8",     "svc", "ovn", 508, "8. run_checks()", color="#0284c7")
    msg("m9",     "ovn", "eng", 544, "9. esegui readiness command [retry loop]", color="#0f766e")
    msg("m9b",    "eng", "sbx", 574, "esegui il comando", color="#15803d")
    msg("m9_r1",  "sbx", "eng", 620, "exit_code == 0", dashed=True, color="#15803d")
    msg("m9_r2",  "eng", "ovn", 646, "ExecResult", dashed=True, color="#0f766e")

    msg("m10",    "ovn", "eng", 690, "10. esegui comandi [verifica]", color="#0f766e")
    msg("m10b",   "eng", "sbx", 716, "Esegui script di verifica nei cloni", color="#15803d")
    msg("m10_r1", "sbx", "eng", 760, "exit_code == 0 (patch valida)", dashed=True, color="#15803d")
    msg("m10_r2", "eng", "ovn", 772, "ExecResult", dashed=True, color="#0f766e")
    msg("m11",    "ovn", "svc", 788, "11. VerifyResultResp (passed = true)", dashed=True, color="#0284c7")

    # --- FASE 3: TEARDOWN ---
    msg("m12",    "svc", "ovn", 852, "12. __aexit__() [Teardown deterministico]", color="#c2410c")
    msg("m13",    "ovn", "eng", 886, "13. elimina istanze e cloni", color="#c2410c")
    msg("m13b",   "eng", "sbx", 916, "Arresta ed elimina container sandbox", color="#b91c1c")

    # Destruction X on Sandbox lifeline at y=955
    sx, sy = X["sbx"], 955
    add_line("sbx_x1", sx - 14, sy - 14, sx + 14, sy + 14, stroke="#dc2626", stroke_w=3, stroke_style="solid")
    add_line("sbx_x2", sx + 14, sy - 14, sx - 14, sy + 14, stroke="#dc2626", stroke_w=3, stroke_style="solid")

    msg("m14",    "ovn", "eng", 944, "14. elimina la rete [Switch OVN]", color="#c2410c")
    msg("m14_r1", "eng", "ovn", 988, "Teardown completato", dashed=True, color="#c2410c")
    msg("m14_r2", "ovn", "svc", 1006, "Sandbox rimossa, rilascia lock verify:{team_k}", dashed=True, color="#c2410c")

    # --- 15. RISPOSTA HTTP ---
    msg("m15", "svc", "ctf", 1054, "15. HTTP 200 OK (VerifyResultResp: passed=true)", dashed=True, color="#15803d")

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
    for target in (OUT_SEQ, OUT_UC03, OUT_HOME, OUT_DL):
        if target.parent.exists():
            target.write_text(raw, encoding="utf-8")
            print(f"[+] Saved {target} ({len(elements)} elements)")


if __name__ == "__main__":
    build_diagram()
