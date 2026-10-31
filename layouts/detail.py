from dash import html, dcc
import dash_bootstrap_components as dbc

# El scatter (desempleo vs. ingresos) se dibuja en callbacks/detalle.py según el tema
layout = html.Div([
    html.H2("Análisis Detallado y Métricas del País", className="section-title"),
    dbc.Card(
        dbc.CardBody(dcc.Graph(id='grafico-scatter-detalle', className="chart")),
        className="chart-card",
    ),
])
