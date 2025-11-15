# 📖 LIRE D'ABORD - Guide de Navigation Rapide

## 🎯 Vous êtes...

### 👨‍🎓 Un étudiant qui commence le stage

**Ordre de lecture recommandé** :

1. **Ce fichier** (vous êtes ici) - 5 min
2. **`MISE_A_JOUR_15_NOV_2025.md`** - 10 min (résumé des changements)
3. **`md files/demarche_methodologique_stage_v2_integree.md`** - 2h (document principal)
4. **`md files/Analyse251115.md`** - 1h (justifications)
5. **`Corine_codes/README.md`** - 30 min (scripts et inputs)
6. **`Corine_codes/PROTOTYPES.md`** - 30 min (molécules)

**Temps total** : ~4h (à faire avant le stage)

---

### 👨‍🏫 Un encadrant qui supervise le stage

**Ordre de lecture recommandé** :

1. **Ce fichier** (vous êtes ici) - 5 min
2. **`MISE_A_JOUR_15_NOV_2025.md`** - 10 min (résumé des changements)
3. **`md files/demarche_methodologique_stage_v2_integree.md`** - 2h (document principal)
4. **`md files/Analyse251115.md`** - 1h (justifications et risques)
5. **`md files/INDEX_DOCUMENTS_COMPLETS_v2.md`** - 30 min (vue d'ensemble)

**Temps total** : ~3.5h

**Points clés à vérifier** :
- Section 12 (recommandations pour l'étudiant)
- Section 4.3.2 (goulets d'étranglement)
- Analyse251115 section 6 (recommandations finales)

---

### 🔧 Un développeur qui maintient les scripts

**Ordre de lecture recommandé** :

1. **Ce fichier** (vous êtes ici) - 5 min
2. **`Corine_codes/README.md`** - 30 min (vue d'ensemble)
3. **`Corine_codes/PROTOTYPES.md`** - 30 min (molécules)
4. **`md files/Guide_Pratique_ORCA_Scripts_Troubleshooting.md`** - 1h (dépannage)

**Temps total** : ~2h

**Points clés à vérifier** :
- Inputs ORCA (Phase 1–4)
- Scripts SLURM (soumission)
- Scripts bash (automatisation)

---

### 📊 Un chercheur qui veut comprendre la méthodologie

**Ordre de lecture recommandé** :

1. **Ce fichier** (vous êtes ici) - 5 min
2. **`md files/demarche_methodologique_stage_v2_integree.md` section 2** - 30 min (théorie)
3. **`md files/Integration des methodes OO-DFT.md`** - 30 min (justification ΔDFT)
4. **`md files/Analyse251115.md` section 2** - 30 min (forces méthodologiques)

**Temps total** : ~1.5h

---

## 📁 Structure des Fichiers

### 📚 Fichiers Principaux (À lire en priorité)

```
/home/taamangtchu/Documents/Github/Master-s-work/
├── LIRE_D_ABORD.md ⭐ (vous êtes ici)
├── MISE_A_JOUR_15_NOV_2025.md ⭐ (résumé des changements)
├── md files/
│   ├── demarche_methodologique_stage_v2_integree.md ⭐ (DOCUMENT PRINCIPAL)
│   ├── Analyse251115.md ⭐ (ANALYSE RÉVISÉE)
│   └── INDEX_DOCUMENTS_COMPLETS_v2.md ⭐ (INDEX COMPLET)
└── Corine_codes/
    ├── README.md ⭐ (GUIDE SCRIPTS)
    └── PROTOTYPES.md ⭐ (DESCRIPTION MOLÉCULES)
```

### 📖 Fichiers Secondaires (Référence)

```
md files/
├── Resume_Executif_Aide_Memoire.md (synthèse exécutive)
├── Synthese_Analyse_Integration.md (synthèse analyses)
├── Synthese_Visuelle_Points_Cles.md (points clés visuels)
├── Guide_Pratique_ORCA_Scripts_Troubleshooting.md (dépannage)
├── Integration des methodes OO-DFT.md (justification théorique)
├── Planification_Gantt_Optimisation_Ressources.md (planning)
├── Estimation_Temps_Calculs251114.md (estimations temps)
├── README_GUIDE_NAVIGATION.md (guide navigation)
├── Stokes_Shift.md (analyse spécialisée)
└── DEMARRAGE_RAPIDE.txt (démarrage rapide)
```

### 🔧 Fichiers Techniques (Scripts et Inputs)

```
Corine_codes/
├── README.md ⭐ (guide scripts)
├── PROTOTYPES.md ⭐ (description molécules)
├── run_examples.README.md (exemples)
├── S0_gas_opt.inp (Phase 1a)
├── S0_water_opt.inp (Phase 1b)
├── ADC2_vertical.inp (Phase 2)
├── T1_opt_UKS.inp (Phase 3a)
├── S1_opt_DeltaUKS.inp (Phase 3b)
├── DeltaSCF_SOC.inp (Phase 4 - recommandé)
├── TDDFT_SOC_quick.inp (Phase 4 - Plan B)
├── submit_S0.slurm (soumettre S0 gaz)
├── submit_S0_water.slurm (soumettre S0 eau)
├── submit_ADC2.slurm (soumettre ADC(2))
├── submit_T1.slurm (soumettre T1)
├── submit_S1.slurm (soumettre S1)
├── submit_SOC.slurm (soumettre SOC)
├── copy_and_prepare.sh (copier et préparer)
├── prepare_and_submit.sh (préparer et soumettre)
├── Iodo_Opt.xyz (géométrie Iodo-BODIPY)
└── TPP_Opt.xyz (géométrie TPP-BODIPY)
```

---

## 🚀 Démarrage Rapide

### Pour un étudiant (Semaine 1)

```bash
# 1. Lire les documents clés
cat LIRE_D_ABORD.md
cat MISE_A_JOUR_15_NOV_2025.md
cat md\ files/demarche_methodologique_stage_v2_integree.md

# 2. Consulter les scripts
cat Corine_codes/README.md
cat Corine_codes/PROTOTYPES.md

# 3. Tester la chaîne ΔDFT sur benzène
cd Corine_codes/
orca S0_gas_opt.inp > S0_gas_opt.out
```

### Pour un encadrant (Avant le stage)

```bash
# 1. Vérifier la portée révisée
grep -A 5 "Portée révisée" md\ files/demarche_methodologique_stage_v2_integree.md

# 2. Vérifier les recommandations pour l'étudiant
grep -A 50 "## 12. Recommandations pour l'étudiant" md\ files/demarche_methodologique_stage_v2_integree.md

# 3. Vérifier les risques
grep -A 20 "Gestion des risques" md\ files/Analyse251115.md
```

---

## 📊 Changements Majeurs (15/11/2025)

| Aspect | Avant | Après | Impact |
| :--- | :--- | :--- | :--- |
| **Portée** | 3 prototypes | 1 ref + 2 prototypes | Focus clinique |
| **SOC** | NEVPT2 (300 min) | ΔDFT+SOC (60 min) | Gain 10× |
| **Cahier des charges** | Implicite | Grille Go/No-Go | Objectivité |
| **Test comparatif** | Aucun | def2-SVP vs TZVP | Économie 9h |
| **Recommandations** | Aucune | Section 12 | Préparation |
| **Score projet** | 15/20 | 18/20 | Très bon |

---

## ✅ Checklist Avant le Stage

- [ ] Lire `demarche_methodologique_stage_v2_integree.md`
- [ ] Lire `Analyse251115.md`
- [ ] Consulter `Corine_codes/README.md`
- [ ] Consulter `Corine_codes/PROTOTYPES.md`
- [ ] Tester la chaîne ΔDFT sur benzène
- [ ] Créer convention de nommage pour les fichiers
- [ ] Vérifier les ressources HPC (RAM, file d'attente)
- [ ] Préparer le jeu de test pré-rempli (semaine 1)

---

## 🎯 Points Clés à Retenir

### Pour l'étudiant

1. **Semaine 2** : Grille Go/No-Go = votre boussole
2. **Semaine 3** : Test comparatif def2-SVP vs def2-TZVP (économie 9h)
3. **Semaine 7** : Pré-test des guesses S₁ (3 guesses différents)
4. **Semaine 9** : Activation du Plan B sans culpabilité (si S₁ échoue)
5. **Tout au long** : Archivage systématique des fichiers

### Pour l'encadrant

1. **Audit HPC** : Vérifier RAM (≥ 32–64 Go), file d'attente (< 24h)
2. **Jeu de test** : Fournir BODIPY de référence pré-rempli (semaine 1)
3. **Milestone** : Convergence S₁ réussie à fin semaine 7
4. **Plan B** : TD-DFT ωB97X-D comme fallback explicite
5. **Buffer** : +200–300% pour ΔSCF S₁ (3–5 tentatives)

---

## 📞 Besoin d'Aide?

### Pour des questions sur le projet

→ Consulter `md files/demarche_methodologique_stage_v2_integree.md` section 12

### Pour des questions sur les scripts

→ Consulter `Corine_codes/README.md` section "Troubleshooting"

### Pour des questions sur la méthodologie

→ Consulter `md files/Analyse251115.md` section 2

### Pour des questions sur les molécules

→ Consulter `Corine_codes/PROTOTYPES.md`

---

## 📈 Statistiques du Projet

| Métrique | Valeur |
| :--- | :--- |
| **Durée du stage** | 14 semaines |
| **Nombre de molécules** | 3 (1 ref + 2 prototypes) |
| **Nombre de phases de calcul** | 5 (S0, ADC(2), T1, S1, SOC) |
| **Temps total estimé** | ~20h mur (+ buffer) |
| **Nombre de fichiers** | 50+ (inputs, scripts, géométries) |
| **Score du projet** | 18/20 (très bon, faisable) |

---

## 🎓 Conclusion

Vous avez maintenant **tous les outils** pour réussir ce stage. Le projet est **scientifiquement excellent, méthodologiquement à la pointe, et réaliste en 14 semaines**.

**Bonne chance!** 🚀

---

**Document créé** : 15 novembre 2025
**Version** : 1.0
**Statut** : À jour
