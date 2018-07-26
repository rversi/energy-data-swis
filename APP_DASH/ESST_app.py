import os
import pandas as pd 
import numpy as np 
import plotly.graph_objs as go 
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt


import ESST_model as model
import ESST_data as data

# Importation des données de consommation 

city_cons = data.city_cons

coal_cons = data.coal_cons
oil_cons = data.oil_cons
gas_cons = data.gas_cons
direct_elec_cons = data.direct_elec_cons
heat_pump_cons = data.heat_pump_cons
wood_cons = data.wood_cons
thermal_cons = data.thermal_cons




city_emissions = list(data.city_emissions['Emissions corrigée (M. Téq)'])
CO2_emissions = data.CO2_emissions
old_sre = data.old_sre
population = list(data.population['Population'])
year = list(range(2000,2051))

efficiency = data.efficiency
global_eff = data.global_eff

app = dash.Dash()


# Templates importation

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/62f0eb4f1fadbefea64b2404493079bf848974e8/dash-uber-ride-demo.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

# App Breakdown Structure

app.layout = html.Div([

	html.H1([
		'Quelle politique énergétique mener pour réaliser les objectifs de la SE 2050 ?'
		], style = {'textAlign': 'center', 'color': 'black', 'fontSize': 24, 'marginTop': 20, 'marginBottom': 40}),

# First column : Parameters input	

	html.Div([

		html.Div([

			html.H2([
				'PARAMÈTRES'
				], style = {'textAlign': 'center', 'color': 'black', 'fontSize': 20,  'marginBottom': 20, 'backgroundColor': 'peachpuff'})

			]),

			html.Div([

			
				html.H6([
				'Évolution démographique (en %)'
				], style = {'fontSize': 14, 'marginBottom': 5}),

				dcc.Slider(
				id = 'dem_slider',
				min = -1,
				max = 3,
				value = 1,
				step = 0.5,
				marks = {str(i): str(i) for i in range(-1, 4, 1)})

			], style = {'width': '95%','marginBottom': 50}),

		
		html.Div([

			html.H6([
				'Nouvelles Constructions'
				], style = {'textAlign': 'center', 'fontSize': 16, 'marginBottom': 10, 'backgroundColor': 'whitesmoke'}),

			html.Div([

				html.H6([
					'Normes d\'isolation'
					], style = {'fontSize': 14, 'marginBottom': 5}),

				dcc.RadioItems(
					id = 'insulation_standards',
					options=[{'label': 'Norme SIA  ', 'value': 190},
	                         {'label': 'Minergie  ', 'value': 3.6*38},
	                         {'label': 'Minergie P  ', 'value': 3.6*30},
	                         {'label': 'Minergie A  ', 'value': 0}],
	                value= 190,
	                labelStyle = {'textAlign': 'center', 'display': 'inline-block', 'fontSize': 14},
	                style = {'textAlign': 'center'}
	           	),

	           	html.H6([
	           		'Part d\'énergie renouvelable (en %)'
	           		], style = {'fontSize': 14, 'marginBottom': 5}),

	           	dcc.Slider(
	           		id = 'renewable_rate_nc',
	           		min = 0,
	           		max = 100,
	           		value = 20,
	           		step = 10,
	           		marks = {str(i): str(i) for i in range(0, 101, 20)})
        	
	        ], style = {'width': '95%', 'marginBottom': 50})
        ]),

        html.Div([

			html.H6([
				'Rénovations'
				], style = {'textAlign': 'center', 'fontSize': 16, 'marginBottom': 10, 'backgroundColor': 'whitesmoke'}
				),

			html.Div([

				html.H6([
			        'Taux d\'assainissement (en %)'
			        ], style = {'fontSize': 14, 'marginBottom': 5}
			        ),

			    dcc.Slider(
			        id = 'refurbishment_rate',
			        min = 0,
			        max = 2,
			        value = 1,
			        step = 0.25,
			        marks = {str(i): str(i) for i in list([0, 0.5, 1, 1.5, 2])}
			        ),
						

				html.H6([
					'Normes de rénovation'
					], style = {'fontSize': 14, 'marginTop': 30, 'marginBottom': 5}
					),

				dcc.RadioItems(
					id = 'insulation_standards_ref',
					options=[{'label': 'Norme SIA  ', 'value': 1.25*190},
			                 {'label': 'Minergie  ', 'value': 3.6*1.25*38},
			                 {'label': 'Minergie P  ', 'value': 3.6*1.25*30},
			                 {'label': 'Minergie A  ', 'value': 0}],
			        value= 1.25*190,
			        labelStyle = {'textAlign': 'center', 'display': 'inline-block', 'fontSize': 14},
			        style = {'textAlign': 'center'}
			        ),

			    html.H6([
			        'Part d\'énergie renouvelable (en %)'
			        ], style = {'fontSize': 14, 'marginBottom': 5}
			        ),

			    dcc.Slider(
			        id = 'renewable_rate_ref',
			        min = 0,
			        max = 100,
			        value = 20,
			        step = 10,
			        marks = {str(i): str(i) for i in range(0, 101, 20)})
		        	
			], style = {'width': '95%', 'marginBottom': 50})
        ]),

        html.Div([

        	html.H6([
				'Mix Énergétique'
				], style = {'textAlign': 'center', 'fontSize': 16, 'marginBottom': 10, 'backgroundColor': 'whitesmoke'}
			),

			html.H6([
			        'Part de Mazout (en %)'
			        ], style = {'fontSize': 14, 'marginBottom': 5}
			        ),

			dcc.Slider(
			        id = 'oil',
			        min = 0,
			        max = 100,
			        value = 40,
			        step = 5,
			        marks = {str(i): str(i) for i in range(0, 101, 10)}
			    ),

			html.H6([
			        'Part de Gaz (en %)'
			        ], style = {'fontSize': 14, 'marginTop': 30, 'marginBottom': 5}
			        ),

			dcc.Slider(
			        id = 'gas',
			        min = 0,
			        max = 100,
			        value = 25,
			        step = 5,
			        marks = {str(i): str(i) for i in range(0, 101, 10)}
			    ),

			html.H6([
			        'Part d\'Électricité Directe (en %)'
			        ], style = {'fontSize': 14, 'marginTop': 30, 'marginBottom': 5}
			        ),

			dcc.Slider(
			        id = 'direct_elec',
			        min = 0,
			        max = 100,
			        value = 15,
			        step = 5,
			        marks = {str(i): str(i) for i in range(0, 101, 10)}
			    ),


			html.H6([
			        'Part de PAC (en %)'
			        ], style = {'fontSize': 14, 'marginTop': 30, 'marginBottom': 5}
			        ),

			dcc.Slider(
			        id = 'heating_pump',
			        min = 0,
			        max = 100,
			        value = 10,
			        step = 5,
			        marks = {str(i): str(i) for i in range(0, 101, 10)}
			    ),

			html.H6([
			        'Part de Bois (en %)'
			        ], style = {'fontSize': 14, 'marginTop': 30, 'marginBottom': 5}
			        ),

			dcc.Slider(
			        id = 'wood',
			        min = 0,
			        max = 100,
			        value = 5,
			        step = 5,
			        marks = {str(i): str(i) for i in range(0, 101, 10)}
			    ),

			html.H6([
			        'Part de Solaire (PV&TH) (en %)'
			        ], style = {'fontSize': 14, 'marginTop': 30, 'marginBottom': 5}
			        ),

			dcc.Slider(
			        id = 'thermal',
			        min = 0,
			        max = 100,
			        value = 5,
			        step = 5,
			        marks = {str(i): str(i) for i in range(0, 101, 10)}
			    )
        ], style = {'width': '95%', 'marginBottom': 50})


	], style = {'width': '23%', 'display': 'inline-block', 'vertical-align': 'top', 'marginLeft': 15}),

# Second column : Diplay of the results

	html.Div([

		html.Div([

			html.H2([
				'IMPACT SUR LA CONSOMMATION D\'ÉNERGIE PRIMAIRE'
				], style = {'fontSize': 20, 'textAlign': 'center', 'marginBottom': 10, 'marginLeft': 60, 'backgroundColor': 'peachpuff'}),

			dcc.Graph(
				id = 'energy_consumption',
				style = {'marginTop': 0},
				animate = True
				)

			]),

		html.Div([

			html.H2([
				'IMPACT SUR LES ÉMISSIONS DE CO2'
				], style = {'fontSize': 20, 'textAlign': 'center', 'marginLeft': 60, 'backgroundColor': 'peachpuff'}),

			dcc.Graph(
				id = 'co2_emissions',
				animate = True
				)


			])

	], style = {'width': '75%', 'display': 'inline-block', 'vertical-align': 'top'})

])


