# AIMO Proof Pilot — grading task

You are an **expert olympiad grader** for the AIMO Proof Pilot. Your job is to grade **one**
submission against the official markscheme and return a completed grading sheet as a LaTeX
(`.tex`) file.

- **Problem:** `1_DIVALL`
- **Submission:** `team_6`

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
\section*{Problem 1 (DIVALL)}


\problem[6]{%
There are $k \geq 3$ different positive integers $a_1, \ldots, a_k$ with product $P$, and sum strictly less than $3 \cdot 10^{6}$. Let $g$ be the largest positive integer that divides each of $(P/a_i)+1$ for $1 \leq i \leq k$. Across all possible choices for $a_i$ and $k \geq 3$, what is the maximum possible value of $g$?
}{998285}

\vspace{2cm}

\textbf{Original AIMO3 Formulation:} 

There are $k \geq 3$ different positive integers $a_1, \ldots, a_k$ with product $P$, and sum strictly less than $3 \cdot 10^{6}$. Let $g$ be the largest positive integer that divides each of $(P/a_i)+1$ for $1 \leq i \leq k$. Across all possible choices for $a_i$ and $k \geq 3$, let $G$ be the maximum possible value of $g$. What is the remainder when $G$ is divided by $10^{5}$?

\textbf{Answer:} 98285

\vspace{1cm}

\textbf{Remark:} Relative to the AIMO3 version, we removed the modulo $10^5$ answer modification as we are not restricted to $5$-digit answers in the Proof Pilot.

\clearpage


