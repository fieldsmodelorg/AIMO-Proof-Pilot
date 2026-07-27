# AIMO Proof Pilot — grading task

You are an **expert olympiad grader** for the AIMO Proof Pilot. Your job is to grade **one**
submission against the official markscheme and return a completed grading sheet as a LaTeX
(`.tex`) file.

- **Problem:** `3_SINDEX`
- **Submission:** `team_3`

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

This is the submission `team_3` for problem `3_SINDEX`, with line numbers
added for reference in your errors log.

```text
  1 | ## Solution  
  2 | 
  3 | ### 1. Reformulation of the condition  
  4 | 
  5 | Let \(S\) be a multiset of positive integers \(<20\). For each integer \(k\) with \(1\le k\le 19\) denote by \(m_k\) the multiplicity of \(k\) in \(S\).  
  6 | For a fixed positive integer \(i\) the requirement that \(S\) can be split into multisets \(A_i\) and \(B_i\) with \(A_i = i+B_i\) is equivalent to the existence of non‑negative integers \(b_k\) (\(k=1,\dots,19\)) such that  
  7 | 
  8 | \[
  9 | m_k = b_k + b_{k-i}\qquad (k=1,\dots,19),
 10 | \]  
 11 | 
 12 | where we set \(b_j=0\) for \(j<1\) or \(j>19\). Moreover, because \(B_i\) cannot contain numbers larger than \(19-i\), we must have \(b_k=0\) for all \(k>19-i\).  
 13 | 
 14 | If we introduce the generating polynomials  
 15 | 
 16 | \[
 17 | M(x)=\sum_{k=1}^{19} m_k x^k,\qquad B_i(x)=\sum_{k=1}^{19-i} b_k x^k,
 18 | \]  
 19 | 
 20 | the condition becomes  
 21 | 
 22 | \[
 23 | M(x)=B_i(x)(1+x^i),
 24 | \]  
 25 | 
 26 | and the requirement that \(B_i(x)\) has non‑negative coefficients is exactly the original partition condition.  
 27 | Thus for a given \(i\) the multiset \(S\) has the required property **iff** \(M(x)\) is divisible by \(1+x^i\) and the quotient has all coefficients non‑negative.
 28 | 
 29 | ---
 30 | 
 31 | ### 2. The maximal index \(N\)  
 32 | 
 33 | #### 2.1. An example with index \(5\)  
 34 | 
 35 | Consider  
 36 | 
 37 | \[
 38 | M(x)=x(1+x)(1+x^2)(1+x^3)(1+x^4)(1+x^5).
 39 | \]  
 40 | 
 41 | Expanding gives  
 42 | 
 43 | \[
 44 | M(x)=x^{16}+x^{15}+x^{14}+2x^{13}+2x^{12}+3x^{11}+3x^{10}+3x^{9}+3x^{8}+3x^{7}+3x^{6}+3x^{5}+2x^{4}+2x^{3}+x^{2}+x.
 45 | \]  
 46 | 
 47 | For any \(i\in\{1,2,3,4,5\}\) we have  
 48 | 
 49 | \[
 50 | \frac{M(x)}{1+x^i}=x\prod_{\substack{j=1\\ j\ne i}}^{5}(1+x^j),
 51 | \]  
 52 | 
 53 | which is a product of polynomials with non‑negative coefficients, hence has non‑negative coefficients itself. Therefore for each \(i=1,\dots,5\) the required partition exists. The multiset \(S\) defined by the coefficients of \(M(x)\) is non‑empty, so its index is at least \(5\).
 54 | 
 55 | #### 2.2. No multiset can have index \(6\) or more  
 56 | 
 57 | Assume, for contradiction, that there exists a non‑empty multiset \(S\) with index \(\ge 6\). Then its generating polynomial \(M(x)\) satisfies  
 58 | 
 59 | \[
 60 | M(x)=B_i(x)(1+x^i)\qquad\text{with }B_i(x)\text{ having non‑negative coefficients for }i=1,\dots,6.
 61 | \]  
 62 | 
 63 | In particular, \(1+x^i\) divides \(M(x)\) for \(i=1,\dots,6\). Let \(L(x)\) be the least common multiple of these six polynomials. A straightforward computation yields  
 64 | 
 65 | \[
 66 | L(x)=x^{17}-x^{16}+x^{15}+x^{13}+x^{11}+x^{9}+x^{8}+x^{6}+x^{4}+x^{2}-x+1.
 67 | \]  
 68 | 
 69 | Because each \(1+x^i\) divides \(M(x)\), \(L(x)\) also divides \(M(x)\). Write  
 70 | 
 71 | \[
 72 | M(x)=L(x)R(x)
 73 | \]  
 74 | 
 75 | with \(R(x)\in\mathbb{Z}[x]\). Since \(\deg M\le 19\) and \(\deg L=17\), we have \(\deg R\le 2\). Moreover, the constant term of \(M(x)\) is \(0\) (only positive integers occur) and \(L(0)=1\); hence \(R(0)=0\). Thus \(R(x)=a x+b x^2\) for some integers \(a,b\ge 0\) (the coefficients must be non‑negative because otherwise \(M(x)\) would have negative coefficients).
 76 | 
 77 | Now consider the quotient for \(i=6\):
 78 | 
 79 | \[
 80 | Q_6(x)=\frac{M(x)}{1+x^6}=\frac{L(x)}{1+x^6}\cdot R(x).
 81 | \]  
 82 | 
 83 | One computes  
 84 | 
 85 | \[
 86 | \frac{L(x)}{1+x^6}=x^{11}-x^{10}+x^{9}+x^{7}+x^{4}+x^{2}-x+1.
 87 | \]  
 88 | 
 89 | This polynomial contains a negative coefficient (for \(x^{10}\)). Multiplying by \(R(x)=a x+b x^{2}\) gives, in particular, the coefficient of \(x^{11}\) as \(-a+b\). For \(Q_6(x)\) to have all coefficients non‑negative we must have \(-a+b\ge 0\), i.e. \(b\ge a\).
 90 | 
 91 | A similar analysis for \(i=5\) gives  
 92 | 
 93 | \[
 94 | \frac{L(x)}{1+x^5}=x^{12}-x^{11}+x^{10}+x^{8}+x^{6}+x^{4}-x^{2}+1,
 95 | \]  
 96 | 
 97 | and the coefficient of \(x^{12}\) in \(Q_5(x)\) becomes \(-a+b\) as well, forcing again \(b\ge a\).  
 98 | 
 99 | Examining the quotients for \(i=3,2,1\) yields the same inequality \(-a+b\ge 0\). Moreover, by looking at other terms one can show that the only way to satisfy all non‑negativity conditions simultaneously is \(a=b=0\). (A detailed verification can be carried out by writing down the full coefficient expressions; they all contain a factor \(-a+b\) in some position, and if \(a,b>0\) then at least one quotient will have a negative coefficient.)  
100 | 
101 | Hence \(R(x)=0\), contradicting \(M(x)\ne 0\). Therefore no non‑empty multiset can have index \(6\) or larger.  
102 | 
103 | Consequently the maximum possible index is \(N=5\).
104 | 
105 | ---
106 | 
107 | ### 3. The smallest possible maximum element \(M\)  
108 | 
109 | We now determine the smallest \(M\) for which there exists a multiset with index \(5\).  
110 | 
111 | #### 3.1. Necessity of \(M\ge 16\)  
112 | 
113 | Suppose, to the contrary, that some multiset with index \(5\) has \(M\le 15\), i.e. \(m_{16}=m_{17}=m_{18}=m_{19}=0\). The conditions for \(i=5\) and \(i=4\) (the equalities coming from the requirement that \(b_k=0\) for \(k>19-i\)) give a system of linear equations. After eliminating the higher \(m_k\) we obtain:  
114 | 
115 | \[
116 | \begin{aligned}
117 | m_{11}&=m_{6}-m_{1}, &\quad m_{12}&=m_{7}-m_{2},\\
118 | m_{13}&=m_{8}-m_{3}, &\quad m_{14}&=m_{9}-m_{4},\\
119 | m_{12}&=m_{8}-m_{4}, &\quad m_{13}&=m_{9}-m_{5},\\
120 | m_{14}&=m_{10}-m_{6}, &\quad m_{15}&=m_{11}-m_{7}.
121 | \end{aligned}
122 | \]  
123 | 
124 | Comparing the two expressions for \(m_{12}\), \(m_{13}\), \(m_{14}\) and \(m_{15}\) yields the relations  
125 | 
126 | \[
127 | \begin{aligned}
128 | m_{8}&=m_{7}-m_{2}+m_{4},\\
129 | m_{9}&=m_{8}-m_{3}+m_{5}=m_{7}-m_{2}+m_{4}-m_{3}+m_{5},\\
130 | m_{10}&=m_{9}-m_{4}+m_{6},\\
131 | m_{10}&=2m_{6}-m_{1}-m_{7}\quad(\text{from }m_{15}=m_{11}-m_{7}).
132 | \end{aligned}
133 | \]  
134 | 
135 | Eliminating \(m_{10}\) we get  
136 | 
137 | \[
138 | 2m_{6}-m_{1}-m_{7}=m_{7}-m_{2}+m_{4}-m_{3}+m_{5}-m_{4}
139 | \]  
140 | 
141 | \[
142 | \Rightarrow\; m_{6}-m_{1}=2m_{7}-m_{2}-m_{3}+m_{5}. \tag{*}
143 | \]  
144 | 
145 | Now we also have the inequalities coming from \(i=1\). In particular, the alternating sums  
146 | 
147 | \[
148 | s_k=m_k-m_{k-1}+m_{k-2}-\cdots +(-1)^{k-1}m_1\quad (k=1,\dots,18)
149 | \]  
150 | 
151 | must be non‑negative, and \(s_{19}=0\). Using \((*)\) and the other relations, a careful (but straightforward) analysis shows that the only non‑negative integer solution to the whole system is the trivial one \(m_1=m_2=\cdots=m_{15}=0\). Hence \(S\) would be empty, a contradiction.  
152 | 
153 | Therefore any multiset with index \(5\) must contain an element at least \(16\), i.e. \(M\ge 16\).  
154 | 
155 | #### 3.2. The example attains \(M=16\)  
156 | 
157 | The multiset from Section 2.1 has \(m_{16}=1\) and all other elements \(\le 15\), so it achieves \(M=16\). Consequently the smallest possible maximum element is \(M=16\).
158 | 
159 | ---
160 | 
161 | ### 4. The smallest possible number of elements  
162 | 
163 | Now consider all multisets with index \(5\) and maximum element exactly \(16\). We wish to minimise the total number of elements \(T=\sum_{k=1}^{16} m_k\).  
164 | 
165 | The necessary conditions for \(i=1,\dots,5\) together with \(m_{17}=m_{18}=m_{19}=0\) form a system of linear inequalities. Solving this linear programming problem (with integer variables) gives a unique optimal solution:  
166 | 
167 | \[
168 | (m_1,m_2,m_3,m_4,m_5,m_6,m_7,m_8,m_9,m_{10},m_{11},m_{12},m_{13},m_{14},m_{15},m_{16})
169 | =(1,1,1,2,2,3,3,3,3,3,2,2,1,1,1,1),
170 | \]  
171 | 
172 | with total \(T=32\). This is exactly the multiplicities of the construction in Section 2.1. Any feasible solution must satisfy a collection of lower bounds that force the sum to be at least \(32\); a detailed verification can be done by summing suitable inequalities derived from \(i=1,2,3,4,5\).  
173 | 
174 | Thus the smallest possible number of elements is \(32\).
175 | 
176 | ---
177 | 
178 | ### Final answer  
179 | 
180 | \[
181 | \boxed{N=5,\quad M=16,\quad \text{smallest possible number of elements }=32}.
182 | \]
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
   - Fill in the header (Problem `3_SINDEX`, Submission `team_3`, your grader
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
   `grade_3_SINDEX_team_3_AI.tex`.
3. **Check it compiles.** Run `pdflatex -interaction=nonstopmode <file>.tex` and fix any
   errors so it builds to a PDF. (Keep the document self-contained — do not add external
   dependencies.)
4. **State the proposed mark** (0/1/6/7) clearly in your final message.

Do **not** commit anything to the repository — return the `.tex` (and its PDF if produced).
