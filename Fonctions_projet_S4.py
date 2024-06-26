#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 16:02:10 2024

@author: mghezal001
"""


import pandas as pd
import numpy as np


def excel_to_fulldf(df_sondage):
    
    participant = list(df_sondage["Qui êtes-vous ?"])
    list_matiere = ['En Informatique :','En Biologie :','En Mathématiques :','En Physique :','En Chime :']
        
    dico = {}
    
    nb_participant = len(participant)
    
    #for i in range(nb_participant):
    for i in range(nb_participant):
        L=[]
        for matiere in list_matiere:
            L = L + df_sondage.iloc[i][matiere].split(",")
        for j in range(len(L)):
            L[j]=L[j].strip()
        K=[element for element in L]
        for element in K:
            if element not in participant:  #je sais pas si c'est ce que t'as demandé mais ça enlève les gens mentionés qui n'ont pas participer... enfin je crois
                dico[element] = []
        dico[participant[i]] = L
    matrice, sommets = suiv2adj(dico)
    matrice.dtype = np.float64
    for i in range(len(matrice)):
      x = sum(matrice[:, i])
      if x != 0:
        matrice[:, i] = matrice[:, i]/x
    df =pd.DataFrame(matrice, index=sommets, columns=sommets)
    return df
    
    
    
def suiv2adj(dict_suiv):
    """
    Parameters
    ----------
    suiv_prec : dictionnaire dont les valeurs sont des listes
        dictionnaire des successeurs du graphe


    Returns
    -------
    numpy.array
        tableau représentant la matrice d'adjacence d'un graphe orienté

    """
    sommets = list(dict_suiv.keys())
    n = len(sommets)
    matrice_adj = np.zeros((n,n), dtype=int)
    for i in range(n):
        s = sommets[i]
        for voisin in dict_suiv[s]:
            j = sommets.index(voisin)
            matrice_adj[i,j] += 1
    return matrice_adj.T,sommets



def excel_to_df(df_sondage, matiere):
  participant = list(df_sondage["Qui êtes-vous ?"])
  dico = {}

  nb_participant = len(participant)
  for i in range(nb_participant):
    L=[]
    L = L + df_sondage.iloc[i][matiere].split(",")
    for j in range(len(L)):
        L[j]=L[j].strip()
    K=[element for element in L]
    for element in K:
        if element not in participant:
            dico[element] = []
    dico[participant[i]] = L
  matrice, sommets = suiv2adj(dico)
  matrice.dtype = np.float64
  for i in range(len(matrice)):
    x = sum(matrice[:, i])
    if x != 0:
      matrice[:, i] = matrice[:, i]/x
  df =pd.DataFrame(matrice, index=sommets, columns=sommets)
  return df

def norme_epsilon(x, y):
    return max([np.linalg.norm(v) for v in (x-y)])

def pageRankTP(G, epsilon, beta=0.85):
  dim = len(G)
  r = np.ones((dim,)) / dim
  B = (1-beta)*r
  new_r = beta*np.dot(G,r) + B
  ite = 1
  while norme_epsilon(new_r, r) > epsilon:
    new_r, r = beta*np.dot(G,new_r) + B, new_r
    ite += 1
  return r/sum(r), ite


def resultats_nb_votes(df_sondage, matiere):
  df = excel_to_df(df_sondage, matiere)
  participants = list(df.columns)
  resultats = []
  for i in range(len(participants)):
    resultats.append((participants[i],
                      sum(df.iloc[i,:])*5/df.sum().sum())) # f
  resultats.sort(key=lambda x:x[1],reverse=True)

  return resultats



def resultats_full_nb_votes(df_sondage):
  df = excel_to_fulldf(df_sondage)
  participants = list(df.columns)
  resultats = []
  for i in range(len(participants)):
    resultats.append((participants[i],
                      sum(df.iloc[i,:])*5/df.sum().sum())) # f
  resultats.sort(key=lambda x:x[1],reverse=True)

  return resultats

def resultats_contacts(df_sondage):
    resultats = []
    for i in range(df_sondage.shape[0]):
        row = df_sondage.iloc[i,:]
        resultats.append((row["Qui êtes-vous ?"], row["Contacts"]))
    return resultats

def df_to_pr(df): #Fonction à appeler
  pr = pageRankTP(df, 1e-4)[0]
  participants = df.columns
  resultats = []

  for i in range(len(participants)):
    resultats.append(([participants[i]] , pr[i]))
  resultats.sort(key=lambda x:x[1],reverse=True)
  return resultats

def hyperlink(url):
    if url != None:
        return f'<a target="_blank" href="{url}">{url}</a>'

def tuple2df(resultat,nb_votes,contacts):
    nom = []
    fiabilite = []
    score = []
    
    for elt in resultat:
        nom.append(elt[0])
        score.append(str(round(elt[1]*100,2))+" %")
        if round(elt[1]*100,2) >= 5:
            fiabilite.append(3*'🌟')
        elif round(elt[1]*100,2) >= 1:
            fiabilite.append(2*'🌟')
        elif round(elt[1]*100,2) < 1:
            fiabilite.append('🌟')
    
    data = pd.DataFrame({'Nom': list(map(lambda x : x[0], nom)), 'Fiabilité' : fiabilite, 'Score w/ PR' : score})
    data.insert(2, '% de votes', [None]*data.shape[0],True)
    data.insert(4, 'Contacts', [None]*data.shape[0],True)
    
    for elt in nb_votes:
        index = data.index[data.Nom == elt[0]]
        data.loc[index,'% de votes'] = str(round(elt[1]*100/5,2))+" %"
        
    for elt in contacts:
        index = data.index[data.Nom == elt[0]]
        data.loc[index,'Contacts'] = elt[1]
        
          
    return data



