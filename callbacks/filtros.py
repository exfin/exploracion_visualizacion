from dash import Output, Input, callback
import plotly.express as px
from data.data_processing import df

@callback(
    [
        Output('kpi-total-canales', 'children'),
        Output('kpi-total-vistas', 'children'),
        Output('grafico-top-subscribers', 'figure'),
        Output('grafico-categoria-ingresos', 'figure')
    ],
    [Input('filtro-pais', 'value')]
)
def actualizar_dashboard(pais_seleccionado):
    # Filtrar datos
    if pais_seleccionado:
        dff = df[df['Country'] == pais_seleccionado]
    else:
        dff = df.copy()

    # Solo el número: la etiqueta ya está en la tarjeta del KPI
    total_canales = f"{len(dff):,}"
    total_vistas = f"{dff['video views'].sum():,.0f}"

    #grafico top 10
    top_10 = dff.nlargest(10, 'subscribers')
    fig_top = px.bar(
        top_10,
        x='subscribers',
        y='Youtuber',
        orientation='h',
        title="Top 10 YouTubers por Suscriptores",
        color='subscribers',
        color_continuous_scale='Viridis'
    )
    fig_top.update_layout(yaxis={'categoryorder': 'total ascending'})

    # boxplots ingresos categoria
    fig_cat = px.box(
        dff,
        x='category',
        y='highest_yearly_earnings',
        title="Ingresos Anuales Máximos por Categoría",
        color='category'
    )
    fig_cat.update_layout(showlegend=False, xaxis_tickangle=-45)

    return total_canales, total_vistas, fig_top, fig_cat