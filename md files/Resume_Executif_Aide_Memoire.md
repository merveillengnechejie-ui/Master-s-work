# Résumé Exécutif : Comparaison TD-DFT vs OO-DFT/ΔDFT et Aide-Mémoire Pratique

## Partie 1 : Tableau Comparatif Détaillé TD-DFT vs OO-DFT/ΔDFT

| Aspect | TD-DFT (Ancien) | OO-DFT/ΔDFT (Nouveau) | Avantage pour BODIPY |
|:---|:---|:---|:---|
| **Théorie** | Réponse linéaire, oscillateur | Orbitales optimisées, état spécifique | ★★★★★ ΔDFT |
| **Précision S₁** | Surestime (erreur +0.3-0.5 eV) | Précision chimique (<0.05 eV) | ★★★★★ ΔDFT |
| **Précision T₁** | Sous-estime (erreur -0.3-0.5 eV) | Précision chimique (<0.05 eV) | ★★★★★ ΔDFT |
| **ΔE_ST** | Mauvais (erreur > 0.5 eV) | Excellent (erreur < 0.05 eV) | ★★★★★ ΔDFT |
| **λ_max** | Acceptable si bien calibré | Excellent (surtout avec ADC(2)) | ★★★★ Hybride |
| **Relaxation orbitale** | Non capturée (LR-TDDFT) | Explicitement capturée | ★★★★★ ΔDFT |
| **Doubles excitations** | Partiellement (RPA) | Implicites (meilleur traitement) | ★★★★ ΔDFT |
| **États CT** | Surcharge (charge-transfer band problématique) | Meilleur traitement | ★★★★ ΔDFT |
| **Coût computationnel** | Bas-Moyen | Moyen-Élevé (ΔUKS/ΔROKS rapides) | ★★★ TD-DFT pour screening |
| **SOC intégré** | Oui, mais imprécis | Non (nécessite méthode MR) | ★★ TD-DFT |
| **Compatibilité CPCM** | Oui (LR-PCM) | Oui (SS-PCM, meilleur) | ★★★ ΔDFT |
| **Applicabilité BODIPY** | ⚠ Problématique (open-shell character) | ★★★★★ Idéale | ★★★★★ ΔDFT |

---

## Partie 2 : Protocole de Calcul Recommandé (Résumé Exécutif)

### Stratégie en 6 étapes

```
ÉTAPE 1 (rapide)     → S0 optimisation (DFT, phase gaz)
        ↓
ÉTAPE 2 (rapide)     → S0 optimisation (DFT, CPCM-eau)   [REFERENCE]
        ↓
ÉTAPE 3 (cher)       → Excitation verticale (ADC(2) ou TD-DFT)  [λ_max]
        ↓
ÉTAPE 4 (cher)       → T1 optimisation (ΔUKS, CPCM)      [ISC]
        ↓
ÉTAPE 5 (très cher)  → S1 optimisation (ΔSCF, CPCM)      [PTT]
        ↓
ÉTAPE 6 (très cher)  → SOC (NEVPT2 ou TD-DFT)           [PDT]
        ↓
ANALYSE & DECISION   → Comparer prototypes, scorer les candidats
```

### Flux des données

```
S0_opt.gbw (Étape 2)
    ├─→ ADC2_vertical.inp  (Étape 3) → λ_max, spectrum
    ├─→ T1_opt.inp         (Étape 4) → E_T1, geometry
    ├─→ S1_opt.inp         (Étape 5) → E_S1, ΔE_ST
    └─→ NEVPT2_SOC.inp     (Étape 6) → SOC matrix

Résultats:  E_ad = E_S0 - E_S1  (PTT potential)
            ΔE_ST = E_S1 - E_T1  (ISC/PDT potential)
```

---

## Partie 3 : Guide de Sélection de Prototypes

### Critères d'évaluation

