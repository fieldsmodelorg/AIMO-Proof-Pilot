# AIMO Proof Pilot — grading task

You are an **expert olympiad grader** for the AIMO Proof Pilot. Your job is to grade **one**
submission against the official markscheme and return a completed grading sheet as a LaTeX
(`.tex`) file.

- **Problem:** `2_ALTORO`
- **Submission:** `team_1`

Grade the submission's argument **on its own merits against the markscheme** — *not* on how
closely it resembles the reference solution. Work carefully and verify every step against the
markscheme before deciding a mark.

## How to grade

**Scoring scale — 0 / 1 / 6 / 7, decided by two binary questions:**

1. **Is the solution essentially complete?** (allowing only minor slips described in the markscheme)
   - **No** → award **1** for *significant partial progress*, otherwise **0**.
   - **Yes** → award **7**, or **6** if there is a *minor error or omission*.

The bar for "essentially complete" is **stricter than the IMO**, and partial credit is
**harsher** (no 2–5 continuum). An *accumulation* of small omissions can amount to a material
hole, dropping an otherwise-complete solution into the 0/1 band.

**Use the markscheme's labelled points.** Each problem's markscheme lists:
- **ME** — minor errors/omissions that turn 7 → 6.
- **NME** — slips that should *not* be penalised.
- **NEC** — gaps that mean the solution is *not essentially complete* (cap at 0/1).
- **NPP** — things that are *not* enough, on their own, for the 1-mark partial-progress band.

When logging issues, map severity to these: **NME → trivial**, **ME → minor**, **NEC → major**.

**Alternative approaches.** Olympiad problems admit many valid routes. If the submission
differs from the reference solution, map its argument onto the **same milestones** in the
markscheme — an alternative that reaches the equivalent decisive step earns the equivalent
credit. Record your mapping and rationale in the "Significantly different approach?" box and
flag it.

**What counts as an error.** Flag not only false statements and logical gaps but also:
answering the **wrong problem**, **changing or weakening a hypothesis** from the one given,
proving a different statement, or assuming what was to be proved — these are usually **major**.
Reference the **line numbers** of the numbered submission below for every issue you log. If the
solution is entirely wrong (a clear 0), you need not catalogue every error — label the most
serious ones and note that minor errors were not itemised.

**Where to focus (in order):** (1) the **proposed mark + reasoning**, (2) the **errors/issues
log** with line numbers, (3) the two **proof-quality** questions (qualitative, lowest priority,
do **not** affect the mark).

---

## Problem and markscheme

The following is the problem statement, reference solution, and markscheme (LaTeX source from
the official document; some figures are omitted — that is fine).

