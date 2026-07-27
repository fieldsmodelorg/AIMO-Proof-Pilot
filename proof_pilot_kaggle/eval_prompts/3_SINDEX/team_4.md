# AIMO Proof Pilot — grading task

You are an **expert olympiad grader** for the AIMO Proof Pilot. Your job is to grade **one**
submission against the official markscheme and return a completed grading sheet as a LaTeX
(`.tex`) file.

- **Problem:** `3_SINDEX`
- **Submission:** `team_4`

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

This is the submission `team_4` for problem `3_SINDEX`, with line numbers
added for reference in your errors log.

```text
  1 | We consider a finite nonempty multiset \(S\) of positive integers \(<20\).  Let  
  2 | \[
  3 | f(x)=\sum_{a\in S}x^a
  4 | \]  
  5 | be its generating function (coefficient of \(x^a\) equals the multiplicity of \(a\)).  
  6 | For a fixed positive integer \(i\) the condition that \(S\) can be partitioned into \(A_i,B_i\) with \(A_i=i+B_i\) is equivalent to  
  7 | \[
  8 | f(x)=(1+x^i)g_i(x)
  9 | \]  
 10 | for some polynomial \(g_i(x)\) with non‑negative integer coefficients.  
 11 | The index of \(S\) is the largest \(n\) for which this holds for every \(i=1,\dots,n\); if no such \(n\) exists the index is \(0\).
 12 | 
 13 | Let \(L_n(x)\) be the least common multiple (in \(\mathbb Z[x]\)) of the polynomials \(1+x^i\) for \(i=1,\dots,n\).  
 14 | If \(S\) has index at least \(n\) then each \(1+x^i\) divides \(f(x)\), hence \(L_n(x)\) divides \(f(x)\); therefore  
 15 | \[
 16 | f(x)=L_n(x)\,h(x)
 17 | \]  
 18 | for some polynomial \(h(x)\) with integer coefficients.  Moreover \(f(0)=0\) and \(\deg f\le 19\) (because all elements are \(<20\)).
 19 | 
 20 | ---
 21 | ### 1.  The maximum possible index \(N\)
 22 | 
 23 | The cyclotomic factorisation of \(1+x^i\) is  
 24 | \[
 25 | 1+x^i=\prod_{\substack{d\mid 2i\\ d\nmid i}}\Phi_d(x),
 26 | \]  
 27 | where \(\Phi_d\) are the cyclotomic polynomials.  Hence  
 28 | \[
 29 | L_n(x)=\prod_{\substack{d\ \text{primitive for some}\ i\le n}}\Phi_d(x).
 30 | \]  
 31 | For \(n=5\) the relevant divisors are \(2,4,6,8,10\); for \(n=6\) we also have \(12\).  
 32 | Thus  
 33 | \[
 34 | L_5(x)=\Phi_2\Phi_4\Phi_6\Phi_8\Phi_{10},\qquad
 35 | L_6(x)=L_5(x)\,\Phi_{12}.
 36 | \]  
 37 | Their degrees are  
 38 | \[
 39 | \deg L_5=1+2+2+4+4=13,\qquad \deg L_6=13+4=17.
 40 | \]
 41 | 
 42 | **Index \(6\) is impossible.**  
 43 | Assume that a multiset \(S\) has index \(\ge6\). Then \(f=L_6h\) with \(\deg f\le19\), so \(\deg h\le2\). Write \(h(x)=ax+bx^2\) (\(a,b\) integers).  Because \(f(0)=0\) we have \(h(0)=0\).  
 44 | Now consider the condition for \(i=1\).  Set \(Q_1(x)=L_6(x)/(1+x)\).  Using the product form,  
 45 | \[
 46 | Q_1(x)=\bigl(\Phi_4\Phi_6\Phi_8\Phi_{10}\bigr)(1-x^2+x^4)
 47 | \]  
 48 | and an explicit multiplication gives  
 49 | \[
 50 | Q_1(x)=1-2x+3x^2-3x^3+4x^4-4x^5+5x^6-5x^7+6x^8-5x^9+5x^{10}-4x^{11}+4x^{12}-3x^{13}+3x^{14}-2x^{15}+x^{16}.
 51 | \]  
 52 | The product \(Q_1(x)h(x)\) must have non‑negative coefficients.  Computing the coefficients yields the inequalities  
 53 | 
 54 | \[
 55 | \begin{aligned}
 56 | k=1 &: a\ge0,\\
 57 | k=2 &: -2a+b\ge0 \;\Rightarrow\; b\ge2a,\\
 58 | k=3 &: 3a-2b\ge0 \;\Rightarrow\; b\le\frac32a,\\
 59 | k=11 &: 5a-5b\ge0 \;\Rightarrow\; a\ge b,\\
 60 | k=17 &: a-2b\ge0 \;\Rightarrow\; a\ge2b.
 61 | \end{aligned}
 62 | \]  
 63 | The conditions \(b\ge2a\) and \(b\le\frac32a\) force \(b=2a\); then \(a\ge2b\) gives \(a\ge4a\), so \(a=0\) and consequently \(b=0\).  Hence no non‑zero polynomial \(h\) of degree \(\le2\) exists, contradicting the existence of a non‑empty \(S\) with index \(6\).  Therefore \(N\le5\).
 64 | 
 65 | **Index \(5\) is attainable.**  
 66 | Define  
 67 | \[
 68 | f(x)=x\prod_{i=1}^{5}(1+x^i)=x+x^2+x^3+2x^4+2x^5+3x^6+3x^7+3x^8+3x^9+3x^{10}+2x^{11}+2x^{12}+x^{13}+x^{14}+x^{15}+x^{16}.
 69 | \]  
 70 | For each \(i=1,\dots,5\) we have  
 71 | \[
 72 | \frac{f(x)}{1+x^i}=x\prod_{\substack{j=1\\j\neq i}}^{5}(1+x^j),
 73 | \]  
 74 | which is a product of polynomials with non‑negative coefficients, hence has non‑negative coefficients.  Thus the index of this multiset is at least \(5\).  Combined with \(N\le5\) we obtain \(N=5\).
 75 | 
 76 | ---
 77 | ### 2.  The smallest possible maximum element \(M\) for index \(5\)
 78 | 
 79 | Let \(S\) have index \(5\) and write \(f(x)=L_5(x)\,h(x)\) with \(h(0)=0\) and \(\deg f\le19\).  Because \(\deg L_5=13\), we have \(\deg h\le6\).  We first show that \(\deg h\ge3\).  Suppose \(\deg h\le2\), write \(h(x)=ax+bx^2\).  
 80 | Now use the condition for \(i=1\): \(f/(1+x)= (L_5/(1+x))\,h\) must have non‑negative coefficients.  
 81 | Set  
 82 | \[
 83 | Q_1^{(5)}(x)=\frac{L_5(x)}{1+x}= \Phi_4\Phi_6\Phi_8\Phi_{10}=
 84 | 1-2x+4x^2-5x^3+7x^4-7x^5+8x^6-7x^7+7x^8-5x^9+4x^{10}-2x^{11}+x^{12}.
 85 | \]  
 86 | The product \((ax+bx^2)Q_1^{(5)}\) gives the inequalities  
 87 | 
 88 | \[
 89 | \begin{aligned}
 90 | x^2 &: -2a+b\ge0 \;\Rightarrow\; b\ge2a,\\
 91 | x^3 &: 4a-2b\ge0 \;\Rightarrow\; b\le2a,
 92 | \end{aligned}
 93 | \]  
 94 | so \(b=2a\).  Then the coefficient of \(x^5\) is \(7a-5b=7a-10a=-3a\ge0\), which forces \(a=0\) and hence \(b=0\).  Thus no non‑zero \(h\) of degree \(\le2\) exists.  Therefore \(\deg h\ge3\), and consequently \(\deg f=\deg L_5+\deg h\ge13+3=16\).  Hence the maximum element \(M\) of \(S\) satisfies \(M\ge16\).
 95 | 
 96 | The example above has maximum element \(16\); therefore \(M=16\).
 97 | 
 98 | ---
 99 | ### 3.  The smallest possible number of elements for index \(5\) and maximum element \(16\)
100 | 
101 | Now assume that \(S\) has index \(5\) and its maximum element is exactly \(16\).  Then \(\deg f=16\) and \(\deg h=3\).  Write \(h(x)=ax+bx^2+cx^3\) with integers \(a,b,c\).  Because all coefficients of \(f\) are non‑negative and \(f(0)=0\), we have \(a,b,c\ge0\) (the coefficient of \(x^1\) is \(a\), etc.).  The number of elements of \(S\) is  
102 | \[
103 | f(1)=L_5(1)\,h(1)=8\,(a+b+c),
104 | \]  
105 | since \(L_5(1)=\Phi_2(1)\Phi_4(1)\Phi_6(1)\Phi_8(1)\Phi_{10}(1)=2\cdot2\cdot1\cdot2\cdot1=8\).  To minimise the number of elements we must minimise \(a+b+c\) subject to the condition that for every \(i=1,\dots,5\) the polynomial \(Q_i(x)h(x)\) has non‑negative coefficients, where \(Q_i(x)=L_5(x)/(1+x^i)\).
106 | 
107 | The most restrictive condition comes from \(i=1\).  Using the same \(Q_1^{(5)}(x)\) as above, the coefficients of \((ax+bx^2+cx^3)Q_1^{(5)}\) must be non‑negative.  Computing these coefficients gives the following inequalities (the coefficient of \(x^k\) is \(a\,q_{k-1}+b\,q_{k-2}+c\,q_{k-3}\), where \(q_j\) are the coefficients of \(Q_1^{(5)}\)):
108 | 
109 | \[
110 | \begin{array}{c|c}
111 | k & \text{coefficient} \\ \hline
112 | 2 & -2a+b \\
113 | 3 & 4a-2b+c \\
114 | 4 & -5a+4b-2c \\
115 | 5 & 7a-5b+4c \\
116 | 6 & -7a+7b-5c \\
117 | 7 & 8a-7b+7c \\
118 | 8 & -7a+8b-7c \\
119 | 9 & 7a-7b+8c \\
120 | 10 & -5a+7b-7c \\
121 | 11 & 4a-5b+7c \\
122 | 12 & -2a+4b-5c \\
123 | 13 & a-2b+4c \\
124 | 14 & b-2c \\
125 | 15 & c
126 | \end{array}
127 | \]
128 | 
129 | All of these must be \(\ge0\).  The first and last inequalities give \(b\ge2a\) and \(b\ge2c\), so \(a,b,c\ge0\).
130 | 
131 | **Solving the system.**  
132 | If \(a=0\) then from \(b\ge2c\) and the inequality for \(k=5\) (\(7\cdot0+4c\ge5b\)) we obtain \(4c\ge5b\ge10c\), hence \(c=0\) and then \(b=0\).  Thus \(a\ge1\).  
133 | 
134 | For \(a=1\) we have \(b\ge2\).  The inequality \(b\ge2c\) together with \(a+4c\ge2b\) (from \(k=13\)) gives  
135 | \[
136 | 1+4c\ge2b\ge4c\quad\Longrightarrow\quad1\ge0,
137 | \]  
138 | which is always true.  The strongest constraints are the ones from the coefficients of \(x^5\) and \(x^6\):  
139 | \[
140 | 7+4c\ge5b,\qquad 7+5c\le7b.
141 | \]  
142 | For \(b=2\) we obtain \(4c\ge3\) and \(5c\le7\), so \(c=1\).  For \(b=3\) we would need \(c\ge?\) but then \(b\ge2c\) forces \(c\le1\), and the inequality \(7+5c\le7b\) becomes \(7+5c\le21\), which is satisfied, but the inequality \(7+4c\ge5b\) gives \(7+4c\ge15\Rightarrow4c\ge8\Rightarrow c\ge2\), contradicting \(c\le1\).  Hence the only possibility for \(a=1\) is \((a,b,c)=(1,2,1)\).
143 | 
144 | For \(a\ge2\) we have \(b\ge2a\ge4\).  The inequality \(b\ge2c\) together with \(a+4c\ge2b\) gives  
145 | \[
146 | 2b\le a+4c\le a+2b\quad\text{(since }c\le b/2\text{)},
147 | \]  
148 | which is automatically true.  The inequality \(7a+5c\le7b\) forces \(c\le (7b-7a)/5\).  For \(a=2\) and \(b=4\) we get \(c\le (28-14)/5=3.2\), and from \(b\ge2c\) we have \(c\le2\).  The inequality \(7a+4c\ge5b\) gives \(14+4c\ge20\Rightarrow4c\ge6\Rightarrow c\ge2\).  Hence \(c=2\).  Then \(a+b+c=8\).  For larger \(a\) the sum is even larger.  Thus the smallest possible sum is \(a+b+c=4\), attained at \((1,2,1)\).
149 | 
150 | Therefore the number of elements is at least \(8\cdot4=32\).  The example \(f(x)=x\prod_{i=1}^5(1+x^i)\) corresponds to \(h(x)=x+2x^2+x^3\) and has exactly \(32\) elements.  Hence the minimal possible number of elements is \(m=32\).
151 | 
152 | ---
153 | ### 4.  Conclusion
154 | 
155 | \[
156 | \boxed{N=5},\qquad \boxed{M=16},\qquad \boxed{m=32}.
157 | \]
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
   - Fill in the header (Problem `3_SINDEX`, Submission `team_4`, your grader
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
   `grade_3_SINDEX_team_4_AI.tex`.
3. **Check it compiles.** Run `pdflatex -interaction=nonstopmode <file>.tex` and fix any
   errors so it builds to a PDF. (Keep the document self-contained — do not add external
   dependencies.)
4. **State the proposed mark** (0/1/6/7) clearly in your final message.

Do **not** commit anything to the repository — return the `.tex` (and its PDF if produced).
