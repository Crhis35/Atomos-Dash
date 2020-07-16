import dash
import dash_table
import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.figure_factory as ff

plata = pd.read_csv('./datos/Ag.csv', sep=';')
yodo = pd.read_csv('./datos/Yodo.csv', sep=';')

df1 = pd.DataFrame(plata).astype(float)
df2 = pd.DataFrame(yodo).astype(float)
df = pd.concat([df1, df2])

Ag = df1.to_numpy()
I = df2.to_numpy()


def U(r):
    return 8.987e9*(-1.6e-19 * 1.6e-19)/r


def distancia(vec1, vec2):
    return np.sqrt((np.sum(np.square(vec1-vec2)))) * 1e-10


energia = 0
t = 0
for i in range(len(Ag)):
    for j in range(len(Ag)):
        if i != j:
            for k in range(len(I)):
                energia += U(distancia(Ag[i], I[k]))
            t += 1
            energia += U(distancia(Ag[i], Ag[j]))


app = dash.Dash()

app.layout = html.Div([
    html.Div([
        html.H1(
            children="Enegia potencial Electroestatica",
            style={
                'text-align': 'center',
                'color':  '#7FDBFF'
            }
        ),
        html.P(children='Seleccione el numero del elemento'),
        dcc.Dropdown(
            id='opcion',
            options=[{'label': 'Ag-'+str(i+1), 'value': i}
                     for i in range(len(Ag))],
            value=[1],
            multi=True
        ),
        dcc.Graph(id='feature-graphic')
    ], style={
        'width': '48%'
    }),
    html.Div([
        html.P(children='Energia total del sistema: '+str(energia)),
        dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in df1.columns]
        ),
    ], style={
        'width': '48%'
    })

], style={
    'display': 'flex',
    'flex-direction': 'row',
    'align-items': 'center',
    'justify-content': 'center',
})


@app.callback(
    Output('feature-graphic', 'figure'),
    [Input('opcion', 'value')]
)
def update_graph(index):
    traces = []
    for num in index:
        y = []
        x = []
        for i in range(len(Ag)):
            energia = 0
            if(i != num):
                x.append(i)
                for k in range(len(I)):
                    energia += U(distancia(Ag[num], I[k]))
                energia += U(distancia(Ag[num], Ag[i]))
                y.append(energia)
        traces.append({'x': x, 'y': y, 'name': num,
                       'mode': 'lines', 'name': 'Ag-'+str(num)})
    fig = {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Numero de Ag'},
            yaxis={'title': 'Energia'},
            hovermode='closest'
        )
    }
    return fig


@app.callback(
    Output('table', 'data'),
    [Input('opcion', 'value')]
)
def update_table(index):
    datos = []
    for i in index:
        data = {}
        for k, v in df1.to_dict('records')[i].items():
            data[k] = v
        datos.append(data)
    return datos


if __name__ == '__main__':
    app.run_server(debug=True)