```latex
\section*{Problem 2 (ALTORO)}


\problem[4]{%
Let $ABC$ be a triangle such that $AB = 26$, $BC = 17$, and $AC = 25$. Let $\Omega$ and $H$ be the circumcircle and orthocentre of triangle $ABC$, respectively. Let the feet of the altitudes from $A$, $B$, and $C$ in triangle $ABC$ be $D$, $E$, and $F$, respectively. Let lines $EF$ and $BC$ intersect at $X$ and let $AX$ intersect $\Omega$ again at $Q \neq A$. Segment $HQ$ intersects circle $DEF$ at a point $P$. Suppose the ratio $PQ/PE = a/b$ where $a$ and $b$ are coprime positive integers. What is the value of $a+b$?
}{216}

\vspace{2cm}

\textbf{Original AIMO3 Formulation:} 

Let $ABC$ be a triangle such that $AB = 26$, $BC = 17$, and $AC = 25$. Let $\Omega$ and $H$ be the circumcircle and orthocentre of triangle $ABC$, respectively. Let the feet of the altitudes from $A$, $B$, and $C$ in triangle $ABC$ be $D$, $E$, and $F$, respectively. Let lines $EF$ and $BC$ intersect at $X$ and let $AX$ intersect $\Omega$ again at $Q \neq A$. Segment $HQ$ intersects circle $DEF$ at a point $P$. Suppose the ratio $PQ/PE = a/b$ where $a$ and $b$ are coprime positive integers. What is the remainder when $ab$ is divided by $10^5$?

\textbf{Answer:} 11375

\vspace{1cm}

\textbf{Remark:} Relative to the AIMO3 version, we modified the final answer to ask for $a+b$ (rather than $ab$) to simplify the arithmetic.


\clearpage


\polishedsolution[SB][4]{%
Let $M$ be the midpoint of $BC$, and let $A'$ be the point diametrically opposite $A$ on circle $ABC$. Since $AB=26$ is the largest side and
\begin{equation*}
    26^2<25^2+17^2,
\end{equation*}
triangle $ABC$ is acute. In particular, its orthocentre $H$ lies inside triangle $ABC$.

\includegraphics[width=\textwidth]{../figures/fig_2.pdf}

\textbf{Claim 1:} $Q$, $H$, $M$, and $A'$ are collinear.

\begin{proof}
    Since $BH$ and $CA'$ are both perpendicular to $AC$, we have $BH \parallel CA'$. Similarly, $CH \parallel BA'$. Therefore $BHCA'$ is a parallelogram. Its diagonals $BC$ and $HA'$ bisect each other, so $A'$, $M$, and $H$ are collinear.

    Now $BFEC$ is cyclic with diameter $BC$. Hence, by power of a point at $X$ with respect to $\Omega$ and to circle $BFEC$,
    \begin{equation*}
        XQ \cdot XA = XC \cdot XB = XE \cdot XF.
    \end{equation*}
    By the converse of power of a point, $A,Q,E,F$ are cyclic.
    
    Also, $A,E,H,F$ are cyclic with diameter $AH$. Since the two circles through $A,E,F$ coincide, $A,Q,E,H,F$ are cyclic. Thus $\angle AQH=90^\circ$. On the other hand, $AA'$ is a diameter of $\Omega$, so $\angle AQA'=90^\circ$. Hence $QH$ and $QA'$ are the same line, and therefore $Q$, $H$, $M$, and $A'$ are collinear.
\end{proof}

\textbf{Claim 2 (\href{https://en.wikipedia.org/wiki/Nine-point_circle}{Nine-point Circle}):} The image of circle $DEF$ under the homothety with centre $H$ and scale factor $2$ is $\Omega$.

\begin{proof}
    Let $D'$ be the image of $D$ under this homothety. Since $H,D,A$ are collinear and $HD \perp BC$, the point $D'$ is the reflection of $H$ in the line $BC$. As $H$ lies inside triangle $ABC$ (since it is acute), we have

    Let $D'$ be the image of $D$ under this homothety. Since $H,D,A$ are collinear and $HD \perp BC$, the point $D'$ is the reflection of $H$ in the line $BC$. As $ABC$ is acute, $H$ lies on the same side of $BC$ as $A$, so $D'$ lies on the opposite side of $BC$ from $A$. We therefore have
    \begin{equation*}
        \angle BD'C = \angle BHC = 180^\circ-A,
    \end{equation*}
    Hence $\angle BD'C+\angle BAC=180^\circ$, and since $A$ and $D'$ are on opposite sides of $BC$, the points $A,B,C,D'$ are cyclic. Thus $D'$ lies on $\Omega$.

    Similarly, the images $E'$ and $F'$ of $E$ and $F$ lie on $\Omega$. The image of circle $DEF$ under the homothety is a circle through the three distinct points $D',E',F'$ on $\Omega$, so this image circle is exactly $\Omega$.
\end{proof}
Take $E'$ as defined in Claim 2, so $E'$ is the reflection of $H$ in $E$. Since $Q$ lies on $\Omega$, its preimage under the same homothety is the midpoint of $HQ$; this point lies on circle $DEF$. We now check that this is the required point $P$ on segment $HQ$.

By Claim 1, the line $HQ$ also contains $A'$, and the two intersections of this line with $\Omega$ are $Q$ and $A'$. Under the homothety, their preimages on circle $DEF$ are the midpoints of $HQ$ and $HA'$, respectively. But $M$ is the midpoint of $HA'$, since $BHCA'$ is a parallelogram. As $H$ lies inside $\Omega$, the points $Q$ and $A'$ lie on opposite rays from $H$, so $M$ is not on segment $HQ$. Therefore the intersection of segment $HQ$ with circle $DEF$ is the midpoint of $HQ$, namely $P$. Hence
\begin{equation*}
    HP=PQ=\frac{HQ}{2}.
\end{equation*}
The homothety also sends segment $PE$ to segment $QE'$, so $QE'=2PE$. Hence
\begin{equation*}
    \frac{PQ}{PE}=\frac{HQ/2}{QE'/2}=\frac{QH}{QE'}.
\end{equation*}

Since $B,E,H,E'$ are collinear and, by Claim 1, $Q,H,A'$ are collinear,
\begin{equation*}
    \angle E'HQ = \angle BHA'.
\end{equation*}
Moreover, $Q,E',A',B$ all lie on $\Omega$, so
\begin{equation*}
    \angle QE'H = \angle QE'B = \angle QA'B = \angle HA'B.
\end{equation*}
Thus $\triangle QHE' \sim \triangle BHA'$ and so
\begin{equation*}
    \frac{QH}{QE'}=\frac{BH}{BA'}.
\end{equation*}
It remains only to evaluate $BH/BA'$.

First, in triangle $ABA'$, the side $AA'$ is a diameter, so $\angle ABA'=90^\circ$. Also $\angle BA'A=\angle BCA=C$, since both angles subtend chord $BA$. Hence $\angle BAA'=90^\circ-C$, and the extended sine rule gives
\begin{equation*}
    BA'=2R \cdot \sin(90^\circ-C)=2R \cdot \cos C,
\end{equation*}
where $R$ is the circumradius of $ABC$.

Similarly, in the right-angled triangles $ADB$ and $BDH$, we have
\begin{equation*}
    BD=AB \cdot \cos B=2R \cdot \sin C\cos B
\end{equation*}
and, since $BH \perp AC$, we have $\angle DBH=90^\circ-C$. Therefore,
\begin{equation*}
    BH=\frac{BD}{\cos(90^\circ-C)}
       =\frac{2R\sin C\cos B}{\sin C}
       =2R\cos B.
\end{equation*}
Putting everything together,
\begin{equation*}
    \frac{PQ}{PE}=\frac{BH}{BA'}=\frac{2R\cos B}{2R\cos C}=\frac{\cos B}{\cos C}.
\end{equation*}

Now set $x=BC$, $y=AC$, $z=AB$. By the cosine rule,
\begin{equation*}
    \cos B=\frac{x^2+z^2-y^2}{2xz}
    \qquad\text{and}\qquad
    \cos C=\frac{x^2+y^2-z^2}{2xy}.
\end{equation*}
Therefore
\begin{equation*}
    \frac{PQ}{PE}
    =\frac{y(x^2+z^2-y^2)}{z(x^2+y^2-z^2)}.
\end{equation*}
Substituting $x=17$, $y=25$, and $z=26$ gives
\begin{equation*}
    \frac{PQ}{PE}
    =\frac{25(17^2+26^2-25^2)}{26(17^2+25^2-26^2)}
    =\frac{8500}{6188}
    =\frac{125}{91}.
\end{equation*}
Thus $a=125$ and $b=91$, so the required value is
\begin{equation*}
    a+b=\boxed{216}.
\end{equation*}
}

\clearpage

\markscheme{%
A solution is \emph{essentially complete} if it proves an expression for $PQ/PE$ involving only basic properties of the triangle. Specifically, it must prove that 
\begin{equation*}
    \frac{PQ}{PE}=\frac{
    S(R,x,y,z,\sin A,\sin B,\sin C,\cos A,\cos B,\cos C)
    }{
    T(R,x,y,z,\sin A,\sin B,\sin C,\cos A,\cos B,\cos C)
    }
\end{equation*}
where $S$ and $T$ are multivariate polynomials and the parameters are as defined in the solution above ($x=BC$, $y=AC$, and $z=AB$). For the avoidance of doubt, the expression \textbf{cannot} include other length terms or angles even if they can be shown to be equal to an expression involving terms above (e.g. $BA'$, $\sin{\angle CA'B}$). 

A coordinate, vector, or trigonometric solution can also be essentially complete. To qualify, it must compute the relevant constructed objects exactly, not just numerically (i.e. quantities must be expressed exactly rather than as decimal approximations), and it must identify the correct intersection point $P$ on segment $HQ$.

An essentially complete solution should receive $6$ rather than $7$ if it contains a minor error or omission: a gap that is not merely a small arithmetic slip, but which can be repaired without changing the main structure of the solution. Examples include:
\begin{enumerate}[label=(ME\arabic*)]
    \item Quoting one of the key geometric facts below without a sufficiently precise statement of what it says in this configuration (e.g. asserting Claim 2 without linking this to the nine-point circle configuration).
    \item Reaching a final expression such as $\cos B/\cos C$ but omitting the side-length substitution or final reduction to the required ratio.
\end{enumerate}

The following should \emph{not} generally be penalised:
\begin{enumerate}[label=(NME\arabic*)]
    \item A single routine arithmetic slip after a correct exact expression for the ratio has been obtained.
    \item Assuming the triangle is acute without proving this and/or using that the triangle is acute when chasing angles without explicitly stating this.
    \item Failing to rule out the possibility that segment $HQ$ intersects circle $DEF$ at two points. 
    \begin{itemize}
        \item We feel that this and the point above are both sufficiently obvious from drawing a diagram (particularly given the side lengths are fixed here) and would not usually be penalised in an Olympiad competition.
    \end{itemize}
\end{enumerate}

\clearpage

The following results may be quoted, provided they are stated precisely:
\begin{itemize}
    \item $A'$, $M$, and $H$ collinear.
    \item $DEFM$ is cyclic as this is the nine-point circle of triangle $ABC$.
    \item Claim 2, provided this is related to the nine-point circle.
    \item $Q$ lies on the line through $A'$, $M$, $H$---this must be related to $Q$ being the \href{https://web.evanchen.cc/handouts/GeoSlang/GeoSlang.pdf}{$A$-queue point} of triangle $ABC$.
\end{itemize}
}{%
Award $1$ mark to an incomplete solution if it proves that either
\begin{equation*}
    \frac{PQ}{PE}=\frac{QH}{QE'} \quad \text{or} \quad \frac{PQ}{PE}=\frac{BH}{BA'}
\end{equation*}
where in the first case, $E'$ is shown to be the second intersection of $BH$ with $\Omega$ other than $B$ (it may be initially defined differently). 

For clarity, none of the following on its own is enough for the partial-progress mark:
\begin{enumerate}[label=(NPP\arabic*)]
    \item Proving only Claim 1, namely $Q,H,A'$ collinear.
    \item Proving only Claim 2, namely the homothety/nine-point circle relation.
    \item Proving only preliminary cyclic facts such as $BFEC$ cyclic or $AEHF$ cyclic.
    \item Computing side-length data such as $R$, the area, $\cos B$, or $\cos C$ without connecting it to $PQ/PE$.
    \item Stating the final answer $216$, or the ratio $125/91$, without a derivation.
    \item Setting up coordinates or other computations without completing the proof.
\end{enumerate}

As is the case at the IMO, computational solutions (e.g. Cartesian coordinates) will not generally be awarded partial progress marks unless the intermediate results are interpreted synthetically (i.e. in terms of the points and length ratios in the diagram).  
}
```

