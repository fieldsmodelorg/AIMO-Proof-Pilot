# AIMO Proof Pilot — grading task

You are an **expert olympiad grader** for the AIMO Proof Pilot. Your job is to grade **one**
submission against the official markscheme and return a completed grading sheet as a LaTeX
(`.tex`) file.

- **Problem:** `6_AMAZIN`
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
\section*{Problem 6 (AMAZIN)}


\problem[7]{%
Let $ABC$ be an acute triangle with $\angle CBA=75^{\circ}$, orthocentre $H$, and circumcircle $\Omega$. Let line $AH$ meet $\Omega$ again at $H_A \neq A$. Similarly, let line $CH$ meet $\Omega$ again at $H_C$. Let the circle centred at $B$ with radius $BH$ meet the line $BC$ at $X$ on the opposite side of $B$ from $C$. Assume that lines $XH_A$ and $CH$ are not parallel, and let them intersect at $P$. Let lines $XH_C$ and $AH$ intersect at $Q$. 

Let $n$ be an odd positive integer. We call a triangle $ABC$ $n$-\textit{good} if $\frac{CP}{CH} = \sqrt{n}$ and the length $AQ$ is a positive integer. We say $n$ is \textit{amazing} if there exists an $n$-good triangle where the length $H_C Q$ is also a positive integer.

Let $1 \leq n_1<n_2<n_3<\cdots$ be a list of all amazing, odd positive integers.

Let $x$ be the largest real number for which there exists a positive real number $y$ such that for all sufficiently large $i$, $n_{2i} \geq y \cdot x^i$. For this choice of $x$, let $z$ be the largest real number such that for all sufficiently large $i$, $n_{2i} \geq z \cdot x^i$. 

It is possible to write $x+2016z=p+q\sqrt{r}$ where $p$, $q$, and $r$ are positive integers with $r$ square-free. What is $p+q+r$?
}{31070}

\vspace{1cm}

\textbf{Original AIMO3 Formulation:}

Let $ABC$ be an acute triangle with $\angle CBA=75^{\circ}$, orthocentre $H$, and circumcircle $\Omega$. Let $AH$ meet $BC$ at $D$ and $\Omega$ again at $H_A$. Similarly, let $CH$ meet $\Omega$ again at $H_C$. Let the circle centred at $B$ with radius $BH$ meet $BC$ at $X$ on the opposite side of $B$ as $C$. Let lines $XH_A$ and $CH$ intersect at $P$ and lines $XH_C$ and $AH$ intersect at $Q$. 

Let $n$ be an odd positive integer. We call a triangle $ABC$ $n$-\textit{good} if $\frac{CP}{CH} = \sqrt{n}$ and the length $AQ$ is a positive integer. We say $n$ is \textit{amazing} if there exists an $n$-good triangle where the length $H_C Q$ is also a positive integer.

Let $1 \leq n_1<n_2<n_3<\cdots$ be a list of all amazing, odd positive integers.

Let $x$ be the largest real number for which there exists a positive real number $y$ such that for all sufficiently large $i$, $n_{2i} \geq y \cdot x^i$. For this choice of $x$, let $z$ be the largest real number such that for all sufficiently large $i$, $n_{2i} \geq z \cdot x^i$. 

It is possible to write $x+2016z=p+q\sqrt{r}$ where $p$, $q$, and $r$ are positive integers with $r$ square-free. What is the remainder when $p+q+r$ is divided by $10^{5}$?

\textbf{Answer:} 31070

\vspace{1cm}

