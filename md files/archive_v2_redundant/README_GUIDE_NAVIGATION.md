# 📚 README : Guide de Navigation pour le Stage en Chimie Computationnelle

**Conception In Silico d'Agents Théranostiques Photodynamiques pour le TNBC**

---

## 🎯 Vue d'Ensemble du Projet

Ce projet vise à concevoir et valider *in silico* trois prototypes de molécules BODIPY pour la photothérapie dynamique (PDT) et photothermique (PTT) du cancer du sein triple négatif (TNBC). Le stage combine chimie quantique théorique (DFT, ADC, OO-DFT), calcul haute performance (ORCA 6.1), et analyse critique des résultats pour aboutir à un candidat pharmacophore optimal.

---

## 📁 Structure des Fichiers Documentaires

### Document 1️⃣ : **Méthodologie Intégrée (VERSION 2)**
**Fichier :** `md files/demarche_methodologique_stage_v3_260302.md`

**Contenu clé :**
- ✅ Fondements théoriques complets (sections 1-2)
- ✅ **Remplacement TD-DFT → OO-DFT/ΔDFT intégré**
- ✅ Codes ORCA 6.1 prêts à l'emploi (section 3)
- ✅ Tableau des temps de calcul (section 4)
- ✅ Stratégies de convergence robuste (section 5)
- ✅ Défis cliniques et perspectives (section 6)
- ✅ Chronogramme 14 semaines (section 7)

**Points méthodologiques pratiques inclus :**
- Recommandation d'utiliser ptSS-PCM pour les calculs d'émission (états CT) en solution
- Fonctionnelles conseillées : OT-ωB97M-V (ΔUKS/ΔROKS), PBE0 (ΔUKS robuste), PBE38-D4 (robustesse E_em)
- Méthode IMOM recommandée pour les excitations ICT (stabilité de convergence)
- Objectifs de benchmarking : ΔE_{ST} cible MAE < 0,05 eV ; λ_max/E_em ≤ 0,1 eV

**À quand l'utiliser :**
- **Premier jour :** Lire sections 1-2 pour comprendre la théorie
- **Semaine 1 :** Imprimer et annoter les codes ORCA (section 3)
- **Semaine 3 :** Adapter les inputs pour vos 3 prototypes
- **En continu :** Référence pour troubleshooting (section 5)

**Comment l'utiliser :**
1. Lire d'abord l'Introduction (Partie 1) : contexte, objectifs
  > Thématique du stage : Optimisation de nanoparticules de BODIPY pour une thérapie combinée photodynamique et photothermique ciblée sur les cellules de cancer du sein triple négatif
2. Comprendre les théories (Partie 2) : DFT, ADC(2), OO-DFT
3. Utiliser les codes ORCA comme templates (Partie 3)
4. Adapter le chronogramme à votre calendrier (Partie 4)

---

### Document 2️⃣ : **Guide Pratique ORCA et Scripts**
**Fichier :** `Guide_Pratique_ORCA_Scripts_Troubleshooting.md`

**Contenu clé :**
- 🔧 Scripts bash automatisés (partie 1)
- 🔧 8 templates d'inputs ORCA prêts à copier-coller (partie 1.2)
- 🔧 Script Python pour post-traitement (partie 1.3)
- 🆘 Guide Troubleshooting détaillé (partie 2)
- ✅ Checklist pré-soumission (partie 3)

**À quand l'utiliser :**
- **Semaine 3 :** Copier les scripts dans vos répertoires
- **Semaine 4-11 :** Adapter les inputs et lancer les calculs
- **En continu :** Checker le troubleshooting si problème
- **Après calculs :** Utiliser le script Python pour analyse rapide

**Ordre d'utilisation :**
1. Lire la section "Partie 1.1" pour comprendre le workflow global
2. Adapter le script `run_protocol.sh` pour votre infrastructure
3. Copier les 8 templates (Partie 1.2) dans vos répertoires
4. Consulter Troubleshooting (Partie 2) si problème
5. Utiliser le script Python (Partie 1.3) pour extraction de résultats

---

### Document 3️⃣ : **Résumé Exécutif et Aide-Mémoire**
**Fichier :** `Resume_Executif_Aide_Memoire.md`

**Contenu clé :**
- 📊 Tableau comparatif TD-DFT vs OO-DFT (partie 1)
- 📊 Protocole en 6 étapes (partie 2)
- 🎯 Critères de sélection des prototypes (partie 3)
- 📋 Aide-mémoire à imprimer (partie 4)
- ⚡ Stratégies d'accélération (partie 6)

