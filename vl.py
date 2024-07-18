from pathlib import Path
from datetime import datetime
import pandas as pd
from taipy.gui import Gui
import taipy.gui.builder as tgb
import numpy as np
import re
from dateutil.parser import parse

# this_dir  = Path(__file__).parent if __file__ in locals() else Path.cwd()
wb_file_path = "Excel files\SUIVI AFFAIRES 2024-1.xlsx"

def filter_and_select(df, filter_col, filter_val, select_cols):
    filtered_df = df[df[filter_col] == filter_val]
    return filtered_df[select_cols]


def sales_data_cleaner(df,name_sale : str) :

    df["Prime_for_n"] = df[name_sale]
    for a in ["CP", "."] :
        row_index = df['Prime_for_n'].str.contains(a, case=False, na=False)
        j = df["Prime_for_n"][row_index].values
        j = re.sub(r'\D+', '', j[0])
        print(j)
        df["Prime_for_n"][row_index] = j
    df['Prime_for_n'] = df["Prime_for_n"].fillna(0).astype(int)
    col_name = name_sale+"cleaned"
    df[col_name] = df['Prime_for_n']

    return df,col_name

def contrat_type_extractor(bia) :
    splitted_type = bia.split("/")
    if len(splitted_type)<2 :
        splitted_type = splitted_type[0]
    return splitted_type[1]

def dataframe_AA(file_path,column_for_date,k = False):

    excel_file = pd.ExcelFile(file_path)
    dfs = []
    for sheet_name in excel_file.sheet_names:
        if sheet_name != "RETOUR POLICE ANTE":
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name, dtype={column_for_date:str})
                df['SheetName'] = sheet_name
                df = df.dropna(subset=[column_for_date])
                df= df.dropna(axis=1, how='all')
                df[column_for_date] = pd.to_datetime(df[column_for_date])
            except Exception as e:
                horror = True
                match = f"Erreur au niveau de la | {column_for_date}  de la feuille | {sheet_name}  du fichier | {file_path} "
                print(e)
                return match , "*" ,k

            dfs.append(df)
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df = combined_df.sort_values(by=column_for_date)
    combined_df["Contrat_type"] = combined_df["Numéro de BIA"].apply(contrat_type_extractor)
    #combined_df['Date de réception BIA'] = df['Date de réception BIA'].apply(convert_date)
    t = combined_df[column_for_date]
    return combined_df,t,k

