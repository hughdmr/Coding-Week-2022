## Importation ##

import dash
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html
from dash import html, dcc, Input, Output, State, callback
from dash.dependencies import Input, Output
from tweets_collect.to_dataframe import to_dataframe
from tweets_collect.main_collect import *
from tweets_analysis.stats import *


dash.register_page(__name__, path="/users",
                   title='Insultes par utilisateur', name='users')

dff = main_user('sandrousseau')

fig = px.scatter(dff, x="user.followers_count", y="retweet_count",
                 size="favorite_count", color="user.verified")

layout = html.Div(
    children=[
        html.H1(children="Informations sur un utilisateur",
                style={'padding-left': '20px'}),
        dbc.Row([
            dbc.Col(dbc.Input(placeholder="Entrer un utilisateur",
                              id='user_name', type='text')), dbc.Col(dbc.Button('Submit', id='submit-val-user', n_clicks=0, style={'background': '#FF7C7C'}))], style={'width': '48%', 'padding': '10px 10px 10px 20px'}),
        html.Div([

            html.Div(
                 dcc.Dropdown(options={'favorite_count': 'Nombre de likes', 'retweet_count': 'Nombre de retweets', 'user.favourites_count': 'Nombre de Likes du compte', 'user.followers_count': 'Nombre de followers',
                                       'user.friends_count': "Nombre d'amis", 'insult': 'Caractère insultant du tweet'}, id='menu_abcisses-user'), style={'width': '48%', 'display': 'inline-block', 'padding': '10px 10px 10px 20px'}),

            html.Div(
                dcc.Dropdown(options={'favorite_count': 'Nombre de likes', 'retweet_count': 'Nombre de retweets', 'user.favourites_count': 'Nombre de Likes du compte', 'user.followers_count': 'Nombre de followers',
                                      'user.friends_count': "Nombre d'amis", 'insult': 'Caractère insultant du tweet'}, id='menu_ordonnées-user'), style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'padding': '10px 10px 10px 10px'})
        ]),
        html.Div(
            dcc.Graph(id='dash_graph_user')),
        html.H1(children="Bloquer un utilisateur",
                style={'padding': '0 0 40px 20px'}),
        dbc.Row([
            dbc.Col(dbc.Input(placeholder="Entrer un utilisateur",
                              id='user_name_2', type='text')), dbc.Col(dbc.Button('Bloquer', id='submit-val-user-2', n_clicks=0, style={'background': '#A0A0A0'}))], style={'width': '48%', 'padding': '10px 10px 10px 20px'})
    ])


@callback(
    Output('dash_graph_user', 'figure'),
    State('user_name', 'value'),
    Input('submit-val-user', 'n_clicks'),
    Input('menu_abcisses-user', 'value'),
    Input('menu_ordonnées-user', 'value'), suppress_callback_exceptions=True)
def update_graphe(user_name, n_clicks, xaxis_column_name, yaxis_column_name):
    if n_clicks >= 1:
        n_clicks = 0
        dff = main_user(user_name)
        dff = ajout_colonnes(dff)
    fig = px.scatter(dff, x=xaxis_column_name,
                     y=yaxis_column_name)

    fig.update_xaxes(title=xaxis_column_name, type='linear')

    fig.update_yaxes(title=yaxis_column_name, type='linear')

    return fig
