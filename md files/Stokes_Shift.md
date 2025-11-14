La méthode Stokes-shift relaxation utilisée pour estimer les propriétés des états excités relaxés, notamment le gap singulet-triplet (∆EST) corrigé par relaxation.

Voici un résumé du concept nécessaire pour réaliser la figure TikZ demandée :

- La relaxation est approximée par l'utilisation de l'énergie de relaxation de l'état triplet T1 comme un proxy pour la relaxation de l'état singulet S1.
- L'énergie de relaxation ΔErelax(T1) est la différence entre l'énergie verticale d'excitation S0→T1 (∆Ev(S0→T1)) et l'énergie de relaxation correspondante (∆Er(S0→T1)).
- L'énergie de relaxation de S1 est approximée ainsi : $$ E_r(S_1) \approx E_v(S_1) - S_{shift} $$ où $$ S_{shift} \approx \Delta E_{relax}(T_1) $$.
- Le gap singulet-triplet corrigé est donné par : $$ \Delta E_{ST,relaxed} \approx E_r(S_1) - E_r(T_1) $$.

----------------
Le concept de la méthode de relaxation du décalage de Stokes, est une heuristique qui permet d'estimer les propriétés des états excités relaxés, notamment l'écart d'énergie singulet-triplet relaxé ($\mathbf{\Delta E_{ST,relaxed}}$). Cette méthode s'appuie sur le fait que la relaxation de géométrie et/ou de solvant dans l'état excité ($S_1$) abaisse son énergie, conduisant au décalage de Stokes entre l'absorption verticale et l'émission verticale.

La figure TikZ ci-dessous représente ce processus, incluant les surfaces d'énergie potentielle (SEP) des états singulet et triplet ($S_0$, $S_1$, $T_1$) et utilise les labels anglais requis par les conventions des sources.

### TikZ Figure: Stokes-Shift Relaxation Method