**À quand l'utiliser :**
- **Première semaine :** Imprimer la Partie 4 et afficher au bureau !
- **Semaine 4 :** Appliquer les critères de la Partie 3
- **Semaine 11 :** Utiliser le scoring (Partie 3) pour comparer prototypes
- **En cas de doute :** Consulter le tableau comparatif (Partie 1)

**Format :**
- **Compact :** À imprimer et garder à proximité
- **Visuels :** Tableaux, checklists, aide-mémoire
- **Rapide :** Consultation < 2 minutes

---

### Document 4️⃣ : **Planification Gantt et Optimisation**
**Fichier :** `Planification_Gantt_Optimisation_Ressources.md`

**Contenu clé :**
- 📅 Gantt détaillé par semaine (partie 1-2)
- ⚙️ Stratégies de parallélisation (partie 3)
- ⚙️ Allocations SLURM optimales (partie 3.2)
- ⚙️ Gestion des crises et retards (partie 5)
- 📊 Tableau de suivi d'avancement (partie 4)

**À quand l'utiliser :**
- **Dimanche de Semaine 1 :** Adapter le calendrier à vos dates
- **Chaque lundi :** Mettre à jour le tableau de suivi (partie 4)
- **Pendant calculs :** Référence pour parallélisation (partie 3)
- **En cas de retard :** Consulter gestion des crises (partie 5)

**Comment l'utiliser :**
1. Imprimer la Partie 1-2 et afficher sur le mur
2. Adapter les dates selon votre calendrier réel
3. Cocher les étapes complétées
4. Utiliser les allocations SLURM (Partie 3.2) comme template

---

## 🚀 Guide de Démarrage Rapide (Jour 1)

### Étape 1 : Structurer votre environnement (30 min)

```bash
# Créer la structure de répertoires
mkdir -p ~/stage_BODIPY/{proto-{A,B,C},calculs,results,scripts}
cd ~/stage_BODIPY

# Copier les documents de référence
cp ~/Documents/Corine/demarche_methodologique_stage_v3_260302.md .
cp ~/Documents/Corine/Guide_Pratique_ORCA_Scripts_Troubleshooting.md .
cp ~/Documents/Corine/Resume_Executif_Aide_Memoire.md .
cp ~/Documents/Corine/Planification_Gantt_Optimisation_Ressources.md .

# Adapter le calendrier (Gantt)
# Modifier les dates dans Planification_Gantt...md
# Imprimer et afficher
```

### Étape 2 : Configuration ORCA 6.1 (15 min)

```bash
# Vérifier ORCA est accessible
module load orca/6.1
which orca
orca -v

# Créer un répertoire pour les templates
mkdir -p scripts/orca_templates
cd scripts/orca_templates

# Copier les 8 templates du Guide_Pratique
# (Sections 1.2.1 à 1.2.8)
# Nommer : S0_gas_opt.inp, S0_water_opt.inp, etc.
```

### Étape 3 : Créer vos premières molécules (2-3 h)

```bash
# Lancer Avogadro
avogadro &

# Construire Proto-A, Proto-B, Proto-C
# Exporter en XYZ : File → Export → .xyz

# Placer les fichiers
cp proto-A.xyz ~/stage_BODIPY/proto-A/
cp proto-B.xyz ~/stage_BODIPY/proto-B/
cp proto-C.xyz ~/stage_BODIPY/proto-C/
```

### Étape 4 : Première lecture (1 h)

- Lire la section "1. Introduction" de `demarche_methodologique_stage_v2_integree.md`
- Imprimer l'aide-mémoire (partie 4 de `Resume_Executif_Aide_Memoire.md`)

---

## 📖 Flux de Lecture Recommandé

### Pour les **théoriciens** (chimistes quantiques)

1. **Jour 1 :** Sections 1-2 de `demarche_methodologique_stage_v3_260302.md`
2. **Jour 2-3 :** Sections 2.1-2.2 (justification OO-DFT)
3. **Semaine 1 :** Sections 3-5 (codes ORCA, stratégies convergence)

### Pour les **computationnels** (programmeurs HPC)

