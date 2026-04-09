# Concept 5 — La DFT Expliquée Simplement
## De l'équation de Schrödinger aux calculs ORCA

---

## 1. Le problème fondamental : trop d'électrons

Pour décrire une molécule quantiquement, il faut résoudre l'**équation de Schrödinger** :

```
Ĥ Ψ = E Ψ

Ĥ = opérateur hamiltonien (cinétique + répulsions e⁻-e⁻ + attractions e⁻-noyaux)
Ψ = fonction d'onde à N électrons
E = énergie totale de la molécule
```

**Problème** : Pour N électrons, Ψ dépend de 3N coordonnées spatiales. Pour le BODIPY (~50 atomes, ~200 électrons), c'est **impossible à résoudre exactement** même avec les supercalculateurs actuels.

---

## 2. L'idée de la DFT : remplacer Ψ par ρ

La **Théorie de la Fonctionnelle de la Densité (DFT)** repose sur un théorème de Hohenberg-Kohn (1964) :

> *L'énergie d'un système est une fonctionnelle unique de la densité électronique ρ(r).*

Au lieu de calculer Ψ (fonction de 3N variables), on calcule **ρ(r)** (fonction de 3 variables seulement) :

```
Ψ(r₁, r₂, ..., r_N)  →  ρ(r)  =  Σᵢ |ψᵢ(r)|²

3N variables                3 variables
Impossible pour N > 10      Faisable pour N = 200 !
```

---

## 3. Orbitales de Kohn-Sham

En pratique, on utilise le formalisme de **Kohn-Sham** : on résout N équations mono-électroniques couplées :

```
[-½∇² + v_eff(r)] ψᵢ(r) = εᵢ ψᵢ(r)

v_eff = v_ext + v_Hartree + v_xc

v_ext    : potentiel des noyaux
v_Hartree: répulsion électron-électron classique
v_xc     : potentiel d'échange-corrélation (le terme inconnu !)
```

**Le problème** : v_xc est inconnu exactement. C'est là qu'interviennent les **fonctionnelles**.

---

## 4. Les fonctionnelles : approximations de v_xc

Une **fonctionnelle** est une approximation de v_xc. Il en existe des centaines. Voici celles que nous utilisons :

| Fonctionnelle | Type | % HF | Points forts | Points faibles |
|---|---|---|---|---|
| **B3LYP** | Global hybrid | 20% | Standard, bien testé | Surestime λ_max BODIPY |
| **PBE0** | Global hybrid | 25% | Bon équilibre S₁/T₁ | États CT sous-estimés |
| **ωB97X-D** | Range-separated | 22→100% | Meilleur pour CT | Plus lent |
| **CAM-B3LYP** | Range-separated | 19→65% | Bon pour S₁ | Peut surestimer gap |
| **M06-2X** | Meta-hybrid | 54% | Bon pour 2PA | Peut surestimer CT |
| **MN15** | Meta-hybrid | 44% | Meilleur λ_max BODIPY | Moins testé |

> **Pourquoi tester 6 fonctionnelles ?** Parce qu'aucune n'est parfaite pour tous les systèmes. Le benchmark nous dit laquelle est la meilleure pour **nos** molécules BODIPY-NTR spécifiques.

---

## 5. Les bases : discrétiser l'espace

Les orbitales ψᵢ sont développées sur une **base de fonctions** (gaussiennes) :

```
ψᵢ(r) = Σ_μ c_μi φ_μ(r)

φ_μ = fonctions de base (gaussiennes centrées sur les atomes)
c_μi = coefficients à optimiser
```

| Base | Taille | Coût | Usage |
|------|--------|------|-------|
| **def2-SVP** | Petite | Rapide | Criblage, optimisation géométrie |
| **def2-TZVP** | Moyenne | Modéré | Énergies d'excitation finales |
| **def2-QZVP** | Grande | Lent | Validation ponctuelle |

**Règle pratique** :
- Optimisation géométrie → def2-SVP (suffisant)
- Calcul λ_max final → def2-TZVP (plus précis)
- Jamais def2-QZVP sur 32 GB RAM pour BODIPY (~60 atomes)

---

## 6. Le cycle SCF : comment ORCA résout les équations

```
1. Deviner une densité initiale ρ⁰ (guess)
        │
        ▼
2. Calculer v_eff[ρ]
        │
        ▼
3. Résoudre les équations KS → nouvelles orbitales ψᵢ
        │
        ▼
4. Calculer nouvelle densité ρ_new = Σ |ψᵢ|²
        │
        ▼
5. Convergé ? (|ρ_new - ρ_old| < seuil)
   OUI → Énergie finale
   NON → ρ_old = ρ_new → retour à l'étape 2
```

Ce cycle s'appelle **SCF (Self-Consistent Field)**. Si ORCA dit "SCF not converged", c'est que ce cycle n'a pas convergé → voir [`../troubleshooting/T1_convergence_SCF.md`](../troubleshooting/T1_convergence_SCF.md).

---

## 7. TD-DFT : étendre la DFT aux états excités

La DFT standard calcule l'état fondamental S₀. Pour les états excités (S₁, T₁), on utilise la **TD-DFT (Time-Dependent DFT)** :

```
TD-DFT résout les équations de Casida :
[A  B ] [X]   [1  0 ] [X]
[B* A*] [Y] = [0 -1 ] [Y] × ω

ω = énergie d'excitation (en eV)
X,Y = amplitudes de transition
```

**Ce que TD-DFT calcule** :
- Énergies d'excitation verticales (λ_max)
- Forces d'oscillateur (intensité d'absorption)
- Orbitales de transition naturelles (NTO)

**Limitation pour les BODIPY** : TD-DFT surestime S₁ et sous-estime T₁ pour les BODIPY (caractère légèrement couche ouverte). C'est pourquoi nous utilisons Δ-DFT pour ΔE_ST → voir [`07_pourquoi_Delta_DFT.md`](07_pourquoi_Delta_DFT.md).

---

## 8. Lire un fichier de sortie ORCA

Après un calcul TD-DFT, chercher dans le `.out` :

```
ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
---------------------------------------------------------------------------
State   Energy    Wavelength   fosc         T2         TX        TY        TZ
        (cm-1)      (nm)                  (au**2)     (au)      (au)      (au)
---------------------------------------------------------------------------
   1   15234.5     656.4       0.8234      ...
   2   17891.2     559.0       0.0123      ...
```

- **State 1** = S₁ (premier état excité singulet)
- **Energy** = énergie en cm⁻¹ (diviser par 8065.5 pour avoir eV)
- **Wavelength** = λ_max en nm ← c'est ce que vous cherchez
- **fosc** = force d'oscillateur (> 0.3 = absorption forte)

---

## 📖 Références clés

- Kohn & Sham, *Phys. Rev.* 1965, 140, A1133 — article fondateur KS-DFT
- Alkhatib et al., *RSC Adv.* 2022, 12, 1704 — benchmark fonctionnelles BODIPY
- ORCA 6.1.1 Manual, Chapitre 8 (DFT) et Chapitre 9 (TD-DFT)

---

*Suite → [`06_etats_excites_S1_T1.md`](06_etats_excites_S1_T1.md)*
