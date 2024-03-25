#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 16:05:33 2024

@author: mghezal001
"""

import streamlit as st
import pandas as pd
import numpy as np
from Fonctions_projet_S4 import *

with st.columns(3)[1]:
   st.title(":sos: Googl'INP :sos:")

st.write("Ajd on se retrouve avec inoxtag")

matiere = st.selectbox(
   "Dans quelle matière as-tu besoin d'aide?",
   ('Informatique','Biologie','Mathématiques','Physique','Chimie','Général'),
   index=None,
   placeholder="Ex : Mathématiques...",
)

st.write('You selected:',matiere)

df_sondage = pd.read_csv('Sondage.csv')
participant = list(df_sondage["Qui êtes-vous ?"])
list_matiere = ['En Informatique :','En Biologie :','En Mathématiques :','En Physique :','En Chime :']

if matiere != None:
    if matiere == 'Général':
        df = excel_to_fulldf(df_sondage)
        resultats = df_to_pr(df)
        resultats_df = tuple2df(resultats)
        resultats_df.index += 1 
        st.write(resultats_df)
        
    else :
        for elt in list_matiere:
            if str(matiere) == elt[3:-2]:
                matiere = elt
                break
            elif matiere == 'Chimie':
                matiere = 'En Chime :'
        st.write(matiere)
    
        df = excel_to_df(df_sondage, matiere)
        resultats = df_to_pr(df)
        resultats_df = tuple2df(resultats)
        resultats_df.index += 1 
        st.write(resultats_df)
