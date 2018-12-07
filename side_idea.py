import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

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
    dcc.Graph(id='bar_plot',
              figure=go.Figure(data=create_traces(df_f),
                               layout=go.Layout(barmode='stack'))
              )
])

if __name__ == '__main__':
    app.run_server(port=8060)
