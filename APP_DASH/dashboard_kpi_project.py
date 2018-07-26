import os
import pandas as pd 
import numpy as np 
import plotly.graph_objs as go 
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt

import dashboard_sankey_formating as sankey
import dashboard_data as data

df = pd.read_excel(os.path.join('../PRE_PROCESS_DATA/fake_city_data.xlsx'), sheetname='Données')
dff = pd.read_excel(os.path.join('../PRE_PROCESS_DATA/fake_city_data.xlsx'), sheetname='Indicateurs')

source = sankey.source
target = sankey.target
value = sankey.value
label = sankey.label

colors = sankey.colors
labels = sankey.labels

data_new = data.data_new
data_ren = data.data_ren
data_cae = data.data_cae

app = dash.Dash()

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/62f0eb4f1fadbefea64b2404493079bf848974e8/dash-uber-ride-demo.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

app.layout = html.Div([

    
    html.Div([
        dcc.Slider(
            id='year_slider',
            min=df['Année'].min(),
            max=df['Année'].max(),
            value=df['Année'].max(),
            step=None,
            marks={str(year): str(year) for year in df['Année'].unique()}
        )

    ], style={'marginTop': 30, 'marginLeft':50, 'marginBottom':50, 'width': '95%'}),

    # FIRST COLUMN

    html.Div([

        # structure
        html.Div([


            html.Div([

                html.H3(
                    'INVESTMENTS SANKEY DIAGRAM', 
                    style = dict(backgroundColor= 'lavender', textAlign= 'center', fontSize = 24, marginLeft = 40, marginRight = 40)
                    ),
                
                dcc.Graph(
                    id ='sankey_diagram',
                    style = {'marginTop': 0}
                    ),
                
                ], style={}),

            html.Div([

                html.H3(
                    'RETURN ON INVESTMENTS', 
                    style = dict(backgroundColor= 'lavender', textAlign= 'center', fontSize = 24, marginLeft = 40, marginRight = 40)
                    ),

                dcc.Graph(
                    id='roi_graph'
                    ),

                ], style={'marginBottom':0}),
            
            html.Div([
                html.H3(''),
                dcc.RadioItems(
                    id='roi_choice_items',
                    options=[{'label': 'kWh', 'value': 'kWh'},
                            {'label': 'CO2', 'value': 'CO2'},
                            {'label': 'Aubaine', 'value': 'aubaine'},
                           	{'label': 'CHF', 'value': 'CHF'}],
                    value= 'kWh',
                    labelStyle = {'textAlign': 'center', 'display': 'inline-block', 'fontSize': 14},
                    style = {'textAlign': 'center', 'marginTop': 0}
                    )
                ])

            ], style={}),

    ], style={'width': '47%', 'display': 'inline-block', 'vertical-align': 'top', 'marginTop': 20, 'marginRight': 40}),

    # SECOND COLUMN

    html.Div([
    
        # title
        html.H1(''),

        # structure
        html.Div([

            # dropdown
            html.Div([
                dcc.Dropdown(
                id='ind_dropdown',
                options=[
                    {'label': 'Consommation électricité', 'value': 'conso_elec'},
                    {'label': 'Consommation chaleur', 'value': 'conso_chaleur'},
                    {'label': 'Émissions CO2', 'value': 'emissions_CO2'},
                    {'label': 'Variation IDC', 'value': 'IDC'}],
                value= 'conso_elec')
                 ], style={'marginTop': 0}),

            # graph in function of year and dropdown

            # table in function of year
            html.Div([
                dcc.Graph(id = 'ind_graph')
                ], style={}),

            html.Div([

                html.H3(
                    'KEY PERFORMANCE INDICATORS',
                    style = dict(backgroundColor= 'lavender', textAlign= 'center', fontSize = 24, marginRight = 20)),

                html.Div([
                    dt.DataTable(
                    id='datatable1',
                    rows=[{}],
                    editable=False
                    )
                ], style={'marginTop': 30, 'marginLeft':'30','width': '90%', 'display': 'inline-block', 'vertical-align': 'top'}),


            ], style={'marginTop': 17,'marginLeft': 50,'horizontal-align':'center'})
                

    ]),

        ], style= {'width': '47%', 'display': 'inline-block', 'vertical-align': 'top'})

], style={})

# Sankey Diagram

@app.callback(
    dash.dependencies.Output('sankey_diagram', 'figure'),
    [dash.dependencies.Input('year_slider', 'value')])
def sankey_graph(year):

    data = dict(
       type='sankey',
       node = dict(
           pad = 15,
           thickness = 20,
           line = dict(
               color = "black",
               width = 1
           ),
            label = labels,
            color = colors,
            opacity = 0.7
       ),
       link = dict(
           source = source,
           target = target,
           value = value,
           label = label,
           color = 'lightgray'
       )
    )

    layout = go.Layout(
        margin = dict(t=30, l=100)
        )


    figure = dict(data=[data], layout=layout)
    return figure