def change_propagator(df):
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    
    jj = [col_name_collected,col_name]
    dt_show = df.groupby(["Apporteur",'Contrat_type']).agg({
        "Apporteur": 'size',
        col_name :'sum',
        col_name_collected :'sum'

    }).rename(columns={'Apporteur': 'Nombre_occurrences'}).reset_index()
    dt_client_show = df.groupby(["Nom souscripteur","Contrat_type"]).agg({
        "Nom souscripteur": 'size',
        "Primecleaned" :'sum',
        "Prime totale encaisséecleaned" :'sum'
    }).rename(columns = {"Nom souscripteur": "num_occu"}).reset_index()
    dt_client_show = dt_client_show.sort_values(by=["num_occu","Contrat_type"], ascending=[False,False])
    dt_show = dt_show.sort_values(by="Nombre_occurrences", ascending=False)
    dt_contrat_type = dt_show.groupby("Contrat_type").sum().reset_index()
    dt_contrat_type = dt_contrat_type.sort_values(by="Nombre_occurrences", ascending=False)
    

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ind_best = dt_client_show[dt_client_show["Contrat_type"]== dt_contrat_type["Contrat_type"].iloc[0]]["num_occu"].idxmax()
    ind_best_value = dt_client_show[dt_client_show["Contrat_type"]== dt_contrat_type["Contrat_type"].iloc[0]]["Primecleaned"].idxmax()
    ind_best_contrat = df[df["Contrat_type"]== dt_contrat_type["Contrat_type"].iloc[0]]["Primecleaned"].idxmax()
    ind_best_agent_for_produc_type = dt_show[dt_show["Contrat_type"]==dt_contrat_type["Contrat_type"].iloc[0]]["Primecleaned"].idxmax()
    contrats_sales = list()
    for contrat in list_type_contrat :
        vente = df[df["Contrat_type"] == contrat]['Primecleaned'].sum()
        class sales_contrat : 
            Contrat_type = contrat
            Montant = int(vente)
                    
                
        contrats_sales.append(sales_contrat)


    class Data_for_dash :
        sales_amount_prime = "{:,}".format(int(df[col_name].sum()))
        sales_amount_prime_collected = "{:,}".format(int(df[col_name_collected].sum()))
        Chiffres_affaire_par_type_de_contrat  = contrats_sales
        Nombre_ventes  = "{:,}".format(int(dt_show["Nombre_occurrences"].sum()))
    
    class Data_most_selled_product :

        product_name = dt_contrat_type["Contrat_type"].iloc[0]
        amount = "{:,}".format(int(dt_contrat_type["Primecleaned"].iloc[0]))
        Best_agent_for_this_product = dt_show["Apporteur"].loc[ind_best_agent_for_produc_type]
        Total_prime = "{:,}".format(int(dt_contrat_type["Primecleaned"].iloc[0]))
        Total_prime_collected = "{:,}".format(int(dt_contrat_type["Prime totale encaisséecleaned"].iloc[0]))

        Client_holding_the_biggest_amount = dt_client_show["Nom souscripteur"].loc[ind_best_value]
        Value_1 = "{:,}".format(int(dt_client_show["Primecleaned"].loc[ind_best_value]))
        Client_holding_the_largest_number_of_this_contract = dt_client_show["Nom souscripteur"].loc[ind_best]
        Value_2 = "{:,}".format(int(dt_client_show["Primecleaned"].loc[ind_best]))
    
    Data_for_dashboard =[Data_for_dash,Data_most_selled_product]
    print("#####################################################")
    d = dt_show[(dt_show["Apporteur"] == "LOKOSSI CHRISTOPHE") & (dt_show["Contrat_type"] == "AHR")]['Primecleaned'].sum()
    # print("{:,}".format(Data_for_dash.Nombre_ventes))
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    List_agent = list()
    
    categories_uniques = df['Apporteur'].unique()
    print(categories_uniques)
    for nom in categories_uniques:
        max_prime = df[df["Apporteur"]==nom]["Primecleaned"].idxmax()
        max_contrat = df["Contrat_type"].loc[max_prime]
        max_name = df["Nom souscripteur"].loc[max_prime]
        max_prime = df["Primecleaned"].loc[max_prime]
        

        contrat_sales = list()
        for contrat in list_type_contrat :
            vente = dt_show[(dt_show["Apporteur"] == nom) & (dt_show["Contrat_type"] == contrat)]['Primecleaned'].sum()
            if vente > 0 :
                class sales_contrat : 
                    Contrat_type = contrat,
                    Montant = "{:,}".format(int(vente))

                contrat_sales.append(sales_contrat)
        class datas :
            Nom_agent = nom
            Nombre_contrat = "{:,}".format(int(dt_show.loc[dt_show["Apporteur"] == nom, 'Nombre_occurrences'].sum()))
            Chiffres_affaires_agent =  int(dt_show.loc[dt_show["Apporteur"] == nom, 'Primecleaned'].sum())
            Chiffres_affaires_contrat = contrat_sales
            Tableau_contrat =  filter_and_select(df,"Apporteur",nom,["Nom souscripteur","Nom assuré","Contrat_type","Primecleaned"])

        class Plus_gros_contrat : 
            Nom_client = max_name
            Type_contrat = max_contrat
            Montant_contrat = "{:,}".format(int(max_prime))

        mm =[datas,Plus_gros_contrat]
                                
            
        List_agent.append(mm)
        List_agent = sorted(List_agent, key=lambda x: x[0].Chiffres_affaires_agent,reverse=True)
        
    return List_agent,Data_for_dashboard,dt_client_show,dt_show,dt_contrat_type
def on_slider(state):
    global column
    state.df = df[df[column].dt.to_period("M") == state.n_month]
    state.List_agent,state.Data_for_dash,state.dt_client_show,state.dt_show,state.dt_contrat_type = change_propagator(state.df)



column = "Date de réception BIA"
df,gg,checker= dataframe_AA(wb_file_path,column)
list_type_contrat = df['Contrat_type'].unique()
# df = "{df}"


if not checker :
    df,col_name_collected = sales_data_cleaner(df,"Prime totale encaissée")
    df,col_name= sales_data_cleaner(df,"Prime")
    df['year_months'] = df[column].dt.to_period("M")
    List_agent,Data_for_dash,dt_client_show,dt_show,dt_contrat_type = change_propagator(df)
    year_months = sorted(df['year_months'].unique().astype(str))
    n_month = year_months[0]
    # year_months = df.to_dict(orient='dict')
