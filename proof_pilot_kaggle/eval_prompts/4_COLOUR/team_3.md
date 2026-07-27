# AIMO Proof Pilot — grading task

You are an **expert olympiad grader** for the AIMO Proof Pilot. Your job is to grade **one**
submission against the official markscheme and return a completed grading sheet as a LaTeX
(`.tex`) file.

- **Problem:** `4_COLOUR`
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

This is the submission `team_3` for problem `4_COLOUR`, with line numbers
added for reference in your errors log.

```text
  1 | ## Solution  
  2 | 
  3 | ### Part (a) – The game always ends  
  4 | 
  5 | Let \(G\) be the set of grey cells.  
  6 | * **Linda’s move:** She chooses one cell. If that cell is grey, it is removed from \(G\); otherwise \(G\) stays the same.  
  7 | * **Sue’s move:** She chooses a \(2\times2\) block that contains at least one grey cell. All four cells of the block become scarlet, so every grey cell in the block is removed from \(G\). Hence \(|G|\) decreases by at least \(1\).
  8 | 
  9 | Thus on every move \(|G|\) does not increase, and on every move of Sue it strictly decreases.  
 10 | If at some moment \(|G|>0\), then any grey cell belongs to at least one \(2\times2\) block (because the grid is at least \(2\times2\) in every direction). Therefore Sue always has a legal move as long as \(|G|>0\).  
 11 | 
 12 | Suppose the game were to continue indefinitely. Then \(|G|\) would never reach \(0\), but Sue’s moves would keep reducing \(|G|\) whenever she plays. Even if Linda occasionally paints a non‑grey cell (which does not change \(|G|\)), Sue will still get turns and reduce \(|G|\). Since \(|G|\) is a non‑negative integer, it can be reduced only a finite number of times. Consequently after a finite number of moves \(|G|\) must become \(0\), and the game ends. ∎  
 13 | 
 14 | ---
 15 | 
 16 | ### Part (b) – Number of lime cells under optimal play  
 17 | 
 18 | We will prove that the value of the game (the number of lime cells when both players play optimally) is exactly \(3\).  
 19 | 
 20 | The grid is \(2025\times2025\); we use coordinates \((i,j)\) with \(0\le i,j\le 2024\).  
 21 | 
 22 | #### 1. Lower bound – Linda can guarantee at least \(3\) lime cells  
 23 | 
 24 | Linda chooses three cells that are **pairwise not contained in any common \(2\times2\) block**.  
 25 | A convenient choice is  
 26 | \[
 27 | A=(0,0),\qquad B=(0,2),\qquad C=(2,0).
 28 | \]  
 29 | Indeed, any \(2\times2\) block spans at most two consecutive rows and two consecutive columns, so it cannot contain two cells whose row indices differ by \(2\) or whose column indices differ by \(2\); hence each block contains at most one of \(A,B,C\).  
 30 | 
 31 | Linda’s strategy is to force the game to end with these three cells turning lime.  
 32 | She proceeds in two phases:
 33 | 
 34 | * **Phase 1** – She paints grey cells that are not among \(\{A,B,C\}\) whenever possible. The goal is to drive the board to a situation where the only remaining grey cells are exactly \(A,B,C\) (all other cells are already scarlet). Because no block contains two of these three, Sue can never turn two of them into scarlet in a single move.
 35 | 
 36 | * **Phase 2** – When only \(A,B,C\) are grey, the game reduces to a small subgame. Linda now paints these cells one by one. After she paints one, say \(A\), it becomes lime while \(B,C\) stay grey. Sue, on her turn, must choose a \(2\times2\) block that contains at least one grey cell. Because any block containing \(A\) cannot contain \(B\) or \(C\) (by the choice of the cells), such a block would have no grey cells if the other three cells are already scarlet. To keep the invariant that the other three cells are scarlet, Linda ensures that before each of her moves all cells except \(A,B,C\) are scarlet. Then Sue is forced to pick a block that contains \(B\) or \(C\). She paints that block, turning the contained grey cell into scarlet and possibly turning any lime cells inside the block (but by construction the only lime cell in that block would be the one just painted by Linda, and it will be turned to scarlet).  
 37 | 
 38 | Now \(B\) (or \(C\)) becomes scarlet, but it can be repainted lime on Linda’s next turn. Since Sue can only affect one of the three target cells at a time, Linda can always recover any cell that Sue turns to scarlet before the game ends. Moreover, the turn order can be managed so that after the last grey cell is eliminated, the three cells \(A,B,C\) are all lime.  
 39 | 
 40 | A more formal induction on the number of grey cells shows that Linda can enforce this plan. Consequently she can ensure at least three lime cells at the end.  
 41 | 
 42 | #### 2. Upper bound – Sue can guarantee at most \(3\) lime cells  
 43 | 
 44 | Sue uses a strategy that confines the game to a small region and then limits the lime count inside that region.  
 45 | 
 46 | * **Partition the board.** Consider the \(2025\times2025\) grid. Because the board is large, Sue can mentally partition it into four quadrants by splitting rows and columns at index \(1012\). She will work to turn all cells outside a central \(3\times3\) block into scarlet.  
 47 | 
 48 | * **Turning the outside into scarlet.** Whenever Linda creates a lime cell (or any non‑grey cell) outside the central \(3\times3\) region, Sue responds by choosing a \(2\times2\) block that contains that cell and at least one grey cell. She paints that block, which makes all four cells scarlet. By repeatedly applying this tactic, she can gradually scarlet the whole outside region. Because each such block eliminates at least one grey cell and turns the lime cell (if present) to scarlet, the process terminates with all cells outside the \(3\times3\) region becoming scarlet.  
 49 | 
 50 | * **Handling the central \(3\times3\) region.** Once the outside is all scarlet, the game effectively reduces to a \(3\times3\) board. On a \(3\times3\) board we have already determined (by exhaustive analysis or by the small‑case results given in the problem statement) that the second player (Sue) can force at most three lime cells. Sue now follows the optimal \(3\times3\) strategy inside this subgrid, while keeping the outside already scarlet.  
 51 | 
 52 | An invariant can be maintained: after each of Sue’s moves,  
 53 | - every cell outside the \(3\times3\) central block is scarlet,  
 54 | - the number of lime cells inside the central \(3\times3\) block is at most \(3\).  
 55 | 
 56 | She can keep this invariant by responding appropriately to Linda’s moves. If Linda paints a cell inside the central block, Sue chooses a block inside that block that contains at least one grey cell and that reduces the lime count as much as possible (following the \(3\times3\) optimal strategy). If Linda paints a cell outside the central block, Sue immediately scarelts it using a block that also contains a grey cell, preserving the invariant.  
 57 | 
 58 | Since the invariant guarantees that the total number of lime cells never exceeds three, Sue can ensure that the final number is at most three.  
 59 | 
 60 | #### 3. Conclusion  
 61 | 
 62 | Linda can force at least three lime cells, and Sue can force at most three lime cells. Therefore, under optimal play the number of lime cells at the end is exactly \(3\).  
 63 | 
 64 | \[
 65 | \boxed{3}
 66 | \]
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
   - Fill in the header (Problem `4_COLOUR`, Submission `team_3`, your grader
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
   `grade_4_COLOUR_team_3_AI.tex`.
3. **Check it compiles.** Run `pdflatex -interaction=nonstopmode <file>.tex` and fix any
   errors so it builds to a PDF. (Keep the document self-contained — do not add external
   dependencies.)
4. **State the proposed mark** (0/1/6/7) clearly in your final message.

Do **not** commit anything to the repository — return the `.tex` (and its PDF if produced).
