import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from dash import dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
# import subprocess
import os
import demo_perplexity
import demo_openai

# Load the new dataset
nevo_df = pd.read_csv('NEVO2023_8.0_clean.csv')

app = dash.Dash(__name__)
server = app.server

# Assuming the dataset has a column 'Food Item' and 'Vitamin C (mg/100g)'
food_items = nevo_df['Food group'].unique().tolist()
food_options = [{'label': item, 'value': item} for item in food_items]

value_items = ['Bevat sporen van/Contains traces of', 'Is verrijkt met/Is fortified with', 'ENERCJ (kJ)', 'ENERCC (kcal)', 'WATER (g)', 'PROT (g)', 'PROTPL (g)', 'PROTAN (g)', 'NT (g)', 'TRP (mg)', 'FAT (g)', 'FACID (g)', 'FASAT (g)', 'FAMSCIS (g)', 'FAPU (g)', 'FAPUN3 (g)', 'FAPUN6 (g)', 'FATRS (g)', 'CHO (g)', 'SUGAR (g)', 'STARCH (g)', 'POLYL (g)', 'FIBT (g)', 'ALC (g)', 'OA (g)', 'ASH (g)', 'CHORL (mg)', 'NA (mg)', 'K (mg)', 'CA (mg)', 'P (mg)', 'MG (mg)', 'FE (mg)', 'HAEM (mg)', 'NHAEM (mg)', 'CU (mg)', 'SE (µg)', 'ZN (mg)', 'ID (µg)', 'VITA_RAE (µg)', 'VITA_RE (µg)', 'RETOL (µg)', 'CARTBTOT (µg)', 'CARTA (µg)', 'LUTN (µg)', 'ZEA (µg)', 'CRYPXB (µg)', 'LYCPN (µg)', 'VITD (µg)', 'CHOCALOH (µg)', 'CHOCAL (µg)', 'ERGCAL (µg)', 'VITE (mg)', 'TOCPHA (mg)', 'TOCPHB (mg)', 'TOCPHD (mg)', 'TOCPHG (mg)', 'VITK (µg)', 'VITK1 (µg)', 'VITK2 (µg)', 'THIA (mg)', 'RIBF (mg)', 'VITB6 (mg)', 'VITB12 (µg)', 'NIAEQ (mg)', 'NIA (mg)', 'FOL (µg)', 'FOLFD (µg)', 'FOLAC (µg)', 'VITC (mg)', 'F4:0 (g)', 'F6:0 (g)', 'F8:0 (g)', 'F10:0 (g)', 'F11:0 (g)', 'F12:0 (g)', 'F13:0 (g)', 'F14:0 (g)', 'F15:0 (g)', 'F16:0 (g)', 'F17:0 (g)', 'F18:0 (g)', 'F19:0 (g)', 'F20:0 (g)', 'F21:0 (g)', 'F22:0 (g)', 'F23:0 (g)', 'F24:0 (g)', 'F25:0 (g)', 'F26:0 (g)', 'FASATXR (g)', 'F10:1CIS (g)', 'F12:1CIS (g)', 'F14:1CIS (g)', 'F16:1CIS (g)', 'F18:1CIS (g)', 'F20:1CIS (g)', 'F22:1CIS (g)', 'F24:1CIS (g)', 'FAMSCXR (g)', 'F18:2CN6 (g)', 'F18:2CN9 (g)', 'F18:2CT (g)', 'F18:2TC (g)', 'F18:2R (g)', 'F18:3CN3 (g)', 'F18:3CN6 (g)', 'F18:4CN3 (g)', 'F20:2CN6 (g)', 'F20:3CN9 (g)', 'F20:3CN6 (g)', 'F20:3CN3 (g)', 'F20:4CN6 (g)', 'F20:4CN3 (g)', 'F20:5CN3 (g)', 'F21:5CN3 (g)', 'F22:2CN6 (g)', 'F22:2CN3 (g)', 'F22:3CN3 (g)', 'F22:4CN6 (g)', 'F22:5CN6 (g)', 'F22:5CN3 (g)', 'F22:6CN3 (g)', 'F24:2CN6 (g)', 'FAPUXR (g)', 'F10:1TRS (g)', 'F12:1TRS (g)', 'F14:1TRS (g)', 'F16:1TRS (g)', 'F18:1TRS (g)', 'F18:2TTN6 (g)', 'F18:3TTTN3 (g)', 'F20:1TRS (g)', 'F20:2TT (g)', 'F22:1TRS (g)', 'F24:1TRS (g)', 'FAMSTXR (g)', 'FAUN (g)']
value_options = [{'label': item, 'value': item} for item in value_items]