1. **Jour 1 :** `Resume_Executif_Aide_Memoire.md` entièrement
2. **Jour 2 :** `Planification_Gantt_Optimisation_Ressources.md` (partie 1-3)
3. **Semaine 1 :** `Guide_Pratique_ORCA_Scripts_Troubleshooting.md` (partie 1)

### Pour les **managers** (encadrants, jury)

1. **10 min :** `Resume_Executif_Aide_Memoire.md` (parties 1, 3, 4)
2. **30 min :** Section 1 de `Planification_Gantt_Optimisation_Ressources.md`
3. **30 min :** Sections 1, 3 de `demarche_methodologique_stage_v2_integree.md`

---

## 🔄 Utilisation Pendant les Phases

### Phase 1 : Immersion (Semaines 1-3)

**Documents clés :** 
- `demarche_methodologique_stage_v2_integree.md` (sections 1-2)
- `Resume_Executif_Aide_Memoire.md` (partie 3 : critères prototypes)

**Tâches :**
- [ ] Lire 10 articles clés
- [ ] Rédiger synthèse bibliographique
- [ ] Sélectionner les 3 prototypes
- [ ] Justifier le design chimique

---

### Phase 2 : Calculs Fondamentaux (Semaines 4-8)

**Documents clés :**
- `Guide_Pratique_ORCA_Scripts_Troubleshooting.md` (partie 1 : templates)
- `Planification_Gantt_Optimisation_Ressources.md` (partie 2 : calendrier hebdo)
- `Resume_Executif_Aide_Memoire.md` (partie 4 : aide-mémoire)

**Processus :**
```
Chaque semaine:
1. Consulter le calendrier détaillé (Planification_Gantt...)
2. Lancer les calculs appropriés en s'aidant des templates
3. En cas de problème → Troubleshooting (Guide_Pratique...)
4. Mettre à jour le tableau de suivi (Planification_Gantt... partie 4)
```

---

### Phase 3 : Analyse (Semaines 9-11)

**Documents clés :**
- `Resume_Executif_Aide_Memoire.md` (parties 3, 5 : scoring et stratégies)
- `demarche_methodologique_stage_v2_integree.md` (section 6 : analyse)
- Script Python `analyze_results.py` (pour extraction rapide)

**Processus :**
```
1. Extraire λ_max, E_ad, ΔE_ST, SOC pour les 3 prototypes
2. Compiler dans un tableau comparatif
3. Appliquer le scoring (Resume_Executif... partie 3)
4. Ranger les prototypes
5. Justifier le candidat optimal
```

---

### Phase 4 : Synthèse (Semaines 12-14)

**Documents clés :**
- `demarche_methodologique_stage_v2_integree.md` (intégralité comme référence)
- Tous les graphiques/tableaux des phases antérieures

**Processus :**
```
Rapport (30-50 pages):
1. Intro + Contexte (3-4 pages) → Refer à section 1 de demarche...
2. État art (5-7 pages) → Vos notes de biblio de phase 1
3. Théorie/Méthodes (8-10 pages) → Sections 2-3 de demarche...
4. Résultats (10-12 pages) → Tableaux/graphiques de phase 2-3
5. Discussion (5-8 pages) → Sections 6 de demarche..., votre analyse
6. Perspectives (3-4 pages) → Défis cliniques (section 6), votre vision
```

---

## 🛠️ Ressources Externes Essentielles

### Documentation ORCA 6.1
- **Lien :** https://www.factsci.org/orca/
- **Sections clés :** 
  - DFT, Geometry Optimization
  - Post-HF Methods (ADC)
  - TD-DFT/TDDFT
  - Relativistics (ZORA)

### Littérature Recommandée (À consulter)
- **BODIPY photophysics :** Loudet & Burgess (2007), Chem. Rev.
- **PDT photosensitizers :** Plaetzer et al. (2009), Photochem. Photobiol.
- **OO-DFT :** Casanova (2012), J. Comput. Chem.

### Outils Complémentaires
- **Multiwfn :** http://sobereva.com/multiwfn/ (analyse de charge, MEP)
- **Avogadro :** https://avogadro.cc/ (construction moléculaire)
- **VMD :** https://www.ks.uiuc.edu/Research/vmd/ (visualisation)

---

## 📋 Checklist d'Auto-Évaluation

### Semaine 1 : ✓ Tout lu et compris ?
- [ ] J'ai lu la section "Introduction et objectifs" complètement
- [ ] Je comprends la différence TD-DFT vs OO-DFT
- [ ] J'ai identifié les 3 prototypes et leur design chimique
- [ ] Je sais où trouver les 10 articles bibliographiques clés
- [ ] J'ai fait un plan du rapport de stage

