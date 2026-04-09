# Projet Master 2 — Design In Silico de Photosensibilisateurs BODIPY-NTR
## Thérapie PDT/PTT Ciblée sur le Cancer du Sein Triple Négatif (TNBC)

**Auteure** : Corine Merveille KENGNE NGNECHEJIE  
**Formation** : Master 2 Physique Atomique, Moléculaire et Biophysique  
**Établissement** : Université de Yaoundé I, Cameroun  
**Durée** : 12 semaines | **Matériel** : 32 GB RAM, 4–8 cœurs  
**Logiciels** : ORCA 6.1.1 · xTB 6.6 · RDKit 2024 · Multiwfn 3.8+

---

## 🎯 Question scientifique centrale

> *Comment concevoir computationnellement des photosensibilisateurs BODIPY activés sélectivement par la nitroreductase (NTR) — une enzyme surexprimée dans les tumeurs hypoxiques — pour une thérapie combinée PDT/PTT contre le TNBC ?*

---

## 🗺️ Navigation rapide

### 📚 Comprendre les concepts (commencer ici)
| Fichier | Contenu |
|---------|---------|
| [`concepts/01_TNBC_et_hypoxie.md`](concepts/01_TNBC_et_hypoxie.md) | Pourquoi le TNBC ? Qu'est-ce que l'hypoxie tumorale ? |
| [`concepts/02_BODIPY_photophysique.md`](concepts/02_BODIPY_photophysique.md) | Structure BODIPY, propriétés optiques, règles de design |
| [`concepts/03_PDT_PTT_mecanismes.md`](concepts/03_PDT_PTT_mecanismes.md) | PDT vs PTT : mécanismes, différences, synergie |
| [`concepts/04_NTR_trigger_hypoxie.md`](concepts/04_NTR_trigger_hypoxie.md) | La nitroreductase comme interrupteur moléculaire |
| [`concepts/05_DFT_pour_debutants.md`](concepts/05_DFT_pour_debutants.md) | La DFT expliquée simplement : orbitales, fonctionnelles, bases |
| [`concepts/06_etats_excites_S1_T1.md`](concepts/06_etats_excites_S1_T1.md) | États singulet/triplet, ISC, SOC — le cœur de la PDT |
| [`concepts/07_pourquoi_Delta_DFT.md`](concepts/07_pourquoi_Delta_DFT.md) | Pourquoi Δ-DFT plutôt que TD-DFT pour les BODIPY ? |
| [`concepts/08_solvation_modeles.md`](concepts/08_solvation_modeles.md) | SMD, CPCM, ptSS-PCM : quel modèle choisir et pourquoi ? |

### 🔬 Protocoles de calcul
| Fichier | Contenu |
|---------|---------|
| [`protocols/P1_installation_verification.md`](protocols/P1_installation_verification.md) | Semaine 1 : installer et vérifier la chaîne de calcul |
| [`protocols/P2_construction_molecules.md`](protocols/P2_construction_molecules.md) | Construire les géométries de départ avec Avogadro/xTB |
| [`protocols/P3_optimisation_S0.md`](protocols/P3_optimisation_S0.md) | Optimisation de l'état fondamental S₀ |
| [`protocols/P4_benchmark_TDDFT.md`](protocols/P4_benchmark_TDDFT.md) | Benchmark TD-DFT : 6 fonctionnelles, comment choisir |
| [`protocols/P5_protocole_NTR_ON_OFF.md`](protocols/P5_protocole_NTR_ON_OFF.md) | Protocole dual-state : nitro (OFF) vs amine (ON) |
| [`protocols/P6_Delta_DFT_SOC.md`](protocols/P6_Delta_DFT_SOC.md) | Calculs Δ-DFT et couplage spin-orbite (SOC) |
| [`protocols/P7_scoring_PDT_PTT.md`](protocols/P7_scoring_PDT_PTT.md) | Scoring synergique PDT/PTT et grille Go/No-Go |

### 🛠️ Dépannage
| Fichier | Contenu |
|---------|---------|
| [`troubleshooting/T1_convergence_SCF.md`](troubleshooting/T1_convergence_SCF.md) | SCF ne converge pas : diagnostic et solutions |
| [`troubleshooting/T2_S1_effondrement.md`](troubleshooting/T2_S1_effondrement.md) | L'état S₁ s'effondre vers S₀ : que faire ? |
| [`troubleshooting/T3_erreurs_frequentes.md`](troubleshooting/T3_erreurs_frequentes.md) | Erreurs ORCA fréquentes et leurs corrections |

