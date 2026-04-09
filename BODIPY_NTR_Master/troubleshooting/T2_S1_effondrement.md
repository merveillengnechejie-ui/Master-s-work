# Troubleshooting T2 — L'État S₁ s'Effondre vers S₀
## Le problème le plus difficile du projet

---

## Pourquoi ce problème existe

Quand on optimise la géométrie de S₁ avec ΔSCF, ORCA cherche le minimum d'énergie. Mais S₀ est plus stable que S₁ — si les orbitales "glissent" vers la configuration S₀, le calcul converge vers S₀ au lieu de S₁.

```
Énergie
  │
  │  S₁ ──●── (ce qu'on veut)
  │        \
  │         \  ← glissement variationnel
  │          \
  │  S₀ ─────●── (où ORCA converge à tort)
```

**Symptôme** : L'énergie finale de "S₁" est identique ou très proche de S₀.

---

## Diagnostic

```bash
# Comparer l'énergie finale avec S₀
grep "FINAL SINGLE POINT ENERGY" S0_opt.out
grep "FINAL SINGLE POINT ENERGY" S1_attempt.out

# Si les deux énergies sont identiques (±0.001 Eh) → effondrement confirmé

# Vérifier aussi les occupations orbitales
grep "ORBITAL ENERGIES" S1_attempt.out -A 30
# Les occupations HOMO/LUMO doivent être différentes de S₀
```

---

## Solution 1 : Générer un bon guess initial (HOMO→LUMO)

C'est l'étape la plus importante. Il faut forcer ORCA à démarrer avec les électrons dans la bonne configuration.

```bash
# Étape 1 : Calculer S₀ normalement → obtenir S0.gbw
orca S0_opt.inp > S0_opt.out

# Étape 2 : Utiliser le script gen_s1_guesses.sh
../../gen_s1_guesses.sh -t S1_template.inp \
                         -x S0_opt.xyz \
                         -g S0_opt.gbw \
                         -n 4
# Ce script génère 3 guesses : HOMO→LUMO, HOMO-1→LUMO, HOMO→LUMO+1
# et sélectionne celui qui converge à la plus basse énergie
```

---

## Solution 2 : Input S₁ avec guess explicite

```orca
# S1_BODIPY_attempt1.inp

! Opt UKS B3LYP D3BJ def2-SVP RIJCOSX TightSCF SlowConv
! CPCM(water)
%pal nprocs 4 end
%maxcore 7000
%cpcm
  SMD true
  SMDSolvent "water"
end
%scf
  HFTyp UKS
  SCF_ALGORITHM DIIS_TRAH
  TRAH_MaxDim 20
  MaxIter 500
  DampFac 0.7
  LevelShift 0.3
  ConvForce 1e-5
end
%geom
  MaxStep 0.1    # Pas géométrique réduit
  Trust 0.15
end
# Utiliser le gbw de S₀ comme point de départ
%moinp "S0_opt.gbw"
* xyz 0 1
[Coordonnées de S0_opt.xyz]
*
```

---

## Solution 3 : Escalade complète (checklist)

Essayer dans cet ordre :

```
Tentative 1 : DampFac 0.7 + LevelShift 0.3 + DIIS_TRAH
Tentative 2 : DampFac 0.8 + LevelShift 0.5 + MaxStep 0.1
Tentative 3 : Guess HOMO-1→LUMO (au lieu de HOMO→LUMO)
Tentative 4 : Guess HOMO→LUMO+1
Tentative 5 : Base def2-TZVP (plus flexible)
```

Utiliser le script automatisé :
```bash
../../run_troubleshoot_S1.sh -i S1_template.inp \
                              -x S0_opt.xyz \
                              -g S0_opt.gbw \
                              -n 4
```

---

## Plan B : Si S₁ échoue après 5 tentatives

**Activer le Plan B sans culpabilité** — c'est une décision scientifique valide.

```
Plan B :
  - Garder T₁ optimisé (robuste, converge bien)
  - Garder SOC calculé
  - Utiliser ΔE_ST vertical (TD-DFT) comme approximation
  - Mentionner explicitement dans le mémoire :
    "L'optimisation de S₁ par ΔSCF n'a pas convergé pour cette
     molécule après 5 tentatives. L'énergie adiabatique de S₁
     est estimée par TD-DFT vertical comme approximation."
```

**Ce que vous pouvez encore publier avec Plan B** :
- λ_max (TD-DFT) ✓
- ΔE_ST vertical (TD-DFT) ✓ (moins précis mais publiable)
- SOC ✓
- Activation NTR ON/OFF ✓
- Scoring PDT/PTT ✓ (avec ΔE_ST vertical)

---

## Pourquoi S₁ est difficile et T₁ est facile

```
T₁ (triplet) :
  Multiplicité 3 → ORCA utilise UKS avec 2 électrons non appariés
  → Configuration clairement différente de S₀
  → Pas de risque d'effondrement vers S₀
  → Converge généralement bien

S₁ (singulet excité) :
  Multiplicité 1 → même multiplicité que S₀ !
  → ORCA peut "glisser" vers S₀ sans s'en rendre compte
  → Nécessite un contrôle explicite des occupations orbitales
  → Difficile par nature
```

---

## Documentation de l'échec

Si S₁ échoue, documenter dans `JOURNAL_DE_BORD.md` :

```markdown
## Semaine X — Tentatives S₁ pour [molécule]

| Tentative | Paramètres | Résultat | Énergie finale |
|-----------|-----------|---------|----------------|
| 1 | DampFac 0.7, LevelShift 0.3 | Effondrement | = E(S₀) |
| 2 | DampFac 0.8, LevelShift 0.5 | Effondrement | = E(S₀) |
| 3 | Guess HOMO-1→LUMO | Oscillation | Non convergé |
| 4 | Guess HOMO→LUMO+1 | Effondrement | = E(S₀) |
| 5 | def2-TZVP | Effondrement | = E(S₀) |

**Décision** : Plan B activé. ΔE_ST estimé par TD-DFT vertical.
```
