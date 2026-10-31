from dash import Dash, html, dcc, Output, Input, State, ClientsideFunction, clientside_callback
import dash_bootstrap_components as dbc
import theme  # registra las plantillas yt_light / yt_dark de Plotly
import callbacks.filtros

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
    html.H1("Dashboard Analítico de YouTube"),
    dcc.Tabs(id="tabs-navegacion", value='tab-home', children=[
        dcc.Tab(label='Vista General', value='tab-home'),
        dcc.Tab(label='Análisis Avanzado', value='tab-detail'),
    ]),
    html.Div(id='contenido-tab')
])

@app.callback(
    Output('contenido-tab', 'children'),
    Input('tabs-navegacion', 'value')
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