```tikz
\documentclass[border=10pt]{standalone}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning}

\begin{document}
\begin{tikzpicture}[
    scale=1.4,
    every node/.style={scale=1.0},
    >=stealth
]

    % Color definitions
    \definecolor{groundColor}{RGB}{50,50,50}
    \definecolor{singletColor}{RGB}{200,50,50}
    \definecolor{tripletColor}{RGB}{50,100,180}
    \definecolor{relaxOrange}{RGB}{220,140,40}
    \definecolor{relaxPurple}{RGB}{140,70,170}
    \definecolor{shiftGreen}{RGB}{40,160,90}
    \definecolor{estimateBrown}{RGB}{120,100,80}

    % Parameters for parabolas
    \def\xmin{-1.5}
    \def\xmax{6.5}
    \def\parabWidth{0.20}

    % Nuclear coordinate positions
    \def\qS{0}
    \def\qT{3.5}
    \def\qSone{2.5}

    % Energy offsets
    \def\ESzero{0}
    \def\ETone{3.0}
    \def\ESone{5.2}

    % Helper function for parabola
    \newcommand{\parab}[3]{#3 + \parabWidth*(#1-#2)^2}

    % Draw S0 parabola
    \draw[line width=1.4pt, groundColor, domain=\xmin:\xmax, smooth, samples=80]
        plot (\x, {\parab{\x}{\qS}{\ESzero}});
    \node[right, font=\sffamily, groundColor] at (\xmax-1.5, \ESzero) {(Ground state) $S_0$ };

    % Draw T1 parabola
    \draw[line width=1.4pt, tripletColor, domain=\xmin:\xmax, smooth, samples=80]
        plot (\x, {\parab{\x}{\qT}{\ETone}});
    \node[right, font=\sffamily, tripletColor] at (\xmax+0.2, \ETone) {$T_1$};

    % Draw S1 parabola
    \draw[line width=1.4pt, singletColor, domain=\xmin:\xmax, smooth, samples=80]
        plot (\x, {\parab{\x}{\qSone}{\ESone}});
    \node[right, font=\sffamily, singletColor] at (\xmax+0.2, \ESone) {$S_1$};

    % Calculate key points
    \coordinate (S0) at (\qS, {\parab{\qS}{\qS}{\ESzero}});
    \coordinate (S1_vert) at (\qS, {\parab{\qS}{\qSone}{\ESone}});
    \coordinate (S1_relax) at (\qSone, {\parab{\qSone}{\qSone}{\ESone}});
    \coordinate (T1_vert) at (\qS, {\parab{\qS}{\qT}{\ETone}});
    \coordinate (T1_relax) at (\qT, {\parab{\qT}{\qT}{\ETone}});

    % Reference line at bottom
    \draw[line width=0.8pt, black!40] (\xmin, -0.4) -- (\xmax, -0.4);

    % Vertical dotted lines
    \draw[densely dotted, black!50, line width=1.0pt] (\qS, -0.4) -- (\qS, 7.0);
    \draw[densely dotted, black!50, line width=1.0pt] (\qT, -0.4) -- (\qT, 0.5);
    \draw[densely dotted, black!50, line width=1.0pt] (\qSone, -0.4) -- (\qSone, 0.5);

    % Geometry labels
    \node[below, font=\sffamily\small] at (\qS, -0.4) {$q_{S_0}$};
    \node[below, font=\sffamily\small] at (\qT, -0.4) {$q_{T_1}^{\text{opt}}$};
    \node[below, font=\sffamily\small] at (\qSone, -0.4) {$q_{S_1}^{\text{est}}$};

    % Mark points with circles
    \fill[groundColor] (S0) circle (2pt);
    \fill[singletColor] (S1_vert) circle (2pt);
    \fill[singletColor] (S1_relax) circle (2pt);
    \fill[tripletColor] (T1_vert) circle (2pt);
    \fill[tripletColor] (T1_relax) circle (2pt);

    % Horizontal dashed lines at key energy levels (for arrow positioning)
    \draw[singletColor, line width=1.0pt, densely dashed] ($(S1_vert)+(-0.75,0)$) -- ($(S1_vert)+(2,0)$);
    \draw[singletColor, line width=1.0pt, densely dashed] ($(S1_relax)+(-0.3,0)$) -- ($(S1_relax)+(2,0)$);
    \draw[tripletColor, line width=1.0pt, densely dashed] ($(T1_vert)+(-0.75,0)$) -- ($(T1_vert)+(0.8,0)$);
    \draw[tripletColor, line width=1.0pt, densely dashed] ($(T1_relax)+(-0.8,0)$) -- ($(T1_relax)+(1.0,0)$);

    % Energy labels (on the left, aligned with dashed lines)
    \node[left, font=\sffamily\footnotesize, singletColor] at ($(S1_vert)+(-0.7,0)$) {$E_v(S_1)$ (Vertical)};
    \node[left, font=\sffamily\footnotesize, singletColor, fill=white, fill opacity=0.95, text opacity=1] at ($(S1_relax)+(3.5,0)$) {$E_r(S_1)$ (Relaxed)};
    \node[left, font=\sffamily\footnotesize, tripletColor] at ($(T1_vert)+(-0.7,0)$) {$E_v(T_1)$ (Vertical)};
    \node[left, font=\sffamily\footnotesize, tripletColor] at ($(T1_relax)+(2.7,0)$) {$E_r(T_1)$ (Relaxed)};

    % Vertical excitation arrows (very slight separation)
    \draw[->, singletColor, line width=1.6pt]
        ($(S0)+(-0.05,0.08)$) -- ($(S1_vert)+(-0.05,-0.08)$)
        node[pos=0.65, left, font=\sffamily\small, text width=2.2cm, align=center, xshift=0.35cm, yshift=-1cm]
        {Excitation\\$S_0 \to S_1$\\(vertical)};

    \draw[->, tripletColor, line width=1.6pt]
        ($(S0)+(0.05,0.08)$) -- ($(T1_vert)+(0.05,-0.08)$)
        node[pos=0.35, right, font=\sffamily\small, text width=2.2cm, align=center, xshift=-0.35cm]
        {Excitation\\$S_0 \to T_1$\\(vertical)};

    % Relaxation arrows (curved, along the surface)
    \draw[->, relaxOrange, line width=1.5pt]
        ($(S1_vert)+(0.15,-0.05)$) to[out=-25, in=140]
        node[above right, pos=0.5, font=\sffamily\small, fill=white, inner sep=2pt, rounded corners=1pt, xshift=-0.5cm, fill opacity=0.9, text opacity=1,sloped]
        {Relaxation $S_1$}
        ($(S1_relax)+(-0.1,0.05)$);

    \draw[->, relaxPurple, line width=1.5pt]
        ($(T1_vert)+(0.15,-0.05)$) to[out=-20, in=130]
        node[above right, pos=0.4, font=\sffamily\small, fill=white, inner sep=2pt, rounded corners=1pt, xshift=-0.75cm, fill opacity=0.9, text opacity=1, sloped]
        {Relaxation $T_1$}
        ($(T1_relax)+(-0.15,0.05)$);

    % Stokes shift measurement (T1) - using dashed horizontal lines
    \draw[<->, shiftGreen, line width=1.4pt, densely dotted]
        ($(T1_vert)+(-0.6,0)$) -- ($(T1_relax)+(-0.6,0)$)
        node[midway, font=\sffamily\footnotesize, sloped, rounded corners=2pt, yshift=0.28cm,fill=white,]
        {$S_{\text{shift}} \approx \Delta E_{\text{relax}}(T_1)$};

    % Energy estimation for S1 - using dashed horizontal lines at different x
    \draw[->, estimateBrown, line width=1.4pt, densely dotted]
        ($(S1_vert)+(1.90,0)$) -- ($(S1_relax)+(1.90,0)$)
        node[midway, font=\sffamily\footnotesize, text width=3.45cm, sloped,
             fill=white, fill opacity=0.95, text opacity=1, inner sep=3pt, rounded corners=2pt, xshift=-0.25cm,  yshift=0.5cm]
        {Estimation relaxation effect\\$E_r(S_1) \approx E_v(S_1) - S_{\text{shift}}$};

    % Relaxed ST gap - between the two relaxed minima
    \draw[<->, black!70, line width=1.3pt, densely dotted]
        (S1_relax) -- (T1_relax)
        node[midway, font=\sffamily\footnotesize, text width=1.75cm, sloped, yshift=.4cm,
             fill=white, inner sep=2pt, rounded corners=2pt]
        {Relaxed gap\\$\Delta E_{\text{ST,relaxed}}$};

    % Axis labels
    \node[left, font=\sffamily] at (\xmin-0.2, 3.5) {Energy};
    \node[below, font=\sffamily] at (2.5, -0.9) {Nuclear coordinate $q$};

\end{tikzpicture}
\end{document}
```

