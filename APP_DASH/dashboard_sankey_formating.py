import pandas as pd
import dashboard_data as data

data_cae = data.data_cae
data_new = data.data_new
data_ren = data.data_ren

#nodes = [["total_CAE", "total_NEW", "total_REN"], ["private", "canton", "commune"], ["useful", "dead_weight"], ['bois', 'PAC', 'NC Minergie', 'NC MinergieP', 'REN Minergie', 'REN MinergieP']]
nodes = [[0, 1, 2], [3, 4, 5], [6, 7], [8, 9, 10, 11, 12, 13]]

flows = []

for _, row in data_cae.iterrows():
    flows.append({"SRC": nodes[0][0], "TAR":nodes[1][0], "VAL": row["BudgetPrivate"], "LAB": row['IdProjet']})
    flows.append({"SRC": nodes[0][0], "TAR":nodes[1][1], "VAL": row["BudgetSubCan"], "LAB": row['IdProjet']})
    flows.append({"SRC": nodes[0][0], "TAR":nodes[1][2], "VAL": row["BudgetSubCom"], "LAB": row['IdProjet']})
    
    if row["EffAubaine"] == "no":
        flows.append({"SRC": nodes[1][0], "TAR":nodes[2][0], "VAL": row["BudgetPrivate"], "LAB": row['IdProjet']})
        flows.append({"SRC": nodes[1][1], "TAR":nodes[2][0], "VAL": row["BudgetSubCan"], "LAB": row['IdProjet']})
        flows.append({"SRC": nodes[1][2], "TAR":nodes[2][0], "VAL": row["BudgetSubCom"], "LAB": row['IdProjet']})
    
        if row['AgEner_1'] == 'Bois':
            flows.append({"SRC": nodes[2][0], "TAR":nodes[3][0], "VAL": row["BudgetTotal"], "LAB": row['IdProjet']})
        
        if row['AgEner_1'] == 'PAC':
            flows.append({"SRC": nodes[2][0], "TAR":nodes[3][1], "VAL": row["BudgetTotal"], "LAB": row['IdProjet']})
        
    if row["EffAubaine"] == "yes":
        flows.append({"SRC": nodes[1][0], "TAR":nodes[2][1], "VAL": row["BudgetPrivate"], "LAB": row['IdProjet']})
        flows.append({"SRC": nodes[1][1], "TAR":nodes[2][1], "VAL": row["BudgetSubCan"], "LAB": row['IdProjet']})
        flows.append({"SRC": nodes[1][2], "TAR":nodes[2][1], "VAL": row["BudgetSubCom"], "LAB": row['IdProjet']})
        
        if row['AgEner_1'] == 'Bois':
            flows.append({"SRC": nodes[2][1], "TAR":nodes[3][0], "VAL": row["BudgetTotal"], "LAB": row['IdProjet']})

        if row['AgEner_1'] == 'PAC':
            flows.append({"SRC": nodes[2][1], "TAR":nodes[3][1], "VAL": row["BudgetTotal"], "LAB": row['IdProjet']})
        
for _, row in data_new.iterrows():
    flows.append({"SRC": nodes[0][1], "TAR":nodes[1][0], "VAL": row["BudgetPrivate"], "LAB": row['IdProjet']})
    flows.append({"SRC": nodes[0][1], "TAR":nodes[1][1], "VAL": row["BudgetSubCan"], "LAB": row['IdProjet']})
    flows.append({"SRC": nodes[0][1], "TAR":nodes[1][2], "VAL": row["BudgetSubCom"], "LAB": row['IdProjet']})
    
    if row["EffAubaine"] == "no":
        flows.append({"SRC": nodes[1][0], "TAR":nodes[2][0], "VAL": row["BudgetPrivate"], "LAB": row['IdProjet']})
        flows.append({"SRC": nodes[1][1], "TAR":nodes[2][0], "VAL": row["BudgetSubCan"], "LAB": row['IdProjet']})
        flows.append({"SRC": nodes[1][2], "TAR":nodes[2][0], "VAL": row["BudgetSubCom"], "LAB": row['IdProjet']})
        
        if row['Label'] == 'Minergie':
            flows.append({"SRC": nodes[2][0], "TAR":nodes[3][2], "VAL": row["BudgetTotal"], "LAB": row['IdProjet']})
        
        if row['Label'] == 'MinergieP':
            flows.append({"SRC": nodes[2][0], "TAR":nodes[3][3], "VAL": row["BudgetTotal"], "LAB": row['IdProjet']})
    
    if row["EffAubaine"] == "yes":
        flows.append({"SRC": nodes[1][0], "TAR":nodes[2][1], "VAL": row["BudgetPrivate"], "LAB": row['IdProjet']})
        flows.append({"SRC": nodes[1][1], "TAR":nodes[2][1], "VAL": row["BudgetSubCan"], "LAB": row['IdProjet']})
        flows.append({"SRC": nodes[1][2], "TAR":nodes[2][1], "VAL": row["BudgetSubCom"], "LAB": row['IdProjet']})
    
        if row['Label'] == 'Minergie':
            flows.append({"SRC": nodes[2][1], "TAR":nodes[3][2], "VAL": row["BudgetTotal"], "LAB": row['IdProjet']})
        
        if row['Label'] == 'MinergieP':
            flows.append({"SRC": nodes[2][1], "TAR":nodes[3][3], "VAL": row["BudgetTotal"], "LAB": row['IdProjet']})
        
