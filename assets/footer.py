from dash import html
import dash_bootstrap_components as dbc

_footer = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.Hr(className='hr-footer'), width=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.Ul([
                    html.Li(
                        html.A(html.I(className="fa-brands fa-github me-3 fa-1x", style={'color': 'white'}), href='https://github.com/redbluee/Raumakustik-CAD', target='_blank')
                    ),
                    html.Li(
                        html.A(html.I(className="fas fa-book me-3 fa-1x", style={'color': 'white'}), href='https://redbluee.github.io/Raumakustik-CAD/', title="Documentation", target='_blank')
                    ),
                ], className='list-unstyled d-flex mb-0')
            ], width='auto'),
            dbc.Col(
                html.P("Copyright © 2025 Paula Klein, Deniz Sharideh, Linus Staubach", className="text-end mb-0"),
                width=True
            )
        ], justify="between", align="center")
    ], fluid=True)
], className = 'footer no-print')