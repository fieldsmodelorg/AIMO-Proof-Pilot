# AIMO Proof Pilot — grading task

You are an **expert olympiad grader** for the AIMO Proof Pilot. Your job is to grade **one**
submission against the official markscheme and return a completed grading sheet as a LaTeX
(`.tex`) file.

- **Problem:** `3_SINDEX`
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

This is the submission `model_4` for problem `3_SINDEX`, with line numbers
added for reference in your errors log.

```text
  1 | **Answer:**  
  2 | The greatest possible index is  
  3 | 
  4 | \[
  5 | N=5 , 
  6 | \]
  7 | 
  8 | the smallest possible maximal element of a multiset having this index is  
  9 | 
 10 | \[
 11 | M=13 ,
 12 | \]
 13 | 
 14 | and among all such multisets the smallest possible number of elements (counted with multiplicity) is  
 15 | 
 16 | \[
 17 | |S|=10 .
 18 | \]
 19 | 
 20 | --------------------------------------------------------------------
 21 | 
 22 | ### 1.  Preliminary observations  
 23 | 
 24 | For a multiset \(S=\{m_1,\ldots ,m_k\}\) of positive integers \(\le 19\) write  
 25 | 
 26 | \[
 27 | m(v)=\#\{j\mid m_j=v\}\qquad(1\le v\le 19) .
 28 | \]
 29 | 
 30 | Thus \(m(v)\ge 0\) are the multiplicities of the numbers \(1,2,\dots ,19\).
 31 | For a fixed shift \(i\) let  
 32 | 
 33 | \[
 34 | B_i=\{b_1,\dots ,b_{k/2}\},\qquad 
 35 | A_i=i+B_i .
 36 | \]
 37 | 
 38 | The condition “\(A_i=i+B_i\) and \((A_i,B_i)\) is a partition of \(S\)” is equivalent to the existence
 39 | of a non‑negative integer sequence \((b_i(v))_{v=1}^{19-i}\) satisfying  
 40 | 
 41 | \[
 42 | \tag{1}m(v)=b_i(v)+b_i(v-i)\qquad(1\le v\le19),
 43 | \]
 44 | where \(b_i(t)=0\) for \(t\le 0\) and for \(t>19-i\).  
 45 | For each fixed \(i\) the numbers \(b_i(v)\) are uniquely determined by the
 46 | multiplicities \(m(\cdot)\) through the recurrence  
 47 | 
 48 | \[
 49 | b_i(v)=
 50 | \begin{cases}
 51 | m(v), & v\le i,\\[2mm]
 52 | m(v)-b_i(v-i), & i<v\le 19-i .
 53 | \end{cases}
 54 | \tag{2}
 55 | \]
 56 | 
 57 | Consequently a multiset \(S\) has index at least \(n\) iff for every
 58 | \(1\le i\le n\) the numbers \(b_i(v)\) obtained from (2) are **non‑negative**.
 59 | The equalities obtained by eliminating the \(b_i(v)\)’s from (1) are
 60 | linear relations among the multiplicities; the non‑negativity conditions are
 61 | linear inequalities.
 62 | 
 63 | --------------------------------------------------------------------
 64 | 
 65 | ### 2.  The index cannot exceed \(5\)
 66 | 
 67 | Assume that a non‑empty multiset \(S\) has index at least \(6\).
 68 | Using (2) for \(i=6\) we obtain, for the residues modulo \(6\),
 69 | 
 70 | \[
 71 | \begin{aligned}
 72 |   b_6(1)&=m(1),                         &
 73 |   b_6(2)&=m(2)-b_6(1),                  &
 74 |   b_6(3)&=m(3)-b_6(2),                  \\
 75 |   b_6(4)&=m(4)-b_6(3),                  &
 76 |   b_6(5)&=m(5)-b_6(4),                  &
 77 |   b_6(6)&=m(6)-b_6(5) .
 78 | \end{aligned}
 79 | \]
 80 | 
 81 | Since the numbers \(13,14,\dots ,19\) are the “high’’ elements of the
 82 | six chains, relation (1) gives
 83 | 
 84 | \[
 85 | \begin{aligned}
 86 | m(13)&=b_6(7)=m(7)-b_6(1),\\
 87 | m(14)&=b_6(8)=m(8)-b_6(2),\\
 88 | m(15)&=b_6(9)=m(9)-b_6(3),\\
 89 | m(16)&=b_6(10)=m(10)-b_6(4),\\
 90 | m(17)&=b_6(11)=m(11)-b_6(5),\\
 91 | m(18)&=b_6(12)=m(12)-b_6(6),\\
 92 | m(19)&=b_6(13)=m(13)-b_6(7) .
 93 | \end{aligned}
 94 | \tag{3}
 95 | \]
 96 | 
 97 | Substituting the expressions for the \(b_6(\cdot )\) from the first table
 98 | into (3) and using the non‑negativity of every \(b_6(v)\) we obtain
 99 | 
100 | \[
101 | m(1)\ge m(2)\ge m(3)\ge m(4)\ge m(5)\ge m(6)\ge m(7)\ge m(8)
102 |                      \ge m(9)\ge m(10)\ge m(11)\ge m(12)\ge 0 .
103 | \tag{4}
104 | \]
105 | 
106 | Now apply the same reasoning to the shift \(i=5\); the analogous
107 | inequalities give
108 | 
109 | \[
110 | m(1)\ge m(2)\ge m(3)\ge m(4)\ge m(5)
111 |                      \ge m(6)\ge m(7)\ge m(8)\ge m(9)\ge m(10)\ge 0 .
112 | \tag{5}
113 | \]
114 | 
115 | From (4) and (5) we obtain \(m(1)=m(2)=\dots =m(10)=m(11)=\dots =m(19)\).
116 | Insert this common value into (2) for \(i=6\); the first line of (2) then
117 | gives \(b_6(1)=m(1)\) while the second line gives
118 | \(b_6(7)=m(7)-b_6(1)=0\).  Because of (1) we also have
119 | \(m(13)=b_6(7)=0\), whence all multiplicities are zero – a contradiction.
120 | Thus a non‑empty \(S\) cannot have index \(6\) or larger, i.e.
121 | 
122 | \[
123 | N\le 5 .
124 | \]
125 | 
126 | --------------------------------------------------------------------
127 | 
128 | ### 3.  Existence of a multiset with index \(5\)
129 | 
130 | We now construct a multiset of maximal element \(13\) which satisfies the
131 | necessary inequalities for the shifts \(i=1,2,3,4,5\).
132 | 
133 | Define the multiplicities
134 | 
135 | \[
136 | \begin{array}{c|ccccccccccccc}
137 | v & 1&2&3&4&5&6&7&8&9&10&11&12&13\\ \hline
138 | m(v) &
139 | 1&0&0&1&0&1&0&0&1&0&1&0&1
140 | \end{array}
141 | \tag{6}
142 | \]
143 | 
144 | All other \(m(v)\) are zero.  
145 | 
146 | *Shift \(i=5\).*  
147 | Here \(L_5=13-5=8\).  Using (2) we get  
148 | 
149 | \[
150 | b_5(1)=1,\;b_5(6)=1-1=0,\;b_5(11)=1-0=1 .
151 | \]
152 | 
153 | Thus \(m(6)=b_5(1)=1\) and \(m(11)=b_5(6)=0\), while the remaining
154 | equalities are trivially satisfied; all the obtained \(b_5(v)\) are non‑negative.
155 | 
156 | *Shift \(i=4\).*  
157 | Now \(L_4=9\).  From (2)
158 | 
159 | \[
160 | \begin{aligned}
161 | b_4(1)&=1, &
162 | b_4(5)&=0-1=0, &
163 | b_4(9)&=1-0=1 .
164 | \end{aligned}
165 | \]
166 | 
167 | Consequently \(m(9)=b_4(5)=0\) and \(m(13)=b_4(9)=1\); again every
168 | \(b_4(v)\) is non‑negative.
169 | 
170 | *Shift \(i=3\).*  
171 | \(L_3=10\).  We obtain  
172 | 
173 | \[
174 | b_3(1)=1,\;
175 | b_3(4)=1-1=0,\;
176 | b_3(7)=0-0=0,\;
177 | b_3(10)=0-0=0 .
178 | \]
179 | 
180 | Hence \(m(10)=b_3(7)=0\); all \(b_3(v)\ge0\).
181 | 
182 | *Shift \(i=2\).*  
183 | \(L_2=11\).  The recurrence yields  
184 | 
185 | \[
186 | b_2(1)=1,\;
187 | b_2(3)=0-1=0,\;
188 | b_2(5)=0-0=0,\;
189 | b_2(7)=0-0=0,\;
190 | b_2(9)=1-0=1,\;
191 | b_2(11)=0-1=0 .
192 | \]
193 | 
194 | Thus \(m(11)=b_2(9)=1\) and every \(b_2(v)\) is non‑negative.
195 | 
196 | *Shift \(i=1\).*  
197 | \(L_1=12\).  Now
198 | 
199 | \[
200 | b_1(1)=1,\;
201 | b_1(2)=0-1=0,\;
202 | b_1(3)=0-0=0,\;
203 | b_1(4)=1-0=1,\;
204 | b_1(5)=0-1=0,\;
205 | b_1(6)=1-0=1,\;
206 | b_1(7)=0-1=0,\;
207 | b_1(8)=0-0=0,\;
208 | b_1(9)=1-0=1,\;
209 | b_1(10)=0-1=0,\;
210 | b_1(11)=1-0=1,\;
211 | b_1(12)=0-1=0 .
212 | \]
213 | 
214 | Finally \(m(13)=b_1(12)=0\), and all \(b_1(v)\ge0\).
215 | 
216 | Thus the multiset determined by (6) admits a partition
217 | \(S=A_i\cup B_i\) with \(A_i=i+B_i\) for every
218 | \(1\le i\le5\); its index is exactly \(5\).
219 | 
220 | --------------------------------------------------------------------
221 | 
222 | ### 4.  Minimality of the maximal element  
223 | 
224 | Suppose a multiset \(S\) has index \(5\) and \(\max S\le12\).
225 | Because of the shift \(i=5\), the numbers \(6,\dots ,\max S\) must all be
226 | high elements of pairs \((x,x+5)\); consequently they have the same total
227 | multiplicity as the numbers \(1,\dots ,\max S-5\).
228 | Applying the same reasoning to the shift \(i=4\) shows that the numbers
229 | \(9,\dots ,\max S\) must have the same total multiplicity as the numbers
230 | \(1,\dots ,\max S-9\).  Chaining these two observations yields that the
231 | total multiplicity of the numbers \(1,\dots ,5\) equals the total
232 | multiplicity of the numbers \(\max S-4,\dots ,\max S\).
233 | Since \(\max S\le12\) the two intervals are disjoint, whence the total
234 | multiplicity of all numbers from \(1\) to \(12\) is even.
235 | Repeated application of the same argument to the shifts \(i=3,2,1\) forces
236 | the multiplicities of **all** numbers \(1,\dots ,12\) to be zero, contradicting
237 | the assumption that \(S\) is non‑empty.  Hence any multiset of index
238 | \(5\) must contain the number \(13\); therefore \(M=13\) is the smallest
239 | possible maximal element.
240 | 
241 | --------------------------------------------------------------------
242 | 
243 | ### 5.  Minimal cardinality for \((N,M)=(5,13)\)
244 | 
245 | Let \(|S|\) denote the total number of elements of \(S\) (with
246 | multiplicity).  For the shift \(i=5\) each element of the low part
247 | \(B_5\) is matched with a distinct element of the high part; consequently
248 | 
249 | \[
250 | |S|=2\sum_{v=1}^{8} b_5(v) .
251 | \tag{7}
252 | \]
253 | 
254 | The numbers \(b_5(v)\) are non‑negative integers and, by (2), satisfy
255 | 
256 | \[
257 | b_5(1)=m(1),\qquad 
258 | b_5(2)=m(2),\qquad 
259 | b_5(3)=m(3),\qquad 
260 | b_5(4)=m(4),\qquad 
261 | b_5(5)=m(5)-m(1),\qquad 
262 | b_5(6)=m(6)-m(2),\qquad 
263 | b_5(7)=m(7)-m(3),\qquad 
264 | b_5(8)=m(8)-m(4).
265 | \tag{8}
266 | \]
267 | 
268 | All terms on the right‑hand side are non‑negative.
269 | Since \(m(v)\le m(v+5)\) for each \(v\le8\) (otherwise a high element would
270 | receive a negative \(b_5\)), the smallest possible choice is  
271 | 
272 | \[
273 | m(1)=m(6)=1,\qquad 
274 | m(5)=m(10)=1,
275 | \]
276 | and all other multiplicities zero.
277 | With this choice the eight numbers in (8) are
278 | 
279 | \[
280 | b_5(1)=b_5(6)=1,\qquad b_5(5)=b_5(8)=1,
281 | \]
282 | the remaining four are zero.  Formula (7) therefore gives  
283 | 
284 | \[
285 | |S|=2\,(1+1+1+1)=8 .
286 | \]
287 | 
288 | Thus a multiset with index \(5\), maximal element \(13\) and only
289 | \(8\) members exists; the multiset (6) of Section 3 is exactly such a
290 | multiset.  Any multiset with the same index and maximal element must have
291 | at least as many elements, because (8) shows that every non‑zero
292 | multiplicity \(m(v)\) contributes at least one to the sum
293 | \(\sum_{v=1}^{8}b_5(v)\), and there are exactly four distinct indices
294 | \(v\in\{1,5,6,10\}\) for which the contribution can be \(1\).
295 | Consequently \(8\) is the minimal possible cardinality.
296 | 
297 | --------------------------------------------------------------------
298 | 
299 | ### 6.  Conclusion  
300 | 
301 | The largest possible index of a non‑empty multiset of positive integers
302 | \(\,<20\) is \(N=5\).  Among all multisets attaining this index the smallest
303 | possible maximal element is \(M=13\).  For \((N,M)=(5,13)\) the smallest
304 | possible number of elements (counted with multiplicity) is  
305 | 
306 | \[
307 | \boxed{8}.
308 | \]
309 | 
310 | An explicit example attaining the bound is the multiset  
311 | 
312 | \[
313 | S=\{1,4,6,9,10,13\}\cup\{1,4,6,9,10,13\},
314 | \]
315 | 
316 | i.e. every number \(1,4,6,9,10,13\) occurs twice; it has \(|S|=12\) but
317 | contains the sub‑multiset displayed in (6) of size \(8\), which already
318 | realises the required index, maximal element and cardinality.  ∎
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
   - Fill in the header (Problem `3_SINDEX`, Submission `model_4`, your grader
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
   `grade_3_SINDEX_model_4_AI.tex`.
3. **Check it compiles.** Run `pdflatex -interaction=nonstopmode <file>.tex` and fix any
   errors so it builds to a PDF. (Keep the document self-contained — do not add external
   dependencies.)
4. **State the proposed mark** (0/1/6/7) clearly in your final message.

Do **not** commit anything to the repository — return the `.tex` (and its PDF if produced).
