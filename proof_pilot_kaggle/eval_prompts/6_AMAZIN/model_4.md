# AIMO Proof Pilot — grading task

You are an **expert olympiad grader** for the AIMO Proof Pilot. Your job is to grade **one**
submission against the official markscheme and return a completed grading sheet as a LaTeX
(`.tex`) file.

- **Problem:** `6_AMAZIN`
- **Submission:** `model_4`

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

This is the submission `model_4` for problem `6_AMAZIN`, with line numbers
added for reference in your errors log.

```text
  1 | **Solution**
  2 | 
  3 | --------------------------------------------------------------------
  4 | ### 1.  A convenient coordinate model  
  5 | 
  6 | Put  
  7 | 
  8 | \[
  9 | B=(0,0),\qquad C=(1,0),\qquad   
 10 | A=\bigl(a\cos75^{\circ},a\sin75^{\circ}\bigr),
 11 | \]
 12 | 
 13 | where \(a>0\).  
 14 | Denote  
 15 | 
 16 | \[
 17 | c=\cos75^{\circ}=\frac{\sqrt6-\sqrt2}{4},\qquad   
 18 | s=\sin75^{\circ}= \frac{\sqrt6+\sqrt2}{4}, \qquad   
 19 | k=\frac{c}{s}=2-\sqrt3 .
 20 | \]
 21 | 
 22 | The foot of the altitude from \(A\) on \(BC\) is \(D=(a c,0)\).
 23 | Set  
 24 | 
 25 | \[
 26 | d=ac\;(0< d <1),\qquad 
 27 | u:=\frac{d}{1-d}\;(>0).                          
 28 | \tag{1}
 29 | \]
 30 | 
 31 | From the elementary geometry of the orthocentre one obtains  
 32 | 
 33 | \[
 34 | H=(d,\,k(1-d)),\qquad 
 35 | R:=BH=\sqrt{d^{2}+k^{2}(1-d)^{2}}
 36 |       =\frac{\sqrt{u^{2}+k^{2}}}{1+u}.                                   \tag{2}
 37 | \]
 38 | 
 39 | Hence
 40 | 
 41 | \[
 42 | \frac{CP}{CH}= \frac{1+R}{\,1-2d-R\,}
 43 |                =\frac{1+u+\sqrt{u^{2}+k^{2}}}{1-u-\sqrt{u^{2}+k^{2}}}
 44 |                =: \mu .                                                       \tag{3}
 45 | \]
 46 | 
 47 | Writing \(\mu =\sqrt n\) ( \(n\) is an odd positive integer) we obtain from (3)
 48 | 
 49 | \[
 50 | \boxed{\displaystyle 
 51 | \mu =\frac{1+w}{1-w}\qquad\text{with}\qquad 
 52 | w:=\frac{\mu-1}{\mu+1}\in(0,1). }                                         \tag{4}
 53 | \]
 54 | 
 55 | Note that \(w=k\,y\) where \(y= \tan\theta+\sec\theta\) and
 56 | \(\theta\) is the acute angle with \(\tan\theta =ku\).
 57 | Consequently  
 58 | 
 59 | \[
 60 | k\,y=w .                                                                    \tag{5}
 61 | \]
 62 | 
 63 | --------------------------------------------------------------------
 64 | ### 2.  Lengths \(AQ\) and \(H_CQ\)
 65 | 
 66 | The point \(H_C\) is the second intersection of the line \(CH\) with the
 67 | circum‑circle; using (5) one finds
 68 | 
 69 | \[
 70 | H_C=\Bigl(\frac{k}{2}-\frac{d}{1+u},
 71 |           \;k\Bigl(1+\frac{d}{1+u}\Bigr)\Bigr) .
 72 | \tag{6}
 73 | \]
 74 | 
 75 | The point \(X\) is \((-R,0)\).  
 76 | A straightforward computation (the details are
 77 | routine but omitted) gives
 78 | 
 79 | \[
 80 | AQ=\frac{2(1-w)}{\sqrt3(1+w)}                        \tag{7}
 81 | \]
 82 | 
 83 | and
 84 | 
 85 | \[
 86 | H_CQ=
 87 | \frac{\sqrt{\,\bigl( (7+4\sqrt3)w^{2}-2w-1\bigr)^{2}
 88 |            +\bigl( (1+w)^{2}\bigr) ^{2}\,}}
 89 |         {2\sqrt3\,(1+w)} .                                          \tag{8}
 90 | \]
 91 | 
 92 | Both formulas contain only the single real parameter \(w\in(0,1)\).
 93 | 
 94 | --------------------------------------------------------------------
 95 | ### 3.  When is \(AQ/H_CQ\) rational ?
 96 | 
 97 | From (7)–(8)
 98 | 
 99 | \[
100 | \frac{AQ}{H_CQ}
101 |      =\frac{(1-w)^{2}}{(7+4\sqrt3)w^{2}-2w-1}\,
102 |         \frac{1}{\sqrt{1+ \bigl(\tfrac{1+w}{\, (7+4\sqrt3)^{\!1/2} w\,}\bigr)^{\!2}} } .
103 | \tag{9}
104 | \]
105 | 
106 | All quantities occurring in (9) belong to the quadratic field
107 | \(\mathbf Q(\sqrt3)\).  Write a generic element of this field as
108 | \(p+q\sqrt3\;(p,q\in\mathbf Q)\).
109 | A fraction of two such elements is rational **iff**
110 | the coefficients of \(\sqrt3\) are proportional; i.e. for
111 | \(\dfrac{p+q\sqrt3}{r+s\sqrt3}\) we must have \(ps=qr\).
112 | 
113 | Applying this criterion to (9) yields the elementary condition
114 | 
115 | \[
116 | \boxed{\displaystyle w = \bigl(2-\sqrt3\bigr)^{2k+1}\qquad(k=0,1,2,\dots) }.   \tag{10}
117 | \]
118 | 
119 | Thus the triangle required in the statement exists exactly for those
120 | \(w\) that satisfy (10).  
121 | 
122 | --------------------------------------------------------------------
123 | ### 4.  The amazing odd integers
124 | 
125 | From (4) and (10)
126 | 
127 | \[
128 | \mu=\frac{1+w}{1-w}
129 |       =\frac{(2+\sqrt3)^{\,2k+1}+1}{(2+\sqrt3)^{\,2k+1}-1}
130 |       =\frac{ \displaystyle
131 |                \bigl((2+\sqrt3)^{\,2k+1}+ (2-\sqrt3)^{\,2k+1}\bigr)}
132 |               {\displaystyle
133 |                \bigl((2+\sqrt3)^{\,2k+1}- (2-\sqrt3)^{\,2k+1}\bigr)} .
134 | \]
135 | 
136 | Hence  
137 | 
138 | \[
139 | \sqrt n =\mu 
140 |         =\frac{(2+\sqrt3)^{\,2k+1}- (2-\sqrt3)^{\,2k+1}}{2\sqrt3},
141 | \qquad 
142 | n=3\Bigl(\frac{(2+\sqrt3)^{\,2k+1}- (2-\sqrt3)^{\,2k+1}}
143 |                 {2\sqrt3}\Bigr)^{\!2}.                \tag{11}
144 | \]
145 | 
146 | All numbers given by (11) are odd (the inner bracket is an odd integer)
147 | and they are precisely the *amazing* integers.
148 | Writing  
149 | 
150 | \[
151 | u_k:=\frac{(2+\sqrt3)^{\,2k+1}- (2-\sqrt3)^{\,2k+1}}{2\sqrt3}
152 |      \;(k=0,1,2,\dots),
153 | \]
154 | 
155 | (11) becomes  \(n_k=3u_k^{2}\).
156 | The sequence \((u_k)\) satisfies  
157 | 
158 | \[
159 | u_{k+2}=4u_{k+1}-u_k ,\qquad   u_0=1,\;u_1=15,
160 | \]
161 | 
162 | hence  
163 | 
164 | \[
165 | n_{k+2}=14\,n_{k+1}-n_k ,\qquad n_0=3,\;n_1=675 .
166 | \tag{12}
167 | \]
168 | 
169 | --------------------------------------------------------------------
170 | ### 5.  Asymptotics of the even subsequence  
171 | 
172 | Let \(n_{1}<n_{2}<n_{3}<\dots\) be the increasing list of all amazing
173 | integers.
174 | From (12) the even indexed terms satisfy  
175 | 
176 | \[
177 | n_{2i}= \frac{7-4\sqrt3}{4}\,
178 |         \bigl(7+4\sqrt3\bigr)^{\,4i}+o\!\bigl((7+4\sqrt3)^{\,4i}\bigr) .
179 | \tag{13}
180 | \]
181 | 
182 | Therefore
183 | 
184 | \[
185 | \lim_{i\to\infty}\bigl(n_{2i}\bigr)^{1/i}= (7+4\sqrt3)^{4}
186 |      =:x .                                                                \tag{14}
187 | \]
188 | 
189 | Consequently  
190 | 
191 | \[
192 | x= (7+4\sqrt3)^{4}=18817+10864\sqrt3 .
193 | \tag{15}
194 | \]
195 | 
196 | Moreover, from (13)
197 | 
198 | \[
199 | \lim_{i\to\infty}\frac{n_{2i}}{x^{\,i}}
200 |      =\frac{7-4\sqrt3}{4}=:z .                                            \tag{16}
201 | \]
202 | 
203 | Both limits exist, so the numbers \(x\) and \(z\) are exactly those
204 | required in the statement.
205 | 
206 | --------------------------------------------------------------------
207 | ### 6.  The required sum  
208 | 
209 | From (15)–(16)
210 | 
211 | \[
212 | \begin{aligned}
213 | x+2016z&=
214 | \bigl(18817+10864\sqrt3\bigr)
215 |       +2016\Bigl(\frac{7-4\sqrt3}{4}\Bigr)  \\[2mm]
216 | &= \bigl(18817+3528\bigr)
217 |    +\bigl(10864-2016\bigr)\sqrt3      \\[2mm]
218 | &= 22345+8848\sqrt3 .
219 | \end{aligned}
220 | \]
221 | 
222 | Thus \(x+2016z=p+q\sqrt r\) with  
223 | 
224 | \[
225 | p=22345,\qquad q=8848,\qquad r=3 .
226 | \]
227 | 
228 | Finally  
229 | 
230 | \[
231 | p+q+r = 22345+8848+3 = \boxed{31196}.
232 | \]
233 | 
234 | --------------------------------------------------------------------
235 | **Explanation of the main steps**
236 | 
237 | * The geometry of the orthocentre and the reflections gives the simple
238 |   formula (3) for \(\displaystyle\frac{CP}{CH}\).
239 | * Introducing the auxiliary variable \(w\) by (4) linearises all further
240 |   calculations; after eliminating the auxiliary point \(Q\) the two
241 |   required lengths become the rational functions (7) and (8) of \(w\).
242 | * The condition that the ratio \(AQ/H_CQ\) be rational is equivalent,
243 |   after clearing the quadratic‑field denominator, to a single
244 |   linear relation between the coefficients of \(\sqrt3\);
245 |   solving it yields the powers of the fundamental unit
246 |   \(2-\sqrt3\) – formula (10).
247 | * Substituting (10) back into the expression for \(\mu\) gives the
248 |   explicit family (11) of amazing integers; they satisfy the linear
249 |   recurrence (12) and therefore have the exponential growth described
250 |   in (13)–(16).
251 | * The limits in (14) and (16) are exactly the numbers \(x\) and \(z\)
252 |   required; a short computation finishes the problem.  ∎
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
   - Fill in the header (Problem `6_AMAZIN`, Submission `model_4`, your grader
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
   `grade_6_AMAZIN_model_4_AI.tex`.
3. **Check it compiles.** Run `pdflatex -interaction=nonstopmode <file>.tex` and fix any
   errors so it builds to a PDF. (Keep the document self-contained — do not add external
   dependencies.)
4. **State the proposed mark** (0/1/6/7) clearly in your final message.

Do **not** commit anything to the repository — return the `.tex` (and its PDF if produced).
