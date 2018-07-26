import pandas as pd
import ESST_data as data


def update_sre(old_sre, dem_slider):
	
	new_sre = list(old_sre['SRE'])
	
	for i in range(2016, 2051): 
		x = new_sre[-1]*(1+dem_slider/100)
		new_sre.append(x)

	new_sre = new_sre[-35:]
	return new_sre

def update_heatneed(refurbishment_rate, dem_slider, insulation_standards, insulation_standards_ref):
	
	new_heat_need = list(data.old_heat_need)

	for i in range(2016, 2051):

		new_heat_need += [(new_heat_need[-1]*(1-refurbishment_rate/100)+(insulation_standards_ref*refurbishment_rate/100)+(dem_slider*1e-2*insulation_standards))/(1+dem_slider*1e-2)]		
	
	new_heat_need = new_heat_need[-35:]
	return new_heat_need


def update_energy_mix(new_energy_mix):

	energy_mix = data.old_energy_mix.append(new_energy_mix)

	for year in range(2016, 2050):
    
	    x = pd.DataFrame({
	        
	        'year': year,
	        'coal': (energy_mix[energy_mix['year']==year-1]['coal'])+(energy_mix[energy_mix['year']==2050]['coal']-energy_mix[energy_mix['year']==year-1]['coal'])/(2050-2015),
	        'direct_elec': (energy_mix[energy_mix['year']==year-1]['direct_elec'])+(energy_mix[energy_mix['year']==2050]['direct_elec']-energy_mix[energy_mix['year']==2015]['direct_elec'])/(2050-2015),
	        'oil': (energy_mix[energy_mix['year']==year-1]['oil'])+(energy_mix[energy_mix['year']==2050]['oil']-energy_mix[energy_mix['year']==2015]['oil'])/(2050-2015),
	        'gas': (energy_mix[energy_mix['year']==year-1]['gas'])+(energy_mix[energy_mix['year']==2050]['gas']-energy_mix[energy_mix['year']==2015]['gas'])/(2050-2015),
	        'heating_pump': (energy_mix[energy_mix['year']==year-1]['heating_pump'])+(energy_mix[energy_mix['year']==2050]['heating_pump']-energy_mix[energy_mix['year']==2015]['heating_pump'])/(2050-2015),
	        'wood': (energy_mix[energy_mix['year']==year-1]['wood'])+(energy_mix[energy_mix['year']==2050]['wood']-energy_mix[energy_mix['year']==2015]['wood'])/(2050-2015),
	        'thermal': (energy_mix[energy_mix['year']==year-1]['thermal'])+(energy_mix[energy_mix['year']==2050]['thermal']-energy_mix[energy_mix['year']==2015]['thermal'])/(2050-2015),

	    })
	    
	    energy_mix = energy_mix.append(x)

	energy_mix.sort_values('year', inplace=True)
	energy_mix.reset_index(drop=True, inplace=True)
	energy_mix = energy_mix[energy_mix['year']>2015]
	
	return energy_mix

def update_pop(dem_slider, value):
	x = value
	pop = []
	for i in range(2016, 2051):
		x = x*(1+dem_slider*1e-2)
		pop.append(x)
	return pop

