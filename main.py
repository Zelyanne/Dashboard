from pathlib import Path
from agent_sales import Agent_sales
from datetime import datetime
import pandas as pd
from taipy.gui import Gui
import taipy.gui.builder as tgb
import numpy as np
import re
from dateutil.parser import parse
from vl import *


    

with tgb.Page() as root_page:
    tgb.navbar()

with tgb.Page()  as pages:
    if checker :        
        tgb.text("{df}")
        
    else :   
        with tgb.layout(columns="1") :

        
            tgb.text(" 📊 Sales Dashboard",class_name="h1")
    
            tgb.slider("{n_month}", lov= "{year_months}",on_change=on_slider)
            tgb.text("Resumé des ventes",class_name="h2 text-center")
            with tgb.layout(columns="1 1 1 1"):
                with tgb.part(class_name= "card"):
                    tgb.text("{Data_for_dash[0].Nombre_ventes}",class_name="h2 text-center")
                    tgb.text("Nombre de contrat obtenus",class_name="h6")
                with tgb.part(class_name= "card"):
                    with tgb.layout(columns="1 1") :
                        tgb.text("{Data_for_dash[0].sales_amount_prime}",class_name="h2 text-center color_warning")
                        tgb.text("Fcfa")
                    tgb.text("Montant total des ventes",class_name="h6")
                with tgb.part(class_name= "card"): 
                    tgb.text("{Data_for_dash[1].product_name}",class_name="h2 text-center")
                    tgb.text("Types d affaires le plus vendu",class_name="h6")
                with tgb.part(class_name= "card"):
                    tgb.text("{List_agent[0][0].Nom_agent}",class_name="h2")
                    tgb.text("Commercial le plus performant",class_name="h6")
    

            
            tgb.chart("{df}",mode="lines",x=column, y__1=col_name)
            tgb.chart("{dt_contrat_type}",type="bar",x="Contrat_type", y__1="Nombre_occurrences",class_name="container")
            tgb.table("{df}",class_name="container",filter=True)

"""  "Highest contract for this product" : {
            "Nom client" : df["Nom souscripteur"].loc[ind_best_contrat],
            "Nom agent" : df["Apporteur"].loc[ind_best_contrat],
            "Montant" : df["Primecleaned"].loc[ind_best_contrat]
        },"""


pages_dash = {
    "/": root_page,
    "Analyse_générale_des_donnéés": pages,
    "Agent_sales": Agent_sales
}


Gui(pages = pages_dash).run(
        title="Sales Dashboard",
        use_reloader= True,
        debug=True,
    )
