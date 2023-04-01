## Importation ##

import dash
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dcc, State, callback
from dash.dependencies import Input, Output
from tweets_collect.to_dataframe import to_dataframe
from tweets_collect.main_collect import *
from insult_detector.detecteur_v1 import detecteur_v1
from tweets_collect.main_collect import main_subject
from tweets_analysis.stats import *

## Code ##

dash.register_page(__name__, path="/subject",
                   title='Insultes par thème', name='subject')

dff = to_dataframe('data_politique.json')

fig = px.scatter(dff, x="user.followers_count", y="retweet_count",
                 size="favorite_count", color="user.verified")

# Graphe insultes par sujet
# Fonction qui est dans stats à modifier comme tel ou alors tu la laisses dans subject


def insult_subject(subject):

    nom_fichier = 'data_' + subject + '.json'
    df = to_dataframe(nom_fichier)
    nb_insultes = 0
    nombre = len(df.index)
    if nombre > 0:
        for i in range(nombre):
            nb_insultes += detecteur_v1(df.iloc[i]['text'])
        ratio_insultes_subject = nb_insultes/nombre
        return ratio_insultes_subject
    return 0


# créer une liste de sujets que l'on veut comparer, mais faut que ce soit unique à l'anglais et/ou français
X2 = ['religion', 'macron', 'vaccin', 'guerre']
Y2 = [insult_subject(subject) for subject in X2]

df2 = pd.DataFrame({"subject": X2,
                   "count of insults": Y2, })

fig2 = px.bar(df2, x="subject",
              y="count of insults")


layout = html.Div(
    children=[
        html.H1('Analyse des tweets par thème',
                style={'padding-left': '20px'}),
        dcc.Graph(id='example-graph', figure=fig2),
        html.H2("Analyse des données du sujet",
                style={'padding': '30px 0 0 30px'}),
        dbc.Row([
            dbc.Col(dbc.Input(placeholder="Entrer un thème",
                              id='subject_name', type='text')), dbc.Col(dbc.Button('Submit', id='submit-val', n_clicks=0, style={'background': '#FF7C7C'}))], style={'width': '48%', 'padding': '20px 10px 10px 20px'}),
        dbc.Row([
            dbc.Col(dbc.Toast(
                [html.P("user_name", id='toast-1', className="mb-0")],
                id="simple-toast-1",
                header="Nombre d'insultes du sujet",
                icon="primary",
                dismissable=True,
                is_open=True)),
            dbc.Col(dbc.Toast(
                [html.P("nb_insultes", id='toast-2', className="mb-0")],
                id="simple-toast-2",
                header="Nombres d'insultes max d'un user",
                icon="alert",
                dismissable=True,
                is_open=True))], style={'padding': '30px 0 30px 50px'}),
        html.Div([

            html.Div(
                 dcc.Dropdown(options={'favorite_count': 'Nombre de likes', 'retweet_count': 'Nombre de retweets', 'user.favourites_count': 'Nombre de Likes du compte', 'user.followers_count': 'Nombre de followers',
                                       'user.friends_count': "Nombre d'amis", 'insult': 'Caractère insultant du tweet'}, id='menu_abcisses'), style={'width': '48%', 'display': 'inline-block', 'padding': '10px 10px 10px 20px'}),

            html.Div(
                dcc.Dropdown(options={'favorite_count': 'Nombre de likes', 'retweet_count': 'Nombre de retweets', 'user.favourites_count': 'Nombre de Likes du compte', 'user.followers_count': 'Nombre de followers',
                                      'user.friends_count': "Nombre d'amis", 'insult': 'Caractère insultant du tweet'}, id='menu_ordonnées'), style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'padding': '10px 10px 10px 10px'})
        ]),
        html.Div(
            dcc.Graph(id='dash_graph', style={'padding': '30px 0 0 0'}))
    ])


@ callback(
    Output('dash_graph', 'figure'),
    Output('toast-1', component_property='children'),
    Output('toast-2', component_property='children'),
    State('subject_name', 'value'),
    Input('submit-val', 'n_clicks'),
    Input('menu_abcisses', 'value'),
    Input('menu_ordonnées', 'value'))
def update_graphe(subject_name, n_clicks, xaxis_column_name, yaxis_column_name):
    if n_clicks >= 1:
        n_clicks = 0
        dff = main_subject(subject_name)
        dff = ajout_colonnes(dff)
    fig = px.scatter(dff, x=xaxis_column_name,
                     y=yaxis_column_name)

    fig.update_xaxes(title=xaxis_column_name, type='linear')

    fig.update_yaxes(title=yaxis_column_name, type='linear')

    nb = nb_insultes(dff)[0]
    max = max_insultes(dff)

    return fig, nb, max