@app.callback(
    dash.dependencies.Output('energy_consumption', 'figure'),
    [dash.dependencies.Input('dem_slider', 'value'),
     dash.dependencies.Input('insulation_standards', 'value'),
     #dash.dependencies.Input('renewable_rate_nc', 'value'),
     dash.dependencies.Input('refurbishment_rate', 'value'),
     dash.dependencies.Input('insulation_standards_ref', 'value'),
     #dash.dependencies.Input('renewable_rate_ref', 'value'),
     dash.dependencies.Input('oil', 'value'),
     dash.dependencies.Input('gas', 'value'),
     dash.dependencies.Input('direct_elec', 'value'),
     dash.dependencies.Input('heating_pump', 'value'),
     dash.dependencies.Input('wood', 'value'),
     dash.dependencies.Input('thermal', 'value')])
def update_graph_conso(dem_slider, insulation_standards, refurbishment_rate, insulation_standards_ref, oil, gas, direct_elec, heating_pump, wood, thermal):

	new_energy_mix = pd.DataFrame({

	    'year': [2050], 
	    'coal' : 0,
	    'oil': 0.01*oil, 
	    'gas': 0.01*gas,
	   	'direct_elec' : 0.01*direct_elec, 
	    'heating_pump': 0.01*heating_pump, 
	    'wood': 0.01*wood, 
	    'thermal': 0.01*thermal

	})

	new_sre = model.update_sre(old_sre, dem_slider)

	new_heat_need = model.update_heatneed(refurbishment_rate, dem_slider, insulation_standards, insulation_standards_ref)

	energy_mix = model.update_energy_mix(new_energy_mix)
	new_population = model.update_pop(dem_slider, population[-1])
	consumption_SE2050 = list((514)*3600*24*365*1e3*item*1e-12 for item in (population+new_population))  # 514 W représente la valeur cible de la société à 2000W à l'horizon 2050 cf. SIA 2000W
	
	y1 = list(coal_cons)
	y2 = list(coal_cons+oil_cons for coal_cons, oil_cons in zip(coal_cons, oil_cons))
	y3 = list(coal_cons+oil_cons+gas_cons for coal_cons, oil_cons, gas_cons in zip(coal_cons, oil_cons, gas_cons))
	y4 = list(coal_cons+oil_cons+gas_cons+2.9*direct_elec_cons for coal_cons, oil_cons, gas_cons, direct_elec_cons in zip(coal_cons, oil_cons, gas_cons, direct_elec_cons))
	y5 = list(coal_cons+oil_cons+gas_cons+2.9*direct_elec_cons+2.9*heat_pump_cons for coal_cons, oil_cons, gas_cons, direct_elec_cons, heat_pump_cons in zip(coal_cons, oil_cons, gas_cons, direct_elec_cons, heat_pump_cons))
	y6 = list(coal_cons+oil_cons+gas_cons+2.9*direct_elec_cons+2.9*heat_pump_cons+wood_cons for coal_cons, oil_cons, gas_cons, direct_elec_cons, heat_pump_cons, wood_cons in zip(coal_cons, oil_cons, gas_cons, direct_elec_cons, heat_pump_cons, wood_cons))
	y7 = list(coal_cons+oil_cons+gas_cons+2.9*direct_elec_cons+2.9*heat_pump_cons+wood_cons+thermal_cons for coal_cons, oil_cons, gas_cons, direct_elec_cons, heat_pump_cons, wood_cons, thermal_cons in zip(coal_cons, oil_cons, gas_cons, direct_elec_cons, heat_pump_cons, wood_cons, thermal_cons))

	
	updated_coal_cons = list(1e-6*np.asarray(new_sre)*np.asarray(new_heat_need)*energy_mix['coal']/efficiency['coal'])
	updated_coal_cons= np.random.normal(loc=1, scale=0.03, size=35)*np.asanyarray(updated_coal_cons)	
	updated_oil_cons = list(1e-6*np.asarray(new_sre)*np.asarray(new_heat_need)*energy_mix['oil']/efficiency['oil'])
	updated_oil_cons = np.random.normal(loc=1, scale=0.03, size=35)*np.asanyarray(updated_oil_cons)
	updated_gas_cons = list(1e-6*np.asarray(new_sre)*np.asarray(new_heat_need)*energy_mix['gas']/efficiency['gas'])
	updated_gas_cons = np.random.normal(loc=1, scale=0.03, size=35)*np.asanyarray(updated_gas_cons)
	updated_direct_elec_cons = list(1e-6*np.asarray(new_sre)*np.asarray(new_heat_need)*energy_mix['direct_elec']/efficiency['direct_elec'])
	updated_direct_elec_cons = np.random.normal(loc=1, scale=0.03, size=35)*np.asanyarray(updated_direct_elec_cons)
	updated_heat_pump_cons = list(1e-6*np.asarray(new_sre)*np.asarray(new_heat_need)*energy_mix['heating_pump']/efficiency['heating_pump'])
	updated_heat_pump_cons = np.random.normal(loc=1, scale=0.03, size=35)*np.asanyarray(updated_heat_pump_cons)
	updated_wood_cons = list(1e-6*np.asarray(new_sre)*np.asarray(new_heat_need)*energy_mix['wood']/efficiency['wood'])
	updated_wood_cons = np.random.normal(loc=1, scale=0.03, size=35)*np.asanyarray(updated_wood_cons)
	updated_thermal_cons = list(1e-6*np.asarray(new_sre)*np.asarray(new_heat_need)*energy_mix['thermal']/efficiency['thermal'])
	updated_thermal_cons = np.random.normal(loc=1, scale=0.03, size=35)*np.asanyarray(updated_thermal_cons)

	
	y11 = list(updated_coal_cons)
	y21 = list(updated_coal_cons+updated_oil_cons for updated_coal_cons, updated_oil_cons in zip(updated_coal_cons, updated_oil_cons))
	y31 = list(updated_coal_cons+updated_oil_cons+updated_gas_cons for updated_coal_cons, updated_oil_cons, updated_gas_cons in zip(updated_coal_cons, updated_oil_cons, updated_gas_cons))
	y41 = list(updated_coal_cons+updated_oil_cons+updated_gas_cons+2.9*updated_direct_elec_cons for updated_coal_cons, updated_oil_cons, updated_gas_cons, updated_direct_elec_cons in zip(updated_coal_cons, updated_oil_cons, updated_gas_cons, updated_direct_elec_cons))
	y51 = list(updated_coal_cons+updated_oil_cons+updated_gas_cons+2.9*updated_direct_elec_cons+2.9*updated_heat_pump_cons for updated_coal_cons, updated_oil_cons, updated_gas_cons, updated_direct_elec_cons, updated_heat_pump_cons in zip(updated_coal_cons, updated_oil_cons, updated_gas_cons, updated_direct_elec_cons, updated_heat_pump_cons))
	y61 = list(updated_coal_cons+updated_oil_cons+updated_gas_cons+2.9*updated_direct_elec_cons+2.9*updated_heat_pump_cons+updated_wood_cons for updated_coal_cons, updated_oil_cons, updated_gas_cons, updated_direct_elec_cons, updated_heat_pump_cons, updated_wood_cons in zip(updated_coal_cons, updated_oil_cons, updated_gas_cons, updated_direct_elec_cons, updated_heat_pump_cons, updated_wood_cons))
	y71 = list(updated_coal_cons+updated_oil_cons+updated_gas_cons+2.9*updated_direct_elec_cons+2.9*updated_heat_pump_cons+updated_wood_cons+updated_thermal_cons for updated_coal_cons, updated_oil_cons, updated_gas_cons, updated_direct_elec_cons, updated_heat_pump_cons, updated_wood_cons, updated_thermal_cons in zip(updated_coal_cons, updated_oil_cons, updated_gas_cons, updated_direct_elec_cons, updated_heat_pump_cons, updated_wood_cons, updated_thermal_cons))

	coal = go.Scatter(
	    x = year,
	    y = y1+y11,
	    mode = 'lines',
	    line = dict(width = 0.2),
	    name = 'Charbon',
	    fill = 'tozeroy'
	)

	oil = go.Scatter(
	    x = year,
	    y = y2+y21,
	    mode = 'lines',
	    line = dict(width = 0.2, color = 'rgb(100,100,100)'),
	    name = 'Mazout',
	    fill = 'tonexty'
	)

	gas = go.Scatter(
	    x = year,
	    y = y3+y31,
	    mode = 'lines',
	    line = dict(width = 0.2, color = 'rgb(200,200,200)'),
	    name = 'Gaz',
	    fill = 'tonexty'
	)

	direct_elec = go.Scatter(
	    x = year,
	    y = y4+y41,
	    mode = 'lines',
	    line = dict(width = 0.2, color = '#F6F60F'),
	    name = 'Électricité directe',
	    fill = 'tonexty'
	)

	heating_pump = go.Scatter(
	    x = year,
	    y = y5+y51,
	    mode = 'lines',
	    line = dict(width = 0.2),
	    name = 'PAC',
	    fill = 'tonexty'
	)

	wood = go.Scatter(
	    x = year,
	    y = y6+y61,
	    mode = 'lines',
	    line = dict(width = 0.2, color = '#B26633'),
	    name = 'Bois',
	    fill = 'tonexty'
	)

	thermal = go.Scatter(
	    x = year,
	    y = y7+y71,
	    mode = 'lines',
	    line = dict(width = 0.2, color = '#50BD4D'),
	    name = 'Renouvelables',
	    fill = 'tonexty'
	)

	cons_target = go.Scatter(
	    x = year,
	    y = consumption_SE2050,
	    mode = 'lines',
	    line = dict(width = 1.5, color = 'red'),
	    name = 'SE 2050'
	)


	layout = go.Layout(
	    legend = dict(x = 1.1, y=0.25),
	    xaxis = dict(range=[2001, 2051]),
	    yaxis = dict(title = 'Consommation énergie primaire (TJ)', range=[0, 1.15*max(y71)]),
	    margin = dict(t=20, l=100)
	)

	data = [coal, oil, gas, direct_elec, heating_pump, wood, thermal, cons_target]
	figure = dict(data = data, layout = layout)
	return figure

	print(global_eff)