---

## Submission to grade

This is the submission `team_1` for problem `2_ALTORO`, with line numbers
added for reference in your errors log.

```text
  1 | Let $ABC$ be a triangle with $AB = 26$, $BC = 17$, and $AC = 25$. We place $B$ at $(0,0)$, $C$ at $(17,0)$, and find $A$ at $(10,24)$ using coordinate geometry. The feet of the altitudes are $D(10,0)$ (from $A$), $E\left(\frac{9792}{625}, \frac{2856}{625}\right)$ (from $B$), and $F\left(\frac{425}{169}, \frac{1020}{169}\right)$ (from $C$).
  2 | 
  3 | Using Menelaus' theorem on $\triangle ABC$ with transversal $EFX$, we find $BX/XC = 170/119$, leading to $X = D(10,0)$. The line $AX$ (which is $AD$) intersects the circumcircle $\Omega$ again at $Q(10, -\frac{35}{12})$, the reflection of the orthocenter $H(10, \frac{35}{12})$ over $BC$.
  4 | 
  5 | The nine-point circle (circle $DEF$) has center at $\left(\frac{37}{4}, \frac{323}{48}\right)$ and radius $\frac{\sqrt{(3/4)^2 + (323/48)^2}}{2}$. The line $HQ$ (vertical line $x=10$) intersects this circle at $D(10,0)$ and $\left(10, \frac{323}{24}\right)$. Only $D$ lies on segment $HQ$, so $P = D$.
  6 | 
  7 | Calculating distances, $PQ = \frac{35}{12}$ and $PE = ED = \frac{182}{25}$. The ratio $\frac{PQ}{PE} = \frac{35/12}{182/25} = \frac{125}{312}$, where $125$ and $312$ are coprime. Thus, $a + b = 125 + 312 = 437$.
  8 | 
  9 | \boxed{437}
```

