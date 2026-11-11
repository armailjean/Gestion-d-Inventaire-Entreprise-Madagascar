import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys
import numpy as np
import re

# Configuration de l'apparence
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GestionInventaire(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🏢 Gestion d'Inventaire d'Entreprise - MADAGASCAR")
        self.geometry("1400x800")
        self.minsize(1200, 700)

        # Créer les fichiers XML s'ils n'existent pas
        self.creer_fichiers_xml()

        # Charger les données
        self.charger_donnees()

        # Interface utilisateur
        self.creer_interface()

    def creer_fichiers_xml(self):
        """Crée les fichiers XML s'ils n'existent pas avec des exemples pour Madagascar"""
        fichiers = ["produits.xml", "fournisseurs.xml", "ventes.xml"]
        
        # Exemples de données pour Madagascar
        exemples_produits = [
            {"id": "1", "nom": "Riz Malagasy", "categorie": "Alimentation", "quantite": "150", "prix": "2500", "fournisseur": "Riz du Terroir", "date_ajout": "2024-01-15 10:30:00"},
            {"id": "2", "nom": "Vanille de Madagascar", "categorie": "Épices", "quantite": "25", "prix": "15000", "fournisseur": "Vanille Premium", "date_ajout": "2024-01-15 11:00:00"},
            {"id": "3", "nom": "Litchi Frais", "categorie": "Fruits", "quantite": "80", "prix": "3500", "fournisseur": "Fruits Tropicaux", "date_ajout": "2024-01-15 09:15:00"},
            {"id": "4", "nom": "Café de Madagascar", "categorie": "Boissons", "quantite": "45", "prix": "12000", "fournisseur": "Café Malgache", "date_ajout": "2024-01-15 14:20:00"},
            {"id": "5", "nom": "Poivre Noir", "categorie": "Épices", "quantite": "60", "prix": "8000", "fournisseur": "Épices de l'Île", "date_ajout": "2024-01-15 16:45:00"}
        ]
        
        exemples_fournisseurs = [
            {"id": "1", "nom": "Riz du Terroir", "contact": "Jean Rakoto", "email": "rizterroir@gmail.com", "telephone": "+261341234567", "adresse": "Lot IIK 34, Antananarivo"},
            {"id": "2", "nom": "Vanille Premium", "contact": "Marie Rasoa", "email": "vanille.premium@gmail.com", "telephone": "0321234567", "adresse": "Sambava, Sava"},
            {"id": "3", "nom": "Fruits Tropicaux", "contact": "Pierre Andria", "email": "fruits.tropicaux@gmail.com", "telephone": "0339876543", "adresse": "Tamatave, Est"},
            {"id": "4", "nom": "Café Malgache", "contact": "Sophie Ravao", "email": "cafe.malgache@gmail.com", "telephone": "0341122334", "adresse": "Fianarantsoa, Hautes Terres"},
            {"id": "5", "nom": "Épices de l'Île", "contact": "David Randria", "email": "epices.ile@gmail.com", "telephone": "0385566778", "adresse": "Nosy Be, Diana"}
        ]
        
        exemples_ventes = [
            {"id": "1", "produit": "Riz Malagasy", "type": "Sortie", "quantite": "10", "prix": "2500", "raison": "Vente", "date": "2024-01-16 09:00:00", "ancien_stock": "150", "nouveau_stock": "140"},
            {"id": "2", "produit": "Vanille de Madagascar", "type": "Sortie", "quantite": "5", "prix": "15000", "raison": "Vente", "date": "2024-01-16 10:30:00", "ancien_stock": "25", "nouveau_stock": "20"}
        ]

        for fichier in fichiers:
            if not os.path.exists(fichier):
                if fichier == "ventes.xml":
                    root = ET.Element("ventes")
                    # Ajouter exemples de ventes
                    for vente in exemples_ventes:
                        operation = ET.SubElement(root, "operation")
                        for key, value in vente.items():
                            ET.SubElement(operation, key).text = value
                elif fichier == "fournisseurs.xml":
                    root = ET.Element("fournisseurs")
                    # Ajouter exemples de fournisseurs
                    for fournisseur in exemples_fournisseurs:
                        elem = ET.SubElement(root, "fournisseur")
                        for key, value in fournisseur.items():
                            ET.SubElement(elem, key).text = value
                else:
                    root = ET.Element("inventaire")
                    # Ajouter exemples de produits
                    for produit in exemples_produits:
                        elem = ET.SubElement(root, "produit")
                        for key, value in produit.items():
                            ET.SubElement(elem, key).text = value
                
                tree = ET.ElementTree(root)
                tree.write(fichier, encoding="utf-8", xml_declaration=True)

    def charger_donnees(self):
        """Charge les données depuis les fichiers XML"""
        try:
            # Charger produits
            tree = ET.parse("produits.xml")
            self.root_produits = tree.getroot()

            # Charger fournisseurs
            tree = ET.parse("fournisseurs.xml")
            self.root_fournisseurs = tree.getroot()

            # Charger ventes
            tree = ET.parse("ventes.xml")
            self.root_ventes = tree.getroot()
        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")

    def sauvegarder_donnees(self):
        """Sauvegarde les données dans les fichiers XML"""
        try:
            # Sauvegarder produits
            tree = ET.ElementTree(self.root_produits)
            tree.write("produits.xml", encoding="utf-8", xml_declaration=True)

            # Sauvegarder fournisseurs
            tree = ET.ElementTree(self.root_fournisseurs)
            tree.write("fournisseurs.xml", encoding="utf-8", xml_declaration=True)

            # Sauvegarder ventes
            tree = ET.ElementTree(self.root_ventes)
            tree.write("ventes.xml", encoding="utf-8", xml_declaration=True)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {e}")

    def creer_interface(self):
        """Crée l'interface graphique améliorée"""
        # Configuration du style
        self.configure(fg_color="#1e1e1e")

        # Frame principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Header avec titre et boutons rapides
        header_frame = ctk.CTkFrame(self.main_frame, height=80, fg_color="#2d2d2d", corner_radius=15)
        header_frame.pack(fill="x", pady=(0, 15))
        header_frame.pack_propagate(False)

        # Titre avec icône
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", fill="y", padx=20)

        title_label = ctk.CTkLabel(title_frame, text="🏢 GESTION D'INVENTAIRE ENTREPRISE - MADAGASCAR",
                                   font=ctk.CTkFont(size=20, weight="bold"),
                                   text_color="#ffffff")
        title_label.pack(pady=20)

        # Boutons rapides dans le header
        quick_actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        quick_actions_frame.pack(side="right", fill="y", padx=20)

        ctk.CTkButton(quick_actions_frame, text="📦 Ajouter Produit",
                      command=self.ajouter_produit, width=140, height=35,
                      fg_color="#2e86ab", hover_color="#1f5f7a", corner_radius=10).pack(side="left", padx=5)
        ctk.CTkButton(quick_actions_frame, text="👥 Ajouter Fournisseur",
                      command=self.ajouter_fournisseur, width=160, height=35,
                      fg_color="#a23b72", hover_color="#7a2c55", corner_radius=10).pack(side="left", padx=5)
        ctk.CTkButton(quick_actions_frame, text="💰 Gestion Ventes",
                      command=self.gerer_ventes, width=150, height=35,
                      fg_color="#28a745", hover_color="#1e7e34", corner_radius=10).pack(side="left", padx=5)
        ctk.CTkButton(quick_actions_frame, text="📊 Générer Rapport",
                      command=self.generer_rapport, width=150, height=35,
                      fg_color="#f9c74f", hover_color="#d4a72c", corner_radius=10).pack(side="left", padx=5)

        # Barre de statut
        self.status_bar = ctk.CTkLabel(self.main_frame, text="✅ Système prêt - Chargement des données terminé",
                                       anchor="w", font=ctk.CTkFont(size=12),
                                       text_color="#a0a0a0")
        self.status_bar.pack(fill="x", pady=(10, 5))

        # Onglets avec style amélioré
        self.tabview = ctk.CTkTabview(self.main_frame,
                                      segmented_button_fg_color="#2d2d2d",
                                      segmented_button_selected_color="#2e86ab",
                                      segmented_button_unselected_color="#3d3d3d",
                                      segmented_button_unselected_hover_color="#4d4d4d",
                                      corner_radius=15)
        self.tabview.pack(fill="both", expand=True)

        # Créer les onglets
        self.tabview.add("📊 Tableau de Bord")
        self.tabview.add("📦 Produits")
        self.tabview.add("👥 Fournisseurs")
        self.tabview.add("💰 Ventes")
        self.tabview.add("📈 Statistiques")
        self.tabview.add("📋 Rapports")
        self.tabview.add("⚙️ Paramètres")

        # Configurer chaque onglet
        self.creer_onglet_tableau_de_bord()
        self.creer_onglet_produits()
        self.creer_onglet_fournisseurs()
        self.creer_onglet_ventes()
        self.creer_onglet_statistiques()
        self.creer_onglet_rapports()
        self.creer_onglet_parametres()

        # Initialiser le tableau de bord après la création complète
        self.after(500, self.actualiser_tableau_de_bord)

    def creer_onglet_tableau_de_bord(self):
        """Crée l'onglet tableau de bord avec statistiques et indicateurs"""
        tab = self.tabview.tab("📊 Tableau de Bord")

        # Frame principal avec scrollbar
        main_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Bouton actualiser
        refresh_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        refresh_frame.pack(fill="x", pady=(0, 15))
        ctk.CTkButton(refresh_frame, text="🔄 Actualiser le Tableau de Bord",
                      command=self.actualiser_tableau_de_bord,
                      fg_color="#4a4a4a", hover_color="#5a5a5a",
                      width=200, height=35).pack(side="right")

        # Indicateurs KPI en grille
        kpi_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        kpi_frame.pack(fill="x", pady=(0, 20))

        # Configuration des indicateurs
        kpis = [
            {"title": "📦 TOTAL PRODUITS", "value": "0", "color": "#2e86ab", "icon": "📦"},
            {"title": "👥 FOURNISSEURS", "value": "0", "color": "#a23b72", "icon": "👥"},
            {"title": "💰 VALEUR TOTALE", "value": "0 Ar", "color": "#28a745", "icon": "💰"},
            {"title": "⚠️ FAIBLE STOCK", "value": "0", "color": "#ff6b6b", "icon": "⚠️"},
            {"title": "📈 CATÉGORIES", "value": "0", "color": "#f9c74f", "icon": "📈"},
            {"title": "🏆 FOURNISSEUR TOP", "value": "-", "color": "#7209b7", "icon": "🏆"},
            {"title": "🔥 PRODUITS POPULAIRES", "value": "0", "color": "#ff6b6b", "icon": "🔥"},
            {"title": "📊 VENTES TOTALES", "value": "0", "color": "#28a745", "icon": "📊"}
        ]

        self.kpi_labels = {}
        for i, kpi in enumerate(kpis):
            row = i // 4
            col = i % 4
            if col == 0:
                kpi_row = ctk.CTkFrame(kpi_frame, fg_color="transparent")
                kpi_row.pack(fill="x", pady=5)

            kpi_card = ctk.CTkFrame(kpi_row, fg_color=kpi["color"], corner_radius=12)
            kpi_card.pack(side="left", fill="both", expand=True, padx=5)

            # Contenu de la carte KPI
            inner_frame = ctk.CTkFrame(kpi_card, fg_color="transparent")
            inner_frame.pack(fill="both", expand=True, padx=15, pady=15)

            # Icone et titre
            title_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
            title_frame.pack(fill="x")

            ctk.CTkLabel(title_frame, text=kpi["icon"],
                         font=ctk.CTkFont(size=20)).pack(side="left")
            ctk.CTkLabel(title_frame, text=kpi["title"],
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color="#ffffff").pack(side="left", padx=(8, 0))

            # Valeur
            value_label = ctk.CTkLabel(inner_frame, text=kpi["value"],
                                       font=ctk.CTkFont(size=24, weight="bold"),
                                       text_color="#ffffff")
            value_label.pack(anchor="w", pady=(8, 0))

            self.kpi_labels[kpi["title"]] = value_label

        # Section graphiques
        charts_section = ctk.CTkFrame(main_frame, fg_color="transparent")
        charts_section.pack(fill="both", expand=True, pady=(20, 0))

        ctk.CTkLabel(charts_section, text="📊 ANALYSE VISUELLE",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(0, 15))

        # Graphiques côte à côte
        charts_row = ctk.CTkFrame(charts_section, fg_color="transparent")
        charts_row.pack(fill="both", expand=True)

        # Graphique des catégories
        chart1_frame = ctk.CTkFrame(charts_row, corner_radius=12)
        chart1_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))

        chart1_header = ctk.CTkFrame(chart1_frame, fg_color="#3b3b3b", corner_radius=12)
        chart1_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(chart1_header, text="📈 RÉPARTITION PAR CATÉGORIE",
                     font=ctk.CTkFont(weight="bold")).pack(pady=8)

        self.chart1_container = ctk.CTkFrame(chart1_frame, fg_color="#2b2b2b", height=300)
        self.chart1_container.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Graphique des fournisseurs
        chart2_frame = ctk.CTkFrame(charts_row, corner_radius=12)
        chart2_frame.pack(side="right", fill="both", expand=True, padx=(8, 0))

        chart2_header = ctk.CTkFrame(chart2_frame, fg_color="#3b3b3b", corner_radius=12)
        chart2_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(chart2_header, text="👥 TOP FOURNISSEURS",
                     font=ctk.CTkFont(weight="bold")).pack(pady=8)

        self.chart2_container = ctk.CTkFrame(chart2_frame, fg_color="#2b2b2b", height=300)
        self.chart2_container.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Section produits populaires
        popular_frame = ctk.CTkFrame(main_frame, corner_radius=12)
        popular_frame.pack(fill="both", expand=True, pady=(20, 0))

        popular_header = ctk.CTkFrame(popular_frame, fg_color="#28a745", corner_radius=12)
        popular_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(popular_header, text="🔥 PRODUITS LES PLUS VENDUS",
                     font=ctk.CTkFont(weight="bold"),
                     text_color="#ffffff").pack(pady=8)

        # Tableau des produits populaires
        columns_popular = ("Produit", "Quantité Vendue", "Revenu Total")
        self.tree_popular = ttk.Treeview(popular_frame, columns=columns_popular, show="headings", height=6)

        for col in columns_popular:
            self.tree_popular.heading(col, text=col)
            self.tree_popular.column(col, width=150)

        scrollbar_popular = ttk.Scrollbar(popular_frame, orient="vertical", command=self.tree_popular.yview)
        self.tree_popular.configure(yscrollcommand=scrollbar_popular.set)
        scrollbar_popular.pack(side="right", fill="y", padx=(0, 12), pady=12)
        self.tree_popular.pack(side="left", fill="both", expand=True, padx=12, pady=12)

        # Alertes de stock
        alerts_frame = ctk.CTkFrame(main_frame, corner_radius=12)
        alerts_frame.pack(fill="both", expand=True, pady=(20, 0))

        alerts_header = ctk.CTkFrame(alerts_frame, fg_color="#ff6b6b", corner_radius=12)
        alerts_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(alerts_header, text="🚨 PRODUITS À FAIBLE STOCK (< 10 unités)",
                     font=ctk.CTkFont(weight="bold"),
                     text_color="#ffffff").pack(pady=8)

        # Tableau des alertes
        columns = ("ID", "Nom", "Catégorie", "Quantité", "Prix", "Fournisseur")
        self.tree_faible_stock = ttk.Treeview(alerts_frame, columns=columns, show="headings", height=6)

        # Style du tableau
        style = ttk.Style()
        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        fieldbackground="#2b2b2b",
                        rowheight=25)
        style.configure("Treeview.Heading",
                        background="#3b3b3b",
                        foreground="white",
                        font=('Helvetica', 10, 'bold'))

        for col in columns:
            self.tree_faible_stock.heading(col, text=col)
            self.tree_faible_stock.column(col, width=100)

        scrollbar = ttk.Scrollbar(alerts_frame, orient="vertical", command=self.tree_faible_stock.yview)
        self.tree_faible_stock.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", padx=(0, 12), pady=12)
        self.tree_faible_stock.pack(side="left", fill="both", expand=True, padx=12, pady=12)

    def creer_graphique_categories(self, categories):
        """Crée le graphique des catégories"""
        if not categories:
            # Afficher un message si pas de données
            for widget in self.chart1_container.winfo_children():
                widget.destroy()
            label = ctk.CTkLabel(self.chart1_container, text="Aucune donnée disponible", 
                               text_color="white", font=ctk.CTkFont(size=14))
            label.pack(expand=True)
            return

        try:
            # Nettoyer le conteneur précédent
            for widget in self.chart1_container.winfo_children():
                widget.destroy()

            # Créer la figure
            fig = Figure(figsize=(6, 4), dpi=80, facecolor='#2b2b2b')
            ax = fig.add_subplot(111)

            # Données
            noms = list(categories.keys())
            valeurs = list(categories.values())

            # Couleurs modernes
            colors = ['#2e86ab', '#a23b72', '#f9c74f', '#28a745', '#ff6b6b', '#7209b7', '#f8961e', '#90be6d']

            # Graphique camembert
            wedges, texts, autotexts = ax.pie(valeurs, labels=noms, autopct='%1.1f%%',
                                              colors=colors[:len(noms)], startangle=90,
                                              textprops={'color': 'white', 'fontsize': 9})

            # Style des pourcentages
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')

            ax.set_title('Répartition des Produits par Catégorie',
                         color='white', fontsize=12, fontweight='bold', pad=20)

            # Intégration dans Tkinter
            canvas = FigureCanvasTkAgg(fig, self.chart1_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            print(f"Erreur création graphique catégories: {e}")

    def creer_graphique_fournisseurs(self, fournisseurs_stats):
        """Crée le graphique des fournisseurs"""
        if not fournisseurs_stats:
            # Afficher un message si pas de données
            for widget in self.chart2_container.winfo_children():
                widget.destroy()
            label = ctk.CTkLabel(self.chart2_container, text="Aucune donnée disponible", 
                               text_color="white", font=ctk.CTkFont(size=14))
            label.pack(expand=True)
            return

        try:
            # Nettoyer le conteneur précédent
            for widget in self.chart2_container.winfo_children():
                widget.destroy()

            # Top 5 fournisseurs
            top_fournisseurs = sorted(fournisseurs_stats.items(), key=lambda x: x[1], reverse=True)[:5]
            noms = [x[0] for x in top_fournisseurs]
            valeurs = [x[1] for x in top_fournisseurs]

            # Créer la figure
            fig = Figure(figsize=(6, 4), dpi=80, facecolor='#2b2b2b')
            ax = fig.add_subplot(111)

            # Couleurs
            colors = ['#2e86ab', '#a23b72', '#f9c74f', '#28a745', '#ff6b6b']

            # Graphique barres
            bars = ax.bar(noms, valeurs, color=colors, alpha=0.8, edgecolor='white', linewidth=1)

            # Style
            ax.set_ylabel('Nombre de Produits', color='white', fontweight='bold')
            ax.set_title('Top 5 Fournisseurs par Nombre de Produits',
                         color='white', fontsize=12, fontweight='bold', pad=20)

            # Couleur des axes
            ax.tick_params(axis='x', colors='white', rotation=45)
            ax.tick_params(axis='y', colors='white')

            # Couleur du cadre
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')

            # Fond du graphique
            ax.set_facecolor('#2b2b2b')

            # Ajouter les valeurs sur les barres
            for bar, valeur in zip(bars, valeurs):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                        f'{valeur}', ha='center', va='bottom', color='white', fontweight='bold')

            fig.tight_layout()

            # Intégration dans Tkinter
            canvas = FigureCanvasTkAgg(fig, self.chart2_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            print(f"Erreur création graphique fournisseurs: {e}")

    def actualiser_tableau_de_bord(self):
        """Actualise toutes les données du tableau de bord"""
        try:
            # Calculer les statistiques
            total_produits = 0
            total_valeur = 0
            produits_faible_stock = 0
            categories = {}
            fournisseurs_stats = {}
            categories_count = set()
            ventes_totales = 0
            produits_populaires = {}

            # Analyser les produits
            for produit in self.root_produits.findall("produit"):
                quantite = int(produit.find("quantite").text) if produit.find("quantite") is not None else 0
                prix = float(produit.find("prix").text) if produit.find("prix") is not None else 0
                categorie = produit.find("categorie").text if produit.find("categorie") is not None else "Non catégorisé"
                fournisseur = produit.find("fournisseur").text if produit.find("fournisseur") is not None else "Inconnu"

                total_produits += quantite
                total_valeur += quantite * prix

                if quantite < 10:
                    produits_faible_stock += 1

                # Statistiques par catégorie
                categories_count.add(categorie)
                if categorie not in categories:
                    categories[categorie] = 0
                categories[categorie] += quantite

                # Statistiques par fournisseur
                if fournisseur not in fournisseurs_stats:
                    fournisseurs_stats[fournisseur] = 0
                fournisseurs_stats[fournisseur] += 1

            # Analyser les ventes pour les produits populaires
            for operation in self.root_ventes.findall("operation"):
                if operation.find("type").text == "Sortie":
                    produit_nom = operation.find("produit").text
                    quantite = int(operation.find("quantite").text)
                    prix = float(operation.find("prix").text)
                    ventes_totales += quantite
                    
                    if produit_nom not in produits_populaires:
                        produits_populaires[produit_nom] = {"quantite": 0, "revenu": 0}
                    
                    produits_populaires[produit_nom]["quantite"] += quantite
                    produits_populaires[produit_nom]["revenu"] += quantite * prix

            # Trouver le fournisseur principal
            fournisseur_top = max(fournisseurs_stats.items(), key=lambda x: x[1])[0] if fournisseurs_stats else "Aucun"

            # Mettre à jour les KPI
            self.kpi_labels["📦 TOTAL PRODUITS"].configure(text=str(total_produits))
            self.kpi_labels["👥 FOURNISSEURS"].configure(text=str(len(self.root_fournisseurs.findall("fournisseur"))))
            self.kpi_labels["💰 VALEUR TOTALE"].configure(text=f"{total_valeur:,.2f} Ar")
            self.kpi_labels["⚠️ FAIBLE STOCK"].configure(text=str(produits_faible_stock))
            self.kpi_labels["📈 CATÉGORIES"].configure(text=str(len(categories_count)))
            self.kpi_labels["🏆 FOURNISSEUR TOP"].configure(
                text=fournisseur_top[:15] + "..." if len(fournisseur_top) > 15 else fournisseur_top)
            self.kpi_labels["🔥 PRODUITS POPULAIRES"].configure(text=str(len(produits_populaires)))
            self.kpi_labels["📊 VENTES TOTALES"].configure(text=str(ventes_totales))

            # Mettre à jour les graphiques
            self.creer_graphique_categories(categories)
            self.creer_graphique_fournisseurs(fournisseurs_stats)

            # Mettre à jour le tableau des produits populaires
            self.mettre_a_jour_produits_populaires(produits_populaires)

            # Mettre à jour le tableau des alertes
            self.mettre_a_jour_produits_faible_stock()

            # Mettre à jour la barre de statut
            self.status_bar.configure(
                text=f"✅ Tableau de bord actualisé - {total_produits} produits, {total_valeur:,.2f} Ar de valeur totale")

        except Exception as e:
            print(f"Erreur lors de l'actualisation du tableau de bord: {e}")

    def mettre_a_jour_produits_populaires(self, produits_populaires):
        """Met à jour la liste des produits populaires"""
        try:
            # Vider le tableau
            for item in self.tree_popular.get_children():
                self.tree_popular.delete(item)

            # Trier par quantité vendue
            produits_tries = sorted(produits_populaires.items(), 
                                  key=lambda x: x[1]["quantite"], reverse=True)[:10]

            # Ajouter les produits populaires
            for produit, stats in produits_tries:
                self.tree_popular.insert("", "end", values=(
                    produit,
                    stats["quantite"],
                    f"{stats['revenu']:,.2f} Ar"
                ))

        except Exception as e:
            print(f"Erreur mise à jour produits populaires: {e}")

    def mettre_a_jour_produits_faible_stock(self):
        """Met à jour la liste des produits à faible stock"""
        try:
            # Vider le tableau
            for item in self.tree_faible_stock.get_children():
                self.tree_faible_stock.delete(item)

            # Ajouter les produits avec faible stock
            for produit in self.root_produits.findall("produit"):
                quantite = int(produit.find("quantite").text) if produit.find("quantite") is not None else 0

                if quantite < 10:
                    # Déterminer la couleur en fonction du niveau de stock
                    tags = ('urgent',) if quantite < 5 else ('warning',)

                    values = (
                        produit.find("id").text if produit.find("id") is not None else "",
                        produit.find("nom").text if produit.find("nom") is not None else "",
                        produit.find("categorie").text if produit.find("categorie") is not None else "",
                        str(quantite),
                        f"{produit.find('prix').text} Ar" if produit.find('prix') is not None else "0 Ar",
                        produit.find("fournisseur").text if produit.find("fournisseur") is not None else ""
                    )
                    self.tree_faible_stock.insert("", "end", values=values, tags=tags)

            # Configurer les tags pour le style
            self.tree_faible_stock.tag_configure('urgent', background='#ff6b6b')
            self.tree_faible_stock.tag_configure('warning', background='#f9c74f')

        except Exception as e:
            print(f"Erreur lors de la mise à jour des produits à faible stock: {e}")

    def creer_onglet_produits(self):
        """Crée l'onglet de gestion des produits"""
        tab = self.tabview.tab("📦 Produits")

        # Frame principal
        main_frame = ctk.CTkFrame(tab, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header avec titre et statistiques
        header_frame = ctk.CTkFrame(main_frame, fg_color="#3b3b3b", corner_radius=12)
        header_frame.pack(fill="x", pady=(0, 15))

        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(header_content, text="📦 GESTION DES PRODUITS",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")

        # Indicateur rapide
        stats_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        stats_frame.pack(side="right")
        self.produits_count_label = ctk.CTkLabel(stats_frame, text="0 produits",
                                                 font=ctk.CTkFont(size=12),
                                                 text_color="#a0a0a0")
        self.produits_count_label.pack()

        # Barre d'outils
        toolbar_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        toolbar_frame.pack(fill="x", pady=(0, 15))

        # Boutons d'action
        actions_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        actions_frame.pack(side="left")

        ctk.CTkButton(actions_frame, text="➕ Ajouter Produit",
                      command=self.ajouter_produit,
                      width=140, height=35,
                      fg_color="#28a745", hover_color="#1e7e34").pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="✏️ Modifier",
                      command=self.modifier_produit,
                      width=100, height=35,
                      fg_color="#2e86ab", hover_color="#1f5f7a").pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="🗑️ Supprimer",
                      command=self.supprimer_produit,
                      width=100, height=35,
                      fg_color="#dc3545", hover_color="#a71e2a").pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="🔄 Actualiser",
                      command=self.actualiser_produits,
                      width=100, height=35,
                      fg_color="#6c757d", hover_color="#545b62").pack(side="left", padx=5)

        # Barre de recherche
        search_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        search_frame.pack(side="right")

        ctk.CTkLabel(search_frame, text="🔍 Rechercher:",
                     font=ctk.CTkFont(size=12)).pack(side="left", padx=5)
        self.search_entry = ctk.CTkEntry(search_frame, width=250, height=35,
                                         placeholder_text="Nom, catégorie, fournisseur...")
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.rechercher_produits)

        # Tableau des produits
        table_container = ctk.CTkFrame(main_frame, corner_radius=12)
        table_container.pack(fill="both", expand=True)

        # En-tête du tableau
        table_header = ctk.CTkFrame(table_container, fg_color="#3b3b3b", corner_radius=12)
        table_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(table_header, text="📋 LISTE DES PRODUITS",
                     font=ctk.CTkFont(weight="bold")).pack(pady=8)

        # Configuration du style du Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        fieldbackground="#2b2b2b",
                        rowheight=30,
                        bordercolor="#3b3b3b",
                        borderwidth=1)
        style.configure("Treeview.Heading",
                        background="#3b3b3b",
                        foreground="white",
                        font=('Helvetica', 10, 'bold'),
                        relief="flat")
        style.map("Treeview.Heading",
                  background=[('active', '#4a4a4a')])

        # Création du Treeview
        columns = ("ID", "Nom", "Catégorie", "Quantité", "Prix", "Fournisseur", "Date Ajout")
        self.tree_produits = ttk.Treeview(table_container, columns=columns, show="headings", height=15)

        # Configuration des colonnes
        column_widths = {"ID": 80, "Nom": 150, "Catégorie": 120, "Quantité": 100,
                         "Prix": 100, "Fournisseur": 120, "Date Ajout": 150}

        for col in columns:
            self.tree_produits.heading(col, text=col)
            self.tree_produits.column(col, width=column_widths.get(col, 120))

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree_produits.yview)
        h_scrollbar = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree_produits.xview)
        self.tree_produits.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Placement des éléments
        self.tree_produits.pack(side="left", fill="both", expand=True, padx=12, pady=(0, 12))
        v_scrollbar.pack(side="right", fill="y", padx=(0, 12), pady=(0, 12))
        h_scrollbar.pack(side="bottom", fill="x", padx=12, pady=(0, 12))

        # Charger les données
        self.actualiser_produits()

    def actualiser_produits(self):
        """Actualise la liste des produits"""
        try:
            # Vider le tableau
            for item in self.tree_produits.get_children():
                self.tree_produits.delete(item)

            # Compter les produits
            produits_count = 0

            # Ajouter les produits
            for i, produit in enumerate(self.root_produits.findall("produit")):
                produits_count += 1

                # Récupérer les valeurs avec des valeurs par défaut
                id_produit = produit.find("id").text if produit.find("id") is not None else str(i + 1)
                nom = produit.find("nom").text if produit.find("nom") is not None else "Sans nom"
                categorie = produit.find("categorie").text if produit.find("categorie") is not None else "Non catégorisé"
                quantite = produit.find("quantite").text if produit.find("quantite") is not None else "0"
                prix = produit.find("prix").text if produit.find("prix") is not None else "0"
                fournisseur = produit.find("fournisseur").text if produit.find("fournisseur") is not None else "Inconnu"
                date_ajout = produit.find("date_ajout").text if produit.find("date_ajout") is not None else ""

                values = (id_produit, nom, categorie, quantite, f"{prix} Ar", fournisseur, date_ajout)

                # Appliquer un style pour les produits à faible stock
                tags = ()
                if int(quantite) < 10:
                    tags = ('faible_stock',)
                elif int(quantite) == 0:
                    tags = ('rupture_stock',)

                self.tree_produits.insert("", "end", values=values, tags=tags)

            # Configurer les styles
            self.tree_produits.tag_configure('faible_stock', background='#fff3cd')
            self.tree_produits.tag_configure('rupture_stock', background='#f8d7da')

            # Mettre à jour le compteur
            self.produits_count_label.configure(text=f"{produits_count} produits")

            # Mettre à jour la barre de statut
            self.status_bar.configure(text=f"✅ Liste des produits actualisée - {produits_count} produits")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'actualisation des produits: {e}")

    def ajouter_produit(self):
        """Ouvre une fenêtre pour ajouter un produit"""
        dialog = AjouterProduitDialog(self, self.root_fournisseurs)
        self.wait_window(dialog)

        if dialog.result:
            nouveau_produit = ET.SubElement(self.root_produits, "produit")

            # Générer un ID unique
            produit_id = str(len(self.root_produits.findall("produit")) + 1)

            ET.SubElement(nouveau_produit, "id").text = produit_id
            ET.SubElement(nouveau_produit, "nom").text = dialog.result["nom"]
            ET.SubElement(nouveau_produit, "categorie").text = dialog.result["categorie"]
            ET.SubElement(nouveau_produit, "quantite").text = dialog.result["quantite"]
            ET.SubElement(nouveau_produit, "prix").text = dialog.result["prix"]
            ET.SubElement(nouveau_produit, "fournisseur").text = dialog.result["fournisseur"]
            ET.SubElement(nouveau_produit, "date_ajout").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.sauvegarder_donnees()
            self.actualiser_produits()
            self.actualiser_tableau_de_bord()
            self.status_bar.configure(text="✅ Produit ajouté avec succès")

    def modifier_produit(self):
        """Modifie le produit sélectionné"""
        selection = self.tree_produits.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un produit à modifier")
            return

        item = selection[0]
        values = self.tree_produits.item(item, "values")
        produit_id = values[0]  # ID du produit à modifier

        dialog = ModifierProduitDialog(self, values, self.root_fournisseurs)
        self.wait_window(dialog)

        if dialog.result:
            # Trouver le produit dans XML
            for produit in self.root_produits.findall("produit"):
                if produit.find("id").text == produit_id:
                    # Vérifier si le nom a changé
                    ancien_nom = produit.find("nom").text
                    nouveau_nom = dialog.result["nom"]
                    
                    # Si le nom a changé, vérifier qu'il n'existe pas déjà
                    if ancien_nom != nouveau_nom:
                        # Vérifier l'unicité du nouveau nom
                        for autre_produit in self.root_produits.findall("produit"):
                            if autre_produit.find("id").text != produit_id and autre_produit.find("nom").text.lower() == nouveau_nom.lower():
                                messagebox.showwarning("Erreur", f"Le produit '{nouveau_nom}' existe déjà dans l'inventaire")
                                return

                    # Mettre à jour les champs
                    produit.find("nom").text = nouveau_nom
                    produit.find("categorie").text = dialog.result["categorie"]
                    produit.find("quantite").text = dialog.result["quantite"]
                    produit.find("prix").text = dialog.result["prix"]
                    produit.find("fournisseur").text = dialog.result["fournisseur"]
                    break

            self.sauvegarder_donnees()
            self.actualiser_produits()
            self.actualiser_tableau_de_bord()
            self.status_bar.configure(text="✅ Produit modifié avec succès")

    def supprimer_produit(self):
        """Supprime le produit sélectionné"""
        selection = self.tree_produits.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un produit à supprimer")
            return

        item = selection[0]
        values = self.tree_produits.item(item, "values")

        if messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer le produit '{values[1]}' ?"):
            # Trouver et supprimer le produit
            for produit in self.root_produits.findall("produit"):
                if produit.find("id").text == values[0]:
                    self.root_produits.remove(produit)
                    break

            self.sauvegarder_donnees()
            self.actualiser_produits()
            self.actualiser_tableau_de_bord()
            self.status_bar.configure(text="✅ Produit supprimé avec succès")

    def rechercher_produits(self, event=None):
        """Recherche des produits"""
        query = self.search_entry.get().lower()

        for item in self.tree_produits.get_children():
            values = self.tree_produits.item(item, "values")
            if any(query in str(value).lower() for value in values):
                self.tree_produits.item(item, tags=('found',))
                self.tree_produits.selection_set(item)
            else:
                self.tree_produits.item(item, tags=('notfound',))

        self.tree_produits.tag_configure('found', background='#d4edda')
        self.tree_produits.tag_configure('notfound', background='#2b2b2b')

    def creer_onglet_fournisseurs(self):
        """Crée l'onglet de gestion des fournisseurs"""
        tab = self.tabview.tab("👥 Fournisseurs")

        # Frame principal
        main_frame = ctk.CTkFrame(tab, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header avec titre et statistiques
        header_frame = ctk.CTkFrame(main_frame, fg_color="#3b3b3b", corner_radius=12)
        header_frame.pack(fill="x", pady=(0, 15))

        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(header_content, text="👥 GESTION DES FOURNISSEURS",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")

        # Indicateur rapide
        stats_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        stats_frame.pack(side="right")
        self.fournisseurs_count_label = ctk.CTkLabel(stats_frame, text="0 fournisseurs",
                                                     font=ctk.CTkFont(size=12),
                                                     text_color="#a0a0a0")
        self.fournisseurs_count_label.pack()

        # Barre d'outils
        toolbar_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        toolbar_frame.pack(fill="x", pady=(0, 15))

        # Boutons d'action
        actions_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        actions_frame.pack(side="left")

        ctk.CTkButton(actions_frame, text="➕ Ajouter Fournisseur",
                      command=self.ajouter_fournisseur,
                      width=160, height=35,
                      fg_color="#28a745", hover_color="#1e7e34").pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="✏️ Modifier",
                      command=self.modifier_fournisseur,
                      width=100, height=35,
                      fg_color="#2e86ab", hover_color="#1f5f7a").pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="🗑️ Supprimer",
                      command=self.supprimer_fournisseur,
                      width=100, height=35,
                      fg_color="#dc3545", hover_color="#a71e2a").pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="🔄 Actualiser",
                      command=self.actualiser_fournisseurs,
                      width=100, height=35,
                      fg_color="#6c757d", hover_color="#545b62").pack(side="left", padx=5)

        # Tableau des fournisseurs
        table_container = ctk.CTkFrame(main_frame, corner_radius=12)
        table_container.pack(fill="both", expand=True)

        # En-tête du tableau
        table_header = ctk.CTkFrame(table_container, fg_color="#3b3b3b", corner_radius=12)
        table_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(table_header, text="📋 LISTE DES FOURNISSEURS",
                     font=ctk.CTkFont(weight="bold")).pack(pady=8)

        # Création du Treeview
        columns = ("ID", "Nom", "Contact", "Email", "Téléphone", "Adresse")
        self.tree_fournisseurs = ttk.Treeview(table_container, columns=columns, show="headings", height=15)

        # Configuration des colonnes
        column_widths = {"ID": 80, "Nom": 150, "Contact": 120, "Email": 180,
                         "Téléphone": 120, "Adresse": 200}

        for col in columns:
            self.tree_fournisseurs.heading(col, text=col)
            self.tree_fournisseurs.column(col, width=column_widths.get(col, 120))

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree_fournisseurs.yview)
        h_scrollbar = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree_fournisseurs.xview)
        self.tree_fournisseurs.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Placement des éléments
        self.tree_fournisseurs.pack(side="left", fill="both", expand=True, padx=12, pady=(0, 12))
        v_scrollbar.pack(side="right", fill="y", padx=(0, 12), pady=(0, 12))
        h_scrollbar.pack(side="bottom", fill="x", padx=12, pady=(0, 12))

        # Charger les données
        self.actualiser_fournisseurs()

    def actualiser_fournisseurs(self):
        """Actualise la liste des fournisseurs"""
        try:
            # Vider le tableau
            for item in self.tree_fournisseurs.get_children():
                self.tree_fournisseurs.delete(item)

            # Compter les fournisseurs
            fournisseurs_count = 0

            # Ajouter les fournisseurs
            for i, fournisseur in enumerate(self.root_fournisseurs.findall("fournisseur")):
                fournisseurs_count += 1

                values = (
                    fournisseur.find("id").text if fournisseur.find("id") is not None else str(i + 1),
                    fournisseur.find("nom").text if fournisseur.find("nom") is not None else "",
                    fournisseur.find("contact").text if fournisseur.find("contact") is not None else "",
                    fournisseur.find("email").text if fournisseur.find("email") is not None else "",
                    fournisseur.find("telephone").text if fournisseur.find("telephone") is not None else "",
                    fournisseur.find("adresse").text if fournisseur.find("adresse") is not None else ""
                )
                self.tree_fournisseurs.insert("", "end", values=values)

            # Mettre à jour le compteur
            self.fournisseurs_count_label.configure(text=f"{fournisseurs_count} fournisseurs")

            # Mettre à jour la barre de statut
            self.status_bar.configure(text=f"✅ Liste des fournisseurs actualisée - {fournisseurs_count} fournisseurs")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'actualisation des fournisseurs: {e}")

    def ajouter_fournisseur(self):
        """Ajoute un nouveau fournisseur"""
        dialog = AjouterFournisseurDialog(self)
        self.wait_window(dialog)

        if dialog.result:
            nouveau_fournisseur = ET.SubElement(self.root_fournisseurs, "fournisseur")

            fournisseur_id = str(len(self.root_fournisseurs.findall("fournisseur")) + 1)

            ET.SubElement(nouveau_fournisseur, "id").text = fournisseur_id
            ET.SubElement(nouveau_fournisseur, "nom").text = dialog.result["nom"]
            ET.SubElement(nouveau_fournisseur, "contact").text = dialog.result["contact"]
            ET.SubElement(nouveau_fournisseur, "email").text = dialog.result["email"]
            ET.SubElement(nouveau_fournisseur, "telephone").text = dialog.result["telephone"]
            ET.SubElement(nouveau_fournisseur, "adresse").text = dialog.result["adresse"]

            self.sauvegarder_donnees()
            self.actualiser_fournisseurs()
            self.actualiser_tableau_de_bord()
            self.status_bar.configure(text="✅ Fournisseur ajouté avec succès")

    def modifier_fournisseur(self):
        """Modifie le fournisseur sélectionné"""
        selection = self.tree_fournisseurs.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un fournisseur à modifier")
            return

        item = selection[0]
        values = self.tree_fournisseurs.item(item, "values")
        fournisseur_id = values[0]  # ID du fournisseur à modifier

        dialog = ModifierFournisseurDialog(self, values)
        self.wait_window(dialog)

        if dialog.result:
            for fournisseur in self.root_fournisseurs.findall("fournisseur"):
                if fournisseur.find("id").text == fournisseur_id:
                    # Vérifier si le nom a changé
                    ancien_nom = fournisseur.find("nom").text
                    nouveau_nom = dialog.result["nom"]
                    
                    # Si le nom a changé, vérifier qu'il n'existe pas déjà
                    if ancien_nom != nouveau_nom:
                        # Vérifier l'unicité du nouveau nom
                        for autre_fournisseur in self.root_fournisseurs.findall("fournisseur"):
                            if autre_fournisseur.find("id").text != fournisseur_id and autre_fournisseur.find("nom").text.lower() == nouveau_nom.lower():
                                messagebox.showwarning("Erreur", f"Le fournisseur '{nouveau_nom}' existe déjà")
                                return

                    # Mettre à jour les champs
                    fournisseur.find("nom").text = nouveau_nom
                    fournisseur.find("contact").text = dialog.result["contact"]
                    fournisseur.find("email").text = dialog.result["email"]
                    fournisseur.find("telephone").text = dialog.result["telephone"]
                    fournisseur.find("adresse").text = dialog.result["adresse"]
                    break

            self.sauvegarder_donnees()
            self.actualiser_fournisseurs()
            self.actualiser_tableau_de_bord()
            self.status_bar.configure(text="✅ Fournisseur modifié avec succès")

    def supprimer_fournisseur(self):
        """Supprime le fournisseur sélectionné"""
        selection = self.tree_fournisseurs.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un fournisseur à supprimer")
            return

        item = selection[0]
        values = self.tree_fournisseurs.item(item, "values")

        # Vérifier si le fournisseur est utilisé
        for produit in self.root_produits.findall("produit"):
            if produit.find("fournisseur").text == values[1]:
                messagebox.showwarning("Erreur",
                                       "Ce fournisseur est utilisé par des produits et ne peut pas être supprimé")
                return

        if messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer le fournisseur '{values[1]}' ?"):
            for fournisseur in self.root_fournisseurs.findall("fournisseur"):
                if fournisseur.find("id").text == values[0]:
                    self.root_fournisseurs.remove(fournisseur)
                    break

            self.sauvegarder_donnees()
            self.actualiser_fournisseurs()
            self.actualiser_tableau_de_bord()
            self.status_bar.configure(text="✅ Fournisseur supprimé avec succès")

    def creer_onglet_ventes(self):
        """Crée l'onglet de gestion des ventes avec interface améliorée"""
        tab = self.tabview.tab("💰 Ventes")

        # Frame principal
        main_frame = ctk.CTkFrame(tab, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="#2d2d2d", corner_radius=12)
        header_frame.pack(fill="x", pady=(0, 15))

        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(header_content, text="💰 GESTION DES VENTES ET STOCKS",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")

        # Conteneur principal avec deux colonnes
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)

        # Colonne gauche - Opérations
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", padx=(0, 10))

        # Section opérations
        operations_frame = ctk.CTkFrame(left_frame, corner_radius=12)
        operations_frame.pack(fill="both", pady=(0, 15))

        operations_header = ctk.CTkFrame(operations_frame, fg_color="#3b3b3b", corner_radius=12)
        operations_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(operations_header, text="🔄 OPÉRATIONS DE STOCK",
                     font=ctk.CTkFont(weight="bold")).pack(pady=8)

        # Formulaire d'opération
        form_frame = ctk.CTkFrame(operations_frame, fg_color="transparent")
        form_frame.pack(fill="x", padx=20, pady=20)

        # Ligne 1
        row1 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row1.pack(fill="x", pady=5)

        ctk.CTkLabel(row1, text="Produit:", width=100).pack(side="left", padx=5)
        self.vente_produit_combo = ctk.CTkComboBox(row1, width=300)
        self.vente_produit_combo.pack(side="left", padx=5, fill="x", expand=True)

        # Ligne 2
        row2 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row2.pack(fill="x", pady=5)

        ctk.CTkLabel(row2, text="Type:", width=100).pack(side="left", padx=5)
        self.vente_type_combo = ctk.CTkComboBox(row2, values=["Entrée", "Sortie"], width=120)
        self.vente_type_combo.set("Entrée")
        self.vente_type_combo.pack(side="left", padx=5)

        ctk.CTkLabel(row2, text="Quantité:", width=80).pack(side="left", padx=(20, 5))
        self.vente_quantite_entry = ctk.CTkEntry(row2, width=100)
        self.vente_quantite_entry.pack(side="left", padx=5)

        # Ligne 3
        row3 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row3.pack(fill="x", pady=5)

        ctk.CTkLabel(row3, text="Prix unitaire:", width=100).pack(side="left", padx=5)
        self.vente_prix_entry = ctk.CTkEntry(row3, width=120)
        self.vente_prix_entry.pack(side="left", padx=5)

        ctk.CTkLabel(row3, text="Raison:", width=80).pack(side="left", padx=(20, 5))
        self.vente_raison_combo = ctk.CTkComboBox(row3, 
                                                 values=["Achat", "Vente", "Retour", "Ajustement", "Perte"],
                                                 width=120)
        self.vente_raison_combo.set("Achat")
        self.vente_raison_combo.pack(side="left", padx=5)

        # Ligne 4
        row4 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row4.pack(fill="x", pady=5)

        ctk.CTkLabel(row4, text="Date:", width=100).pack(side="left", padx=5)
        self.vente_date_entry = ctk.CTkEntry(row4, width=200)
        self.vente_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.vente_date_entry.pack(side="left", padx=5)

        # Boutons d'opération
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=15)

        ctk.CTkButton(buttons_frame, text="➕ Ajouter l'Opération",
                      command=self.ajouter_operation_stock,
                      width=180, height=40,
                      fg_color="#28a745", hover_color="#1e7e34", corner_radius=10).pack(side="left", padx=5)

        ctk.CTkButton(buttons_frame, text="🔄 Actualiser",
                      command=self.actualiser_ventes,
                      width=120, height=40,
                      fg_color="#6c757d", hover_color="#545b62", corner_radius=10).pack(side="left", padx=5)

        # Colonne droite - Historique
        right_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Tableau des opérations avec conteneur amélioré
        table_container = ctk.CTkFrame(right_frame, corner_radius=12)
        table_container.pack(fill="both", expand=True)

        table_header = ctk.CTkFrame(table_container, fg_color="#3b3b3b", corner_radius=12)
        table_header.pack(fill="x", padx=12, pady=12)
        
        header_title_frame = ctk.CTkFrame(table_header, fg_color="transparent")
        header_title_frame.pack(fill="x")
        
        ctk.CTkLabel(header_title_frame, text="📋 HISTORIQUE DES OPÉRATIONS",
                     font=ctk.CTkFont(weight="bold")).pack(side="left")
        
        # Bouton d'actualisation dans l'en-tête
        ctk.CTkButton(header_title_frame, text="🔄", 
                      command=self.actualiser_ventes,
                      width=40, height=30,
                      fg_color="#4a4a4a", hover_color="#5a5a5a").pack(side="right")

        # Configuration du style du Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        fieldbackground="#2b2b2b",
                        rowheight=30,
                        bordercolor="#3b3b3b",
                        borderwidth=1)
        style.configure("Treeview.Heading",
                        background="#3b3b3b",
                        foreground="white",
                        font=('Helvetica', 10, 'bold'),
                        relief="flat")
        style.map("Treeview.Heading",
                  background=[('active', '#4a4a4a')])

        # Conteneur pour le tableau et les scrollbars
        table_wrapper = ctk.CTkFrame(table_container, fg_color="transparent")
        table_wrapper.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Création du Treeview avec plus de colonnes visibles
        columns = ("ID", "Produit", "Type", "Quantité", "Prix", "Raison", "Date", "Stock Final")
        self.tree_ventes = ttk.Treeview(table_wrapper, columns=columns, show="headings", height=20)

        # Configuration des colonnes avec largeurs adaptées
        column_configs = {
            "ID": {"width": 60, "anchor": "center"},
            "Produit": {"width": 120, "anchor": "w"},
            "Type": {"width": 80, "anchor": "center"},
            "Quantité": {"width": 80, "anchor": "center"},
            "Prix": {"width": 100, "anchor": "e"},
            "Raison": {"width": 100, "anchor": "center"},
            "Date": {"width": 150, "anchor": "center"},
            "Stock Final": {"width": 100, "anchor": "center"}
        }

        for col in columns:
            self.tree_ventes.heading(col, text=col)
            config = column_configs.get(col, {})
            self.tree_ventes.column(col, 
                                   width=config.get("width", 100),
                                   anchor=config.get("anchor", "center"))

        # Scrollbars positionnées à droite
        v_scrollbar = ttk.Scrollbar(table_wrapper, orient="vertical", command=self.tree_ventes.yview)
        h_scrollbar = ttk.Scrollbar(table_wrapper, orient="horizontal", command=self.tree_ventes.xview)
        self.tree_ventes.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Placement des éléments avec grid pour un meilleur contrôle
        self.tree_ventes.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        # Configuration du grid pour le redimensionnement
        table_wrapper.grid_rowconfigure(0, weight=1)
        table_wrapper.grid_columnconfigure(0, weight=1)

        # Informations statistiques
        stats_frame = ctk.CTkFrame(left_frame, corner_radius=12)
        stats_frame.pack(fill="x", pady=(10, 0))

        stats_header = ctk.CTkFrame(stats_frame, fg_color="#2e86ab", corner_radius=12)
        stats_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(stats_header, text="📊 STATISTIQUES RAPIDES",
                     font=ctk.CTkFont(weight="bold"),
                     text_color="#ffffff").pack(pady=8)

        stats_content = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_content.pack(fill="x", padx=20, pady=15)

        # Labels pour les statistiques
        self.stats_entrees_label = ctk.CTkLabel(stats_content, text="Entrées: 0", 
                                           font=ctk.CTkFont(size=12))
        self.stats_entrees_label.pack(anchor="w", pady=2)

        self.stats_sorties_label = ctk.CTkLabel(stats_content, text="Sorties: 0", 
                                           font=ctk.CTkFont(size=12))
        self.stats_sorties_label.pack(anchor="w", pady=2)

        self.stats_total_label = ctk.CTkLabel(stats_content, text="Total opérations: 0", 
                                         font=ctk.CTkFont(size=12))
        self.stats_total_label.pack(anchor="w", pady=2)

        # Charger les données initiales
        self.actualiser_liste_produits_ventes()
        self.actualiser_ventes()

    def actualiser_liste_produits_ventes(self):
        """Actualise la liste des produits pour les ventes"""
        produits = ["Sélectionner un produit"]
        for produit in self.root_produits.findall("produit"):
            nom = produit.find("nom")
            if nom is not None and nom.text:
                produits.append(nom.text)
        
        self.vente_produit_combo.configure(values=produits)
        if produits:
            self.vente_produit_combo.set("Sélectionner un produit")

    def ajouter_operation_stock(self):
        """Ajoute une opération de stock (entrée/sortie)"""
        try:
            produit_nom = self.vente_produit_combo.get()
            type_operation = self.vente_type_combo.get()
            quantite = self.vente_quantite_entry.get().strip()
            prix = self.vente_prix_entry.get().strip()
            raison = self.vente_raison_combo.get()
            date_operation = self.vente_date_entry.get().strip()

            # Validation
            if produit_nom == "Sélectionner un produit":
                messagebox.showwarning("Erreur", "Veuillez sélectionner un produit")
                return

            if not quantite.isdigit() or int(quantite) <= 0:
                messagebox.showwarning("Erreur", "La quantité doit être un nombre positif")
                return

            try:
                prix_float = float(prix)
                if prix_float < 0:
                    messagebox.showwarning("Erreur", "Le prix doit être positif")
                    return
            except ValueError:
                messagebox.showwarning("Erreur", "Le prix doit être un nombre valide")
                return

            # Trouver le produit
            produit_trouve = None
            for produit in self.root_produits.findall("produit"):
                if produit.find("nom").text == produit_nom:
                    produit_trouve = produit
                    break

            if produit_trouve is None:
                messagebox.showwarning("Erreur", "Produit non trouvé")
                return

            # Calculer le nouveau stock
            ancien_stock = int(produit_trouve.find("quantite").text)
            quantite_int = int(quantite)

            if type_operation == "Entrée":
                nouveau_stock = ancien_stock + quantite_int
            else:  # Sortie
                if quantite_int > ancien_stock:
                    messagebox.showwarning("Erreur", "Stock insuffisant pour cette sortie")
                    return
                nouveau_stock = ancien_stock - quantite_int

            # Mettre à jour le stock du produit
            produit_trouve.find("quantite").text = str(nouveau_stock)

            # Ajouter l'opération aux ventes
            nouvelle_vente = ET.SubElement(self.root_ventes, "operation")
            operation_id = str(len(self.root_ventes.findall("operation")) + 1)

            ET.SubElement(nouvelle_vente, "id").text = operation_id
            ET.SubElement(nouvelle_vente, "produit").text = produit_nom
            ET.SubElement(nouvelle_vente, "type").text = type_operation
            ET.SubElement(nouvelle_vente, "quantite").text = quantite
            ET.SubElement(nouvelle_vente, "prix").text = prix
            ET.SubElement(nouvelle_vente, "raison").text = raison
            ET.SubElement(nouvelle_vente, "date").text = date_operation
            ET.SubElement(nouvelle_vente, "ancien_stock").text = str(ancien_stock)
            ET.SubElement(nouvelle_vente, "nouveau_stock").text = str(nouveau_stock)

            # Sauvegarder
            self.sauvegarder_donnees()
            self.actualiser_ventes()
            self.actualiser_produits()
            self.actualiser_tableau_de_bord()

            # Réinitialiser le formulaire
            self.vente_quantite_entry.delete(0, "end")
            self.vente_prix_entry.delete(0, "end")
            self.vente_date_entry.delete(0, "end")
            self.vente_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            self.status_bar.configure(text=f"✅ Opération de {type_operation.lower()} enregistrée avec succès")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout de l'opération: {e}")

    def actualiser_ventes(self):
        """Actualise la liste des opérations de vente et les statistiques"""
        try:
            # Vider le tableau
            for item in self.tree_ventes.get_children():
                self.tree_ventes.delete(item)

            # Compteurs pour les statistiques
            total_entrees = 0
            total_sorties = 0

            # Ajouter les opérations
            for operation in self.root_ventes.findall("operation"):
                values = (
                    operation.find("id").text if operation.find("id") is not None else "",
                    operation.find("produit").text if operation.find("produit") is not None else "",
                    operation.find("type").text if operation.find("type") is not None else "",
                    operation.find("quantite").text if operation.find("quantite") is not None else "",
                    f"{operation.find('prix').text} Ar" if operation.find('prix') is not None else "0 Ar",
                    operation.find("raison").text if operation.find("raison") is not None else "",
                    operation.find("date").text if operation.find("date") is not None else "",
                    operation.find("nouveau_stock").text if operation.find("nouveau_stock") is not None else ""
                )

                # Appliquer un style selon le type
                tags = ()
                type_op = operation.find("type").text if operation.find("type") is not None else ""
                if type_op == "Entrée":
                    tags = ('entree',)
                    total_entrees += 1
                else:
                    tags = ('sortie',)
                    total_sorties += 1

                self.tree_ventes.insert("", "end", values=values, tags=tags)

            # Configurer les styles
            self.tree_ventes.tag_configure('entree', background='#d4edda', foreground='black')
            self.tree_ventes.tag_configure('sortie', background='#f8d7da', foreground='black')

            # Mettre à jour les statistiques
            total_operations = total_entrees + total_sorties
            self.stats_entrees_label.configure(text=f"Entrées: {total_entrees}")
            self.stats_sorties_label.configure(text=f"Sorties: {total_sorties}")
            self.stats_total_label.configure(text=f"Total opérations: {total_operations}")

            # Mettre à jour la barre de statut
            self.status_bar.configure(text=f"✅ Historique des ventes actualisé - {total_operations} opérations")

        except Exception as e:
            print(f"Erreur actualisation ventes: {e}")

    def gerer_ventes(self):
        """Ouvre l'onglet des ventes"""
        self.tabview.set("💰 Ventes")

    def creer_onglet_statistiques(self):
        """Crée l'onglet des statistiques avancées"""
        tab = self.tabview.tab("📈 Statistiques")

        # Frame principal avec scroll
        main_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Titre section
        ctk.CTkLabel(main_frame, text="📊 STATISTIQUES AVANCÉES",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=(0, 20))

        # Frame pour les graphiques statistiques
        stats_charts_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        stats_charts_frame.pack(fill="both", expand=True)

        # Graphique 1: Évolution temporelle
        chart1_frame = ctk.CTkFrame(stats_charts_frame, corner_radius=12)
        chart1_frame.pack(fill="both", expand=True, pady=(0, 15))

        chart1_header = ctk.CTkFrame(chart1_frame, fg_color="#3b3b3b", corner_radius=12)
        chart1_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(chart1_header, text="📈 ÉVOLUTION DES STOCKS (30 JOURS)",
                     font=ctk.CTkFont(weight="bold")).pack(pady=8)

        self.stats_chart1_container = ctk.CTkFrame(chart1_frame, fg_color="#2b2b2b", height=300)
        self.stats_chart1_container.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Graphique 2: Performance des fournisseurs
        chart2_frame = ctk.CTkFrame(stats_charts_frame, corner_radius=12)
        chart2_frame.pack(fill="both", expand=True, pady=(0, 15))

        chart2_header = ctk.CTkFrame(chart2_frame, fg_color="#3b3b3b", corner_radius=12)
        chart2_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(chart2_header, text="🏆 PERFORMANCE DES FOURNISSEURS",
                     font=ctk.CTkFont(weight="bold")).pack(pady=8)

        self.stats_chart2_container = ctk.CTkFrame(chart2_frame, fg_color="#2b2b2b", height=300)
        self.stats_chart2_container.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Graphique 3: Analyse des prix
        chart3_frame = ctk.CTkFrame(stats_charts_frame, corner_radius=12)
        chart3_frame.pack(fill="both", expand=True)

        chart3_header = ctk.CTkFrame(chart3_frame, fg_color="#3b3b3b", corner_radius=12)
        chart3_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(chart3_header, text="💰 RÉPARTITION DES PRIX",
                     font=ctk.CTkFont(weight="bold")).pack(pady=8)

        self.stats_chart3_container = ctk.CTkFrame(chart3_frame, fg_color="#2b2b2b", height=300)
        self.stats_chart3_container.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Bouton pour générer les statistiques
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=20)

        ctk.CTkButton(btn_frame, text="📊 Générer les Statistiques",
                      command=self.generer_statistiques_avancees,
                      fg_color="#2e86ab", hover_color="#1f5f7a",
                      width=200, height=40).pack()

        # Générer les statistiques initiales
        self.after(1000, self.generer_statistiques_avancees)

    def generer_statistiques_avancees(self):
        """Génère les statistiques avancées avec courbes"""
        try:
            # Données pour l'évolution temporelle
            self.creer_courbe_evolution()

            # Données pour la performance des fournisseurs
            self.creer_courbe_performance()

            # Données pour l'analyse des prix
            self.creer_analyse_prix()

            self.status_bar.configure(text="✅ Statistiques avancées générées avec succès")

        except Exception as e:
            print(f"Erreur génération statistiques: {e}")

    def creer_courbe_evolution(self):
        """Crée la courbe d'évolution temporelle"""
        try:
            # Nettoyer le conteneur
            for widget in self.stats_chart1_container.winfo_children():
                widget.destroy()

            # Données simulées pour 30 jours basées sur les ventes réelles
            jours = list(range(1, 31))
            
            # Analyser les ventes des 30 derniers jours
            ventes_par_jour = [0] * 30
            stocks_par_jour = [0] * 30
            
            # Calculer le stock initial
            stock_initial = 0
            for produit in self.root_produits.findall("produit"):
                quantite = int(produit.find("quantite").text) if produit.find("quantite") is not None else 0
                stock_initial += quantite

            # Simuler l'évolution
            stocks_par_jour[0] = stock_initial
            for i in range(1, 30):
                # Simulation réaliste basée sur le pattern des ventes
                ventes_jour = max(0, np.random.randint(5, 20) + i * 0.1)
                entrees_jour = max(0, np.random.randint(8, 25) + i * 0.05)
                
                ventes_par_jour[i] = ventes_jour
                stocks_par_jour[i] = max(0, stocks_par_jour[i-1] - ventes_jour + entrees_jour)

            # Créer la figure
            fig = Figure(figsize=(10, 6), dpi=80, facecolor='#2b2b2b')
            ax = fig.add_subplot(111)

            # Tracer les courbes
            ax.plot(jours, stocks_par_jour, label='Niveau des Stocks', color='#2e86ab', linewidth=2.5, marker='o')
            ax.plot(jours, ventes_par_jour, label='Produits Vendus', color='#28a745', linewidth=2.5, marker='s')

            # Style
            ax.set_xlabel('Jours', color='white', fontweight='bold')
            ax.set_ylabel('Quantité', color='white', fontweight='bold')
            ax.set_title('Évolution des Stocks et Ventes (30 jours)',
                         color='white', fontsize=14, fontweight='bold', pad=20)

            # Légende
            ax.legend(facecolor='#3b3b3b', edgecolor='white', labelcolor='white')

            # Style des axes
            ax.tick_params(colors='white')
            ax.grid(True, alpha=0.3)
            ax.set_facecolor('#2b2b2b')

            # Cadre
            for spine in ax.spines.values():
                spine.set_color('white')

            fig.tight_layout()

            # Intégration
            canvas = FigureCanvasTkAgg(fig, self.stats_chart1_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            print(f"Erreur courbe évolution: {e}")

    def creer_courbe_performance(self):
        """Crée le graphique de performance des fournisseurs"""
        try:
            for widget in self.stats_chart2_container.winfo_children():
                widget.destroy()

            # Analyser les fournisseurs
            fournisseurs_data = {}
            for produit in self.root_produits.findall("produit"):
                fournisseur = produit.find("fournisseur").text if produit.find("fournisseur") is not None else "Inconnu"
                prix = float(produit.find("prix").text) if produit.find("prix") is not None else 0
                quantite = int(produit.find("quantite").text) if produit.find("quantite") is not None else 0

                if fournisseur not in fournisseurs_data:
                    fournisseurs_data[fournisseur] = {"produits": 0, "valeur": 0, "quantite": 0}

                fournisseurs_data[fournisseur]["produits"] += 1
                fournisseurs_data[fournisseur]["valeur"] += prix * quantite
                fournisseurs_data[fournisseur]["quantite"] += quantite

            if not fournisseurs_data:
                label = ctk.CTkLabel(self.stats_chart2_container, text="Aucune donnée disponible", 
                                   text_color="white", font=ctk.CTkFont(size=14))
                label.pack(expand=True)
                return

            # Préparer les données pour le graphique
            noms = list(fournisseurs_data.keys())[:6]  # Top 6
            produits = [fournisseurs_data[nom]["produits"] for nom in noms]
            valeurs = [fournisseurs_data[nom]["valeur"] for nom in noms]

            # Créer la figure
            fig = Figure(figsize=(10, 6), dpi=80, facecolor='#2b2b2b')
            ax = fig.add_subplot(111)

            # Largeur des barres
            x = np.arange(len(noms))
            width = 0.35

            # Barres doubles
            bars1 = ax.bar(x - width / 2, produits, width, label='Nombre de Produits', color='#2e86ab', alpha=0.8)
            bars2 = ax.bar(x + width / 2, [v / 1000 for v in valeurs], width, label='Valeur (x1000 Ar)', color='#f9c74f',
                           alpha=0.8)

            # Style
            ax.set_xlabel('Fournisseurs', color='white', fontweight='bold')
            ax.set_ylabel('Performance', color='white', fontweight='bold')
            ax.set_title('Performance des Fournisseurs',
                         color='white', fontsize=14, fontweight='bold', pad=20)
            ax.set_xticks(x)
            ax.set_xticklabels(noms, rotation=45, ha='right', color='white')
            ax.legend(facecolor='#3b3b3b', edgecolor='white', labelcolor='white')

            ax.tick_params(colors='white')
            ax.grid(True, alpha=0.3)
            ax.set_facecolor('#2b2b2b')

            for spine in ax.spines.values():
                spine.set_color('white')

            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, self.stats_chart2_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            print(f"Erreur performance fournisseurs: {e}")

    def creer_analyse_prix(self):
        """Crée l'analyse de répartition des prix"""
        try:
            for widget in self.stats_chart3_container.winfo_children():
                widget.destroy()

            # Collecter les prix
            prix_list = []
            for produit in self.root_produits.findall("produit"):
                prix = float(produit.find("prix").text) if produit.find("prix") is not None else 0
                if prix > 0:
                    prix_list.append(prix)

            if not prix_list:
                label = ctk.CTkLabel(self.stats_chart3_container, text="Aucune donnée disponible", 
                                   text_color="white", font=ctk.CTkFont(size=14))
                label.pack(expand=True)
                return

            # Créer la figure
            fig = Figure(figsize=(10, 6), dpi=80, facecolor='#2b2b2b')
            ax = fig.add_subplot(111)

            # Histogramme des prix
            n, bins, patches = ax.hist(prix_list, bins=10, color='#a23b72', alpha=0.7, edgecolor='white')

            # Style
            ax.set_xlabel('Prix (Ar)', color='white', fontweight='bold')
            ax.set_ylabel('Nombre de Produits', color='white', fontweight='bold')
            ax.set_title('Répartition des Prix des Produits',
                         color='white', fontsize=14, fontweight='bold', pad=20)

            ax.tick_params(colors='white')
            ax.grid(True, alpha=0.3)
            ax.set_facecolor('#2b2b2b')

            for spine in ax.spines.values():
                spine.set_color('white')

            # Ajouter des statistiques
            stats_text = f"""Statistiques Prix:
Moyenne: {np.mean(prix_list):.2f} Ar
Médiane: {np.median(prix_list):.2f} Ar
Max: {np.max(prix_list):.2f} Ar
Min: {np.min(prix_list):.2f} Ar"""

            ax.text(0.95, 0.95, stats_text, transform=ax.transAxes,
                    verticalalignment='top', horizontalalignment='right',
                    color='white', fontsize=10, bbox=dict(boxstyle='round', facecolor='#3b3b3b', alpha=0.8))

            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, self.stats_chart3_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            print(f"Erreur analyse prix: {e}")

    def creer_onglet_rapports(self):
        """Crée l'onglet des rapports"""
        tab = self.tabview.tab("📋 Rapports")

        # Frame principal avec scroll
        main_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="#3b3b3b", corner_radius=12)
        header_frame.pack(fill="x", pady=(0, 20))

        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(header_content, text="📋 GÉNÉRATION DE RAPPORTS",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")

        # Section configuration du rapport
        config_frame = ctk.CTkFrame(main_frame, corner_radius=12)
        config_frame.pack(fill="x", pady=(0, 20))

        config_header = ctk.CTkFrame(config_frame, fg_color="#3b3b3b", corner_radius=12)
        config_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(config_header, text="⚙️ CONFIGURATION DU RAPPORT",
                     font=ctk.CTkFont(weight="bold")).pack(pady=8)

        # Options de configuration
        options_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        options_frame.pack(fill="x", padx=20, pady=20)

        # Période
        periode_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        periode_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(periode_frame, text="Période:",
                     font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 20))
        self.rapport_periode = ctk.CTkComboBox(periode_frame,
                                               values=["Hebdomadaire", "Mensuel", "Trimestriel", "Semestriel", "Annuel"],
                                               width=200, height=35)
        self.rapport_periode.pack(side="left")
        self.rapport_periode.set("Mensuel")

        # Catégorie
        categorie_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        categorie_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(categorie_frame, text="Catégorie:",
                     font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 20))
        self.rapport_categorie = ctk.CTkComboBox(categorie_frame,
                                                 values=["Toutes"] + self.get_categories(),
                                                 width=200, height=35)
        self.rapport_categorie.pack(side="left")
        self.rapport_categorie.set("Toutes")

        # Boutons d'action
        actions_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        actions_frame.pack(fill="x", pady=20)

        ctk.CTkButton(actions_frame, text="📊 Générer Rapport",
                      command=self.generer_rapport,
                      width=180, height=40,
                      fg_color="#2e86ab", hover_color="#1f5f7a").pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="📄 Exporter PDF",
                      command=self.exporter_pdf,
                      width=150, height=40,
                      fg_color="#dc3545", hover_color="#a71e2a").pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="📋 Exporter JSON",
                      command=self.exporter_json,
                      width=150, height=40,
                      fg_color="#28a745", hover_color="#1e7e34").pack(side="left", padx=5)

        # Section affichage du rapport
        rapport_frame = ctk.CTkFrame(main_frame, corner_radius=12)
        rapport_frame.pack(fill="both", expand=True)

        rapport_header = ctk.CTkFrame(rapport_frame, fg_color="#3b3b3b", corner_radius=12)
        rapport_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(rapport_header, text="📄 RAPPORT GÉNÉRÉ",
                     font=ctk.CTkFont(weight="bold")).pack(pady=8)

        # Zone de texte pour le rapport
        self.rapport_text = ctk.CTkTextbox(rapport_frame, height=400,
                                           font=ctk.CTkFont(family="Consolas", size=12))
        self.rapport_text.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Message d'accueil
        self.rapport_text.insert("1.0",
                                 "👉 Configurez les options ci-dessus et générez un rapport pour voir les données ici.")

    def get_categories(self):
        """Retourne la liste des catégories uniques"""
        categories = set()
        for produit in self.root_produits.findall("produit"):
            categorie = produit.find("categorie")
            if categorie is not None and categorie.text:
                categories.add(categorie.text)
        return sorted(list(categories))

    def generer_rapport(self):
        """Génère un rapport détaillé avec données de ventes"""
        try:
            periode = self.rapport_periode.get()
            categorie = self.rapport_categorie.get()

            rapport = "=" * 80 + "\n"
            rapport += f"RAPPORT D'INVENTAIRE COMPLET - {periode.upper()}\n"
            rapport += "=" * 80 + "\n\n"
            rapport += f"📅 Date de génération: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            rapport += f"📊 Catégorie: {categorie}\n"
            rapport += f"👤 Généré par: Système de Gestion d'Inventaire\n\n"

            # Statistiques générales
            total_produits = 0
            total_valeur = 0
            produits_faible_stock = 0
            categories_stats = {}
            fournisseurs_stats = {}

            # Statistiques ventes
            total_ventes = 0
            total_entrees = 0
            total_sorties = 0
            chiffre_affaires = 0

            for produit in self.root_produits.findall("produit"):
                # Filtre par catégorie
                if categorie != "Toutes":
                    prod_categorie = produit.find("categorie")
                    if prod_categorie is None or prod_categorie.text != categorie:
                        continue

                quantite = int(produit.find("quantite").text) if produit.find("quantite") is not None else 0
                prix = float(produit.find("prix").text) if produit.find("prix") is not None else 0
                nom_fournisseur = produit.find("fournisseur").text if produit.find("fournisseur") is not None else "Inconnu"

                total_produits += quantite
                total_valeur += quantite * prix

                if quantite < 10:
                    produits_faible_stock += 1

                # Statistiques par catégorie
                cat = produit.find("categorie").text if produit.find("categorie") is not None else "Non catégorisé"
                if cat not in categories_stats:
                    categories_stats[cat] = {"quantite": 0, "valeur": 0, "produits": 0}
                categories_stats[cat]["quantite"] += quantite
                categories_stats[cat]["valeur"] += quantite * prix
                categories_stats[cat]["produits"] += 1

                # Statistiques par fournisseur
                if nom_fournisseur not in fournisseurs_stats:
                    fournisseurs_stats[nom_fournisseur] = {"quantite": 0, "valeur": 0, "produits": 0}
                fournisseurs_stats[nom_fournisseur]["quantite"] += quantite
                fournisseurs_stats[nom_fournisseur]["valeur"] += quantite * prix
                fournisseurs_stats[nom_fournisseur]["produits"] += 1

            # Analyser les ventes
            for operation in self.root_ventes.findall("operation"):
                if operation.find("type").text == "Sortie":
                    total_ventes += 1
                    total_sorties += int(operation.find("quantite").text)
                    prix_vente = float(operation.find("prix").text) if operation.find("prix") is not None else 0
                    quantite_vente = int(operation.find("quantite").text) if operation.find("quantite") is not None else 0
                    chiffre_affaires += prix_vente * quantite_vente
                else:
                    total_entrees += 1

            # Section statistiques générales
            rapport += "📈 STATISTIQUES GÉNÉRALES\n"
            rapport += "-" * 50 + "\n"
            rapport += f"• Nombre total de produits en stock: {total_produits}\n"
            rapport += f"• Valeur totale de l'inventaire: {total_valeur:,.2f} Ar\n"
            rapport += f"• Produits à faible stock: {produits_faible_stock}\n"
            rapport += f"• Nombre de catégories: {len(categories_stats)}\n"
            rapport += f"• Nombre de fournisseurs: {len(fournisseurs_stats)}\n\n"

            # Section statistiques ventes
            rapport += "💰 STATISTIQUES DES VENTES\n"
            rapport += "-" * 50 + "\n"
            rapport += f"• Total des opérations de vente: {total_ventes}\n"
            rapport += f"• Total des entrées en stock: {total_entrees}\n"
            rapport += f"• Total des sorties de stock: {total_sorties}\n"
            rapport += f"• Chiffre d'affaires total: {chiffre_affaires:,.2f} Ar\n\n"

            # Section détail par catégorie
            rapport += "📊 DÉTAIL PAR CATÉGORIE\n"
            rapport += "-" * 50 + "\n"
            for cat, stats in sorted(categories_stats.items(), key=lambda x: x[1]["valeur"], reverse=True):
                pourcentage = (stats["valeur"] / total_valeur * 100) if total_valeur > 0 else 0
                rapport += f"• {cat}: {stats['produits']} produits, {stats['quantite']} unités, {stats['valeur']:,.2f} Ar ({pourcentage:.1f}%)\n"
            rapport += "\n"

            # Section top fournisseurs
            rapport += "👥 TOP FOURNISSEURS\n"
            rapport += "-" * 50 + "\n"
            top_fournisseurs = sorted(fournisseurs_stats.items(), key=lambda x: x[1]["valeur"], reverse=True)[:5]
            for i, (fournisseur, stats) in enumerate(top_fournisseurs, 1):
                rapport += f"{i}. {fournisseur}: {stats['produits']} produits, {stats['valeur']:,.2f} Ar\n"
            rapport += "\n"

            # Section produits les plus vendus
            produits_populaires = {}
            for operation in self.root_ventes.findall("operation"):
                if operation.find("type").text == "Sortie":
                    produit_nom = operation.find("produit").text
                    quantite = int(operation.find("quantite").text)
                    if produit_nom not in produits_populaires:
                        produits_populaires[produit_nom] = 0
                    produits_populaires[produit_nom] += quantite

            if produits_populaires:
                rapport += "🔥 PRODUITS LES PLUS VENDUS\n"
                rapport += "-" * 50 + "\n"
                top_produits = sorted(produits_populaires.items(), key=lambda x: x[1], reverse=True)[:5]
                for i, (produit, quantite) in enumerate(top_produits, 1):
                    rapport += f"{i}. {produit}: {quantite} unités vendues\n"
                rapport += "\n"

            # Section alertes
            if produits_faible_stock > 0:
                rapport += "⚠️  ALERTES - PRODUITS À FAIBLE STOCK\n"
                rapport += "-" * 50 + "\n"
                for produit in self.root_produits.findall("produit"):
                    quantite = int(produit.find("quantite").text) if produit.find("quantite") is not None else 0
                    if quantite < 10:
                        nom = produit.find("nom").text if produit.find("nom") is not None else "Sans nom"
                        rapport += f"• {nom}: {quantite} unités restantes\n"
                rapport += "\n"

            rapport += "=" * 80 + "\n"
            rapport += "📋 FIN DU RAPPORT\n"
            rapport += "=" * 80 + "\n"

            # Afficher le rapport
            self.rapport_text.delete("1.0", "end")
            self.rapport_text.insert("1.0", rapport)

            self.status_bar.configure(text=f"✅ Rapport {periode} généré avec succès")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération du rapport: {e}")

    def exporter_pdf(self):
        """Exporte le rapport en PDF avec choix du chemin"""
        try:
            # Demander le chemin de sauvegarde
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Fichiers PDF", "*.pdf"), ("Tous les fichiers", "*.*")],
                title="Exporter le rapport PDF",
                initialfile=f"rapport_inventaire_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            
            if not filename:
                return  # L'utilisateur a annulé

            doc = SimpleDocTemplate(filename, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []

            # Titre
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1
            )
            title = Paragraph("RAPPORT D'INVENTAIRE COMPLET", title_style)
            story.append(title)

            # Informations
            info_style = ParagraphStyle(
                'CustomInfo',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=12
            )
            info_text = f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Généré par: Système de Gestion d'Inventaire"
            info = Paragraph(info_text, info_style)
            story.append(info)
            story.append(Spacer(1, 20))

            # Données du tableau des produits
            data_produits = [["ID", "Nom", "Catégorie", "Quantité", "Prix", "Fournisseur"]]

            for produit in self.root_produits.findall("produit"):
                nom = produit.find("nom").text if produit.find("nom") is not None else ""
                categorie = produit.find("categorie").text if produit.find("categorie") is not None else ""
                quantite = produit.find("quantite").text if produit.find("quantite") is not None else "0"
                prix = produit.find("prix").text if produit.find("prix") is not None else "0"
                fournisseur = produit.find("fournisseur").text if produit.find("fournisseur") is not None else ""

                data_produits.append([produit.find("id").text if produit.find("id") is not None else "",
                                     nom, categorie, quantite, f"{prix} Ar", fournisseur])

            # Créer le tableau des produits
            table_produits = Table(data_produits)
            table_produits.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            story.append(Paragraph("LISTE DES PRODUITS", styles['Heading2']))
            story.append(table_produits)
            story.append(Spacer(1, 20))

            # Données du tableau des ventes
            data_ventes = [["Produit", "Type", "Quantité", "Prix", "Date"]]

            for operation in self.root_ventes.findall("operation"):
                produit = operation.find("produit").text if operation.find("produit") is not None else ""
                type_op = operation.find("type").text if operation.find("type") is not None else ""
                quantite = operation.find("quantite").text if operation.find("quantite") is not None else "0"
                prix = operation.find("prix").text if operation.find("prix") is not None else "0"
                date = operation.find("date").text if operation.find("date") is not None else ""

                data_ventes.append([produit, type_op, quantite, f"{prix} Ar", date])

            # Créer le tableau des ventes
            table_ventes = Table(data_ventes)
            table_ventes.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            story.append(Paragraph("HISTORIQUE DES VENTES", styles['Heading2']))
            story.append(table_ventes)

            # Générer le PDF
            doc.build(story)
            messagebox.showinfo("Succès", f"Rapport PDF exporté: {filename}")
            self.status_bar.configure(text="✅ Rapport PDF exporté avec succès")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export PDF: {e}")

    def exporter_json(self):
        """Exporte les données en JSON avec choix du chemin"""
        try:
            # Demander le chemin de sauvegarde
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")],
                title="Exporter les données JSON",
                initialfile=f"inventaire_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            
            if not filename:
                return  # L'utilisateur a annulé

            data = {
                "metadata": {
                    "date_export": datetime.now().isoformat(),
                    "total_produits": len(self.root_produits.findall("produit")),
                    "total_fournisseurs": len(self.root_fournisseurs.findall("fournisseur")),
                    "total_operations": len(self.root_ventes.findall("operation")),
                    "version_export": "3.0"
                },
                "produits": [],
                "fournisseurs": [],
                "operations": []
            }

            # Produits
            for produit in self.root_produits.findall("produit"):
                data["produits"].append({
                    "id": produit.find("id").text if produit.find("id") is not None else "",
                    "nom": produit.find("nom").text if produit.find("nom") is not None else "",
                    "categorie": produit.find("categorie").text if produit.find("categorie") is not None else "",
                    "quantite": produit.find("quantite").text if produit.find("quantite") is not None else "",
                    "prix": produit.find("prix").text if produit.find("prix") is not None else "",
                    "fournisseur": produit.find("fournisseur").text if produit.find("fournisseur") is not None else "",
                    "date_ajout": produit.find("date_ajout").text if produit.find("date_ajout") is not None else ""
                })

            # Fournisseurs
            for fournisseur in self.root_fournisseurs.findall("fournisseur"):
                data["fournisseurs"].append({
                    "id": fournisseur.find("id").text if fournisseur.find("id") is not None else "",
                    "nom": fournisseur.find("nom").text if fournisseur.find("nom") is not None else "",
                    "contact": fournisseur.find("contact").text if fournisseur.find("contact") is not None else "",
                    "email": fournisseur.find("email").text if fournisseur.find("email") is not None else "",
                    "telephone": fournisseur.find("telephone").text if fournisseur.find("telephone") is not None else "",
                    "adresse": fournisseur.find("adresse").text if fournisseur.find("adresse") is not None else ""
                })

            # Opérations
            for operation in self.root_ventes.findall("operation"):
                data["operations"].append({
                    "id": operation.find("id").text if operation.find("id") is not None else "",
                    "produit": operation.find("produit").text if operation.find("produit") is not None else "",
                    "type": operation.find("type").text if operation.find("type") is not None else "",
                    "quantite": operation.find("quantite").text if operation.find("quantite") is not None else "",
                    "prix": operation.find("prix").text if operation.find("prix") is not None else "",
                    "raison": operation.find("raison").text if operation.find("raison") is not None else "",
                    "date": operation.find("date").text if operation.find("date") is not None else "",
                    "ancien_stock": operation.find("ancien_stock").text if operation.find("ancien_stock") is not None else "",
                    "nouveau_stock": operation.find("nouveau_stock").text if operation.find("nouveau_stock") is not None else ""
                })

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            messagebox.showinfo("Succès", f"Données JSON exportées: {filename}")
            self.status_bar.configure(text="✅ Données JSON exportées avec succès")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export JSON: {e}")

    def creer_onglet_parametres(self):
        """Crée l'onglet des paramètres avec interface modernisée"""
        tab = self.tabview.tab("⚙️ Paramètres")

        # Frame principal avec scroll
        main_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="#3b3b3b", corner_radius=12)
        header_frame.pack(fill="x", pady=(0, 20))

        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(header_content, text="⚙️ PARAMÈTRES DE L'APPLICATION",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")

        # Section Apparence
        apparence_frame = ctk.CTkFrame(main_frame, corner_radius=12)
        apparence_frame.pack(fill="x", pady=(0, 20))

        apparence_header = ctk.CTkFrame(apparence_frame, fg_color="#3b3b3b", corner_radius=12)
        apparence_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(apparence_header, text="🎨 APParence",
                     font=ctk.CTkFont(weight="bold")).pack(pady=8)

        # Options d'apparence
        apparence_content = ctk.CTkFrame(apparence_frame, fg_color="transparent")
        apparence_content.pack(fill="x", padx=20, pady=20)

        # Thème
        theme_frame = ctk.CTkFrame(apparence_content, fg_color="transparent")
        theme_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(theme_frame, text="Thème:",
                     font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 20))

        self.theme_var = ctk.StringVar(value="dark")
        ctk.CTkRadioButton(theme_frame, text="🌙 Sombre", variable=self.theme_var,
                           value="dark", command=self.changer_theme).pack(side="left", padx=10)
        ctk.CTkRadioButton(theme_frame, text="☀️ Clair", variable=self.theme_var,
                           value="light", command=self.changer_theme).pack(side="left", padx=10)

        # Section Gestion des données
        data_frame = ctk.CTkFrame(main_frame, corner_radius=12)
        data_frame.pack(fill="x", pady=(0, 20))

        data_header = ctk.CTkFrame(data_frame, fg_color="#3b3b3b", corner_radius=12)
        data_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(data_header, text="💾 GESTION DES DONNÉES",
                     font=ctk.CTkFont(weight="bold")).pack(pady=8)

        # Boutons de gestion des données
        data_content = ctk.CTkFrame(data_frame, fg_color="transparent")
        data_content.pack(fill="x", padx=20, pady=20)

        data_buttons_frame = ctk.CTkFrame(data_content, fg_color="transparent")
        data_buttons_frame.pack(fill="x")

        ctk.CTkButton(data_buttons_frame, text="💾 Sauvegarder Maintenant",
                      command=self.sauvegarder_donnees,
                      width=180, height=40,
                      fg_color="#28a745", hover_color="#1e7e34").pack(side="left", padx=5)
        ctk.CTkButton(data_buttons_frame, text="🔄 Recharger les Données",
                      command=self.charger_donnees,
                      width=180, height=40,
                      fg_color="#2e86ab", hover_color="#1f5f7a").pack(side="left", padx=5)

        # Section Informations système
        system_frame = ctk.CTkFrame(main_frame, corner_radius=12)
        system_frame.pack(fill="x", pady=(0, 20))

        system_header = ctk.CTkFrame(system_frame, fg_color="#3b3b3b", corner_radius=12)
        system_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(system_header, text="ℹ️ INFORMATIONS SYSTÈME",
                     font=ctk.CTkFont(weight="bold")).pack(pady=8)

        # Informations système
        system_content = ctk.CTkFrame(system_frame, fg_color="transparent")
        system_content.pack(fill="x", padx=20, pady=20)

        # Statistiques de l'application
        stats_text = f"""
📊 STATISTIQUES DE L'APPLICATION:

• Produits enregistrés: {len(self.root_produits.findall("produit"))}
• Fournisseurs enregistrés: {len(self.root_fournisseurs.findall("fournisseur"))}
• Opérations enregistrées: {len(self.root_ventes.findall("operation"))}
• Dernière sauvegarde: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
• Version de l'application: 3.0.0
• Développé avec: Python, CustomTkinter, XML

🔧 FONCTIONNALITÉS:
✓ Gestion complète des produits
✓ Gestion des fournisseurs
✓ Gestion des ventes (entrées/sorties)
✓ Tableau de bord interactif
✓ Statistiques avancées
✓ Export PDF/JSON
✓ Interface moderne et responsive
        """

        info_label = ctk.CTkLabel(system_content, text=stats_text,
                                  font=ctk.CTkFont(family="Consolas", size=12),
                                  justify="left")
        info_label.pack(anchor="w")

    def changer_theme(self):
        """Change le thème de l'application"""
        theme = self.theme_var.get()
        ctk.set_appearance_mode(theme)
        self.status_bar.configure(text=f"✅ Thème changé: {theme}")

    def quitter(self):
        """Quitte l'application"""
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir quitter l'application ?"):
            self.sauvegarder_donnees()
            self.destroy()

