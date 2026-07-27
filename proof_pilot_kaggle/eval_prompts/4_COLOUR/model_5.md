# AIMO Proof Pilot — grading task

You are an **expert olympiad grader** for the AIMO Proof Pilot. Your job is to grade **one**
submission against the official markscheme and return a completed grading sheet as a LaTeX
(`.tex`) file.

- **Problem:** `4_COLOUR`
- **Submission:** `model_5`

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
\section*{Problem 4 (COLOUR)}


\problem[4]{%
Linda and Sue play a game on a $2025\times 2025$ grid of cells. Initially, every cell is grey. Linda moves first, and the players then alternate turns.

On each of Linda's turns, she chooses one cell and paints it lime, regardless of its current colour. On each of Sue's turns, she chooses an axis-aligned $2 \times 2$ block of cells containing at least one grey cell, and paints all four cells scarlet, regardless of their current colours.

After each move, if there are no grey cells left, the game ends immediately. Linda wants to maximise the number of cells whose final colour is lime, and Sue wants to maximise the number of cells whose final colour is scarlet.

\begin{enumerate}[label=\alph*)]
    \item Prove that the game always ends after finitely many moves.
    \item Suppose both players play optimally. Determine the number of lime cells at the end of the game.
\end{enumerate}
}{1026168}

\vspace{2cm}

\textbf{Original AIMO3 Formulation:} 

Linda and Sue play a game on a $2025 \times 2025$ grey square grid as follows. Linda starts by picking a cell of any colour and painting it lime. Then Sue picks a $2 \times 2$ square, at least one of which is grey, and paints all four cells scarlet (including any cells already painted lime). They alternate turns with the game finishing immediately once no cell is grey. Linda wants to maximise the number of lime cells and Sue wants to maximise the number of scarlet cells. If both players play optimally, the game will end with $L$ lime cells. What is the remainder when $L$ is divided by $10^5$?

\textbf{Answer:} 26168

\vspace{1cm}

\textbf{Remark:} Relative to the AIMO3 version, we have made it more explicit how the game progresses, and that the players' objectives are determined by the final colours of the cells. We regard the intended meaning of the original formulation as clear in context, but these small changes remove possible sources of misreading. We have also added part \emph{a)} to make explicit that the game always terminates, so that the optimisation question in part \emph{b)} is well-defined.

\clearpage

\polishedsolution[SB][4]{%
We prove a slightly more general statement. For an $n \times n$ grid with $n \geq 2$, if both players play optimally then the final number of lime cells is
\begin{equation*}
    \left\lceil \frac{n}{2}\right\rceil^2 - 1.
\end{equation*}
Substituting $n=2025$ gives
\begin{equation*}
    L=\left\lceil\frac{2025}{2}\right\rceil^2 - 1=1013^2-1=\boxed{1026168}.
\end{equation*}

We first prove part \emph{a)}. On each of Sue's turns, she is required to choose a $2 \times 2$ square containing at least one grey cell. After she paints the square scarlet, at least one formerly grey cell is no longer grey. Linda's move cannot increase the number of grey cells. Therefore the number of grey cells strictly decreases on every Sue turn, and there are only finitely many grey cells to begin with. Hence the game must end after finitely many turns.

Partition the grid into a grid of $2 \times 2$ squares. If $n$ is odd, as it is in the problem here, extend down and right to a $(n+1) \times (n+1)$ grid and partition there, then restrict to the original grid. We get $\left\lceil\frac{n}{2} \right\rceil^2$ regions which we call \emph{compartments}, each of which has a unique top-left cell which we call \emph{special}. Every $2 \times 2$ square of the grid, not necessarily a compartment, contains exactly one special cell. 

\begin{figure}[H]
    \centering
    \input{../figures/fig_1.tex}
\end{figure}

