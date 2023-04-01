## Importation ##

import dash
import nltk
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc, Input, Output, State, callback
from dash.dependencies import Input, Output
from tweets_collect.to_dataframe import *
from insult_detector.main_detector import detecteur

dash.register_page(__name__, path='/dashboard', title='Accueil',
                   name='accueil', order=0)

df = to_dataframe('data_G20.json')
df = epuration_dataframe_elevee(df)


def generate_table(dataframe, max_rows=10):
    return dbc.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])], bordered=True, style={'border-collapse': 'collapse', 'padding': '30px 15px', 'text-align': 'left', 'border-bottom': '1px solid #E1E1E1', 'padding-left': '0', 'padding-right': '0'})


layout = html.Div([
    html.H1("Bienvenue sur InsulBlock, le meilleur bloqueur d'insultes",
            style={'textAlign': 'center'}),
    dbc.Row([
        dbc.Col(dbc.Toast(
            [html.P("1400", className="mb-0")],
            id="simple-toast-1",
            header="Nombre de Tweets postés",
            icon="primary",
            dismissable=True,
            is_open=True)),
        dbc.Col(dbc.Toast(
            [html.P("66", className="mb-0")],
            id="simple-toast-2",
            header="Nombres de tweets insultes",
            icon="alert",
            dismissable=True,
            is_open=True)),
        dbc.Col(dbc.Toast(
            [html.P("4,71%", className="mb-0")],
            id="simple-toast-3",
            header="Pourcentage d'insultes",
            icon="danger",
            dismissable=True,
            is_open=True))], style={'padding': '30px 0 0 40px'}),
    html.H2("Détectez si un tweet est une insulte!",
            style={'textAlign': 'center', 'padding': '60px 0 0 0'}),
    dbc.Row([
        dbc.Col([dbc.Input(id='my-input', placeholder="Inserer un tweet",
                           type='text')], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'}
                ),
        dbc.Col(dbc.Button('Submit', id='submit-val', n_clicks=0,
                           style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw', 'background': '#FF7C7C'})),
        dbc.Col(html.Div(id='my-output',
                         style={'margin-left': '3vw', 'margin-top': '3vw'}))]),
    html.Div(id='output-state'),
    html.Br(),
    html.H2("Tweets en live #Actualité",
            style={'textAlign': 'center', 'padding': '40px 0 0 40px'}),
    generate_table(df)

])


@ callback(
    Output(component_id='my-output', component_property='children'),
    State('my-input', 'value'),
    Input('submit-val', 'n_clicks'))
def update_output_div(input_value, n_clicks):

    if n_clicks >= 1:
        n_clicks = 0
        if detecteur(input_value) == True:
            return "c'est une insulte"
        else:
            return "Ce n'est pas une insulte"

    else:
        return
