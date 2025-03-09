from dash import Dash
from dash.html import Center
import plotly.express as px
<<<<<<< HEAD
=======
import plotly.graph_objects as go
from alpha_vantage.timeseries import TimeSeries
>>>>>>> main
from dash import dcc, html, Output, Input, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import os
from demo_app2_dash.utils.commodity_etl import CommodityData
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import os
from prophet import Prophet
from prophet.plot import plot_plotly
from demo_app2_dash.utils.common import prep_train_data_prophet
from datetime import datetime

bootstrap_css_path = os.path.join('static', 'vendor', 'bootstrap','css', 'bootstrap.min.css')

def init_com_dashboard(server):
    """Create a Plotly Dash dashboard. 
    To analyse and forecast crude oil prices"""
    dash_app1 = Dash(server=server , 
           routes_pathname_prefix='/dashapp1/',
           external_stylesheets=[bootstrap_css_path, 'static\\vendor\\main.css', 'static\\vendor\\aos\\aos.css'],
           meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])

    # Main Layout 
    dash_app1.layout = html.Div( style=
                        { 'display': 'flex', 
                        'justify-content': 'center', 
                        'align-items': 'center',
                        'gap': '30px', 
                            }, 
                        children=[dbc.Container( [
                                        html.H2("Crude Oil Price Tracker", className='section-title'  ),
                                        # Selector section
                                        html.Div([
                                            html.P('Select Commodity',style={'padding': '20px', 'fontWeight': 'bold'}),
                                            dcc.Dropdown(id='commodity_id', options=[{'label': 'WTI', 'value': 'WTI'}, 
                                                                                    {'label': 'Brent', 'value': 'brent'}], value='WTI'), 
                                            html.P('Pick Date Interval', style={'padding': '10px', 'fontWeight': 'bold'}),
                                            dcc.RadioItems(id='interval_id', options=[{'label': 'Daily', 'value': 'daily'}, 
                                                                    {'label': 'Weekly', 'value': 'weekly', } , 
                                                                    {'label': 'Monthly', 'value': 'monthly', } ], inline=True, value='daily', style={'marginRight':'20px'}),
                                            html.P('Prediction Range', style={'padding': '10px', 'fontWeight': 'bold'}),
                                            dcc.Slider( id='prediction_slider', min=1, max=30, step=2, value=30, 
                                                    marks={i: str(i) for i in range(1, 31)}, 
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
                                                                end_date=datetime.today().date() ),
                                            html.H4(children='Price Trend', style={'padding': '20px'}),
                                            
                                            
                                            dcc.Graph(id='trend_graph', figure={},style={ 'borderRadius': '10px', 
                                                          'backgroundColor': '#f9f9f9', 
                                                           'marginBottom': '20px'  }),
                                                
                                                
                                                ], style={ 'borderRadius': '10px', 
                                                         'border': '1px solid #ccc', 
                                                          'padding': '10px', 
                                                           'backgroundColor': '#f9f9f9', 
                                                           'marginBottom': '20px'  }),
                                            # Time series Prediction Graph section
                                        html.Div([
                                            
                                            html.H4(children='Price Prediction', style={'padding': '20px'}),
                                            
                                            
                                            dcc.Graph(id='pred_graph', figure={},style={ 'borderRadius': '10px', 
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

    # Forecasting Graph
    @dash_app1.callback(
        Output(component_id='pred_graph', component_property='figure'),
        Input(component_id='commodity_id', component_property='value'),
        Input(component_id='interval_id', component_property='value'),
        Input(component_id='prediction_slider', component_property='value'),
        Input(component_id='date-picker-range', component_property='start_date'),
        Input(component_id='date-picker-range', component_property='end_date')
    )
    def draw_pred_graph(commodity, interval, horizon, start_date, end_date):
        # Initialse the dataloader
        cd = CommodityData()
        # Upload data from storage
        df = cd.etl_commodity_data(commodity, interval, start_date, end_date)

       # Prep data for Prophet
        train_df, _ = prep_train_data_prophet(df) 

        # Initialse the model
        model = Prophet(
        changepoint_prior_scale=0.1,
        seasonality_prior_scale=10.0,
        holidays_prior_scale=0.1,
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
        )  
        
        # Fit the model
        model.fit(train_df)

        # define horizon
        forecast_period = interval
        period_dict = {'daily': 1, 'weekly': 7, 'monthly': 30}
        n_select = horizon
        period_days = period_dict[forecast_period] * n_select

        # make future dataframe
        future = model.make_future_dataframe(periods=period_dict[forecast_period] * n_select)

        # Forecast for future
        forecast = model.predict(future)

        # Plot the forecast
        fig = plot_plotly(model, forecast)
        
        # Add labels
        fig.layout.update(title = f'{forecast_period}'.title() + " Forecast for " + f'{commodity.upper()} ' + "(" +  
                    f'{period_days} days'+ ")",
                    xaxis_title= 'Date', yaxis_title='Price', 
                        showlegend=True,
                        xaxis=dict(
                    rangeslider=dict(
                        visible=True
                    )))
        # Provide custom legend labels
        fig.update_traces(
            name="Forecast",   
            selector=dict(mode="lines")  
        )
        fig.update_traces(
            name="",  
            selector=dict(fill="tonexty"))  
        
        return fig



    # if __name__=='__main__':
    #     dash_app1.run_server(debug=True, port=8000)

