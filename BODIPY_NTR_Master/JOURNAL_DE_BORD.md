# Journal de Bord — Projet Master BODIPY-NTR
## À remplir chaque semaine

---

> **Instructions** : Remplir ce journal chaque vendredi soir. Il sert à la fois de suivi personnel et de documentation pour le mémoire. Les entrées détaillées facilitent la rédaction finale.

---

## Semaine 1 — Installation et validation

**Dates** : ___/___/___ au ___/___/___

### Logiciels installés
| Logiciel | Version | Statut |
|----------|---------|--------|
| ORCA | | ☐ OK ☐ Problème |
| xTB | | ☐ OK ☐ Problème |
| RDKit | | ☐ OK ☐ Problème |
| Multiwfn | | ☐ OK ☐ Problème |
| Python | | ☐ OK ☐ Problème |

### Vérifications critiques
- ☐ sTDA disponible dans ORCA 6.1.1 : OUI / NON
- ☐ CC2 disponible dans ORCA 6.1.1 : OUI / NON
- ☐ Bug SMDSolvent "mixed" corrigé
- ☐ Test de chaîne BODIPY-Ph réussi

### Test de chaîne BODIPY-Ph
- λ_max calculé : _____ nm
- λ_max expérimental : 505 nm
- Erreur : _____ nm
- Fonctionnelle utilisée : _____

### Problèmes rencontrés
```
[Décrire ici tout problème rencontré et comment il a été résolu]
```

### Temps passé
- Calculs : _____ h
- Lecture/bibliographie : _____ h
- Rédaction/documentation : _____ h

---

## Semaine 2 — Construction des molécules

**Dates** : ___/___/___ au ___/___/___

### Molécules construites
| # | Molécule | Fichier .xyz | xTB convergé | HOMO-LUMO gap (eV) |
|---|----------|-------------|-------------|-------------------|
| 1 | BODIPY-Ph | | ☐ | |
| 2 | BODIPY-Ph-NO₂ | | ☐ | |
| 3 | BODIPY-Ph-NH₂ | | ☐ | |
| 4 | Iodo-BODIPY | | ☐ | |
| 5 | Iodo-BODIPY-NO₂ | | ☐ | |
| 6 | Iodo-BODIPY-NH₂ | | ☐ | |
| 7 | TPP-Iodo-BODIPY | | ☐ | |
| 8 | aza-BODIPY-NO₂ | | ☐ | |

### Données expérimentales collectées
- ☐ `data/experimental_benchmark.csv` créé
- Valeurs vérifiées dans les articles originaux :
  - Baig 2024 : ΦT = _____ (vérifié ☐)
  - Bartusik-Aebisher 2025 : η(tBu) = _____ % (vérifié ☐)

### Observations sur les géométries xTB
```
[Noter les géométries inhabituelles, angles dièdres importants, etc.]
```

---

## Semaine 3 — Optimisation S₀ + sTDA

**Dates** : ___/___/___ au ___/___/___

### Optimisations S₀ complétées
| Molécule | Gaz ✓ | Eau ✓ | Fréq. imag. | Remarques |
|----------|-------|-------|-------------|-----------|
| BODIPY-Ph | ☐ | ☐ | ☐ | |
| BODIPY-Ph-NO₂ | ☐ | ☐ | ☐ | |
| BODIPY-Ph-NH₂ | ☐ | ☐ | ☐ | |
| Iodo-BODIPY | ☐ | ☐ | ☐ | |
| Iodo-BODIPY-NO₂ | ☐ | ☐ | ☐ | |
| Iodo-BODIPY-NH₂ | ☐ | ☐ | ☐ | |
| TPP-Iodo-BODIPY | ☐ | ☐ | ☐ | |
| aza-BODIPY-NO₂ | ☐ | ☐ | ☐ | |

### Résultats sTDA (λ_max en nm)
| Molécule | λ_max sTDA | f_S1 | Remarques |
|----------|-----------|------|-----------|
| BODIPY-Ph | | | |
| BODIPY-Ph-NO₂ | | | |
| BODIPY-Ph-NH₂ | | | |
| Iodo-BODIPY | | | |