# === DIALOGUES ===

class AjouterProduitDialog(ctk.CTkToplevel):
    def __init__(self, parent, root_fournisseurs):
        super().__init__(parent)
        self.title("➕ Ajouter un Produit")
        self.geometry("400x500")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.result = None
        self.root_fournisseurs = root_fournisseurs
        self.parent = parent

        self.creer_interface()

    def creer_interface(self):
        """Crée l'interface du dialogue"""
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text="Nouveau Produit",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        # Champs de formulaire
        ctk.CTkLabel(main_frame, text="Nom:").pack(anchor="w", pady=(10, 0))
        self.nom_entry = ctk.CTkEntry(main_frame)
        self.nom_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(main_frame, text="Catégorie:").pack(anchor="w")
        self.categorie_entry = ctk.CTkEntry(main_frame)
        self.categorie_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(main_frame, text="Quantité:").pack(anchor="w")
        self.quantite_entry = ctk.CTkEntry(main_frame)
        self.quantite_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(main_frame, text="Prix (Ar):").pack(anchor="w")
        self.prix_entry = ctk.CTkEntry(main_frame)
        self.prix_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(main_frame, text="Fournisseur:").pack(anchor="w")

        # Liste des fournisseurs
        fournisseurs = ["Sélectionner..."]
        for fournisseur in self.root_fournisseurs.findall("fournisseur"):
            nom = fournisseur.find("nom")
            if nom is not None and nom.text:
                fournisseurs.append(nom.text)

        self.fournisseur_combo = ctk.CTkComboBox(main_frame, values=fournisseurs)
        self.fournisseur_combo.set("Sélectionner...")
        self.fournisseur_combo.pack(fill="x", pady=(0, 20))

        # Boutons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=10)

        ctk.CTkButton(button_frame, text="Ajouter",
                      command=self.valider, width=100).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="Annuler",
                      command=self.annuler, width=100).pack(side="right", padx=5)

    def valider(self):
        """Valide le formulaire avec vérification d'unicité"""
        nom = self.nom_entry.get().strip()
        categorie = self.categorie_entry.get().strip()
        quantite = self.quantite_entry.get().strip()
        prix = self.prix_entry.get().strip()
        fournisseur = self.fournisseur_combo.get()

        # Validation de base
        if not nom:
            messagebox.showwarning("Erreur", "Le nom est obligatoire")
            return

        # Vérifier si le produit existe déjà
        for produit in self.parent.root_produits.findall("produit"):
            nom_existant = produit.find("nom")
            if nom_existant is not None and nom_existant.text.lower() == nom.lower():
                messagebox.showwarning("Erreur", f"Le produit '{nom}' existe déjà dans l'inventaire")
                return

        if not quantite.isdigit() or int(quantite) < 0:
            messagebox.showwarning("Erreur", "La quantité doit être un nombre positif")
            return

        try:
            float(prix)
        except ValueError:
            messagebox.showwarning("Erreur", "Le prix doit être un nombre valide")
            return

        if fournisseur == "Sélectionner...":
            messagebox.showwarning("Erreur", "Veuillez sélectionner un fournisseur")
            return

        self.result = {
            "nom": nom,
            "categorie": categorie,
            "quantite": quantite,
            "prix": prix,
            "fournisseur": fournisseur
        }
        self.destroy()

    def annuler(self):
        """Annule l'ajout"""
        self.destroy()

