import os
import pandas as pd


# SRE Suisse 2000 - 2015
dem = 1.01
year = list(range(2000,2016))
sre = [0.75*357e6]*16 # Initialisation année 2000 

for i in range(16):
    sre[i] *= dem**i #  

old_sre = pd.DataFrame({'Année': year, 'SRE': sre}) # en m²

#  Données de consommation (TJ)

city_cons = pd.read_excel(os.path.join('../RAW_DATA/data_educative_app.xlsx'))
city_cons = city_cons[city_cons['Secteur']=='Chauffage et autres'].loc[:,['Agent Énergétique', 'Année', 'Consommation (TJ)']]
city_cons = city_cons[city_cons['Consommation (TJ)']!=0]
city_cons.reset_index(drop=True, inplace=True)

#  Correction Degré.jour sur Genève (année référence = 2000)

deg_jour = pd.read_excel(os.path.join('../RAW_DATA/degré.jour_geneve.xlsx'))
deg_jour = deg_jour[deg_jour['Année']>1999]
city_cons = pd.merge(city_cons, deg_jour)
city_cons['Consommation corrigée (TJ)'] = (city_cons['Consommation (TJ)']/city_cons['Degré.jour'])*2238



coal_cons = city_cons[city_cons['Agent Énergétique']=='Charbon']['Consommation corrigée (TJ)']
coal_cons.reset_index(drop=True, inplace=True)

oil_cons =city_cons[city_cons['Agent Énergétique']=='Huile de chauffage extra-légère']['Consommation corrigée (TJ)']
oil_cons.reset_index(drop=True, inplace=True)

gas_cons  = city_cons[city_cons['Agent Énergétique']=='Gaz naturel']['Consommation corrigée (TJ)']
gas_cons.reset_index(drop=True, inplace=True)

elec_cons  = city_cons[city_cons['Agent Énergétique']=='Electricité']['Consommation corrigée (TJ)']
elec_cons.reset_index(drop=True, inplace=True)
elec_cons = elec_cons - 22*(3600/1e9)*old_sre['SRE']  # Retrait de la consommation d'électrcité non liée au Chauffage (selon SIA)


# Répartition de la consommation d'électricité acteulle liée au Chauffage, entre PAC et élec directe

heat_pump_cons = 0.25*elec_cons
direct_elec_cons = 0.75*elec_cons

district_heating_cons  = city_cons[city_cons['Agent Énergétique']=='Chaleur à distance']['Consommation corrigée (TJ)']
district_heating_cons.reset_index(drop=True, inplace=True)

wood_cons  = city_cons[city_cons['Agent Énergétique']=='Bois et charbon de bois']['Consommation corrigée (TJ)']
wood_cons.reset_index(drop=True, inplace=True)

thermal_cons  = city_cons[city_cons['Agent Énergétique']=='Géothermie, chaleur ambiante et énergie solaire thermique']['Consommation corrigée (TJ)']
thermal_cons.reset_index(drop=True, inplace=True)

total_cons = city_cons[city_cons['Agent Énergétique']=='Tous les agents énergétiques']['Consommation corrigée (TJ)']
total_cons.reset_index(drop=True, inplace=True)
total_cons = total_cons - 22*(3600/1e9)*old_sre['SRE'] - district_heating_cons  # Suppression 

old_idc = 1e6*total_cons / old_sre['SRE'] # en MJ/m²


# Mix énergétique en 2015

old_energy_mix = pd.DataFrame({
    
    'year' : [2015],
    'coal' : coal_cons.iloc[-1]/total_cons.iloc[-1],
    'oil' : oil_cons.iloc[-1]/total_cons.iloc[-1],
    'gas' : gas_cons.iloc[-1]/total_cons.iloc[-1],
    'direct_elec' : direct_elec_cons.iloc[-1]/total_cons.iloc[-1],
    'heating_pump' : heat_pump_cons.iloc[-1]/total_cons.iloc[-1],
    'wood' : wood_cons.iloc[-1]/total_cons.iloc[-1],
    'thermal' : thermal_cons.iloc[-1]/total_cons.iloc[-1]

})


# Rendement des technologies valeurs SIA Société 2000W

efficiency = {

	'coal': 0.5,
	'oil': 0.85,
	'gas': 0.9,
	'direct_elec': 1,
	'heating_pump': 2.5,
	'wood': 0.75,
	'thermal': 1
}


CO2_emissions = {

    'coal': 0.450/3.6e3,
    'oil': 0.301/3.6e3,
    'gas': 0.228/3.6e3,
    'direct_elec': 0.063/3.6e3,
    'heating_pump': 0.063/3.6e3,
    'wood': 0.050/3.6e3,
    'thermal': 0.030/3.6e3
}

# Émissions de CO2 2000 - 2015

city_emissions = pd.read_excel(os.path.join('../RAW_DATA/CO2-emissions.xlsx'), sheetname = 'Tous les GES par secteur CO2-V', skipfooter = 10)
city_emissions = pd.DataFrame({
    'Année': list(range(2000, 2016)),
    'Emissions': city_emissions.iloc[12:,0]
})

city_emissions.reset_index(drop=True, inplace=True)
city_emissions = pd.merge(city_emissions, deg_jour)
city_emissions['Emissions corrigée (M. Téq)'] = city_emissions['Emissions']/city_emissions['Degré.jour']*2238

# Évolution démographique 2000 - 2015

population = pd.read_excel(os.path.join('../RAW_DATA/OFS/Données démographie suisse.xlsx'), sheetname = 'Population')
population = population.T
population.drop(population.index[0],inplace=True)
population.columns=['Population']


global_eff = float(sum(efficiency[k]*old_energy_mix[k] for k in efficiency))
old_heat_need = 1e6*total_cons/(global_eff*old_sre['SRE'])  #   MJ/m²