Cette figure illustre le principe fondamental de la **correction par décalage de Stokes** (Stokes-shift correction) utilisée pour obtenir les énergies des états excités relaxés, en particulier l'écart singulet-triplet relaxé ($\mathbf{\Delta E_{ST,relaxed}}$).

1.  **Vertical excitation ($E_{abs}$):** Le système passe de l'état fondamental relaxé $S_0(Q_0)$ à l'état singulet excité vertical $S_1(Q_0)$ (flèche violette), conformément au principe de Franck-Condon. $E_{abs}$ est l'énergie d'absorption.
2.  **$S_1$ relaxation:** Dans l'état excité, le système se détend vers sa géométrie d'équilibre $Q_1$, stabilisant ainsi l'énergie de $S_1$ (flèche bleue pointillée). Cette relaxation mène à l'état **$S_1(Q_1)$ relaxé**.
3.  **Vertical emission ($E_{em}$):** L'émission se produit verticalement de $S_1(Q_1)$ vers $S_0(Q_1)$ (flèche sarcelle), résultant en l'énergie $E_{em}$.
4.  **Décalage de Stokes ($\Delta E_{Stokes}$):** La différence entre $E_{abs}$ et $E_{em}$ est le décalage de Stokes. L'ampleur de ce décalage est directement liée à la relaxation structurelle et/ou environnementale qui a eu lieu dans $S_1$.
5.  **$\Delta E_{ST,relaxed}$:** La méthode de relaxation du décalage de Stokes permet de calculer l'énergie de l'état relaxé $S_1(Q_1)$ et de l'état triplet $T_1(Q_1)$. La quantité **$\Delta E_{\text{ST,relaxed}}$** (barre orange) représente l'écart entre ces minima relaxés et est l'estimation pragmatique des propriétés des états excités relaxés fournie par cette heuristique. C'est cette valeur qui est rapportée dans le travail pour les systèmes TADF.
