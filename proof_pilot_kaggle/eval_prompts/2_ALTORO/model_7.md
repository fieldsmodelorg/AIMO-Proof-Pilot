# AIMO Proof Pilot — grading task

You are an **expert olympiad grader** for the AIMO Proof Pilot. Your job is to grade **one**
submission against the official markscheme and return a completed grading sheet as a LaTeX
(`.tex`) file.

- **Problem:** `2_ALTORO`
- **Submission:** `model_7`

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

This is the submission `model_7` for problem `2_ALTORO`, with line numbers
added for reference in your errors log.

```text
  1 | ================================================================================
  2 | PROBLEM
  3 | ================================================================================
  4 | Let ABC be a triangle with AB = 26, BC = 17, AC = 25. Let Omega and H be the
  5 | circumcircle and orthocentre. Let D, E, F be the feet of the altitudes from
  6 | A, B, C respectively (so D lies on BC, E on CA, F on AB). Let lines EF and BC
  7 | meet at X, and let line AX meet Omega again at Q (Q != A). The segment HQ meets
  8 | the circle DEF (the nine-point circle) at a point P. If PQ/PE = a/b in lowest
  9 | terms, find a + b.
 10 | 
 11 | ANSWER:  PQ/PE = 125/91, so a + b = 125 + 91 = 216.
 12 | 
 13 | ================================================================================
 14 | SET-UP: COORDINATES
 15 | ================================================================================
 16 | Place
 17 |         B = (0, 0),    C = (17, 0),    A = (10, 24).
 18 | 
 19 | Check of the side lengths:
 20 |         BC = 17,
 21 |         AB = sqrt(10^2 + 24^2) = sqrt(100 + 576) = sqrt(676) = 26,
 22 |         AC = sqrt((10-17)^2 + 24^2) = sqrt(49 + 576) = sqrt(625) = 25.
 23 | 
 24 | So this triangle is congruent to the given one, and all metric quantities
 25 | (lengths, ratios) computed below are the required ones.
 26 | 
 27 | --------------------------------------------------------------------------------
 28 | Orthocentre H.
 29 | --------------------------------------------------------------------------------
 30 | Since BC lies on the x-axis, the altitude from A is the vertical line x = 10.
 31 | The line AC has slope (0-24)/(17-10) = -24/7, so the altitude from B (through
 32 | the origin, perpendicular to AC) has slope 7/24, i.e. y = (7/24)x. At x = 10
 33 | this gives y = 70/24 = 35/12. Hence
 34 | 
 35 |         H = (10, 35/12).
 36 | 
 37 | (Consistency check with the altitude from C: line AB has slope 24/10 = 12/5,
 38 | so the altitude from C is 12x - 5y = 170 - ... ; explicitly 5x + 12y = 85,
 39 | which at x = 10 gives y = 35/12. Agreed.)
 40 | 
 41 | --------------------------------------------------------------------------------
 42 | Feet of the altitudes D, E, F.
 43 | --------------------------------------------------------------------------------
 44 | D = foot from A on BC = (10, 0).
 45 | 
 46 | E = foot from B on line AC. Line AC passes through A(10,24) with slope -24/7,
 47 | i.e. 24x + 7y = 408 (indeed 24*10 + 7*24 = 240 + 168 = 408). The foot of the
 48 | perpendicular from the origin to the line 24x + 7y = 408 is
 49 |         E = (408 / (24^2 + 7^2)) * (24, 7) = (408/625)(24, 7)
 50 |           = (9792/625, 2856/625).
 51 | 
 52 | F = foot from C on line AB. Line AB is 12x - 5y = 0. The foot from C = (17,0) is
 53 |         F = C - ((12*17 - 5*0)/(12^2 + 5^2)) (12, -5)
 54 |           = (17, 0) - (204/169)(12, -5)
 55 |           = (425/169, 1020/169).
 56 | 
 57 | --------------------------------------------------------------------------------
 58 | The circumcircle Omega.
 59 | --------------------------------------------------------------------------------
 60 | Write Omega: x^2 + y^2 + d x + e y + f = 0.
 61 |   Through B(0,0):  f = 0.
 62 |   Through C(17,0): 289 + 17 d = 0  => d = -17.
 63 |   Through A(10,24):100 + 576 - 170 + 24 e = 0 => 506 + 24 e = 0 => e = -253/12.
 64 | Hence
 65 |         Omega:  x^2 + y^2 - 17 x - (253/12) y = 0.            (1)
 66 | 
 67 | ================================================================================
 68 | STEP 1:  THE POINT X = EF n BC
 69 | ================================================================================
 70 | Lemma (harmonic conjugate). X is the harmonic conjugate of D with respect to
 71 | B and C; equivalently (B, C; D, X) = -1.
 72 | 
 73 | Proof. Because angle BEC = angle BFC = 90 degrees, the points B, C, E, F lie on
 74 | the circle omega with diameter BC. Consider this circle. Its chord BC and its
 75 | chord EF meet at X. Its chord BF (= line AB) and its chord CE (= line CA) meet
 76 | at A. Its chord BE and its chord CF meet at H (the two altitudes BE, CF cross at
 77 | the orthocentre). Thus, for the complete quadrilateral inscribed in omega with
 78 | vertices B, F, E, C, the three diagonal points are X (= BC n EF), A (= BF n CE)
 79 | and H (= BE n CF). Consequently the line AH is the polar of X with respect to
 80 | omega. The line AH is the A-altitude, which meets BC at D. Since X also lies on
 81 | BC, the polar of X meets BC at D, and therefore D and X are harmonic conjugates
 82 | with respect to the points B, C where BC cuts omega:  (B, C; D, X) = -1.    [].
 83 | 
 84 | Computation of X. On the x-axis use the coordinates B = 0, C = 17, D = 10.
 85 | With X = (x0, 0), the relation (B, C; D, X) = -1 reads
 86 |         (DB/DC) : (XB/XC) = -1,   i.e.   XB/XC = -(DB/DC).
 87 | Here DB = 10, DC = 7 (directed B->C), so XB/XC = -10/7, giving
 88 |         x0/(x0 - 17) = -10/7  =>  7 x0 = -10 x0 + 170  => 17 x0 = 170
 89 |         =>  x0 = 10 ... (that is D);
 90 | the harmonic conjugate is the OTHER solution of XB/XC = 10/7 taken externally:
 91 |         x0/(x0 - 17) = 10/7  =>  7 x0 = 10 x0 - 170  =>  3 x0 = 170,
 92 | so
 93 | 
 94 |         X = (170/3, 0).                                        (2)
 95 | 
 96 | (Direct check by intersecting line EF with y = 0 from the coordinates of E and F
 97 | gives the same value 170/3; this is carried out and confirmed.)
 98 | 
 99 | ================================================================================
100 | STEP 2:  THE POINT Q = (line AX) n Omega
101 | ================================================================================
102 | The direction of AX is X - A = (170/3 - 10, -24) = (140/3, -24), parallel to
103 | (35, -18). Parametrise the line AX by
104 |         (x, y) = (10 + 35 t, 24 - 18 t),     t in R,   t = 0 giving A.
105 | 
106 | Substitute into (1). Compute each piece:
107 |    x^2 + y^2 = (10+35t)^2 + (24-18t)^2
108 |              = (100 + 700t + 1225 t^2) + (576 - 864t + 324 t^2)
109 |              = 676 - 164 t + 1549 t^2,
110 |    -17 x     = -170 - 595 t,
111 |    -(253/12) y = -(253/12)(24 - 18 t) = -506 + (759/2) t.
112 | 
113 | Adding, the constant term is 676 - 170 - 506 = 0 (this just re-expresses that
114 | A lies on Omega), and the equation (1) becomes
115 |         1549 t^2 - (759/2) t = 0   =>   t ( 1549 t - 759/2 ) = 0.
116 | The root t = 0 is A; the second intersection corresponds to
117 |         t = 759 / (2 * 1549) = 759/3098.
118 | Therefore
119 |         Q_x = 10 + 35 * 759/3098 = (30980 + 26565)/3098 = 57545/3098,
120 |         Q_y = 24 - 18 * 759/3098 = (74352 - 13662)/3098 = 60690/3098 = 30345/1549,
121 | i.e.
122 | 
123 |         Q = (57545/3098, 30345/1549).                          (3)
124 | 
125 | (One checks directly that Q satisfies (1): substituting (3) into the left side
126 | of (1) yields exactly 0.)
127 | 
128 | ================================================================================
129 | STEP 3:  THE POINT P = HQ n (circle DEF)  IS THE MIDPOINT OF HQ
130 | ================================================================================
131 | The circle through D, E, F is the nine-point circle of triangle ABC. It is the
132 | image of the circumcircle Omega under the homothety h centred at the orthocentre
133 | H with ratio 1/2. (Standard fact: h maps the circumcentre O to the nine-point
134 | centre N = (O + H)/2, the midpoint of OH, and scales the radius by 1/2; under h
135 | each vertex of the triangle maps to the Euler point, and the whole circumcircle
136 | maps onto the nine-point circle, which passes through D, E, F.)
137 | 
138 | Since Q lies on Omega, its image
139 |         h(Q) = H + (1/2)(Q - H) = (H + Q)/2
140 | lies on the nine-point circle, i.e. on circle DEF. Moreover (H + Q)/2 is the
141 | midpoint of HQ, which lies in the interior of the segment HQ. The line HQ meets
142 | the circle DEF in at most two points; the midpoint is one of them and is the one
143 | lying on the segment HQ (the second intersection of line HQ with the circle is
144 | the point H + (1/2 - delta)... in fact it lies strictly outside the segment, as
145 | a direct solve of the quadratic confirms: parametrising HQ by H + u(Q - H), the
146 | two intersections occur at u = 1/2 and at a value u < 0). Hence the point P named
147 | in the problem is
148 | 
149 |         P = (H + Q)/2.                                          (4)
150 | 
151 | Using (3) and H = (10, 35/12):
152 |         P_x = (10 + 57545/3098)/2 = (88525/3098)/2 = 88525/6196,
153 |         P_y = (35/12 + 30345/1549)/2.
154 | For P_y put both terms over 18588 = 12*1549:
155 |         35/12 = 54215/18588,   30345/1549 = 364140/18588,
156 |         sum = 418355/18588,   half = 418355/37176.
157 | So
158 |         P = (88525/6196, 418355/37176).                        (5)
159 | 
160 | ================================================================================
161 | STEP 4:  THE LENGTHS PQ AND PE
162 | ================================================================================
163 | --------------------------------------------------------------------------------
164 | Length PQ.
165 | --------------------------------------------------------------------------------
166 | By (4), PQ = (1/2) HQ. Now
167 |         Q - H = (57545/3098 - 10,  30345/1549 - 35/12)
168 |               = (26565/3098,  309925/18588).
169 | Put both coordinates over the common denominator 18588 = 12*1549 (note
170 | 26565/3098 = 159390/18588):
171 |         Q - H = (1/18588) (159390, 309925).
172 | Hence
173 |         HQ^2 = (159390^2 + 309925^2) / 18588^2.
174 | 
175 | Numerator:  159390^2 + 309925^2 = 121,458,677,725.
176 | This factors as
177 |         121,458,677,725 = 1549 * 8855^2,           (8855^2 = 78,411,025),
178 | which one verifies by multiplication: 1549 * 78,411,025 = 121,458,677,725.
179 | Denominator:  18588^2 = 144 * 1549^2.
180 | Therefore
181 |         HQ^2 = (1549 * 8855^2) / (144 * 1549^2) = 8855^2 / (144 * 1549),
182 | and, since 144 * 1549 = (12)^2 * 1549,
183 |         HQ = 8855 / (12 * sqrt(1549)),
184 |         PQ = HQ/2 = 8855 / (24 * sqrt(1549)).                  (6)
185 | 
186 | --------------------------------------------------------------------------------
187 | Length PE.
188 | --------------------------------------------------------------------------------
189 | From (5) and E = (9792/625, 2856/625) put both points over the common
190 | denominator 23,235,000 = 625 * 37176 (here 37176 = 24*1549):
191 |         E   = (364,027,392 / 23235000,  106,174,656 / 23235000),
192 |         P   = (331,968,750 / 23235000,  261,471,875 / 23235000).
193 | Hence
194 |         E - P = ( 32,058,642 / 23235000,  -155,297,219 / 23235000),
195 |         PE^2  = (32,058,642^2 + 155,297,219^2) / 23,235,000^2.
196 | 
197 | Numerator:
198 |         32,058,642^2 + 155,297,219^2 = 25,144,982,756,018,125.
199 | This factors as
200 |         25,144,982,756,018,125 = 625 * 1549 * 161161^2,
201 |                                             (161161^2 = 25,972,867,921),
202 | verified by multiplication:
203 |         161161^2 = 25,972,867,921,
204 |         25,972,867,921 * 1549 = 40,231,972,409,629,
205 |         40,231,972,409,629 * 625 = 25,144,982,756,018,125.
206 | Denominator:
207 |         23,235,000^2 = (3 * 5 * 1549 * 1000)^2 = 2^6 * 3^2 * 5^8 * 1549^2.
208 | Therefore
209 |         PE^2 = (625 * 1549 * 161161^2) / (2^6 * 3^2 * 5^8 * 1549^2)
210 |              = 161161^2 / (2^6 * 3^2 * 5^4 * 1549)
211 |              = 161161^2 / (360000 * 1549),
212 | and, since 360000 = 600^2,
213 |         PE = 161161 / (600 * sqrt(1549)).                      (7)
214 | 
215 | ================================================================================
216 | STEP 5:  THE RATIO PQ/PE
217 | ================================================================================
218 | Dividing (6) by (7), the common factor sqrt(1549) cancels:
219 | 
220 |         PQ      8855 / 24            8855 * 600       8855 * 25
221 |        ---- = -------------- = ----------------- = ------------- .
222 |         PE     161161 / 600       24 * 161161         161161
223 | 
224 | Now use the prime factorisations
225 |         8855  = 5 * 7 * 11 * 23,        so 8855 * 25 = 5^3 * 7 * 11 * 23 = 221375,
226 |         161161 = 7^2 * 11 * 13 * 23.
227 | Their greatest common divisor is 7 * 11 * 23 = 1771, and
228 |         221375 / 1771 = 125,        161161 / 1771 = 91.
229 | Hence
230 | 
231 |         PQ/PE = 221375 / 161161 = 125 / 91.
232 | 
233 | Finally 125 = 5^3 and 91 = 7 * 13 share no common factor, so 125/91 is already
234 | in lowest terms. (Numerically 125/91 = 1.37362..., matching the direct numerical
235 | evaluation of PQ/PE.)
236 | 
237 | ================================================================================
238 | CONCLUSION
239 | ================================================================================
240 |         PQ / PE = 125 / 91,   with a = 125, b = 91 coprime.
241 | 
242 |         a + b = 125 + 91 = 216.
243 | 
244 | ================================================================================
245 | REMARK (a structural check)
246 | ================================================================================
247 | A coordinate-free reason why Q is special: by the power of the point X,
248 |         XA * XQ = XB * XC      (X, A, Q collinear on Omega; X, B, C collinear),
249 | and also XB * XC = XE * XF, the power of X with respect to the circle omega on
250 | diameter BC (which contains B, C, E, F). Hence XA * XQ = XE * XF, so A, E, F, Q
251 | are concyclic. But A, E, F, H already lie on the circle with diameter AH (since
252 | angle AEH = angle AFH = 90 degrees). Therefore Q lies on the circle with
253 | diameter AH, giving angle AQH = 90 degrees, i.e. HQ is perpendicular to AX.
254 | (This perpendicularity is confirmed by the direction vectors: HQ ~ (26565/3098,
255 | 309925/18588) is orthogonal to AX ~ (35, -18).) This is the geometric content
256 | behind the clean factorisations appearing above; it is not needed for the final
257 | arithmetic, which is established rigorously in Steps 1-5.
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
   - Fill in the header (Problem `2_ALTORO`, Submission `model_7`, your grader
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
   `grade_2_ALTORO_model_7_AI.tex`.
3. **Check it compiles.** Run `pdflatex -interaction=nonstopmode <file>.tex` and fix any
   errors so it builds to a PDF. (Keep the document self-contained — do not add external
   dependencies.)
4. **State the proposed mark** (0/1/6/7) clearly in your final message.

Do **not** commit anything to the repository — return the `.tex` (and its PDF if produced).
