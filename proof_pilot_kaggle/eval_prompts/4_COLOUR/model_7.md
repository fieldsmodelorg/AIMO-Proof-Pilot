# AIMO Proof Pilot — grading task

You are an **expert olympiad grader** for the AIMO Proof Pilot. Your job is to grade **one**
submission against the official markscheme and return a completed grading sheet as a LaTeX
(`.tex`) file.

- **Problem:** `4_COLOUR`
- **Submission:** `model_7`

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

This is the submission `model_7` for problem `4_COLOUR`, with line numbers
added for reference in your errors log.

```text
  1 | PROBLEM
  2 | =======
  3 | Linda and Sue play a game on a 2025 x 2025 grid of cells.  Initially every
  4 | cell is grey.  Linda moves first and the players alternate.
  5 | 
  6 |   * On Linda's turn she chooses one cell and paints it LIME (whatever its
  7 |     current colour).
  8 |   * On Sue's turn she chooses an axis-aligned 2x2 block containing at least one
  9 |     grey cell and paints all four of its cells SCARLET (whatever their colours).
 10 | 
 11 | After each move, if no grey cell remains the game ends immediately.  Linda wants
 12 | to maximise the number of LIME cells at the end, Sue the number of SCARLET cells.
 13 | 
 14 |   (a) Prove the game always ends after finitely many moves.
 15 |   (b) With optimal play, determine the number of lime cells at the end.
 16 | 
 17 | Throughout write n = 2025 (n is odd) and N = n^2 for the number of cells.  A
 18 | cell is "coloured" if it is lime or scarlet, i.e. not grey.
 19 | 
 20 | 
 21 | ==============================================================================
 22 | PART (a):  THE GAME TERMINATES
 23 | ==============================================================================
 24 | 
 25 | Key monotonicity observation.
 26 | -----------------------------
 27 | No move ever creates a grey cell:
 28 | 
 29 |   * Linda only paints a cell LIME, which is not grey.
 30 |   * Sue only paints cells SCARLET, which is not grey.
 31 | 
 32 | Hence the set G of grey cells never gains an element; it can only lose
 33 | elements.  In particular the number |G| of grey cells is non-increasing
 34 | throughout the whole game.
 35 | 
 36 | Sue's moves strictly decrease |G|.
 37 | ----------------------------------
 38 | On any turn of Sue the rules require her chosen 2x2 block to contain at least
 39 | one grey cell.  She paints all four cells scarlet, so that grey cell (and
 40 | possibly more) becomes scarlet.  Therefore EVERY move of Sue decreases |G| by
 41 | at least 1.
 42 | 
 43 | Sue can always move while grey cells remain.
 44 | --------------------------------------------
 45 | If a grey cell exists, it lies in at least one axis-aligned 2x2 block (every
 46 | cell of an n x n board with n >= 2 belongs to some 2x2 block).  That block
 47 | contains a grey cell, so it is a legal choice for Sue.  Thus whenever it is
 48 | Sue's turn and the game has not already ended, she has a legal move.
 49 | 
 50 | Termination.
 51 | ------------
 52 | Start with |G| = N = n^2.  Consider the moves of Sue, in order.  Each of them
 53 | decreases the (always non-negative, integer) quantity |G| by at least 1, and
 54 | |G| is never increased by Linda's moves in between.  Consequently Sue can make
 55 | at most N moves in the entire game: after at most N of her moves we would have
 56 | |G| = 0 and the game would already have ended.
 57 | 
 58 | Since the players alternate and Linda starts, the total number of moves is at
 59 | most 2N + 1.  In particular the game ends after finitely many moves.          [].
 60 | 
 61 | 
 62 | ==============================================================================
 63 | PART (b)
 64 | ==============================================================================
 65 | 
 66 | Because the game ends exactly when no grey cell remains, at the end every cell
 67 | is either lime or scarlet, so
 68 | 
 69 |         (lime cells at end) + (scarlet cells at end) = N.
 70 | 
 71 | Thus maximising lime is the same as minimising scarlet: the game is a zero-sum
 72 | game with a well-defined value, and "Linda maximises lime" while "Sue maximises
 73 | scarlet" are exactly opposite objectives.  Let V(n) denote the number of lime
 74 | cells under optimal play.  We determine the order of growth of V(n) exactly and
 75 | describe the optimal strategies.
 76 | 
 77 | ------------------------------------------------------------------------------
 78 | 1.  THE SAFE-CELL LEMMA  (the structural heart of the problem)
 79 | ------------------------------------------------------------------------------
 80 | For a cell p let N[p] be its closed king-neighbourhood: p together with all
 81 | cells sharing a side or a corner with p (the 3x3 square centred at p, truncated
 82 | at the border).  Equivalently, N[p] is the union of all 2x2 blocks that contain
 83 | p, because each such block consists of p and three of its king-neighbours.
 84 | 
 85 | LEMMA (Safe cells).  Suppose at some moment every cell of N[p] is coloured (no
 86 | grey cell in N[p]).  Then for the rest of the game Sue can never repaint p.
 87 | 
 88 | Proof.  Sue may repaint p only by choosing a 2x2 block B that contains p.
 89 | Every such B is contained in N[p].  By hypothesis N[p] has no grey cell, so B
 90 | has no grey cell, hence B is not a legal choice for Sue.  Moreover, grey cells
 91 | never reappear (Part (a)), so N[p] stays grey-free forever.  Therefore no legal
 92 | Sue-block ever contains p again.                                              []
 93 | 
 94 | Call p RIPE (at a given moment) if N[p] contains no grey cell.  By the lemma,
 95 | once p is ripe it can never be scarleted again; so if Linda paints p lime at or
 96 | after the moment it becomes ripe, p is lime forever.  We say Linda has SECURED
 97 | p.  Conversely, a cell can change colour only while it is not ripe.
 98 | 
 99 | Two immediate consequences:
100 | 
101 |   (S1) Ripeness is monotone: once a cell is ripe it stays ripe (grey never
102 |        returns), and the set of ripe cells only grows, from empty to all cells.
103 | 
104 |   (S2) Vulnerability.  If p is NOT ripe, some cell q in N[p] is grey; the 2x2
105 |        block containing both p and q is then legal for Sue, so Sue CAN repaint
106 |        p scarlet in one move.  Hence any lime cell that is not yet ripe can be
107 |        destroyed by Sue immediately.
108 | 
109 | Thus the final lime cells are precisely the cells Linda paints lime while they
110 | are ripe (equivalently, cells that are lime at the first instant they become
111 | ripe and are never re-limed-then-lost, which cannot happen after ripeness).
112 | The whole of part (b) is the combinatorics of who controls the growth of the
113 | ripe region.
114 | 
115 | ------------------------------------------------------------------------------
116 | 2.  THE ANSWER IS QUADRATIC IN n  (so the small cases are misleading)
117 | ------------------------------------------------------------------------------
118 | It is tempting to compute small boards.  Exact game-tree search gives
119 | 
120 |         V(1)=1, V(2)=0, V(3)=3, V(4)=3.
121 | 
122 | These tiny values are deceptive: they are dominated by border effects.  We now
123 | prove that V(n) grows like a constant times n^2; in particular V(n) is NOT
124 | O(n) and the small-board values do not extrapolate.
125 | 
126 | LEMMA (Lower bound, order n^2).  V(n) >= n^2/45 for all large n.
127 | 
128 | Proof.  Two facts.
129 | 
130 | (i)  The game lasts at least n^2/5 rounds.  Indeed in one round Linda colours
131 |      at most 1 grey cell and Sue at most 4, so |G| drops by at most 5 per
132 |      round.  Starting from |G| = n^2 it takes at least n^2/5 rounds to reach
133 |      |G| = 0.  In particular Linda makes at least n^2/5 moves.
134 | 
135 | (ii) Linda can secure any chosen cell p using at most 10 of her own moves,
136 |      regardless of Sue.  She simply paints, one per turn, the (at most 8)
137 |      king-neighbours of p that are still grey; once a cell is coloured it stays
138 |      coloured (Part (a)), and Sue cannot restore grey, so after at most 8 such
139 |      moves the eight neighbours of p are all coloured.  One more Linda move
140 |      paints p itself lime.  At that instant N[p] is grey-free, so p is ripe and
141 |      lime; by the Safe-cell Lemma it is lime forever.  (If Sue happens to
142 |      scarlet p in between, Linda needs one extra move to re-lime the now-ripe
143 |      p, still at most 10 moves total.)
144 | 
145 | Now Linda fixes a family of disjoint 3x3 squares (there are floor(n/3)^2 of
146 | them) and secures their centres one at a time using the routine in (ii); the
147 | routine for one centre only ever paints cells of its own 3x3 square, so the
148 | routines do not interfere.  Each secured centre costs <= 10 Linda-moves and the
149 | 9 cells it touches contain at most 5 grey cells removed by Linda plus at most
150 | 4*10 removed by Sue meanwhile, i.e. at most 45 grey cells leave the board per
151 | secured centre; so as long as fewer than n^2/45 centres are done, grey cells
152 | remain and the game continues.  Hence Linda secures at least n^2/45 cells:
153 | V(n) >= n^2/45.                                                               []
154 | 
155 | LEMMA (Upper bound, order n^2).  V(n) <= 3n^2/4 trivially, and Sue can do far
156 | better: with the "spread" strategy below she keeps a constant fraction of the
157 | board scarlet, so V(n) <= c n^2 with c < 1.  (Made precise in Section 3.)
158 | 
159 | Together these show V(n) = Theta(n^2).  In particular the value for n = 2025 is
160 | a quadratic-sized number, not a small constant, and the n <= 4 data are pure
161 | boundary phenomena.
162 | 
163 | ------------------------------------------------------------------------------
164 | 3.  OPTIMAL STRATEGIES AND THE EXACT VALUE
165 | ------------------------------------------------------------------------------
166 | By Section 1 the game reduces to the following "ripening race".  Colouring is
167 | monotone, so think of the board being gradually coloured from all-grey to
168 | all-coloured.  A cell becomes ripe when the last grey cell of its 3x3
169 | neighbourhood is coloured; from then on only Linda can change it, and she will
170 | make it lime.  Linda secures one ripe cell per move; she may instead spend a
171 | move colouring a grey cell to MAKE cells ripen sooner.  Sue colours four cells
172 | per move (overwriting any non-ripe limes, by (S2)) and chooses WHERE, hence she
173 | controls how fast and in what pattern cells ripen.  The two opposing strategies
174 | are:
175 | 
176 | Linda's strategy (lower bound).  Linda never wastes a turn on an already-ripe
177 | lime.  Priority 1: if some ripe cell is not lime, lime it (this is permanent).
178 | Priority 2 (no ripe cell available): colour a still-grey cell that maximises the
179 | number of cells that thereby become ripe, building solid coloured blocks whose
180 | interiors ripen.  Building a solid k x k coloured block costs about k^2 colour
181 | moves and ripens its (k-2)^2 interior cells, an asymptotic ratio 1, so Linda
182 | converts essentially all of her many moves into secured cells.
183 | 
184 | Sue's strategy (upper bound).  Sue keeps the grey set a "king-dominating" set
185 | for as long as possible: she colours four grey cells per move but always so that
186 | the remaining grey cells still touch (within a king-step) every uncoloured
187 | region, so that NO cell is ripe.  Concretely she keeps grey on the cells whose
188 | row or column is divisible by 3 (the "walls"), colouring only the interiors of
189 | the 2x2 "patches" between the walls.  While the walls survive, every cell has a
190 | grey cell within king-distance 1, so the ripe set is empty and Linda secures
191 | nothing; only when the walls must finally be eaten do cells ripen, and Sue eats
192 | them so as to ripen as few cells per move as possible.  This keeps a definite
193 | fraction of the board scarlet.
194 | 
195 | These two strategies pin V(n) to a constant times n^2.  Carrying the ripening
196 | race out exactly (balancing Linda's "build-and-harvest" rate against the speed
197 | at which Sue is forced to dismantle her king-dominating wall set) yields, for
198 | n = 2025,
199 | 
200 |         V(2025) = 1025156  =  1012 * 1013  =  (2025^2 - 1)/4 .
201 | 
202 | Equivalently, with optimal play Linda secures a quarter of the board:
203 | lime = (n^2 - 1)/4 and scarlet = (3n^2 + 1)/4.  The "1/4" is the two-dimensional
204 | analogue of the one-dimensional version of this game (Sue's block a 1x2 domino),
205 | which is exactly solvable and has value floor((n-1)/2) ~ n/2 per dimension; the
206 | 2x2 block squares this to ~ n^2/4.
207 | 
208 | ==============================================================================
209 | ANSWER
210 | ==============================================================================
211 | (a)  The game always terminates (each Sue move strictly decreases the number of
212 |      grey cells, which is a non-negative integer never increased by Linda, so
213 |      Sue makes at most n^2 moves and the game lasts at most 2n^2+1 moves).
214 | 
215 | (b)  With optimal play the number of lime cells is
216 | 
217 |                     (2025^2 - 1)/4  =  1012 * 1013  =  1025156 .
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
   - Fill in the header (Problem `4_COLOUR`, Submission `model_7`, your grader
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
   `grade_4_COLOUR_model_7_AI.tex`.
3. **Check it compiles.** Run `pdflatex -interaction=nonstopmode <file>.tex` and fix any
   errors so it builds to a PDF. (Keep the document self-contained — do not add external
   dependencies.)
4. **State the proposed mark** (0/1/6/7) clearly in your final message.

Do **not** commit anything to the repository — return the `.tex` (and its PDF if produced).
