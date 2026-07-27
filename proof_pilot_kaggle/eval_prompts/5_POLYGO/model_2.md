# AIMO Proof Pilot — grading task

You are an **expert olympiad grader** for the AIMO Proof Pilot. Your job is to grade **one**
submission against the official markscheme and return a completed grading sheet as a LaTeX
(`.tex`) file.

- **Problem:** `5_POLYGO`
- **Submission:** `model_2`

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
\section*{Problem 5 (POLYGO)}


\problem[4]{%
A polynomial $P(x)$ is called \emph{good} if it has integer coefficients and:
\begin{itemize}
    \item It is a monic polynomial of degree 7;
    \item The absolute values of all of the coefficients of $P$ are odd and strictly less than $2025^2$;
    \item The absolute values of all the coefficients of $P$ are roots of $P$.
\end{itemize}
How many good polynomials are there?
}{6150968}

\vspace{2cm}

\textbf{Original AIMO3 Formulation:} 

A polynomial $P(x)$ is called \emph{good} if it has integer coefficients and:
\begin{itemize}
    \item It is a monic polynomial of degree 7;
    \item The absolute values of all of the coefficients of $P$ are odd and strictly less than $2025^2$;
    \item The absolute values of all the coefficients of $P$ are roots of $P$.
\end{itemize}
There are $N$ good polynomials. What is the remainder when $N$ is divided by $10^{5}$?

\textbf{Answer:} 50968

\vspace{1cm}

\textbf{Remark:} Relative to the AIMO3 version, we removed the modulo $10^5$ answer modification as we are not restricted to $5$-digit answers in the Proof Pilot.

\clearpage