---

## The grading template to complete

Fill out a **copy** of the LaTeX grading sheet below. This is the exact template graders use.

```latex
% =====================================================================
%  AIMO Proof Pilot — Independent grading template
%
%  HOW TO USE THIS FILE
%  --------------------
%  1. COPY this file (do not edit it in place) and rename it, e.g.
%        grade_4_COLOUR_team_3_<your-initials>.tex
%  2. Fill in EVERY field marked  [ like this ]  (italic) below, and
%     delete the surrounding brackets.
%  3. Compile with pdflatex if you like, then EMAIL the .tex
%     to the organisers.
%  4. Do NOT commit your grade to the repository. Initial grading is
%     independent; the organisers collect the grades and upload them later.
%
%  Organisers note: when grades are reconciled, this single-grader page
%  is combined with the other graders' pages behind a front page that
%  records the final grading decision.
% =====================================================================
\documentclass[11pt]{article}
\usepackage[margin=2.2cm]{geometry}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{booktabs}
\usepackage{array}
\usepackage{enumitem}
\usepackage{longtable}
\usepackage[hidelinks]{hyperref}
\usepackage{parskip}

\newcommand{\field}[1]{\textbf{#1:}\hspace{0.5em}}
% Placeholder for text the grader replaces. Renders as italic in [brackets]
% so it displays cleanly and is easy to spot. Delete it once filled in.
\newcommand{\fillin}[1]{{\itshape[#1]}}

\begin{document}

% ----------------------------------------------------------------------
%  Header — identify the submission and grader
% ----------------------------------------------------------------------
{\centering\Large\bfseries AIMO Proof Pilot — Grading Sheet\par}
\vspace{1em}

\begin{tabular}{@{}p{0.5\textwidth}p{0.45\textwidth}@{}}
\field{Problem (\#\_ID)} \fillin{e.g. 4\_COLOUR}      & \field{Submission} \fillin{e.g. team\_3 / model\_2} \\[0.6em]
\field{Grader initials} \fillin{e.g. SB}             & \field{Date} \fillin{YYYY-MM-DD} \\
\end{tabular}

\vspace{0.4em}
\hrule
\vspace{0.8em}

% ----------------------------------------------------------------------
%  Reminder of the scoring scale
% ----------------------------------------------------------------------
\textbf{Scoring scale (0/1/6/7) — two binary decisions:}
\begin{enumerate}[label=\textbf{Step \arabic*.}, leftmargin=*, nosep]
    \item \textbf{Is the solution essentially complete?}
    \begin{itemize}[leftmargin=1.4em, nosep]
        \item If \textbf{no}: award \textbf{1} for significant partial progress, otherwise \textbf{0}.
        \item If \textbf{yes}: award \textbf{7}, or \textbf{6} if there is a minor error or omission.
    \end{itemize}
\end{enumerate}
Grade against the \textbf{markscheme} (\texttt{docs/markschemes.pdf}).

\vspace{0.8em}

% ----------------------------------------------------------------------
%  Proposed mark
% ----------------------------------------------------------------------
\section*{1. Proposed mark}

\textbf{Proposed mark} (choose one): \qquad \fbox{0} \qquad \fbox{1} \qquad \fbox{6} \qquad \fbox{7}

% ----------------------------------------------------------------------
%  Reasoning
% ----------------------------------------------------------------------
\section*{2. Reasoning}

Justify the mark with explicit reference to the markscheme points (e.g. \texttt{ME1}) where possible.

\bigskip
\fillin{Your reasoning here.}
\bigskip

\paragraph{Significantly different approach?}
If the solution is significantly different from the reference solution, map it onto the markscheme milestones as best you can, state your rationale here, and flag it for discussion.

\bigskip
\fillin{If applicable: how you matched the approach to the milestones, and your rationale. Otherwise write ``N/A''.}
\bigskip

\clearpage

% ----------------------------------------------------------------------
%  Errors / issues log
% ----------------------------------------------------------------------
\section*{3. Errors / issues}

List \textbf{every} error or issue you find, \emph{even minor ones}, with the corresponding line number(s) in the submission. The \emph{short summary} should be a brief phrase (we will later turn these into reusable codes); the \emph{detailed description} should give the full explanation. Mark each as:
\begin{itemize}
	\item \emph{Trivial} -- those listed under \texttt{NME} which we won't penalise;
	\item \emph{Minor} -- those listed under \texttt{ME} which could turn $7 \to 6$; or
	\item \emph{Major} -- those listed under \texttt{NEC} which would drop a solution to $0/1$
\end{itemize}
guided by the markscheme.

\paragraph{Exception for fundamentally wrong solutions.} If the solution is \emph{entirely} wrong (so the mark is clearly $0$), you do \textbf{not} need to rigorously catalogue every single error. Label the most serious ones --- enough to justify the mark --- and add a final row (or a note) recording that there were further minor errors which you have not itemised.

\paragraph{What counts as an error.} Flag as errors not only false statements and logical gaps, but also issues such as \textbf{answering the wrong problem}, \textbf{using a different set of conditions from those given in the problem} (e.g.\ silently changing or weakening a hypothesis), proving a different statement from the one asked, or assuming what was to be proved. Record these with an appropriate severity (usually \emph{major}).

\renewcommand{\arraystretch}{1.3}
\begin{longtable}{@{}p{1.6cm}p{3.2cm}p{8.0cm}p{1.7cm}@{}}
\toprule
\textbf{Line(s)} & \textbf{Short summary} & \textbf{Detailed description} & \textbf{Severity} \\
\midrule
\endhead
\fillin{e.g. 12--15} & \fillin{brief phrase} & \fillin{full explanation} & \fillin{trivial / minor / major} \\
\addlinespace
 & & & \\
\addlinespace
 & & & \\
\addlinespace
 & & & \\
\bottomrule
\end{longtable}

(Add rows as needed.)

\clearpage

% ----------------------------------------------------------------------
%  Proof quality (qualitative — does not affect the 0/1/6/7 mark)
% ----------------------------------------------------------------------
\section*{4. Proof quality (qualitative)}

These two questions capture \emph{stylistic} qualities of the write-up for our later analysis. They do \textbf{not} affect the 0/1/6/7 mark --- answer them independently of the score. Choose one option per question (the examples are there to keep graders consistent).

\subsection*{4a. Readability}
\textit{How much difficulty did you have following the proof? (Was it easy to read, or did you have to re-read passages to understand them?)}

\medskip
\textbf{Choose one:} \qquad \fbox{None} \qquad \fbox{A bit} \qquad \fbox{A lot}
\begin{itemize}[leftmargin=1.6em, nosep]
    \item \textbf{None} --- read smoothly in a single pass; steps, notation, and structure were clear throughout.
    \item \textbf{A bit} --- mostly clear, but a few passages needed re-reading (e.g.\ a terse step, ambiguous notation, or a slightly confusing ordering).
    \item \textbf{A lot} --- frequently hard to follow; had to re-read many parts, reconstruct missing links, or untangle a disorganised argument.
\end{itemize}

\medskip
\fillin{Optional: a sentence or two on the worst readability issues, with line numbers.}

\subsection*{4b. Conciseness}
\textit{How much unnecessary or inefficient content was there? (Were lemmas proved efficiently, or was there significant irrelevant / repetitive material?)} Judge \textbf{local} optimisations only --- e.g.\ a sub-argument proved more verbosely than needed, or repetition --- \emph{not} whether the overall approach takes a globally sub-optimal route.

\medskip
\textbf{Choose one:} \qquad \fbox{None} \qquad \fbox{A bit} \qquad \fbox{A lot}
\begin{itemize}[leftmargin=1.6em, nosep]
    \item \textbf{None} --- tight throughout; lemmas proved efficiently, with little or no wasted content.
    \item \textbf{A bit} --- some redundancy or slightly laboured steps, but nothing major (e.g.\ a lemma proved more verbosely than necessary, or a little repetition).
    \item \textbf{A lot} --- substantial irrelevant or repetitive content, or several sub-arguments proved far less efficiently than they could have been.
\end{itemize}

\medskip
\fillin{Optional: a sentence or two on the main conciseness issues, with line numbers.}

\end{document}

```