| Critère | Cible | Poids | Calcul ORCA |
|:---|:---|:---|:---|
| **λ_max (absorption)** | 600-900 nm (idéal: 750-850) | 25% | ADC(2) |
| **E_adiabatic (PTT)** | < 1.0 eV | 20% | ΔE_S0-S1 |
| **ΔE_ST (ISC/PDT)** | 0.05-0.15 eV | 25% | ΔE_S1-T1 |
| **SOC (ISC speed)** | > 50 cm⁻¹ (avec I) | 20% | NEVPT2/TD-DFT |
| **Targeting (charges)** | Q_TPP > +1 e | 10% | Mulliken/RESP |

### Tableau de scoring

```
Prototype | λ_max | E_ad | ΔE_ST | SOC | Targeting | TOTAL | Verdict
----------|-------|------|-------|-----|-----------|-------|----------
Proto-A   |  /25  | /20  | /25   | /20 | /10       | /100  |
Proto-B   |  /25  | /20  | /25   | /20 | /10       | /100  |
Proto-C   |  /25  | /20  | /25   | /20 | /10       | /100  |
```

**Règles de scoring :**
- λ_max ∈ [750-850]: 25/25; ∈ [600-900]: 20/25; ailleurs: ≤ 10/25
- E_ad < 0.8: 20/20; < 1.2: 15/20; ailleurs: < 10/20
- ΔE_ST < 0.1: 25/25; < 0.15: 20/25; > 0.3: < 10/25
- SOC > 100: 20/20; > 50: 15/20; < 10: < 5/20
- Q_TPP > +1.5: 10/10; +1 à +1.5: 8/10; < +0.5: < 5/10

---

## Partie 4 : Aide-Mémoire Pratique (A4 à Imprimer)

### Pour démarrer

```bash
# 1. Charger ORCA et configurer
module load orca/6.1
export PATH=/path/to/orca:$PATH

# 2. Créer les répertoires de travail
mkdir -p proto-{A,B,C}/{S0,S1,T1,ADC2,SOC}

# 3. Copier les fichiers d'entrée
cp S0_gas_opt.inp proto-A/
cp S0_water_opt.inp proto-A/

# 4. Lancer les calculs (exemple SLURM)
sbatch submit_S0.slurm

# 5. Vérifier le statut
squeue -u $USER
```

### Commandes clés ORCA

| Action | Commande |
|:---|:---|
| **Lancer calcul** | `orca input.inp > output.out &` |
| **Voir progression** | `tail -f output.out` |
| **Extraire énergie** | `grep "FINAL SINGLE POINT" output.out` |
| **Voir λ_max (ADC2)** | `grep "S_1 state" output.out` |
| **Vérifier SOC** | `grep -A5 "Spin-Orbit" output.out` |
| **Converger géométrie** | `grep "Geometry convergence" output.out` |
| **Vérifier fréquences** | `grep "imaginary frequencies" output.out` |

### Conversions utiles

$$\lambda_{\text{max}} (\text{nm}) = \frac{1240 \text{ eV·nm}}{E (\text{eV})}$$

$$\Delta E (\text{eV}) = E (\text{a.u.}) \times 27.211$$

$$E (\text{cm}^{-1}) = E (\text{eV}) \times 8066$$

### Signaux d'alerte

| Signal | Cause probable | Action |
|:---|:---|:---|
| SCF ne converge pas | Géométrie mauvaise | Revoir XYZ, réduire MaxStep |
| Fréquences imaginaires | Point selle, pas minimum | Relancer optimisation |
| S1 collapse → S0 | Pas de configuration excitée | Augmenter damping, utiliser TRAH |
| λ_max très différent | Mauvaise méthode/base | Benchmarking requis |
| SOC très faible (< 1) | Atome lourd absent ? | Vérifier composition moléculaire |

---

## Partie 5 : Chronogramme Réaliste (14 semaines)

### Semaine 1-3 : Préparation
- Bibliographie, sélection prototypes, préparation XYZ
- **Effort :** 20% calcul, 80% lecture/design

### Semaine 4 : S0 optimisations (6-8 heures CPU par prototype)
- S0 gas + S0 water pour les 3 prototypes
- **Total estimé :** 20-24 heures CPU
- **Durée réelle :** ~1 semaine (calculs parallèles)

### Semaine 5-6 : Excitations verticales (20-30 heures CPU par prototype)
- ADC(2) pour λ_max, spectres d'absorption
- **Total estimé :** 60-90 heures CPU
- **Durée réelle :** ~2 semaines (coûteux)