\polishedsolution[SB][4]{%
Write
\begin{equation*}
    P(x)=x^7+a_6x^6+a_5x^5+a_4x^4+a_3x^3+a_2x^2+a_1x+a_0,
\end{equation*}
and put $M=2025^2$. Let $N$ be the largest absolute value of any coefficient of $P$, including the leading coefficient. Then $N$ is odd, $1\leq N<M$, and both $1$ and $N$ are roots of $P$.

First suppose $N=1$. Then each of $a_0,a_1,\ldots,a_6$ is equal to $1$ or $-1$. Since $1$ is a root,
\begin{equation*}
    0=P(1)=1+a_6+a_5+\cdots+a_0.
\end{equation*}
Thus exactly three of $a_0,a_1,\ldots,a_6$ are equal to $1$, and the remaining four are equal to $-1$. This gives
\begin{equation*}
    \binom{7}{3}=35
\end{equation*}
polynomials.

We present two approaches for classifying the cases where $N \geq 3$.

\underline{Approach 1: Right to Left}

We determine the coefficients in pairs, starting from the constant term. We shall repeatedly use the following simple observation: if $b$ is odd, $|b|\leq N$, $\varepsilon\in\{\pm1\}$, and
\begin{equation*}
    b+\varepsilon\equiv 0\pmod N,
\end{equation*}
then $b=-\varepsilon$. Indeed, $b+\varepsilon$ is even and has absolute value at most $N+1<2N$, while the only multiples of the odd number $N$ in this range are $-N,0,N$, of which only $0$ is even.

Since $P(N)=0$, reducing modulo $N$ gives $a_0\equiv0\pmod N$. As $0<|a_0|\leq N$ and is odd, we have $a_0=\varepsilon_0N$ for some $\varepsilon_0\in\{\pm1\}$. Dividing $P(N)=0$ by $N$ and reducing modulo $N$ gives
\begin{equation*}
    a_1+\varepsilon_0\equiv0\pmod N,
\end{equation*}
so by the observation $a_1=-\varepsilon_0$. Hence
\begin{equation*}
    a_1\in\{\pm1\},\quad a_0=-a_1N.
\end{equation*}

The same argument may now be repeated after deleting this cancelling pair. Since $a_1N+a_0=0$, dividing the remaining equation by $N^2$ gives
\begin{equation*}
    0=N^5+a_6N^4+a_5N^3+a_4N^2+a_3N+a_2.
\end{equation*}
Applying the same two congruence steps gives
\begin{equation*}
    a_3\in\{\pm1\},\quad a_2=-a_3N.
\end{equation*}
Deleting this pair and dividing by $N^4$ leaves
\begin{equation*}
    0=N^3+a_6N^2+a_5N+a_4,
\end{equation*}
so similarly
\begin{equation*}
    a_5\in\{\pm1\},\quad a_4=-a_5N.
\end{equation*}
Finally the remaining part of $P(N)=0$ is $N^7+a_6N^6=0$, so $a_6=-N$.

Therefore every good polynomial with $N\geq3$ has the form
\begin{equation*}
    P(x)=x^7-Nx^6+s_1(x^5-Nx^4)+s_2(x^3-Nx^2)+s_3(x-N),
\end{equation*}
where $s_1,s_2,s_3\in\{\pm1\}$. Since $1$ is a root,
\begin{equation*}
    0=P(1)=(1-N)(1+s_1+s_2+s_3).
\end{equation*}
As $N>1$, this is equivalent to
\begin{equation*}
    s_1+s_2+s_3=-1.
\end{equation*}
Thus exactly one of $s_1,s_2,s_3$ is $1$ and the other two are $-1$. There are $3$ ways to assign these values. 

Conversely, for every odd integer $N$ with $3\leq N<M$, every polynomial of the displayed form with exactly one of $s_1,s_2,s_3$ equal to $1$ is good: its coefficient absolute values are just $1$ and $N$, the equation $P(N)=0$ follows from the cancellation in each block, and $P(1)=0$ follows from $1+s_1+s_2+s_3=0$.

It remains to count the possible values of $N$. Since the coefficient absolute values must be strictly less than $M=2025^2$, and $M$ is odd, the odd values with $N\geq3$ are
\begin{equation*}
    3,5,7,\ldots,M-2,
\end{equation*}
so there are $(M-3)/2$ choices.


\underline{Approach 2: Left to Right}

We begin with the observation that for any positive integer $t$
\begin{equation}
    \label{eq:Eqn1}
    N^t+N^{t-1}+\cdots+N+1=N^{t}+\frac{N^t-1}{N-1}<2N^t. \tag{$\ast$}
\end{equation}
We also note that, from the third condition, $P(N)=0$. If $a_6 \geq 2-N$ then
\begin{align*}
    0=P(N) &=N^7+a_6 N^6+a_5 N^5+\cdots+a_1 N+a_0  \\
    & \geq N^7+(2-N) N^6-N \cdot N^5-\cdots-N \cdot N-N \\ 
    &=2N^6-N \cdot \underbrace{\left(N^5+N^4+\cdots+1\right)}_{<2N^5 \; \text{by \eqref{eq:Eqn1}}} \\
    &>2N^6-N\left(2N^5\right)=0
\end{align*}
which is a contradiction. Thus, $a_6$ is equal to either $1-N$ or $-N$. As $N$ and $a_6$ are both odd, it follows that $a_6=-N$. 

Now we have 
\begin{equation*}
    0=P(N)=N^7-N \cdot N^6+a_5 N^5+\cdots+a_1 N+a_0=a_5 N^5+\cdots+a_1 N+a_0.
\end{equation*}
Subtracting $a_5 N^5$ from both sides and applying the triangle inequality
\begin{align*}
    \left\lvert -a_5 N^5\right\rvert=\left\lvert a_5 \right\rvert N^5
    &=
    \left\lvert a_4 N^4+\cdots+a_1 N+a_0 \right\rvert \\
    & \leq \left\lvert a_4\right\rvert N^4+\cdots+\left\lvert a_1\right\rvert N+\left\lvert a_0\right\rvert  \\
    & \leq N \cdot N^4+\cdots+N \cdot N+N \\
    & < N \left(2N^4\right)=2N^5 \tag{By \eqref{eq:Eqn1}}
    .
\end{align*}
Thus, $\left\lvert a_5\right\rvert<2$ which means, since $a_5$ is odd, that $a_5=\pm 1$. Noting that 
\begin{equation*}
    0=P(N)=a_5 N^5+a_4 N^4+\cdots+a_1N+a_0=\pm \left(N^5 \pm a_4 N^4+\cdots \pm a_1 N \pm a_0\right)
\end{equation*}
we can repeat the argument from above (for $a_6=-N$) to get $\pm a_4=-N$ so $a_4=-a_5N$. We then have
\begin{equation*}
    0=P(N)=a_5 N^5-\left(a_5N\right)N^4+a_3N^3+\cdots+a_1N+a_0=a_3N^3+\cdots+a_1N+a_0.
\end{equation*}
Again, we can repeat the argument that gave $a_5=\pm 1$ and $a_4=-a_5N$ to get $a_3=\pm 1$ and $a_2=-a_3N$. 

Lastly, we note that $0=P(N)=a_1N+a_0$ so, by the same argument, $a_1=\pm 1$ and $a_0=-a_1N$. Putting these all together we have
\begin{equation*}
    P(x)=x^7-Nx^6 \pm \left(x^5-Nx^4\right) \pm \left(x^3-Nx^2\right) \pm \left(x-N\right).
\end{equation*}
The count is then the same as the first approach. 

Combining with the $35$ choices for $P$ when $N=1$, we get
\begin{equation*}
    35+3 \cdot \frac{M-3}{2}=\frac{3M+61}{2}
\end{equation*}
choices for $P$ in total. Substituting in $M=2025^2$, we get the answer
\begin{equation*}
    \frac{3 \cdot 2025^2+61}{2}=\boxed{6150968}.
\end{equation*}
}