### Semaine 4 : ✓ Premiers calculs lancés ?
- [ ] Mes 3 fichiers XYZ sont validés (géométrie raisonnable)
- [ ] J'ai copié les templates ORCA et adaptés pour mes molécules
- [ ] J'ai soumis S0 gas optim. pour proto-A
- [ ] Je comprends les allocations SLURM (CPU, temps, mémoire)
- [ ] J'ai mis à jour mon tableau de suivi (Gantt)

### Semaine 8 : ✓ Résultats commencent à arriver ?
- [ ] J'ai λ_max pour les 3 prototypes
- [ ] λ_max est dans la gamme attendue (600-900 nm)
- [ ] J'ai comparé avec la littérature (benchmarking)
- [ ] J'ai lancé S1/T1 optim. (difficile, mais essayé)
- [ ] J'ai un plan de backup régulier des fichiers GBW

### Semaine 11 : ✓ Prêt à analyser ?
- [ ] Tous les calculs principaux sont terminés
- [ ] J'ai un tableau comparatif complet (λ_max, E_ad, ΔE_ST, SOC)
- [ ] J'ai scorer les prototypes et rangé les candidats
- [ ] J'ai justifié le candidat optimal par écrit
- [ ] J'ai identifié les limitations de mon approche

### Semaine 14 : ✓ Prêt pour la soutenance ?
- [ ] Rapport final écrit (30-50 pages, complet)
- [ ] Diapositives préparées (15-20 slides de haute qualité)
- [ ] J'ai répété ma présentation (timing OK, discours fluide)
- [ ] Tous les fichiers archivés proprement
- [ ] J'ai répondu mentalement aux questions possibles (jury)

---

## 🆘 Dépannage Rapide

**"Je ne sais pas par où commencer"**
→ Lire `Resume_Executif_Aide_Memoire.md` partie 2 (protocole 6 étapes)

**"Mon calcul S0 ne converge pas"**
→ Consulter `Guide_Pratique_ORCA_Scripts_Troubleshooting.md` Problème 1

**"Je suis en retard sur le calendrier"**
→ Consulter `Planification_Gantt_Optimisation_Ressources.md` partie 5 (gestion des crises)

**"Je ne comprends pas la théorie OO-DFT"**
→ Lire `demarche_methodologique_stage_v2_integree.md` section 2.1-2.2 + Integration des methodes OO-DFT.md

**"Je dois réduire les temps de calcul"**
→ Consulter `Resume_Executif_Aide_Memoire.md` partie 6 (stratégies rapides)

**"Comment scorer les prototypes ?"**
→ Utiliser le tableau `Resume_Executif_Aide_Memoire.md` partie 3

---

## 📞 Contact et Support

### Avant de demander de l'aide, vérifier :

1. Consulter la **table des matières** du document pertinent
2. Utiliser `Ctrl+F` pour chercher le mot-clé
3. Consulter les **Troubleshooting** (Guide_Pratique...)
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
├── 📚 demarche_methodologique_stage_v2_integree.md
├── 📚 Guide_Pratique_ORCA_Scripts_Troubleshooting.md
├── 📚 Resume_Executif_Aide_Memoire.md
├── 📚 Planification_Gantt_Optimisation_Ressources.md
│
├── 🗂️ proto-A/
│   ├── S0_gas_opt.inp
│   ├── S0_gas_opt.out
│   ├── S0_water_opt.gbw
│   ├── ADC2_vertical.inp
│   ├── T1_water_opt.gbw
│   ├── S1_water_opt.gbw
│   ├── NEVPT2_SOC.out
│   └── results_proto-A.txt
│
├── 🗂️ proto-B/
│   └── [même structure]
│
├── 🗂️ proto-C/
│   └── [même structure]
│
├── 📊 results/
│   ├── comparison_table.csv
│   ├── prototypes_scoring.xlsx
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
2. ✅ Lancez les calculs parallèles (gain 3×)
3. ✅ Consultez les documents régulièrement
4. ✅ Préparez un plan B si retard

**Bon courage et bon stage !** 🚀

---

**Version :** 1.0  
**Date :** 13 novembre 2025  
**Pour :** Stage Master 2 UY1 Montpellier 2025
