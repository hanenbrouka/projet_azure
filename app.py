import streamlit as st
import pyodbc
import pandas as pd
import os


# Connexion à la base de données Azure SQL
def connect_db():
    server = 'serveurrr.database.windows.net'  # Nom du serveur Azure
    database = 'societe' # Nom de la base de données
    username = 'hanen'  # Nom d'utilisateur
    password =  'Iset1234'  # Mot de passe
    driver = '{ODBC Driver 18 for SQL Server}'
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}')
    return conn

# Fonctions pour gérer les régions
def ajouter_region(libelle):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO region (libelle) VALUES (?)", (libelle,))
    conn.commit()
    conn.close()

def lister_regions():
    conn = connect_db()
    df = pd.read_sql("SELECT * FROM region", conn)
    conn.close()
    return df

def modifier_region(ID_region, libelle):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE region SET libelle = ? WHERE ID_region = ?", (libelle, ID_region))
    conn.commit()
    conn.close()

def supprimer_region(ID_region):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM region WHERE ID_region = ?", (ID_region,))
    conn.commit()
    conn.close()

# Fonctions pour gérer les clients
def ajouter_client(nom, prenom, age, ID_region):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO client (nom, prenom, age, ID_region) VALUES (?, ?, ?, ?)", (nom, prenom, age, ID_region))
    conn.commit()
    conn.close()

def lister_clients():
    conn = connect_db()
    df = pd.read_sql("""
        SELECT c.ID_client, c.nom, c.prenom, c.age, r.libelle AS region
        FROM client c
        LEFT JOIN region r ON c.ID_region = r.ID_region
    """, conn)
    conn.close()
    return df

def modifier_client(ID_client, nom, prenom, age, ID_region):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE client SET nom = ?, prenom = ?, age = ?, ID_region = ? WHERE ID_client = ?", 
                   (nom, prenom, age, ID_region, ID_client))
    conn.commit()
    conn.close()

def supprimer_client(ID_client):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM client WHERE ID_client = ?", (ID_client,))
    conn.commit()
    conn.close()

# Interface Streamlit
st.title("Gestion des Clients et Régions")

menu = ["Clients", "Régions"]
choix = st.sidebar.selectbox("Menu", menu)

if choix == "Régions":
    st.subheader("Gestion des Régions")
    action = st.selectbox("Action", ["Lister", "Ajouter", "Modifier", "Supprimer"])

    if action == "Lister":
        st.dataframe(lister_regions())

    elif action == "Ajouter":
        libelle = st.text_input("Libellé de la région")
        if st.button("Ajouter"):
            ajouter_region(libelle)
            st.success(f"Région '{libelle}' ajoutée avec succès !")

    elif action == "Modifier":
        regions = lister_regions()
        ID_region = st.selectbox("Sélectionnez une région", regions['ID_region'])
        libelle = st.text_input("Nouveau libellé", regions[regions['ID_region'] == ID_region]['libelle'].values[0])
        if st.button("Modifier"):
            modifier_region(ID_region, libelle)
            st.success(f"Région ID {ID_region} modifiée avec succès !")

    elif action == "Supprimer":
        regions = lister_regions()
        ID_region = st.selectbox("Sélectionnez une région à supprimer", regions['ID_region'])
        if st.button("Supprimer"):
            supprimer_region(ID_region)
            st.success(f"Région ID {ID_region} supprimée avec succès !")

elif choix == "Clients":
    st.subheader("Gestion des Clients")
    action = st.selectbox("Action", ["Lister", "Ajouter", "Modifier", "Supprimer"])

    if action == "Lister":
        st.dataframe(lister_clients())

    elif action == "Ajouter":
        nom = st.text_input("Nom")
        prenom = st.text_input("Prénom")
        age = st.number_input("Âge", min_value=0, step=1)
        regions = lister_regions()
        ID_region = st.selectbox("Région", regions['ID_region'], format_func=lambda x: f"{x} - {regions[regions['ID_region'] == x]['libelle'].values[0]}")
        if st.button("Ajouter"):
            ajouter_client(nom, prenom, age, ID_region)
            st.success(f"Client {nom} {prenom} ajouté avec succès !")

    elif action == "Modifier":
        clients = lister_clients()
        ID_client = st.selectbox("Sélectionnez un client", clients['ID_client'])
        nom = st.text_input("Nom", clients[clients['ID_client'] == ID_client]['nom'].values[0])
        prenom = st.text_input("Prénom", clients[clients['ID_client'] == ID_client]['prenom'].values[0])
        age = st.number_input("Âge", min_value=0, step=1, value=int(clients[clients['ID_client'] == ID_client]['age'].values[0]))
        regions = lister_regions()
        ID_region = st.selectbox("Région", regions['ID_region'], format_func=lambda x: f"{x} - {regions[regions['ID_region'] == x]['libelle'].values[0]}")
        if st.button("Modifier"):
            modifier_client(ID_client, nom, prenom, age, ID_region)
            st.success(f"Client ID {ID_client} modifié avec succès !")

    elif action == "Supprimer":
        clients = lister_clients()
        ID_client = st.selectbox("Sélectionnez un client à supprimer", clients['ID_client'])
        if st.button("Supprimer"):
            supprimer_client(ID_client)
            st.success(f"Client ID {ID_client} supprimé avec succès !")