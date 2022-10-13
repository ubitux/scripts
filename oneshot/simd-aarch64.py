import colorsys
from math import ceil
from textwrap import dedent, indent
from dataclasses import dataclass


@dataclass
class Transform:
    title: str
    in0: str
    in1: str
    out: str


transforms = [
    Transform("trn1", "ABCD", "EFGH", "AECG"),
    Transform("trn2", "ABCD", "EFGH", "BFDH"),
    Transform("uzp1", "ABCD", "EFGH", "ACEG"),
    Transform("uzp2", "ABCD", "EFGH", "BDFH"),
    Transform("zip1", "ABCD", "EFGH", "AEBF"),
    Transform("zip2", "ABCD", "EFGH", "CGDH"),
    Transform("ext #0", "ABCD", "EFGH", "ABCD"),
    Transform("ext #4", "ABCD", "EFGH", "BCDE"),
    Transform("ext #8", "ABCD", "EFGH", "CDEF"),
    Transform("ext #12", "ABCD", "EFGH", "DEFG"),
]


def _get_palette(n: int = 8):
    ret = []
    for i in range(n):
        clr = colorsys.hls_to_rgb(i / n, 0.4, 0.4)
        hexclr = "#" + "".join("%02X" % int(c * 255) for c in clr)
        ret.append(hexclr)
    return ret


pad = 50
hspace = 20
vspace = 50
palette = dict(zip("ABCDEFGH", _get_palette()))
cell_w = 30
cell_h = 26
stroke_width = 2
font_size = min(cell_w, cell_h) // 2
reg_w = cell_w * 4
reg_h = cell_h
disabled_color = "#555"
fg_color = "white"

trf_title_h = 30
trf_title_bot_pad = 10
trf_w = reg_w * 2 + pad * 2 + hspace
trf_h = trf_title_h + trf_title_bot_pad + reg_h * 2 + pad * 2 + vspace

nb_cols = 2
nb_rows = ceil(len(transforms) / nb_cols)
svg_w = nb_cols * trf_w
svg_h = nb_rows * trf_h


def pad_str(level):
    return " " * 2 * level


def indent1p(s, level):
    p = pad_str(level)
    return indent(s, p).removeprefix(p)


def _get_register_svg(content: str, enabled: str) -> str:
    cells = []
    for i, c in enumerate(content):
        color = palette[c] if c in enabled else disabled_color
        w, h = cell_w, cell_h
        x, y = cell_w * i, 0
        cells.append(
            dedent(
                f"""\
                <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" stroke="{fg_color}" stroke-width="{stroke_width}" />
                <text x="{x+w//2}" y="{y+h//2}" fill="{fg_color}" font-size="{font_size}" dominant-baseline="middle" text-anchor="middle">{c}</text>"""
            )
        )
    return "\n".join(cells)


def _get_links_svg(trf: Transform) -> str:
    links = []

    for out_index, c in enumerate(trf.out):
        if c in trf.in0:
            ivec = trf.in0
            offset = 0
        else:
            ivec = trf.in1
            offset = reg_w + hspace

        in_index = ivec.index(c)
        x1 = offset + in_index * cell_w + cell_w // 2
        y1 = cell_h
        x2 = (reg_w + hspace) // 2 + out_index * cell_w + cell_w // 2
        y2 = reg_h + vspace

        links.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{fg_color}" stroke-width="{stroke_width}" stroke-linecap="round" />'
        )

    return "\n".join(links)


def _get_trf_svg(trf: Transform) -> str:
    in0 = _get_register_svg(trf.in0, trf.out)
    in1 = _get_register_svg(trf.in1, trf.out)
    out = _get_register_svg(trf.out, trf.out)

    links = _get_links_svg(trf)

    svg = dedent(
        f"""\
        <g transform="translate({pad},{pad})">
          <text x="{(trf_w-pad*2)//2}" y="0" fill="{fg_color}" font-size="{font_size*2}" dominant-baseline="middle" text-anchor="middle" w="{trf_w}" h="{trf_title_h}">{trf.title}</text>
          <g transform="translate(0,{trf_title_h+trf_title_bot_pad})">
            LINKS
            <g transform="translate(0,0)">
              IN0
            </g>
            <g transform="translate({reg_w+hspace},0)">
              IN1
            </g>
            <g transform="translate({(reg_w+hspace)//2},{reg_h+vspace})">
              OUT
            </g>
          </g>
        </g>"""
    )

    svg = svg.replace("IN0", indent1p(in0, 3))
    svg = svg.replace("IN1", indent1p(in1, 3))
    svg = svg.replace("OUT", indent1p(out, 3))
    svg = svg.replace("LINKS", indent1p(links, 2))
    return svg


def _get_sheet_svg():
    figs = []
    col, row = 0, 0
    for trf in transforms:
        if col == nb_cols:
            col = 0
            row += 1

        svg = dedent(
            f"""\
            <g transform="translate({col*trf_w},{row*trf_h})">
              TRF
            </g>"""
        )
        svg = svg.replace("TRF", indent1p(_get_trf_svg(trf), 1))
        figs.append(svg)
        col += 1

    content = "\n".join(figs)

    s = dedent(
        f"""\
        <!DOCTYPE html>
        <html>
          <head><title>AArch64 SIMD instructions schematics</title></head>
          <body style="background-color:#333">
            <svg width="{svg_w}" height="{svg_h}" style="background-color:#1c1c1c;font-family:monospace;font-weight:bold">
              CONTENT
            </svg>
          </body>
        </html>"""
    )
    s = s.replace("CONTENT", indent1p(content, 3))

    return s


print(_get_sheet_svg())
