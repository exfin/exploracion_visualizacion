from dash import Output, Input, callback
import plotly.express as px
import plotly.graph_objects as go
from data.data_processing import df
import theme

TITULO_TOP = "Top 10 YouTubers por suscriptores"
TITULO_CATEGORIA = "Ingresos anuales máximos por categoría"
# Alto común de los dos gráficos (la leyenda de categorías ocupa lugar abajo)
ALTO = 600


def grafico_top10(dff, tema, plantilla, mapa):
    """Barras del top 10 coloreadas por categoría, con un avatar (inicial) en la punta."""
    top_10 = dff.nlargest(10, 'subscribers').copy()
    top_10['categoria'] = top_10['category'].fillna(theme.SIN_CATEGORIA)

    # Nombres repetidos (p. ej. varios 'Nombre Local') se apilarían en la misma
    # barra: se les agrega su ranking para que cada canal tenga su fila
    repetido = top_10['Youtuber'].duplicated(keep=False)
    top_10['canal'] = top_10['Youtuber'].where(
        ~repetido, top_10['Youtuber'] + ' (#' + top_10['rank'].astype(str) + ')'
    )

    # Leyenda: solo las categorías presentes, en el orden fijo del mapeo
    presentes = [cat for cat in mapa if cat in set(top_10['categoria'])]

    fig = px.bar(
        top_10,
        x='subscribers',
        y='canal',
        color='categoria',
        orientation='h',
        title=TITULO_TOP,
        labels={'subscribers': 'Suscriptores', 'canal': '', 'categoria': 'Categoría'},
        category_orders={'categoria': presentes},
        color_discrete_map=mapa,
        custom_data=['categoria'],
        template=plantilla,
    )
    fig.update_traces(
        hovertemplate='<b>%{y}</b><br>Categoría: %{customdata[0]}'
                      '<br>Suscriptores: %{x:,}<extra></extra>'
    )

    # Avatares: círculo del color de la categoría con la inicial del canal.
    # Sin leyenda ni tooltip propio (el tooltip lo da la barra).
    colores = [mapa[cat] for cat in top_10['categoria']]
    borde = theme.PALETA['dark' if tema == 'dark' else 'light']['card']
    fig.add_trace(go.Scatter(
        x=top_10['subscribers'],
        y=top_10['canal'],
        mode='markers+text',
        text=[theme.inicial(nombre) for nombre in top_10['Youtuber']],
        textposition='middle center',
        textfont=dict(family=theme.FUENTE, size=11, weight='bold',
                      color=[theme.color_texto(c) for c in colores]),
        # 22 px: entra en la altura de cada fila también en celulares
        marker=dict(size=22, color=colores, line=dict(width=2, color=borde)),
        hoverinfo='skip',
        showlegend=False,
        cliponaxis=False,
    ))

    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},  # el mayor arriba
        bargap=0.2,                                   # espacio entre barras
        barmode='overlay',                            # una barra por canal
        # Leyenda debajo del gráfico con el título arriba. Plotly la ajusta al
        # ancho del área de barras: en celular queda en una columna, por eso ALTO
        # deja lugar suficiente para que los avatares no se encimen.
        legend=dict(orientation='h', yanchor='top', y=-0.18, x=0,
                    title=dict(text='Categoría', side='top left'),
                    font=dict(size=12)),
        height=ALTO,
    )
    # 10 % más de eje X para que el avatar de la barra más larga no se corte
    fig.update_xaxes(range=[0, top_10['subscribers'].max() * 1.1])
    # Siempre lugar para 10 filas: con menos resultados las barras mantienen su
    # grosor y quedan arriba. Nombres largos acortados solo en el eje
    # (el tooltip muestra el nombre completo).
    n = len(top_10)
    fig.update_yaxes(
        range=[n - 10.5, n - 0.5],
        tickmode='array',
        tickvals=top_10['canal'].tolist(),
        ticktext=[c if len(c) <= 18 else c[:17] + '…' for c in top_10['canal']],
    )
    return fig


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
                theme.figura_vacia(tema, TITULO_TOP).update_layout(height=ALTO),
                theme.figura_vacia(tema, TITULO_CATEGORIA).update_layout(height=ALTO))

    plantilla = theme.get_template(tema)
    # Mismo color por categoría en todos los gráficos (mapeo fijo de theme.py)
    mapa = theme.get_mapa_categorias(tema)

    # Gráfico top 10 por suscriptores
    fig_top = grafico_top10(dff, tema, plantilla, mapa)

    # Boxplots de ingresos por categoría (ordenadas por mediana, de mayor a menor)
    dfc = dff.dropna(subset=['category'])
    if dfc.empty:
        fig_cat = theme.figura_vacia(tema, TITULO_CATEGORIA, "Estos canales no tienen categoría")
        fig_cat.update_layout(height=ALTO)
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
            color='category',
            color_discrete_map=mapa,
            hover_name='Youtuber',
            template=plantilla,
        )
        # overlay: cada caja ocupa su lugar completo (sin desplazarse por color);
        # sin leyenda porque el eje X ya nombra cada categoría
        fig_cat.update_layout(showlegend=False, xaxis_tickangle=-45, boxmode='overlay', height=ALTO)

    return total_canales, total_vistas, fig_top, fig_cat
