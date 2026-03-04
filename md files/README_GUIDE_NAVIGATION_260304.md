# 📚 README : Guide de Navigation pour le Stage en Chimie Computationnelle

**Conception In Silico d'Agents Théranostiques Photodynamiques pour le TNBC**

> **Mise à jour : 04 mars 2026 (260304)**
> - Exécution locale 16 Go RAM / TD-DFT ωB97X-D3
> - Configuration : 4 cœurs, %maxcore 3500
> - Archivage v1 créé pour anciens documents

---

## 🎯 Vue d'Ensemble du Projet

Ce projet vise à concevoir et valider *in silico* des molécules BODIPY pour la photothérapie dynamique (PDT) et photothermique (PTT) du cancer du sein triple négatif (TNBC).

**Portée révisée (260304) :**
- **1 molécule de référence expérimentale** (benchmarking uniquement)
- **2 prototypes internes** : Iodo-BODIPY + TPP-Iodo-BODIPY
- **Configuration** : 4 cœurs / 16 Go RAM (%maxcore 3500)
- **Méthodologie** : ΔDFT+SOC (remplace NEVPT2, gain 10×)

---

## 📁 Structure des Fichiers Documentaires

### 📄 Document Principal : Méthodologie Intégrée

**Fichier :** `md files/demarche_methodologique_stage_v3_260302.md`

**Contenu clé :**
- ✅ Fondements théoriques complets (sections 1-2)
- ✅ Codes ORCA 6.1 prêts à l'emploi (section 3)
- ✅ Tableau des temps de calcul (section 4)
- ✅ Stratégies de convergence robuste (section 5)
- ✅ Chronogramme 14 semaines (section 7)
- ✅ Grille Go/No-Go quantitative (section 8)
- ✅ Recommandations pour l'étudiant (section 12)

**À quand l'utiliser :**
- **Premier jour :** Lire sections 1-2 pour comprendre la théorie
- **Semaine 1 :** Imprimer et annoter les codes ORCA (section 3)
- **Semaine 3 :** Adapter les inputs pour les 2 prototypes
- **En continu :** Référence pour troubleshooting (section 5)

---

### 📄 Document 2 : Guide Pratique ORCA et Scripts

**Fichier :** `md files/Guide_Pratique_ORCA_Scripts_Troubleshooting.md`

**Contenu clé :**
- 🔧 Scripts bash automatisés (partie 1)
- 🔧 Templates d'inputs ORCA prêts à copier-coller
- 🔧 Script Python pour post-traitement
- 🆘 Guide Troubleshooting détaillé
- ✅ Checklist pré-soumission

**À quand l'utiliser :**
- **Semaine 3 :** Copier les scripts dans vos répertoires
- **Semaine 4-11 :** Adapter les inputs et lancer les calculs
- **En continu :** Consulter troubleshooting si problème

---

### 📄 Document 3 : Résumé Exécutif et Aide-Mémoire

**Fichier :** `md files/Resume_Executif_Aide_Memoire_260304.md` ⭐ **MIS À JOUR**

**Contenu clé :**
- 📊 Tableau comparatif TD-DFT vs OO-DFT
- 📊 Protocole en 7 étapes (local 16 Go)
- 🎯 Critères de sélection des prototypes (Grille Go/No-Go)
- 📋 Aide-mémoire à imprimer (partie 4)
- ⚡ Stratégies d'accélération

**À quand l'utiliser :**
- **Première semaine :** Imprimer la Partie 4 et afficher au bureau !
- **Semaine 4 :** Appliquer les critères de la Partie 3
- **Semaine 11 :** Utiliser le scoring pour comparer prototypes

---

### 📄 Document 4 : Planification Gantt et Optimisation

**Fichier :** `md files/Planification_Gantt_Optimisation_Ressources.md`

**Contenu clé :**
- 📅 Gantt détaillé par semaine
- ⚙️ Stratégies de parallélisation
- ⚙️ Allocations optimales (4 cœurs, 16 Go)
- 📊 Tableau de suivi d'avancement

---

