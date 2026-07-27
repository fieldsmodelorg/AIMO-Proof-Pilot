# AIMO Proof Pilot — grading task

You are an **expert olympiad grader** for the AIMO Proof Pilot. Your job is to grade **one**
submission against the official markscheme and return a completed grading sheet as a LaTeX
(`.tex`) file.

- **Problem:** `3_SINDEX`
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
\section*{Problem 3 (SINDEX)}


\problem[5]{%
For a finite, nonempty multiset $S$ of positive integers strictly less than $20$, we define its \emph{index} to be the greatest positive integer $n$ such that for every $i$ with $1 \leq i \leq n$ we can partition $S$ into multisets $A_i$ and $B_i$ in such a way that $A_i=i+B_i$. If no such $n$ exists, we define the index to be equal to $0$.

Let $N$ denote the maximum index across all choices for $S$. Across all choices of $S$ with index $N$, let $M$ denote the smallest possible value for the maximum element in $S$. 

Across all multisets $S$ with index $N$ and maximum element $M$, what is the smallest possible number of elements of $S$ (counted with multiplicity)?

\textit{For two multisets $X$ and $Y$ and a positive integer $l$, we write $X=l+Y$ if $X=\{l+y: y \in Y\}$ where the right-hand side is interpreted as a multiset.}
}{32}

\vspace{2cm}

\textbf{Original AIMO3 Formulation:} 

For a finite, nonempty multiset $S$ of positive integers strictly less than $20$, we define its \emph{index} to be the greatest positive integer $n$ such that for every $i$ with $1 \leq i \leq n$ we can partition $S$ into multisets $A_i$ and $B_i$ in such a way that $A_i=i+B_i$. If no such $n$ exists, we define the index to be equal to $0$.

Let $N$ denote the maximum index across all choices for $S$. Across all choices of $S$ with index $N$, let $M$ denote the smallest possible value for the maximum element in $S$. 

Across all multisets $S$ with index $N$ and maximum element $M$, what is the smallest possible number of elements of $S$ (counted with multiplicity)?

\textit{For two multisets $X$ and $Y$ and a positive integer $l$, we write $X=l+Y$ if $X=\{l+y: y \in Y\}$ where the right-hand side is interpreted as a multiset.}

\textbf{Answer:} 32


\clearpage

