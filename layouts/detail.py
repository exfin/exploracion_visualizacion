from dash import html, dcc
import plotly.express as px
from data.data_processing import df

# scatter entre edesempleo e ingresos
fig_scatter = px.scatter(
    df,
    x='Unemployment rate',
    y='highest_yearly_earnings',
    size='subscribers',
    color='category',
    hover_name='Youtuber',
    title="Relación: Tasa de Desempleo del País vs. Ingresos del YouTuber"
)

layout = html.Div([
    html.H2("Análisis Detallado y Métricas del País"),
    dcc.Graph(figure=fig_scatter)
])