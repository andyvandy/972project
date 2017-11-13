'''
main file for simple web viewer

This is not going to the final product but is an initial template 

For now we'll just keep this as a dash app so that we don't have to spend time thinking about html or js

unclear atm how much will be different between the paper trading viewer and the real viewer

required general features:
    -coin prices from various exchanges
    -graphing:
        -plotting value of the portfolio over time:
            -display trade events as markers on the chart.

live features:
    -fetch current portfolio
    -fetch open orders


TODO:
    

'''

import sys
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import configparser
import ccxt
import pandas as pd
import os
import tailer

config = configparser.SafeConfigParser(allow_no_value=True)
config.read('viewer.ini')
print(list(config['EXCHANGES'].keys()))
EXCHANGES={
    exchange:getattr(ccxt, exchange)({
            'rateLimit': 3000,
            'enableRateLimit': True,
            # 'verbose': True,
            }) 
    for exchange in config['EXCHANGES'].keys()
}
DROPDOWN_OPTIONS=[{'label':name,'value':class_name} for name,class_name in config["STRATEGIES"].items()]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H3("value"),
    dcc.Dropdown(id='dropdown-algo', options=DROPDOWN_OPTIONS , value=DROPDOWN_OPTIONS[0]['value']),
    html.Div([
        dcc.Graph(id="graph-portfoliovalue"),
        ]),
    html.H3("coin"),
    dcc.Input(id='input-1', type="text", value='ETH'),
    html.H3("basis"),
    dcc.Input(id='input-2', type="text", value='BTC'),
    html.Div(id='table'),
    html.H2("logs"),
    dcc.Markdown(id='markdown-logs'),
])


@app.callback(Output('table', 'children'),
              [Input('input-1', 'value'),
               Input('input-2', 'value')])
def update_output(input1, input2):
    pair="{}/{}".format(input1,input2)
    snapshots={name:exchange.fetch_ticker(pair) for name,exchange in EXCHANGES.items()}
    columns=['last','bid','ask','baseVolume','timestamp']
    rows=[[data[column] for column in columns ]for name,data in snapshots.items()]
    df= pd.DataFrame(rows,columns=columns,index=list(EXCHANGES.keys()))
    print(df)
    return generate_table(df,100)



def generate_table(dataframe, max_rows=10):
    table= html.Table(
        # Header
        [html.Tr([html.Th('exchange')]+[ html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr(
            [html.Td(exchange)]+[html.Td(data) for data in row.tolist()] 
        ) for exchange,row in dataframe.iterrows()]
    )
    print(table)
    return table

@app.callback(Output('graph-portfoliovalue', 'figure'),
              [Input('dropdown-algo', 'value')])
def update_value_graph(algo):

    df=pd.read_csv(os.path.join(config['GENERAL']['LOGS_DIR'],"value_history_{}.csv".format(algo)),
                names=["timestamp","value"],
                index_col=0,
                parse_dates=True
        )
    print(df)
    fig = {
        'data': [
            {
                'x':df.index,
                'y':df['value'],
                'name':"{} value over time".format(algo),
            }
        ]
    }
    return fig


@app.callback(Output('markdown-logs', 'children'),
              [Input('dropdown-algo', 'value')])
def display_logs(algo):
    #todo
    logs="  \n".join(tailer.tail(open(os.path.join(config['GENERAL']['LOGS_DIR'],"test.log"),"r"),100 ))
    print(logs)
    return logs



if __name__ == '__main__':
    app.run_server(debug=True)