### 📄 Document 5 : Analyse Critique et Justifications

**Fichier :** `md files/Analyse251115.md`

**Contenu clé :**
- 📈 Évaluation 18/20 (très bon, faisable)
- 📝 Justifications des changements méthodologiques
- ⚠️ Gestion des risques détaillée
- 💡 Recommandations finales

---

### 📄 Document 6 : Index Complet des Documents

**Fichier :** `md files/INDEX_DOCUMENTS_COMPLETS_v2.md`

**Contenu clé :**
- 📑 Vue d'ensemble de tous les documents
- 📊 Matrice de mise à jour
- ✅ Checklist de mise à jour

---

### 📄 Document 7 : Synthèse Analyse Intégration

**Fichier :** `md files/Synthese_Analyse_Integration.md`

**Contenu clé :**
- 🔗 Intégration des recommandations méthodologiques
- 📋 Points-clés pratiques
- 🎯 Cibles de benchmarking

---

### 📄 Document 8 : Synthèse Visuelle Points Clés

**Fichier :** `md files/Synthese_Visuelle_Points_Cles.md`

**Contenu clé :**
- 🎨 Diagrammes visuels
- 📊 Matrice de sélection
- 📋 Checklist à imprimer

---

## 🚀 Guide de Démarrage Rapide (Jour 1)

### Étape 1 : Structurer votre environnement (30 min)

```bash
# Créer la structure de répertoires
mkdir -p ~/stage_BODIPY/{reference,iodo,tpp-iodo}/{S0,S1,T1,TDDFT,SOC,MEP}
cd ~/stage_BODIPY

# Copier les documents de référence
cp ~/Master-s-work/md\ files/demarche_methodologique_stage_v3_260302.md .
cp ~/Master-s-work/md\ files/Resume_Executif_Aide_Memoire_260304.md .
cp ~/Master-s-work/md\ files/Guide_Pratique_ORCA_Scripts_Troubleshooting.md .

# Imprimer l'aide-mémoire (Partie 4)
```

### Étape 2 : Configuration ORCA 6.1 (15 min)

```bash
# Vérifier ORCA est accessible
which orca
orca -v

# Créer un répertoire pour les templates
mkdir -p scripts/orca_templates
cd scripts/orca_templates

# Copier les templates depuis Corine_codes/
cp ../../../Corine_codes/*.inp .
```

### Étape 3 : Créer vos premières molécules (2-3 h)

```bash
# Lancer Avogadro
avogadro &

# Construire les 3 molécules (1 ref + 2 prototypes)
# Exporter en XYZ

# Placer les fichiers
cp proto-reference.xyz ~/stage_BODIPY/reference/
cp proto-iodo.xyz ~/stage_BODIPY/iodo/
cp proto-tpp-iodo.xyz ~/stage_BODIPY/tpp-iodo/
```

### Étape 4 : Première lecture (1 h)

- Lire la section "1. Introduction" de `demarche_methodologique_stage_v3_260302.md`
- Imprimer l'aide-mémoire (Partie 4 de `Resume_Executif_Aide_Memoire_260304.md`)

---

## 📖 Flux de Lecture Recommandé

### Pour les **théoriciens** (chimistes quantiques)

1. **Jour 1 :** Sections 1-2 de `demarche_methodologique_stage_v3_260302.md`
2. **Jour 2-3 :** Sections 2.1-2.2 (justification ΔDFT)
3. **Semaine 1 :** Sections 3-5 (codes ORCA, stratégies convergence)

### Pour les **computationnels** (programmeurs HPC)

1. **Jour 1 :** `Resume_Executif_Aide_Memoire_260304.md` entièrement
2. **Jour 2 :** `Guide_Pratique_ORCA_Scripts_Troubleshooting.md` (partie 1)
3. **Semaine 1 :** Templates ORCA et scripts bash

### Pour les **managers** (encadrants, jury)

1. **10 min :** `Resume_Executif_Aide_Memoire_260304.md` (parties 1, 3, 4)
2. **30 min :** Sections 1, 3 de `demarche_methodologique_stage_v3_260302.md`
3. **30 min :** `Analyse251115.md` (évaluation et risques)

