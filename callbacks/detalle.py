from dash import Output, Input, callback
import plotly.express as px
from data.data_processing import df
import theme

TITULO_SCATTER = "Desempleo del país vs. ingresos del YouTuber"

# En un scatter solo 3 colores se distinguen bien entre sí:
# se destacan las 3 categorías con más canales y el resto se agrupa en "Otras".
TOP_CATEGORIAS = df['category'].value_counts().index[:3].tolist()
OTRAS = 'Otras'

# Datos del scatter (las filas sin tasa de desempleo no se pueden ubicar en el eje X)
df_scatter = df.dropna(subset=['Unemployment rate']).copy()
df_scatter['grupo'] = df_scatter['category'].where(
    df_scatter['category'].isin(TOP_CATEGORIAS), OTRAS
)


@callback(
    Output('grafico-scatter-detalle', 'figure'),
    Input('theme-store', 'data'),  # el tema vuelve a dibujar el gráfico
)
def actualizar_scatter(tema):
    secuencia = theme.get_secuencia(tema)
    colores = {cat: secuencia[i] for i, cat in enumerate(TOP_CATEGORIAS)}
    colores[OTRAS] = theme.get_neutro(tema)

    fig = px.scatter(
        df_scatter,
        x='Unemployment rate',
        y='highest_yearly_earnings',
        size='subscribers',
        color='grupo',
        color_discrete_map=colores,
        # "Otras" se dibuja primero para quedar debajo de las categorías destacadas
        category_orders={'grupo': [OTRAS] + TOP_CATEGORIAS},
        hover_name='Youtuber',
        hover_data={'grupo': False, 'category': True, 'Country': True, 'subscribers': ':,'},
        labels={
            'Unemployment rate': 'Tasa de desempleo del país (%)',
            'highest_yearly_earnings': 'Ingresos anuales máximos',
            'grupo': 'Categoría',
            'category': 'Categoría',
            'Country': 'País',
            'subscribers': 'Suscriptores',
        },
        title=TITULO_SCATTER,
        template=theme.get_template(tema),
    )

    # Borde del color de la tarjeta para separar burbujas superpuestas
    borde = theme.PALETA['dark' if tema == 'dark' else 'light']['card']
    fig.update_traces(marker=dict(opacity=0.85, line=dict(width=1, color=borde)))

    # Leyenda: destacadas primero, "Otras" al final; debajo del gráfico (cabe en móvil)
    for traza in fig.data:
        traza.legendrank = 1000 if traza.name == OTRAS else 10 + TOP_CATEGORIAS.index(traza.name)
    fig.update_layout(
        legend=dict(orientation='h', yanchor='top', y=-0.2, x=0, title_text='Categoría'),
        margin=dict(b=96),
        height=560,
    )
    return fig
