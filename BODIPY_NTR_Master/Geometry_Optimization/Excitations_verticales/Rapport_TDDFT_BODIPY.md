# Rapport d'Analyse TD-DFT — Caractérisation du Squelette BODIPY Nu

## 1. Configuration Méthodologique et Système

Le calcul porte sur le squelette BODIPY nu entouré de 3 molécules d'eau explicites (micro-solvatation), soit un total de **30 atomes**.

| Paramètre | Valeur |
|-----------|--------|
| Fonctionnelle | ωB97X-D3 (hybride à séparation de portée, correction de dispersion) |
| Base de calcul | def2-TZVP (Triple-Zeta avec polarisation) + approximation ZORA |
| Solvatation | CPCM/SMD paramétré pour l'eau |
| Fonctions de base | 605 |
| Accélération | RIJCOSX |

---

## 2. Propriétés Calculées — Résultats des Excitations Verticales

| Propriété | Valeur Calculée | Note |
|-----------|----------------|------|
| Énergie SCF totale | −911,62234 Eh | État fondamental S₀ en milieu aqueux |
| Moment dipolaire | 5,533 D | Polarité induite par les molécules d'eau |
| λ_max (état S₁) | 469,6 nm | Domaine bleu-cyan |
| Énergie S₁ (verticale) | 2,640 eV | Transition HOMO → LUMO |
| Force d'oscillateur (*f*_osc) | 0,533 | Transition permise et intense |
| Énergie T₁ (verticale) | 1,635 eV | Premier état triplet excité |
| Écart singulet-triplet (ΔE_ST) | 1,005 eV | Calculé : E(S₁) − E(T₁) |

---

## 3. Benchmarking — Précision et Corrélation Spectrale

### 3.1 Précision chimique (MAE)

La cible méthodologique est une erreur moyenne absolue (MAE) < 0,05 eV. La transition S₁ identifiée est quasi-purement HOMO → LUMO (contribution de **96,5 %**), ce qui limite les erreurs systématiques liées aux excitations de Rydberg ou de transfert de charge.

### 3.2 Corrélation spectrale (R²)

La valeur calculée de **469,6 nm** doit être rapprochée de la référence expérimentale du cœur BODIPY nu, généralement comprise entre **470 et 490 nm** selon le solvant (les BODIPY substitués affichent un redshift vers ~505 nm). La fonctionnelle ωB97X-D3 restitue correctement la physique de la molécule. Le décalage vers le proche infrarouge (NIR) ne peut être obtenu sans modification chimique du squelette.

---

## 4. Analyse de l'Écart Singulet-Triplet (ΔE_ST) et Potentiel PDT

L'écart énergétique entre S₁ et T₁ conditionne la capacité du photosensibilisateur à générer de l'oxygène singulet (¹O₂) via la transition inter-système (ISC).

$$\Delta E_{ST} = E(S_1) - E(T_1) = 2{,}640 - 1{,}635 = \mathbf{1{,}005 \ eV}$$

| Critère | Valeur |
|---------|--------|
| Seuil PDT "excellente" | < 0,05 eV |
| ΔE_ST calculé | 1,005 eV |
| Rapport (calculé / seuil) | ×20 |

**Conclusion :** Avec ΔE_ST = 1,005 eV, la transition inter-système est prédite lente. Le potentiel PDT du squelette BODIPY nu est faible.

---

## 5. Conclusion et Orientations

Le benchmarking du squelette BODIPY nu met en évidence deux limitations  majeures pour une application en thérapie combinée PDT/PTT contre le TNBC.

### 5.1 Limitation spectrale

L'absorption à **469,6 nm** est incompatible avec la fenêtre de pénétration tissulaire (NIR-I : 650–750 nm).

### 5.2 Limitation de l'ISC

Le ΔE_ST de **1,005 eV** dépasse d'un facteur 20 le seuil requis pour une PDT efficace (< 0,05 eV).

### 5.3 Étape suivante

L'introduction d'**atomes d'iode** sur le squelette BODIPY est la modification prioritaire à tester. L'effet d'atome lourd augmente le couplage spin-orbite, ce qui devrait :

1. Réduire significativement le ΔE_ST et accélérer l'ISC,
2. Provoquer un redshift de l'absorption vers le NIR.

---