\textbf{Remark:} Relative to the AIMO3 version, we have made explicit the assumption that $XH_A$ and $CH$ are not parallel, so that the point $P$ is well defined. This does not affect the answer, since in the parallel case $P$ is undefined and the triangle is not $n$-good. We have also inserted the word `line' in a few places to avoid any misunderstandings that these referred to segments. The point $D$ was removed from the problem statement as it was not actually used. Finally, we removed the modulo $10^{5}$ answer modification since it did not actually have any effect on the final answer here. 

\clearpage

\polishedsolution[SB][7]{%
We use \href{https://web.evanchen.cc/handouts/Directed-Angles/Directed-Angles.pdf}{directed angles} modulo $180^\circ$. This is especially important here because there are two possible configurations, depending on the relative positions of $P$ and $Q$.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.8\textwidth]{../figures/fig_3.pdf}
    \caption{The \emph{inside} configuration}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.6\textwidth]{../figures/fig_4.pdf}
    \caption{The \emph{outside} configuration}
\end{figure}

\clearpage

We will determine exactly when each configuration occurs after proving the following geometric relation.

\textbf{Claim:} We have
\begin{equation*}
    \frac{CP}{CH}=\frac{AH}{AQ},
\end{equation*}
where the length ratios are \href{https://en.wikipedia.org/wiki/Line_segment\#Directed_line_segment}{directed}.

\begin{proof}
    Let $P'$ be the reflection of $P$ in $BC$. It's well-known that $H_A$ and $H_C$ are respectively the reflections of $H$ in $BC$ and $AB$, so
    \begin{equation*}
        CP=CP',\qquad AH=AH_C,
    \end{equation*}
    and also $P'\in CH_A$ and $PP'\parallel HH_A$.

    Also $BH=BX=BH_A=BH_C$, so $X,H_A,H,H_C$ are concyclic with centre $B$. Now
    \begin{equation*}
        \measuredangle HH_CA
        =\measuredangle CH_CA
        =\measuredangle CH_AH
        =\measuredangle CP'P.
    \end{equation*}
    Therefore the isosceles triangles $AHH_C$ and $PCP'$ are similar, with correspondence
    \begin{equation*}
        A\leftrightarrow C,\quad
        H\leftrightarrow P,\quad
        H_C\leftrightarrow P'.
    \end{equation*}

    It remains to identify the point on $CP$ corresponding to $Q\in AH$. Using the reflection in $BC$ and the circle through $X,H_A,H,H_C$, we get
    \begin{equation*}
        \measuredangle HP'P
        =\measuredangle P'PH_A
        =\measuredangle HH_AX
        =\measuredangle HH_CX
        =\measuredangle HH_CQ.
    \end{equation*}
    Thus, under the above similarity, the line $H_CQ$ corresponds to the line $P'H$. Hence $Q$ corresponds to $H$, since $Q$ lies on $AH$ and $H$ lies on $CP$. Therefore $AQ$ corresponds to $CH$, while $AH$ corresponds to $CP$, giving
    \begin{equation*}
       \frac{CP}{CH}=\frac{AH}{AQ},
    \end{equation*}
    as required.
\end{proof}
We next seek to understand what the possible values for $\frac{CP}{CH}$ are and when we get the inside versus outside configurations.

Set $\gamma=\angle ACB$. Since $\angle CBA=75^\circ$ and $ABC$ is acute, we have $15^\circ<\gamma<90^\circ$.


Choose Cartesian coordinates with $A=(0,0)$ and $AH$ on the positive $x$-axis. Since
\begin{equation*}
    \angle BAH=90^\circ-\angle CBA=15^\circ,
\end{equation*}
we may take $AB$ to make angle $-15^\circ$ with the $x$-axis. Let $D=(d,0)$ be where $AH$ intersects $BC$ and set
\begin{equation*}
    t=\tan15^\circ=2-\sqrt3.
\end{equation*}
Then
\begin{equation*}
    B=(d,-dt),\quad C=(d,d\cot\gamma),
\end{equation*}
and the orthocentre is
\begin{equation*}
    H=(h,0),\quad h=d(1-t\cot\gamma).
\end{equation*}
Moreover
\begin{equation*}
    BH=dt\csc\gamma,
    \quad
    X=(d,-dt(1+\csc\gamma)),
\end{equation*}
while the reflection of $H$ in $AB$ is
\begin{equation*}
    H_C=(h\cos30^\circ,-h\sin30^\circ).
\end{equation*}

Let $\lambda=\frac{AQ}{AH}$ be the directed ratio, positive on the ray $AH$ and negative on the opposite ray. Intersecting $XH_C$ with the $x$-axis gives
\begin{equation*}
    \lambda
    =\frac{t\sqrt3(\sin\gamma+1)-\sin\gamma}
    {2t(\sin\gamma+1)-\sin\gamma+t\cos\gamma}.
\end{equation*}
To see that $\lambda$ is strictly decreasing, set
\begin{equation*}
    s=\frac{1+\sin\gamma}{\cos\gamma}
      =\tan\left(45^\circ+\frac{\gamma}{2}\right).
\end{equation*}
As $\gamma$ increases from $15^\circ$ to $90^\circ$, the quantity
$45^\circ+\frac{\gamma}{2}$ increases from $52.5^\circ$ to $90^\circ$, so $s$ is strictly increasing. Using
\begin{equation*}
    \sin\gamma=\frac{s^2-1}{s^2+1},
    \qquad
    \cos\gamma=\frac{2s}{s^2+1},
    \qquad
    1+\sin\gamma=\frac{2s^2}{s^2+1},
\end{equation*}
and also
\begin{equation*}
    t\sqrt3=1-2t,
    \qquad
    t^2=4t-1,
\end{equation*}
the expression for $\lambda$ simplifies to
\begin{equation*}
\begin{aligned}
    \lambda
    &=\frac{t\sqrt3(1+\sin\gamma)-\sin\gamma}
    {2t(1+\sin\gamma)-\sin\gamma+t\cos\gamma}  \\
    &=\frac{1-t^2s^2}{1+2ts+t^2s^2}
     =\frac{1-ts}{1+ts}=-1+\frac{2}{1+ts}.
\end{aligned}
\end{equation*}
Since $s$ is strictly increasing and $t$ is fixed, this shows that $\lambda$ is a decreasing function of $\gamma$. The endpoint values are
\begin{equation*}
    \lim_{\gamma\downarrow15^\circ}\lambda
    =\frac{2}{1+\sqrt2+\sqrt3},
    \qquad
    \lambda(60^\circ)=0,
    \qquad
    \lim_{\gamma\uparrow90^\circ}\lambda=-1
\end{equation*}
and by continuity, $\lambda$ takes each value between these points as $\gamma$ varies.

By the Claim, using ordinary lengths in the definition of $n$-good,
\begin{equation*}
    \sqrt n=\frac{CP}{CH}=\frac{AH}{AQ}=\frac1{|\lambda|}.
\end{equation*}
Hence
\begin{equation*}
\begin{array}{ll}
15^\circ<\gamma<60^\circ:
& \text{inside configuration},\quad
  \displaystyle \frac{CP}{CH}\in\left(\frac{1+\sqrt2+\sqrt3}{2},\infty\right),\\[1.1em]
60^\circ<\gamma<90^\circ:
& \text{outside configuration},\quad
  \displaystyle \frac{CP}{CH}\in(1,\infty).
\end{array}
\end{equation*}
Since
\begin{equation*}
    \sqrt3<\frac{1+\sqrt2+\sqrt3}{2}<\sqrt5,
\end{equation*}
the first case can occur for odd $n$ exactly when $n\geq5$, while the second can occur for odd $n$ exactly when $n\geq3$.

Now suppose $ABC$ is $n$-good, and write $AQ=q$, where $q$ is a positive integer. The Claim gives
\begin{equation*}
    AH=q\sqrt n.
\end{equation*}
Also $AH_C=AH$, and, since $H_C$ is the reflection of $H$ in $AB$,
\begin{equation*}
    \angle H_CAH=2\angle BAH=30^\circ.
\end{equation*}
If $Q$ lies on the ray $AH$, the cosine rule in triangle $AH_CQ$ gives
\begin{equation*}
    H_CQ^2=q^2(n+1-\sqrt{3n}).
\end{equation*}
If $Q$ lies on the opposite ray, the angle at $A$ is $150^\circ$, and
\begin{equation*}
    H_CQ^2=q^2(n+1+\sqrt{3n}).
\end{equation*}
Thus $H_CQ$ can be integral only if $n+1\pm\sqrt{3n}$ is a rational square. Hence $\sqrt{3n}$ is rational, so, since $n$ is an integer, $3n$ is a square. Writing $3n=(3m)^2$, we get
\begin{equation*}
    n=3m^2,
\end{equation*}
where $m$ is an odd positive integer. Then $n+1\pm\sqrt{3n}=3m^2+1\pm3m$ is an integer; if it is a rational square, it must in fact be an integer square.

Conversely, if one of the corresponding integers below is a square, then the range analysis above lets us choose the required shape of triangle, and then scale it so that $AQ=1$. This gives an $n$-good triangle for which $H_CQ$ is an integer. Therefore the amazing integers are exactly those obtained from one of
\begin{equation*}
\begin{cases}
    u^2=3m^2-3m+1, & m\geq3\text{ odd},\quad\text{inside configuration},\\
    v^2=3m^2+3m+1, & m\geq1\text{ odd},\quad\text{outside configuration}.
\end{cases}
\end{equation*}
The first equation is equivalent to
\begin{equation*}
    (2u)^2-3(2m-1)^2=1,
\end{equation*}
with $2m-1\equiv1\pmod4$ and $2m-1\geq5$. The second equation is equivalent to
\begin{equation*}
    (2v)^2-3(2m+1)^2=1,
\end{equation*}
with $2m+1\equiv3\pmod4$ and $2m+1\geq3$.

Both are instances of the \href{https://en.wikipedia.org/wiki/Pell\%27s_equation}{Pell equation}
\begin{equation*}
    N^2-3M^2=1.
\end{equation*}
By standard theory of Pell's equation, since the fundamental solution is
$\left(N_0,M_0\right)=\left(2,1\right)$, all its positive solutions are given by
\begin{equation*}
    N_k+M_k\sqrt3=(2+\sqrt3)^{k+1},
    \qquad k\geq0.
\end{equation*}
Equivalently,
\begin{equation*}
    N_{k+1}=2N_k+3M_k,
    \qquad
    M_{k+1}=N_k+2M_k,
\end{equation*}
starting from $(N_0,M_0)=(2,1)$.

We only need solutions with $N$ even. Reducing the recurrence modulo $2$, we see that $N_k$ is even exactly when $k$ is even. Write
\begin{equation*}
    S_j=M_{2j}\qquad (j\geq0).
\end{equation*}
The two-step recurrence gives
\begin{equation*}
    M_{k+2}=4N_k+7M_k,
\end{equation*}
so
\begin{equation*}
    S_{j+1}\equiv -S_j\pmod4.
\end{equation*}
Since $S_0=1$, it follows that
\begin{equation*}
    S_j\equiv(-1)^j\pmod4.
\end{equation*}
Thus the inside solutions, for which $M=2m-1\equiv1\pmod4$, correspond to even $j$, while the outside solutions, for which $M=2m+1\equiv3\pmod4$, correspond to odd $j$. The only even-$j$ solution excluded by the condition $m\geq3$ is $j=0$, since $S_0=1=2m-1$ gives $m=1$.

Consequently, after removing this excluded case, the amazing integers occur in increasing order as
\begin{equation*}
    \sqrt{n_j/3}=\frac{S_j+(-1)^j}{2},
    \qquad j\geq1.
\end{equation*}
Indeed, the sequence $S_j$ is strictly increasing, so these values of $m$ are strictly increasing.

Define
\begin{equation*}
    \alpha=(2+\sqrt3)^2=7+4\sqrt3,
    \qquad
    \beta=(2-\sqrt3)^2=7-4\sqrt3=\alpha^{-1}.
\end{equation*}
Then $0<\beta<1$, and
\begin{equation*}
    S_j=M_{2j}
    =\frac{(2+\sqrt3)\alpha^j-(2-\sqrt3)\beta^j}{2\sqrt3}.
\end{equation*}
For the even-indexed amazing numbers,
\begin{equation*}
    n_{2i}=3\left(\frac{S_{2i}+1}{2}\right)^2.
\end{equation*}
Hence
\begin{equation*}
    \frac{n_{2i}}{\alpha^{4i}}
    =\frac34\left(\frac{S_{2i}+1}{\alpha^{2i}}\right)^2
    \xrightarrow{i\to\infty}
    \frac34\left(\frac{2+\sqrt3}{2\sqrt3}\right)^2
    =\frac{7+4\sqrt3}{16}
    =\frac{\alpha}{16}.
\end{equation*}
Moreover,
\begin{equation*}
    S_{2i}+1
    =\frac{2+\sqrt3}{2\sqrt3}\alpha^{2i}
    +1-\frac{2-\sqrt3}{2\sqrt3}\beta^{2i}
    >\frac{2+\sqrt3}{2\sqrt3}\alpha^{2i},
\end{equation*}
because $0<\frac{2-\sqrt3}{2\sqrt3}\beta^{2i}<1$. Therefore
\begin{equation*}
    n_{2i}>\frac{\alpha}{16}\alpha^{4i}
\end{equation*}
for all $i\geq1$. From the definitions of $x$ and $z$, we obtain
\begin{equation*}
    x=\alpha^4,
    \qquad
    z=\frac{\alpha}{16}.
\end{equation*}
Finally,
\begin{equation*}
\begin{aligned}
    x+2016z
    &=(7+4\sqrt3)^4+126(7+4\sqrt3)\\
    &=19699+11368\sqrt3.
\end{aligned}
\end{equation*}
Therefore
\begin{equation*}
    p+q+r=19699+11368+3=\boxed{31070}.
\end{equation*}
}

\clearpage

\markscheme{%
A solution is \emph{essentially complete} if, allowing only minor errors or omissions of the kind described below, it gives a coherent proof of all of the following:
\begin{enumerate}[label=(EC\arabic*)]
    \item A valid geometric reduction, including the directed-ratio relation
    \begin{equation*}
        \frac{CP}{CH}=\frac{AH}{AQ},
    \end{equation*}
    or an equivalent relation strong enough to connect the condition $\frac{CP}{CH}=\sqrt n$ with the position of $Q$ on the line $AH$.
    \item A correct analysis of the two configurations, including the possible ranges of $\frac{CP}{CH}$ in the inside and outside cases, or an equivalent existence argument that justifies exactly which odd values of $n$ can occur in each case.
    \item A correct integrality reduction showing that every amazing integer has the form $n=3m^2$ with $m$ odd, and that the remaining conditions are exactly
    \begin{equation*}
    \begin{cases}
        u^2=3m^2-3m+1, & m\geq3\text{ odd},\\
        v^2=3m^2+3m+1, & m\geq1\text{ odd}.
    \end{cases}
    \end{equation*}
    This should include the converse direction, for example by explaining that the triangle can be scaled so that $AQ=1$.
    \item A correct solution of the resulting Pell equation, with the parity and congruence restrictions handled correctly, leading to
    \begin{equation*}
        \sqrt{n_j/3}=\frac{S_j+(-1)^j}{2},
        \qquad j\geq1,
    \end{equation*}
    where $S_j=M_{2j}$ and $N_k^2-3M_k^2=1$.
    \item A correct asymptotic evaluation of the even-indexed amazing integers, giving
    \begin{equation*}
        x=(7+4\sqrt3)^4,
        \qquad
        z=\frac{7+4\sqrt3}{16},
    \end{equation*}
    and hence the final value $31070$.
\end{enumerate}

\clearpage

An essentially complete solution should receive $6$ rather than $7$ if it contains a minor error or omission: a gap that is not merely a small arithmetic slip, but which can be repaired without changing the main structure of the solution. Examples include:

\begin{enumerate}[label=(ME\arabic*)]
    \item Deriving the formula for $\lambda$ but giving an incomplete justification for the range of possible (signed) values it can take. For example, calculating the correct endpoint values, but giving an incorrect proof of monotonicity, such as saying only that the numerator and denominator are decreasing. 
    \item Failing to justify why different (integer) choices of $AQ$ do not lead to more possibilities for amazing $n$.
    \item Computing the limiting constant for $z$ correctly but omitting the short argument that the inequality needed in the definition of $z$ holds eventually, not just that $z$ is the limiting value.
\end{enumerate}

The following should \emph{not} generally be penalised:
\begin{enumerate}[label=(NME\arabic*)]
    \item Routine arithmetic or simplification slips that do not affect the final structural conclusions, such as a harmless intermediate trigonometric simplification that is corrected later.
    \item Invoking standard Pell equation theory without reproving it from first principles, provided the relevant parity, congruence, and indexing restrictions are dealt with correctly.
    \item Not separately proving that the listed amazing integers are already in increasing order, provided this is clear from the monotonicity of the Pell parameter used.
    \item A simple final addition slip in $19699+11368+3$, provided the values of $p$, $q$, and $r$ have been identified correctly.
\end{enumerate}

The following are \emph{not} essentially complete, even if they contain some substantial correct work:
\begin{enumerate}[label=(NEC\arabic*)]
    \item A solution that assumes one of the two configurations from the diagram and never treats the other one.
    \item A solution that fails to exclude $n=3$ (as this will throw off the indexing for the remainder of the proof and lead to an incorrect result since for odd indexes, no such $x$ and $z$ exist).
    \item A solution that states the relation $\frac{CP}{CH}=\frac{AH}{AQ}$ without proof or derives it only from a diagram-dependent, non-directed argument that fails in one configuration\footnote{Usually, diagram-dependence would not be penalised at the IMO; however, here having two configurations is integral to the problem so both must be dealt with.}.
    \item A solution that gives only necessary conditions for $n$ to be amazing, without justifying the converse.
    \item A solution that reduces to a Pell equation but applies the wrong parity or congruence class, thereby including the wrong Pell subsequence or missing every other amazing integer.
    \item A solution that obtains the correct Pell equations but does not determine the asymptotic behaviour of $n_{2i}$ and hence does not determine both $x$ and $z$.
    \item A solution that gives only a numerical guess for $x$, $z$, or the final answer, even if the guess is correct.
\end{enumerate}
\clearpage
}{%
Award $1$ mark to an incomplete solution if it contains one of the following pieces of significant, correct progress:
\begin{enumerate}[label=(PP\arabic*)]
    \item A valid proof of the core geometric relation
    \begin{equation*}
        \frac{CP}{CH}=\frac{AH}{AQ},
    \end{equation*}
    with directed lengths or with a separate argument that correctly handles both configurations.
    \item A correct reduction from the geometry and integrality conditions to the two equations
    \begin{equation*}
    \begin{cases}
        u^2=3m^2-3m+1,\\
        v^2=3m^2+3m+1,
    \end{cases}
    \end{equation*}
    including the fact that $n=3m^2$ with $m$ odd and the correct interpretation of the two signs.
\end{enumerate}

Do not award the partial-progress mark for any of the following on its own:
\begin{enumerate}[label=(NPP\arabic*)]
    \item Setting up coordinates for the geometry, or computing some of the points $B,C,H,X,H_C$, without reaching a substantive relation among $CP$, $CH$, $AH$, and $AQ$.
    \item Stating, guessing, or reading from the diagram that $\frac{CP}{CH}=\frac{AH}{AQ}$, without a valid proof.
    \item Deriving only that $n=3m^2$, without obtaining the two square conditions or an equivalent Pell reduction.
    \item Solving the generic Pell equation $N^2-3M^2=1$ without connecting the solutions to the correct parity and congruence classes required by the problem.
    \item Producing numerical examples of amazing integers, or correctly guessing the final answer, without a proof of the relevant structure.
    \item Calculating $x$ or $z$ from an asserted sequence of amazing integers, unless the asserted sequence has been justified by one of the substantial reductions above.
\end{enumerate}
}
```

