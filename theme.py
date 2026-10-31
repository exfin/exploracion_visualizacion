"""Paleta y plantillas de Plotly para los modos claro y oscuro.

Los colores de los gráficos no los controla el CSS: se definen aquí y deben
coincidir con las variables --yt-* de assets/style.css.
"""
import copy
import re

import plotly.graph_objects as go
import plotly.io as pio

from data.data_processing import df

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

# Gris neutro para agrupar el resto de categorías ("Otras") y para los canales
# sin categoría; contraste >= 3:1
NEUTRO = {"light": "#8C8C8C", "dark": "#757575"}

# ---------------------------------------------------------------------------
# Colores por categoría: UN mapeo fijo compartido por los tres gráficos.
# Se arma con la lista ordenada de todas las categorías del dataset, así no
# cambia al filtrar. Los colores están en el mismo orden que CATEGORIAS.
# Entertainment, Music y People & Blogs conservan el rojo, azul y aqua del scatter.
# Verificado: contraste >= 3:1 con la tarjeta en cada modo; todos los pares
# se distinguen con visión normal (ΔE OKLab >= 10 en claro, >= 9.6 en oscuro) y
# las categorías vecinas (orden alfabético y orden del boxplot) también con
# daltonismo protan/deutan (ΔE >= 11). Con 18 colores no todos los pares son
# distinguibles para daltónicos: los nombres siguen en ejes, leyenda y tooltips.
# ---------------------------------------------------------------------------
CATEGORIAS = sorted(df["category"].dropna().unique())

_COLORES_CATEGORIA = {
    # Modo claro, en el orden de CATEGORIAS
    "light": ["#BF4306",  # Autos & Vehicles
              "#B142AB",  # Comedy
              "#DF66C9",  # Education
              "#FF0000",  # Entertainment
              "#8A1586",  # Film & Animation
              "#0A7520",  # Gaming
              "#8287D1",  # Howto & Style
              "#8A5100",  # Movies
              "#2A78D6",  # Music
              "#C08843",  # News & Politics
              "#249EBD",  # Nonprofits & Activism
              "#01A773",  # People & Blogs
              "#4A4C90",  # Pets & Animals
              "#9661E2",  # Science & Technology
              "#A95A7B",  # Shows
              "#7B850D",  # Sports
              "#9D1135",  # Trailers
              "#DC655F"],  # Travel & Events
    # Modo oscuro: mismo tono por categoría, con luminosidad ajustada al fondo oscuro
    "dark": ["#DB5D2C", "#D362CC", "#B0389C", "#FF0000", "#FC88F4", "#78D47C",
             "#6669B0", "#EBAC6C", "#3987E5", "#9A6418", "#63D1F2", "#199E70",
             "#A0A6F3", "#9D67E9", "#CA7899", "#939E33", "#C03A51", "#FF847D"],
}

SIN_CATEGORIA = "Sin categoría"
OTRAS = "Otras"

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
        # Título justo encima del área del gráfico, debajo de la barra de herramientas
        # (en móvil la barra siempre está visible y tapaba el título)
        title=dict(font=dict(size=16, color=p["text"]), x=0, xanchor="left",
                   yref="paper", y=1, yanchor="bottom", pad=dict(b=14)),
        colorway=SECUENCIA[modo],
        margin=dict(l=56, r=24, t=76, b=48),
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
        # Barra de herramientas de Plotly acorde al tema
        modebar=dict(
            bgcolor="rgba(0,0,0,0)",
            color=p["text_secondary"],
            activecolor=p["text"],
        ),
    )
    return template


# Registro de las plantillas con nombre propio
pio.templates["yt_light"] = _crear_template("light")
pio.templates["yt_dark"] = _crear_template("dark")


def get_template(theme: str) -> go.layout.Template:
    """Devuelve la plantilla de Plotly según el tema ('light' o 'dark')."""
    return pio.templates["yt_dark" if theme == "dark" else "yt_light"]


def get_neutro(theme: str) -> str:
    """Devuelve el gris neutro según el tema."""
    return NEUTRO["dark" if theme == "dark" else "light"]


def get_mapa_categorias(theme: str) -> dict:
    """Mapeo categoría -> color del tema, más 'Sin categoría' y 'Otras' en gris.

    Si el dataset llegara a tener más categorías que colores, las que sobran
    usan el gris neutro.
    """
    modo = "dark" if theme == "dark" else "light"
    colores = _COLORES_CATEGORIA[modo]
    mapa = {cat: (colores[i] if i < len(colores) else NEUTRO[modo])
            for i, cat in enumerate(CATEGORIAS)}
    mapa[SIN_CATEGORIA] = NEUTRO[modo]
    mapa[OTRAS] = NEUTRO[modo]
    return mapa


def _luminancia(hex_color: str) -> float:
    """Luminancia relativa WCAG de un color #RRGGBB."""
    canales = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in canales]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def color_texto(fondo: str) -> str:
    """Blanco o negro, el que tenga más contraste sobre el color de fondo."""
    lum = _luminancia(fondo)
    contraste_blanco = 1.05 / (lum + 0.05)
    contraste_negro = (lum + 0.05) / 0.05
    return "#FFFFFF" if contraste_blanco >= contraste_negro else "#000000"


def inicial(nombre) -> str:
    """Inicial del canal para el avatar.

    Primero busca una letra o número latino (A-Z, 0-9, con tildes); si no hay,
    usa el primer carácter alfanumérico de cualquier alfabeto; si tampoco, '?'.
    """
    nombre = str(nombre) if nombre is not None else ""
    latino = re.search(r"[0-9A-Za-zÀ-ÖØ-öø-ÿ]", nombre)
    if latino:
        return latino.group(0).upper()
    otro = next((c for c in nombre if c.isalnum()), None)
    return otro.upper() if otro else "?"


def figura_vacia(theme: str, titulo: str,
                 mensaje: str = "No hay datos para los filtros seleccionados") -> go.Figure:
    """Figura de estado vacío: un mensaje en lugar de un gráfico sin datos."""
    fig = go.Figure()
    fig.update_layout(
        template=get_template(theme),
        title=titulo,
        # Sin ejes ni márgenes automáticos para que el mensaje quede centrado
        xaxis=dict(visible=False, automargin=False),
        yaxis=dict(visible=False, automargin=False),
        margin=dict(l=24, r=24, t=76, b=24),
        annotations=[dict(
            text=mensaje,
            showarrow=False,
            xref="paper", yref="paper", x=0.5, y=0.5,
            font=dict(size=14, color=PALETA["dark" if theme == "dark" else "light"]["text_secondary"]),
        )],
    )
    return fig
