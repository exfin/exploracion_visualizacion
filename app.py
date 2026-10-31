from dash import Dash, html, dcc, Output, Input, State, ClientsideFunction, clientside_callback
import dash_bootstrap_components as dbc
import theme  # registra las plantillas yt_light / yt_dark de Plotly
import callbacks.filtros   # filtros, KPIs y gráficos de la vista general
import callbacks.detalle   # gráfico de dispersión de la vista detallada

# Importar vistas
from layouts.home import layout as home_layout
from layouts.detail import layout as detail_layout

# Bootstrap 5 (vía DBC) e íconos de Bootstrap
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
)
server = app.server

app.layout = html.Div([
    # Tema elegido por el usuario (se guarda en el navegador)
    dcc.Store(id="theme-store", storage_type="local"),
    # Botón de tema: el ícono cambia solo con CSS según [data-bs-theme]
    dbc.Button(
        [
            html.I(className="bi bi-moon-stars-fill icon-moon", **{"aria-hidden": "true"}),
            html.I(className="bi bi-sun-fill icon-sun", **{"aria-hidden": "true"}),
            # Nombre accesible del botón (dbc.Button no admite aria-label)
            html.Span("Cambiar tema", id="theme-toggle-texto", className="visually-hidden"),
        ],
        id="theme-toggle",
        className="theme-toggle",
        title="Cambiar tema",
    ),
    dbc.Container(
        [
            # Encabezado: único título de la página, con el ícono rojo de YouTube
            html.Header(
                [
                    html.H1(
                        [
                            html.I(className="bi bi-youtube brand-icon", **{"aria-hidden": "true"}),
                            html.Span("Dashboard Analítico de YouTube"),
                        ],
                        className="app-title",
                    ),
                    html.P(
                        "Estadísticas globales de los principales canales de YouTube",
                        className="app-subtitle",
                    ),
                ],
                className="app-header",
            ),
            # Pestañas de navegación (los valores tab-home / tab-detail se mantienen)
            dbc.Tabs(
                id="tabs-navegacion",
                active_tab="tab-home",
                className="yt-tabs",
                children=[
                    dbc.Tab(label="Vista General", tab_id="tab-home"),
                    dbc.Tab(label="Análisis Avanzado", tab_id="tab-detail"),
                ],
            ),
            # Contenido de la pestaña activa
            html.Main(id="contenido-tab", className="tab-body"),
        ],
        fluid=True,
        className="app-container",
    ),
])

@app.callback(
    Output('contenido-tab', 'children'),
    Input('tabs-navegacion', 'active_tab')
)
def renderizar_pestana(tab):
    if tab == 'tab-home':
        return home_layout
    elif tab == 'tab-detail':
        return detail_layout

# Tema: el clic alterna el valor del Store (funciones en assets/theme.js)
clientside_callback(
    ClientsideFunction(namespace="tema", function_name="alternar"),
    Output("theme-store", "data"),
    Input("theme-toggle", "n_clicks"),
    State("theme-store", "data"),
)

# Tema: el Store aplica data-bs-theme en <html> y actualiza los textos del botón
clientside_callback(
    ClientsideFunction(namespace="tema", function_name="aplicar"),
    Output("theme-toggle-texto", "children"),
    Output("theme-toggle", "title"),
    Input("theme-store", "data"),
)

if __name__ == '__main__':
    app.run(debug=True, port=8050)