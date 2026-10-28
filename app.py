from dash import Dash, html, dcc, Output, Input
import callbacks.filtros  

# Importar vistas
from layouts.home import layout as home_layout
from layouts.detail import layout as detail_layout

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
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

if __name__ == '__main__':
    app.run(debug=True, port=8050)