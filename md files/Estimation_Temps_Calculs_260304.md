# Estimation des Temps de Calcul (Version 260304)

> **Mise à jour : 04 mars 2026 (260304)**
> - Exécution locale 16 Go RAM / TD-DFT ωB97X-D3
> - Configuration : 4 cœurs, %maxcore 3500
> - Séquentiel local (nohup) au lieu de SLURM/HPC

---

## Tableau d'estimation des temps de calcul (Local 16 Go, 4 cœurs)

Les temps indiqués représentent le **temps de calcul (Wall Time)** pour une étape sur un prototype BODIPY (~30 atomes), en utilisant ORCA 6.1 avec configuration locale.

| Phase | Méthode & Niveau de Théorie | Propriété Calculée | Complexité | Temps Estimé (4 cœurs) |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1 : Optimisation S₀** | B3LYP-D3/def2-SVP (phase gaz) | Géométrie S₀ | DFT (Économique) | **30-60 minutes** |
| **Phase 1 : Optimisation S₀** | B3LYP-D3/def2-SVP (SMD mixed) | Géométrie S₀ (solvaté) | DFT (Économique) | **45-90 minutes** |
| **Phase 2 : Absorption Verticale** | TD-DFT ωB97X-D3/def2-SVP | λ_max (excitation verticale) | TD-DFT (Rapide) | **15-30 minutes** |
| **Phase 3 : Triplet Relaxé** | ΔUKS B3LYP/def2-SVP + SMD | Optimisation géométrie T₁ | ΔDFT (Robuste) | **60-120 minutes** |
| **Phase 3 : Singulet Relaxé** | ΔUKS B3LYP/def2-SVP + SMD (ΔSCF) | Optimisation géométrie S₁ | ΔDFT (Difficile) | **120-180 minutes** |
| **Phase 4 : SOC (Standard)** | ΔDFT+SOC (ZORA, dosoc) | Constantes SOC (S₁↔Tₙ) | ΔDFT+SOC (Rapide) | **30-60 minutes** |
| **Phase 4 : SOC (Validation)** | FIC-NEVPT2/def2-TZVP | Validation ponctuelle SOC | MR-WFT (Très coûteux) | **150-300 minutes** |
| **Phase 5 : Post-Traitement** | Multiwfn (ESP, charges) | MEP, charges Hirshfeld | Post-SCF (Très rapide) | **5-15 minutes** |

---

## Temps Total par Molécule

### Configuration locale (4 cœurs, 16 Go RAM)

| Molécule | S₀ (gaz+eau) | TD-DFT | T₁ | S₁ | SOC | MEP | **TOTAL** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Référence** | 75-150 min | 15-30 min | 60-120 min | 120-180 min | 30-60 min | 5-15 min | **5-8 h** |
| **Iodo-BODIPY** | 75-150 min | 15-30 min | 60-120 min | 120-180 min | 30-60 min | 5-15 min | **5-8 h** |
| **TPP-Iodo-BODIPY** | 75-150 min | 15-30 min | 60-120 min | 120-180 min | 30-60 min | 15-30 min | **5-8 h** |

---

## Temps Total du Projet (3 molécules, séquentiel)

### Sans buffer S₁

| Étape | Temps unitaire | 3 molécules (séquentiel) |
| :--- | :--- | :--- |
| S₀ (gaz + eau) | 75-150 min | 4-8 h |
| TD-DFT vertical | 15-30 min | 1-1.5 h |
| T₁ optimisation | 60-120 min | 3-6 h |
| S₁ optimisation | 120-180 min | 6-9 h |
| ΔDFT+SOC | 30-60 min | 1.5-3 h |
| MEP/ciblage | 5-15 min | 0.5-1 h |
| **TOTAL** | **~5-8 h/mol** | **~16-28 h** |

### Avec buffer S₁ (+200-300%)

| Étape | Temps unitaire | 3 molécules (séquentiel) |
| :--- | :--- | :--- |
| S₀ (gaz + eau) | 75-150 min | 4-8 h |
| TD-DFT vertical | 15-30 min | 1-1.5 h |
| T₁ optimisation | 60-120 min | 3-6 h |
| S₁ optimisation (buffer) | 360-540 min | 18-27 h |
| ΔDFT+SOC | 30-60 min | 1.5-3 h |
| MEP/ciblage | 5-15 min | 0.5-1 h |
| **TOTAL** | **~10-15 h/mol** | **~28-46 h** |

---

## Détail par Phase

### Phase 1 : Optimisation S₀ (75-150 min/molécule)

```bash
# S₀ phase gaz (30-60 min)
%maxcore 3500
%pal nprocs 4 end
! B3LYP D3BJ def2-SVP Opt Freq

# S₀ eau (SMD mixed) (45-90 min)
%maxcore 3500
%pal nprocs 4 end
! B3LYP D3BJ def2-SVP Opt Freq CPCM SMD
%cpcm
  SMDSolvent "mixed"
end
```

**Facteurs influençant le temps :**
- Taille molécule (~30 atomes = standard)
- Convergence géométrie (TIGHTOPT = +20%)
- Présence atomes lourds (Iode = +10%)

---

### Phase 2 : TD-DFT Vertical (15-30 min/molécule)

```bash
# TD-DFT ωB97X-D3 (rapide, adapté 16 Go)
%maxcore 3500
%pal nprocs 4 end
! wB97X-D3 def2-SVP TightSCF TD-DFT(nroots=10) CPCM SMD
%cpcm
  SMDSolvent "mixed"
end
```

