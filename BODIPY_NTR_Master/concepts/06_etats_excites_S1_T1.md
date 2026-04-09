# Concept 6 — États Excités S₁ et T₁, ISC et SOC
## Le cœur quantique de la PDT

---

## 1. Singulet vs Triplet : une question de spin

Chaque électron possède un **spin** : +½ (↑) ou −½ (↓).

```
État singulet S (multiplicité = 1) :
  Spins appariés : ↑↓
  Moment magnétique total = 0
  → Diamagnétique

État triplet T (multiplicité = 3) :
  Spins parallèles : ↑↑
  Moment magnétique total = 1
  → Paramagnétique
  → 3 sous-états : ms = -1, 0, +1
```

**Règle de Hund** : Pour deux électrons dans des orbitales différentes, l'état triplet est plus stable (énergie plus basse) que le singulet correspondant.

```
Énergie
  │
  │  S₁ ─────  (singulet excité)
  │
  │  T₁ ─────  (triplet excité, plus bas que S₁)
  │
  │  S₀ ─────  (singulet fondamental)
```

---

## 2. L'écart singulet-triplet ΔE_ST

```
ΔE_ST = E(S₁) - E(T₁)

Toujours positif (S₁ > T₁ en énergie)
```

**Origine physique de ΔE_ST** : L'écart vient de l'**échange électronique** (interaction de Coulomb entre électrons de même spin). Plus les orbitales HOMO et LUMO se chevauchent, plus ΔE_ST est grand.

```
Grand chevauchement HOMO-LUMO → Grand ΔE_ST → ISC lente → PDT faible
Petit chevauchement HOMO-LUMO → Petit ΔE_ST → ISC rapide → PDT forte
```

**Pour les BODIPY avec atomes lourds** : L'iode perturbe les orbitales et réduit le chevauchement → ΔE_ST diminue → ISC s'accélère.

---

## 3. L'Intersystem Crossing (ISC)

L'ISC est la transition **interdite** S₁ → T₁ (changement de multiplicité de spin).

```
S₁ (↑↓*)  →  T₁ (↑↑*)

Interdit par les règles de sélection de spin !
Mais rendu possible par le couplage spin-orbite (SOC)
```

**Règle d'El-Sayed** : L'ISC est favorisée quand le changement de multiplicité s'accompagne d'un changement de caractère orbital :

```
¹(π→π*) → ³(n→π*)  : ISC rapide  ✓
¹(π→π*) → ³(π→π*)  : ISC lente   ✗ (mais compensée par SOC fort)
```

**Taux d'ISC** (approximation de Fermi) :
```
k_ISC ∝ |⟨T₁|Ĥ_SOC|S₁⟩|² / ΔE_ST²

Plus SOC est grand → k_ISC augmente
Plus ΔE_ST est petit → k_ISC augmente
```

---

## 4. Le Couplage Spin-Orbite (SOC)

Le SOC est l'interaction entre le **moment magnétique de spin** de l'électron et son **moment orbital** :

```
Ĥ_SOC = α² Σᵢ (1/rᵢ³) Lᵢ · Sᵢ

α = constante de structure fine (~1/137)
L = moment angulaire orbital
S = moment de spin
r = distance au noyau
```

**Effet d'atome lourd** : Le SOC scale comme Z⁴ (Z = numéro atomique) :

```
H  (Z=1)  : SOC ≈ 0.0001 cm⁻¹
C  (Z=6)  : SOC ≈ 0.03 cm⁻¹
Br (Z=35) : SOC ≈ 30–60 cm⁻¹   ← utile
I  (Z=53) : SOC ≈ 80–150 cm⁻¹  ← très utile
```

C'est pourquoi nous ajoutons de l'iode aux positions 2,6 du BODIPY !

---

## 5. Comment calculer ΔE_ST avec Δ-DFT

### Méthode TD-DFT (insuffisante pour BODIPY)

```
ΔE_ST(TD-DFT) = E_TD-DFT(S₁) - E_TD-DFT(T₁)
Erreur typique : > 0.3 eV  ← trop imprécis
```

### Méthode Δ-DFT (notre choix)

On calcule S₀ et T₁ comme deux **états SCF séparés** :

```
Étape 1 : Calculer S₀ (RKS, multiplicité 1)
  E(S₀) avec géométrie optimisée S₀

Étape 2 : Calculer T₁ (UKS, multiplicité 3)
  E(T₁) avec géométrie optimisée T₁

Étape 3 : ΔE_ST adiabatique
  ΔE_ST = E(S₁, géom S₁) - E(T₁, géom T₁)
```

**Pourquoi "adiabatique" ?** Parce qu'on utilise la géométrie relaxée de chaque état (pas la géométrie verticale de S₀). C'est plus réaliste physiquement.

**Précision Δ-DFT** : MAE < 0.05 eV (précision chimique) vs > 0.3 eV pour TD-DFT.

---

## 6. Comment calculer SOC avec ORCA

Nous utilisons l'approche **ΔDFT+SOC perturbatif** avec l'approximation ZORA :

```orca
! UKS PBE0 D3BJ def2-SVP ZORA RIJCOSX TightSCF
%tddft
  dosoc true
  SOCROTs 20
end
```

**Ce que ORCA calcule** :
```
⟨S₁|Ĥ_SOC|T₁⟩  en cm⁻¹

Chercher dans le .out :
"Spin-Orbit Coupling elements"
  S1 <-> T1 : XX.X cm-1
```

**Interprétation** :
- < 10 cm⁻¹ : SOC faible, ISC lente
- 10–50 cm⁻¹ : SOC modéré, ISC possible
- > 50 cm⁻¹ : SOC fort, ISC rapide (avec I)

---

## 7. Résumé : ce que nous calculons et pourquoi

| Propriété | Méthode | Précision | Lien thérapeutique |
|-----------|---------|-----------|-------------------|
| λ_max | TD-DFT/ωB97X-D | MAE ~0.15 eV | Fenêtre NIR-I |
| ΔE_ST | Δ-DFT (ΔROKS) | MAE < 0.05 eV | Efficacité ISC → PDT |
| SOC | ΔDFT+SOC ZORA | Tendances fiables | Vitesse ISC → PDT |
| E_ad | ΔUKS | ~0.1 eV | Potentiel PTT |
| f_S1 | TD-DFT | Exact | Proxy Φ_f → PTT |

---

## 📖 Références clés

- El-Sayed, *J. Chem. Phys.* 1963, 38, 2834 — règles d'El-Sayed
- Baig et al., *J. Comput. Chem.* 2025, 46, 7 — SOC pour I-BODIPY
- Ponte et al., *J. Mol. Model.* 2018, 24, 183 — SOC pour Br-BODIPY

---

*Suite → [`07_pourquoi_Delta_DFT.md`](07_pourquoi_Delta_DFT.md)*
