# INDEX COMPLET DES DOCUMENTS - Version 2 (15 novembre 2025)

## 📋 Vue d'ensemble

Ce projet de Master 2 porte sur l'**optimisation computationnelle de nanoparticules BODIPY** pour une thérapie combinée photodynamique (PDT) et photothermique (PTT) ciblée sur le cancer du sein triple négatif (TNBC).

**Portée révisée (Mar. 2026)** :
- **1 molécule de référence expérimentale** (externe, publiée) pour benchmarking
- **2 prototypes internes** : Iodo-BODIPY (PDT) + TPP–Iodo–BODIPY (théranostique)
- **Méthodologie** : TD-DFT/wB97X-D3 (Remplace ADC(2) pour rapidité/précision laptop)
- **Configuration** : 4 cœurs / 16 Go RAM (%maxcore 3500)
- **Durée** : 14 semaines de stage Master 2

---

## 📁 Structure des fichiers

### 1. **Documents Méthodologiques Principaux**

#### `md files/demarche_methodologique_stage_v3_260302.md` ⭐ **DOCUMENT PRINCIPAL**
- **Statut** : ✅ À jour (03/03/2026)
- **Contenu** : 
  - Portée révisée (1 référence + 2 prototypes)
  - Méthodologie adaptée localement (16 Go RAM)
  - TD-DFT wB97X-D3 pour les excitations verticales
  - Protocole détaillé ORCA 6.1 (5 phases)
  - Chronogramme 14 semaines adapté localement
  - Grille Go/No-Go quantitative
- **Utilisation** : Lire en premier, c'est le guide complet du projet

#### `demarche_methodologique_stage.md`
- **Statut** : ⚠️ Obsolète (version antérieure)
- **Contenu** : Ancienne version avec 3 prototypes et NEVPT2
- **Action** : À archiver ou supprimer

---

### 2. **Documents d'Analyse Critique**

#### `Analyse251115.md` ⭐ **ANALYSE RÉVISÉE**
- **Statut** : ✅ À jour (15/11/2025)
- **Contenu** :
  - Évaluation globale : **18/20** (très bon projet, faisable)
  - Points forts de la correction (portée réduite, ΔDFT+SOC, grille Go/No-Go)
  - Points d'attention résiduels (base ADC(2), critères ciblage)
  - Recommandations finales pour l'étudiant
  - Gestion des risques
- **Utilisation** : Lire après le document principal pour comprendre les justifications

#### `Analyse251114.md`
- **Statut** : ⚠️ Obsolète (version antérieure)
- **Contenu** : Analyse de la version originale (15/20)
- **Action** : À archiver

---

### 3. **Documents de Synthèse et Aide-M��moire**

#### `Resume_Executif_Aide_Memoire.md`
- **Statut** : ✅ À jour
- **Contenu** : Résumé exécutif du projet (16 Go / TD-DFT)
- **Action** : Aucune requise

#### `Synthese_Analyse_Integration.md`
- **Statut** : ⚠️ À mettre à jour
- **Contenu** : Synthèse des analyses
- **Action requise** : Intégrer l'analyse 251115

#### `Synthese_Visuelle_Points_Cles.md`
- **Statut** : ⚠️ À mettre à jour
- **Contenu** : Points clés visuels
- **Action requise** : Ajouter grille Go/No-Go, critères quantitatifs

---

### 4. **Documents Techniques et Pratiques**

#### `Guide_Pratique_ORCA_Scripts_Troubleshooting.md`
- **Statut** : ✅ Pertinent
- **Contenu** : Checklist ΔSCF, scripts bash, dépannage
- **Action** : Vérifier cohérence avec section 5 du document principal

#### `Estimation_Temps_Calculs251114.md`
- **Statut** : ⚠️ À mettre à jour
- **Contenu** : Estimations de temps (ancienne version)
- **Action requise** : Remplacer par section 4.3 du document principal

#### `Planification_Gantt_Optimisation_Ressources.md`
- **Statut** : ⚠️ À mettre à jour
- **Contenu** : Gantt et optimisation
- **Action requise** : Intégrer le chronogramme révisé (section 7)

#### `Integration des methodes OO-DFT.md`
- **Statut** : ✅ Pertinent
- **Contenu** : Justification théorique ΔDFT vs TD-DFT
- **Action** : Vérifier cohérence avec section 2.2

#### `Stokes_Shift.md`
- **Statut** : ✅ Pertinent
- **Contenu** : Analyse Stokes shift
- **Action** : Aucune (document spécialisé)