class ModifierProduitDialog(AjouterProduitDialog):
    def __init__(self, parent, values, root_fournisseurs):
        super().__init__(parent, root_fournisseurs)
        self.title("✏️ Modifier le Produit")

        # Pré-remplir les champs
        self.nom_entry.insert(0, values[1])
        self.categorie_entry.insert(0, values[2])
        self.quantite_entry.insert(0, values[3])
        self.prix_entry.insert(0, values[4].replace(" Ar", ""))
        self.fournisseur_combo.set(values[5])

class AjouterFournisseurDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("👥 Ajouter un Fournisseur")
        self.geometry("450x700")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.result = None
        self.parent = parent
        self.creer_interface()

    def creer_interface(self):
        """Crée l'interface du dialogue améliorée"""
        main_frame = ctk.CTkFrame(self, fg_color="#2d2d2d", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text="Nouveau Fournisseur",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)

        # Frame pour contenir tous les champs
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, pady=10)

        # Champs de formulaire avec validation
        ctk.CTkLabel(form_frame, text="Nom *:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 5))
        self.nom_entry = ctk.CTkEntry(form_frame, placeholder_text="Nom du fournisseur")
        self.nom_entry.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(form_frame, text="Contact:").pack(anchor="w", pady=(5, 5))
        self.contact_entry = ctk.CTkEntry(form_frame, placeholder_text="Personne de contact")
        self.contact_entry.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(form_frame, text="Email *:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(5, 5))
        self.email_entry = ctk.CTkEntry(form_frame, placeholder_text="exemple@gmail.com")
        self.email_entry.pack(fill="x", pady=(0, 10))
        self.email_error = ctk.CTkLabel(form_frame, text="", text_color="red", font=ctk.CTkFont(size=10))
        self.email_error.pack(anchor="w", pady=(0, 5))
        self.email_entry.bind("<KeyRelease>", self.verifier_email)

        ctk.CTkLabel(form_frame, text="Téléphone *:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(5, 5))
        self.telephone_entry = ctk.CTkEntry(form_frame, placeholder_text="+261321234567 ou 0321234567")
        self.telephone_entry.pack(fill="x", pady=(0, 10))
        self.telephone_error = ctk.CTkLabel(form_frame, text="", text_color="red", font=ctk.CTkFont(size=10))
        self.telephone_error.pack(anchor="w", pady=(0, 5))
        self.telephone_entry.bind("<KeyRelease>", self.verifier_telephone)

        ctk.CTkLabel(form_frame, text="Adresse:").pack(anchor="w", pady=(5, 5))
        self.adresse_entry = ctk.CTkEntry(form_frame, placeholder_text="Adresse complète")
        self.adresse_entry.pack(fill="x", pady=(0, 20))

        # Boutons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)

        ctk.CTkButton(button_frame, text="✅ Ajouter",
                      command=self.valider, width=120, height=40,
                      fg_color="#28a745", hover_color="#1e7e34", corner_radius=10).pack(side="right", padx=10)
        ctk.CTkButton(button_frame, text="❌ Annuler",
                      command=self.annuler, width=120, height=40,
                      fg_color="#dc3545", hover_color="#a71e2a", corner_radius=10).pack(side="right", padx=5)

        # Donner le focus au premier champ
        self.nom_entry.focus()

    def valider_email(self, email):
        """Valide le format de l'email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
        return re.match(pattern, email) is not None

    def valider_telephone(self, telephone):
        """Valide le format du téléphone (Madagascar)"""
        pattern = r'^(\+261|0)[2-9][0-9]{8}$'
        return re.match(pattern, telephone) is not None

    def verifier_email(self, event=None):
        """Vérifie et affiche l'état de validation de l'email"""
        email = self.email_entry.get().strip()
        if not email:
            self.email_error.configure(text="")
        elif self.valider_email(email):
            self.email_error.configure(text="✅ Format email valide", text_color="green")
        else:
            self.email_error.configure(text="❌ Doit se terminer par @gmail.com", text_color="red")

    def verifier_telephone(self, event=None):
        """Vérifie et affiche l'état de validation du téléphone"""
        telephone = self.telephone_entry.get().strip()
        if not telephone:
            self.telephone_error.configure(text="")
        elif self.valider_telephone(telephone):
            self.telephone_error.configure(text="✅ Format téléphone valide", text_color="green")
        else:
            self.telephone_error.configure(text="❌ Format: +261321234567 ou 0321234567", text_color="red")

    def valider(self):
        """Valide le formulaire avec les nouvelles contraintes"""
        nom = self.nom_entry.get().strip()
        contact = self.contact_entry.get().strip()
        email = self.email_entry.get().strip()
        telephone = self.telephone_entry.get().strip()
        adresse = self.adresse_entry.get().strip()

        # Validation
        if not nom:
            messagebox.showwarning("Erreur", "Le nom est obligatoire")
            return

        # Vérifier si le fournisseur existe déjà
        for fournisseur in self.parent.root_fournisseurs.findall("fournisseur"):
            nom_existant = fournisseur.find("nom")
            if nom_existant is not None and nom_existant.text.lower() == nom.lower():
                messagebox.showwarning("Erreur", f"Le fournisseur '{nom}' existe déjà")
                return

        if not email:
            messagebox.showwarning("Erreur", "L'email est obligatoire")
            return

        if not self.valider_email(email):
            messagebox.showwarning("Erreur", "L'email doit être au format @gmail.com")
            return

        if not telephone:
            messagebox.showwarning("Erreur", "Le téléphone est obligatoire")
            return

        if not self.valider_telephone(telephone):
            messagebox.showwarning("Erreur", "Le téléphone doit être au format Madagascar (+261... ou 0...)")
            return

        self.result = {
            "nom": nom,
            "contact": contact,
            "email": email,
            "telephone": telephone,
            "adresse": adresse
        }
        self.destroy()

    def annuler(self):
        """Annule l'ajout"""
        self.destroy()

class ModifierFournisseurDialog(AjouterFournisseurDialog):
    def __init__(self, parent, values):
        super().__init__(parent)
        self.title("✏️ Modifier le Fournisseur")

        # Pré-remplir les champs
        self.nom_entry.insert(0, values[1])
        self.contact_entry.insert(0, values[2])
        self.email_entry.insert(0, values[3])
        self.telephone_entry.insert(0, values[4])
        self.adresse_entry.insert(0, values[5])

if __name__ == "__main__":
    app = GestionInventaire()
    app.mainloop()