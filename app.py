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

st.markdown("<h1 style='text-align: center; color: red;'>Googl'INP</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: black;'>Voici les résultats !!</h3>", unsafe_allow_html=True)

matiere = st.selectbox(
   "Dans quelle matière as-tu besoin d'aide?",
   ('Informatique','Biologie','Mathématiques','Physique','Chimie','Général'),
   index=None,
   placeholder="Ex : Mathématiques...",
)
col1, col2= st.columns(2)

with col1:
    st.checkbox("Contacts", value=False, key="contact")

with col2:
    st.checkbox("Plus de détails", value=False, key="detail")

df_sondage = pd.read_csv('Sondage.csv')
participant = list(df_sondage["Qui êtes-vous ?"])
list_matiere = ['En Informatique :','En Biologie :','En Mathématiques :','En Physique :','En Chime :']

if matiere != None:
    if matiere == 'Général':
        df = excel_to_fulldf(df_sondage)
        resultats = df_to_pr(df)
        resultats_df = tuple2df(resultats)
        resultats_df.index += 1
        if st.session_state.contact and st.session_state.detail:
            st.dataframe(resultats_df,use_container_width=True)
        elif st.session_state.detail:
            st.dataframe(resultats_df,use_container_width=True, column_order=('Nom','Fiabilité','Score'))
        else :
            st.dataframe(resultats_df,use_container_width=True, column_order=('Nom','Fiabilité'))
    
    else :
       for elt in list_matiere:
            if str(matiere) == elt[3:-2]:
                matiere = elt
                break
            elif matiere == 'Chimie':
                matiere = 'En Chime :'
       df = excel_to_df(df_sondage, matiere)
       resultats = df_to_pr(df)
       resultats_df = tuple2df(resultats)
       resultats_df.index +=1 
       st.dataframe(resultats_df,use_container_width=True)
