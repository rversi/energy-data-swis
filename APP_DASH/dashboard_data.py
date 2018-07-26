import pandas as pd
import numpy as np

list_egid = range(100)

CO2 = {
    
    "mazout" : 0.301,
    "gaz" : 0.228,
    "e_directe" : 0.063,
    "Bois" : 0.045,
    "PAC" : 0.063,
}

data_ren = pd.DataFrame(columns=["EGID"])

for i, e in enumerate(list_egid[:50]):
    data_ren.loc[i, "EGID"] = "BAT{}".format(int(e))

data_ren["EpConstr"] = np.random.choice(["_1918", "1919_1945", "1946_1960", "1961_1970", "1971_1980", "1981_1985", "1986_1990"], size=50)
data_ren["SRE"] = np.random.uniform(low=100, high=2000, size=50)
data_ren["Affect"] = np.random.choice(['I', 'II', 'III', 'IV', 'V', 'VI', 'XI'], size=50)

data_ren["EffAubaine"] = np.random.choice(["yes", "no"], p=[0.05, 0.95], size=50)
data_ren["PerCentSubMin"] = np.random.normal(loc=0.1, scale=0.015, size=50)

data_ren["AgEner"] = np.random.choice(["mazout", "gaz", "e_direct"], size=50)
data_ren["Label"] = np.random.choice(["Minergie", "MinergieP"], p=[0.75, 0.25], size=50)

data_ren["BudgetTotal"] = np.random.normal(loc=800, scale=10, size=50)*data_ren["SRE"]
data_ren["BudgetTotal"] = data_ren["BudgetTotal"].map(int)

sub_can = {"Minergie": 0.09,
          "MinergieP": 0.11}

sub_com = {"Minergie": 0.04,
          "MinergieP": 0.08}

data_ren['BudgetSubCan'] = data_ren['BudgetTotal'].map(int)
data_ren['BudgetSubCom'] = data_ren['BudgetTotal'].map(int)

for i in data_ren.index:
    data_ren.at[i, 'BudgetSubCan'] *= sub_can['MinergieP'] if [data_ren['Label']=="MinergieP"] else data_ren["BudgetSubCan"][i]*sub_can['MinergieP']
    data_ren.at[i, 'BudgetSubCom'] *= sub_com['MinergieP'] if [data_ren['Label']=="MinergieP"] else data_ren["BudgetSubCom"][i]*sub_com['MinergieP']

data_ren["BudgetSubCan"] = data_ren["BudgetSubCan"].map(lambda x: min(20000, x))
data_ren["BudgetSubCom"] = data_ren["BudgetSubCom"].map(lambda x: min(10000, x))
data_ren["BudgetPrivate"] = data_ren["BudgetTotal"] - data_ren["BudgetSubCan"] - data_ren["BudgetSubCom"]


data_ren["IdProjet"] = data_ren["EGID"] + "-REN"
data_ren.reset_index(inplace=True, drop=True)

data_new = pd.DataFrame(columns=["EGID"])

for i, e in enumerate(list_egid[-20:]):
    data_new.loc[i, "EGID"] = "BAT{}".format(int(e))

data_new["EpConstr"] = np.random.choice(range(2000, 2018), size=20)
data_new["SRE"] = np.random.uniform(low=100, high=2000, size=20)
data_new["Alloc"] = np.random.choice(range(1, 12), size=20)

data_new["EffAubaine"] = np.random.choice(["yes", "no"], p=[0.6, 0.4], size=20)
data_new["PerCentSubMin"] = np.random.normal(loc=0.05, scale=0.002, size=20)

data_new["AgEner"] = np.random.choice(["PAC", "Bois"], size=20)

data_new["Label"] = np.random.choice(["Minergie", "MinergieP"], p=[0.6, 0.4], size=20)

data_new["BudgetTotal"] = np.random.normal(loc=3500, scale=200, size=20)*data_new["SRE"]
data_new["BudgetTotal"] = data_new["BudgetTotal"].map(int)

sub_can = {"Minergie": 0.08,
          "MinergieP": 0.10}

sub_com = {"Minergie": 0.03,
          "MinergieP": 0.06}