---

## 🔄 Utilisation Pendant les Phases

### Phase 1 : Immersion (Semaines 1-3)

**Documents clés :**
- `demarche_methodologique_stage_v3_260302.md` (sections 1-2)
- `Resume_Executif_Aide_Memoire_260304.md` (partie 3 : critères prototypes)

**Tâches :**
- [ ] Lire 10 articles clés
- [ ] Rédiger synthèse bibliographique
- [ ] Sélectionner la référence expérimentale
- [ ] Construire les 2 prototypes

---

### Phase 2 : Calculs Fondamentaux (Semaines 4-8)

**Documents clés :**
- `Guide_Pratique_ORCA_Scripts_Troubleshooting.md` (templates)
- `demarche_methodologique_stage_v3_260302.md` (section 3 : codes ORCA)
- `Resume_Executif_Aide_Memoire_260304.md` (partie 4 : aide-mémoire)

**Processus :**
```
Chaque semaine:
1. Consulter le calendrier détaillé
2. Lancer les calculs appropriés
3. En cas de problème → Troubleshooting
4. Archiver systématiquement (.gbw, .out)
```

---

### Phase 3 : Analyse (Semaines 9-11)

**Documents clés :**
- `Resume_Executif_Aide_Memoire_260304.md` (parties 3, 5 : scoring)
- `demarche_methodologique_stage_v3_260302.md` (section 8 : grille Go/No-Go)

**Processus :**
```
1. Extraire λ_max, E_ad, ΔE_ST, SOC pour les 2 prototypes
2. Compiler dans un tableau comparatif
3. Appliquer la grille Go/No-Go
4. Identifier le candidat optimal
```

---

### Phase 4 : Synthèse (Semaines 12-14)

**Documents clés :**
- Tous les graphiques/tableaux des phases antérieures

**Processus :**
```
Rapport (30-50 pages):
1. Intro + Contexte (3-4 pages)
2. État art (5-7 pages)
3. Théorie/Méthodes (8-10 pages)
4. Résultats (10-12 pages)
5. Discussion (5-8 pages)
6. Perspectives (3-4 pages)
```

---

## 🛠️ Ressources Externes Essentielles

### Documentation ORCA 6.1
- **Lien :** https://www.factsci.org/orca/
- **Sections clés :** DFT, Geometry Optimization, Post-HF (ADC), TD-DFT

### Littérature Recommandée
- **BODIPY photophysics :** Loudet & Burgess (2007), Chem. Rev.
- **PDT photosensitizers :** Plaetzer et al. (2009), Photochem. Photobiol.
- **ΔDFT/OO-DFT :** Casanova (2012), J. Comput. Chem.

### Outils Complémentaires
- **Multiwfn :** http://sobereva.com/multiwfn/ (analyse de charge, MEP)
- **Avogadro :** https://avogadro.cc/ (construction moléculaire)
- **VMD :** https://www.ks.uiuc.edu/Research/vmd/ (visualisation)

---

## 📋 Checklist d'Auto-Évaluation

### Semaine 1 : ✓ Tout lu et compris ?
- [ ] J'ai lu la section "Introduction et objectifs" complètement
- [ ] Je comprends la différence TD-DFT vs ΔDFT
- [ ] J'ai identifié la référence et les 2 prototypes
- [ ] J'ai fait un plan du rapport de stage

### Semaine 4 : ✓ Premiers calculs lancés ?
- [ ] Mes 3 fichiers XYZ sont validés
- [ ] J'ai copié les templates ORCA et adaptés
- [ ] J'ai soumis S0 gas optim. pour référence
- [ ] J'ai mis à jour mon tableau de suivi

### Semaine 8 : ✓ Résultats commencent à arriver ?
- [ ] J'ai λ_max pour les 3 molécules
- [ ] λ_max est dans la gamme attendue (600-900 nm)
- [ ] J'ai comparé avec la littérature (benchmarking)
- [ ] J'ai lancé S1/T1 optim.

