# Protocole P8 — Test de Solvatation Explicite (Nitro-Quenching)
## Audit #10 — Validation de la sensibilité aux liaisons hydrogène

---

## Objectif

Valider l'impact de la micro-solvatation sur l'efficacité du quenching par le groupe nitro. Les modèles de solvant continu (SMD/CPCM) échouent souvent à capturer les interactions directionnelles par liaisons hydrogène qui stabilisent les états de transfert de charge (CT) dans la forme OFF.

---

## 1. Construction du Cluster Micro-solvaté

1.  Prendre la forme OFF (nitro-BODIPY).
2.  Placer **3 à 5 molécules d'eau** (H₂O) autour du groupe nitro, en ciblant les sites accepteurs de liaisons H (atomes d'oxygène du groupe NO₂).
3.  Utiliser xTB pour une pré-optimisation rapide du cluster :
    ```bash
    xtb nitro_bodipy_5h2o.xyz --opt tight --gfn 2 --alpb water
    ```
4.  Vérifier visuellement que les molécules d'eau sont bien liées au groupe nitro.

---

## 2. Calcul TD-DFT du Cluster

Lancer un calcul d'excitation verticale sur le cluster optimisé :

```orca
! RKS wB97X-D def2-SVP AutoAux RIJCOSX TightSCF
! CPCM(water)
%pal nprocs 8 end
%maxcore 4000
%cpcm
  SMD true
  SMDSolvent "water"
  StateSpecificSolvation true
end
%tddft
  n_roots 10
  DoNTOs true
end
* xyzfile 0 1 nitro_bodipy_5h2o_opt.xyz
```

---

## 3. Analyse Comparative

Comparer les résultats obtenus avec et sans molécules d'eau explicites :

| Propriété | Sans H₂O (Continu seul) | Avec H₂O (Cluster) | Δ (Différence) |
|-----------|-------------------------|--------------------|----------------|
| λ_max (nm) | | | |
| f_S1 | | | |
| D_CT (Å)* | | | |

*\* D_CT : Distance de transfert de charge (Audit #13) — à extraire avec Multiwfn si possible.*

**Verdict Scientifique** :
- Si **Δλ_max > 20 nm** ou **Δf_S1 > 0.1** : La micro-solvatation est critique. Inclure les clusters dans le manuscrit final.
- Si **Δ < seuil** : Le modèle continu est suffisant. Mentionner la validation par cluster en information supplémentaire (SI).

---

## 4. Livrable

- `results/explicit_solvation_test.md` — Rapport de comparaison et conclusion sur la sensibilité au solvant.