\polishedsolution[SB][6]{%
We prove that the maximum is $\boxed{998285}$.

\textbf{Claim 1:} $g$ and $P$ are coprime.

\begin{proof}
    Suppose, for contradiction, that some prime $q$ divides both $g$ and $P$. Since $P=a_1a_2\cdots a_k$, the prime $q$ divides some $a_i$. Choose an index $j\neq i$, which is possible since $k\geq 3$. Then $a_i$ is one of the factors of $P/a_j$, so $q\mid P/a_j$. But $q\mid g$, and $g$ divides $(P/a_j)+1$, so $q\mid (P/a_j)+1$. Hence $q$ divides both $P/a_j$ and $(P/a_j)+1$, which is impossible. Thus no prime divides both $g$ and $P$.
\end{proof}

\textbf{Claim 2:} For $1 \leq i<j \leq k$ we have $g \mid a_j-a_i$.

\begin{proof}
    Since $g$ divides both $(P/a_i)+1$ and $(P/a_j)+1$, it divides their difference. Thus,
    \begin{equation*}
      g\mid \left((P/a_i)+1\right)-\left((P/a_j)+1\right)
        = \frac{P}{a_ia_j}(a_j-a_i).
    \end{equation*}
    The factor $P/(a_ia_j)$ is a product of some of the $a_\ell$, so it divides $P$. By Claim 1, it is therefore coprime to $g$. This means that $g$ must divide the factor $\left(a_j-a_i\right)$ as claimed.
\end{proof}

It follows from Claim 2 that all the $a_i$ leave the same residue $\pmod g$, say $0 \leq r<g$. If $g=1$, then certainly $g<998285$, so for the upper bound we may assume $g \geq 2$. In this case, Claim 1 tells us $r \neq 0$. WLOG order the numbers so that $a_1<a_2<\cdots<a_k$. Since the $a_i$ are distinct positive integers in the same residue class modulo $g$, we have
\begin{equation*}
  a_i\geq r+(i-1)g \quad \text{for }1\leq i\leq k.
\end{equation*}
Also, for every $i$,
\begin{equation*}
  0\equiv (P/a_i)+1 \equiv r^{k-1}+1 \pmod g,
\end{equation*}
so
\begin{equation*}
  g\mid r^{k-1}+1. \tag{1}
\end{equation*}

We now split into cases according to $k$.

\textbf{Case 1: $k=3$.} From the lower bound on the three $a_i$,
\begin{equation*}
  3\cdot 10^6>a_1+a_2+a_3\geq r+(g+r)+(2g+r)=3(g+r),
\end{equation*}
so
\begin{equation*}
  g+r<10^6. \tag{2}
\end{equation*}
By $(1)$, we have $g\mid r^2+1$. Write
\begin{equation*}
  r^2+1=\ell g
\end{equation*}
for some positive integer $\ell$.

\begin{itemize}
    \item If $\ell=1$, then $g=r^2+1$. By $(2)$,
    \begin{equation*}
      r^2+r+1=g+r<10^6,
    \end{equation*}
    so $r\leq 999$, and therefore
    \begin{equation*}
      g=r^2+1\leq 999^2+1=998002<998285.
    \end{equation*}
    \item If $\ell=2$, then
    \begin{equation*}
      g+r=\frac{r^2+1}{2}+r=\frac{(r+1)^2}{2}<10^6.
    \end{equation*}
    Hence $r+1<1000\sqrt2$, so $r\leq 1413$. Therefore
    \begin{equation*}
      g=\frac{r^2+1}{2}\leq \frac{1413^2+1}{2}=998285.
    \end{equation*}
    This is attainable by setting $r=1413$, $g=(r^2+1)/2$, and 
    \begin{equation*}
        a_1=r, \; a_2=g+r, \; a_3=2g+r.
    \end{equation*}
    which are distinct positive integers. The divisibility conditions then hold since $(P/a_i)+1 \equiv r^2+1 \pmod{g}$ and by construction the sum $3(g+r)<3 \cdot 10^{6}$. 
    \item If $\ell=3$, then no integer $r$ is possible, because squares are congruent to $0$ or $1$ modulo $3$, so $r^2+1$ is congruent to $1$ or $2$ modulo $3$ and is never divisible by $3$.
    \item Finally suppose $\ell\geq 4$. It is enough to rule out the possibility that $g>998285$. If $g>998285$, then $g\geq 998286$, so $(2)$ gives $r\leq 1713$. But then
    \begin{equation*}
      g=\frac{r^2+1}{\ell}\leq \frac{1713^2+1}{4}<998285,
    \end{equation*}
    which is a contradiction. Thus, in the case $k=3$, we always have $g\leq 998285$.
\end{itemize}

\textbf{Case 2: $k\geq 4$.} Using only the four smallest of the $a_i$, we get
\begin{equation*}
  3\cdot 10^6>a_1+a_2+\cdots+a_k\geq a_1+a_2+a_3+a_4
     \geq r+(g+r)+(2g+r)+(3g+r).
\end{equation*}
The right-hand side is $6g+4r$, which is greater than $6g$. Therefore
\begin{equation*}
  3\cdot 10^6>6g,
\end{equation*}
so $g<500000<998285$. Hence the case $k\geq 4$ cannot improve on the bound found for $k=3$.

Thus, the maximum possible value for $g$ is $\boxed{998285}$ as claimed.
} 

\clearpage