# Indicator histogram

@app.callback(
    dash.dependencies.Output('roi_graph','figure'),
    [dash.dependencies.Input('year_slider','value'),
     dash.dependencies.Input('roi_choice_items','value')])
def roi_histogram(year, roi_item):
    if year==2018 and roi_item=='kWh':
        trace0 = go.Bar(
            x=['kWh/CHF_subv', 'kWh/CHF_tot'],
            y=[15, 0.2],
            name = 'NC Minergie',
            opacity= 0.7)

        trace1 = go.Bar(
            x=['kWh/CHF_subv', 'kWh/CHF_tot'],
            y=[17, 0.19],
            name = 'NC Minergie P',
            opacity= 0.7)

        trace2 = go.Bar(
            x=['kWh/CHF_subv', 'kWh/CHF_tot'],
            y=[10, 2],
            name = 'REN Minergie',
            opacity= 0.7)

        trace3 = go.Bar(
            x=['kWh/CHF_subv', 'kWh/CHF_tot'],
            y=[7, 1.5],
            name = 'REN Minergie P',
            opacity= 0.7)

        trace4 = go.Bar(
            x=['kWh/CHF_subv', 'kWh/CHF_tot'],
            y=[6, 1],
            name = 'PAC',
            opacity= 0.7)


        trace5 = go.Bar(
            x=['kWh/CHF_subv', 'kWh/CHF_tot'],
            y=[5, 1.3],
            name = 'Bois',
            opacity= 0.7)

        data = [trace0, trace1, trace2, trace3, trace4, trace5]

    elif year==2018 and roi_item=='CO2':
        
        trace0 = go.Bar(
            x=['t.éq CO2/CHF_subv', 't.éq CO2/CHF_tot'],
            y=[3, 2],
            name = 'NC Minergie',
            opacity= 0.7)

        trace1 = go.Bar(
            x=['t.éq CO2/CHF_subv', 't.éq CO2/CHF_tot'],
            y=[4, 3],
            name = 'NC Minergie P',
            opacity= 0.7)

        trace2 = go.Bar(
            x=['t.éq CO2/CHF_subv', 't.éq CO2/CHF_tot'],
            y=[6, 4],
            name = 'REN Minergie',
            opacity= 0.7)

        trace3 = go.Bar(
            x=['t.éq CO2/CHF_subv', 't.éq CO2/CHF_tot'],
            y=[7, 5],
            name = 'REN Minergie P',
            opacity= 0.7)

        trace4 = go.Bar(
            x=['t.éq CO2/CHF_subv', 't.éq CO2/CHF_tot'],
            y=[6, 8],
            name = 'PAC',
            opacity= 0.7)


        trace5 = go.Bar(
            x=['t.éq CO2/CHF_subv', 't.éq CO2/CHF_tot'],
            y=[13, ],
            name = 'Bois',
            opacity= 0.7)

        data = [trace0, trace1, trace2, trace3, trace4, trace5]

    elif year==2018 and roi_item=='aubaine':

    	trace0 = go.Bar(
            x=['% Aubaine', '% Subventionnement Cant.', '% Subventionnement Com.'],
            y=[66.4, 5, 3],
            name = 'NC Minergie',
            opacity= 0.7)

    	trace1 = go.Bar(
            x=['% Aubaine', '% Subventionnement Cant.', '% Subventionnement Com.'],
            y=[60.1, 7, 3],
            name = 'NC Minergie P',
            opacity= 0.7)

    	trace2 = go.Bar(
            x=['% Aubaine', '% Subventionnement Cant.', '% Subventionnement Com.'],
            y=[4.4, 9, 4],
            name = 'REN Minergie',
            opacity= 0.7)

    	trace3 = go.Bar(
            x=['% Aubaine', '% Subventionnement Cant.', '% Subventionnement Com.'],
            y=[11.3, 11, 8],
            name = 'REN Minergie P',
            opacity= 0.7)

    	trace4 = go.Bar(
            x=['% Aubaine', '% Subventionnement Cant.', '% Subventionnement Com.'],
            y=[20, 20, 10],
            name = 'PAC',
            opacity= 0.7)

    	trace5 = go.Bar(
            x=['% Aubaine', '% Subventionnement Cant.', '% Subventionnement Com.'],
            y=[13.2, 10, 30],
            name = 'Bois',
            opacity= 0.7)

    	data = [trace0, trace1, trace2, trace3, trace4, trace5]


    elif year==2018 and roi_item=='CHF':

    	trace0 = go.Bar(
    		x=['NC Minergie', 'NC Minergie P', 'REN Minergie', 'REN Minergie P', 'PAC', 'Bois'],
    		y=[sum(data_new[data_new['Label']=='Minergie']['BudgetTotal']),
    			 sum(data_new[data_new['Label']=='MinergieP']['BudgetTotal']),
    			 sum(data_ren[data_ren['Label']=='Minergie']['BudgetTotal']),
    			 sum(data_ren[data_ren['Label']=='MinergieP']['BudgetTotal']),
    			 sum(data_cae[data_cae['AgEner_1']=='PAC']['BudgetTotal']),
    			 sum(data_cae[data_cae['AgEner_1']=='Bois']['BudgetTotal'])],
    		name='Technologies',
    		opacity = 0.7)

    	data = [trace0]

    layout = go.Layout(
    	barmode='group', 
    	bargroupgap=0.15, 
    	margin= dict(t= 30, b=30), 
    	showlegend = True,
    	yaxis=dict(
			title=''),
    	yaxis2=dict(
        	title='yaxis2 title',
        	overlaying='y',
        	side='right'
    		)
    	
    )

    figure = dict(data=data, layout=layout)
    return figure