app.layout = html.Div(children=[
    html.H1('NEVO 2023 Food Dataset Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    dcc.Dropdown(id='food_dropdown', options=food_options, placeholder='Select a group of food item', searchable=True),
    html.Br(),
    dcc.Dropdown(id='value_dropdown', options=value_options, placeholder='Select a value to display', searchable=True),
    html.Br(),
    html.Div(dcc.Graph(id='bar-chart')),
    html.Br(),

    # Use a Row to split the screen
    dbc.Row([
        # Left column for the data table
        dbc.Col([
            html.Div([
                dash_table.DataTable(
                    id='data-table',
                    columns=[{"name": i, "id": i} for i in nevo_df.columns],
                    data=nevo_df.to_dict('records'),
                    page_size=10,  # Number of rows per page
                    style_table={'overflowX': 'auto', 'overflowY': 'auto', 'height': '400px'},
                    style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '100px', 'maxWidth': '100px'},
                ),
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),  # Adjust width as needed

            html.Div([
                dcc.RadioItems(
                    id='model_selector',
                    options=[
                        {'label': 'Perplexity', 'value': 'perplexity'},
                        {'label': 'OpenAI', 'value': 'openai'}
                    ],
                    value='perplexity',  # Default value
                    labelStyle={'display': 'inline-block'}
                ),
                html.Br(),
                dcc.Textarea(
                    id='question-input',
                    placeholder='Enter your question here',
                    style={'width': '80%', 'height': '100px', 'margin': '0 auto'}
                ),
                html.Br(),
                html.Button('Submit', id='submit-button', n_clicks=0),
                html.Br(),
                dcc.Loading(
                    id="loading",
                    type="circle",  # You can choose "default", "circle", or "dot"
                    children=[
                        html.Div(id='output-container', children='Enter a question and press submit')
                    ]
                ),
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '20px'}),
        ], width='auto'),  # Set width to auto for flexible spacing
    ]),
    html.Br(),
])

@app.callback(
    Output(component_id='bar-chart', component_property='figure'),
    [Input(component_id='food_dropdown', component_property='value'),
     Input(component_id='value_dropdown', component_property='value')]
)
def update_bar_chart(selected_food, selected_value):
    if selected_food:
        df = nevo_df[nevo_df['Food group'] == selected_food]
        df = df.sort_values(by=selected_value, ascending=True)
        fig = px.bar(df, x='Engelse naam/Food name', y=selected_value, title=f'{selected_value} in {selected_food}')
    else:
        fig = px.bar(nevo_df, x='Engelse naam/Food name', y=selected_value, title=f'{selected_value} in All Food Items')
    return fig

@app.callback(
    Output('output-container', 'children'),
    [Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('question-input', 'value'),
     dash.dependencies.State('model_selector', 'value')]
)
def update_output(n_clicks, value, selected_model):
    if n_clicks > 0 and value:
        if selected_model == 'perplexity':
            script, citations, output = demo_perplexity.llm(value)
        else:
            script, citations, output = demo_openai.llm(value)

        # Check for new files in the current directory
        new_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.csv') and not f.startswith('NEVO')]
        
        if new_files:
            latest_file = max(new_files, key=os.path.getctime)
            print(latest_file)
            new_df = pd.read_csv(latest_file)
            
            # Create a DataTable for the new CSV
            table = dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in new_df.columns],
                data=new_df.to_dict('records'),
                page_size=10,
                style_table={'overflowX': 'auto', 'overflowY': 'auto', 'height': '400px'},
                style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '100px', 'maxWidth': '100px'},
            )
            
            # Delete the file after processing
            os.remove(latest_file)
            
            return table

        lst = []
        new_line = html.Br()
        if output:
            blocks = output.split('\n')
            for block in blocks:
                lst.append(html.Div(block))  # Convert each line to a Dash HTML component
                
        lst.append(new_line)
        if script:
            lst.append(html.Div(html.B('The following is the script used to generate the answer:')))
            try:
                blocks = script.stdout.split('\n')
            except AttributeError:
                blocks = script.split('\n')
            for each in blocks:
                lst.append(html.Div(each))  # Convert each line to a Dash HTML component
        
        lst.append(new_line)

        if citations:
            lst.append(html.Div(html.B('The following are the citations used:')))
            lst.append(new_line)
            for i, citation in enumerate(citations):
                lst.append(html.Div(f'[{i+1}]'+citation))
        
        return lst
    
    # return 'Enter a question and press submit'

if __name__ == '__main__':
    app.run_server(debug=False)