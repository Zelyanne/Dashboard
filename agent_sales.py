from pathlib import Path
from datetime import datetime
import pandas as pd
from taipy.gui import Gui
import taipy.gui.builder as tgb
import numpy as np
import re
from vl import *
from dateutil.parser import parse




with tgb.Page() as Agent_sales :
    tgb.text("hummmmmmmmmmmmmmm")
    with tgb.layout(columns="1"):
        for agent in List_agent  :
            with tgb.part(class_name="card") :
                with tgb.layout("1 1"):
                    with tgb.part() :
                        tgb.text("Nom agent")
                        tgb.text(agent[0].Nom_agent)
                        tgb.text("Nombre contrat")
                        tgb.text(agent[0].Nombre_contrat)
                        tgb.text("Chiffre d'affaire de l'agent commercial")
                        tgb.text("{:,}".format(agent[0].Chiffres_affaires_agent))
                    with tgb.part():
                        tgb.text("Plus gros contrat du commercial")
                        tgb.text("Nom du client")
                        tgb.text(agent[1].Nom_client)
                        tgb.text("Nom du produit")
                        tgb.text(agent[1].Type_contrat)
                        tgb.text("Montant du contrat")
                        tgb.text(agent[1].Montant_contrat)
                
                agent_table = agent[0].Tableau_contrat
                with tgb.expandable("Tableau des contrats de l'agent",expanded=False) :
                    tgb.text("Tableau des contrats de l'agent")
                    # tgb.table("{agent_table}",width ="3rem")

