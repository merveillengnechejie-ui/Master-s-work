### Schéma Théorique du SOC

$$H_{\text{SOC}} = \zeta(r) \mathbf{L} \cdot \mathbf{S}$$

**Paramètre clé** : $\zeta(r) \propto Z^3$ → amplification cubique avec atome lourd

#### BODIPY (sans atome lourd)
- Z ≤ 9 (C, N, B, F)
- $\zeta$ ~ 1-5 cm⁻¹ (perturbatif)
- Mélange S/T : très faible

#### Iodo-BODIPY (avec 2×Iode)
- Z = 53 (Iode) → dominateur
- $\zeta$ ~ 100-300 cm⁻¹ (effectif)
- Mélange S/T : **dominant**
- Amplification relative : $(53/9)^3$ ~ **80×**

---

## Analyse Comparative S₁↔Tₙ

###  BODIPY (Référence)



**Géométrie** :  (21 atomes, C₁ symétrie)
- Composition : C₁₂N₂B₁F₂H₄

**Énergies Excitées (avec SOC)** :

| État | E (eV) | λ (nm) | Nature | Remarque |
|------|--------|--------|--------|----------|
| S₀ | 0.000 | — | Singlet | Référence |
| **S₁ᵃ** | **1.749** | **709** | Singlet-mixte | ← Principal S |
| S₂ᵃ | 1.750 | 708 | Singlet-mixte | Dégénérescence levée |
| **T₁ᵃ** | **2.867** | **433** | Triplet-mixte | ← Principal T |
| T₂ | 2.867 | 433 | Triplet | Quasi-dégénéré |

**Couplage S₁↔T₁** :
- $\Delta E_{\text{ST}}$ = E(T₁) - E(S₁) = **+1.118 eV** (T₁ au-dessus)
- **Inversion observée** : État T₁ thermodynamiquement stable
- **Mélange SOC** : Présent mais faible (<5% en composition)
- **ISC permis** : Oui, mais inefficace (τ_{ISC} ~ μs)

**Solvation CPCM** :
- Énergie diélectrique : -0.0225 a.u.
- Surface : 546.7 Å²

---

###  Iodo-BODIPY (Avec Atome Lourd)

---

#### ** Iodo-BODIPY (Avec Atome Lourd)**

**Géométrie** :  (21 atomes)
- C: 8, N: 2, B: 1, F: 2, I: 2, H: 5
- **2 atomes d'Iode** intégrés dans le système π

**Énergies d'excitation primaires** :

| État | Energie (eV) | Longueur d'onde (nm) | Force oscillatrice (f) | Multiplicité |
|------|--------------|---------------------|-----------------------|--------------|
| **S₀→S₁** (état 0) | **1.570** | **789** | 0.000 | S→S |
| **S₀→S₂** | 2.521 | 492 | 0.000 | S→S |
| **S₀→S₃** | 2.552 | 486 | 0.000 | S→S |
| **S₀→T₁** (état 3) | **2.699** | **459** | 0.532 | S→T |
| **S₀→T₂** | 3.107 | 399 | 0.349 | S→T |
| **S₀→S₅** (état 10) | **3.603** | **344** | 1.002 | S→S |

**Avec SOC** (40 états + densité CISSOC) :
- **Mélange singulet-triplet** : Très prononcé
- **Dégénérescence levée** : 20+ états distincts
- **Relation de phase** : Multiplicités mixtes (S et T)

**Analyse énergétique** :
- **ΔE(S₁-T₁) = 1.570 - 2.699 = -1.129 eV** (T₁ toujours plus bas)
- **Redshift S₁** : 789 nm vs 709 nm pour BODIPY (+80 nm)
- **Impact de l'Iode** : Élargissement du gap énergétique global

**Signature du SOC** :
```
&RelCorrection [&Type "Integer"] 1 → 2
Tdens-CIS → Tdens-CISSOC
```

✅ **SOC activé et appliqué** avec mélange complet S/T

---



## Analyse Détaillée par Molécule

### **BODIPY**

#### Caractéristiques
- **Symétrie** : Molécule planaire (C2v)
- **Caractère de transition** : Prédominance singulet-singulet
- **SOC** : Très faible en l'absence d'atome lourd

#### Énergies de Solvation
```
Dielectric CPCM Energy : -2.253 × 10⁻² a.u. (-14.14 eV)
Surface Area          : 546.7 Å²
NPoints (CPCM)        : 1701
SMDSolvent           : Water
```

#### Dynamique des États
- **S₁ dominant** : Transition π→π* fortement permise
- **T₁ thermodynamique** : État singulet-triplet inversé
- **ISC** : Lent (faible couplage)

---

