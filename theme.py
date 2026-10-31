"""Paleta y plantillas de Plotly para los modos claro y oscuro.

Los colores de los gráficos no los controla el CSS: se definen aquí y deben
coincidir con las variables --yt-* de assets/style.css.
"""
import copy

import plotly.graph_objects as go
import plotly.io as pio

# Paleta de la interfaz (igual que en assets/style.css)
PALETA = {
    "light": {
        "bg": "#FFFFFF",
        "surface": "#F2F2F2",
        "card": "#FFFFFF",
        "text": "#0F0F0F",
        "text_secondary": "#606060",
        "border": "#E5E5E5",
        "red": "#FF0000",
        "red_text": "#CC0000",
        "link": "#065FD4",
    },
    "dark": {
        "bg": "#0F0F0F",
        "surface": "#272727",
        "card": "#181818",
        "text": "#F1F1F1",
        "text_secondary": "#AAAAAA",
        "border": "#3F3F3F",
        "red": "#FF0000",
        "red_text": "#FF4E45",
        "link": "#3EA6FF",
    },
}

# Secuencias categóricas encabezadas por el rojo de YouTube.
# Orden validado (daltonismo protan/deutan y visión normal) en ambos modos:
# rojo, azul, aqua, naranja, violeta, amarillo, magenta, verde.
# Los 3 primeros también son distinguibles entre sí en gráficos de dispersión.
# Usar en orden fijo; con más de 8 categorías conviene agrupar en "Otras".
SECUENCIA = {
    "light": ["#FF0000", "#2A78D6", "#1BAF7A", "#EB6834",
              "#6250D6", "#EDA100", "#E87BA4", "#008300"],
    "dark": ["#FF0000", "#3987E5", "#199E70", "#D95926",
             "#9085E9", "#C98500", "#D55181", "#008300"],
}

FUENTE = "Roboto, Arial, sans-serif"


def _crear_template(modo: str) -> go.layout.Template:
    """Construye la plantilla de Plotly para 'light' o 'dark'."""
    p = PALETA[modo]
    base = "plotly_white" if modo == "light" else "plotly_dark"
    template = copy.deepcopy(pio.templates[base])

    eje = dict(
        gridcolor=p["border"],
        linecolor=p["border"],
        zerolinecolor=p["border"],
        tickcolor=p["border"],
        tickfont=dict(color=p["text_secondary"]),
        title=dict(font=dict(color=p["text_secondary"])),
        automargin=True,
    )

    template.layout.update(
        paper_bgcolor="rgba(0,0,0,0)",  # transparente: toma el color de la tarjeta
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FUENTE, color=p["text"], size=13),
        title=dict(font=dict(size=16, color=p["text"]), x=0, xanchor="left"),
        colorway=SECUENCIA[modo],
        margin=dict(l=56, r=24, t=56, b=48),
        xaxis=eje,
        yaxis=eje,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=p["text_secondary"]),
            title=dict(font=dict(color=p["text"])),
        ),
        hoverlabel=dict(
            bgcolor=p["card"],
            bordercolor=p["border"],
            font=dict(family=FUENTE, color=p["text"]),
        ),
    )
    return template


# Registro de las plantillas con nombre propio
pio.templates["yt_light"] = _crear_template("light")
pio.templates["yt_dark"] = _crear_template("dark")


def get_template(theme: str) -> go.layout.Template:
    """Devuelve la plantilla de Plotly según el tema ('light' o 'dark')."""
    return pio.templates["yt_dark" if theme == "dark" else "yt_light"]


def get_secuencia(theme: str) -> list:
    """Devuelve la secuencia categórica según el tema."""
    return SECUENCIA["dark" if theme == "dark" else "light"]
