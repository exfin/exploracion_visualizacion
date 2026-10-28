from dash import html, dcc
import plotly.express as px
from data.data_processing import df

# opciones filtro pais
paises_options = [{'label': pais, 'value': pais} for pais in sorted(df['Country'].dropna().unique())]

layout = html.Div([
    html.H1("Dashboard Global de YouTube", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Seleccionar País:"),
        dcc.Dropdown(
            id='filtro-pais',
            options=paises_options,
            placeholder="Todos los países",
            clearable=True
        ),
    ], style={'width': '40%', 'padding': '10px'}),

    html.Div([
        html.Div(id='kpi-total-canales', style={'padding': '15px', 'border': '1px solid #ddd', 'borderRadius': '5px'}),
        html.Div(id='kpi-total-vistas', style={'padding': '15px', 'border': '1px solid #ddd', 'borderRadius': '5px'}),
    ], style={'display': 'flex', 'gap': '20px', 'padding': '10px'}),

    html.Div([
        dcc.Graph(id='grafico-top-subscribers'),
        dcc.Graph(id='grafico-categoria-ingresos')
    ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '10px'})
])