### 📊 Plan et résultats
| Fichier | Contenu |
|---------|---------|
| [`PLAN_12_SEMAINES.md`](PLAN_12_SEMAINES.md) | Planning détaillé semaine par semaine |
| [`JOURNAL_DE_BORD.md`](JOURNAL_DE_BORD.md) | Modèle de journal de bord à remplir chaque semaine |
| [`results/SYNTHESE_RESULTATS.md`](results/SYNTHESE_RESULTATS.md) | Tableau de synthèse des résultats (à remplir) |

---

## 🧪 Les 8 molécules du projet

```
Catégorie A — Référence
  1. BODIPY-Ph              → benchmarking expérimental (λ_max ~505 nm)

Catégorie B — Atome lourd
  4. Iodo-BODIPY            → SOC élevé, PDT de référence

Catégorie E — Trigger NTR (cœur du projet)
  2. BODIPY-Ph-NO₂          → forme OFF (prodrug, NTR inactif)
  3. BODIPY-Ph-NH₂          → forme ON (activée par NTR)
  5. Iodo-BODIPY-Ph-NO₂     → OFF : atome lourd + NTR
  6. Iodo-BODIPY-Ph-NH₂     → ON  : atome lourd + NTR activé

Catégorie B+E — Ciblage
  7. TPP-Iodo-BODIPY        → ciblage mitochondrial (TPP⁺)

Extension (si temps disponible)
  8. aza-BODIPY-NO₂         → NIR-I étendu + NTR
```

---

## 🔄 Cascade de calcul (Tiers 0 → 2.5)

```
Molécule .xyz
    │
    ▼ Tier 0 : GFN2-xTB (~2 min/mol)                    [Semaine 2]
    │  → Géométrie de départ, HOMO-LUMO gap, flexibilité
    │
    ▼ Tier 1 : sTDA-PBE0/def2-SVP (~10 min/mol)         [Semaine 3]
    │  → λ_max rapide, criblage, NTO
    │
    ▼ Tier 2 : TD-DFT × 6 fonctionnelles/def2-SVP       [Semaines 4–5]
    │  (~3 h/mol/fonctionnelle)
    │  → Benchmark vs expérience, sélection meilleure fonctionnelle
    │  → ptSS-PCM non-équilibre OBLIGATOIRE pour excitations
    │
    ▼ Tier 2.5 : Δ-DFT (ΔROKS/PBE0) + SOC (~5 h/mol)   [Semaines 6–7]
       → ΔE_ST précis (MAE < 0.05 eV vs > 0.3 eV pour TD-DFT)
       → Constantes SOC (cm⁻¹) via ZORA perturbatif
       → Classification PDT Type I / Type II
```

> **Pourquoi Tier 2.5 et pas Tier 3 ?** Ce tier est intercalé entre TD-DFT (Tier 2) et SOS-CIS(D) (Tier 3 du projet de publication). Il offre une précision chimique (MAE < 0.05 eV) à un coût modéré, sans nécessiter les méthodes de fonction d'onde coûteuses réservées à la publication.

---

## ⚠️ Avertissements importants

1. **Bug solvant** : Ne jamais utiliser `SMDSolvent "mixed"` dans ORCA 6.1.1 — ce mot-clé est invalide et tombe silencieusement en phase gaz. Toujours utiliser `SMDSolvent "water"`.

2. **Excitations verticales** : Toujours activer `StateSpecificSolvation true` dans `%cpcm` pour les calculs d'excitation (ptSS-PCM non-équilibre). Sans cela, les énergies d'excitation sont surestimées de 0.05–0.15 eV.

3. **ADC(2) exclu** : ADC(2) est fermé-couche uniquement dans ORCA 6.1.1 — l'optimisation T₁ est impossible. De plus, il sous-estime les états CT de 0.3–0.5 eV. Voir [`concepts/07_pourquoi_Delta_DFT.md`](concepts/07_pourquoi_Delta_DFT.md).

---

## 📈 Lien avec la publication scientifique

Ce projet Master constitue les **Tiers 0–2.5** du projet de publication complet décrit dans [`../Research_Paper_Roadmap_BODIPY_NTR.md`](../Research_Paper_Roadmap_BODIPY_NTR.md).

| Ce projet Master | Projet de publication |
|---|---|
| 8 molécules | 310 molécules |
| Tiers 0–2.5 | Tiers 0–8 (+ TSH-MD, SOS-CIS(D), STEOM-CCSD) |
| 12 semaines | 18–20 semaines |
| Mémoire M2 | Articles JCTC + JCIM |

Les résultats obtenus ici (benchmark TD-DFT, activation NTR ON/OFF, ΔE_ST, SOC) seront directement réutilisés et étendus dans le projet de publication.

---

*Dernière mise à jour : Avril 2026*
