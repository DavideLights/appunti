"""Build presentazione_blueagent.pptx (slides 1-3 of the HTML deck + results summary).

Geometry is taken from the browser layout of presentazione_blueagent.html
(1280x720 px canvas == 13.333x7.5 in at 96 dpi, so 1 px == 9525 EMU).
Fonts: Arial (text) and Courier New (code) only. Text widths are computed with
Liberation Sans / Liberation Mono, which are metrically identical to Arial /
Courier New, so code chips line up in PowerPoint as well.
"""
import copy
from pathlib import Path

import cairosvg
from lxml import etree
from PIL import ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

HERE = Path(__file__).resolve().parent
TESI = HERE.parent
HTML_DIR = TESI / 'presentazione_blueagent'
ASSETS = HERE / 'assets'
ASSETS.mkdir(exist_ok=True)
FIG = HERE / 'figures'

FONT = 'Arial'
MONO = 'Courier New'
LIB = Path('/usr/share/fonts/liberation')
_font_files = {
    (FONT, False, False): 'LiberationSans-Regular.ttf',
    (FONT, True, False): 'LiberationSans-Bold.ttf',
    (FONT, False, True): 'LiberationSans-Italic.ttf',
    (FONT, True, True): 'LiberationSans-BoldItalic.ttf',
    (MONO, False, False): 'LiberationMono-Regular.ttf',
    (MONO, True, False): 'LiberationMono-Bold.ttf',
}
_font_cache = {}

INTER_ASC = 0.96875   # Inter hhea ascender (browser baseline = line box top + asc * size)
MONO_ASC = 1.02       # JetBrains Mono ascender
ASC = {FONT: 0.905, MONO: 0.833}  # Arial / Courier New ascender used to place PPTX text
K_CAL = 1.0           # global calibration factor for baseline placement

# palette
DARK = '0F172A'; TEXT = '475569'; BLUE = '1E40AF'; ACCENT = '0EA5E9'
BG = 'F8FAFC'; BORDER = 'E2E8F0'; CODE_BG = 'EFF6FF'; CODE_FG = '1E40AF'


def px(v):
    return Emu(int(round(v * 9525)))


def pt(px_size):
    return Pt(px_size * 0.75)


def measure(text, size, bold=False, italic=False, font=FONT, spc_em=0.0, caps=False):
    key = (font, bold, italic, round(size * 4))
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(str(LIB / _font_files[(font, bold, italic)]), size=round(size * 4))
    f = _font_cache[key]
    t = text.upper() if caps else text
    return f.getlength(t) / 4 + spc_em * size * len(t)


def _strip_style(shape):
    st = shape._element.find(qn('p:style'))
    if st is not None:
        shape._element.remove(st)