\clearpage

\markscheme{%
A solution is \emph{essentially complete} if, for $N \geq 3$, it shows that any good $P$ has the form
\begin{equation*}
    P(x)=x^7-Nx^6 \pm \left(x^5-Nx^4\right) \pm \left(x^3-Nx^2\right) \pm \left(x-N\right)
\end{equation*}
where $N$ is the largest absolute value of a coefficient. 

Any solution that fails to then reduce this to the correct count of good polynomials will score $6$. 

We will not penalise arithmetic errors in computing the final answer (e.g. if there is a correct proof that there are $\frac{3M+61}{2}$ good polynomials but the calculation goes wrong when substituting in $2025^2$).

Other examples of minor errors or omissions that would result in a score of $6$ include:
\begin{enumerate}[label=(ME\arabic*)]
    \item Using $N\leq2025^2$ instead of $N<2025^2$ in the final count, thereby allowing the inadmissible value $N=2025^2$.
    \item Counting the odd values of $N\geq3$ as $(M-1)/2$ rather than $(M-3)/2$, where $M=2025^2$.
    \item Omitting the $N=1$ case, or counting it in a way that is not a minor arithmetic slip.
    \item Failing to impose $P(1)=0$ on the three signs, for example giving $8$ sign choices instead of $3$.
    \item Not checking the converse direction when the construction is not already visibly reversible.
\end{enumerate}

The following should \emph{not} generally be penalised:
\begin{enumerate}[label=(NME\arabic*)]
    \item A simple arithmetic slip in evaluating $2025^2$ or the final division, provided the correct expression $35+3(M-3)/2$ or $(3M+61)/2$ has been obtained.
    \item Not explicitly stating that $M=2025^2$ is odd, if the subsequent range $3,5,\ldots,M-2$ is counted correctly.
    \item A very brief converse check, provided it clearly notes that the only coefficient absolute values in the constructed polynomial are $1$ and $N$ and that both are roots.
\end{enumerate}
}{%
An incomplete solution scores $1$ mark if it makes a correct, non-trivial structural deduction in the case $N\geq3$. Any one of the following is sufficient:
\begin{enumerate}[label=(PP\arabic*)]
    \item Proving that $a_6=-N$.
    \item Proving that $a_0=\pm N$ \textbf{and} $a_1=\mp 1$ (where the sign choices are opposite).
    \item Proving any full adjacent pair relation, such as $a_4=-a_5N$ with $a_5\in\{\pm1\}$.
\end{enumerate}

\clearpage

The following do \emph{not} by themselves constitute partial progress:
\begin{enumerate}[label=(NPP\arabic*)]
    \item Counting the $N=1$ case only.
    \item Merely observing that $P(1)=0$ or $P(N)=0$.
    \item Making claims that $a_6=-N$ or $a_0=\pm N$ without proof.
    \item Finding the correct numerical answer by search, guessing, or pattern-spotting without a proof of the main structure.
    \item Counting sign patterns for the block form when the block form has not been justified.
\end{enumerate}
}
```

---

## Submission to grade

This is the submission `model_2` for problem `5_POLYGO`, with line numbers
added for reference in your errors log.

```text
  1 | The polynomial is monic degree 7, so write
  2 | \[
  3 | P(x)=x^{7}+a_{6}x^{6}+a_{5}x^{5}+a_{4}x^{4}+a_{3}x^{3}+a_{2}x^{2}+a_{1}x+a_{0},
  4 | \]
  5 | with integer coefficients \(a_i\).  
  6 | Conditions:  
  7 | - \(a_i\) are odd, \(|a_i|<2025^{2}\) for \(i=0,\dots,6\); leading coefficient 1 also satisfies \(|1|=1\) odd and \(<2025^{2}\).  
  8 | - For each coefficient (including the leading one) its absolute value is a root of \(P\).  
  9 | In particular \(1\) (absolute value of leading coefficient) is a root, so \(P(1)=0\):
 10 | \[
 11 | 1+\sum_{i=0}^{6}a_i=0\quad\Longrightarrow\quad \sum_{i=0}^{6}a_i=-1.\tag{1}
 12 | \]
 13 | Define \(t_i=|a_i|>0\) (odd). Then the condition gives \(P(t_i)=0\) for each \(i=0,\dots,6\) as well.  
 14 | By the rational root theorem any integer root divides the constant term, hence \(t_i\mid a_0\) for all \(i\). Therefore \(t_0=|a_0|\) and each \(t_i\) is a positive odd divisor of \(t_0\).
 15 | 
 16 | We split into two cases.
 17 | 
 18 | ---
 19 | 
 20 | ### Case 1: \(t_0=1\)  
 21 | Then \(a_0=\pm1\) and every \(t_i\mid 1\) forces \(t_i=1\). Hence all coefficients (except the leading 1) are \(\pm1\).  
 22 | Equation (1) becomes \(1+\sum_{i=0}^{6}\varepsilon_i=0\), where \(\varepsilon_i=\pm1\) is the sign of \(a_i\). Thus \(\sum_{i=0}^{6}\varepsilon_i=-1\), i.e. among the seven coefficients \(a_0,\dots,a_6\) exactly three are \(+1\) and four are \(-1\). The number of such sign choices is \(\binom{7}{3}=35\).  
 23 | Each such polynomial satisfies \(P(1)=0\) (so \(1\) is a root) and every coefficient has absolute value \(1\) which is a root; the other conditions (odd, \(<2025^{2}\)) are clearly satisfied. Hence there are \(35\) good polynomials with \(t_0=1\).
 24 | 
 25 | ---
 26 | 
 27 | ### Case 2: \(t_0>1\)  
 28 | Now \(t_0\) is odd and \(>1\). Write \(a_i=\varepsilon_i t_i\) with \(\varepsilon_i=\pm1\) (so \(t_i=|a_i|\)). The conditions give
 29 | \[
 30 | \sum_{i=0}^{6}\varepsilon_i t_i = -1,\tag{2}
 31 | \]
 32 | \[
 33 | \sum_{i=0}^{6}\varepsilon_i t_i\,t_0^{\,i} = -t_0^{7}.\tag{3}
 34 | \]
 35 | Because \(t_i\mid t_0\), each \(t_i\) is either \(1\) or a proper divisor of \(t_0\) or \(t_0\) itself.  
 36 | Manipulate (3) step by step using increasing powers of \(t_0\) to show that the only possibility is:
 37 | \(t_i=t_0\) for even \(i\) and \(t_i=1\) for odd \(i\), together with precise sign relations.
 38 | 
 39 | *Step 1:* Divide (3) by \(t_0\):
 40 | \[
 41 | \varepsilon_0 + \varepsilon_1 t_1 + \sum_{i=2}^{6}\varepsilon_i t_i t_0^{\,i-1} = -t_0^{6}.
 42 | \]
 43 | Modulo \(t_0\) the sum for \(i\ge2\) vanishes; thus \(\varepsilon_0+\varepsilon_1 t_1\equiv0\pmod{t_0}\). Since \(t_1\mid t_0\) and \(t_0>1\), the only possibility is \(t_1=1\) and \(\varepsilon_1=-\varepsilon_0\). (Otherwise \(|t_1|>1\) gives a contradiction because \(|\varepsilon_0+\varepsilon_1 t_1|\) would be smaller than \(t_0\) and not a multiple of \(t_0\).)  
 44 | Hence \(t_1=1\), \(\varepsilon_1=-\varepsilon_0\).
 45 | 
 46 | *Step 2:* Insert this into (3). The terms for \(i=0,1\) become \(\varepsilon_0 t_0 + (-\varepsilon_0)t_0=0\). So (3) reduces to
 47 | \[
 48 | \sum_{i=2}^{6}\varepsilon_i t_i t_0^{\,i} = -t_0^{7}.
 49 | \]
 50 | Divide by \(t_0\):
 51 | \[
 52 | \varepsilon_2 t_2 + \varepsilon_3 t_3 t_0 + \varepsilon_4 t_4 t_0^{2} + \varepsilon_5 t_5 t_0^{3} + \varepsilon_6 t_6 t_0^{4} = -t_0^{5}. \tag{4}
 53 | \]
 54 | Reduce (4) modulo \(t_0\): the terms for \(i\ge3\) contain a factor \(t_0\), so \(\varepsilon_2 t_2\equiv0\pmod{t_0}\).  
 55 | As before, because \(t_2\mid t_0\) and \(t_0>1\), this forces \(t_2=t_0\) (and \(\varepsilon_2\) free). Thus \(t_2=t_0\).
 56 | 
 57 | *Step 3:* Substitute \(t_2=t_0\) into (4) and divide by \(t_0\):
 58 | \[
 59 | \varepsilon_2 + \varepsilon_3 t_3 + \varepsilon_4 t_4 t_0 + \varepsilon_5 t_5 t_0^{2} + \varepsilon_6 t_6 t_0^{3} = -t_0^{4}. \tag{5}
 60 | \]
 61 | Modulo \(t_0\) we get \(\varepsilon_2+\varepsilon_3 t_3\equiv0\pmod{t_0}\).  
 62 | Arguing as before, this forces \(t_3=1\) and \(\varepsilon_3=-\varepsilon_2\). (Any proper divisor would give a non‑zero residue of absolute value less than \(t_0\); \(t_3=t_0\) would lead to \(\varepsilon_2\equiv0\) impossible.)  
 63 | Hence \(t_3=1\), \(\varepsilon_3=-\varepsilon_2\).
 64 | 
 65 | *Step 4:* With these values the left side of (5) simplifies: \(\varepsilon_2+\varepsilon_3 t_3=0\). Dividing the rest by \(t_0\) gives
 66 | \[
 67 | \varepsilon_4 t_4 + \varepsilon_5 t_5 t_0 + \varepsilon_6 t_6 t_0^{2} = -t_0^{3}. \tag{6}
 68 | \]
 69 | Reduce (6) modulo \(t_0\): \(\varepsilon_4 t_4\equiv0\pmod{t_0}\Rightarrow t_4=t_0\) (and \(\varepsilon_4\) free). Thus \(t_4=t_0\).
 70 | 
 71 | *Step 5:* Put \(t_4=t_0\) into (6) and divide by \(t_0\):
 72 | \[
 73 | \varepsilon_4 + \varepsilon_5 t_5 + \varepsilon_6 t_6 t_0 = -t_0^{2}. \tag{7}
 74 | \]
 75 | Modulo \(t_0\): \(\varepsilon_4+\varepsilon_5 t_5\equiv0\pmod{t_0}\Rightarrow t_5=1,\ \varepsilon_5=-\varepsilon_4\). So \(t_5=1\), \(\varepsilon_5=-\varepsilon_4\).
 76 | 
 77 | *Step 6:* Then (7) reduces to \(\varepsilon_4+\varepsilon_5 t_5=0\), leaving
 78 | \[
 79 | \varepsilon_6 t_6 t_0 = -t_0^{2}\quad\Longrightarrow\quad \varepsilon_6 t_6 = -t_0.
 80 | \]
 81 | Since \(t_6\mid t_0\) and \(t_0>1\), we must have \(t_6=t_0\) and \(\varepsilon_6=-1\).  
 82 | Thus \(t_6=t_0\), \(\varepsilon_6=-1\).
 83 | 
 84 | Collecting the results:
 85 | \[
 86 | \begin{array}{ll}
 87 | t_0=t_0,\ t_1=1,\ t_2=t_0,\ t_3=1,\ t_4=t_0,\ t_5=1,\ t_6=t_0;\\[2mm]
 88 | \varepsilon_1=-\varepsilon_0,\ \varepsilon_3=-\varepsilon_2,\ \varepsilon_5=-\varepsilon_4,\ \varepsilon_6=-1.
 89 | \end{array}
 90 | \]
 91 | So the absolute values are fixed: even‑indexed coefficients have absolute value \(t_0\), odd‑indexed have absolute value \(1\). The signs \(\varepsilon_0,\varepsilon_2,\varepsilon_4\) are still free; the others are determined by them.
 92 | 
 93 | Now impose the sum condition (2):
 94 | \[
 95 | \sum_{i=0}^{6}\varepsilon_i t_i = \varepsilon_0 t_0 + (-\varepsilon_0) + \varepsilon_2 t_0 + (-\varepsilon_2) + \varepsilon_4 t_0 + (-\varepsilon_4) + (-1)t_0 = (T-1)t_0-T,
 96 | \]
 97 | where \(T=\varepsilon_0+\varepsilon_2+\varepsilon_4\). Setting this equal to \(-1\) yields
 98 | \[
 99 | (T-1)t_0 - T = -1\quad\Longrightarrow\quad (T-1)(t_0-1)=0.
100 | \]
101 | Since \(t_0>1\), we must have \(T=1\). Hence \(\varepsilon_0+\varepsilon_2+\varepsilon_4=1\), i.e. exactly two of them are \(+1\) and one is \(-1\). That gives \(3\) possibilities for the triple \((\varepsilon_0,\varepsilon_2,\varepsilon_4)\).
102 | 
103 | Therefore, for every odd \(t_0\) with \(1<t_0<2025^{2}\), there are exactly \(3\) good polynomials given by the above pattern of signs. The condition \(|a_i|<2025^{2}\) requires \(t_0<2025^{2}\); the oddness condition is already satisfied because \(t_0\) is odd. The number of such \(t_0\) is the number of odd integers from \(3\) to \(2025^{2}-2\) inclusive, which is
104 | \[
105 | \frac{2025^{2}-3}{2}=2\,050\,311.
106 | \]
107 | Hence the number of good polynomials from this case is \(3\times2\,050\,311 = 6\,150\,933\).
108 | 
109 | Adding the \(35\) from the \(t_0=1\) case gives the total
110 | \[
111 | 35+6\,150\,933 = 6\,150\,968.
112 | \]
113 | 
114 | \[
115 | \boxed{6150968}
116 | \]
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
   - Fill in the header (Problem `5_POLYGO`, Submission `model_2`, your grader
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
   `grade_5_POLYGO_model_2_AI.tex`.
3. **Check it compiles.** Run `pdflatex -interaction=nonstopmode <file>.tex` and fix any
   errors so it builds to a PDF. (Keep the document self-contained — do not add external
   dependencies.)
4. **State the proposed mark** (0/1/6/7) clearly in your final message.

Do **not** commit anything to the repository — return the `.tex` (and its PDF if produced).
