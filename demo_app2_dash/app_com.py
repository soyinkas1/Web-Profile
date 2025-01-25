from dash import Dash, dcc, html, Output, Input

from dash.html import Center
import plotly.express as px
import plotly.graph_objects as go
from alpha_vantage.timeseries import TimeSeries
from dash import dcc, html, Output, Input, dash_table
import plotly.express as px
from alpha_vantage.commodities import Commodities
import dash_bootstrap_components as dbc
import os
from .commodity_etl import CommodityData

bootstrap_css_path = os.path.join('static', 'vendor', 'bootstrap','css', 'bootstrap.min.css')

def init_com_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app1 = Dash(server=server , 
           routes_pathname_prefix='/dashapp1/',
           external_stylesheets=[bootstrap_css_path, 'static\\vendor\\main.css', 'static\\vendor\\aos\\aos.css'],
           meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])

# app = Dash(server=server , 
#            routes_pathname_prefix='dashapp1',
#            external_stylesheets=[bootstrap_css_path, 'static\\vendor\\main.css', 'static\\vendor\\aos\\aos.css'],
#            meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])

    dash_app1.layout = html.Div( style=
                        { 'display': 'flex', 
                        'justify-content': 'center', 
                        'align-items': 'center',
                        'gap': '30px', 
                            }, 
                        children=[dbc.Container( [
                                        html.H2("Commodity Price Tracker", className='section-title'  ),
                                        # Selector section
                                        html.Div([
                                            html.P('Select commodity',style={'padding': '20px', 'fontWeight': 'bold'}),
                                            dcc.Dropdown(id='commodity_id', options=[{'label': 'WTI', 'value': 'WTI'}, 
                                                                                    {'label': 'Brent', 'value': 'brent'}], value='WTI'), 
                                            html.P('Pick date interval', style={'padding': '10px', 'fontWeight': 'bold'}),
                                            dcc.RadioItems(id='interval_id', options=[{'label': 'Daily', 'value': 'daily'}, 
                                                                    {'label': 'Weekly', 'value': 'weekly', } , 
                                                                    {'label': 'Monthly', 'value': 'monthly', } ], inline=True, value='daily', style={'marginRight':'20px'}),
                                            html.P('Predition Range (years)', style={'padding': '10px', 'fontWeight': 'bold'}),
                                            dcc.Slider( id='prediction_slider', min=1, max=10, step=1, value=5, 
                                                    marks={i: str(i) for i in range(1, 11)}, 
                                                    tooltip={'always_visible': True, 'placement': 'bottom'} )
                                                ],style={ 'borderRadius': '10px', 
                                                         'border': '1px solid #ccc', 
                                                          'padding': '10px', 
                                                          'marginBottom': '20px',
                                                           'backgroundColor': '#f9f9f9'  }),

                                        # Time series Trend Graph section
                                        html.Div([
                                            html.P("Select Date Range", style={'padding': '10px', 'fontWeight': 'bold'}),
                                            dcc.DatePickerRange( id='date-picker-range', 
                                                                start_date='2024-01-01', 
                                                                end_date='2025-01-01' ),
                                            html.H4(children='Price Trend', style={'padding': '20px'}),
                                            
                                            
                                            dcc.Graph(id='trend_graph', figure={},style={ 'borderRadius': '10px', 
                                                          'backgroundColor': '#f9f9f9', 
                                                           'marginBottom': '20px'  }),
                                                
                                                
                                                ], style={ 'borderRadius': '10px', 
                                                         'border': '1px solid #ccc', 
                                                          'padding': '10px', 
                                                           'backgroundColor': '#f9f9f9', 
                                                           'marginBottom': '20px'  }),




    ], style={'align-items': 'center', 'width':800, 'gap': '30px'})
    ])

      # Pass dash_app1 as a parameter
    init_callbacks(dash_app1)

    return dash_app1.server
    
def init_callbacks(dash_app1):

    @dash_app1.callback(
        Output(component_id='trend_graph', component_property='figure'),
        Input(component_id='commodity_id', component_property='value'),
        Input(component_id='interval_id', component_property='value'),
        Input(component_id='date-picker-range', component_property='start_date'),
        Input(component_id='date-picker-range', component_property='end_date')
    )
    def draw_trend_graph(commodity, interval, start_date, end_date):
        # Initialse the dataloader
        cd = CommodityData()
        # Upload data from storage
        df = cd.etl_commodity_data(commodity, interval, start_date, end_date)

        # Create the trend chart 
        fig = px.line(df,y='value', title=f'Commodity - {commodity} Price Trend Over Time ({interval})',
                    labels={'value': 'Price', 'date': 'Date'})

        # Add labels
        fig.update_layout(title={'xanchor': 'left', 'yanchor': 'top' },
                        legend_title_text='Legend', 
                        xaxis_title='Date', 
                        yaxis_title='Price', 
                        showlegend=True,
                       xaxis=dict(
        rangeslider=dict(
            visible=True
        )
    ))
        return fig




    # if __name__=='__main__':
    #     dash_app1.run_server(debug=True, port=8000)