for _, row in data_ren.iterrows():
    flows.append({"SRC": nodes[0][2], "TAR":nodes[1][0], "VAL": row["BudgetPrivate"], "LAB": row['IdProjet']})
    flows.append({"SRC": nodes[0][2], "TAR":nodes[1][1], "VAL": row["BudgetSubCan"], "LAB": row['IdProjet']})
    flows.append({"SRC": nodes[0][2], "TAR":nodes[1][2], "VAL": row["BudgetSubCom"], "LAB": row['IdProjet']})
    
    if row["EffAubaine"] == "no":
        flows.append({"SRC": nodes[1][0], "TAR":nodes[2][0], "VAL": row["BudgetPrivate"], "LAB": row['IdProjet']})
        flows.append({"SRC": nodes[1][1], "TAR":nodes[2][0], "VAL": row["BudgetSubCan"], "LAB": row['IdProjet']})
        flows.append({"SRC": nodes[1][2], "TAR":nodes[2][0], "VAL": row["BudgetSubCom"], "LAB": row['IdProjet']})
    
        if row['Label'] == 'Minergie':
            flows.append({"SRC": nodes[2][0], "TAR":nodes[3][4], "VAL": row["BudgetTotal"], "LAB": row['IdProjet']})

        if row['Label'] == 'MinergieP':
            flows.append({"SRC": nodes[2][0], "TAR":nodes[3][5], "VAL": row["BudgetTotal"], "LAB": row['IdProjet']})
            
    if row["EffAubaine"] == "yes":
        flows.append({"SRC": nodes[1][0], "TAR":nodes[2][1], "VAL": row["BudgetPrivate"], "LAB": row['IdProjet']})
        flows.append({"SRC": nodes[1][1], "TAR":nodes[2][1], "VAL": row["BudgetSubCan"], "LAB": row['IdProjet']})
        flows.append({"SRC": nodes[1][2], "TAR":nodes[2][1], "VAL": row["BudgetSubCom"], "LAB": row['IdProjet']})
        
        if row['Label'] == 'Minergie':
            flows.append({"SRC": nodes[2][1], "TAR":nodes[3][4], "VAL": row["BudgetTotal"], "LAB": row['IdProjet']})

        if row['Label'] == 'MinergieP':
            flows.append({"SRC": nodes[2][1], "TAR":nodes[3][5], "VAL": row["BudgetTotal"], "LAB": row['IdProjet']})
    
    

source = []
target = []
value = []
label = []

labels = ["Chang Ag Éner", "Rénovations", "Nouvelles Cons", "Investissements Privés", "Subv Cantonale", "Subv Communale", "Encouragement Réussi", "Aubaine", 'Bois', 'PAC', 'NC Minergie', 'NC MinergieP', 'REN Minergie', 'REN MinergieP']
colors = ["White", "White", "White", "White", "White", "White", "White", "White", 'White', 'White', 'White', 'White', 'White', 'White']


for i, _ in enumerate(flows):
    source.append(flows[i]['SRC'])
    target.append(flows[i]['TAR'])
    value.append(flows[i]['VAL'])
    label.append(flows[i]['LAB'])