**Facteurs influençant le temps :**
- Nombre de racines (nroots=10 = standard)
- Base (def2-SVP = rapide, def2-TZVP = +50%)

---

### Phase 3 : T₁ Optimisation (60-120 min/molécule)

```bash
# T₁ ΔUKS (robuste)
%maxcore 3500
%pal nprocs 4 end
! B3LYP D3BJ def2-SVP Opt Freq UKS MoreAdhoc
%scf
  MOM true
end
```

**Facteurs influençant le temps :**
- Convergence SCF (MOM = stable)
- Présence atomes lourds (Iode = +10%)

---

### Phase 4 : S₁ Optimisation (120-180 min/molécule, buffer +200-300%)

```bash
# S₁ ΔSCF (délicat, nécessite stratégies)
%maxcore 3500
%pal nprocs 4 end
! B3LYP D3BJ def2-SVP Opt Freq UKS MoreAdhoc
%scf
  MOM true
  NoIncFock true
  MaxIter 150
  DampPercentage 40
end
```

**Stratégies de convergence (en cas d'échec) :**
1. Augmenter DampPercentage (40→60)
2. Utiliser LevelShift (0.2→0.5)
3. Réduire MaxStep (0.2→0.1)
4. Utiliser DIIS_TRAH avec TRAH_MaxDim 20
5. Changer guess électronique (HOMO→LUMO, HOMO-1→LUMO, HOMO→LUMO+1)

**Buffer recommandé : +200-300% (3-5 tentatives)**

---

### Phase 5 : SOC (30-60 min/molécule)

```bash
# ΔDFT+SOC (ZORA, dosoc - standard)
%maxcore 3500
%pal nprocs 4 end
! B3LYP D3BJ def2-SVP ZORA DOSOC TightSCF
%rel
  DoSOC true
end
```

**Validation ponctuelle NEVPT2 (optionnel, 150-300 min) :**
```bash
# NEVPT2 (seulement si ressources disponibles)
%maxcore 3500
%pal nprocs 4 end
! NEVPT2 def2-TZVP ZORA
```

---

## Comparaison des Méthodes

### ΔDFT+SOC vs NEVPT2

| Méthode | Temps | Précision | Recommandation |
| :--- | :--- | :--- | :--- |
| **ΔDFT+SOC** | 30-60 min | Bonne (tendances) | **Standard (recommandé)** |
| **NEVPT2** | 150-300 min | Excellente | Validation ponctuelle seulement |

**Gain : 10× avec ΔDFT+SOC**

---

### def2-SVP vs def2-TZVP

| Base | Temps | Précision | Usage |
| :--- | :--- | :--- | :--- |
| **def2-SVP** | 1× (référence) | Bonne | Screening, local 16 Go |
| **def2-TZVP** | +50-100% | Excellente | Validation, si ressources |

**Test comparatif semaine 3 :**
- Si MAE < 5 nm vs expérimental → def2-SVP (économie 3h/molécule)
- Si MAE > 10 nm → def2-TZVP (nécessaire)

---

## Optimisation du Temps de Calcul

### 1. Utiliser def2-SVP (si validé par test semaine 3)

**Économie : ~3h par molécule, ~9h total**

### 2. ΔDFT+SOC au lieu de NEVPT2

**Économie : ~2-4h par molécule, ~6-12h total**

### 3. Lancer S₁ avec bon guess (gen_s1_guesses.sh)

**Économie : +50% sur tentatives échouées**

### 4. Utiliser run_troubleshoot_S1.sh

**Automatisation de l'escalade, gain de temps manuel**

---

## Planning Réaliste (14 semaines, local 16 Go)

| Semaine | Phase | Temps calcul | Temps total (avec buffer) |
| :--- | :--- | :--- | :--- |
| 1-2 | Immersion | - | - |
| 3 | Construction + Test | 2-3 h | 4-6 h |
| 4 | S₀ optimisations | 4-8 h | 4-8 h |
| 5-6 | TD-DFT vertical | 1-1.5 h | 2-3 h |
| 7 | T₁ optimisations | 3-6 h | 3-6 h |
| 8 | S₁ optimisations | 6-9 h | 18-27 h (buffer) |
| 9 | SOC | 1.5-3 h | 1.5-3 h |
| 10 | Analyse | - | 4-8 h |
| 11 | Scoring + Décision | - | 4-8 h |
| 12-14 | Rapport + Soutenance | - | - |

**Total calcul : ~20-30 h mur (séquentiel, 4 cœurs)**

**Total projet : ~150-200 h (incluant analyse, rédaction)**

---

## Recommandations Finales

### Pour minimiser les temps

1. **Valider def2-SVP semaine 3** (économie 9h)
2. **Utiliser ΔDFT+SOC standard** (économie 6-12h)
3. **Pré-tester guesses S₁** (gen_s1_guesses.sh)
4. **Archiver systématiquement** (éviter recalculs)

### Buffer recommandé

| Étape | Buffer | Justification |
| :--- | :--- | :--- |
| S₀ | +0% | Robuste, converge toujours |
| TD-DFT | +0% | Rapide, stable |
| T₁ | +20% | Robuste, parfois lent |
| S₁ | +200-300% | Délicat, 3-5 tentatives |
| SOC | +0% | Rapide, stable |

---

**Document d'estimation — Version 260304 (04 mars 2026)**

**Configuration : Local 16 Go RAM / 4 cœurs / TD-DFT ωB97X-D3**