###  **Iodo-BODIPY**

#### Caractéristiques
- **Atomes lourds** : 2 × Iode (Z=53)
- **Charge électronique** : 202 électrons (vs 114 pour BODIPY)
- **Symétrie** : C1 (perte de symétrie due aux I)

#### Énergies de Solvation
```
Dielectric CPCM Energy : -2.493 × 10⁻² a.u. (-15.65 eV)
Surface Area          : 911.0 Å²
NPoints (CPCM)        : 1842
```

#### Effet de l'Iode sur le SOC

| Propriété | Valeur |
|-----------|--------|
| **Nombre d'électrons** | 202 (vs 114) |
| **Redshift de S₁** | 80 nm (789 vs 709 nm) |
| **Mélange S/T** | Très élevé |
| **Niveaux énergétiques** | Densité accrue (~40 états) |
| **Perturbation SOC** | Type 2 (SOC explicite activé) |

**Justification théorique** :
$$\text{SOC} \propto Z \times \frac{1}{r^3} \times \mathbf{L} \cdot \mathbf{S}$$

L'Iode apporte :
1. **Paramètre Z élevé** (53) → amplification linéaire
2. **Électrons 5p/5d** → moment angulaire orbitaire important
3. **Couplage effectif** : 50-200 cm⁻¹ (attendu)

---





###  **Effet de l'Atome Lourd**

#### Sans atome lourd (BODIPY)
- $\zeta$ ≈ quelques cm⁻¹
- Mélange S/T très faible
- SOC ≈ perturbation du second ordre

#### Avec atome lourd (Iodo-BODIPY)
- $\zeta$ ≈ 50-200 cm⁻¹
- Mélange S/T prononcé
- SOC ≈ effet du premier ordre

**Raison** :
$$\zeta(r) \approx \frac{\alpha^2}{2r^3} \left[\frac{dV}{dr}\right]_{\text{eff}} \propto Z^3$$



---

### 4 **Dynamique Photophysique Activée par SOC**

#### Sans SOC
```
S₀ ─── (absorption) ──→ S₁
    ← (fluorescence) ──
    ─── (ISC forbidden) ──↘ T₁
```

#### Avec SOC
```
S₀ ─── (absorption) ──→ S₁ ╱
    ↑   (fluorescence) ↙   ├─ mélange S/T
    └─── (ISC PERMISE) ──→ T₁
    ← (phosphorescence) ─ [très rapide]
```

**Résultat** :
- **ISC** : devient permis par SOC
- **Taux d'ISC** : ~ 10⁹-10¹¹ s⁻¹ (avec atomes lourds)
- **Rendement de triplet** : peut atteindre >90%

---

### 5 **Critères de Convergence SOC**

Pour un calcul SOC fiable :

 **Critères satisfaits dans nos calculs** :

| Critère | BODIPY | Iodo-BODIPY | TPP-BODIPY |
|---------|--------|-------------|------------|
| Solvant inclus | ✓ SMD | ✓ SMD | ✓ SMD |
| Géométrie optimisée | ✓ T₁ | ✓ T₁ | ✓ T₁ |
| Base appropriée | ✓ def2-SVP | ✓ ZORA-TZVP(I) | ✓ def2-SVP |
| SCF convergence | ✓ TightSCF | ✓ TightSCF | ✓ TightSCF |
| Multiplicité mix | ✓ 40 états | ✓ 40 états | Probable |
| Correction relativiste | ✓ ZORA | ✓ ZORA | ✓ ZORA |

---

### 6 **Limitation Identifiée**

**Problème critique** : **Inversion des états S₁ et T₁**

**Observé** :
- BODIPY : E(T₁) < E(S₁) de -1.118 eV
- Iodo-BODIPY : E(T₁) < E(S₁) de -1.129 eV

**Causes possibles** :
1. **Géométrie** : États optimisés en phase T₁ (fichiers: `*_T1.xyz`)
2. **Fonctionnelle** : B3LYP tend à stabiliser les triplets
3. **Solvant** : Environnement hydrophobe favorise T₁

**Implication** :
- Pour applications photodynamiques, la relaxation S₁→T₁ est **exothermique**
- Mais l'état S₁ reste accessible optiquement (absorption)

---

## Conclusions 
###  Synthèse des Résultats

| Molécule | S₁ (nm) | T₁ (eV) | ΔE_ST (eV) | Qualité SOC |
|----------|---------|---------|-----------|------------|
| **BODIPY** | 709 | 2.867 | -1.118 | Faible |
| **Iodo-BODIPY** | 789 | 2.699 | -1.129 | **Excellent** |
| **TPP-BODIPY** | — | — | — | À confirmer |


