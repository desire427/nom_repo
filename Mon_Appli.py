import streamlit as st
import base64
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns

st.markdown("<h1 style='text-align: center; color: black;'>Mon Projet Final</h1>", unsafe_allow_html=True)

# Injection de CSS personnalisé pour mettre le texte en blanc
def ajout_css():
    st.markdown(
        """
        <style>
            /* Change la couleur du texte en blanc */
            body {
                color: white !important;
            }
            /* Assurez-vous que le fond est sombre pour une meilleure visibilité */
            .stApp {
                background-color: #1e1e1e !important;
            }
            /* Optionnel : Changement de couleur des titres */
            h1, h2, h3, h4, h5, h6, p {
                color: white !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
ajout_css()

#  Injection de CSS personnalise
st.markdown(
    """
    
    <style>
    

        /* Couleur de fond rouge pour la barre latérale gauche */
        [data-testid="stSidebar"] {
            background-color: #3A44BA; /* Rouge clair */
        }

        /* Contour noir autour des tables */
        table {
            border: 30px solid black;
            border-radius: 8px;
            overflow: hidden;
        }

        /* Contour noir autour des iframes (formulaires) */
        .formulaire-iframe {
            # border: 10px solid #DE1C03 !important;
            border-radius: 8px;
            overflow: hidden;
        }

        /* Styles personnalisés pour les boutons */
        button, .stButton > button {
            background-color: #C2C2C2 !important; /* Couleur de fond des boutons */
            border: 2px solid black !important; /* Bordure noire */
            border-radius: 5px !important; /* Rayon de bordure */
            padding: 0.5rem 1rem !important; /* Espacement intérieur */
        }

        /* Styles personnalisés pour les boutons de téléchargement */
        .stDownloadButton > button, .stDownloadButton > button:hover {
            background-color: #C2C2C2 !important; /* Couleur de fond des boutons de téléchargement */
            border: 2px solid black !important; /* Bordure noire */
            border-radius: 5px !important; /* Rayon de bordure */
        }
    </style>
    """,
    unsafe_allow_html=True,
)
# Injection de CSS personnalisé pour réduire la largeur du selectbox
# st.markdown(
#     """
#     <style>
#         .stSelectbox [data-baseweb="select"] {
#             width: 300px; /* Ajustez la largeur selon vos besoins */
#         }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

    # Ajout d'une image en tant qu'arrière-plan pour la partie droite

# Background function
def add_bg_from_local(img):
    with open(img, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url(data:image/{"jpg"};base64,{encoded_string});
                background-size: cover;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Appeler la fonction avec le chemin correct de l'image
try:
    add_bg_from_local("img.jpg")  # Assurez-vous que le fichier img.jpg est dans le même répertoire
except Exception as e:
    st.error(f"Une erreur s'est produite lors du chargement de l'image : {e}")
# 🌍 Présentation de l'application
st.markdown("""
This app allows you to scrape and analyze data on dogs and sheep from Expat-Dakar.
* **Python libraries:** requests, pandas, beautifulsoup4, streamlit
* **Data source:** [sn.coinafrique](https://sn.coinafrique.com/).
""")

# 📂 Menu de navigation dans la barre laterale
st.sidebar.title("📂 Navigation")
menu_option = st.sidebar.radio(
    "📌 Sélectionnez une option :", 
    ["Voir les datasets existants", "Scraper de nouvelles données", "Remplir le formulaire"],
    index=0
)

# 📌 **Saisie du nombre de pages à scraper
st.sidebar.write("### 📄 Nombre de pages à scraper")
num_pages = st.sidebar.number_input("Entrez le nombre de pages (entre 1 et 10) :", min_value=1, max_value=16, value=1, step=1)

# 📥 **Affichage du formulaire directement dans l'application**
if menu_option == "Remplir le formulaire":
    st.write("## 📝 Remplissez le formulaire")
    
    # Sélection du formulaire à afficher
    form_choice = st.radio("🔍 Sélectionnez le formulaire à afficher :", ["KoboToolbox", "Google Forms"])
    
    # Ajout d'une classe personnalisée pour appliquer le style aux iframes
    if form_choice == "KoboToolbox":
        st.markdown(
            f'<div class="formulaire-iframe">'
            f'<iframe src="https://ee.kobotoolbox.org/i/1GHgyJAk" height="800" width="100%" frameborder="0" scrolling="yes"></iframe>'
            f'</div>',
            unsafe_allow_html=True
        )
    elif form_choice == "Google Forms":
        st.markdown(
            f'<div class="formulaire-iframe">'
            f'<iframe src="https://docs.google.com/forms/d/e/1FAIpQLSckUpCziHgojj0m5uqZhLZOihtAxIpGm1N5Mj0ZIadKS75Ghw/viewform?usp=dialog" height="800" width="100%" frameborder="0" scrolling="yes"></iframe>'
            f'</div>',
            unsafe_allow_html=True
        )
# 🕵️ **Fonction pour scraper les données**
def scrape_data(url, num_pages):
    all_data = []
    
    for page in range(1, num_pages + 1):
        st.write(f"📡 Scraping page {page}...")
        response = requests.get(f"{url}?page={page}")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Recherche des conteneurs d'annonces
        conteneurs = soup.find_all('div', class_='col s6 m4 l3')  # Utilisation de la classe correspondante
        
        for contenaire in conteneurs:
            # Extraction des données avec le format correct
            nom = contenaire.find("p", class_="ad__card-description").text.strip() if contenaire.find("p", class_="ad__card-description") else "N/A"
            prix = contenaire.find("p", class_="ad__card-price").text.replace("CFA", "").replace(" ", "").strip() if contenaire.find("p", class_="ad__card-price") else "N/A"
            adresse = contenaire.find("p", class_="ad__card-location").text.replace("location_on", "").strip() if contenaire.find("p", class_="ad__card-location") else "N/A"
            img = contenaire.find("a", class_="card-image ad__card-image waves-block waves-light").img["src"] if contenaire.find("a", class_="card-image ad__card-image waves-block waves-light") else "N/A"
            
            # Création d'un dictionnaire avec les données extraites
            data = {
                'NOM': nom,
                'PRIX': prix,
                'ADRESSE': adresse,
                'IMAGE': img
            }
            all_data.append(data)
    
    return pd.DataFrame(all_data)

# 📥 **Fonction pour charger et afficher un dataset**
def load_dataset(file_path, dataset_name):
    df = pd.read_csv(file_path)
    max_rows = num_pages * 84
    displayed_df = df.head(max_rows)
    st.write(f"### 📊 Aperçu du jeu de données : {dataset_name}")
    st.write(f"🔢 Nombre de lignes affichées : {min(len(df), max_rows)}")
    st.dataframe(displayed_df)

    # Ajout d'un bouton pour calculer les prix
    # Ajout d'un bouton pour calculer les prix
    if st.button("💰 Calculer les prix"):
        st.write("### 💰 Statistiques sur les prix")
        try:
            # Assurez-vous que la colonne 'PRIX' est convertie en numérique
            displayed_df['PRIX'] = pd.to_numeric(displayed_df['PRIX'], errors='coerce')

            # Calcul des statistiques
            price_stats = displayed_df['PRIX'].describe()
            total_price = displayed_df['PRIX'].sum()  # Calcul du prix total

            # Création de deux colonnes pour afficher les statistiques et le prix total côte à côte
            col1, col2 = st.columns(2)

            # Affichage des statistiques dans la première colonne
            with col1:
                st.write("#### 📊 Détails des prix")
                st.write(price_stats)

            # Affichage du prix total dans la deuxième colonne
            with col2:
                st.write("#### 📈 Prix total")
                st.write(f"**{total_price} CFA**")

        except Exception as e:
            st.error(f"Une erreur s'est produite lors du calcul des prix : {e}")
            
            # Affichage des statistiques
            st.write(price_stats)
            st.write(f"📈 **Prix total :** {total_price} CFA")
        except Exception as e:
            st.error(f"Une erreur s'est produite lors du calcul des prix : {e}")

    # Ajout d'un bouton pour afficher le résumé statistique
    if st.button("📊 Afficher le résumé statistique"):
        st.write("### 📊 Résumé statistique")
        st.write(displayed_df.describe())

    st.sidebar.download_button(
        label="📥 Télécharger ces données",
        data=displayed_df.to_csv(index=False), 
        file_name=f"{dataset_name}_extrait.csv",
        mime="text/csv"
    )

# 🎯 **Voir les datasets existants**
if menu_option == "Voir les datasets existants":
    st.write("## 📂 Voir les datasets existants")
    
    # Création de deux colonnes pour afficher la catégorie et le dataset côte à côte
    col1, col2 = st.columns(2)
    
    with col1:
        # Sélection de la catégorie (Notebook ou Web)
        category_choice = st.selectbox("📂 Sélectionnez une catégorie :", ["Notebook", "Web"], key="category_select")
    
    with col2:
        # Mappage des fichiers selon la catégorie sélectionnée
        if category_choice == "Notebook":
            dataset_choice = st.selectbox("🔍 Sélectionnez un dataset Notebook :", 
                                          ["Chien NoteBook", "Mouton NoteBook"], key="notebook_dataset")
            file_mapping = {
                "Chien NoteBook": 'Categorie_Chien_Notebook.csv',
                "Mouton NoteBook": 'Categorie_Mouton_Notebook.csv'
            }
        elif category_choice == "Web":
            dataset_choice = st.selectbox("🔍 Sélectionnez un dataset Web :", 
                                          ["Chien Web", "Mouton Web"], key="web_dataset")
            file_mapping = {
                "Chien Web": 'Categorie_Chien_Web.csv',
                "Mouton Web": 'Categorie_Mouton_Web.csv'
            }
   
    # Charger et afficher le dataset sélectionné
    if dataset_choice in file_mapping:
        load_dataset(file_mapping[dataset_choice], dataset_choice)

# 🔍 **Scraper de nouvelles données**
elif menu_option == "Scraper de nouvelles données":
    st.write("## 🔍 Scraper de nouvelles données")
    url = st.text_input("🌍 Entrez l'URL à scraper :", "...")
    
    if st.sidebar.button("🚀 Lancer le scraping"):
        st.info("📡 Scraping en cours... Patientez.")
        scraped_data = scrape_data(url, num_pages)
        
        if not scraped_data.empty:
            st.success(f"✅ Scraping terminé ! {len(scraped_data)} lignes récupérées.")
            st.write("### 🔍 Aperçu des données")
            st.dataframe(scraped_data.head(num_pages * 84))
            
            # Ajout d'un bouton pour télécharger les données scrapées
            csv_data = scraped_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger les données scrapées",
                data=csv_data,
                file_name="donnees_scrappees.csv",
                mime="text/csv"
            )
        else:
            st.warning("Aucune donnée trouvée, veuillez vérifier l'URL et les classes CSS utilisées.")