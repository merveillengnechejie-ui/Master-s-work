# Concept 8 — Modèles de Solvation : SMD, CPCM, ptSS-PCM
## Simuler l'environnement biologique sans calculer chaque molécule d'eau

---

## 1. Pourquoi la solvation est importante

Nos molécules fonctionnent dans un environnement aqueux (cytoplasme tumoral, pH 6.5–7.4). L'eau affecte :

```
Sans solvant (phase gaz) :
  λ_max calculé ≈ 580 nm

Avec solvant (eau) :
  λ_max calculé ≈ 650 nm  ← plus proche de l'expérience

Erreur si on ignore le solvant : ~70 nm !
```

---

## 2. Les deux approches : implicite vs explicite

### Solvation implicite (notre approche principale)
```
Molécule entourée d'une cavité diélectrique continue
ε(eau) = 78.4

Avantage : rapide, pas de configurations à moyenner
Inconvénient : ignore les liaisons H spécifiques
```

### Solvation explicite (test de validation)
```
Molécule + N molécules d'eau explicites + solvant implicite
Avantage : capture les liaisons H
Inconvénient : lent, nécessite une moyenne sur les configurations
```

---

## 3. Les modèles implicites dans ORCA

### CPCM (Conductor-like PCM)
```orca
! CPCM(water)
```
- Modèle de cavité conductrice
- Rapide, robuste
- Paramètres de cavité standards

### SMD (Solvation Model based on Density)
```orca
! CPCM(water)
%cpcm
  SMD true
  SMDSolvent "water"
end
```
- Améliore les rayons de cavité avec des paramètres empiriques
- Plus précis que CPCM seul pour les énergies de solvatation
- **Notre choix pour toutes les optimisations géométriques**

> **⚠️ Bug critique** : `SMDSolvent "mixed"` est **invalide** dans ORCA 6.1.1. Ce mot-clé tombe silencieusement en phase gaz sans message d'erreur. Toujours utiliser `SMDSolvent "water"`.

---

## 4. Équilibre vs Non-équilibre : la distinction essentielle

C'est la distinction la plus importante pour les calculs d'états excités.

### Solvation à l'équilibre
```
Le solvant a le temps de se réorganiser autour du soluté.
Timescale : picosecondes à nanosecondes

Correct pour :
  - Optimisation géométrie S₀ (état stable)
  - Optimisation géométrie T₁ (état stable)
  - Énergie de l'état fondamental
```

### Solvation hors-équilibre (ptSS-PCM)
```
L'absorption d'un photon est instantanée (10⁻¹⁵ s).
Le solvant n'a PAS le temps de se réorganiser.
Seule la polarisation électronique rapide répond.

Correct pour :
  - Excitations verticales (λ_max)
  - Émission (fluorescence)
  - Tout calcul TD-DFT d'excitation
```

**Erreur si on utilise l'équilibre pour les excitations** :
```
Solvation équilibre pour λ_max : erreur ~0.05–0.15 eV
Solvation non-équilibre (ptSS-PCM) : erreur ~0.02–0.05 eV
```

### Activer ptSS-PCM dans ORCA
```orca
%cpcm
  SMD true
  SMDSolvent "water"
  StateSpecificSolvation true    ← active ptSS-PCM
end
```

---

## 5. Tableau récapitulatif : quel modèle pour quelle étape

| Calcul | Mode | Mot-clé ORCA |
|--------|------|-------------|
| Optimisation S₀ | Équilibre | `SMD true` + `SMDSolvent "water"` |
| Optimisation T₁ | Équilibre | `SMD true` + `SMDSolvent "water"` |
| Excitations verticales TD-DFT | **Non-équilibre** | + `StateSpecificSolvation true` |
| Δ-DFT énergie T₁ | **Non-équilibre** | + `StateSpecificSolvation true` |
| SOC (ΔDFT+SOC) | Équilibre | `SMD true` + `SMDSolvent "water"` |
| xTB (Tier 0) | Équilibre ALPB | `--alpb water` (ligne de commande) |

---

## 6. Test de validation : solvant explicite

Pour répondre à la question "le modèle implicite est-il suffisant ?", nous effectuons un test sur 1 molécule :

```
1. Prendre la meilleure molécule du benchmark TD-DFT
2. Ajouter 3–5 molécules H₂O aux sites donneurs/accepteurs de liaisons H
3. Calculer λ_max avec H₂O explicites + CPCM bulk
4. Comparer avec λ_max CPCM seul

Si |Δλ_max| < 5 nm → modèle implicite suffisant ✓
Si |Δλ_max| > 10 nm → mentionner comme limitation ⚠️
```

---

## 7. Résumé visuel

```
Votre molécule BODIPY dans la tumeur :

Réalité :
  BODIPY entouré de ~1000 molécules H₂O
  + ions Na⁺, Cl⁻, K⁺
  + protéines, lipides
  → Impossible à calculer exactement

Notre approximation :
  BODIPY dans une cavité diélectrique (ε = 78.4)
  + paramètres SMD pour les rayons atomiques
  + ptSS-PCM pour les excitations (polarisation rapide)
  → Erreur résiduelle ~0.05–0.10 eV sur λ_max
  → Acceptable pour notre objectif (tendances, classement)
```

---

## 📖 Références clés

- Marenich et al., *J. Phys. Chem. B* 2009, 113, 6378 — modèle SMD
- Improta et al., *J. Chem. Phys.* 2006, 125, 054103 — ptSS-PCM
- ORCA 6.1.1 Manual, Chapitre 12 (Solvation)