---

### 5. **Documents de Navigation et Démarrage**

#### `README_GUIDE_NAVIGATION.md`
- **Statut** : ✅ À jour
- **Contenu** : Guide de navigation (Référence aux fichiers _260302)
- **Action** : Aucune requise

#### `DEMARRAGE_RAPIDE.txt`
- **Statut** : ⚠️ À mettre à jour
- **Contenu** : Démarrage rapide
- **Action requise** : Intégrer portée révisée, test comparatif def2-SVP vs def2-TZVP

#### `INDEX_DOCUMENTS_COMPLETS.md`
- **Statut** : ⚠️ Obsolète
- **Contenu** : Ancien index
- **Action** : Remplacer par INDEX_v2

---

## 🔧 Fichiers Corine_codes (Scripts et Inputs ORCA)

### Inputs ORCA (à jour)

| Fichier | Phase | Statut | Notes |
| :--- | :--- | :--- | :--- |
| `S0_gas_opt.inp` | Phase 1a | ✅ | Optimisation S₀ gaz |
| `S0_water_opt.inp` | Phase 1b | ✅ | Optimisation S₀ eau (CPCM) |
| `ADC2_vertical.inp` | Phase 2 | ❌ | Remplacé par `TDDFT_vertical.inp` |
| `TDDFT_vertical.inp` | Phase 2 | ✅ | TD-DFT wB97X-D3 (16 Go RAM) |
| `T1_opt_UKS.inp` | Phase 3a | ✅ | Optimisation T₁ |
| `S1_opt_DeltaUKS.inp` | Phase 3b | ✅ | Optimisation S₁ (ΔSCF) |
| `DeltaSCF_SOC.inp` | Phase 4 | ✅ | ΔDFT+SOC (recommandé) |
| `TDDFT_SOC_quick.inp` | Phase 4 | ✅ | TD-DFT SOC (Plan B) |

### Scripts SLURM (à jour)

| Fichier | Utilité | Statut |
| :--- | :--- | :--- |
| `submit_S0.slurm` | Soumettre S₀ gaz | ✅ |
| `submit_S0_water.slurm` | Soumettre S₀ eau | ✅ |
| `submit_ADC2.slurm` | Soumettre ADC(2) | ✅ |
| `submit_T1.slurm` | Soumettre T₁ | ✅ |
| `submit_S1.slurm` | Soumettre S₁ | ✅ |
| `submit_SOC.slurm` | Soumettre SOC | ✅ |

### Scripts Bash (à vérifier)

| Fichier | Utilité | Statut | Action |
| :--- | :--- | :--- | :--- |
| `copy_and_prepare.sh` | Copier et préparer fichiers | ⚠️ | Vérifier chemins |
| `prepare_and_submit.sh` | Préparer et soumettre | ⚠️ | Vérifier chemins |

### Fichiers de Géométrie

| Fichier | Molécule | Statut |
| :--- | :--- | :--- |
| `Bodipy_Opt.xyz` | BODIPY de base | ⚠️ À supprimer (hors portée) |
| `Iodo_Opt.xyz` | Iodo-BODIPY | ✅ |
| `TPP_Opt.xyz` | TPP-BODIPY | ⚠️ À remplacer par TPP-Iodo-BODIPY |

### Documentation Corine_codes

| Fichier | Statut | Action |
| :--- | :--- | :--- |
| `README.md` | ⚠️ À mettre à jour | Intégrer portée révisée |
| `PROTOTYPES.md` | ⚠️ À mettre à jour | Décrire 1 référence + 2 prototypes |
| `run_examples.README.md` | ���️ À mettre à jour | Ajouter test comparatif def2-SVP vs def2-TZVP |

---

## 📊 Matrice de Mise à Jour

### Priorité CRITIQUE (À faire immédiatement)

- [ ] `Resume_Executif_Aide_Memoire.md` : Intégrer portée révisée
- [ ] `Corine_codes/README.md` : Clarifier 1 référence + 2 prototypes
- [ ] `Corine_codes/PROTOTYPES.md` : Décrire les 3 molécules (référence + 2 prototypes)
- [ ] `Corine_codes/Bodipy_Opt.xyz` : Supprimer (hors portée)
- [ ] `Corine_codes/TPP_Opt.xyz` : Remplacer par TPP-Iodo-BODIPY

### Priorité HAUTE (À faire cette semaine)

