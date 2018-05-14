import os
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


df = pd.read_csv('/Users/Roman/desktop/crem/swiss energy data/Données nbre bâtiments par agents énergétiques')
df.drop(['Unnamed: 0'],axis=1,inplace=True)

app = dash.Dash()

app.layout = html.Div([
	html.Div([
 
  		
  	dcc.Graph(id='chauffage'),
  	dcc.Graph(id='ECS'),

    dcc.Slider(
            id='year--slider',
            min=df['Année'].min(),
            max=df['Année'].max(),
            value=df['Année'].max(),
            step=None,
            marks={str(year): str(year) for year in df['Année'].unique()})
	])

@app.callback(
    dash.dependencies.Output('chauffage', 'figure'),
    [dash.dependencies.Input('year--slider', 'value')])

def update_graphCH(year_value):
    dff = df[df['Année'] == year_value]

    return {
        'data': [
        {
            "labels":['Autres','Bois','Capteurs solaires','CAD','Charbon','Électricité','Gaz','Mazout','PAC'],
            "values":dff.groupby(['Agent énergétique chauffage'])['Nombre de bâtiments'].sum(),
            "colors":['Reds'],
            "text":"CHAUF",
      		"textposition":"inside",
      		"domain": {"x": [.52, 1]},
     		"name": "Chauffage",
      		"hoverinfo":"label+percent+name",
      		"hole": .4,
     		"type": "pie"
           }]

            }

@app.callback(
    dash.dependencies.Output('ECS', 'figure'),
    [dash.dependencies.Input('year--slider', 'value')])

def update_graphECS(year_value):
    dff = df[df['Année'] == year_value]

    return {
        'data': [
        {
            "labels":['Autres','Bois','Capteurs solaires','CAD','Charbon','Électricité','Gaz','Mazout','PAC'],
            "values":dff.groupby(['Agent énergétique ECS'])['Nombre de bâtiments'].sum(),
            "text":"ECS",
      		"textposition":"inside",
      		"domain": {"x": [.52, 1]},
     		"name": "ECS",
      		"hoverinfo":"label+percent+name",
      		"hole": .4,
     		"type": "pie"
           }]

            }

if __name__ == '__main__':
    app.run_server()