### Semaine 7-8 : États excités relaxés (30-50 heures CPU par prototype)
- T1 optimisation (rapide) + S1 optimisation (difficile)
- **Total estimé :** 90-150 heures CPU
- **Durée réelle :** ~2-3 semaines (S1 peut nécessiter retries)

### Semaine 9 : SOC et analyse post-traitement (50-100 heures CPU)
- NEVPT2 SOC (très cher) OU TD-DFT rapide
- Calcul MEP, charges, spectres
- **Total estimé :** 50-100 heures CPU
- **Durée réelle :** ~1 semaine (peut être parallélisé)

### Semaine 10-11 : Analyse et scoring
- Comparer prototypes, benchmarking
- Scorer les candidats
- **Effort :** 100% analyse, 0% calcul

### Semaine 12-14 : Rapport et soutenance
- Rédaction, diapositives, répétitions
- **Effort :** 100% rédaction/communication

**Total CPU estimé :** 220-370 heures (~ 10-15 jours CPU avec 8 processeurs)
**Parallélisation effective :** Les 3 prototypes peuvent être lancés simultanément
**Recommandation :** Démarrer S1 optim. et SOC dès que les étapes antérieures sont complètes

---

## Partie 6 : Stratégies de Réduction de Temps

Si le temps est limité (< 10 semaines) :

| Stratégie | Gain de temps | Compromise | |:---|:---|:---|
| Utiliser def-SVP partout au lieu de def-TZVP | -30% | Précision -0.05 eV | |Utiliser TD-DFT pour λ_max au lieu d'ADC(2) | -50% | Précision -0.1-0.2 eV | |Calculer SOC seulement pour meilleur prototype | -60% | Perdre comparaison S1-T1 | |Sauter S0 gas phase | -5% | Minimal | |Paralléliser 8 cores → 16 cores | -50% | Besoin ressources HPC | |Utiliser GPU (si disponible) | -75% | Besoin infrastructure GPU | |

**Recommandation combinée rapide :**
1. S0 en def-SVP (rapide)
2. λ_max en TD-DFT (rapide, 30 min)
3. T1 seulement, pas S1 (économiser 120+ min)
4. SOC en TD-DFT seulement (30 min)
5. Valider λ_max avec benchmarking pour fiabilité

**Temps total :** ~150-200 heures CPU (vs 220-370)

---

## Partie 7 : Résumé des Fichiers à Sauvegarder

```
projet/
├── proto-A/
│   ├── S0_water_opt.gbw        [CRITICAL]
│   ├── S0_water_opt.xyz        [CRITICAL]
│   ├── S1_water_opt.gbw        [Important]
│   ├── T1_water_opt.gbw        [Important]
│   ├── ADC2_vertical.out       [Important - contient λ_max]
│   ├── NEVPT2_SOC.out          [Important - contient SOC]
│   └── analysis_proto-A.txt    [Summary]
│
├── proto-B/
│   └── [même structure]
│
├── proto-C/
│   └── [même structure]
│
├── results_comparison.csv      [Tableau final]
├── prototypes_scoring.xlsx     [Matrice de décision]
└── rapport_stage_final.pdf     [Livrable]
```

**Archivage recommandé :**
- Compresser après chaque étape majeure
- Garder copies locales ET serveur distant (backup)
- Documenter numéro de version et date

---

## Partie 8 : Checklist Finale Avant Soutenance

- [ ] Tous les calculs terminés et validés
- [ ] Benchmarking effectué (méthodes validées)
- [ ] Tableau comparatif des 3 prototypes rédigé
- [ ] Graphiques λ_max, spectres, MEP générés
- [ ] Scoring des candidats complété
- [ ] Rapport (draft) relecture par co-encadrant
- [ ] Diapositives préparées (15-20 slides)
- [ ] Résumé exécutif (1 page) écrit
- [ ] References formatées (ACS ou JACS standard)
- [ ] Répétition de la présentation (15 min)

---

**Document créé pour un démarrage rapide — À imprimer et afficher dans le bureau !**