---

## What to produce

1. **Complete the grading sheet** above:
   - Fill in the header (Problem `2_ALTORO`, Submission `team_1`, your grader
     initials — use `AI` — and today's date).
   - **Section 1:** indicate the single proposed mark (0/1/6/7), e.g. by wrapping the chosen
     `\fbox{...}` in `\boxed`/highlight or removing the other three boxes — make the choice
     unambiguous.
   - **Section 2:** justify the mark with explicit reference to markscheme points (e.g. `ME1`,
     `NEC3`), and complete the "Significantly different approach?" box (or write `N/A`).
   - **Section 3:** log **every** error/issue in the table with line number(s), a short
     summary, a detailed description, and severity (trivial/minor/major).
   - **Section 4:** select one option for each of 4a (readability) and 4b (conciseness).
   - Replace every `\fillin{[...]}` placeholder and delete the brackets.
2. **Return the completed template as a single `.tex` file**, suggested filename
   `grade_2_ALTORO_team_1_AI.tex`.
3. **Check it compiles.** Run `pdflatex -interaction=nonstopmode <file>.tex` and fix any
   errors so it builds to a PDF. (Keep the document self-contained — do not add external
   dependencies.)
4. **State the proposed mark** (0/1/6/7) clearly in your final message.

Do **not** commit anything to the repository — return the `.tex` (and its PDF if produced).