\polishedsolution[SB][5]{%
For a finite multiset $S$, define
\begin{equation*}
    P_S(x)= \sum\limits_{s \in S} x^s.
\end{equation*}
We call a polynomial $Q(x)$ \emph{set-like} if there exists a multiset $T$ of positive integers such that $Q=P_{T}$. This is equivalent to saying that $Q$ has non-negative integer coefficients and no constant term.

\textbf{Claim 1:} For a positive integer $m$, $S$ has index at least $m$ if and only if for each $1 \leq i \leq m$, $\frac{P_S(x)}{1+x^i}$ is a set-like polynomial.
\begin{proof}
    Suppose first that, for a fixed positive integer $i$, we have a partition
    \begin{equation*}
        S=A_i\sqcup B_i
    \end{equation*}
    with $A_i=i+B_i$. Then
    \begin{equation*}
        P_{A_i}(x)=\sum_{a\in A_i}x^a=\sum_{b\in B_i}x^{b+i}=x^iP_{B_i}(x),
    \end{equation*}
    and hence
    \begin{equation*}
        P_S(x)=P_{A_i}(x)+P_{B_i}(x)=(1+x^i)P_{B_i}(x).
    \end{equation*}
    Therefore $P_S(x)/(1+x^i)=P_{B_i}(x)$ is set-like.
    
    Conversely, suppose that $P_S(x)/(1+x^i)$ is set-like. Choose a multiset $B_i$ such that
    \begin{equation*}
        P_{B_i}(x)=\frac{P_S(x)}{1+x^i},
    \end{equation*}
    and define $A_i=i+B_i$. Then
    \begin{equation*}
        P_{A_i}(x)+P_{B_i}(x)=x^iP_{B_i}(x)+P_{B_i}(x)=P_S(x).
    \end{equation*}
    Since equality of these polynomials means equality of the multiplicities of every positive integer, $A_i$ and $B_i$ form the required partition of $S$. Applying this for every $1\leq i\leq m$ proves the claim.
\end{proof}

Throughout the remainder of the solution, we shall use the \href{https://en.wikipedia.org/wiki/Cyclotomic_polynomial}{cyclotomic factorizations}
\begin{equation*}
\begin{aligned}
1+x&=\Phi_2, & 1+x^2&=\Phi_4, & 1+x^3&=\Phi_2\Phi_6,\\
1+x^4&=\Phi_8, & 1+x^5&=\Phi_2\Phi_{10}, & 1+x^6&=\Phi_4\Phi_{12},\\
1+x^7&=\Phi_2\Phi_{14},
\end{aligned}
\end{equation*}
where
\begin{equation*}
\begin{aligned}
\Phi_2&=1+x, & \Phi_4&=1+x^2, & \Phi_6&=1-x+x^2,\\
\Phi_8&=1+x^4, & \Phi_{10}&=1-x+x^2-x^3+x^4,\\
\Phi_{12}&=1-x^2+x^4, & \Phi_{14}&=1-x+x^2-x^3+x^4-x^5+x^6.
\end{aligned}
\end{equation*}
These distinct cyclotomic factors are well-known to be irreducible. Since every $P_S$ also has zero constant term, any multiset with index at least $m$ has $P_S$ divisible by
\begin{equation*}
    x\operatorname{lcm}(1+x,1+x^2,\ldots,1+x^m).
\end{equation*}
We can expand the $\operatorname{lcm}$ as a product of the relevant cyclotomic factors.

\clearpage

\textbf{Claim 2:} $N \leq 6$.
\begin{proof}
    If $S$ had index at least $7$, then by the above, $P_{S}(x)$ is divisible by
    \begin{equation*}
        x \cdot \Phi_2 \cdot \Phi_4 \cdot \Phi_6 \cdot \Phi_8 \cdot \Phi_{10} \cdot \Phi_{12} \cdot \Phi_{14}.
    \end{equation*}
    $P_{S}$ has degree at most $19$ (since the degree is bounded by the largest element) but the above has degree
    \begin{equation*}
         1+1+2+2+4+4+4+6=24
    \end{equation*}
    giving a contradiction.
\end{proof}

\textbf{Claim 3:} $N \leq 5$.
\begin{proof}
    Next suppose, for contradiction, that some $S$ has index at least $6$. Put
    \begin{equation*}
        Q=x \cdot \Phi_2 \cdot \Phi_4 \cdot \Phi_6 \cdot \Phi_8 \cdot \Phi_{10} \cdot \Phi_{12}.
    \end{equation*}
    Then $Q\mid P_S$ by the discussion above and $\deg Q=18$, so
    \begin{equation*}
        P_S=(ax+b)Q
    \end{equation*}
    for some integers $a,b$, since $Q$ is monic and $P_S$ has integer coefficients. Since
    \begin{equation*}
        Q(x)=x-x^2+x^3+\cdots
        \quad \text{and} \quad
        (ax+b)Q(x)=bx+(a-b)x^2+(b-a)x^3+\cdots,
    \end{equation*}
    nonnegativity of the coefficients of $P_S$ at $x^2$ and $x^3$ gives $a=b$. From the $x$ coefficient and $S$ being nonempty, $a=b>0$. But then
    \begin{equation*}
        \frac{P_S}{1+x}=aQ,
    \end{equation*}
    which is not set-like because $Q$ has a negative coefficient. This contradicts the required condition for $i=1$, proving the claim. 
\end{proof}

\textbf{Claim 4:} $N=5$.
\begin{proof}
    Consider
    \begin{equation*}
        P_0(x)=x\prod_{j=1}^5(1+x^j).  
    \end{equation*}
    This is set-like, has degree $1+1+2+3+4+5=16$, and satisfies
    \begin{equation*}
        \frac{P_0(x)}{1+x^i}=x\prod_{\substack{1\le j\le 5\\j\ne i}}(1+x^j),
        \qquad i=1,2,3,4,5,
    \end{equation*}
    which is set-like for each $i$. Thus a multiset of index at least $5$ and maximum element $16$ exists. Since $N\le 5$, we have $N=5$.
\end{proof}

\clearpage

\textbf{Claim 5:} $M=16$.
\begin{proof}
    For contradiction, assume there exists a multiset with index $5$ and maximum element less than $16$. From the discussion above, we have that
    \begin{equation*}
        R(x)=x \cdot \Phi_2 \cdot \Phi_4 \cdot \Phi_6 \cdot \Phi_8 \cdot \Phi_{10}
    \end{equation*}
    divides $P_{S}(x)$. We have
    \begin{equation*}
        \deg{R}=1+1+2+2+4+4=14
    \end{equation*}
    so, as in Claim 3, we must have that
    \begin{equation*}
        P_{S}(x)=(ax+b)R(x)
    \end{equation*}
    for integers $a$ and $b$. Also
    \begin{equation*}
        R=x-x^2+2x^3+\cdots-x^{13}+x^{14}.
    \end{equation*}
    The coefficients of $x^2$ and $x^{14}$ in $(ax+b)R$ are respectively $a-b$ and $b-a$, so being set-like forces $a=b$. The coefficient of $x$ is then $a$, so nonemptiness gives $a>0$. Hence
    \begin{equation*}
        \frac{P_S}{1+x}=aR,
    \end{equation*}
    which is not set-like because $R$ has a negative coefficient. 

    As we have shown in Claim 4 that there exists a multiset with index $5$ and maximum element $16$, we are done.
\end{proof}

\textbf{Claim 6:} For a multiset $S$ attaining the bounds $N=5$ and $M=16$, the minimum possible number of elements is $32$.
\begin{proof}
    The number of elements of $S$ is equal to $P_{S}(1)$. This shows the example given in Claim 4 has $2^{5}=32$ elements. It remains to show we cannot do better.

    Since $R\mid P_S$ and $\deg R=14$, we may write
    \begin{equation*}
        P_S=(ax^2+bx+c)R
    \end{equation*}
    for integers $a,b,c$, with $a\ge 1$ because the coefficient of $x^{16}$ is positive as $S$ must have largest element exactly $16$. The condition for $i=1$ says that
    \begin{equation*}
        \frac{P_S(x)}{1+x}=(ax^2+bx+c)\frac{R(x)}{1+x}
    \end{equation*}
    is set-like. Now
    \begin{equation*}
        \frac{R(x)}{1+x}=x-2x^2+4x^3+\cdots-2x^{12}+x^{13}.
    \end{equation*}
    Looking at the coefficients of $x^{14}$ and $x^3$ in $P_S(x)/(1+x)$ gives
    \begin{equation*}
        b-2a\geq 0,
        \quad
        a-2b+4c\geq 0.
    \end{equation*}
    Thus $b\ge 2a\ge 2$, and
    \begin{equation*}
        c\geq \frac{2b-a}{4}\geq \frac{3a}{4}.
    \end{equation*}
    Since $a,c$ are integers and $a\ge 1$, this gives $c\ge 1$. Therefore
    \begin{equation*}
        |S|=P_S(1)=(a+b+c)R(1)\ge (1+2+1)R(1)=4 \cdot 8=32
    \end{equation*}
    where we have used $R(1)=8$. This proves that $32$ is indeed the minimum.
\end{proof}

Putting all these Claims together, we have shown that the final answer is $\boxed{32}$. 
}

\clearpage

\markscheme{
A solution is \emph{essentially complete} if, allowing only minor slips of the kind described below, it proves the final answer $32$. In particular, it must establish all three optimisation layers in the problem: the maximum possible index is $N=5$, the minimum possible maximum element among multisets with index $5$ is $M=16$, and the minimum possible size among multisets with index $5$ and maximum element $16$ is $32$.

The solution does not have to use the polynomial method above. However, any essentially complete solution must contain both upper-bound arguments and matching constructions for these three values. In a polynomial solution, this means that it is not enough to prove divisibility by the polynomials $1+x^i$: wherever a construction is claimed, the relevant quotients must also be shown to be set-like, or the corresponding partitions must be given by another method.

An essentially complete solution should receive $6$ rather than $7$ if it contains a minor error or omission: a gap that is not merely a small arithmetic slip, but which can be repaired without changing the main structure of the solution. Examples include:
\begin{enumerate}[label=(ME\arabic*)]
    \item Using the correct least common multiple of the polynomials $1+x^i$ but not explicitly justifying why the distinct factors may be multiplied together, for example by mentioning irreducibility, coprimality, or cyclotomic factors.
    \item Correctly reducing the $N\leq 5$ argument to $P_S(x)=(ax+b)Q(x)$, but omitting a short justification that $a$ and $b$ are integers (if the solution requires this), or not explicitly pointing out the negative coefficient that makes $P_S(x)/(1+x)$ fail to be set-like.
    \item Giving the construction $P_S(x)=(1+x)^2R(x)$ but only sketching the verification that the five quotients $P_S(x)/(1+x^i)$ are set-like. If the construction is presented as
    \begin{equation*}
        P_{S}(x)=x\prod\limits_{j=1}^{5}(1+x^j)
    \end{equation*}
    then this is immediate and can simply be acknowledged rather than requiring further justification. 
    \item Making a fixable error in the final coefficient inequalities used to prove $P_S(1)\geq 32$, while still setting up the correct representation $P_S(x)=(ax^2+bx+c)R(x)$ and using the set-likeness of $P_S(x)/(1+x)$.
\end{enumerate}

The following should \emph{not} generally be penalised:
\begin{enumerate}[label=(NME\arabic*)]
    \item Stating the standard factorisations into cyclotomic factors for $1+x^i$, $1\leq i\leq 7$, without proving the irreducibility of each factor, provided the factorisations and least common multiples are used correctly.
    \item Omitting long polynomial expansions, provided the solution clearly states the necessary set-likeness checks and those checks are correct.
    \item Minor arithmetic slips in displayed expansions that do not affect any sign check, degree bound, or final numerical value.
    \item Not proving separately that the construction has index \emph{exactly} $5$, provided the solution has already proved the global upper bound $N\leq 5$ and has verified that the construction has index at least $5$.
    \item An isolated typo such as writing ``set'' instead of ``multiset'', provided the solution otherwise treats multiplicities correctly.
\end{enumerate}

The following are not essentially complete, even if they contain some correct calculations:
\begin{enumerate}[label=(NEC\arabic*)]
    \item A solution that proves $N\leq 6$ but does not rule out index $6$.
    \item A solution that gives only upper bounds, or only a construction, but not both.
    \item A solution that assumes $S$ is an ordinary set rather than a multiset, or otherwise imposes an extra condition not present in the problem.
    \item A polynomial solution that checks only divisibility by $1+x^i$ in its construction and never addresses the non-negativity of the quotient coefficients.
    \item A solution that proves $N=5$ but does not prove the two later minimisation statements, namely $M=16$ and the final size bound $32$.
    \item A solution that relies only on numerical search or pattern-spotting without a proof for the required upper bounds.
\end{enumerate}
}{%

Award $1$ mark to an incomplete solution if it contains a correct proof that $N\leq 6$ (Claim 2).

Do not award the partial-progress mark for any of the following on its own:
\begin{enumerate}[label=(NPP\arabic*)]
    \item Introducing the polynomial $P_S(x)$.
    \item Proving only the translation between partitions and the condition that $P_S(x)/(1+x^i)$ is set-like (Claim 1).
    \item Listing the factorisations of $1+x^i$ without using them to obtain a valid degree contradiction or another meaningful bound.
    \item Guessing or displaying the final `optimal' polynomial $P_S(x)$ without proving the necessary bounds.
    \item Numerical experimentation, checking a few examples, or making conjectures about the maximum possible index.
\end{enumerate}
}
```

---

## Submission to grade

This is the submission `model_7` for problem `3_SINDEX`, with line numbers
added for reference in your errors log.

```text
  1 | ================================================================================
  2 | SOLUTION
  3 | ================================================================================
  4 | 
  5 | ANSWER.  N = 5,  M = 16,  and the smallest possible number of elements is
  6 | 
  7 |                                    32.
  8 | 
  9 | Throughout, a multiset S of positive integers < 20 is encoded by its
 10 | generating polynomial
 11 |                          f_S(x) = sum_{s in S} x^s ,
 12 | where each element s contributes one monomial x^s counted with multiplicity.
 13 | Thus f_S has nonnegative integer coefficients, its support lies in the
 14 | exponents {1,2,...,19}, and the number of elements of S (with multiplicity)
 15 | equals f_S(1).
 16 | 
 17 | --------------------------------------------------------------------------------
 18 | 0.  REFORMULATION
 19 | --------------------------------------------------------------------------------
 20 | 
 21 | LEMMA 1.  Let i be a positive integer.  S can be partitioned into multisets
 22 | A_i, B_i with A_i = i + B_i  if and only if
 23 | 
 24 |         f_S(x) = (1 + x^i) g(x)   for some polynomial g with
 25 |         nonnegative integer coefficients.                          (*)
 26 | 
 27 | Proof.  A partition with A_i = i + B_i is the same as a way of grouping the
 28 | elements of S into unordered pairs {b, b+i} (one element b of B_i together
 29 | with the corresponding element b+i of A_i).  If g(x) = sum_b (mult) x^b is the
 30 | generating polynomial of B_i, then A_i has generating polynomial x^i g(x), and
 31 | S = A_i ⊔ B_i gives f_S = (1+x^i) g.  Conversely, given (*), g has nonnegative
 32 | integer coefficients, so it is the generating polynomial of a multiset B_i,
 33 | and A_i := i + B_i works.  ∎
 34 | 
 35 | Hence the index of S is the largest n such that (*) holds for every
 36 | i = 1,2,...,n; if even i = 1 fails the index is 0.
 37 | 
 38 | In particular, putting x = 1 in (*) shows |S| = f_S(1) is even whenever the
 39 | index is ≥ 1.
 40 | 
 41 | --------------------------------------------------------------------------------
 42 | 1.  A NECESSARY CYCLOTOMIC CONDITION
 43 | --------------------------------------------------------------------------------
 44 | 
 45 | Let Phi_m denote the m-th cyclotomic polynomial.  We use
 46 | 
 47 |    Phi_2  = 1 + x                  Phi_8  = 1 + x^4
 48 |    Phi_4  = 1 + x^2                Phi_10 = 1 - x + x^2 - x^3 + x^4
 49 |    Phi_6  = 1 - x + x^2            Phi_12 = 1 - x^2 + x^4
 50 | 
 51 | and the factorizations
 52 | 
 53 |    1 + x   = Phi_2
 54 |    1 + x^2 = Phi_4
 55 |    1 + x^3 = Phi_2 Phi_6
 56 |    1 + x^4 = Phi_8
 57 |    1 + x^5 = Phi_2 Phi_10
 58 |    1 + x^6 = Phi_4 Phi_12                                          (1)
 59 | 
 60 | (These are read off from 1 + x^i = (x^{2i}-1)/(x^i-1).)
 61 | 
 62 | If S has index ≥ n then for every i ≤ n, (1+x^i) divides f_S, hence every
 63 | cyclotomic factor occurring in (1) for i ≤ n divides f_S.  Since distinct
 64 | cyclotomic polynomials are coprime, their product divides f_S.  Define
 65 | 
 66 |    L_5 = Phi_2 Phi_4 Phi_6 Phi_8 Phi_10              (deg 13),
 67 |    L_6 = Phi_2 Phi_4 Phi_6 Phi_8 Phi_10 Phi_12       (deg 17).
 68 | 
 69 | By (1):
 70 | 
 71 |    index ≥ 5  =>  L_5 | f_S,        index ≥ 6  =>  L_6 | f_S.       (2)
 72 | 
 73 | Their explicit coefficient lists (exponents 0,1,2,...) are
 74 | 
 75 |    L_5 = [1,-1, 2,-1, 2, 0, 1, 1, 0, 2,-1, 2,-1, 1]
 76 |    L_6 = [1,-1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1,-1, 1]    (3)
 77 | 
 78 | (One checks (3) directly by multiplying the cyclotomic polynomials above;
 79 | note L_6 = L_5 · Phi_12.)  Both L_5 and L_6 are monic with constant term 1.
 80 | 
 81 | --------------------------------------------------------------------------------
 82 | 2.  THE MAXIMUM INDEX IS N = 5
 83 | --------------------------------------------------------------------------------
 84 | 
 85 | 2a.  Index 6 is impossible.
 86 | 
 87 | Suppose S has index ≥ 6.  By (2), L_6 | f_S, so f_S = L_6 · h for an integer
 88 | polynomial h.  Because the support of f_S lies in {1,...,19} we have
 89 | deg f_S ≤ 19, so deg h ≤ 19 - 17 = 2; and f_S(0) = 0 with L_6(0) = 1 forces
 90 | h(0) = 0.  Therefore
 91 | 
 92 |                          h(x) = a x + b x^2 ,   a, b integers.
 93 | 
 94 | Using (3), the coefficient of x^2 in f_S is
 95 |        [x^2] f_S = a·L_6[1] + b·L_6[0] = -a + b ,
 96 | and the coefficient of x^3 is
 97 |        [x^3] f_S = a·L_6[2] + b·L_6[1] =  a - b .
 98 | Both must be ≥ 0 (coefficients of a multiset), so -a+b ≥ 0 and a-b ≥ 0, i.e.
 99 | 
100 |                                  a = b =: t .
101 | 
102 | Since S is nonempty, t ≥ 1, and
103 | 
104 |        f_S = t (x + x^2) L_6 = t · x (1+x) L_6 .
105 | 
106 | Now test i = 1.  Dividing by (1 + x) = Phi_2 (which is a genuine factor):
107 |        f_S / (1 + x) = t · x · L_6 .
108 | The coefficient of x^2 here equals t·L_6[1] = -t < 0.  Hence the quotient
109 | g in (*) for i = 1 has a NEGATIVE coefficient, so there is no valid partition
110 | for i = 1 — contradicting index ≥ 6 (which requires i = 1 to work).
111 | 
112 | Therefore no S has index ≥ 6, and  N ≤ 5.
113 | 
114 | 2b.  Index 5 is attained.
115 | 
116 | Take h(x) = x + 2x^2 + x^3 and set f = L_5 · h.  Expanding (using (3)),
117 | 
118 |    f(x) = x + x^2 + x^3 + 2x^4 + 2x^5 + 3x^6 + 3x^7 + 3x^8 + 3x^9
119 |             + 3x^10 + 3x^11 + 2x^12 + 2x^13 + x^14 + x^15 + x^16 ,
120 | 
121 | which corresponds to the multiset
122 | 
123 |    S* = { 1, 2, 3, 4,4, 5,5, 6,6,6, 7,7,7, 8,8,8, 9,9,9,
124 |           10,10,10, 11,11,11, 12,12, 13,13, 14, 15, 16 }.
125 | 
126 | All coefficients are nonnegative and the support is {1,...,16} ⊂ {1,...,19},
127 | so S* is a legitimate multiset.  Its index is exactly 5: explicit partitions
128 | into pairs {b, b+i} for i = 1,2,3,4,5 (each a list of 16 pairs covering S*
129 | exactly) are
130 | 
131 |  i=1: (1,2)(3,4)(4,5)(5,6)(6,7)(6,7)(7,8)(8,9)(8,9)(9,10)(10,11)(10,11)
132 |       (11,12)(12,13)(13,14)(15,16)
133 |  i=2: (1,3)(2,4)(4,6)(5,7)(5,7)(6,8)(6,8)(7,9)(8,10)(9,11)(9,11)(10,12)
134 |       (10,12)(11,13)(13,15)(14,16)
135 |  i=3: (1,4)(2,5)(3,6)(4,7)(5,8)(6,9)(6,9)(7,10)(7,10)(8,11)(8,11)(9,12)
136 |       (10,13)(11,14)(12,15)(13,16)
137 |  i=4: (1,5)(2,6)(3,7)(4,8)(4,8)(5,9)(6,10)(6,10)(7,11)(7,11)(8,12)(9,13)
138 |       (9,13)(10,14)(11,15)(12,16)
139 |  i=5: (1,6)(2,7)(3,8)(4,9)(4,9)(5,10)(5,10)(6,11)(6,11)(7,12)(7,12)(8,13)
140 |       (8,13)(9,14)(10,15)(11,16)
141 | 
142 | (One verifies for each i that the multiset of all entries appearing is exactly
143 | S*.)  Thus partitions exist for i = 1,...,5, so the index is ≥ 5; by part 2a
144 | it cannot exceed 5.  Hence the index of S* equals 5, and combined with 2a,
145 | 
146 |                                  N = 5.
147 | 
148 | [Sufficiency remark used implicitly: whenever f = L_5·h with h having
149 | nonnegative coefficients, dropping any single factor (1+x^i) for i ≤ 5 leaves
150 | a product of (3) with nonnegative pieces and h, but in general we simply verify
151 | each quotient directly, as done above.]
152 | 
153 | --------------------------------------------------------------------------------
154 | 3.  THE SMALLEST MAXIMUM ELEMENT IS M = 16
155 | --------------------------------------------------------------------------------
156 | 
157 | Let S have index 5 (= N).  By (2), L_5 | f_S, so f_S = L_5 · h with h an
158 | integer polynomial, h(0) = 0 (since f_S(0)=0, L_5(0)=1).  The maximum element
159 | of S equals deg f_S = 13 + deg h.  Since h(0) = 0 and h ≠ 0, deg h ≥ 1, giving
160 | maximum element ≥ 14.  We rule out 14 and 15.
161 | 
162 | • Maximum element 14  (deg h = 1):  h = c x, c ≥ 1, so f_S = c·x·L_5.  By (3),
163 |   [x^2] f_S = c·L_5[1] = -c < 0, impossible for a multiset.
164 | 
165 | • Maximum element 15  (deg h = 2):  h = c1 x + c2 x^2 with c2 ≥ 1.  Then
166 |         [x^2]  f_S = c1·L_5[1] + c2·L_5[0] = -c1 + c2 ≥ 0  =>  c2 ≥ c1,
167 |         [x^14] f_S = c1·L_5[13] + c2·L_5[12] =  c1 - c2 ≥ 0  =>  c1 ≥ c2,
168 |   so c1 = c2 =: s ≥ 1 and f_S = s·x(1+x)L_5.  Dividing by (1+x),
169 |         f_S/(1+x) = s·x·L_5 ,  whose [x^2]-coefficient is s·L_5[1] = -s < 0,
170 |   so the i = 1 partition fails — contradicting index 5.
171 | 
172 | Hence every index-5 multiset has maximum element ≥ 16, and S* above achieves
173 | 16.  Therefore  M = 16.
174 | 
175 | --------------------------------------------------------------------------------
176 | 4.  THE SMALLEST NUMBER OF ELEMENTS IS 32
177 | --------------------------------------------------------------------------------
178 | 
179 | Let S have index 5 and maximum element 16.  As in Section 3, f_S = L_5 · h
180 | with h(0) = 0 and deg f_S = 16, so deg h = 3:
181 | 
182 |                  h(x) = c1 x + c2 x^2 + c3 x^3 ,   c3 ≠ 0.
183 | 
184 | KEY IDENTITY (size formula).  Evaluating at x = 1,
185 |        |S| = f_S(1) = L_5(1) · h(1) = 8 · (c1 + c2 + c3),
186 | because L_5(1) = Phi_2(1)Phi_4(1)Phi_6(1)Phi_8(1)Phi_10(1) = 2·2·1·2·1 = 8.
187 | Thus |S| is 8 times the integer h(1) = c1 + c2 + c3, and minimizing |S| means
188 | minimizing c1 + c2 + c3.
189 | 
190 | Sign constraints on the coefficients of f_S = L_5·h (read off via (3)):
191 |        [x^1]  f_S = c1·L_5[0]              = c1            ≥ 0,
192 |        [x^16] f_S = c3·L_5[13]             = c3            ≥ 0,  and c3 ≠ 0,
193 |        [x^2]  f_S = c1·L_5[1] + c2·L_5[0]  = c2 - c1       ≥ 0,
194 |        [x^15] f_S = c2·L_5[13]+ c3·L_5[12] = c2 - c3       ≥ 0.
195 | Therefore  c1 ≥ 0,  c3 ≥ 1,  c2 ≥ c1,  c2 ≥ c3 ≥ 1.  In particular all of
196 | c1, c2, c3 are nonnegative with c2 ≥ 1 and c3 ≥ 1.
197 | 
198 | We claim c1 + c2 + c3 ≥ 4.  Suppose instead c1 + c2 + c3 ≤ 3.  Subject to
199 | 0 ≤ c1 ≤ c2, 1 ≤ c3 ≤ c2, the only integer triples are
200 | 
201 |    (c1,c2,c3) = (0,1,1),  (1,1,1),  (0,2,1).
202 | 
203 | We check each fails to give an index-5 multiset:
204 | 
205 |  (0,1,1):  f = L_5(x^2+x^3) = x^2(1+x)L_5.  Its (1+x)-quotient is x^2 L_5,
206 |            whose [x^3]-coefficient is L_5[1] = -1 < 0, so i = 1 already fails
207 |            (index 0).
208 | 
209 |  (1,1,1):  f = x(1+x+x^2)L_5.  Direct division by (1+x) gives a quotient with
210 |            a negative coefficient (e.g. [x^2] of f/(1+x) is -1), so i = 1
211 |            fails (index 0).
212 | 
213 |  (0,2,1):  f = L_5(2x^2 + x^3) has [x^3] f = 2·L_5[1] + L_5[0] = -2 + 1
214 |            = -1 < 0, so f is not even a valid multiset.
215 | 
216 | (Each statement is a one-line coefficient computation from (3).)  None of the
217 | three has index 5, so c1 + c2 + c3 ≥ 4, hence
218 | 
219 |                        |S| = 8(c1+c2+c3) ≥ 8·4 = 32.
220 | 
221 | This bound is attained: S* from Section 2b has h = x + 2x^2 + x^3, so
222 | c1+c2+c3 = 4 and |S*| = 32, with index 5 and maximum element 16.
223 | 
224 | --------------------------------------------------------------------------------
225 | 5.  CONCLUSION
226 | --------------------------------------------------------------------------------
227 | 
228 | The maximum index over all admissible multisets is N = 5.  Among multisets of
229 | index 5, the smallest possible maximum element is M = 16.  Among multisets of
230 | index 5 with maximum element 16, the number of elements is a multiple of 8 and
231 | is at least 32, with equality achieved by
232 | 
233 |    S* = {1, 2, 3, 4², 5², 6³, 7³, 8³, 9³, 10³, 11³, 12², 13², 14, 15, 16}.
234 | 
235 | Hence the smallest possible number of elements of S (with multiplicity) is
236 | 
237 |                                 ┌──────────┐
238 |                                 │   32     │
239 |                                 └──────────┘
240 | ================================================================================
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
   - Fill in the header (Problem `3_SINDEX`, Submission `model_7`, your grader
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
   `grade_3_SINDEX_model_7_AI.tex`.
3. **Check it compiles.** Run `pdflatex -interaction=nonstopmode <file>.tex` and fix any
   errors so it builds to a PDF. (Keep the document self-contained — do not add external
   dependencies.)
4. **State the proposed mark** (0/1/6/7) clearly in your final message.

Do **not** commit anything to the repository — return the `.tex` (and its PDF if produced).
