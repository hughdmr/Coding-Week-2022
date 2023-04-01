## Importation ##

import dash
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html
from dash import Input, Output, State, html, dcc, callback
import base64

Logo_src = "./visualisation_gui/Logo.png"

encoded_image = base64.b64encode(open(Logo_src, 'rb').read())

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.LUX], use_pages=True)

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem"}


nav_item1 = dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard"))
nav_item2 = dbc.NavItem(dbc.NavLink("Subject", href="/subject"))
nav_item3 = dbc.NavItem(dbc.NavLink("Users", href="users"))

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), height="30px")),
                        dbc.Col(dbc.NavbarBrand(
                            "InsultBlock", className="ms-2")),
                        dbc.Spinner(color="danger", size="sm")
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://twitter.com/home",
                style={"textDecoration": "none"},
            ),
            dbc.Nav(
                [nav_item1, nav_item2, nav_item3],
                className="ms-auto",
                navbar=True,
            )
        ],
    ),
    color="dark",
    dark=True,
    className="mb-5",
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    navbar,
    content,
    dash.page_container
])