---

## Submission to grade

This is the submission `model_7` for problem `6_AMAZIN`, with line numbers
added for reference in your errors log.

```text
  1 | ================================================================================
  2 |                          SOLUTION AND COMPLETE PROOF
  3 | ================================================================================
  4 | 
  5 | FINAL ANSWER:  p + q + r = 31070
  6 |    (with x + 2016 z = 19699 + 11368*sqrt(3), i.e. p=19699, q=11368, r=3.)
  7 | 
  8 | The solution has four parts.
  9 | 
 10 |    PART I.   Reduce the geometry to two scalar identities:
 11 |                  CP/CH  and  H_C Q / A Q.
 12 |    PART II.  Translate "n is amazing" into a number-theoretic condition.
 13 |    PART III. Solve the resulting Pell equation; describe the list (n_i).
 14 |    PART IV.  Carry out the asymptotic analysis and compute p+q+r.
 15 | 
 16 | Throughout, B = angle CBA = 75 degrees.  We write the triangle's angles as
 17 | A = angle BAC, B = 75, C = angle BCA, with A + B + C = 180, so A = 105 - C.
 18 | Acuteness (all angles < 90, with B = 75 < 90) is equivalent to
 19 | 
 20 |         15 < C < 90        (since A = 105 - C < 90  <=>  C > 15).            (1)
 21 | 
 22 | 
 23 | ================================================================================
 24 | PART I.  THE TWO GEOMETRIC IDENTITIES
 25 | ================================================================================
 26 | 
 27 | -------------------------------------------------------------------------------
 28 | I.1  Four points on one circle centred at B.
 29 | -------------------------------------------------------------------------------
 30 | Recall the classical fact: the reflection of the orthocentre H in a side of the
 31 | triangle lies on the circumcircle, and lies on the altitude through the opposite
 32 | vertex.  Hence:
 33 | 
 34 |   * The reflection of H in line BC lies on Omega and on the altitude AH; this is
 35 |     exactly the second intersection H_A of line AH with Omega.
 36 |   * The reflection of H in line AB lies on Omega and on the altitude CH; this is
 37 |     exactly the second intersection H_C of line CH with Omega.
 38 | 
 39 | Reflection in a line through B preserves distance to B, so
 40 | 
 41 |         B H_A = B H = B H_C .
 42 | 
 43 | By definition BX = BH as well.  Therefore the four points
 44 | 
 45 |         H ,  H_A ,  H_C ,  X
 46 | 
 47 | all lie on the circle  omega  centred at B with radius rho := BH.  Moreover
 48 | 
 49 |   * line AH is the chord  H H_A  of omega  (A, H, H_A are collinear),
 50 |   * line CH is the chord  H H_C  of omega  (C, H, H_C are collinear).
 51 | 
 52 | Thus P = (line X H_A) ∩ (line H H_C) and Q = (line X H_C) ∩ (line H H_A) are
 53 | intersections of chords/secants of the single circle omega.
 54 | 
 55 | -------------------------------------------------------------------------------
 56 | I.2  Coordinates.
 57 | -------------------------------------------------------------------------------
 58 | Place B = (0,0) with line BC along the positive x-axis, C on the positive
 59 | x-axis, and A in the upper half plane.  With AB = c, BC = a:
 60 | 
 61 |         C_vertex = (a, 0),     A_vertex = (c cos B, c sin B).
 62 | 
 63 | Altitude from A is the vertical line x = c cos B; altitude from C is
 64 | perpendicular to AB through C_vertex.  Solving, the orthocentre is
 65 | 
 66 |         H = ( c cos B ,  (a - c cos B) (cos B / sin B) ).
 67 | 
 68 | Using the Law of Sines a = 2R sin A, c = 2R sin C and
 69 | sin A - sin C cos B = sin(B+C) - sin C cos B = sin B cos C, one gets the clean form
 70 | 
 71 |         H = 2R cos B * ( sin C , cos C ).
 72 | 
 73 | In particular BH = 2R cos B =: rho.  Since all quantities CP/CH, H_C Q / AQ that we
 74 | need are scale-invariant ratios, we normalise rho = 1 (equivalently 2R cos B = 1);
 75 | absolute lengths are restored by an overall scaling at the very end.  With rho = 1:
 76 | 
 77 |         H    = ( sin C ,  cos C ),
 78 |         H_A  = ( sin C , -cos C )        (reflection of H in the x-axis = BC),
 79 |         X    = ( -1 , 0 )                (BX = 1, opposite side of B from C),
 80 |         A_vertex = ( sin C ,  sin C tan B ),
 81 |         C_vertex = ( sin A / cos B , 0 ),     A = 105 - C.
 82 | 
 83 | For H_C: reflection in line AB (the ray at angle B from the x-axis) sends the point
 84 | at angle (90 - C) [the angle of H] to angle 2B - (90 - C) = 2B - 90 + C.  With
 85 | B = 75 this is 60 + C, so
 86 | 
 87 |         H_C = ( cos(60 + C) ,  sin(60 + C) ).
 88 | 
 89 | Introduce the half-angle
 90 |         u = C/2,        u in (7.5 deg, 45 deg),   u != 30 deg,
 91 | the exclusion u = 30 (i.e. C = 60) being the degenerate case where X H_A || CH.
 92 | 
 93 | -------------------------------------------------------------------------------
 94 | I.3  The ratio CP/CH.
 95 | -------------------------------------------------------------------------------
 96 | A direct computation of P = (line X H_A) ∩ (line C_vertex H) gives, after
 97 | simplification,
 98 | 
 99 |         CP/CH = | sin(B + C) + cos B | / | sin(B - C) - cos B |.
100 | 
101 | Write cos B = sin(90 - B) and apply sum-to-product to numerator and denominator:
102 | 
103 |   sin(B+C) + sin(90 - B) = 2 sin(45 + C/2) cos(B + C/2 - 45),
104 |   sin(B-C) - sin(90 - B) = 2 cos(45 - C/2) sin(B - C/2 - 45).
105 | 
106 | Since sin(45 + C/2) = cos(45 - C/2), these factors cancel and (with B = 75):
107 | 
108 |         CP/CH = cos(30 + u) / | sin(30 - u) | .                              (2)
109 | 
110 | Setting w := tan u and dividing top and bottom by cos u,
111 | 
112 |         cos(30+u) = (sqrt3 cos u - sin u)/2,
113 |         sin(30-u) = (cos u - sqrt3 sin u)/2,
114 | 
115 | we obtain the convenient form
116 | 
117 |         sqrt(n) = CP/CH = | (sqrt3 - w) / (1 - sqrt3 w) | = | phi(w) |,       (3)
118 | 
119 | where phi(t) := (sqrt3 - t)/(1 - sqrt3 t).  Note phi is an involution: phi(phi(t)) = t.
120 | 
121 | Sign of phi(w):  for C < 60 (u < 30, w < tan30 = 1/sqrt3) both sqrt3 - w and
122 | 1 - sqrt3 w are positive, so phi(w) > 0; for C > 60 (u > 30) we get phi(w) < 0.
123 | 
124 | -------------------------------------------------------------------------------
125 | I.4  The ratio H_C Q / A Q.
126 | -------------------------------------------------------------------------------
127 | Q lies on the altitude AH, which is the vertical line x = sin(2u); thus
128 | A_vertex and Q have equal x-coordinate and
129 | 
130 |         AQ = | (A_vertex)_y - Q_y | .
131 | 
132 | Parametrise line X H_C by  X + t (H_C - X);  its x-coordinate is
133 | -1 + t (cos(60+C) + 1), so the value at x = sin C = sin 2u is
134 | 
135 |         t_Q = (sin 2u + 1) / (cos(60 + 2u) + 1).
136 | 
137 | Hence, using sin(60+2u)/(1 + cos(60+2u)) = tan(30 + u) (half-angle),
138 | 
139 |         Q_y = t_Q sin(60 + 2u) = (sin 2u + 1) tan(30 + u),
140 |         (A_vertex)_y = sin 2u tan 75.
141 | 
142 | Therefore
143 |         AQ = | sin 2u tan75 - (sin 2u + 1) tan(30 + u) |.                     (4)
144 | 
145 | For H_C Q, note H_C is the point t = 1 of the same parametrisation, so
146 | H_C Q = | t_Q - 1 | * | H_C - X |.  Now
147 |         | H_C - X | = sqrt( (cos(60+2u)+1)^2 + sin^2(60+2u) )
148 |                     = sqrt( 2 + 2 cos(60+2u) ) = 2 | cos(30 + u) |,
149 |         t_Q - 1 = ( sin 2u - cos(60+2u) ) / ( cos(60+2u) + 1 )
150 |                 = ( sin 2u - cos(60+2u) ) / ( 2 cos^2(30 + u) ),
151 | so
152 | 
153 |         H_C Q = | sin 2u - cos(60 + 2u) | / | cos(30 + u) |.                  (5)
154 | 
155 | Multiplying (4) by cos(30+u) (> 0 since 30+u in (37.5, 75)) and forming the ratio
156 | (the factor cos(30+u) cancels) gives
157 | 
158 |         H_C Q / A Q
159 |           = | sin 2u - cos(60+2u) |
160 |             / | sin 2u tan75 cos(30+u) - (sin2u + 1) sin(30+u) |.
161 | 
162 | Now pass to w = tan u using sin 2u = 2w/(1+w^2), cos 2u = (1-w^2)/(1+w^2), and
163 | sin u = w cos u, cos^2 u = 1/(1+w^2).  Elementary algebra (each step is a finite
164 | rational identity) yields
165 | 
166 |         sin 2u - cos(60+2u) = ( w^2 + (4 + 2 sqrt3) w - 1 ) / ( 2 (1 + w^2) )
167 |                             =: P(w) / ( 2 (1 + w^2) ),
168 | 
169 | and, writing  D(w) := 4(1 + sqrt3) w (1 - w) - (1 + sqrt3 w)(1 + w^2),
170 | 
171 |         sin2u tan75 cos(30+u) - (sin2u+1) sin(30+u)
172 |                             = ( 1 / ( 2 (1 + w^2) ) ) * sqrt(1+w^2) * D(w).
173 | 
174 | Hence
175 | 
176 |         H_C Q / A Q = | P(w) | * sqrt(1 + w^2) / | D(w) |.                    (6)
177 | 
178 | -------------------------------------------------------------------------------
179 | I.5  Simplification of (6) via the involution phi.
180 | -------------------------------------------------------------------------------
181 | Let m := phi(w) = (sqrt3 - w)/(1 - sqrt3 w); since phi is an involution we also have
182 | w = phi(m) = (sqrt3 - m)/(1 - sqrt3 m), and by (3)
183 | 
184 |         m = +sqrt(n)  on the branch C < 60,     m = -sqrt(n)  on the branch C > 60. (7)
185 | 
186 | Substituting w = (sqrt3 - m)/(1 - sqrt3 m) into P, D and 1+w^2 gives the
187 | polynomial identities (verified by direct expansion):
188 | 
189 |         P(w) * (1 - sqrt3 m)^2 =  4 K ,
190 |         D(w) * (1 - sqrt3 m)^3 = -8 K ,
191 |         (1 + w^2) * (1 - sqrt3 m)^2 = 4 ( m^2 - sqrt3 m + 1 ),
192 | 
193 |         where  K = (1 + sqrt3) m^2 - 2(2 + sqrt3) m + (2 + sqrt3).
194 | 
195 | The first two give  D(w) (1 - sqrt3 m) = -2 P(w),  i.e.  P(w)/D(w) = -(1 - sqrt3 m)/2.
196 | Plugging into (6):
197 | 
198 |         ( H_C Q / A Q )^2 = ( P/D )^2 (1 + w^2)
199 |                           = ( (1 - sqrt3 m)^2 / 4 ) * ( 4 (m^2 - sqrt3 m + 1) / (1 - sqrt3 m)^2 )
200 |                           = m^2 - sqrt3 m + 1.
201 | 
202 | Therefore, using (7),
203 | 
204 |   ******************************************************************************
205 |   *                                                                          *
206 |   *   H_C Q / A Q  =  sqrt( n + 1 - sqrt(3n) )    if  C < 60   (m = +sqrt n)  *
207 |   *   H_C Q / A Q  =  sqrt( n + 1 + sqrt(3n) )    if  C > 60   (m = -sqrt n)  *
208 |   *                                                                          *
209 |   *   and          CP / CH  =  sqrt n .                                       *
210 |   *                                                                          *
211 |   ******************************************************************************
212 | 
213 | (These were confirmed numerically against the raw coordinate construction, e.g.
214 | n=147 on the branch C>60 gives H_CQ/AQ = 13 exactly; n=33075 on C<60 gives 181.)
215 | 
216 | -------------------------------------------------------------------------------
217 | I.6  Which n are attainable by an acute triangle (range of each branch).
218 | -------------------------------------------------------------------------------
219 | By (2), n = (CP/CH)^2 = cos^2(30+u)/sin^2(30-u) is a continuous function of
220 | C in (15, 90).
221 | 
222 |   * Branch 2 (C in (60, 90), u in (30, 45)):  as C -> 60+, n -> +infinity;
223 |     as C -> 90-, n -> 1+.  Monotonic, so this branch realises every n in (1, +inf).
224 | 
225 |   * Branch 1 (C in (15, 60), u in (7.5, 30)):  as C -> 60-, n -> +infinity;
226 |     as C -> 15+ (the right-triangle limit A -> 90) n -> n_0 := cos^2(37.5)/sin^2(22.5)
227 |     = 4.2980...; monotonic, so this branch realises every n in (n_0, +inf).
228 | 
229 | In particular every integer n >= 2 is realised on branch 2, and every integer
230 | n >= 5 ( > n_0 ) is also realised on branch 1.  All such triangles are acute by (1).
231 | 
232 | 
233 | ================================================================================
234 | PART II.  TRANSLATING "AMAZING" INTO NUMBER THEORY
235 | ================================================================================
236 | 
237 | Fix an odd positive integer n.  For a triangle of a given shape, both AQ and
238 | H_C Q scale linearly with the overall size, while their ratio
239 | r := H_C Q / A Q is fixed.  Hence:
240 | 
241 |   * One can always rescale so that AQ is a positive integer; so an n-good
242 |     triangle (CP/CH = sqrt n and AQ a positive integer) exists whenever the
243 |     shape with CP/CH = sqrt n exists, i.e. for every n >= 2 by Part I.6.
244 | 
245 |   * Such a triangle can be rescaled so that BOTH AQ and H_C Q are positive
246 |     integers  <=>  r = H_C Q / A Q is a positive rational number.
247 |     (If r = h/a in lowest terms, scale so AQ = a, H_C Q = h; conversely two
248 |     integers force their ratio rational.)
249 | 
250 | Therefore:
251 | 
252 |    n is amazing  <=>  there is a valid (acute) branch giving CP/CH = sqrt n
253 |                       for which  r = H_C Q / A Q  is rational.
254 | 
255 | By Part I.5, r^2 = n + 1 -/+ sqrt(3n)  (minus on branch 1, plus on branch 2).
256 | For r to be rational we need r^2 rational, hence sqrt(3n) rational, hence
257 | 
258 |         3n is a perfect square   <=>   n = 3 j^2   for some positive integer j.
259 | 
260 | Then sqrt(3n) = 3 j and
261 | 
262 |         branch 1:  r^2 = 3 j^2 - 3 j + 1 ,
263 |         branch 2:  r^2 = 3 j^2 + 3 j + 1 .
264 | 
265 | Since n must be ODD and n = 3 j^2, we need j ODD.  Also r^2 is then a positive
266 | integer, and r rational forces r to be a positive integer.  Recalling the branch
267 | ranges (Part I.6): branch 2 is available for all j >= 1 (n = 3 j^2 >= 3 > 1),
268 | branch 1 only for n = 3 j^2 > n_0 = 4.298..., i.e. for odd j >= 3.
269 | 
270 |    ----------------------------------------------------------------------------
271 |    An odd n is amazing  <=>  n = 3 j^2 with j a positive odd integer, and
272 |         (a)  3 j^2 + 3 j + 1  is a perfect square           [branch 2, any j],
273 |               or
274 |         (b)  3 j^2 - 3 j + 1  is a perfect square AND j >= 3 [branch 1].
275 |    ----------------------------------------------------------------------------
276 | 
277 | (The case j = 1, n = 3, has only branch 2 available, and 3+3+1 = 7 is not a
278 | square, so n = 3 is NOT amazing.)
279 | 
280 | 
281 | ================================================================================
282 | PART III.  THE PELL EQUATION AND THE LIST OF AMAZING ODD n
283 | ================================================================================
284 | 
285 | Both conditions reduce to the Pell equation  X^2 - 3 Y^2 = 1:
286 | 
287 |    3 j^2 + 3 j + 1 = k^2  <=>  3(2j+1)^2 + 1 = (2k)^2  <=>  (2k)^2 - 3(2j+1)^2 = 1,
288 |    3 j^2 - 3 j + 1 = k^2  <=>  3(2j-1)^2 + 1 = (2k)^2  <=>  (2k)^2 - 3(2j-1)^2 = 1.
289 | 
290 | So in both cases we need X^2 - 3 Y^2 = 1 with X = 2k EVEN and Y = 2j +/- 1 ODD.
291 | 
292 | All solutions of X^2 - 3 Y^2 = 1 are X + Y sqrt3 = (2 + sqrt3)^t, t = 0,1,2,...:
293 |         t :  0    1    2     3      4       5        6
294 |        (X): 1    2    7    26     97     362     1351
295 |        (Y): 0    1    4    15     56     209     780  ...
296 | X is even exactly for ODD t, and for odd t the corresponding Y is odd.  The
297 | even-X solutions are therefore (X,Y) = (2,1), (26,15), (362,209), (5042,2911),
298 | (70226,40545), ...; list their Y-values as
299 | 
300 |         Y^(0)=1, Y^(1)=15, Y^(2)=209, Y^(3)=2911, Y^(4)=40545, Y^(5)=564719, ...
301 |         Y^(s+1) = 14 Y^(s) - Y^(s-1)     (the recurrence for stepping by (2+sqrt3)^2 = 7+4 sqrt3).
302 | 
303 | Reading off j:
304 | 
305 |    branch 2 ( Y = 2j+1, j = (Y-1)/2 ):  j = 0, 7, 104, 1455, 20272, 282359, ...
306 |    branch 1 ( Y = 2j-1, j = (Y+1)/2 ):  j = 1, 8, 105, 1456, 20273, 282360, ...
307 | 
308 | Keeping only ODD j with the required validity (branch 1 needs j >= 3, so j = 1 is
309 | dropped) and merging in increasing order gives precisely
310 | 
311 |         j  =  7,  105,  1455,  20273,  282359,  ...
312 | 
313 | (an independent brute-force search over all odd j confirms these are exactly the
314 | amazing odd j, with no others below 3,000,000).  In closed form, writing s = 1,2,3,...
315 | 
316 |         j_s = ( Y^(s) + (-1)^s ) / 2 ,     Y^(0)=1, Y^(1)=15, Y^(s+1)=14 Y^(s) - Y^(s-1),
317 | 
318 | so that branch 2 supplies the odd-s terms (j_1=7, j_3=1455, ...) and branch 1 the
319 | even-s terms (j_2=105, j_4=20273, ...).  The amazing odd integers, in increasing
320 | order, are
321 | 
322 |         n_s = 3 j_s^2 ,     s = 1, 2, 3, ... :
323 | 
324 |         n_1 = 147,
325 |         n_2 = 33075,
326 |         n_3 = 6351075,
327 |         n_4 = 1232983587,
328 |         n_5 = 239179814643,  ...
329 | 
330 | (For example j_1 = 7: 3*49 + 3*7 + 1 = 169 = 13^2, giving r = 13; j_2 = 105:
331 | 3*105^2 - 3*105 + 1 = 32761 = 181^2, giving r = 181.)
332 | 
333 | 
334 | ================================================================================
335 | PART IV.  ASYMPTOTICS:  COMPUTING x, z AND THE ANSWER
336 | ================================================================================
337 | 
338 | Put  alpha = 7 + 4 sqrt3,  beta = 7 - 4 sqrt3 = 1/alpha  (the roots of
339 | t^2 - 14t + 1).  Solving the recurrence for Y^(s) with Y^(0)=1, Y^(1)=15:
340 | 
341 |         Y^(s) = A alpha^s + B beta^s ,
342 |         A = 1/2 + sqrt3/3 ,   B = 1/2 - sqrt3/3 .
343 | 
344 | (Indeed A + B = 1 and A alpha + B beta = 7 + 4 sqrt3 (A - B) = 7 + 4 sqrt3 * (2 sqrt3 / 3)
345 | = 7 + 8 = 15.)
346 | 
347 | Since
348 |         n_s = 3 j_s^2 = (3/4) ( Y^(s) + (-1)^s )^2 ,
349 | 
350 | the EVEN-indexed subsequence ( s = 2i, so (-1)^s = +1 ) is
351 | 
352 |         n_{2i} = (3/4) ( Y^(2i) + 1 )^2
353 |                = (3/4) ( A alpha^{2i} + B beta^{2i} + 1 )^2 .
354 | 
355 | Dividing by (alpha^4)^i = alpha^{4i}:
356 | 
357 |         n_{2i} / (alpha^4)^i = (3/4) ( A + (B beta^{2i} + 1) alpha^{-2i} )^2 .   (8)
358 | 
359 | Because beta^{2i} -> 0 and alpha^{-2i} -> 0, the right side tends to (3/4) A^2.
360 | Moreover B beta^{2i} + 1 > 0 for all i (|B| < 1, 0 < beta < 1), so the bracketed
361 | correction term (B beta^{2i}+1) alpha^{-2i} is strictly positive and decreasing
362 | to 0; thus the sequence in (8) decreases strictly to its limit (3/4) A^2.
363 | 
364 | Determining x:
365 |    * If x < alpha^4, then n_{2i}/x^i -> +infinity, so a constant y > 0 exists.
366 |    * If x = alpha^4, then by (8) n_{2i}/x^i -> (3/4)A^2 > 0, again a valid y exists.
367 |    * If x > alpha^4, then n_{2i}/x^i -> 0, so NO positive y can work.
368 |    Hence the largest admissible value is
369 | 
370 |         x = alpha^4 = (7 + 4 sqrt3)^4 .
371 | 
372 | Determining z (for this x):  we need the largest z with n_{2i} >= z x^i for all
373 | large i, i.e. z = inf over large i of n_{2i}/x^i.  By (8) this sequence decreases
374 | strictly to (3/4) A^2, so it stays > (3/4)A^2 (the bound holds for all large i with
375 | z = (3/4)A^2), while any z' > (3/4)A^2 is eventually violated.  Hence
376 | 
377 |         z = (3/4) A^2 .
378 | 
379 | Now compute.  First
380 | 
381 |         (7 + 4 sqrt3)^2 = 49 + 48 + 56 sqrt3 = 97 + 56 sqrt3,
382 |         x = (97 + 56 sqrt3)^2 = 9409 + 9408 + 2*97*56 sqrt3 = 18817 + 10864 sqrt3.
383 | 
384 | Next, with A = 1/2 + sqrt3/3,
385 | 
386 |         A^2 = 1/4 + 2*(1/2)*(sqrt3/3) + 1/3 = 1/4 + 1/3 + sqrt3/3 = 7/12 + sqrt3/3,
387 |         z = (3/4) A^2 = 7/16 + sqrt3/4 .
388 | 
389 | Finally
390 | 
391 |         x + 2016 z = (18817 + 10864 sqrt3) + 2016 * ( 7/16 + sqrt3/4 )
392 |                    = 18817 + 10864 sqrt3 + 882 + 504 sqrt3
393 |                    = 19699 + 11368 sqrt3 .
394 | 
395 | This is of the form p + q sqrt(r) with
396 | 
397 |         p = 19699 ,   q = 11368 ,   r = 3   (square-free).
398 | 
399 | Therefore
400 | 
401 |         p + q + r = 19699 + 11368 + 3 = 31070 .
402 | 
403 | ================================================================================
404 |                               ANSWER:  31070
405 | ================================================================================
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
   - Fill in the header (Problem `6_AMAZIN`, Submission `model_7`, your grader
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
   `grade_6_AMAZIN_model_7_AI.tex`.
3. **Check it compiles.** Run `pdflatex -interaction=nonstopmode <file>.tex` and fix any
   errors so it builds to a PDF. (Keep the document self-contained — do not add external
   dependencies.)
4. **State the proposed mark** (0/1/6/7) clearly in your final message.

Do **not** commit anything to the repository — return the `.tex` (and its PDF if produced).
