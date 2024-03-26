#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

st.markdown("<h1 style='text-align: center; color: red;font-size: 4em;text-decoration: underline;'>Googl'INP</h1><br>", unsafe_allow_html=True)

st.markdown("<h5 style='text-align: center; color: black;'>Bienvenue sur le site d'aide aux devoirs de La Prépa des INP, nous espérons que vous trouverez le tuteur qui VOUS correspond !</h5><br>", unsafe_allow_html=True)

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

df_sondage = pd.read_csv('Sondage1.csv')
participant = list(df_sondage["Qui êtes-vous ?"])
list_matiere = ['En Informatique :','En Biologie :','En Mathématiques :','En Physique :','En Chime :']

if matiere != None:
    if matiere == 'Général':
        df = excel_to_fulldf(df_sondage)
        resultats = df_to_pr(df)
        nb_fullvotes = resultats_full_nb_votes(df_sondage)
        contact = resultats_contacts(df_sondage)
        resultats_df = tuple2df(resultats,nb_fullvotes,contact)
        resultats_df.index += 1
        if st.session_state.contact and st.session_state.detail:
            st.dataframe(resultats_df,use_container_width=True,column_config={"Contacts": st.column_config.LinkColumn("Contacts",display_text = 'Son LinkdIn')})
        elif st.session_state.detail:
            st.dataframe(resultats_df,use_container_width=True, column_order=('Nom','Fiabilité','Score w/ PR','% de votes'))
        
        elif st.session_state.contact:
               st.dataframe(resultats_df,use_container_width=True, column_order=('Nom','Fiabilité','Contacts'),
                            column_config={"Contacts": st.column_config.LinkColumn("Contacts",display_text = 'Son LinkdIn')})
    
               
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
        nb_votes = resultats_nb_votes(df_sondage, matiere)
        contact = resultats_contacts(df_sondage)
        resultats_df = tuple2df(resultats,nb_votes,contact)
        resultats_df.index +=1 
        if st.session_state.contact and st.session_state.detail:
            st.dataframe(resultats_df,use_container_width=True,column_config={"Contacts": st.column_config.LinkColumn("Contacts",display_text = 'Son LinkdIn')})
        elif st.session_state.detail:
            st.dataframe(resultats_df,use_container_width=True, column_order=('Nom','Fiabilité','Score w/ PR','% de votes'))
       
        elif st.session_state.contact:
               st.dataframe(resultats_df,use_container_width=True, column_order=('Nom','Fiabilité','Contacts'),column_config={"Contacts": st.column_config.LinkColumn("Contacts",display_text = 'Son LinkdIn')})
        
        else :
           st.dataframe(resultats_df,use_container_width=True, column_order=('Nom','Fiabilité'))
       
      