def rect(slide, x, y, w, h, fill, line=None, line_w=1.0, radius=0.0):
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    s = slide.shapes.add_shape(kind, px(x), px(y), px(w), px(h))
    _strip_style(s)
    if radius:
        s.adjustments[0] = min(0.5, radius / min(w, h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = RGBColor.from_string(fill)
    if line:
        s.line.color.rgb = RGBColor.from_string(line)
        s.line.width = px(line_w)
    else:
        s.line.fill.background()
    return s


def card(slide, x, y, w, h, top, fill=BG, border=BORDER, radius=10, top_w=4):
    """Rounded card with a coloured top border (CSS border-top on a rounded box)."""
    rect(slide, x, y, w, h, top, radius=radius)
    rect(slide, x, y + top_w, w, h - top_w, fill, line=border, line_w=1, radius=radius)


def _set_run(run, r):
    f = run.font
    f.name = r.get('font', FONT)
    f.size = pt(r['size'])
    f.bold = r.get('bold', False)
    f.italic = r.get('italic', False)
    f.color.rgb = RGBColor.from_string(r.get('color', TEXT))
    rPr = run._r.get_or_add_rPr()
    if r.get('caps'):
        rPr.set('cap', 'all')
    if r.get('spc_em'):
        rPr.set('spc', str(int(round(r['spc_em'] * r['size'] * 0.75 * 100))))
    # make sure every script uses the standard font
    for tag in ('a:ea', 'a:cs'):
        el = rPr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rPr, qn(tag))
        el.set('typeface', r.get('font', FONT))


def textbox(slide, x, top, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(px(x), px(top), px(w), px(h))
    tf = tb.text_frame
    tf.word_wrap = False
    tf.auto_size = None
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = 1.0
    for r in runs:
        run = p.add_run()
        run.text = r['t']
        _set_run(run, r)
    return tb


def run_width(r):
    w = measure(r['t'], r['size'], r.get('bold', False), r.get('italic', False),
                r.get('font', FONT), r.get('spc_em', 0.0), r.get('caps', False))
    return w + r.get('pad_l', 0) + r.get('pad_r', 0)


def code(t, size, pad_l=True, pad_r=True):
    """Inline <code> run: Courier New, blue, chip with 0.36em horizontal padding."""
    return dict(t=t, size=size, font=MONO, bold=True, color=CODE_FG, code=True,
                pad_l=0.36 * size if pad_l else 0, pad_r=0.36 * size if pad_r else 0)


def line(slide, x, baseline, runs, align='l', slack=40):
    """Place one line of text whose browser baseline is `baseline`.

    align: 'l' -> x is the left edge, 'c' -> x is the centre, 'r' -> x is the right edge.
    Runs flagged code=True get their own text box on top of a rounded chip; the
    other runs are grouped in as few text boxes as possible.
    """
    widths = [run_width(r) for r in runs]
    total = sum(widths)
    start = {'l': x, 'c': x - total / 2, 'r': x - total}[align]
    # group consecutive non-code runs
    groups, cur, cx = [], [], start
    gx = start
    for r, w in zip(runs, widths):
        if r.get('code'):
            if cur:
                groups.append((gx, cur))
                cur = []
            groups.append((cx, [r]))
            gx = cx + w
        else:
            if not cur:
                gx = cx
            cur.append(r)
        cx += w
    if cur:
        groups.append((gx, cur))

    for gx, rs in groups:
        size = max(r['size'] for r in rs)
        font = rs[0].get('font', FONT)
        top = baseline - ASC[font] * size * K_CAL
        h = size * 1.3
        if rs[0].get('code'):
            r = rs[0]
            fc = r['size']
            w = run_width(r)
            rect(slide, gx, baseline - (MONO_ASC + 0.1) * fc, w, 1.52 * fc, CODE_BG, radius=4)
            textbox(slide, gx + r.get('pad_l', 0), top, w + slack, h, rs)
        else:
            gw = sum(run_width(r) for r in rs)
            if align == 'c' and len(groups) == 1:
                textbox(slide, x - (gw + slack) / 2, top, gw + slack, h, rs, align=PP_ALIGN.CENTER)
            elif align == 'r' and len(groups) == 1:
                textbox(slide, x - gw - slack, top, gw + slack, h, rs, align=PP_ALIGN.RIGHT)
            else:
                textbox(slide, gx, top, gw + slack, h, rs)


def bl(rect_y, size):
    """Browser baseline from the measured line-box top of Inter text."""
    return rect_y + INTER_ASC * size


def bl_mono(rect_y, size):
    return rect_y + MONO_ASC * size


def symbol(slide, cx, cy, t, size, color, bold=True):
    """Centered glyph (arrows) – independent from fallback-font metrics."""
    textbox(slide, cx - 30, cy - size, 60, 2 * size,
            [dict(t=t, size=size, bold=bold, color=color)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def svg_png(name, svg, size_px, scale=8):
    out = ASSETS / f'{name}.png'
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(out),
                     output_width=int(size_px * scale), output_height=int(size_px * scale))
    return out


def icon(slide, name, inner, color, x, y, size):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
           f'stroke="#{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{inner}</svg>')
    slide.shapes.add_picture(str(svg_png(name, svg, size)), px(x), px(y), px(size), px(size))


def accent_bar(slide, x=18, y=6):
    rect(slide, x, y, 55, 8, BLUE)
    rect(slide, x + 55, y, 55, 8, ACCENT)


def h2(slide, text):
    line(slide, 18, bl(25.9, 34.0625), [dict(t=text, size=34.0625, bold=True, color=DARK, spc_em=-0.02)])


def _add_shadow(sp_pr, blur, dist, color, alpha):
    eff = etree.SubElement(sp_pr, qn('a:effectLst'))
    sh = etree.SubElement(eff, qn('a:outerShdw'), blurRad=str(px(blur)), dist=str(px(dist)),
                          dir='5400000', algn='t', rotWithShape='0')
    c = etree.SubElement(sh, qn('a:srgbClr'), val=color)
    etree.SubElement(c, qn('a:alpha'), val=str(int(alpha * 100000)))


def standard_theme_fonts(prs):
    theme = prs.slide_master.part.part_related_by(RT.THEME)
    xml = theme.blob.decode('utf-8')
    for f in ('Calibri Light', 'Calibri'):
        xml = xml.replace(f'typeface="{f}"', f'typeface="{FONT}"')
    theme._blob = xml.encode('utf-8')


# ---------------------------------------------------------------------------
# Slides
# ---------------------------------------------------------------------------
def slide_cover(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.shapes.add_picture(str(TESI / 'logo_tor_vergata.png'), px(18), px(94.5), px(284), px(64.6))
    uni = dict(size=18.875, bold=True, color=TEXT, caps=True, spc_em=0.05)
    line(s, 320, bl(102.6, 18.875), [dict(t='Università degli Studi di Roma "Tor Vergata"', **uni)])
    line(s, 320, bl(128.0, 18.875), [dict(t='Corso di Laurea in Informatica Triennale', **uni)])
    accent_bar(s, 18, 193)
    line(s, 18, bl(212.7, 52.875), [dict(t='BlueAgent', size=52.875, bold=True, color=DARK, spc_em=-0.02)])
    line(s, 18, bl(291.5, 29.4375), [dict(t='Orchestratore di container per Cyber Range orientati a CTF di Difesa',
                                         size=29.4375, color='334155')])
    rect(s, 18, 388.3, 1244, 2, BORDER)

    # avatar (img 74px + 2px border, circular, soft blue shadow)
    png = ASSETS / 'davide_avatar.png'
    cairosvg.svg2png(url=str(HTML_DIR / 'figures' / 'davide_avatar.svg'), write_to=str(png),
                     output_width=480, output_height=480)
    pic = s.shapes.add_picture(str(png), px(19), px(417.9), px(76), px(76))
    pic._element.spPr.find(qn('a:prstGeom')).set('prst', 'ellipse')
    pic.line.color.rgb = RGBColor.from_string('BFDBFE')
    pic.line.width = px(2)
    _add_shadow(pic._element.spPr, 12, 4, '2563EB', 0.20)

    fs = 20.25
    lab = dict(size=fs, bold=True, color=DARK)
    val = dict(size=fs, color=TEXT)
    line(s, 112, bl(434.4, fs), [dict(t='Candidato:', **lab), dict(t=' Davide Luci', **val)])
    line(s, 112, bl(463.2, fs), [dict(t='Matricola:', **lab), dict(t=' 0341922', **val)])
    r1 = [dict(t='Relatore:', **lab), dict(t=' Prof. Pierpaolo Loreti', **val)]
    r2 = [dict(t='Correlatore:', **lab), dict(t=' Ing. Francesco Mancini', **val)]
    left = 1262 - max(sum(run_width(r) for r in r1), sum(run_width(r) for r in r2))
    line(s, left, bl(434.4, fs), r1)
    line(s, left, bl(463.2, fs), r2)


def flow_step(s, x, y, w, h, fill, border, title, title_y, body):
    rect(s, x, y, w, h, fill, line=border, line_w=1.5, radius=8)
    cx = x + w / 2
    line(s, cx, bl(title_y, 18.6563), [dict(t=title, size=18.6563, bold=True, color=DARK)], align='c')
    for kind, ty, runs in body:
        line(s, cx, (bl_mono if kind == 'mono' else bl)(ty, runs[0]['size']), runs, align='c')


def slide_problem(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    accent_bar(s)
    h2(s, 'Il Problema: CTF Classiche vs CTF Difensive')
    fs_p, fs_s, fs_c, fs_box = 20.25, 17.9375, 15.25, 19.3125
    lab = dict(bold=True, color=DARK)

    for ox, top, icon_name, icon_svg, icon_col, title, obj in (
        (0, BLUE, 'ic_terminal', '<polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/>', BLUE,
         'CTF Classica (Offensiva / Jeopardy)',
         [' Sfruttare una vulnerabilità per leggere un', 'segreto.']),
        (634.8, ACCENT, 'ic_shield', '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>', ACCENT,
         'CTF Difensiva (Patching & Hardening)',
         [' Correggere la vulnerabilità mantenendo attivo il', 'servizio.']),
    ):
        card(s, 18 + ox, 82.2, 609.2, 386.1, top)
        icon(s, icon_name, icon_svg, icon_col, 45.4 + ox, 112.8, 24)
        line(s, 77.4 + ox, bl(108.8, 23.4688), [dict(t=title, size=23.4688, bold=True, color=BLUE)])
        line(s, 45.4 + ox, bl(168.6, fs_p), [dict(t='Obiettivo:', size=fs_p, **lab), dict(t=obj[0], size=fs_p)])
        line(s, 45.4 + ox, bl(197.4, fs_p), [dict(t=obj[1], size=fs_p)])

    # left pipeline
    flow_step(s, 45.4, 256.7, 159.9, 71.3, 'FFFFFF', 'CBD5E1', '1. Attacco', 268.1,
              [('t', 294.9, [dict(t='Exploit remoto', size=fs_s)])])
    symbol(s, 213.4 + 10.6, 292.3, '➔', 25.3125, '64748B')
    flow_step(s, 242.6, 245.0, 160.0, 94.6, 'EFF6FF', '3B82F6', '2. Lettura', 256.5,
              [('mono', 284.3, [code('/root/', fs_c, pad_r=False)]),
               ('mono', 307.6, [code('flag.txt', fs_c, pad_l=False)])])
    symbol(s, 410.6 + 10.6, 292.3, '➔', 25.3125, '64748B')
    flow_step(s, 439.8, 256.7, 159.9, 71.3, 'F0FDF4', '16A34A', '3. Verifica', 268.1,
              [('t', 294.9, [dict(t='Match stringa', size=fs_s)])])

    # right pipeline
    flow_step(s, 680.2, 245.0, 159.9, 94.6, 'FFFBEB', 'F59E0B', '1. Accesso', 256.5,
              [('t', 283.3, [dict(t='Giocatore è', size=fs_s)]),
               ('mono', 307.6, [code('root', fs_c)])])
    symbol(s, 848.2 + 10.6, 292.3, '➔', 25.3125, '64748B')
    flow_step(s, 877.4, 256.7, 160.0, 71.3, 'FFFFFF', 'CBD5E1', '2. Difesa', 268.1,
              [('t', 294.9, [dict(t='Patch', size=fs_s)])])
    symbol(s, 1045.4 + 10.6, 292.3, '➔', 25.3125, '64748B')
    flow_step(s, 1074.6, 256.7, 159.9, 71.3, 'FEF2F2', 'EF4444', '3. Verifica?', 268.1,
              [('t', 294.9, [dict(t='Oracolo esterno', size=fs_s)])])

    # bottom callouts
    card(s, 45.4, 352.3, 554.3, 92.0, '16A34A', fill='F0FDF4', border='BBF7D0')
    g = dict(size=fs_box, color='14532D')
    line(s, 68.3, bl(374.1, fs_box), [dict(t='Verifica Banale:', size=fs_box, **lab), dict(t=' il giocatore ', **g),
                                      dict(t='non ha accesso', italic=True, **g)])
    line(s, 68.3, bl(401.5, fs_box), [dict(t='privilegiato', italic=True, **g),
                                      dict(t='. Basta confrontare la stringa ', **g),
                                      code('flag{...}', 0.85 * fs_box)])
    card(s, 680.2, 352.3, 554.3, 92.0, 'EF4444', fill='FEF2F2', border='FECACA')
    r = dict(size=fs_box, color='7F1D1D')
    line(s, 703.1, bl(374.1, fs_box), [dict(t='Perché è complesso:', size=fs_box, **lab),
                                       dict(t=' il giocatore leggerebbe qualsiasi', **r)])
    line(s, 703.1, bl(401.5, fs_box), [dict(t="flag nel fs. Può intercettare i test dell'oracolo e barare.", **r)])


def slide_goals(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    accent_bar(s)
    h2(s, 'La Nostra Proposta: Obiettivi di BlueAgent')
    fs_p, fs_chk = 19.3125, 17.9375
    b = dict(size=fs_p, bold=True, color=DARK)
    t = dict(size=fs_p, color=TEXT)
    NB = '\u00a0'
    cols = [
        dict(x=18, top=BLUE, ibg='DBEAFE', ic='1E40AF', chk='1E40AF', name='ic_server',
             svg='<rect x="2" y="2" width="20" height="8" rx="2"/><rect x="2" y="14" width="20" height="8" rx="2"/>'
                 '<line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/>',
             title='1. System Container',
             p=[[dict(t='Ambienti completi e realistici gestiti', **t)],
                [dict(t='da' + NB, **t), dict(t='Incus', **b), dict(t=NB + 'offrendo' + NB, **t),
                 code('systemd', 0.85 * fs_p)]],
             checks=[[dict(t='Persistenza delle patch')], [dict(t='Basso uso RAM')]]),
        dict(x=439.6, top=ACCENT, ibg='E0F2FE', ic='0284C7', chk='0284C7', name='ic_share',
             svg='<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/>'
                 '<line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>',
             title='2. Topologie Multi-Nodo',
             p=[[dict(t='Rete dedicata per ogni team', **t)],
                [dict(t='ccessibile da' + NB, **t), dict(t='WireGuard', **b), dict(t='.', **t)]],
             checks=[[dict(t='Nodi multipli')],
                     [dict(t='Isolamento '), code('nftables', 0.85 * fs_chk), dict(t=' tra team')]]),
        dict(x=861.2, top=BLUE, ibg='DCFCE7', ic='15803D', chk='15803D', name='ic_eyeoff',
             svg='<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>'
                 '<line x1="3" y1="3" x2="21" y2="21"/>',
             title='3. Verifica Invisibile',
             p=[[dict(t='Oracolo' + NB + ' su ', **t), dict(t='cloni', **b), dict(t=NB + 'in una rete SDN', **t)],
                [dict(t='OVN', **b), dict(t=' isolata.', **t)]],
             checks=[[dict(t='No leak (tcpdump)')], [dict(t='Nessun impatto sulla produzione')]]),
    ]
    for c in cols:
        x0 = c['x']
        ix = x0 + 27.4
        card(s, x0, 82.2, 400.8, 292.6, c['top'])
        rect(s, ix, 109.2, 46, 46, c['ibg'], radius=10)
        icon(s, c['name'], c['svg'], c['ic'], ix + 10, 119.2, 26)
        line(s, ix, bl(170.9, 23.4688), [dict(t=c['title'], size=23.4688, bold=True, color=BLUE)])
        line(s, ix, bl(230.6, fs_p), c['p'][0])
        line(s, ix, bl(258.0, fs_p), c['p'][1])
        rect(s, ix, 292.4, 345.9, 1, BORDER)
        for y, runs in zip((305.3, 328.6), c['checks']):
            base = bl(y, fs_chk)
            line(s, ix, base, [dict(t='✓', size=fs_chk, bold=True, color=c['chk'])])
            runs = [r if r.get('code') else dict(r, size=fs_chk, bold=True, color=c['chk']) for r in runs]
            line(s, ix + 1.15 * fs_chk, base, runs)


def slide_results(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    accent_bar(s)
    h2(s, 'Validazione: Sintesi dei Risultati')
    W, H, GX, GY = 609.2, 303.9, 25.6, 16
    fs = 17.25
    lab = dict(size=fs, bold=True, color=DARK)
    txt = dict(size=fs, color=TEXT)
    items = [
        ('summary_graph2_microphase.png', BLUE, 'Sotto-fasi:', " il deploy è dominato dall'estrazione dell'immagine."),
        ('summary_graph3_memory.png', ACCENT, 'Memoria:', ' la RAM cresce linearmente, ~5.2 GB con 100 container.'),
        ('summary_graph4_timeline.png', ACCENT, 'Timeline:', ' picco di RAM in verifica, rilascio completo al teardown.'),
        ('summary_graph5_cpu_iowait.png', BLUE, 'CPU vs I/O:', " il collo di bottiglia è l'I/O wait, non la CPU."),
    ]
    for i, (img, top, l, d) in enumerate(items):
        x = 18 + (i % 2) * (W + GX)
        y = 82.2 + (i // 2) * (H + GY)
        card(s, x, y, W, H, top)
        ix, iy, iw = x + 14, y + 16, W - 28
        ih = H - 16 - 12 - 24 - 8
        rect(s, ix, iy, iw, ih, 'FFFFFF', line='CBD5E1', line_w=1, radius=8)
        from PIL import Image
        with Image.open(FIG / img) as im:
            ar = im.width / im.height
        bw, bh = iw - 12, ih - 12
        pw, ph = (bw, bw / ar) if bw / ar <= bh else (bh * ar, bh)
        s.shapes.add_picture(str(FIG / img), px(ix + (iw - pw) / 2), px(iy + (ih - ph) / 2), px(pw), px(ph))
        runs = [dict(t=l, **lab), dict(t=d, **txt)]
        assert sum(run_width(r) for r in runs) <= iw, (l, sum(run_width(r) for r in runs))
        line(s, ix, y + H - 12 - 24 + 0.8 * fs, runs)


def slide_class_diagram(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    accent_bar(s)
    h2(s, 'Architettura del Sistema: Diagramma delle Classi')
    W, H = 1244.0, 615.0
    x, y = 18.0, 82.2
    card(s, x, y, W, H, BLUE)
    ix, iy, iw, ih = x + 14, y + 16, W - 28, H - 32
    rect(s, ix, iy, iw, ih, 'FFFFFF', line='CBD5E1', line_w=1, radius=8)
    from PIL import Image
    img_path = FIG / 'classdiagr.png'
    with Image.open(img_path) as im:
        ar = im.width / im.height
    bw, bh = iw - 16, ih - 16
    pw, ph = (bw, bw / ar) if bw / ar <= bh else (bh * ar, bh)
    s.shapes.add_picture(str(img_path), px(ix + (iw - pw) / 2), px(iy + (ih - ph) / 2), px(pw), px(ph))


def slide_sequence_diagram(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    accent_bar(s)
    h2(s, 'Processo di Verifica: Diagramma di Sequenza (UC-03)')
    W, H = 1244.0, 615.0
    x, y = 18.0, 82.2
    card(s, x, y, W, H, BLUE)
    ix, iy, iw, ih = x + 14, y + 16, W - 28, H - 32
    rect(s, ix, iy, iw, ih, 'FFFFFF', line='CBD5E1', line_w=1, radius=8)
    from PIL import Image
    img_path = FIG / 'seqdiagram.png'
    with Image.open(img_path) as im:
        ar = im.width / im.height
    bw, bh = iw - 16, ih - 16
    pw, ph = (bw, bw / ar) if bw / ar <= bh else (bh * ar, bh)
    s.shapes.add_picture(str(img_path), px(ix + (iw - pw) / 2), px(iy + (ih - ph) / 2), px(pw), px(ph))


def slide_conclusions(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    accent_bar(s)
    h2(s, 'Conclusioni e Spazio alle Domande')

    # Left profile card
    card(s, 18.0, 82.2, 475.2, 397.9, BLUE)
    png = ASSETS / 'davide_avatar.png'
    if not png.exists():
        cairosvg.svg2png(url=str(HTML_DIR / 'figures' / 'davide_avatar.svg'), write_to=str(png),
                         output_width=480, output_height=480)
    pic = s.shapes.add_picture(str(png), px(188.6), px(161.1), px(134.0), px(134.0))
    pic._element.spPr.find(qn('a:prstGeom')).set('prst', 'ellipse')
    pic.line.color.rgb = RGBColor.from_string('BFDBFE')
    pic.line.width = px(3)
    _add_shadow(pic._element.spPr, 24, 8, '2563EB', 0.22)

    cx = 18.0 + 475.2 / 2
    line(s, cx, bl(315.6, 28.75), [dict(t='Davide Luci', size=28.75, bold=True, color=BLUE)], align='c')
    line(s, cx, bl(356.5, 20.25), [dict(t='Matricola: 0341922', size=20.25, bold=True, color=BLUE)], align='c')
    line(s, cx, bl(391.9, 18.4063), [dict(t='Informatica Triennale — Tor Vergata', size=18.4063, color='64748B')], align='c')

    # Top-right card: Obiettivi Raggiunti
    card(s, 518.8, 82.2, 743.2, 260.1, ACCENT)
    line(s, 546.2, bl(105.4, 23.4688), [dict(t='Obiettivi Raggiunti', size=23.4688, bold=True, color=BLUE)])

    fs_li = 18.875
    b_li = dict(size=fs_li, bold=True, color=DARK)
    t_li = dict(size=fs_li, color=TEXT)
    bullets = [
        (143.5, 169.5,
         [dict(t='System Container Leggeri:', **b_li), dict(t=' persistenza delle patch e ', **t_li),
          code('systemd', 16.0313), dict(t=' nativo con', **t_li)],
         [dict(t='~52 MB RAM/nodo.', **t_li)]),
        (203.8, 229.8,
         [dict(t='Verifica Fuori Banda Invisibile:', **b_li), dict(t=' cloni ', **t_li),
          dict(t='ZFS CoW', **b_li), dict(t=' (speedup ', **t_li), dict(t='3.6×', **b_li),
          dict(t=') isolati in', **t_li)],
         [dict(t='SDN ', **t_li), dict(t='OVN & OpenFlow', **b_li), dict(t='.', **t_li)]),
        (264.0, 290.1,
         [dict(t='Integrazione Chiavi in Mano:', **b_li),
          dict(t=' plugin CTFd + API asincrona FastAPI', **t_li)],
         [dict(t='configurabile via YAML.', **t_li)]),
    ]
    for y1, y2, r1, r2 in bullets:
        line(s, 550.5, bl(y1, fs_li), [dict(t='•', size=fs_li, bold=True, color=TEXT)])
        line(s, 567.9, bl(y1, fs_li), r1)
        line(s, 567.9, bl(y2, fs_li), r2)

    # Bottom-right card: Sviluppi Futuri
    card(s, 518.8, 354.3, 743.2, 125.8, BLUE)
    line(s, 546.2, bl(375.1, 23.4688), [dict(t='Sviluppi Futuri', size=23.4688, bold=True, color=BLUE)])

    fs_p = 18.4063
    b_p = dict(size=fs_p, bold=True, color=DARK)
    t_p = dict(size=fs_p, color=TEXT)
    line(s, 546.2, bl(411.7, fs_p), [
        dict(t='CLI ', **b_p), code('bluecmd', 15.6406),
        dict(t=' standalone per debug locale • ', **t_p),
        dict(t='Polling SLA periodico', **b_p), dict(t=' automatico', **t_p),
    ])
    line(s, 546.2, bl(437.8, fs_p), [
        dict(t='• ', **t_p), dict(t='Topologie YAML multi-subnet', **b_p),
        dict(t=' con router intermedi.', **t_p),
    ])


def main():
    # Render diagrams directly from .excalidraw files into figures
    import shutil
    import subprocess
    import sys
    sys_path = Path(__file__).resolve().parent.parent
    if str(sys_path) not in sys.path:
        sys.path.insert(0, str(sys_path))
    from render_excalidraw_to_png import render_excalidraw
    
    render_excalidraw(sys_path / 'classdiagr.excalidraw', FIG / 'classdiagr.png')
    render_excalidraw(sys_path / 'seqdiagram.excalidraw', FIG / 'seqdiagram.png')

    prs = Presentation()
    prs.slide_width, prs.slide_height = px(1280), px(720)
    standard_theme_fonts(prs)
    slide_cover(prs)
    slide_problem(prs)
    slide_goals(prs)
    slide_class_diagram(prs)
    slide_sequence_diagram(prs)
    slide_results(prs)
    slide_conclusions(prs)
    out = HERE / 'presentazione_blueagent.pptx'
    prs.save(out)
    print('[+]', out)

    # Sync to presentazione_blueagent folder
    out_html_dir = HTML_DIR / 'presentazione_blueagent.pptx'
    shutil.copy2(out, out_html_dir)
    print('[+ Sync]', out_html_dir)

    # Convert to PDF via LibreOffice
    subprocess.run(
        ['libreoffice', '--headless', '--convert-to', 'pdf', str(out)],
        cwd=str(HERE), check=True
    )
    pdf_out = HERE / 'presentazione_blueagent.pdf'
    pdf_sync = HTML_DIR / 'presentazione_blueagent.pdf'
    shutil.copy2(pdf_out, pdf_sync)
    print('[+ PDF]', pdf_out)
    print('[+ PDF Sync]', pdf_sync)


if __name__ == '__main__':
    main()
