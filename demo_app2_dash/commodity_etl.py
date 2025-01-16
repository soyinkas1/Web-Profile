
from datetime import datetime
import requests
import pandas as pd
from alpha_vantage.commodities import Commodities
from .config import Configuration
import os
import numpy as np

config = Configuration()




class CommodityData:
    """"
    This class objects defines the data extraction, transformation, cleaning and loading stage of the application"""

    def __init__(self, api_key=config.api_key):
        """ Initiates the class object with the api_key.
        Sets the base directory      
        
        """
        self.api_key=api_key
        self.cd = Commodities(self.api_key)

        base_dir = os.path.abspath(os.path.dirname(__file__))
        print(base_dir)
        self.data_dir = os.path.join(base_dir, 'data')


    def etl_commodity_data(self, commodity, interval, start_date , end_date):
        """" Extract data from alpha-vantage APi and save into csv if not already downloaded
        
        Parameters:
        commodity: The alpha-vantage commodity code 
        interval: Interval for the data - options ['daily', 'monthly', 'yearly']
        start_date: Start date for data in format YYYY-MM-DD 
        end_date: End date for data in format YYYY-MM-DD   
        """    

        # Convert string dates to datetime objects 
        start_date = datetime.strptime(start_date, '%Y-%m-%d') 
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        # today_date = datetime.strptime(str(datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d')
        
        # from IPython import get_ipython # Get the current working directory 
        # base_dir = get_ipython().run_line_magic('pwd', '')
        # Get list of files in data directory
        if commodity == 'WTI':
            wti_dir = os.path.join(self.data_dir, 'WTI')
            # Check if the directory exists and create it if it does not 
            if not os.path.exists(wti_dir): 
                os.makedirs(wti_dir)
            file = os.listdir(wti_dir)
            
            # Check if there is no existing download
            if str(end_date.strftime('%Y-%m-%d') +'.csv') not in file:
                # Download from API for commodity requested
                wti_data = self.cd.get_wti(interval)
                
                if wti_data[0].values.any() != "":
                    wti_df = pd.DataFrame(wti_data[0])
                    
                    # Transform to time-series df
                    wti_df.set_index('date', drop=True, inplace=True)
                    
                    # Convert date column to datetime
                    wti_df.index = pd.to_datetime(wti_df.index)

                    # Replace the . with nan
                    wti_df['value'] = wti_df['value'].replace('.', np.nan)                         
                        
                    # Fill missing data using backfill
                    wti_df = wti_df.bfill()

                    # Load the full file to csv 
                    wti_df.to_csv(f'{self.data_dir}/{commodity}/{str(end_date.strftime('%Y-%m-%d') +'.csv')}')

                    # Filter for the start date and end date
                    wti_df = wti_df[(wti_df.index >= start_date) & (wti_df.index <= end_date)]
                else:
                    data = pd.DataFrame() # Create an empty DataFrame if data is unavailable or response fails return
                    
                    return print("No data available - try again later")
            
                return wti_df    
                    
            else:
                wti_df = pd.read_csv(f'{self.data_dir}/{commodity}/{str(end_date.strftime('%Y-%m-%d') +'.csv')}')
                
                # Transform to time-series df
                wti_df.set_index('date', drop=True, inplace=True)
                
                # Convert date column to datetime
                wti_df.index = pd.to_datetime(wti_df.index)
                                           
                # Replace the . with nan
                wti_df['value'] = wti_df['value'].replace('.', np.nan)        
                # Fill missing data using backfill
                wti_df = wti_df.bfill()
                # Filter for the start date and end date
                wti_df = wti_df[(wti_df.index >= start_date) & (wti_df.index <= end_date)]
            return wti_df
        
        if commodity == 'brent':
            brent_dir = os.path.join(self.data_dir, 'brent')
            # Check if the directory exists and create it if it does not 
            if not os.path.exists(brent_dir): 
                os.makedirs(brent_dir)
            file = os.listdir(brent_dir)
            
            # Check if there is no existing download
            if str(end_date.strftime('%Y-%m-%d') +'.csv') not in file:
                # Download from API for commodity requested
                brent_data = self.cd.get_brent(interval)
                
                if brent_data[0].values.any() != "":
                    brent_df = pd.DataFrame(brent_data[0])
                    
                    # Transform to time-series df
                    brent_df.set_index('date', drop=True, inplace=True)
                    
                    # Convert date column to datetime
                    brent_df.index = pd.to_datetime(brent_df.index)

                    # Replace the . with nan
                    brent_df['value'] = brent_df['value'].replace('.', np.nan)                         
                        
                    # Fill missing data using backfill
                    brent_df = brent_df.bfill()

                    # Load the full file to csv 
                    brent_df.to_csv(f'{self.data_dir}/{commodity}/{str(end_date.strftime('%Y-%m-%d') +'.csv')}')

                    # Filter for the start date and end date
                    brent_df = brent_df[(brent_df.index >= start_date) & (brent_df.index <= end_date)]
                else:
                    data = pd.DataFrame() # Create an empty DataFrame if data is unavailable or response fails return
                    
                    return print("No data available - try again later")
            
                return brent_df    
                    
            else:
                brent_df = pd.read_csv(f'{self.data_dir}/{commodity}/{str(end_date.strftime('%Y-%m-%d') +'.csv')}')
                
                # Transform to time-series df
                brent_df.set_index('date', drop=True, inplace=True)
              
                # Convert date column to datetime
                brent_df.index = pd.to_datetime(brent_df.index)
                                           
                # Replace the . with nan
                brent_df['value'] = brent_df['value'].replace('.', np.nan)        
                # Fill missing data using backfill
                brent_df = brent_df.bfill()
                # Filter for the start date and end date
                brent_df = brent_df[(brent_df.index >= start_date) & (brent_df.index <= end_date)]
            return brent_df
        
