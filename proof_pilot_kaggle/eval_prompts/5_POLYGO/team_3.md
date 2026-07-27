# AIMO Proof Pilot — grading task

You are an **expert olympiad grader** for the AIMO Proof Pilot. Your job is to grade **one**
submission against the official markscheme and return a completed grading sheet as a LaTeX
(`.tex`) file.

- **Problem:** `5_POLYGO`
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

This is the submission `team_3` for problem `5_POLYGO`, with line numbers
added for reference in your errors log.

```text
  1 | ## Solution  
  2 | 
  3 | Let  
  4 | 
  5 | \[
  6 | P(x)=x^7+c_6x^6+c_5x^5+c_4x^4+c_3x^3+c_2x^2+c_1x+c_0
  7 | \]
  8 | 
  9 | be a polynomial satisfying the conditions of a *good* polynomial.  
 10 | All coefficients are integers, \(P\) is monic, every coefficient is odd and its absolute value is \(<2025^2\), and for every coefficient the number \(|c_i|\) is a root of \(P\).
 11 | 
 12 | Denote  
 13 | 
 14 | \[
 15 | r_i=|c_i|\;(i=0,\dots ,6),\qquad t=r_0=|c_0|.
 16 | \]
 17 | 
 18 | All \(r_i\) are positive odd integers with \(1\le r_i<2025^2\).  
 19 | Because \(P(r_i)=0\) and the leading coefficient is \(1\), the Rational Root Theorem gives \(r_i\mid c_0\). Hence \(r_i\mid r_0=t\); in particular \(t\) is the largest among the \(r_i\).
 20 | 
 21 | ---
 22 | 
 23 | ### 1.  Factorisation by \(x-t\)
 24 | 
 25 | Since \(t=r_0\) is a root, we can factor  
 26 | 
 27 | \[
 28 | P(x)=(x-t)Q(x),
 29 | \]
 30 | 
 31 | where \(Q(x)=x^6+a_5x^5+a_4x^4+a_3x^3+a_2x^2+a_1x+a_0\) is monic with integer coefficients.  
 32 | Expanding the product yields  
 33 | 
 34 | \[
 35 | \begin{aligned}
 36 | c_6 &= a_5 - t, \\
 37 | c_5 &= a_4 - t a_5, \\
 38 | c_4 &= a_3 - t a_4, \\
 39 | c_3 &= a_2 - t a_3, \\
 40 | c_2 &= a_1 - t a_2, \\
 41 | c_1 &= a_0 - t a_1, \\
 42 | c_0 &= -t a_0.
 43 | \end{aligned}
 44 | \tag{1}
 45 | \]
 46 | 
 47 | The constant term gives \(|c_0|=t=|-t a_0|\), so \(|a_0|=1\).  Thus  
 48 | 
 49 | \[
 50 | a_0 = \varepsilon_0,\qquad \varepsilon_0=\pm1.
 51 | \tag{2}
 52 | \]
 53 | 
 54 | ---
 55 | 
 56 | ### 2.  The possible values of \(r_i\)
 57 | 
 58 | For any index \(i\) with \(r_i\neq t\) we have \(P(r_i)=0\) and \(r_i\neq t\), hence  
 59 | 
 60 | \[
 61 | 0=P(r_i)=(r_i-t)Q(r_i)\quad\Longrightarrow\quad Q(r_i)=0.
 62 | \]
 63 | 
 64 | \(Q\) is monic with integer coefficients, so by the Rational Root Theorem every integer root of \(Q\) must divide \(a_0=\pm1\).  Consequently every such \(r_i\) must be \(\pm1\); being positive it is \(1\).  Therefore  
 65 | 
 66 | \[
 67 | r_i\in\{1,t\}\qquad\text{for all }i.
 68 | \tag{3}
 69 | \]
 70 | 
 71 | ---
 72 | 
 73 | ### 3.  The case \(t=1\)
 74 | 
 75 | If \(t=1\) then all \(r_i=1\); i.e. every coefficient \(c_i\) is either \(+1\) or \(-1\).  
 76 | Condition \(P(1)=0\) (which holds because \(r_i=1\) is a root) gives  
 77 | 
 78 | \[
 79 | 1+\sum_{i=0}^6 c_i=0.
 80 | \]
 81 | 
 82 | Writing \(p\) for the number of indices with \(c_i=+1\) (the rest are \(-1\)), we obtain  
 83 | 
 84 | \[
 85 | 1+(p-(7-p))=2p-6=0\;\Longrightarrow\; p=3.
 86 | \]
 87 | 
 88 | Thus exactly three of the seven coefficients are \(+1\) and the other four are \(-1\).  
 89 | The leading coefficient is already \(+1\), so we must choose which three of the positions \(\{0,\dots ,6\}\) receive \(+1\).  The number of such choices is  
 90 | 
 91 | \[
 92 | \binom{7}{3}=35.
 93 | \]
 94 | 
 95 | All these polynomials satisfy the oddness and size restrictions because \(1<2025^2\).  Hence **there are 35 good polynomials with \(t=1\)**.
 96 | 
 97 | ---
 98 | 
 99 | ### 4.  The case \(t>1\)
100 | 
101 | Now suppose \(t>1\) (so \(t\) is odd, at least \(3\)).  From (3) each coefficient has absolute value either \(1\) or \(t\).  
102 | If all \(r_i=t\) (i.e. every coefficient has absolute value \(t\)), then \(P(t)=0\) forces  
103 | 
104 | \[
105 | t^7+(t\varepsilon_6)t^6+\dots+t\varepsilon_0=t^0?\; \text{(see below)}.
106 | \]
107 | 
108 | A short analysis shows that this is impossible for \(t>1\) (the leading term \(t^7(1+\varepsilon_6)\) cannot be cancelled by the remaining terms because \(t^5\) dominates).  Hence at least one coefficient has absolute value \(1\).  
109 | For such a coefficient we have \(P(1)=0\), and therefore \(Q(1)=0\) (since \(1\neq t\)).
110 | 
111 | ---
112 | 
113 | #### 4.1  Recurrence from the coefficients
114 | 
115 | Write each \(c_i\) as  
116 | 
117 | \[
118 | c_i=\eta_i r_i,\qquad \eta_i=\pm1,\quad r_i\in\{1,t\}.
119 | \]
120 | 
121 | From (1) we obtain the relations  
122 | 
123 | \[
124 | \begin{aligned}
125 | a_5 &= t + \eta_6 r_6, \tag{4a}\\
126 | a_4 &= t a_5 + \eta_5 r_5, \tag{4b}\\
127 | a_3 &= t a_4 + \eta_4 r_4, \tag{4c}\\
128 | a_2 &= t a_3 + \eta_3 r_3, \tag{4d}\\
129 | a_1 &= t a_2 + \eta_2 r_2, \tag{4e}\\
130 | a_0 &= t a_1 + \eta_1 r_1. \tag{4f}
131 | \end{aligned}
132 | \]
133 | 
134 | ---
135 | 
136 | #### 4.2  Determining \(a_1\) and \(r_1\)
137 | 
138 | Because \(a_0=\pm1\) and \(t>1\), equation (4f) forces \(r_1=1\).  Indeed, if \(r_1=t\) then \(a_0=t(a_1+\eta_1)\) is a multiple of \(t\ge3\), contradicting \(a_0=\pm1\).  Hence \(r_1=1\) and  
139 | 
140 | \[
141 | a_0 = t a_1 + \eta_1. \tag{5}
142 | \]
143 | 
144 | Since \(a_0=\pm1\) and \(t\ge3\), the only possibility is \(a_1=0\) and \(\eta_1=a_0\).  Thus  
145 | 
146 | \[
147 | a_1=0,\qquad r_1=1,\qquad \eta_1=a_0. \tag{6}
148 | \]
149 | 
150 | ---
151 | 
152 | #### 4.3  Determining the remaining indices
153 | 
154 | Now (4e) becomes \(0 = t a_2 + \eta_2 r_2\).  Hence \(r_2\) must be \(t\) (otherwise the right‑hand side would be a multiple of \(t\) plus \(\eta_2\), which cannot vanish with \(a_2\) integer).  Moreover  
155 | 
156 | \[
157 | a_2 = -\eta_2. \tag{7}
158 | \]
159 | 
160 | Insert (7) into (4d):  
161 | 
162 | \[
163 | -\eta_2 = t a_3 + \eta_3 r_3.
164 | \]
165 | 
166 | If \(r_3=t\) the left side is \(-\eta_2\) and the right side is a multiple of \(t\) plus \(\eta_3 t\), forcing \(-\eta_2\equiv0\pmod t\), impossible because \(t\ge3\).  Therefore \(r_3=1\) and the equation becomes  
167 | 
168 | \[
169 | -\eta_2 = t a_3 + \eta_3.
170 | \]
171 | 
172 | Since \(t\ge3\), the only way the right side can be \(\pm1\) is that it is actually \(0\); thus  
173 | 
174 | \[
175 | a_3=0,\qquad \eta_3=-\eta_2,\qquad r_3=1. \tag{8}
176 | \]
177 | 
178 | Repeating the argument, (4c) gives  
179 | 
180 | \[
181 | 0 = t a_4 + \eta_4 r_4.
182 | \]
183 | 
184 | As before, \(r_4\) cannot be \(1\) (otherwise \(t a_4\) would have to be an integer not divisible by \(t\)), so \(r_4=t\) and  
185 | 
186 | \[
187 | a_4 = -\eta_4. \tag{9}
188 | \]
189 | 
190 | Next, (4b):  
191 | 
192 | \[
193 | -\eta_4 = t a_5 + \eta_5 r_5.
194 | \]
195 | 
196 | If \(r_5=t\) we would need \(-\eta_4\equiv0\pmod t\), impossible.  Hence \(r_5=1\) and  
197 | 
198 | \[
199 | -\eta_4 = t a_5 + \eta_5.
200 | \]
201 | 
202 | Again this forces the right side to be \(0\), so  
203 | 
204 | \[
205 | a_5=0,\qquad \eta_5=-\eta_4,\qquad r_5=1. \tag{10}
206 | \]
207 | 
208 | Finally, (4a) yields  
209 | 
210 | \[
211 | 0 = t + \eta_6 r_6.
212 | \]
213 | 
214 | Thus \(r_6\) must be \(t\) and \(\eta_6=-1\).  Consequently  
215 | 
216 | \[
217 | r_6=t,\quad \eta_6=-1. \tag{11}
218 | \]
219 | 
220 | ---
221 | 
222 | #### 4.4  The sign condition and counting
223 | 
224 | Collecting the results we have  
225 | 
226 | \[
227 | \begin{aligned}
228 | &r_6=t,\; \eta_6=-1; & r_5=1,\; \eta_5&=-\eta_4;\\
229 | &r_4=t,\; \eta_4=\pm1; & r_3=1,\; \eta_3&=-\eta_2;\\
230 | &r_2=t,\; \eta_2&=\pm1; & r_1=1,\; \eta_1&=a_0;\\
231 | &a_5=0,\; a_4&=-\eta_4,\; a_3=0,\; a_2&=-\eta_2,\; a_1=0,\; a_0&=\pm1.
232 | \end{aligned}
233 | \]
234 | 
235 | Equation (5) gives \(a_0 = t a_1 + \eta_1 = \eta_1\), but also from the recursion we obtain  
236 | 
237 | \[
238 | a_0 = t a_1 + \eta_1 = 0 + \eta_1 = \eta_1,
239 | \]
240 | 
241 | while using (6)–(11) we can also express \(a_0\) in terms of \(\eta_2,\eta_4\):
242 | 
243 | \[
244 | a_0 = \eta_1 = -\eta_3 = \eta_2.
245 | \]
246 | 
247 | But from (10) we have \(\eta_5=-\eta_4\) and (8) gives \(\eta_3=-\eta_2\); these do not directly give \(a_0\).  A more systematic evaluation of the recurrence from the bottom shows  
248 | 
249 | \[
250 | a_0 = \eta_2 + \eta_4 - 1.
251 | \]
252 | 
253 | (Indeed, substituting all relations into (4f) yields this identity.)  Since \(a_0=\pm1\), we need  
254 | 
255 | \[
256 | \eta_2 + \eta_4 - 1 = \pm1.
257 | \]
258 | 
259 | Both \(\eta_2,\eta_4\) are \(\pm1\).  The possibilities are  
260 | 
261 | \[
262 | \begin{array}{c|c|c}
263 | \eta_2 & \eta_4 & \eta_2+\eta_4-1 \\ \hline
264 | 1 & 1 & 1 \\
265 | 1 & -1 & -1 \\
266 | -1 & 1 & -1 \\
267 | -1 & -1 & -3
268 | \end{array}
269 | \]
270 | 
271 | Only the first three rows give \(a_0=\pm1\).  Hence exactly **three** choices of the signs \((\eta_2,\eta_4)\) are admissible for each fixed \(t>1\).
272 | 
273 | For each such choice we obtain a concrete polynomial, and all coefficients are odd with absolute values either \(1\) or \(t\).  The condition \(P(t)=0\) holds automatically because \(t\) is a root, and \(P(1)=0\) follows from the construction (it is equivalent to \(Q(1)=0\), which is satisfied).
274 | 
275 | Thus for every odd integer \(t\) with \(3\le t<2025^2\) there are **exactly three good polynomials**.
276 | 
277 | ---
278 | 
279 | #### 4.5  Counting the polynomials for \(t>1\)
280 | 
281 | We need the number of odd integers \(t\) in the interval \([3,\,2025^2-1]\).  
282 | Since \(2025\) is odd, \(2025^2\) is odd, so the largest odd less than \(2025^2\) is \(2025^2-2=4\,100\,623\).  
283 | The number of odd integers from \(1\) to \(4\,100\,623\) inclusive is  
284 | 
285 | \[
286 | \frac{4\,100\,623+1}{2}=2\,050\,312.
287 | \]
288 | 
289 | Removing \(t=1\) leaves  
290 | 
291 | \[
292 | N = 2\,050\,312-1 = 2\,050\,311
293 | \]
294 | 
295 | odd values \(t\ge3\) with \(t<2025^2\).
296 | 
297 | Each such \(t\) contributes \(3\) polynomials, so the number for \(t>1\) is  
298 | 
299 | \[
300 | 3\cdot N = 3\cdot 2\,050\,311 = 6\,150\,933.
301 | \]
302 | 
303 | ---
304 | 
305 | ### 5.  Total number of good polynomials
306 | 
307 | Adding the \(35\) polynomials from the case \(t=1\) we obtain  
308 | 
309 | \[
310 | 35 + 6\,150\,933 = 6\,150\,968.
311 | \]
312 | 
313 | ---
314 | 
315 | \[
316 | \boxed{6\,150\,968}
317 | \]
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
   - Fill in the header (Problem `5_POLYGO`, Submission `team_3`, your grader
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
   `grade_5_POLYGO_team_3_AI.tex`.
3. **Check it compiles.** Run `pdflatex -interaction=nonstopmode <file>.tex` and fix any
   errors so it builds to a PDF. (Keep the document self-contained — do not add external
   dependencies.)
4. **State the proposed mark** (0/1/6/7) clearly in your final message.

Do **not** commit anything to the repository — return the `.tex` (and its PDF if produced).
