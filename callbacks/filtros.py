from dash import Output, Input, callback
import plotly.express as px
from data.data_processing import df
import theme

TITULO_TOP = "Top 10 YouTubers por suscriptores"
TITULO_CATEGORIA = "Ingresos anuales máximos por categoría"


@callback(
    Output('kpi-total-canales', 'children'),
    Output('kpi-total-vistas', 'children'),
    Output('grafico-top-subscribers', 'figure'),
    Output('grafico-categoria-ingresos', 'figure'),
    Input('filtro-pais', 'value'),
    Input('filtro-categoria', 'value'),
    Input('theme-store', 'data'),  # el tema vuelve a dibujar los gráficos
)
def actualizar_dashboard(pais_seleccionado, categorias, tema):
    # Filtrar datos (filtro vacío = todos)
    dff = df
    if pais_seleccionado:
        dff = dff[dff['Country'] == pais_seleccionado]
    if categorias:
        dff = dff[dff['category'].isin(categorias)]

    # KPIs: solo el número, la etiqueta ya está en la tarjeta
    total_canales = f"{len(dff):,}"
    total_vistas = f"{dff['video views'].sum():,.0f}"

    # Estado vacío: mensaje en lugar de gráficos sin datos
    if dff.empty:
        return (total_canales, total_vistas,
                theme.figura_vacia(tema, TITULO_TOP),
                theme.figura_vacia(tema, TITULO_CATEGORIA))

    plantilla = theme.get_template(tema)
    # Una sola serie por gráfico -> un solo color (rojo YouTube)
    color = theme.get_secuencia(tema)[0]

    # Gráfico top 10 por suscriptores
    top_10 = dff.nlargest(10, 'subscribers')
    fig_top = px.bar(
        top_10,
        x='subscribers',
        y='Youtuber',
        orientation='h',
        title=TITULO_TOP,
        labels={'subscribers': 'Suscriptores', 'Youtuber': ''},
        template=plantilla,
        color_discrete_sequence=[color],
    )
    fig_top.update_traces(hovertemplate='<b>%{y}</b><br>Suscriptores: %{x:,}<extra></extra>')
    # Barras más finas (más espacio entre ellas) y el mayor arriba
    fig_top.update_layout(yaxis={'categoryorder': 'total ascending'}, bargap=0.35)

    # Boxplots de ingresos por categoría (ordenadas por mediana, de mayor a menor)
    dfc = dff.dropna(subset=['category'])
    if dfc.empty:
        fig_cat = theme.figura_vacia(tema, TITULO_CATEGORIA, "Estos canales no tienen categoría")
    else:
        orden = (dfc.groupby('category')['highest_yearly_earnings']
                 .median().sort_values(ascending=False).index.tolist())
        fig_cat = px.box(
            dfc,
            x='category',
            y='highest_yearly_earnings',
            title=TITULO_CATEGORIA,
            labels={'category': 'Categoría', 'highest_yearly_earnings': 'Ingresos anuales máximos'},
            category_orders={'category': orden},
            hover_name='Youtuber',
            template=plantilla,
            color_discrete_sequence=[color],
        )
        fig_cat.update_layout(showlegend=False, xaxis_tickangle=-45)

    return total_canales, total_vistas, fig_top, fig_cat