---

## Semaines 4–5 — Benchmark TD-DFT

**Dates** : ___/___/___ au ___/___/___

### Résultats benchmark (λ_max en nm)

| Molécule | Exp. | ωB97X-D | CAM-B3LYP | PBE0 | B3LYP | M06-2X | MN15 |
|----------|------|---------|-----------|------|-------|--------|------|
| BODIPY-Ph | 505 | | | | | | |
| Br-BODIPY | 535 | | | | | | |
| I-BODIPY | 545 | | | | | | |

### Métriques de benchmark (MAE en nm)
| Fonctionnelle | MAE (nm) | MAE (eV) | Recommandée ? |
|---|---|---|---|
| ωB97X-D | | | ☐ |
| CAM-B3LYP | | | ☐ |
| PBE0 | | | ☐ |
| B3LYP | | | ☐ |
| M06-2X | | | ☐ |
| MN15 | | | ☐ |

**Fonctionnelle sélectionnée** : _______________
**Justification** : _______________

---

## Semaines 5–6 — Protocole NTR ON/OFF

**Dates** : ___/___/___ au ___/___/___

### Résultats activation NTR
| Paire | λ_max OFF | λ_max ON | Δλ_max | ΔE_ST OFF | ΔE_ST ON | ΔΔE_ST |
|-------|----------|---------|--------|----------|---------|--------|
| BODIPY-Ph | | | | | | |
| Iodo-BODIPY | | | | | | |
| aza-BODIPY | | | | | | |

### Observations
```
[Décrire les tendances observées : quelle molécule montre le plus grand switch ?]
```

---

## Semaine 7 — Δ-DFT + SOC

**Dates** : ___/___/___ au ___/___/___

### Résultats Δ-DFT ΔE_ST (eV)
| Molécule | ΔE_ST TD-DFT | ΔE_ST Δ-DFT | Différence | Type I score |
|----------|-------------|------------|-----------|-------------|
| BODIPY-Ph-NH₂ | | | | |
| Iodo-BODIPY-NH₂ | | | | |

### Résultats SOC (cm⁻¹)
| Molécule | SOC S₁↔T₁ | Interprétation |
|----------|----------|----------------|
| BODIPY-Ph-NH₂ | | |
| Iodo-BODIPY-NH₂ | | |

### Observation clé
```
[La différence TD-DFT vs Δ-DFT pour ΔE_ST confirme-t-elle la nécessité de Δ-DFT ?]
```

---

## Semaine 8 — Scoring et décision

**Dates** : ___/___/___ au ___/___/___

### Scores finaux
| Molécule | PDT_Score | PTT_Score | Synergy_Score | Go/No-Go |
|----------|----------|----------|--------------|---------|
| BODIPY-Ph-NH₂ | | | | |
| Iodo-BODIPY-NH₂ | | | | |
| aza-BODIPY-NH₂ | | | | |
| TPP-Iodo-BODIPY | | | | |

**Top 3 candidats** :
1. _______________
2. _______________
3. _______________

**Justification du choix** :
```
[Expliquer pourquoi ces 3 molécules sont les meilleures candidates]
```

---

## Semaines 9–12 — Rédaction

### Avancement rédaction
| Section | Semaine 9 | Semaine 10 | Semaine 11 | Semaine 12 |
|---------|----------|-----------|-----------|-----------|
| Introduction | ☐ | ☐ | ☐ | ☐ |
| État de l'art | ☐ | ☐ | ☐ | ☐ |
| Méthodes | ☐ | ☐ | ☐ | ☐ |
| Résultats | ☐ | ☐ | ☐ | ☐ |
| Discussion | | ☐ | ☐ | ☐ |
| Conclusion | | | ☐ | ☐ |
| Figures | ☐ | ☐ | ☐ | ☐ |
| Rapport final | | | | ☐ |
| Présentation | | | | ☐ |
