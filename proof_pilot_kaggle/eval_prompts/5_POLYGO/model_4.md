# AIMO Proof Pilot — grading task

You are an **expert olympiad grader** for the AIMO Proof Pilot. Your job is to grade **one**
submission against the official markscheme and return a completed grading sheet as a LaTeX
(`.tex`) file.

- **Problem:** `5_POLYGO`
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

This is the submission `model_4` for problem `5_POLYGO`, with line numbers
added for reference in your errors log.

```text
  1 | **Solution.**  
  2 | Let  
  3 | 
  4 | \[
  5 | P(x)=x^{7}+a_{6}x^{6}+a_{5}x^{5}+a_{4}x^{4}+a_{3}x^{3}+a_{2}x^{2}+a_{1}x+a_{0}
  6 | \qquad (a_i\in\mathbb Z)
  7 | \]
  8 | 
  9 | be a *good* polynomial.
 10 | For \(i=0,\dots ,6\) put  
 11 | 
 12 | \[
 13 | c_i:=|a_i|\;(>0),\qquad c_7:=|a_7|=1 .
 14 | \]
 15 | 
 16 | All the numbers \(c_i\) are odd, satisfy \(c_i<2025^{2}\) and, by definition of a good
 17 | polynomial,
 18 | 
 19 | \[
 20 | P(c_i)=0\qquad (i=0,\dots ,7). \tag{1}
 21 | \]
 22 | 
 23 | --------------------------------------------------------------------
 24 | ### 1.  Preliminary observations
 25 | 
 26 | *Because the leading coefficient is \(1\), evaluating at \(x=1\) gives*
 27 | 
 28 | \[
 29 | P(1)=1+a_6+\dots +a_0=0 \quad\Longrightarrow\quad 
 30 | a_6+\dots +a_0=-1 .\tag{2}
 31 | \]
 32 | 
 33 | Since each \(a_i\) is odd, (2) implies that among the seven
 34 | numbers \(a_0,\dots ,a_6\) exactly three are \(+1\) and four are \(-1\).  
 35 | Consequently every \(c_i\) equals either \(1\) or \(|a_i|>1\).
 36 | 
 37 | --------------------------------------------------------------------
 38 | ### 2.  The largest absolute coefficient
 39 | 
 40 | Let  
 41 | 
 42 | \[
 43 | r:=\max\{c_0,c_1,\dots ,c_6\}.
 44 | \]
 45 | 
 46 | If every \(c_i=1\) we shall deal with this case in §4.
 47 | Hence assume from now on that \(r>1\).
 48 | 
 49 | --------------------------------------------------------------------
 50 | #### Lemma 2.1  
 51 | \(c_0=r\) and \(c_0\) is the absolute value of the product of all
 52 | roots of \(P\).
 53 | 
 54 | *Proof.*  
 55 | Write the factorisation of \(P\) by its roots \(\alpha_1,\dots ,\alpha_7\) :
 56 | 
 57 | \[
 58 | P(x)=\prod_{j=1}^{7}(x-\alpha_j),\qquad
 59 | \alpha_j\in\mathbb C .
 60 | \]
 61 | 
 62 | The constant term is
 63 | \[
 64 | a_0=(-1)^{7}\prod_{j=1}^{7}\alpha_j=-\prod_{j=1}^{7}\alpha_j .
 65 | \]
 66 | Hence  
 67 | 
 68 | \[
 69 | c_0=|a_0|=\Bigl|\prod_{j=1}^{7}\alpha_j\Bigr| .\tag{3}
 70 | \]
 71 | 
 72 | All numbers \(c_i\) are roots of \(P\) by (1), thus
 73 | \(1\) (the absolute value of the leading coefficient) is a root.
 74 | Consequently \(\prod_{j=1}^{7}\alpha_j\) is a product of numbers each
 75 | of which has absolute value at least \(1\); therefore the
 76 | right‑hand side of (3) is at least the largest of the numbers
 77 | \(|\alpha_j|\).  By (1) every \(|\alpha_j|\) belongs to the set
 78 | \(\{c_0,\dots ,c_6\}\); hence \(\max_j |\alpha_j|=r\).
 79 | Thus \(c_0\ge r\).
 80 | On the other hand \(c_0\) itself belongs to the set
 81 | \(\{c_0,\dots ,c_6\}\); therefore \(c_0\le r\).
 82 | Consequently \(c_0=r\).  ∎
 83 | 
 84 | 
 85 | 
 86 | --------------------------------------------------------------------
 87 | ### 3.  Reduction to a quadratic factor
 88 | 
 89 | Because of \(P(1)=0\) (see (2)), the linear factor \((x-1)\) divides
 90 | \(P\).  By Lemma 2.1 the integer \(r=c_0\) is a root of \(P\);
 91 | hence \((x-r)\) also divides \(P\).
 92 | Write
 93 | 
 94 | \[
 95 | P(x)=(x-1)(x-r)Q(x) ,
 96 | \tag{4}
 97 | \]
 98 | 
 99 | where \(Q\) is monic of degree \(5\) and has integer coefficients.
100 | Put  
101 | 
102 | \[
103 | Q(x)=x^{5}+b_{4}x^{4}+b_{3}x^{3}+b_{2}x^{2}+b_{1}x+b_{0},
104 | \qquad b_j\in\mathbb Z .
105 | \]
106 | 
107 | Expanding (4) and comparing coefficients with the generic form of
108 | \(P\) yields
109 | 
110 | \[
111 | \begin{aligned}
112 | a_{6}&=b_{4}-(1+r),\\[2mm]
113 | a_{5}&=b_{3}-(1+r)b_{4}+r,\\
114 | a_{4}&=b_{2}-(1+r)b_{3}+rb_{4},\\
115 | a_{3}&=b_{1}-(1+r)b_{2}+rb_{3},\\
116 | a_{2}&=b_{0}-(1+r)b_{1}+rb_{2},\\
117 | a_{1}&=-(1+r)b_{0}+rb_{1},\\
118 | a_{0}&=r\,b_{0}.
119 | \end{aligned}\tag{5}
120 | \]
121 | 
122 | Recall that \(c_i=|a_i|\) equals either \(1\) or \(r\); the latter is
123 | the maximal value.
124 | From the last line of (5),
125 | 
126 | \[
127 | c_0=|a_{0}|=|r\,b_{0}| .
128 | \]
129 | 
130 | Since \(c_0=r>1\), the only possibility is  
131 | 
132 | \[
133 | |b_{0}|=1 \qquad\text{and}\qquad c_0=r.\tag{6}
134 | \]
135 | 
136 | Let us write \(b_{0}= \varepsilon _0\) with \(\varepsilon _0\in\{\pm1\}\).
137 | 
138 | --------------------------------------------------------------------
139 | #### Lemma 3.1  
140 | \(c_{1}=1\) and \(b_{1}=-\varepsilon _0\).
141 | 
142 | *Proof.*  
143 | From (5) and (6),
144 | 
145 | \[
146 | a_{1}=-(1+r)\varepsilon _0+r b_{1},
147 | \qquad 
148 | c_{1}=|a_{1}|\le r .
149 | \]
150 | 
151 | If \(c_{1}=r\) then  
152 | 
153 | \[
154 | r=|-(1+r)\varepsilon _0+r b_{1}|
155 |    =|r(b_{1}-\varepsilon _0)-\varepsilon _0| .
156 | \]
157 | 
158 | Dividing by \(r\) gives \(|b_{1}-\varepsilon _0-\varepsilon _0/r|=1\).
159 | Because \(r>1\) the fraction \(\varepsilon _0/r\) is not integral,
160 | hence the equality is impossible.  Thus \(c_{1}\neq r\); consequently
161 | \(c_{1}=1\).
162 | Now \( |-(1+r)\varepsilon _0+r b_{1}| =1\) implies
163 | \(r b_{1} = (1+r)\varepsilon _0\pm1\).
164 | Since \(r\) does not divide the integer \(\pm1\) (again because \(r>1\)),
165 | the only way to obtain an integer \(b_{1}\) is  
166 | 
167 | \[
168 | b_{1} = -\varepsilon _0 .
169 | \tag{7}
170 | \]
171 | 
172 | ∎
173 | 
174 | 
175 | 
176 | --------------------------------------------------------------------
177 | #### Lemma 3.2  
178 | No odd integer \(r>1\) satisfies the remaining equations (5).
179 | 
180 | *Proof.*  
181 | Insert \(b_{0}=\varepsilon _0\) and \(b_{1}=-\varepsilon _0\) from (6)–(7)
182 | into the expression for \(a_{2}\) in (5):
183 | 
184 | \[
185 | a_{2}= \varepsilon _0-(1+r)(-\varepsilon _0)+r b_{2}
186 |       = r b_{2}+\varepsilon _0(r+2).   \tag{8}
187 | \]
188 | 
189 | Hence  
190 | 
191 | \[
192 | c_{2}=|a_{2}|=|r b_{2}+ \varepsilon _0(r+2)|
193 |           =|r(b_{2}+\varepsilon _0)+2\varepsilon _0| .\tag{9}
194 | \]
195 | 
196 | Because the absolute values of the coefficients may only be
197 | \(1\) or \(r\), we must have \(c_{2}\in\{1,r\}\).
198 | 
199 | *Case \(c_{2}=1\).*  
200 | Then \(|r(b_{2}+\varepsilon _0)+2\varepsilon _0|=1\).
201 | The term \(r|b_{2}+\varepsilon _0|\) is a multiple of \(r\ge3\)
202 | and therefore its absolute value is at least \(3\) unless it is
203 | zero.  If it is zero we obtain \(|2\varepsilon _0|=2\neq1\).
204 | Hence this case is impossible.
205 | 
206 | *Case \(c_{2}=r\).*  
207 | Now \(|r(b_{2}+\varepsilon _0)+2\varepsilon _0|=r\), i.e.  
208 | 
209 | \[
210 | |\,b_{2}+\varepsilon _0+\frac{2\varepsilon _0}{r}\,|=1 .
211 | \]
212 | 
213 | Since \(0<\bigl|\frac{2\varepsilon _0}{r}\bigr|<1\) (recall \(r\ge3\)),
214 | the left‑hand side can be equal to \(1\) only when
215 | \(b_{2}+\varepsilon _0=0\) and \(\frac{2\varepsilon _0}{r}=0\),
216 | the latter being impossible for \(r>1\).
217 | Thus this case also leads to a contradiction.
218 | 
219 | Both possibilities for \(c_{2}\) are impossible; therefore no odd
220 | \(r>1\) can satisfy the system (5). ∎
221 | 
222 | 
223 | 
224 | --------------------------------------------------------------------
225 | From Lemmas 3.1 and 3.2 we deduce that the assumption \(r>1\) is
226 | false. Consequently
227 | 
228 | \[
229 | \boxed{c_0=c_1=\dots =c_6=1 } .
230 | \tag{10}
231 | \]
232 | 
233 | That is, **every coefficient of a good polynomial has absolute value
234 | \(1\).**  Hence each coefficient is either \(+1\) or \(-1\).
235 | 
236 | --------------------------------------------------------------------
237 | ### 4.  Determining all good polynomials
238 | 
239 | Because all \(|a_i|=1\), condition (1) reduces to the single requirement
240 | that \(1\) be a root of \(P\); indeed \(P(1)=0\) is equivalent to  
241 | 
242 | \[
243 | 1+a_6+\dots +a_0=0 .
244 | \tag{11}
245 | \]
246 | 
247 | Let \(p\) be the number of coefficients equal to \(+1\) among
248 | \(a_0,\dots ,a_6\); then the remaining \(7-p\) coefficients equal \(-1\).
249 | Equation (11) becomes  
250 | 
251 | \[
252 | 1+(p-(7-p))=0\quad\Longleftrightarrow\quad 2p-6=0
253 | \quad\Longleftrightarrow\quad p=3 .
254 | \]
255 | 
256 | Thus exactly three of the seven coefficients \(a_{0},\dots ,a_{6}\) are
257 | \(+1\) and the other four are \(-1\).  
258 | Choosing the three positions of the \(+1\)’s determines the polynomial
259 | uniquely; there are  
260 | 
261 | \[
262 | \binom{7}{3}=35
263 | \]
264 | 
265 | such choices.
266 | 
267 | Every polynomial obtained in this way is monic of degree \(7\),
268 | has all coefficients odd and smaller than \(2025^{2}\),
269 | and satisfies \(P(1)=0\); because each absolute coefficient equals
270 | \(1\), condition (1) is fulfilled.  Hence all \(35\) polynomials are
271 | good.
272 | 
273 | --------------------------------------------------------------------
274 | ### 5.  Conclusion
275 | 
276 | The only possible good polynomials are those whose coefficients are
277 | \(\pm1\) with exactly three \(+1\)’s and four \(-1\)’s; there are  
278 | 
279 | \[
280 | \boxed{35}
281 | \]
282 | 
283 | such polynomials. ∎
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
   - Fill in the header (Problem `5_POLYGO`, Submission `model_4`, your grader
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
   `grade_5_POLYGO_model_4_AI.tex`.
3. **Check it compiles.** Run `pdflatex -interaction=nonstopmode <file>.tex` and fix any
   errors so it builds to a PDF. (Keep the document self-contained — do not add external
   dependencies.)
4. **State the proposed mark** (0/1/6/7) clearly in your final message.

Do **not** commit anything to the repository — return the `.tex` (and its PDF if produced).
