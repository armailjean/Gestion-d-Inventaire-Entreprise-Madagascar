import customtkinter as ctk
from tkinter import ttk, messagebox
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

# Configuration de l'apparence
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class GestionInventaire(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🏢 Gestion d'Inventaire d'Entreprise")
        self.geometry("1400x800")
        self.minsize(1200, 700)

        # Créer les fichiers XML s'ils n'existent pas
        self.creer_fichiers_xml()

        # Charger les données
        self.charger_donnees()

        # Interface utilisateur
        self.creer_interface()

    def creer_fichiers_xml(self):
        """Crée les fichiers XML s'ils n'existent pas"""
        if not os.path.exists("produits.xml"):
            root = ET.Element("inventaire")
            tree = ET.ElementTree(root)
            tree.write("produits.xml", encoding="utf-8", xml_declaration=True)

        if not os.path.exists("fournisseurs.xml"):
            root = ET.Element("fournisseurs")
            tree = ET.ElementTree(root)
            tree.write("fournisseurs.xml", encoding="utf-8", xml_declaration=True)

    def charger_donnees(self):
        """Charge les données depuis les fichiers XML"""
        try:
            # Charger produits
            tree = ET.parse("produits.xml")
            self.root_produits = tree.getroot()

            # Charger fournisseurs
            tree = ET.parse("fournisseurs.xml")
            self.root_fournisseurs = tree.getroot()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des données: {e}")

    def sauvegarder_donnees(self):
        """Sauvegarde les données dans les fichiers XML"""
        try:
            # Sauvegarder produits
            tree = ET.ElementTree(self.root_produits)
            tree.write("produits.xml", encoding="utf-8", xml_declaration=True)

            # Sauvegarder fournisseurs
            tree = ET.ElementTree(self.root_fournisseurs)
            tree.write("fournisseurs.xml", encoding="utf-8", xml_declaration=True)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {e}")

    def creer_interface(self):
        """Crée l'interface graphique"""
        # Configuration du style
        self.configure(fg_color="#2b2b2b")

        # Frame principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Header avec titre et boutons rapides
        header_frame = ctk.CTkFrame(self.main_frame, height=80, fg_color="#3b3b3b")
        header_frame.pack(fill="x", pady=(0, 15))
        header_frame.pack_propagate(False)

        # Titre avec icône
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", fill="y", padx=20)

        title_label = ctk.CTkLabel(title_frame, text="🏢 GESTION D'INVENTAIRE ENTREPRISE",
                                   font=ctk.CTkFont(size=22, weight="bold"),
                                   text_color="#ffffff")
        title_label.pack(pady=20)

        # Boutons rapides dans le header
        quick_actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        quick_actions_frame.pack(side="right", fill="y", padx=20)

        ctk.CTkButton(quick_actions_frame, text="📦 Ajouter Produit",
                      command=self.ajouter_produit, width=140, height=35,
                      fg_color="#2e86ab", hover_color="#1f5f7a").pack(side="left", padx=5)
        ctk.CTkButton(quick_actions_frame, text="👥 Ajouter Fournisseur",
                      command=self.ajouter_fournisseur, width=160, height=35,
                      fg_color="#a23b72", hover_color="#7a2c55").pack(side="left", padx=5)
        ctk.CTkButton(quick_actions_frame, text="📊 Générer Rapport",
                      command=self.generer_rapport, width=150, height=35,
                      fg_color="#28a745", hover_color="#1e7e34").pack(side="left", padx=5)

        # Barre de statut
        self.status_bar = ctk.CTkLabel(self.main_frame, text="✅ Système prêt - Chargement des données terminé",
                                       anchor="w", font=ctk.CTkFont(size=12),
                                       text_color="#a0a0a0")
        self.status_bar.pack(fill="x", pady=(10, 5))

        # Onglets avec style amélioré
        self.tabview = ctk.CTkTabview(self.main_frame,
                                      segmented_button_fg_color="#3b3b3b",
                                      segmented_button_selected_color="#2e86ab",
                                      segmented_button_unselected_color="#4a4a4a",
                                      segmented_button_unselected_hover_color="#5a5a5a")
        self.tabview.pack(fill="both", expand=True)

        # Créer les onglets
        self.tabview.add("📊 Tableau de Bord")
        self.tabview.add("📦 Produits")
        self.tabview.add("👥 Fournisseurs")
        self.tabview.add("📈 Statistiques")
        self.tabview.add("📋 Rapports")
        self.tabview.add("⚙️ Paramètres")

        # Configurer chaque onglet
        self.creer_onglet_tableau_de_bord()
        self.creer_onglet_produits()
        self.creer_onglet_fournisseurs()
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
            {"title": "💰 VALEUR TOTALE", "value": "0 €", "color": "#28a745", "icon": "💰"},
            {"title": "⚠️ FAIBLE STOCK", "value": "0", "color": "#ff6b6b", "icon": "⚠️"},
            {"title": "📈 CATÉGORIES", "value": "0", "color": "#f9c74f", "icon": "📈"},
            {"title": "🏆 FOURNISSEUR TOP", "value": "-", "color": "#7209b7", "icon": "🏆"}
        ]

        self.kpi_labels = {}
        for i, kpi in enumerate(kpis):
            row = i // 3
            col = i % 3
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

        self.chart1_container = ctk.CTkFrame(chart1_frame, fg_color="#2b2b2b")
        self.chart1_container.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Graphique des fournisseurs
        chart2_frame = ctk.CTkFrame(charts_row, corner_radius=12)
        chart2_frame.pack(side="right", fill="both", expand=True, padx=(8, 0))

        chart2_header = ctk.CTkFrame(chart2_frame, fg_color="#3b3b3b", corner_radius=12)
        chart2_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(chart2_header, text="👥 TOP FOURNISSEURS",
                     font=ctk.CTkFont(weight="bold")).pack(pady=8)

        self.chart2_container = ctk.CTkFrame(chart2_frame, fg_color="#2b2b2b")
        self.chart2_container.pack(fill="both", expand=True, padx=12, pady=(0, 12))

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

            # Analyser les produits
            for produit in self.root_produits.findall("produit"):
                quantite = int(produit.find("quantite").text) if produit.find("quantite") is not None else 0
                prix = float(produit.find("prix").text) if produit.find("prix") is not None else 0
                categorie = produit.find("categorie").text if produit.find(
                    "categorie") is not None else "Non catégorisé"
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

            # Mettre à jour les graphiques
            self.creer_graphique_categories(categories)
            self.creer_graphique_fournisseurs(fournisseurs_stats)

            # Mettre à jour le tableau des alertes
            self.mettre_a_jour_produits_faible_stock()

            # Mettre à jour la barre de statut
            self.status_bar.configure(
                text=f"✅ Tableau de bord actualisé - {total_produits} produits, {total_valeur:,.2f} Ar de valeur totale")

        except Exception as e:
            print(f"Erreur lors de l'actualisation du tableau de bord: {e}")

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

    def creer_onglet_statistiques(self):
        """Crée l'onglet des statistiques avancées avec courbes"""
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

        # Graphique 1: Évolution temporelle (simulée)
        chart1_frame = ctk.CTkFrame(stats_charts_frame, corner_radius=12)
        chart1_frame.pack(fill="both", expand=True, pady=(0, 15))

        chart1_header = ctk.CTkFrame(chart1_frame, fg_color="#3b3b3b", corner_radius=12)
        chart1_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(chart1_header, text="📈 ÉVOLUTION DES STOCKS (30 JOURS)",
                     font=ctk.CTkFont(weight="bold")).pack(pady=8)

        self.stats_chart1_container = ctk.CTkFrame(chart1_frame, fg_color="#2b2b2b", height=300)
        self.stats_chart1_container.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.stats_chart1_container.pack_propagate(False)

        # Graphique 2: Performance des fournisseurs
        chart2_frame = ctk.CTkFrame(stats_charts_frame, corner_radius=12)
        chart2_frame.pack(fill="both", expand=True, pady=(0, 15))

        chart2_header = ctk.CTkFrame(chart2_frame, fg_color="#3b3b3b", corner_radius=12)
        chart2_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(chart2_header, text="🏆 PERFORMANCE DES FOURNISSEURS",
                     font=ctk.CTkFont(weight="bold")).pack(pady=8)

        self.stats_chart2_container = ctk.CTkFrame(chart2_frame, fg_color="#2b2b2b", height=300)
        self.stats_chart2_container.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.stats_chart2_container.pack_propagate(False)

        # Graphique 3: Analyse des prix
        chart3_frame = ctk.CTkFrame(stats_charts_frame, corner_radius=12)
        chart3_frame.pack(fill="both", expand=True)

        chart3_header = ctk.CTkFrame(chart3_frame, fg_color="#3b3b3b", corner_radius=12)
        chart3_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(chart3_header, text="💰 RÉPARTITION DES PRIX",
                     font=ctk.CTkFont(weight="bold")).pack(pady=8)

        self.stats_chart3_container = ctk.CTkFrame(chart3_frame, fg_color="#2b2b2b", height=300)
        self.stats_chart3_container.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.stats_chart3_container.pack_propagate(False)

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
            # Données pour l'évolution temporelle (simulée)
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

            # Données simulées pour 30 jours
            jours = list(range(1, 31))

            # Générer des données réalistes basées sur les produits actuels
            total_produits = len(self.root_produits.findall("produit"))
            base_valeur = max(total_produits * 10, 100)  # Valeur de base

            # Courbes simulées
            stocks = [base_valeur + i * 2 + np.random.randint(-5, 5) for i in range(30)]
            ventes = [max(0, np.random.randint(5, 15) + i * 0.1) for i in range(30)]
            commandes = [max(0, np.random.randint(8, 20) + i * 0.15) for i in range(30)]

            # Créer la figure
            fig = Figure(figsize=(10, 6), dpi=80, facecolor='#2b2b2b')
            ax = fig.add_subplot(111)

            # Tracer les courbes
            ax.plot(jours, stocks, label='Niveau des Stocks', color='#2e86ab', linewidth=2.5, marker='o')
            ax.plot(jours, ventes, label='Produits Vendus', color='#28a745', linewidth=2.5, marker='s')
            ax.plot(jours, commandes, label='Nouvelles Commandes', color='#a23b72', linewidth=2.5, marker='^')

            # Style
            ax.set_xlabel('Jours', color='white', fontweight='bold')
            ax.set_ylabel('Quantité', color='white', fontweight='bold')
            ax.set_title('Évolution des Indicateurs Clés (30 jours)',
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

    def creer_onglet_produits(self):
        """Crée l'onglet de gestion des produits avec interface modernisée"""
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

    def creer_onglet_fournisseurs(self):
        """Crée l'onglet de gestion des fournisseurs avec interface modernisée"""
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

    def creer_onglet_rapports(self):
        """Crée l'onglet des rapports avec interface modernisée"""
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
                                               values=["Hebdomadaire", "Mensuel", "Trimestriel", "Semestriel",
                                                       "Annuel"],
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
        ctk.CTkButton(actions_frame, text="🔄 Tout Actualiser",
                      command=self.actualiser_tout,
                      width=150, height=40,
                      fg_color="#6c757d", hover_color="#545b62").pack(side="left", padx=5)

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
        ctk.CTkRadioButton(theme_frame, text="🔵 Bleu", variable=self.theme_var,
                           value="blue", command=self.changer_theme).pack(side="left", padx=10)
        ctk.CTkRadioButton(theme_frame, text="🟢 Vert", variable=self.theme_var,
                           value="green", command=self.changer_theme).pack(side="left", padx=10)

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
        ctk.CTkButton(data_buttons_frame, text="📤 Exporter Sauvegarde",
                      command=self.exporter_sauvegarde,
                      width=180, height=40,
                      fg_color="#f9c74f", hover_color="#d4a72c").pack(side="left", padx=5)
        ctk.CTkButton(data_buttons_frame, text="🗑️ Nettoyer les Données",
                      command=self.nettoyer_donnees,
                      width=180, height=40,
                      fg_color="#dc3545", hover_color="#a71e2a").pack(side="left", padx=5)

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
• Dernière sauvegarde: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
• Version de l'application: 2.0.0
• Développé avec: Python, CustomTkinter, XML

🔧 FONCTIONNALITÉS:
✓ Gestion complète des produits
✓ Gestion des fournisseurs
✓ Tableau de bord interactif
✓ Statistiques avancées
✓ Export PDF/JSON
✓ Interface moderne et responsive
        """

        info_label = ctk.CTkLabel(system_content, text=stats_text,
                                  font=ctk.CTkFont(family="Consolas", size=12),
                                  justify="left")
        info_label.pack(anchor="w")

        # Section Actions système
        actions_frame = ctk.CTkFrame(main_frame, corner_radius=12)
        actions_frame.pack(fill="x")

        actions_header = ctk.CTkFrame(actions_frame, fg_color="#3b3b3b", corner_radius=12)
        actions_header.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(actions_header, text="🚀 ACTIONS SYSTÈME",
                     font=ctk.CTkFont(weight="bold")).pack(pady=8)

        # Boutons d'actions système
        actions_content = ctk.CTkFrame(actions_frame, fg_color="transparent")
        actions_content.pack(fill="x", padx=20, pady=20)

        system_buttons_frame = ctk.CTkFrame(actions_content, fg_color="transparent")
        system_buttons_frame.pack(fill="x")

        ctk.CTkButton(system_buttons_frame, text="🔄 Redémarrer l'Application",
                      command=self.redemarrer_application,
                      width=200, height=45,
                      fg_color="#2e86ab", hover_color="#1f5f7a").pack(side="left", padx=5)
        ctk.CTkButton(system_buttons_frame, text="❌ Quitter l'Application",
                      command=self.quitter,
                      width=200, height=45,
                      fg_color="#dc3545", hover_color="#a71e2a").pack(side="left", padx=5)

    # === MÉTHODES POUR LES PRODUITS ===

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
                categorie = produit.find("categorie").text if produit.find(
                    "categorie") is not None else "Non catégorisé"
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

        dialog = ModifierProduitDialog(self, values, self.root_fournisseurs)
        self.wait_window(dialog)

        if dialog.result:
            # Trouver le produit dans XML
            for produit in self.root_produits.findall("produit"):
                if produit.find("id").text == values[0]:
                    produit.find("nom").text = dialog.result["nom"]
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

    # === MÉTHODES POUR LES FOURNISSEURS ===

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

        dialog = ModifierFournisseurDialog(self, values)
        self.wait_window(dialog)

        if dialog.result:
            for fournisseur in self.root_fournisseurs.findall("fournisseur"):
                if fournisseur.find("id").text == values[0]:
                    fournisseur.find("nom").text = dialog.result["nom"]
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

    # === MÉTHODES POUR LES RAPPORTS ===

    def get_categories(self):
        """Retourne la liste des catégories uniques"""
        categories = set()
        for produit in self.root_produits.findall("produit"):
            categorie = produit.find("categorie")
            if categorie is not None and categorie.text:
                categories.add(categorie.text)
        return sorted(list(categories))

    def generer_rapport(self):
        """Génère un rapport détaillé"""
        try:
            periode = self.rapport_periode.get()
            categorie = self.rapport_categorie.get()

            rapport = "=" * 60 + "\n"
            rapport += f"RAPPORT D'INVENTAIRE - {periode.upper()}\n"
            rapport += "=" * 60 + "\n\n"
            rapport += f"📅 Date de génération: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            rapport += f"📊 Catégorie: {categorie}\n"
            rapport += f"👤 Généré par: Système de Gestion d'Inventaire\n\n"

            # Statistiques générales
            total_produits = 0
            total_valeur = 0
            produits_faible_stock = 0
            categories_stats = {}
            fournisseurs_stats = {}

            for produit in self.root_produits.findall("produit"):
                # Filtre par catégorie
                if categorie != "Toutes":
                    prod_categorie = produit.find("categorie")
                    if prod_categorie is None or prod_categorie.text != categorie:
                        continue

                quantite = int(produit.find("quantite").text) if produit.find("quantite") is not None else 0
                prix = float(produit.find("prix").text) if produit.find("prix") is not None else 0
                nom_fournisseur = produit.find("fournisseur").text if produit.find(
                    "fournisseur") is not None else "Inconnu"

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

            # Section statistiques générales
            rapport += "📈 STATISTIQUES GÉNÉRALES\n"
            rapport += "-" * 40 + "\n"
            rapport += f"• Nombre total de produits: {total_produits}\n"
            rapport += f"• Valeur totale de l'inventaire: {total_valeur:,.2f} Ar\n"
            rapport += f"• Produits à faible stock: {produits_faible_stock}\n"
            rapport += f"• Nombre de catégories: {len(categories_stats)}\n"
            rapport += f"• Nombre de fournisseurs: {len(fournisseurs_stats)}\n\n"

            # Section détail par catégorie
            rapport += "📊 DÉTAIL PAR CATÉGORIE\n"
            rapport += "-" * 40 + "\n"
            for cat, stats in sorted(categories_stats.items(), key=lambda x: x[1]["valeur"], reverse=True):
                pourcentage = (stats["valeur"] / total_valeur * 100) if total_valeur > 0 else 0
                rapport += f"• {cat}: {stats['produits']} produits, {stats['quantite']} unités, {stats['valeur']:,.2f} Ar ({pourcentage:.1f}%)\n"
            rapport += "\n"

            # Section top fournisseurs
            rapport += "👥 TOP FOURNISSEURS\n"
            rapport += "-" * 40 + "\n"
            top_fournisseurs = sorted(fournisseurs_stats.items(), key=lambda x: x[1]["valeur"], reverse=True)[:5]
            for i, (fournisseur, stats) in enumerate(top_fournisseurs, 1):
                rapport += f"{i}. {fournisseur}: {stats['produits']} produits, {stats['valeur']:,.2f} Ar\n"
            rapport += "\n"

            # Section alertes
            if produits_faible_stock > 0:
                rapport += "⚠️  ALERTES - PRODUITS À FAIBLE STOCK\n"
                rapport += "-" * 40 + "\n"
                for produit in self.root_produits.findall("produit"):
                    quantite = int(produit.find("quantite").text) if produit.find("quantite") is not None else 0
                    if quantite < 10:
                        nom = produit.find("nom").text if produit.find("nom") is not None else "Sans nom"
                        rapport += f"• {nom}: {quantite} unités restantes\n"
                rapport += "\n"

            rapport += "=" * 60 + "\n"
            rapport += "📋 FIN DU RAPPORT\n"
            rapport += "=" * 60 + "\n"

            # Afficher le rapport
            self.rapport_text.delete("1.0", "end")
            self.rapport_text.insert("1.0", rapport)

            self.status_bar.configure(text=f"✅ Rapport {periode} généré avec succès")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération du rapport: {e}")

    def exporter_pdf(self):
        """Exporte le rapport en PDF"""
        try:
            if not os.path.exists("export"):
                os.makedirs("export")

            filename = f"export/rapport_inventaire_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

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
            title = Paragraph("RAPPORT D'INVENTAIRE", title_style)
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

            # Données du tableau
            data = [["ID", "Nom", "Catégorie", "Quantité", "Prix", "Fournisseur"]]

            for produit in self.root_produits.findall("produit"):
                nom = produit.find("nom").text if produit.find("nom") is not None else ""
                categorie = produit.find("categorie").text if produit.find("categorie") is not None else ""
                quantite = produit.find("quantite").text if produit.find("quantite") is not None else "0"
                prix = produit.find("prix").text if produit.find("prix") is not None else "0"
                fournisseur = produit.find("fournisseur").text if produit.find("fournisseur") is not None else ""

                data.append([produit.find("id").text if produit.find("id") is not None else "",
                             nom, categorie, quantite, f"{prix} Ar", fournisseur])

            # Créer le tableau
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            story.append(table)
            story.append(Spacer(1, 20))

            # Générer le PDF
            doc.build(story)
            messagebox.showinfo("Succès", f"Rapport PDF exporté: {filename}")
            self.status_bar.configure(text="✅ Rapport PDF exporté avec succès")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export PDF: {e}")

    def exporter_json(self):
        """Exporte les données en JSON"""
        try:
            if not os.path.exists("export"):
                os.makedirs("export")

            filename = f"export/inventaire_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            data = {
                "metadata": {
                    "date_export": datetime.now().isoformat(),
                    "total_produits": len(self.root_produits.findall("produit")),
                    "total_fournisseurs": len(self.root_fournisseurs.findall("fournisseur")),
                    "version_export": "2.0"
                },
                "produits": [],
                "fournisseurs": []
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
                    "telephone": fournisseur.find("telephone").text if fournisseur.find(
                        "telephone") is not None else "",
                    "adresse": fournisseur.find("adresse").text if fournisseur.find("adresse") is not None else ""
                })

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            messagebox.showinfo("Succès", f"Données JSON exportées: {filename}")
            self.status_bar.configure(text="✅ Données JSON exportées avec succès")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export JSON: {e}")

    # === NOUVELLES MÉTHODES POUR LES PARAMÈTRES ===

    def changer_theme(self):
        """Change le thème de l'application"""
        theme = self.theme_var.get()
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme(theme)
        self.status_bar.configure(text=f"✅ Thème changé: {theme}")

    def exporter_sauvegarde(self):
        """Exporte une sauvegarde complète"""
        try:
            if not os.path.exists("sauvegardes"):
                os.makedirs("sauvegardes")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = f"sauvegardes/backup_{timestamp}"
            os.makedirs(backup_dir)

            # Copier les fichiers XML
            import shutil
            shutil.copy2("produits.xml", backup_dir)
            shutil.copy2("fournisseurs.xml", backup_dir)

            # Créer un fichier info
            with open(f"{backup_dir}/info.txt", "w", encoding="utf-8") as f:
                f.write(f"Sauvegarde créée le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Produits: {len(self.root_produits.findall('produit'))}\n")
                f.write(f"Fournisseurs: {len(self.root_fournisseurs.findall('fournisseur'))}\n")

            messagebox.showinfo("Succès", f"Sauvegarde exportée: {backup_dir}")
            self.status_bar.configure(text="✅ Sauvegarde exportée avec succès")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export de sauvegarde: {e}")

    def nettoyer_donnees(self):
        """Nettoie les données (supprime les produits sans stock et sans fournisseur)"""
        if messagebox.askyesno("Confirmation",
                               "Cette action supprimera tous les produits avec quantité 0 et sans fournisseur.\nContinuer?"):
            try:
                produits_supprimes = 0
                for produit in self.root_produits.findall("produit"):
                    quantite = int(produit.find("quantite").text) if produit.find("quantite") is not None else 0
                    fournisseur = produit.find("fournisseur").text if produit.find("fournisseur") is not None else ""

                    if quantite == 0 and not fournisseur:
                        self.root_produits.remove(produit)
                        produits_supprimes += 1

                self.sauvegarder_donnees()
                self.actualiser_produits()
                self.actualiser_tableau_de_bord()

                messagebox.showinfo("Succès", f"{produits_supprimes} produits nettoyés")
                self.status_bar.configure(text=f"✅ Nettoyage terminé - {produits_supprimes} produits supprimés")

            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du nettoyage: {e}")

    def redemarrer_application(self):
        """Redémarre l'application"""
        if messagebox.askyesno("Confirmation",
                               "Redémarrer l'application? Les données non sauvegardées seront perdues."):
            self.sauvegarder_donnees()
            self.destroy()
            # Relancer l'application
            import subprocess
            subprocess.Popen([sys.executable] + sys.argv)

    def actualiser_tout(self):
        """Actualise toutes les données et vues"""
        try:
            self.charger_donnees()
            self.actualiser_produits()
            self.actualiser_fournisseurs()
            self.actualiser_tableau_de_bord()
            self.generer_statistiques_avancees()

            self.status_bar.configure(text="✅ Toutes les données ont été actualisées")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'actualisation générale: {e}")

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
        """Valide le formulaire"""
        nom = self.nom_entry.get().strip()
        categorie = self.categorie_entry.get().strip()
        quantite = self.quantite_entry.get().strip()
        prix = self.prix_entry.get().strip()
        fournisseur = self.fournisseur_combo.get()

        # Validation
        if not nom:
            messagebox.showwarning("Erreur", "Le nom est obligatoire")
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
        self.prix_entry.insert(0, values[4])
        self.fournisseur_combo.set(values[5])


class AjouterFournisseurDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("👥 Ajouter un Fournisseur")
        self.geometry("400x500")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.result = None
        self.creer_interface()

    def creer_interface(self):
        """Crée l'interface du dialogue"""
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text="Nouveau Fournisseur",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        # Frame pour contenir tous les champs avec défilement si nécessaire
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="both", expand=True, pady=10)

        # Champs de formulaire
        ctk.CTkLabel(form_frame, text="Nom:").pack(anchor="w", pady=(10, 0))
        self.nom_entry = ctk.CTkEntry(form_frame)
        self.nom_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Contact:").pack(anchor="w")
        self.contact_entry = ctk.CTkEntry(form_frame)
        self.contact_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Email:").pack(anchor="w")
        self.email_entry = ctk.CTkEntry(form_frame)
        self.email_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Téléphone:").pack(anchor="w")
        self.telephone_entry = ctk.CTkEntry(form_frame)
        self.telephone_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Adresse:").pack(anchor="w")
        self.adresse_entry = ctk.CTkEntry(form_frame)
        self.adresse_entry.pack(fill="x", pady=(0, 10))

        # Boutons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=10)

        ctk.CTkButton(button_frame, text="Ajouter",
                      command=self.valider, width=100).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="Annuler",
                      command=self.annuler, width=100).pack(side="right", padx=5)

        # Donner le focus au premier champ
        self.nom_entry.focus()

    def valider(self):
        """Valide le formulaire"""
        nom = self.nom_entry.get().strip()
        contact = self.contact_entry.get().strip()
        email = self.email_entry.get().strip()
        telephone = self.telephone_entry.get().strip()
        adresse = self.adresse_entry.get().strip()

        if not nom:
            messagebox.showwarning("Erreur", "Le nom est obligatoire")
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