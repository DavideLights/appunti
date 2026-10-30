"""High-fidelity Excalidraw to PNG renderer.

Renders Excalidraw JSON diagrams to crisp, high-resolution PNGs
using Pillow and standard Liberation/Arial fonts.
"""
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

LIB_DIR = Path("/usr/share/fonts/liberation")
FONT_REGULAR = str(LIB_DIR / "LiberationSans-Regular.ttf")
FONT_BOLD = str(LIB_DIR / "LiberationSans-Bold.ttf")


def render_excalidraw(json_path: Path, out_png: Path, scale: float = 2.0, pad: int = 24):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    elements = [e for e in data.get("elements", []) if not e.get("isDeleted", False)]
    if not elements:
        raise ValueError(f"No active elements in {json_path}")

    # Compute bounding box
    min_x, min_y = float("inf"), float("inf")
    max_x, max_y = float("-inf"), float("-inf")

    for e in elements:
        x, y = e.get("x", 0), e.get("y", 0)
        t = e.get("type")
        if t in ("rectangle", "text"):
            w = e.get("width", 0)
            h = e.get("height", 0)
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x + w)
            max_y = max(max_y, y + h)
        elif t in ("arrow", "line"):
            pts = e.get("points", [[0, 0]])
            for px, py in pts:
                min_x = min(min_x, x + px)
                min_y = min(min_y, y + py)
                max_x = max(max_x, x + px)
                max_y = max(max_y, y + py)

    min_x -= pad
    min_y -= pad
    max_x += pad
    max_y += pad

    total_w = int(math.ceil((max_x - min_x) * scale))
    total_h = int(math.ceil((max_y - min_y) * scale))

    # Base image with white background
    img = Image.new("RGBA", (total_w, total_h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    def tx(x_val):
        return (x_val - min_x) * scale

    def ty(y_val):
        return (y_val - min_y) * scale

    def parse_color(c_str, alpha=255):
        if not c_str or c_str == "transparent":
            return None
        c_str = c_str.lstrip("#")
        if len(c_str) == 6:
            r = int(c_str[0:2], 16)
            g = int(c_str[2:4], 16)
            b = int(c_str[4:6], 16)
            return (r, g, b, alpha)
        return (0, 0, 0, alpha)

    # Separate elements: draw grouping rectangles / background bands first, then lifelines/arrows, then boxes, then text
    # Excalidraw element order is z-order!
    for e in elements:
        t = e.get("type")
        opacity = e.get("opacity", 100) / 100.0
        alpha_fill = int(255 * opacity)
        alpha_stroke = int(255 * (1.0 if opacity > 0.6 else opacity * 1.5))

        stroke_color = parse_color(e.get("strokeColor"), alpha_stroke)
        bg_color = parse_color(e.get("backgroundColor"), alpha_fill)
        stroke_w = max(1, int(round(e.get("strokeWidth", 1) * scale)))
        is_dashed = e.get("strokeStyle") == "dashed"

        if t == "rectangle":
            x0 = tx(e["x"])
            y0 = ty(e["y"])
            x1 = tx(e["x"] + e["width"])
            y1 = ty(e["y"] + e["height"])
            r_obj = e.get("roundness")
            radius = int(round(8 * scale)) if r_obj else 0

            # If dashed rectangle, Pillow rounded_rectangle doesn't support dashes, so draw fill then dashed outline
            if radius > 0:
                if bg_color:
                    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=bg_color)
                if stroke_color:
                    if is_dashed:
                        # Draw dashed border
                        dash_len = int(8 * scale)
                        gap_len = int(5 * scale)
                        def draw_dashed_h(y, start_x, end_x):
                            curr = start_x
                            while curr < end_x:
                                nxt = min(curr + dash_len, end_x)
                                draw.line([(curr, y), (nxt, y)], fill=stroke_color, width=stroke_w)
                                curr += dash_len + gap_len
                        def draw_dashed_v(x, start_y, end_y):
                            curr = start_y
                            while curr < end_y:
                                nxt = min(curr + dash_len, end_y)
                                draw.line([(x, curr), (x, nxt)], fill=stroke_color, width=stroke_w)
                                curr += dash_len + gap_len
                        draw_dashed_h(y0, x0 + radius, x1 - radius)
                        draw_dashed_h(y1, x0 + radius, x1 - radius)
                        draw_dashed_v(x0, y0 + radius, y1 - radius)
                        draw_dashed_v(x1, y0 + radius, y1 - radius)
                    else:
                        draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, outline=stroke_color, width=stroke_w)
            else:
                if bg_color:
                    draw.rectangle([x0, y0, x1, y1], fill=bg_color)
                if stroke_color:
                    draw.rectangle([x0, y0, x1, y1], outline=stroke_color, width=stroke_w)

        elif t == "line":
            x_base = e["x"]
            y_base = e["y"]
            pts = [(tx(x_base + px), ty(y_base + py)) for px, py in e.get("points", [])]
            if len(pts) >= 3 and pts[0] == pts[-1]:
                # Closed polygon
                if bg_color:
                    draw.polygon(pts, fill=bg_color)
                if stroke_color:
                    draw.polygon(pts, outline=stroke_color)
                    # redraw outline to ensure stroke width
                    if stroke_w > 1:
                        for i in range(len(pts) - 1):
                            draw.line([pts[i], pts[i+1]], fill=stroke_color, width=stroke_w)
            else:
                # Open polyline
                if stroke_color:
                    if is_dashed:
                        dash_len = int(7 * scale)
                        gap_len = int(5 * scale)
                        for i in range(len(pts) - 1):
                            pA, pB = pts[i], pts[i+1]
                            seg_len = math.hypot(pB[0] - pA[0], pB[1] - pA[1])
                            if seg_len == 0:
                                continue
                            steps = int(seg_len // (dash_len + gap_len))
                            dx = (pB[0] - pA[0]) / seg_len
                            dy = (pB[1] - pA[1]) / seg_len
                            for s in range(steps + 1):
                                st_x = pA[0] + s * (dash_len + gap_len) * dx
                                st_y = pA[1] + s * (dash_len + gap_len) * dy
                                en_x = min(pB[0], st_x + dash_len * dx) if dx >= 0 else max(pB[0], st_x + dash_len * dx)
                                en_y = min(pB[1], st_y + dash_len * dy) if dy >= 0 else max(pB[1], st_y + dash_len * dy)
                                draw.line([(st_x, st_y), (en_x, en_y)], fill=stroke_color, width=stroke_w)
                    else:
                        draw.line(pts, fill=stroke_color, width=stroke_w)

        elif t == "arrow":
            x_base = e["x"]
            y_base = e["y"]
            pts = [(tx(x_base + px), ty(y_base + py)) for px, py in e.get("points", [])]
            if stroke_color and len(pts) >= 2:
                if is_dashed:
                    dash_len = int(7 * scale)
                    gap_len = int(5 * scale)
                    for i in range(len(pts) - 1):
                        pA, pB = pts[i], pts[i+1]
                        seg_len = math.hypot(pB[0] - pA[0], pB[1] - pA[1])
                        if seg_len == 0:
                            continue
                        steps = int(seg_len // (dash_len + gap_len))
                        dx = (pB[0] - pA[0]) / seg_len
                        dy = (pB[1] - pA[1]) / seg_len
                        for s in range(steps + 1):
                            st_x = pA[0] + s * (dash_len + gap_len) * dx
                            st_y = pA[1] + s * (dash_len + gap_len) * dy
                            en_x = min(pB[0], st_x + dash_len * dx) if dx >= 0 else max(pB[0], st_x + dash_len * dx)
                            en_y = min(pB[1], st_y + dash_len * dy) if dy >= 0 else max(pB[1], st_y + dash_len * dy)
                            draw.line([(st_x, st_y), (en_x, en_y)], fill=stroke_color, width=stroke_w)
                else:
                    draw.line(pts, fill=stroke_color, width=stroke_w)

                # Arrowhead
                if e.get("endArrowhead") == "arrow":
                    ex, ey = pts[-1]
                    sx, sy = pts[-2]
                    ang = math.atan2(ey - sy, ex - sx)
                    L = 10 * scale
                    p1 = (ex - L * math.cos(ang - 0.45), ey - L * math.sin(ang - 0.45))
                    p2 = (ex - L * math.cos(ang + 0.45), ey - L * math.sin(ang + 0.45))
                    draw.polygon([(ex, ey), p1, p2], fill=stroke_color)

        elif t == "text":
            font_sz = int(round(e.get("fontSize", 16) * scale))
            eid = e.get("id", "")
            is_non_bold_id = (
                eid.startswith("lbl_")
                or eid.startswith("ht2_")
                or eid.startswith("st_")
                or eid in ("subtitle", "gen_lbl", "comp_lbl", "grp_core_lbl", "grp_net_lbl")
            )
            is_bold = not is_non_bold_id and (
                font_sz >= int(17 * scale)
                or eid.startswith("ms_")
                or eid.startswith("md_")
                or eid.startswith("ht1_")
                or eid.startswith("ft1_")
                or eid.startswith("nm_")
                or eid in ("title", "txt_p1", "txt_p2", "txt_p3")
            )
            font_path = FONT_BOLD if is_bold else FONT_REGULAR
            f = ImageFont.truetype(font_path, font_sz)

            text_str = e.get("text", "")
            lines = text_str.split("\n")
            line_h = font_sz * 1.25

            align = e.get("textAlign", "left")
            bx0 = tx(e["x"])
            by0 = ty(e["y"])
            bw = e.get("width", 0) * scale

            for i, line in enumerate(lines):
                lw = f.getlength(line)
                if align == "center":
                    lx = bx0 + (bw - lw) / 2
                elif align == "right":
                    lx = bx0 + bw - lw
                else:
                    lx = bx0
                ly = by0 + i * line_h
                draw.text((lx, ly), line, fill=stroke_color, font=f)

    # Convert RGBA to RGB with white background
    final_img = Image.new("RGB", (total_w, total_h), (255, 255, 255))
    final_img.paste(img, (0, 0), img)
    final_img.save(out_png, "PNG", optimize=True)
    print(f"[+] Successfully rendered {json_path.name} -> {out_png} ({total_w}x{total_h}px)")


if __name__ == "__main__":
    import sys
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/home/davidel/appunti/tesi/classdiagr.excalidraw")
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("/home/davidel/appunti/tesi/classdiagr.png")
    render_excalidraw(src, dst)
