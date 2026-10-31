from dash import html, dcc
import dash_bootstrap_components as dbc
from data.data_processing import df

# opciones filtro pais
paises_options = [{'label': pais, 'value': pais} for pais in sorted(df['Country'].dropna().unique())]

# opciones filtro categoria (los canales sin categoría solo cuentan cuando no se filtra)
categorias_options = [{'label': cat, 'value': cat} for cat in sorted(df['category'].dropna().unique())]

# Textos internos de dcc.Dropdown en español (por defecto vienen en inglés)
ETIQUETAS_DROPDOWN = {
    'select_all': 'Seleccionar todo',
    'deselect_all': 'Quitar todo',
    'selected_count': '{num_selected} seleccionados',
    'search': 'Buscar',
    'clear_search': 'Borrar búsqueda',
    'clear_selection': 'Borrar selección',
    'no_options_found': 'No se encontraron opciones',
}


def tarjeta_kpi(etiqueta, id_valor, icono):
    """Tarjeta de KPI: etiqueta pequeña y número grande (el callback llena el número)."""
    return dbc.Card(
        dbc.CardBody([
            html.P(
                [html.I(className=f"bi {icono}", **{"aria-hidden": "true"}), etiqueta],
                className="kpi-label",
            ),
            html.P(id=id_valor, className="kpi-value"),
        ]),
        className="kpi-card",
    )


def tarjeta_grafico(id_grafico):
    """Tarjeta que contiene un gráfico de Plotly."""
    return dbc.Card(
        dbc.CardBody(dcc.Graph(id=id_grafico, className="chart")),
        className="chart-card",
    )


layout = html.Div([
    # Filtros: ancho completo en móvil.
    # persistence guarda la selección al cambiar de pestaña (y al recargar en la misma pestaña del navegador)
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Label("Seleccionar país", html_for="filtro-pais", className="filter-label"),
                    dcc.Dropdown(
                        id='filtro-pais',
                        options=paises_options,
                        placeholder="Todos los países",
                        clearable=True,
                        labels=ETIQUETAS_DROPDOWN,
                        persistence=True,
                        persistence_type='session',
                    ),
                ],
                xs=12, md=6, lg=4,
            ),
            dbc.Col(
                [
                    dbc.Label("Categorías", html_for="filtro-categoria", className="filter-label"),
                    dcc.Dropdown(
                        id='filtro-categoria',
                        options=categorias_options,
                        multi=True,
                        placeholder="Todas las categorías",
                        clearable=True,
                        labels=ETIQUETAS_DROPDOWN,
                        persistence=True,
                        persistence_type='session',
                    ),
                ],
                xs=12, md=6, lg=4,
            ),
        ],
        className="filters-row g-3",
    ),

    # KPIs
    dbc.Row(
        [
            dbc.Col(tarjeta_kpi("Canales", 'kpi-total-canales', "bi-collection-play"), xs=12, sm=6, lg=4, xxl=3),
            dbc.Col(tarjeta_kpi("Vistas totales", 'kpi-total-vistas', "bi-eye"), xs=12, sm=6, lg=4, xxl=3),
        ],
        className="kpi-row g-3",
    ),

    # Gráficos: apilados en móvil, dos columnas en pantallas grandes
    dbc.Row(
        [
            dbc.Col(tarjeta_grafico('grafico-top-subscribers'), xs=12, lg=6),
            dbc.Col(tarjeta_grafico('grafico-categoria-ingresos'), xs=12, lg=6),
        ],
        className="charts-row g-3",
    ),
])