- [ ] `Synthese_Analyse_Integration.md` : Intégrer Analyse251115
- [ ] `Synthese_Visuelle_Points_Cles.md` : Ajouter grille Go/No-Go
- [ ] `Planification_Gantt_Optimisation_Ressources.md` : Intégrer chronogramme révisé
- [ ] `Estimation_Temps_Calculs251114.md` : Remplacer par section 4.3 du document principal
- [ ] `README_GUIDE_NAVIGATION.md` : Ajouter lien vers INDEX_v2

### Priorité MOYENNE (À faire avant le stage)

- [ ] `Guide_Pratique_ORCA_Scripts_Troubleshooting.md` : Vérifier cohérence
- [ ] `Corine_codes/ADC2_vertical.inp` : Vérifier base (def2-TZVP vs def2-SVP)
- [ ] `Corine_codes/copy_and_prepare.sh` : Vérifier chemins
- [ ] `Corine_codes/prepare_and_submit.sh` : Vérifier chemins

### Priorité BASSE (Archivage)

- [ ] `demarche_methodologique_stage.md` : Archiver (version antérieure)
- [ ] `Analyse251114.md` : Archiver (version antérieure)
- [ ] `INDEX_DOCUMENTS_COMPLETS.md` : Remplacer par INDEX_v2

---

## 🎯 Checklist de Mise à Jour Complète

### Phase 1 : Mise à jour des documents md

```bash
# Fichiers à mettre à jour (priorité CRITIQUE)
1. Resume_Executif_Aide_Memoire.md
   - Ajouter portée révisée (1 référence + 2 prototypes)
   - Ajouter grille Go/No-Go
   - Ajouter test comparatif def2-SVP vs def2-TZVP

2. Synthese_Analyse_Integration.md
   - Intégrer Analyse251115
   - Ajouter note 18/20

3. Synthese_Visuelle_Points_Cles.md
   - Ajouter grille Go/No-Go quantitative
   - Ajouter critères ciblage TPP⁺

4. README_GUIDE_NAVIGATION.md
   - Ajouter lien vers INDEX_v2
   - Clarifier portée révisée
```

### Phase 2 : Mise à jour des fichiers Corine_codes

```bash
# Fichiers à mettre à jour (priorité CRITIQUE)
1. Corine_codes/README.md
   - Clarifier 1 référence + 2 prototypes
   - Ajouter note sur test comparatif def2-SVP vs def2-TZVP

2. Corine_codes/PROTOTYPES.md
   - Décrire référence expérimentale
   - Décrire Iodo-BODIPY
   - Décrire TPP-Iodo-BODIPY

3. Corine_codes/run_examples.README.md
   - Ajouter exemple test comparatif def2-SVP vs def2-TZVP
   - Ajouter exemple grille Go/No-Go

# Fichiers à supprimer/remplacer
4. Corine_codes/Bodipy_Opt.xyz → SUPPRIMER
5. Corine_codes/TPP_Opt.xyz → Remplacer par TPP-Iodo-BODIPY.xyz
```

### Phase 3 : Archivage

```bash
# Créer dossier archive
mkdir -p /home/taamangtchu/Documents/Github/Master-s-work/md\ files/archive_v1

# Archiver anciens fichiers
mv demarche_methodologique_stage.md archive_v1/
mv Analyse251114.md archive_v1/
mv INDEX_DOCUMENTS_COMPLETS.md archive_v1/
```

---

## 📝 Notes Importantes

### Changements Majeurs (15/11/2025)

1. **Portée** : 3 prototypes → 1 référence + 2 prototypes
2. **SOC** : NEVPT2 → ΔDFT+SOC (gain 10× en temps)
3. **Grille Go/No-Go** : Critères quantitatifs et pondérés
4. **Test comparatif** : def2-SVP vs def2-TZVP en semaine 3 (économie 9h mur)
5. **Critères ciblage** : Distance/angle dièdre (quantitatif) vs surface (qualitatif)
6. **Recommandations** : Section 12 ajoutée pour l'étudiant

### Fichiers Clés à Consulter

- **Pour comprendre le projet** : `demarche_methodologique_stage_v2_integree.md`
- **Pour justifications** : `Analyse251115.md`
- **Pour inputs ORCA** : `Corine_codes/` (tous les `.inp`)
- **Pour scripts** : `Corine_codes/` (tous les `.slurm` et `.sh`)
- **Pour dépannage** : `Guide_Pratique_ORCA_Scripts_Troubleshooting.md`

---

**Document créé** : 15 novembre 2025
**Version** : 2.0 (révisée)
**Statut** : À jour