\textbf{Linda's strategy:} Linda's strategy is to pick a non-special cell on her first move, then for every move after Sue's, to paint the special cell in Sue's previous $2 \times 2$ square lime. First, note that if Sue never paints a fixed special cell, then Linda never does either, so the game will not have ended. Thus, by the time the game has ended, Sue has painted all special cells at least once. Next, note that Linda will always paint over a non-grey cell after her first move, hence Sue makes the last move in order to remove the final grey cell(s). 

Other than the unique special cell in this last $2 \times 2$ square, fix a special cell and consider the last time it is painted scarlet. Immediately after, it is painted lime and remains that way. Thus, other than the last special cell, all special cells are lime, and hence at least $\left\lceil\frac{n}{2}\right\rceil^2 - 1$ are lime at the end.

\textbf{Sue's strategy:} Sue's goal of maximising the number of scarlet cells is the same as minimising the number of lime cells since at the end of the game every cell is coloured one or the other. After Linda's first move, Sue chooses one of the four rotated compartment decompositions such that the lime cell does not lie in its own $1 \times 1$ compartment (which would be the bottom right cell for $n$ odd). Then, Sue picks the compartment containing this lime cell, which necessarily contains a grey cell, and paints a $2 \times 2$ square which covers it (which may overlap a neighbouring compartment if the chosen compartment lies on the boundary). On Sue's subsequent turns, she selects any compartment with a grey cell and paints a legal $2 \times 2$ square covering that compartment.

After Sue picks a compartment, she will not pick it again as it does not contain any grey cells. Hence, the game ends on or before Sue's $\left\lceil\frac{n}{2}\right\rceil^2$th move. Thus, there are at most as many lime cells remaining as there are Linda moves after Sue's first move, hence at most $\left\lceil\frac{n}{2}\right\rceil^2 - 1$ lime cells.

Putting these together gives the required value for $L$.
}

\clearpage

\markscheme{
Let $M=1013^2-1$, the correct value of $L$.

A solution is \emph{essentially complete} if it proves that the game always terminates and proves that $L \in \{M-1,M,M+1\}$. This requires providing and proving a strategy for Linda to obtain at least $M-1$ lime cells and a strategy for Sue to restrict Linda to at most $M+1$ lime cells.

An essentially complete solution that fails to prove the exact value $L=M$ should score $6$ marks.

An essentially complete solution should also receive $6$ rather than $7$ if it contains a minor error or omission: a gap which is not merely a small arithmetic slip, but which can be repaired without changing the main structure of the solution. Examples include:
\begin{enumerate}[label=(ME\arabic*)]
    \item In Linda's strategy, failing to explain why all special cells except possibly the one in Sue's final square are lime at the end.
    \item In Sue's strategy, failing to justify that boundary compartments can be covered by legal $2\times2$ squares.
    \item In Sue's strategy, failing to explain why Linda's first lime cell is overwritten on Sue's first move.
    \item Making a fixable off-by-one error in counting Sue's compartment-clearing moves or Linda's remaining moves, while the intended strategy and final value are otherwise clear.
\end{enumerate}

We generally will not penalise minor arithmetic mistakes unless they are integral to the solution. The final answer may be left as a basic arithmetic expression, such as $1013^2-1$; it does not have to be explicitly calculated as $1026168$ to score full marks.
}{%
If a solution is not essentially complete, it should score $1$ if it proves at least one of the following substantial one-sided results.

\begin{enumerate}[label=(PP\arabic*)]
    \item A valid Linda strategy guaranteeing at least
    \begin{equation*}
        \left\lfloor \frac{2025}{2} \right\rfloor^2-1=1012^2-1=1024143
    \end{equation*}
    lime cells at the end. For example, this might be a correct special-cell strategy on a $2024\times2024$ sub-board, even if it does not handle the last row and column sharply.

    \item A valid Sue strategy guaranteeing at most
    \begin{equation*}
        \left\lceil \frac{2025}{2} \right\rceil^2=1013^2=1026169
    \end{equation*}
    lime cells at the end. For example, this might be a compartment-clearing strategy with a remaining unresolved off-by-one.
\end{enumerate}

The following do \emph{not} count as significant partial progress on their own.

\begin{enumerate}[label=(NPP\arabic*)]
    \item Proving only that the game terminates.
    \item Stating the correct answer, or the correct expression $1013^2-1$, without a proof of optimality.
    \item Checking small cases or giving numerical evidence without a strategy for the $2025\times2025$ board.
    \item Giving only trivial bounds, such as $0\leq L\leq2025^2$.
    \item Describing a $2\times2$ tiling of the board without deriving a substantial lower or upper bound from it.
    \item Giving a strategy that works only if the opponent cooperates, rather than against every legal move of the opponent.
\end{enumerate}
}
```

---

## Submission to grade

This is the submission `model_5` for problem `4_COLOUR`, with line numbers
added for reference in your errors log.

```text
  1 | Let
  2 | \[
  3 | N=2025^2
  4 | \]
  5 | be the total number of cells.
  6 | 
  7 | ### a) The game always terminates
  8 | 
  9 | The number of grey cells never increases. Moreover, on every one of Sue’s turns, her chosen (2\times2) block contains at least one grey cell, and all four cells are painted scarlet. Hence the number of grey cells decreases by at least (1) on every Sue turn.
 10 | 
 11 | Consequently, Sue can make at most (N) moves. Since the players alternate, the entire game has at most (2N) moves and therefore always ends after finitely many moves.
 12 | 
 13 | ### b) The optimal number of lime cells
 14 | 
 15 | Set
 16 | [
 17 | m=\frac{2025+1}{2}=1013.
 18 | ]
 19 | We will prove that the value of the game is
 20 | [
 21 | m^2-1=1013^2-1=1,026,168.
 22 | ]
 23 | 
 24 | #### Linda can guarantee at least (m^2-1) lime cells
 25 | 
 26 | Let
 27 | [
 28 | P={(r,c): r\text{ and }c\text{ are both odd}}.
 29 | ]
 30 | There are (1013) odd-numbered rows and (1013) odd-numbered columns, so
 31 | [
 32 | |P|=1013^2=m^2.
 33 | ]
 34 | 
 35 | Every axis-aligned (2\times2) block contains exactly one cell of (P), since two consecutive rows contain exactly one odd row and two consecutive columns contain exactly one odd column.
 36 | 
 37 | Linda uses the following strategy:
 38 | 
 39 | 1. On her first turn, she paints any cell of (P) lime.
 40 | 2. After each nonterminal move by Sue, let (p) be the unique cell of (P) in the (2\times2) block just painted by Sue. Linda repaints (p) lime.
 41 | 
 42 | After Linda’s first turn, all her moves repaint a cell that Sue has just painted scarlet, so these moves do not remove any grey cells. Thus the eventual terminal move is made by Sue.
 43 | 
 44 | Consider the final (2\times2) block painted by Sue, and let (p_{\mathrm{last}}) be its unique cell in (P). This cell is scarlet at the end. We claim that every other cell of (P) is lime.
 45 | 
 46 | Indeed, take (p\in P\setminus{p_{\mathrm{last}}}).
 47 | 
 48 | * If Sue never painted (p), then (p) must be the cell Linda painted on her first turn; otherwise it would still be grey when the game ended. Hence it is lime.
 49 | * If Sue painted (p), consider the last Sue move whose block contained (p). This was not the terminal move, because (p\ne p_{\mathrm{last}}). Linda therefore immediately repainted (p) lime, and no later Sue move affected it.
 50 | 
 51 | Thus all (m^2-1) cells of (P\setminus{p_{\mathrm{last}}}) are lime. Therefore Linda can guarantee at least
 52 | [
 53 | m^2-1
 54 | ]
 55 | lime cells.
 56 | 
 57 | #### Sue can guarantee at most (m^2-1) lime cells
 58 | 
 59 | Construct the following family of row-pairs:
 60 | [
 61 | {1,2},{3,4},\ldots,{2023,2024},{2024,2025}.
 62 | ]
 63 | There are (1013=m) such pairs, and together they cover every row. Construct the analogous (m) column-pairs.
 64 | 
 65 | Taking every Cartesian product of one row-pair and one column-pair gives a family (\mathcal B) of
 66 | [
 67 | m^2
 68 | ]
 69 | axis-aligned (2\times2) blocks whose union covers the entire board.
 70 | 
 71 | Sue plays as follows.
 72 | 
 73 | * After Linda’s first move, Sue chooses a block of (\mathcal B) containing Linda’s chosen cell and paints it scarlet. This is legal because the other three cells of the block are still grey.
 74 | * Thereafter, whenever grey cells remain, Sue chooses any grey cell and paints an unused block of (\mathcal B) containing it.
 75 | 
 76 | Such an unused block always exists. Indeed, every cell belongs to at least one block of (\mathcal B). A grey cell cannot belong to a block that Sue has already used, because when that block was used the cell became scarlet, and cells never become grey again.
 77 | 
 78 | Thus Sue uses each block of (\mathcal B) at most once, so she makes at most (m^2) moves. Furthermore, Linda’s very first lime mark is immediately overwritten.
 79 | 
 80 | Let (T) be the total number of Linda moves. Every cell that is lime at the end has a distinct last Linda move on which it was painted. None of these last moves can be Linda’s first move, since that mark was overwritten immediately. Hence
 81 | [
 82 | #{\text{final lime cells}}\le T-1.
 83 | ]
 84 | 
 85 | There are two possible ways the game ends.
 86 | 
 87 | * If it ends after Sue’s (s)-th move, then Linda has made (T=s) moves and (s\le m^2). Hence
 88 |   [
 89 |   #{\text{lime cells}}\le s-1\le m^2-1.
 90 |   ]
 91 | * If it ends after Linda’s move following Sue’s (s)-th move, then (T=s+1). In this case (s\le m^2-1), because if Sue had already used all (m^2) blocks, their union would cover the board and the game would have ended on Sue’s preceding move. Therefore
 92 |   [
 93 |   #{\text{lime cells}}\le T-1=s\le m^2-1.
 94 |   ]
 95 | 
 96 | So Sue can ensure that there are at most (m^2-1) lime cells.
 97 | 
 98 | The two bounds coincide. Therefore, under optimal play, the final number of lime cells is
 99 | [
100 | \boxed{1013^2-1=\boxed{1,026,168}}.
101 | ]
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
   - Fill in the header (Problem `4_COLOUR`, Submission `model_5`, your grader
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
   `grade_4_COLOUR_model_5_AI.tex`.
3. **Check it compiles.** Run `pdflatex -interaction=nonstopmode <file>.tex` and fix any
   errors so it builds to a PDF. (Keep the document self-contained — do not add external
   dependencies.)
4. **State the proposed mark** (0/1/6/7) clearly in your final message.

Do **not** commit anything to the repository — return the `.tex` (and its PDF if produced).