@app.callback(
    dash.dependencies.Output('co2_emissions','figure'),
    [dash.dependencies.Input('dem_slider','value'),
     dash.dependencies.Input('insulation_standards','value'),
     #dash.dependencies.Input('renewable_rate_nc','value'),
     dash.dependencies.Input('insulation_standards_ref','value'),
     #dash.dependencies.Input('renewable_rate_ref','value'),
     dash.dependencies.Input('refurbishment_rate','value'),
     dash.dependencies.Input('oil', 'value'),
     dash.dependencies.Input('gas', 'value'),
     dash.dependencies.Input('direct_elec', 'value'),
     dash.dependencies.Input('heating_pump', 'value'),
     dash.dependencies.Input('wood', 'value'),
     dash.dependencies.Input('thermal', 'value')])
def update_graph_emission(dem_slider, insulation_standards, insulation_standards_ref, refurbishment_rate, oil, gas, direct_elec, heating_pump, wood, thermal):

	new_energy_mix = pd.DataFrame({

	    'year': [2050], 
	    'coal' : 0,
	    'oil': 0.01*oil, 
	    'gas': 0.01*gas,
	   	'direct_elec' : 0.01*direct_elec, 
	    'heating_pump': 0.01*heating_pump, 
	    'wood': 0.01*wood, 
	    'thermal': 0.01*thermal

	})

	new_sre = model.update_sre(old_sre, dem_slider)

	new_heat_need = model.update_heatneed(refurbishment_rate, dem_slider, insulation_standards, insulation_standards_ref)

	energy_mix = model.update_energy_mix(new_energy_mix)

	updated_coal_cons = list(1e-6*np.asarray(new_sre)*np.asarray(new_heat_need)*energy_mix['coal']/efficiency['coal'])
	updated_oil_cons = list(1e-6*np.asarray(new_sre)*np.asarray(new_heat_need)*energy_mix['oil']/efficiency['oil'])
	updated_gas_cons = list(1e-6*np.asarray(new_sre)*np.asarray(new_heat_need)*energy_mix['gas']/efficiency['gas'])
	updated_direct_elec_cons = list(1e-6*np.asarray(new_sre)*np.asarray(new_heat_need)*energy_mix['direct_elec']/efficiency['direct_elec'])
	updated_heat_pump_cons = list(1e-6*np.asarray(new_sre)*np.asarray(new_heat_need)*energy_mix['heating_pump']/efficiency['heating_pump'])
	updated_wood_cons = list(1e-6*np.asarray(new_sre)*np.asarray(new_heat_need)*energy_mix['wood']/efficiency['wood'])
	updated_thermal_cons = list(1e-6*np.asarray(new_sre)*np.asarray(new_heat_need)*energy_mix['thermal']/efficiency['thermal'])

	total_cons = list(updated_coal_cons+updated_oil_cons+updated_gas_cons+updated_direct_elec_cons+updated_heat_pump_cons+updated_wood_cons+updated_thermal_cons for updated_coal_cons, updated_oil_cons, updated_gas_cons, updated_direct_elec_cons, updated_heat_pump_cons, updated_wood_cons, updated_thermal_cons in zip(updated_coal_cons, updated_oil_cons, updated_gas_cons, updated_direct_elec_cons, updated_heat_pump_cons, updated_wood_cons, updated_thermal_cons))

	co2_mix = pd.DataFrame({
    
    'coal': energy_mix['coal']*CO2_emissions['coal'],
    'oil': energy_mix['oil']*CO2_emissions['oil'],
    'gas': energy_mix['gas']*CO2_emissions['gas'],
    'direct_elec': energy_mix['direct_elec']*CO2_emissions['direct_elec'],
    'heating_pump': energy_mix['heating_pump']*CO2_emissions['heating_pump'],
    'wood': energy_mix['wood']*CO2_emissions['wood'],
    'thermal': energy_mix['thermal']*CO2_emissions['thermal']
    
	})

	updated_emissions = list(co2_mix.sum(axis=1)*total_cons)
	updated_emissions = list(np.random.normal(loc=1, scale=0.03, size=35)*np.asanyarray(updated_emissions))

	new_population = model.update_pop(dem_slider, population[-1])
	emissions_SE2050 = list(0.5*item*1e-3 for item in (population+new_population))

	emis = go.Scatter(
		x = year,
		y = city_emissions + updated_emissions,
		mode = 'lines',
		line = dict(width = 0.5, color = 'rgb(0,0,0)'),
		name = 'Émissions de CO2',
		fill = 'tozeroy'
		)

	emis_target = go.Scatter(
		x = year,
		y = emissions_SE2050,
		mode = 'lines',
		line = dict(width = 1.5, color = 'red'),
		name = 'Objectif SE 2050'
		)

	layout = go.Layout(
		margin = dict(t=20, l=100),
		yaxis = {'title': 'Millions de t.eq CO2', 'range':[0, 1.15*max(city_emissions)]},
		xaxis = dict(range = [2001, 2051])
		)

	data = [emis, emis_target]
	figure = dict(data = data, layout = layout)
	return figure


if __name__ == '__main__':
    app.run_server(port=8051)

