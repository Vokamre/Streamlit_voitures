import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Chargement des données
url = 'https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv'
df = pd.read_csv(url)

# Nettoyage des espaces et des points dans les noms de région
df['continent'] = df['continent'].str.strip().str.replace('.', '')

# Fonction pour afficher les graphiques
def afficher_graphiques(region):
    if region != 'All':
        data = df[df['continent'] == region]
    else:
        data = df
    
    st.subheader(f"Analyse pour la région : {region}")
    
    # Matrice de corrélation
    st.write("### Matrice de corrélation")
    corr = data.select_dtypes(include=['float64', 'int64']).corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    # Commentaires sur la matrice de corrélation
    st.write("""
    **Commentaires sur la matrice de corrélation :**
    - Une valeur de corrélation proche de 1 ou -1 indique une forte relation linéaire entre deux variables.
    - Une valeur positive indique que les variables augmentent ensemble, tandis qu'une valeur négative indique qu'une variable augmente lorsque l'autre diminue.
    - Par exemple, ici on observe une forte corrélation positive entre `cubicinches` et `hp`, ce qui signifie que la taille du moteur (cubicinches) est fortement liée à la puissance du moteur (hp).
    - Une forte corrélation négative entre `mpg` (miles per gallon) et `weightlbs` (poids en livres) suggère que les voitures plus lourdes consomment plus de carburant.
    """)

    # Distribution des variables
    st.write("### Distribution des variables")
    for column in data.select_dtypes(include=['float64', 'int64']).columns:
        fig, ax = plt.subplots()
        sns.histplot(data[column], kde=True, ax=ax)
        ax.set_title(f"Distribution de {column}")
        st.pyplot(fig)
        
        # Commentaires sur la distribution
        st.write(f"""
        **Commentaires sur la distribution de {column} :**
        - La distribution montre comment les valeurs de {column} sont réparties.
        - Une distribution bimodale pourrait indiquer deux groupes distincts dans les données, tandis qu'une distribution unimodale montre une concentration autour d'une valeur centrale.
        - La courbe KDE (Kernel Density Estimate) superposée permet de visualiser la densité des données.
        """)

# Interface Streamlit
st.title("Analyse des voitures par région")
region = st.selectbox("Sélectionnez la région", options=['All', 'US', 'Europe', 'Japan'])
afficher_graphiques(region)

st.write("""
### Instructions d'utilisation :
- Utilisez le menu déroulant pour sélectionner la région dont vous souhaitez voir l'analyse.
- Les graphiques de corrélation et de distribution se mettront à jour en fonction de la région sélectionnée.
- Lisez les commentaires sous chaque graphique pour mieux comprendre les relations et les distributions des données.
""")