# Indicator graph

@app.callback(
    dash.dependencies.Output('ind_graph','figure'),
    [dash.dependencies.Input('year_slider','value'),
     dash.dependencies.Input('ind_dropdown','value')])
def ind_graph(year, ind):
    if ind == 'conso_elec':
        trace = go.Scatter(
            x=df[df['Année']<=year]['Année'],
            y=df[df['Année']<=year]['Consommation électricité (MWh)'],
            mode='markers+lines',
            opacity = 0.6,
            name='Électricité (en MWh)',
            marker=dict(color='gold'),
            fill='tozeroy')

        trace1 = go.Scatter(
            x=df[df['Année']<=year]['Année'],
            y=9*[25000],
            opacity = 0.7,
            name='Objectifs SE 2050',
            mode='lines',
            marker=dict(color='red'))

        y_axis = 'MWh'
        y_max=df[df['Année']<=year]['Consommation électricité (MWh)'].max()

    
    elif ind == 'conso_chaleur':
        trace  = go.Scatter(
            x=df[df['Année']<=year]['Année'],
            y=df[df['Année']<=year]['Consommation chaleur (MWh)'],
            mode='markers+lines',
            name='Chaleur (en MWh)',
            opacity = 0.5,
            marker=dict(color='black'),
            fill='tozeroy')

        trace1 = go.Scatter(
            x=df[df['Année']<=year]['Année'],
            y=9*[50000],
            opacity = 0.7,
            name='Objectifs SE 2050',
            mode='lines',
            marker=dict(color='red'))

        y_axis = '(MWh)'
        y_max=df[df['Année']<=year]['Consommation chaleur (MWh)'].max()

    elif ind == 'emissions_CO2':
        trace  = go.Scatter(
            x=df[df['Année']<=year]['Année'],
            y=df[df['Année']<=year]['Émissions CO2 (Teq)'],
            mode='markers+lines',
            name='T. éq',
            opacity = 0.5,
            marker=dict(color='drakgrey'),
            fill='tozeroy')

        trace1 = go.Scatter(
            x=df[df['Année']<=year]['Année'],
            y=9*[25000],
            opacity = 0.7,
            name='Objectifs SE 2050',
            mode='lines',
            marker=dict(color='red'))

        y_axis = 't. éq CO2)'
        y_max=df[df['Année']<=year]['Émissions CO2 (Teq)'].max()

    elif ind == 'IDC':
        trace  = go.Scatter(
            x=df[df['Année']<=year]['Année'],
            y=df[df['Année']<=year]['IDC'],
            mode='markers+lines',
            name='IDC',
            opacity = 0.5,
            marker=dict(color='darkgreen'),
            fill='tozeroy')

        trace1 = go.Scatter(
            x=df[df['Année']<=year]['Année'],
            y=9*[180],
            mode='lines',
            name='Objectifs SE 2050',
            opacity = 0.7,
            marker=dict(color='red'))

        y_axis = 'IDC'
        y_max=df[df['Année']<=year]['IDC'].max()

    data = [trace, trace1]
    layout = go.Layout(
        xaxis = {'title':'Année'},
        yaxis = {'title': y_axis, 'autorange': False, 'range' :[1, 1.15*y_max]},
        legend = {'x': 0.6, 'y': 1.2, 'orientation': 'h'},
        margin = {'r': 0}
        )

    figure = dict(data=data, layout=layout)
    return figure


# Table

@app.callback(
    dash.dependencies.Output('datatable1','rows'),
    [dash.dependencies.Input('year_slider','value')])
def update_table1(year):
    table=dff[(dff['Année']==year)|(dff['Année']=='obj')]
    table=table.T
    table.reset_index(inplace=True)
    table.drop(table.index[0], inplace=True)
    table.rename(columns={'index':'Indicateurs','obj': 'Objectifs', 0 :'Résultats 2018', 1: 'Résultats 2017', 2: 'Résultats 2016', 3: 'Résultats 2015', 4: 'Objectifs'}, inplace=True)
    return table.to_dict('records')



if __name__ == '__main__':
    app.run_server()