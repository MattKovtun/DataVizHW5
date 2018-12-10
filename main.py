import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

app = dash.Dash('Hello World')

df = pd.read_csv("population_by_age_sex_year.csv")
df_f = pd.read_csv("population_by_age_sex_year_grouped.csv")


def create_traces(df):
    traces = []
    for group in df["group"].unique():
        years = df["year"].unique()
        xaxis = []
        for year in years:
            ddf = df[df["group"] == group]
            men = ddf.loc[ddf["year"] == year, "men"].sum()
            women = ddf.loc[ddf["year"] == year, "men"].sum()
            xaxis.append(men + women)

        traces.append(go.Bar(
            x=years,
            y=xaxis,
            name=group
        ))
    return traces


app.layout = html.Div([
    html.Div([
        dcc.Graph(id='bar_plot',
                  figure=go.Figure(data=create_traces(df_f),
                                   layout=go.Layout(barmode='stack'))
                  )
    ]),
    dcc.Graph(id='my-graph'),
    html.Div([
        dcc.Slider(
            id='slider',
            min=min(df['year'].unique()),
            max=max(df['year'].unique()),
            marks={int(i): str(i) for i in df['year'].unique()},
            value=min(df['year'].unique()),
            updatemode='drag',

        )], style={"width": "95%"}
    )], style={"max-width": "1140px",
               "margin": "auto"})

df_f = pd.read_csv("population_by_age_sex_year_grouped.csv")


@app.callback(Output('my-graph', 'figure'),
              [Input('slider', 'value')])
def update_graph(val):
    TRACES_CONFIG = [['men', 'none', 'rgb(71, 71, 135)'],
                     ['women', 'tonexty', 'rgb(255, 121, 63)']]
    return {
        'data': [
            go.Scatter(
                x=df[df['year'] == val]['age'],
                y=df[df['year'] == val][i[0]],
                name=i[0],
                mode='lines',
                fill=i[1],
                opacity=0.4,
                line=dict(
                    color=i[2],
                )

            ) for i in TRACES_CONFIG],
        'layout': go.Layout(

            hovermode='closest',
            yaxis=dict(range=[0, 600000])

        )
    }


if __name__ == '__main__':
    app.run_server(host='0.0.0.0')