data_new['BudgetSubCan'] = data_new['BudgetTotal'].map(int)
data_new['BudgetSubCom'] = data_new['BudgetTotal'].map(int)

for i in data_new.index:
    data_new.at[i, 'BudgetSubCan'] *= sub_can['MinergieP'] if [data_new['Label']=="MinergieP"] else data_new["BudgetSubCan"][i]*sub_can['MinergieP']
    data_new.at[i, 'BudgetSubCom'] *= sub_com['MinergieP'] if [data_new['Label']=="MinergieP"] else data_new["BudgetSubCom"][i]*sub_com['MinergieP']

data_new["BudgetSubCan"] = data_new["BudgetSubCan"].map(lambda x: min(50000, x))
data_new["BudgetSubCom"] = data_new["BudgetSubCom"].map(lambda x: min(20000, x))
data_new["BudgetPrivate"] = data_new["BudgetTotal"] - data_new["BudgetSubCan"] - data_new["BudgetSubCom"]

data_new["IdProjet"] = data_new["EGID"] + "-NC"

data_new["kWhEco"] = data_new["SRE"]

for i in data_new.index:
    data_new.at[i, "kWhEco"] *= 15 if [data_new['Label']=="MinergieP"] else 5

data_new["kgCO2Eco"] = data_new["kWhEco"]

for i in data_new.index:
    data_new.at[i, "kgCO2Eco"] *= CO2[data_new.at[i, "AgEner"]]

data_new.reset_index(inplace=True, drop=True)


list_idx_cae = np.random.choice(data_ren.index, size=20)

data_cae = data_ren.loc[list_idx_cae, ["EGID", "EpConstr", "SRE", "Alloc"]]

data_cae2 = pd.DataFrame(columns=["EGID"])
for i, e in enumerate(list_egid[50:80]):
    data_cae2.loc[i, "EGID"] = "BAT{}".format(int(e))

data_cae2["EpConstr"] = np.random.choice(range(1930, 2000), size=30)
data_cae2["SRE"] = np.random.uniform(low=100, high=2000, size=30)
data_cae2["Alloc"] = np.random.choice(range(1, 12), size=30)

data_cae = pd.concat([data_cae, data_cae2])
data_cae = data_cae.reindex()

data_cae["EffAubaine"] = np.random.choice(["yes", "no"], p=[0.2, 0.8], size=50)
data_cae["PerCentSubMin"] = np.random.normal(loc=0.2, scale=0.05, size=50)

data_cae["AgEner_0"] = np.random.choice(["mazout", "gaz", "e_direct"], size=50)
data_cae["AgEner_1"] = np.random.choice(["PAC", "Bois"], size=50)

data_cae["BudgetTotal"] = np.random.normal(loc=80, scale=2, size=50)*data_cae["SRE"]
data_cae["BudgetTotal"] = data_cae["BudgetTotal"].map(int)
data_cae.reset_index(inplace=True, drop=True)


change = [(u[0], u[1]) for u in np.array(np.meshgrid(
    ["mazout", "gaz", "e_direct"], 
    ["PAC", "Bois"])).T.reshape(-1,2)]
change

sub_can = {t: (0.20 if t[1] == "PAC" else 0.1) for t in change}

sub_com = {t: (0.30 if t[1] == "Bois" else 0.1) for t in change}

data_cae["BudgetSubCan"] = [sub_can[(row[6], row[7])]*row[8] for _, row in data_cae.iterrows()]
data_cae["BudgetSubCom"] = [sub_com[(row[6], row[7])]*row[8] for _, row in data_cae.iterrows()]

data_cae["BudgetSubCan"] = data_cae["BudgetSubCan"].map(lambda x: min(5000, x))
data_cae["BudgetSubCom"] = data_cae["BudgetSubCom"].map(lambda x: min(5000, x))
data_cae["BudgetPrivate"] = data_cae["BudgetTotal"] - data_cae["BudgetSubCan"] - data_cae["BudgetSubCom"]

data_cae["IdProjet"] = data_cae["EGID"] + "-CAE"

data_cae.reset_index(inplace=True, drop=True)