\markscheme{%
A solution is \emph{essentially complete} if, allowing only minor slips of the kind described below, it proves both the upper bound $g\leq 998285$ and a construction attaining $g=998285$.

An essentially complete solution should receive $6$ rather than $7$ if it contains a minor error or omission: a gap that is not merely a small arithmetic slip, but which can be repaired without changing the main structure of the solution. Examples include:
\begin{enumerate}[label=(ME\arabic*)]
    \item Proving $\gcd(g,P)=1$ correctly, and later asserting
    \[
      g\mid \frac{P}{a_ia_j}(a_j-a_i) \implies g\mid a_j-a_i
    \]
    without explicitly saying that $P/(a_ia_j)$ is coprime to $g$. This is a minor omission only when there is a valid proof of $\gcd(g,P)=1$ somewhere else in the solution.
    \item Omitting the explanation that the common residue $r$ is non-zero, while otherwise using the common-residue argument correctly.
    \item Making a fixable arithmetic or off-by-one error in one of the small $k=3$ subcases, such as mishandling the strict inequality in the $\ell=2$ case, while the intended bound and final answer are otherwise clear.
    \item Giving the correct construction in the $\ell=2$ case but failing to verify one or more of its required properties, such as the divisibility condition or the sum bound.
\end{enumerate}

The following should \emph{not} generally be penalised:
\begin{enumerate}[label=(NME\arabic*)]
    \item Minor arithmetic slips in the $k\geq 4$ case that still leave a bound comfortably below $998285$.
    \item Not proving separately that the greatest common divisor of the numbers $(P/a_i)+1$ in the constructed example has greatest common divisor exactly $998285$ (i.e. exclude the case that the $\gcd$ could be a larger multiple of this), provided the solution has already proved the global upper bound and has checked that $998285$ divides all the relevant numbers in the example.
\end{enumerate}

The following are not essentially complete, even if they contain many correct later calculations:
\begin{enumerate}[label=(NEC\arabic*)]
    \item A solution that needs but does not prove $\gcd(g,P)=1$.
    \item A solution that assumes the $a_i$ are pairwise coprime, or otherwise adds an assumption not present in the problem.
    \item A solution that considers only $k=3$ and does not rule out $k\geq 4$.
    \item A solution that gives only the construction, or only an upper bound, but not both.
\end{enumerate}
\clearpage
}{%
Award $1$ mark to an incomplete solution if it gives a correct proof of the common-residue result
\begin{equation*}
  g\mid a_i-a_j\qquad\text{for all }i,j,
\end{equation*}
or an equivalent statement forcing all the $a_i$ to lie in a single residue class modulo $g$. To receive this mark, the solution must include any coprimality argument it requires, such as first proving $\gcd(g,P)=1$ and then using it to `cancel' $P/(a_ia_j)$ from the divisibility.

Do not award the partial-progress mark for any of the following on its own:
\begin{enumerate}[label=(NPP\arabic*)]
    \item Proving only that $\gcd(g,P)=1$.
    \item Finding or guessing the example with $g=998285$ (including verifying the example works).
    \item Any bounds following from the assertion, rather than proof, that the $a_i$ have a common residue modulo $g$.
    \item Claiming $g\mid a_i-a_j$ from
    \[
      g\mid \frac{P}{a_ia_j}(a_j-a_i)
    \]
    without proving or otherwise justifying the coprimality needed to cancel $P/(a_ia_j)$.
    \item Numerical experimentation, pattern-spotting, checking several examples etc.
\end{enumerate}
}
```

---

## Submission to grade

This is the submission `team_6` for problem `1_DIVALL`, with line numbers
added for reference in your errors log.

```text
  1 | The maximum possible value of \( g \) is achieved by selecting \( k = 4 \) and choosing the numbers \( a_1 = g - 1 \), \( a_2 = 2g - 1 \), \( a_3 = 3g - 1 \), and \( a_4 = 4g - 1 \). These numbers are distinct positive integers, and their sum is \( 10g - 4 \), which must be strictly less than \( 3 \times 10^6 \). This inequality gives \( g < 300,000.4 \), so the largest integer \( g \) is \( 300,000 \).
  2 | 
  3 | For this choice of \( g \), each \( a_i \equiv -1 \pmod{g} \). The product \( P = (g - 1)(2g - 1)(3g - 1)(4g - 1) \). For any \( i \), \( P/a_i \) is the product of three terms each congruent to \( -1 \pmod{g} \), so \( P/a_i \equiv -1 \pmod{g} \). Thus, \( g \) divides \( (P/a_i) + 1 \) for all \( i \). The sum \( 10 \times 300,000 - 4 = 2,999,996 \) is less than \( 3 \times 10^6 \), satisfying the problem's conditions. No larger \( g \) is possible because the sum would exceed the limit.
  4 | 
  5 | \boxed{300000}
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
   - Fill in the header (Problem `1_DIVALL`, Submission `team_6`, your grader
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
   `grade_1_DIVALL_team_6_AI.tex`.
3. **Check it compiles.** Run `pdflatex -interaction=nonstopmode <file>.tex` and fix any
   errors so it builds to a PDF. (Keep the document self-contained — do not add external
   dependencies.)
4. **State the proposed mark** (0/1/6/7) clearly in your final message.

Do **not** commit anything to the repository — return the `.tex` (and its PDF if produced).
