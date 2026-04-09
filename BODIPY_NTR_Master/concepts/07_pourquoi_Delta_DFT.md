# Concept 7 — Pourquoi Δ-DFT plutôt que TD-DFT pour les BODIPY ?
## Le choix méthodologique le plus important du projet

---

## 1. Pourquoi TD-DFT échoue sur les BODIPY

Les BODIPY présentent un **caractère légèrement couche ouverte** (*mild open-shell character*). Leur état fondamental S₀ a une légère contribution biradicalaire : les deux électrons de la liaison π ne sont pas parfaitement appariés.

```
BODIPY S₀ (réalité) :
  ~95% ↑↓ (fermé)  +  ~5% ↑↑ (ouvert)
  
TD-DFT suppose :
  100% ↑↓ (fermé)  ← approximation incorrecte !
```

**Conséquence** : TD-DFT fait des erreurs systématiques sur les BODIPY.

---

## 2. Erreurs typiques de TD-DFT sur les BODIPY

| Propriété | TD-DFT | Expérience | Erreur |
|-----------|--------|------------|--------|
| E(S₁) | Surestimé | — | +0.2 à +0.4 eV |
| E(T₁) | Sous-estimé | — | −0.1 à −0.3 eV |
| **ΔE_ST** | **Surestimé** | — | **> 0.3 eV** |
| λ_max | Décalé vers le bleu | — | −20 à −50 nm |

**Exemple concret** :
```
Iodo-BODIPY expérimental : ΔE_ST ≈ 0.03 eV
TD-DFT prédit            : ΔE_ST ≈ 0.35 eV
Erreur                   : × 10 !
```

Cette erreur est catastrophique pour prédire l'efficacité PDT.

---

## 3. Pourquoi TD-DFT échoue : l'explication physique

TD-DFT calcule les états excités comme des **perturbations** de S₀. Si S₀ est mal décrit (caractère ouvert ignoré), les états excités héritent de cette erreur.

De plus, TD-DFT dans l'approximation adiabatique **ne peut pas décrire** :
- Les doubles excitations (importantes pour T₁ des BODIPY)
- La relaxation orbitale dans l'état excité
- Les états de transfert de charge à longue portée (sans fonctionnelle range-separated)

---

## 4. La solution : Δ-DFT (Delta-SCF)

L'idée de Δ-DFT est simple : **calculer chaque état comme un SCF séparé**.

```
TD-DFT :
  Calculer S₀ → perturber → obtenir S₁, T₁
  (les orbitales ne se relaxent pas)

Δ-DFT :
  Calculer S₀ avec ses propres orbitales
  Calculer T₁ avec SES propres orbitales (UKS, multiplicité 3)
  ΔE_ST = E(T₁) - E(S₀)
  (chaque état a ses orbitales optimisées)
```

**Avantage clé** : La **relaxation orbitale** est incluse. Les orbitales de T₁ sont différentes de celles de S₀, ce qui est physiquement correct.

---

## 5. Les variantes Δ-DFT

### ΔUKS (Unrestricted Kohn-Sham)
```
Multiplicité 3 (triplet) : deux électrons de spin α non appariés
Avantage : simple, robuste
Inconvénient : contamination de spin possible (⟨S²⟩ ≠ 2.0)
Vérifier : ⟨S²⟩ doit être entre 2.0 et 2.1 dans le .out
```

### ΔROKS (Restricted Open-shell Kohn-Sham)
```
Multiplicité 3 : orbitales doublement occupées + 2 orbitales simplement occupées
Avantage : pas de contamination de spin
Inconvénient : convergence parfois plus difficile
Recommandé pour : calculs ΔE_ST finaux (plus précis)
```

**Notre stratégie** :
- Optimisation T₁ : ΔUKS (plus robuste)
- Énergie ΔE_ST finale : ΔROKS (plus précis)

---

## 6. Précision comparée

| Méthode | MAE ΔE_ST | Coût | Recommandation |
|---------|-----------|------|----------------|
| TD-DFT/B3LYP | > 0.3 eV | Rapide | ❌ Insuffisant pour BODIPY |
| TD-DFT/ωB97X-D | ~0.15 eV | Modéré | ⚠️ Acceptable pour λ_max seulement |
| **ΔUKS/PBE0** | **~0.035 eV** | Modéré | ✅ Bon compromis |
| **ΔROKS/PBE0** | **< 0.05 eV** | Modéré | ✅ Notre choix pour ΔE_ST |
| SOS-CIS(D) | < 0.10 eV | Élevé | ✅ Validation (projet publication) |
| DLPNO-STEOM-CCSD | ~0.10 eV | Très élevé | ✅ Gold standard (projet publication) |

---

## 7. Pourquoi ADC(2) est exclu

ADC(2) est souvent présenté comme une alternative. Voici pourquoi nous ne l'utilisons pas :

| Raison | Détail |
|--------|--------|
| **Fermé-couche uniquement** | ADC(2) dans ORCA 6.1.1 ne supporte que les systèmes RHF → optimisation T₁ **impossible** |
| **Sous-estimation CT** | Sous-estime les états de transfert de charge de 0.3–0.5 eV |
| **Référence MP2 instable** | Si S₀ a un caractère biradicalaire, la référence MP2 diverge |
| **Géométries T₁ incorrectes** | Même quand les énergies semblent raisonnables, la topologie de la surface d'énergie potentielle peut être fausse |

---

## 8. Résumé : notre chaîne méthodologique

```
λ_max (criblage rapide)
  → sTDA-PBE0/def2-SVP  (Tier 1, ~10 min)

λ_max (benchmark)
  → TD-DFT × 6 fonctionnelles/def2-SVP + ptSS-PCM  (Tier 2, ~3 h)

ΔE_ST (précision chimique)
  → ΔROKS/PBE0/def2-SVP + ptSS-PCM  (Tier 2.5, ~4 h)

SOC
  → ΔDFT+SOC/PBE0/ZORA  (~1 h)
```

---

## 📖 Références clés

- Behn et al., *J. Chem. Theory Comput.* 2011, 7, 2485 — caractère ouvert BODIPY
- Alfè et al., *JCTC* 2015, 11, 1 — SOS-CIS(D) MAE < 0.1 eV pour BODIPY
- Alkhatib et al., *RSC Adv.* 2022, 12, 1704 — benchmark 36 fonctionnelles

---

*Suite → [`08_solvation_modeles.md`](08_solvation_modeles.md)*
