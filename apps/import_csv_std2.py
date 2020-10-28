
import base64
import datetime
import io
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd 

from app import app, server

from apps import prepared_csv2 as pc


layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
])

def save_csv(filename):
    location = ("E:/Documents/Programming/Python/Dash/Dash_app2/data/{}").format(filename)
    #print(location)
    return location

def new_save_csv(filename):
    location = ("E:/Documents/Programming/Python/Dash/Dash_app2/data/new_{}").format(filename)
    #print(location)
    return location

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',') # splits a string into a list

    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            location = save_csv(filename) # get the filename string for where the csv is
            global location2
            location2 = new_save_csv(filename)
            data = io.StringIO(decoded.decode('utf-8'))
            
            data = pd.read_csv(io.StringIO(decoded.decode('utf-8')), index_col= False, skiprows=[0], skipinitialspace=True)
            
            data.to_csv(location, index=False) # save original file
                        
            df = pc.prepared_csv(location, location2)
            
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        
        dash_table.DataTable(
            data = df.to_dict('records'),
            columns = [{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

