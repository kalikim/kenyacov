from flask_restful import Resource
from flask import jsonify, request
import pandas as pd
from io import StringIO
import requests
import numpy as np





class kenyacovid(Resource):

    def get(self):
        url = 'https://datahub.io/core/covid-19/r/time-series-19-covid-combined.csv'
        s = requests.get(url).text

        df = pd.read_csv(StringIO(s), usecols=['Date', 'Country/Region', 'Confirmed', 'Recovered', 'Deaths'])
        # newdate=pd.datetime(df.Date, format="%m/%d/%y")
        df.reset_index(drop=True, inplace=True)
        df['newdate'] = pd.to_datetime(df['Date'], format="%Y/%m/%d")
        df_renamed = df.rename(columns={"Country/Region": "country"})

        df_renamed = (df_renamed
                      .filter(['country', 'Confirmed', 'Recovered', 'Deaths', 'newdate'])
                      .sort_values(['country', 'newdate'])
                      )
        df_renamed.set_index('country', inplace=True)
        df_kenya = df_renamed.loc['Kenya']

        list_header=['Confirmed', 'Recovered', 'Deaths','Date']
        result_list=df_kenya.values[-1].tolist()


        combined_result = {"Kenya" : {list_header[j]: result_list[i * len(list_header) + j] for j in
                                                    range(len(list_header))} for i in
                           range(len(result_list) // len(list_header))}
        return jsonify(combined_result)







