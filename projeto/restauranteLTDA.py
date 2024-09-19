from dash import Dash, html, dcc, Output, Input
import pandas as pd
import plotly.express as px

# Inicializar o aplicativo Dash
app = Dash(__name__)

# Leitura do arquivo Excel
df = pd.read_excel("Vendas.xlsx")

# Gera o gráfico inicial
fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")

# Opções para o dropdown
opcoes = list(df['ID Loja'].unique())
opcoes.append("Todas as Lojas")

# Layout do aplicativo com abas
app.layout = html.Div(children=[
    html.H1(children='Faturamento das Lojas'),

    dcc.Tabs([

        dcc.Tab(label='Visão Geral', children=[
            html.H2(children='Gráficos com o faturamento de todas os produtos separado por loja'),
            dcc.Dropdown(opcoes, value='Todas as Lojas', id='lista_lojas'),
            dcc.Graph(id='grafico_quantidade_produto', figure=fig)
        ]),

        dcc.Tab(label='Análise de Faturamento', children=[
            html.H2('Faturamento por Loja'),
            dcc.Graph(id='grafico_faturamento', figure=px.pie(df, names="ID Loja", values="Quantidade",
                                                              title="Percentual de Vendas por Loja"))
        ])

    ])
])

# Callback para atualizar o gráfico de acordo com a loja selecionada
@app.callback(
    Output('grafico_quantidade_produto', 'figure'),
    Input('lista_lojas', 'value')
)
def update_output(value):
    if value == "Todas as Lojas":
        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    else:
        tabela_filtrada = df.loc[df['ID Loja'] == value, :]
        fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")

    return fig

# Rodar o servidor
if __name__ == "__main__":
    app.run(debug=True)
