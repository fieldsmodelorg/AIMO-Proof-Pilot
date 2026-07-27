# AIMO Proof Pilot — grading task

You are an **expert olympiad grader** for the AIMO Proof Pilot. Your job is to grade **one**
submission against the official markscheme and return a completed grading sheet as a LaTeX
(`.tex`) file.

- **Problem:** `3_SINDEX`
- **Submission:** `team_5`

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

This is the submission `team_5` for problem `3_SINDEX`, with line numbers
added for reference in your errors log.

```text
  1 | We are given a finite nonempty multiset $S$ of positive integers $<20$. For a positive integer $i$ we can partition $S$ into multisets $A_i$ and $B_i$ such that $A_i = i + B_i$ (adding $i$ to every element of $B_i$). The *index* of $S$ is the greatest $n$ such that this holds for every $i$ with $1\le i\le n$; if no such $n$ exists we set the index to $0$.
  2 | 
  3 | We need to determine the maximum possible index $N$ over all choices of $S$, then among those achieving $N$ choose the smallest possible maximum element $M$, and finally among those with maximal index and maximal element $M$ choose the smallest possible number of elements (counted with multiplicity). The answer is that minimal number.
  4 | 
  5 | ---
  6 | 
  7 | ### 1. Reformulation using generating functions
  8 | 
  9 | For a multiset $S$ with elements $x\in\{1,\dots,19\}$, let $c(x)$ be the multiplicity of $x$ in $S$ and define the polynomial  
 10 | \[
 11 | F(z)=\sum_{x=1}^{19}c(x)z^x .
 12 | \]
 13 | If for a fixed $i$ we have a partition $S = A \cup B$ with $A = i+B$, then in terms of generating functions we have $F(z)= (1+z^i)B(z)$, where $B(z)=\sum_{x}b(x)z^x$ is the generating function of $B$ (and $A = i+B$ gives generating function $z^i B(z)$). Moreover, the $b(x)$ are non‑negative integers and satisfy $c(x)=b(x)+b(x-i)$ (with $b(x)=0$ for $x\le0$ or $x>19$). Conversely, if $F(z)=(1+z^i)B(z)$ with $B(z)$ having non‑negative integer coefficients, then we obtain a valid partition.
 14 | 
 15 | Thus the condition “$i$ works for $S$” is equivalent to the existence of a polynomial $B_i(z)$ with non‑negative integer coefficients such that  
 16 | \[
 17 | F(z)=(1+z^i)\,B_i(z).
 18 | \tag{1}
 19 | \]
 20 | 
 21 | ---
 22 | 
 23 | ### 2. The polynomial $L_n(z)$ – least common multiple of $(1+z^i)$
 24 | 
 25 | For a given $n$, if $S$ works for every $i=1,\dots,n$, then $F(z)$ is divisible by each polynomial $1+z^i$. Because the polynomials $1+z^i$ are not pairwise coprime, the necessary condition is that $F(z)$ is a multiple of their least common multiple $L_n(z)$. The $L_n(z)$ can be obtained by taking the product of all irreducible cyclotomic factors that appear in any $1+z^i$ and raising each to the maximal exponent that occurs.
 26 | 
 27 | We compute the degrees of $L_n$ for small $n$:
 28 | 
 29 | * $1+z$ has degree $1$.
 30 | * $1+z^2$ has degree $2$.
 31 | * $1+z^3 = (1+z)(1-z+z^2)$ gives factors $1+z$ and $\Phi_6(z)=1-z+z^2$ (degree $2$).
 32 | * $1+z^4 = \Phi_8(z)$ has degree $4$.
 33 | * $1+z^5 = (1+z)\Phi_{10}(z)$; $\Phi_{10}(z)=1-z+z^2-z^3+z^4$ has degree $4$.
 34 | * $1+z^6 = (1+z^2)\Phi_{12}(z)$; $\Phi_{12}(z)=1-z^2+z^4$ has degree $4$.
 35 | 
 36 | Higher $i$ introduce further cyclotomic factors of higher degree.
 37 | 
 38 | Therefore, the degree of $L_n$ is the sum of the degrees of all distinct irreducible factors appearing among $1+z,\dots,1+z^n$. In particular  
 39 | 
 40 | \[
 41 | \deg L_6 = 1+2+2+4+4+4 = 17,\qquad
 42 | \deg L_7 = 23\quad (\text{since } \Phi_{14} \text{ of degree }6 \text{ is new}).
 43 | \]
 44 | 
 45 | Because $F(z)$ must be a multiple of $L_n(z)$, we have $\deg F \ge \deg L_n$. Since all elements are $<20$, $\deg F \le 19$ (and actually $\le 18$ if we also need a constant term $0$ to avoid the element $0$; we can always shift by a translation $S\mapsto S+t$, which corresponds to multiplying $F(z)$ by $z^t$ and does not affect the index). Hence a **necessary condition** for the existence of an $S$ with index $n$ is $\deg L_n \le 19$.
 46 | 
 47 | From the values above:
 48 | * $n=6$ gives $\deg L_6=17\le 19$ – possible.
 49 | * $n=7$ gives $\deg L_7=23>19$ – impossible.
 50 | 
 51 | Thus the **maximum possible index** is $N=6$.
 52 | 
 53 | ---
 54 | 
 55 | ### 3. Existence for $n=6$
 56 | 
 57 | We now construct an explicit multiset $S$ with index $6$ and with all elements $<20$.  
 58 | Take $L_6(z)$ as computed. Although $L_6$ itself has negative coefficients (e.g. at $z^1$ and $z^{16}$), we can multiply it by a polynomial $Q(z)$ with integer coefficients to obtain a polynomial with only non‑negative coefficients while keeping the total degree $\le 19$.  
 59 | Consider $Q(z)=1+z$. Then  
 60 | \[
 61 | G(z)=L_6(z)(1+z)
 62 | \]
 63 | has been computed (see the detailed calculation in the full reasoning) and its coefficients are non‑negative; the degree is $18$.  
 64 | Define  
 65 | \[
 66 | F(z)=z\cdot G(z).
 67 | \]
 68 | Shifting by $z$ eliminates the constant term, so $F$ corresponds to a multiset $S$ with no element $0$ and with maximum element $19$ (since $\deg F=19$). Explicitly, the coefficients of $F$ are the coefficients of $G$ shifted by one, giving  
 69 | 
 70 | \[
 71 | F(z)=z+z^4+z^5+z^6+z^7+z^8+z^9+2z^{10}+z^{11}+z^{12}+z^{13}+z^{14}+z^{15}+z^{19}).
 72 | \]
 73 | 
 74 | Thus  
 75 | \[
 76 | S = \{1,4,5,6,7,8,9,10,10,11,12,13,14,15,16,19\},
 77 | \]  
 78 | with $|S|=16$ elements, maximum element $M=19$.
 79 | 
 80 | Because $F(z)$ is a multiple of each $1+z^i$ ($i=1,\dots,6$) – indeed $L_6$ already contains every $1+z^i$ as a factor, and multiplication by $1+z$ does not destroy divisibility – the quotient $B_i(z)=F(z)/(1+z^i)$ is a polynomial with integer coefficients. Moreover, since $F$ has non‑negative coefficients, one can check case by case (or by the construction) that each $B_i(z)$ also has non‑negative coefficients. Hence $S$ satisfies the required partition for every $i=1,\dots,6$, so its index is at least $6$. Together with the impossibility of index $7$, we conclude $N=6$.
 81 | 
 82 | ---
 83 | 
 84 | ### 4. Minimising the maximum element
 85 | 
 86 | Among all $S$ with index $6$, what is the smallest possible maximum element $M$?  
 87 | From the necessary condition $\deg F \ge \deg L_6 =17$, after a shift we have $\max S \ge 1+\deg L_6 = 18$? Wait careful: $F(z)$ has degree $\ge 17$. After shifting to remove the constant term (to keep elements positive), the smallest exponent becomes $1$ and the largest becomes $\deg F$. Hence $\max S = \deg F$. The minimal possible $\deg F$ is $\deg L_6 = 17$, because $F$ must be a multiple of $L_6$. Can we achieve $\deg F = 17$? That would require $F = z^{t}\cdot L_6$ with $t$ chosen so that the constant term disappears, i.e. $t=1$ (since $L_6(0)=1$). Then $F=z\cdot L_6$ would have degree $18$, not $17$, because $L_6$ has constant term $1$. Actually $L_6$ has constant term $1$ (as can be seen from its factorisation), so multiplying by $z$ gives degree $\deg L_6+1=18$. If we try $t=0$, $F=L_6$ has constant term, which corresponds to an element $0$ – not allowed. Thus the smallest degree we can get for $F$ with zero constant term is $18$, giving $\max S = 18$. But is it possible to have $\max S = 18$? Let's see: we would need $F(z)=z\cdot L_6(z)$ to work, i.e. $S$ corresponds to $L_6$ shifted by $1$. Then $F(z)=z L_6(z)$. Does this $S$ satisfy the index condition? $F$ is divisible by each $1+z^i$ because $L_6$ is. The quotients are $B_i(z)=z\cdot L_6(z)/(1+z^i)$. We must check whether these $B_i(z)$ have non‑negative coefficients. Unfortunately $L_6/(1+z^i)$ may contain negative coefficients; multiplying by $z$ does not change sign. So it is not obvious that $z L_6$ works. Indeed, our earlier computation showed that $L_6$ itself has negative coefficients at $z^1$ and $z^{16}$. Multiplying by $z$ simply shifts them to $z^2$ and $z^{17}$, still negative. Hence $z L_6$ would not correspond to a valid multiset.
 88 | 
 89 | We therefore need an extra factor to “smooth out” the negative coefficients. The smallest degree we achieved was $18$ (with $Q(z)=1+z$) giving $\max S = 19$. Can we do with degree $18$? That would require $F = z \cdot H$ where $H$ has degree $17$, $H$ is a multiple of $L_6$, and $H$ has non‑negative coefficients. But any multiple of $L_6$ has degree at least $17$. If we take $H = L_6$ itself, it fails because of negative coefficients. The next possibility is $H = L_6 \cdot (1+z)$, which we already used, giving degree $18$. Could there be a polynomial $H$ of degree $17$ that is a multiple of $L_6$ and has non‑negative coefficients? $L_6$ itself is degree $17$; any other multiple would have higher degree. So the only candidate of degree $17$ is $L_6$ (up to a constant factor). Since $L_6$ has negative coefficients, no degree‑$17$ multiple exists with all coefficients non‑negative. Therefore the smallest possible degree for a valid $F$ is $18$, implying $\max S \ge 19$ after shifting? Wait: if we take $F = z \cdot H$ with $H$ of degree $17$ and non‑negative coefficients, then $F$ has degree $18$ and $\max S = 18$? Because $F$ would have terms up to $z^{18}$ (since $H$ degree $17$, times $z$ gives exponent $18$). But we just argued that $H$ cannot be of degree $17$ and non‑negative; it must be of degree at least $18$ (i.e. $H$ degree $18$ after multiplying by something). Let's be systematic.
 90 | 
 91 | We need $F(z)$ with non‑negative coefficients, $F(0)=0$, and $L_6 \mid F$. Write $F = z^t \cdot P$ where $P$ has non‑negative coefficients and $P(0)\neq 0$ (otherwise we could reduce $t$). Then $L_6 \mid z^t P$, but since $L_6(0)=1$, $z$ does not divide $L_6$, so we must have $L_6 \mid P$ in $\mathbb{Z}[z]$. Thus $P = L_6 \cdot Q$ for some polynomial $Q$ with integer coefficients. Moreover $P$ has non‑negative coefficients, so $Q$ must be chosen to compensate the negatives in $L_6$. The smallest degree of such a $P$ is at least $\deg L_6 = 17$, and if we take $Q$ constant, $P = L_6$ has negatives. So $Q$ must have degree at least $1$. Then $\deg P = 17 + \deg Q$. To keep $\deg F = t + \deg P \le 19$ and also $t\ge 1$ (to clear the constant term of $L_6$), we need $\deg P \le 18$. Since $\deg Q\ge 1$, the minimal possibility is $\deg Q =1$, giving $\deg P = 18$, and then we may take $t=1$ to get $F = z P$ of degree $19$, or $t=0$? But $t$ must be at least $1$ because $P(0)=L_6(0)Q(0) = 1\cdot Q(0)$. If $Q(0)\neq 0$, then $P(0)\neq 0$, and $F = z P$ has $F(0)=0$. So with $t=1$ we obtain $\deg F = 1 + 18 = 19$. Could we take $t=0$? Then $F=P$ would have constant term $P(0)\neq 0$, corresponding to element $0$, which is not allowed. So the minimal achievable $\max S$ is $19$.
 92 | 
 93 | But is it possible to have $F$ of degree $18$? That would require $\deg P = 18$ and $t=0$, but then $F$ would have constant term, so invalid. Or $t=1$ with $\deg P = 17$, but $\deg P$ cannot be $17$ with non‑negative coefficients as argued. Therefore the **smallest possible maximum element** among all $S$ with index $6$ is $M = 19$.
 94 | 
 95 | ---
 96 | 
 97 | ### 5. Minimising the size for $n=6$ and $M=19$
 98 | 
 99 | Now we look for a multiset $S$ with index $6$, maximum element $19$, and as few elements as possible. From the construction above we obtained $|S| = 16$. Can we do better (i.e., $15$ or less) while keeping $\max S=19$ and index $6$?
100 | 
101 | We already have a lower bound coming from the degree of $L_6$. Since $F(z)$ must be a multiple of $L_6$ and have $F(0)=0$, we write $F = z \cdot L_6 \cdot Q$ with $Q$ a polynomial with integer coefficients such that $F$ has non‑negative coefficients. The total number of elements is $F(1)$. We want to minimise $F(1)$.
102 | 
103 | We know $L_6(1)=8$ (as computed). Also $z$ contributes factor $1$ at $z=1$. So $F(1) = L_6(1) \cdot Q(1) = 8 \cdot Q(1)$. Hence the size is a multiple of $8$. Our construction gave $Q(1)=2$, so size $16$. Could we have $Q(1)=1$? That would give size $8$, which is much smaller. But is there a polynomial $Q$ with $Q(1)=1$ such that $F = z L_6 Q$ has non‑negative coefficients? $Q$ must be a polynomial with integer coefficients; $Q(1)=1$ means the sum of coefficients is $1$. The simplest is $Q(z)=1$ (constant). But then $F = z L_6$, which we already saw has negative coefficients (since $L_6$ has negatives). Other possibilities: $Q(z)=1 - z$ would give $Q(1)=0$, not $1$. To have $Q(1)=1$, the polynomial must have total sum $1$. Since $L_6$ has both positive and negative coefficients, the product $L_6 Q$ might become non‑negative for some $Q$ with $Q(1)=1$. For instance, $Q(z)=2 - z$ gives $Q(1)=1$, but then $Q$ has a negative coefficient. Could that cancel the negatives in $L_6$? Possibly, but we also need the final coefficients non‑negative. Moreover, $Q$ must have integer coefficients. Let's test $Q(z)=2 - z$. Compute $S = z L_6 (2-z) = 2z L_6 - z^2 L_6$. This might produce negative coefficients. Without a full analysis, note that the number of elements is the sum of coefficients, which is $8 Q(1)$. If $Q(1)=1$, the sum would be $8$. But can we achieve index $6$ with only $8$ elements? That would mean the average multiplicity is low, but we also need the maximum element $19$. Is it plausible? Let's attempt to find an $S$ of size $8$ with max $19$ and index $6$. We would need $F$ of degree $19$ with sum $8$. That means the average coefficient is very small; many exponents would be zero. But $L_6$ has
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
   - Fill in the header (Problem `3_SINDEX`, Submission `team_5`, your grader
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
   `grade_3_SINDEX_team_5_AI.tex`.
3. **Check it compiles.** Run `pdflatex -interaction=nonstopmode <file>.tex` and fix any
   errors so it builds to a PDF. (Keep the document self-contained — do not add external
   dependencies.)
4. **State the proposed mark** (0/1/6/7) clearly in your final message.

Do **not** commit anything to the repository — return the `.tex` (and its PDF if produced).