### Semaine 11 : ✓ Prêt à analyser ?
- [ ] Tous les calculs principaux sont terminés
- [ ] J'ai un tableau comparatif complet
- [ ] J'ai appliqué la grille Go/No-Go
- [ ] J'ai justifié le candidat optimal par écrit

### Semaine 14 : ✓ Prêt pour la soutenance ?
- [ ] Rapport final écrit (30-50 pages)
- [ ] Diapositives préparées (15-20 slides)
- [ ] J'ai répété ma présentation
- [ ] Tous les fichiers archivés proprement

---

## 🆘 Dépannage Rapide

| Problème | Solution |
|:---|:---|
| "Je ne sais pas par où commencer" | Lire `Resume_Executif_Aide_Memoire_260304.md` partie 2 |
| "Mon calcul S0 ne converge pas" | Consulter `Guide_Pratique_ORCA_Scripts_Troubleshooting.md` Problème 1 |
| "Je suis en retard sur le calendrier" | Consulter `Planification_Gantt_Optimisation_Ressources.md` partie 5 |
| "Je ne comprends pas la théorie ΔDFT" | Lire `demarche_methodologique_stage_v3_260302.md` section 2.1-2.2 |
| "Je dois réduire les temps de calcul" | Consulter `Resume_Executif_Aide_Memoire_260304.md` partie 7 |
| "Comment scorer les prototypes ?" | Utiliser le tableau `Resume_Executif_Aide_Memoire_260304.md` partie 3 |

---

## 📞 Contact et Support

### Avant de demander de l'aide, vérifier :

1. Consulter la **table des matières** du document pertinent
2. Utiliser `Ctrl+F` pour chercher le mot-clé
3. Consulter les **Troubleshooting**
4. **Puis** contacter l'encadrant avec :
   - Le problème exact
   - Quelle étape du calendrier vous êtes
   - Les 3 dernières lignes de l'output d'erreur
   - Les stratégies déjà essayées

---

## 📁 Arborescence Recommandée Finale

```
~/stage_BODIPY/
├── 📄 README.md (ce fichier)
├── 📚 demarche_methodologique_stage_v3_260302.md
├── 📚 Resume_Executif_Aide_Memoire_260304.md ⭐
├── 📚 Guide_Pratique_ORCA_Scripts_Troubleshooting.md
├── 📚 Planification_Gantt_Optimisation_Ressources.md
│
├── 🗂️ reference/
│   ├── S0_gas_opt.inp
│   ├── S0_gas_opt.out
│   ├── S0_water_opt.gbw
│   ├── TDDFT_vertical.inp
│   ├── T1_water_opt.gbw
│   ├── S1_water_opt.gbw
│   ├── SOC_DeltaDFT.out
│   └── results_reference.txt
│
├── 🗂️ iodo/
│   └── [même structure]
│
├── 🗂️ tpp-iodo/
│   └── [même structure]
│
├── 📊 results/
│   ├── comparison_table.csv
│   ├── prototypes_scoring.xlsx (Grille Go/No-Go)
│   ├── spectres_absorption.png
│   ├── MEP_maps/
│   └── graphiques_publication/
│
├── 📋 rapport_stage_final.pdf
├── 🎤 presentation_soutenance.pptx
│
└── 📜 ARCHIVE/
    └── [Sauvegarde complète du projet]
```

---

## 🎓 Derniers Mots

Ce projet est **ambitieux mais faisable** en 14 semaines si vous :
1. ✅ Restez organisé (checklist hebdomadaire)
2. ✅ Lancez les calculs séquentiellement (4 cœurs, 16 Go)
3. ✅ Consultez les documents régulièrement
4. ✅ Préparez un plan B si retard (TD-DFT fallback)

**Score du projet : 18/20** (Très bon, faisable)

**Bon courage et bon stage !** 🚀

---

**Version :** 2.0 (260304)
**Date :** 04 mars 2026
**Pour :** Stage Master 2 UY1
**Configuration :** Local 16 Go RAM / 4 cœurs / TD-DFT ωB97X-D3
