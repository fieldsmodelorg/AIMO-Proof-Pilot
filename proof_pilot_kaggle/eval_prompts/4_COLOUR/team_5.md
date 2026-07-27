# AIMO Proof Pilot — grading task

You are an **expert olympiad grader** for the AIMO Proof Pilot. Your job is to grade **one**
submission against the official markscheme and return a completed grading sheet as a LaTeX
(`.tex`) file.

- **Problem:** `4_COLOUR`
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

This is the submission `team_5` for problem `4_COLOUR`, with line numbers
added for reference in your errors log.

```text
  1 | ### Part (a): Finiteness
  2 | Initially every cell is grey, so there are \(2025\times 2025 = n^2\) grey cells (with \(n=2025\)).  
  3 | On each of Sue’s turns she must choose a \(2\times 2\) block that contains at least one grey cell and paint all four cells scarlet. Hence at least one grey cell becomes non‑grey, so the number of grey cells strictly decreases.  
  4 | On Linda’s turns she may paint a grey cell (reducing the number of grey cells) or a non‑grey cell (leaving the number unchanged). Therefore the number of grey cells never increases and decreases by at least \(1\) on every Sue turn.  
  5 | Since the number of grey cells starts at \(n^2\) and cannot become negative, after at most \(n^2\) Sue turns the number would have to drop to \(0\). The turns alternate, so the total number of moves is bounded by \(2n^2+1\). In particular the game always ends after finitely many moves.
  6 | 
  7 | ### Part (b): Optimal outcome – exactly one lime cell
  8 | We claim that under optimal play the final configuration contains **exactly one lime cell**.
  9 | 
 10 | We first prove that Linda can force at least one lime cell.  
 11 | Then we show that Sue can force at most one lime cell.  
 12 | Together they give the value \(1\).
 13 | 
 14 | ---
 15 | 
 16 | #### 1. Lower bound – Linda can obtain at least one lime cell
 17 | 
 18 | Linda’s strategy is very simple: she always paints any grey cell (as long as one exists). We analyse the outcome assuming this strategy and that Sue plays optimally (trying to minimise the number of lime cells).  
 19 | 
 20 | Consider the game state at the moment just before Linda’s move. If there is a grey cell that is *isolated* – i.e. every \(2\times2\) block containing it has all other three cells already painted (non‑grey) – then Linda can paint such a grey cell \(c\). After her move the cell \(c\) becomes lime and, because every block containing \(c\) already consisted of non‑grey cells before her move, no future move (by Sue or Linda) can ever affect \(c\) again. Hence \(c\) stays lime till the end, giving at least one lime cell.  
 21 | 
 22 | If, on the other hand, before Linda’s move every grey cell has at least one other grey cell in some \(2\times2\) block, then Linda paints any grey cell. Let \(c\) be the cell she paints. There exists another grey cell \(d\) such that \(c\) and \(d\) lie together in some \(2\times2\) block \(B\). On her very next turn Sue can choose exactly that block \(B\) (it contains the grey cell \(d\), so the move is legal). She paints all four cells of \(B\) scarlet; this makes \(c\) (and \(d\)) non‑grey, and overwrites any previous colour of \(c\).  
 23 | 
 24 | Thus, as long as before Linda’s turn no grey cell is isolated, Sue can immediately reply by painting a block that contains the cell Linda just painted and another grey cell. Consequently the cell Linda painted will never be the last to be painted – it becomes scarlet at Sue’s next turn and stays non‑grey forever.  
 25 | 
 26 | Now observe that the board size \(n=2025\) is odd. Initially every grey cell has many grey neighbours; after each full round (Linda + Sue) the set of grey cells shrinks. We argue that **it is impossible for Sue to keep the “no isolated grey cell” situation forever**. Because if she could, then every grey cell would always have a grey neighbour, meaning the grey cells would form a connected subgraph of the king‑move graph (where two cells are adjacent iff their row and column differ by at most \(1\)). But the grid is finite and the grey set shrinks; eventually the only way to avoid an isolated grey cell would be to have exactly two grey cells that are neighbours (adjacent in a block) or exactly one grey cell. In the latter case, before Linda’s turn there would be a single grey cell – that cell is trivially isolated (no other grey cell exists) – and Linda could paint it, turning it into a lime and ending the game immediately (or at least creating a lime that cannot be overwritten because no grey cells remain to help Sue). In the former case, when only two neighbouring grey cells remain, Linda can paint one of them. After her move only one grey cell remains, and it is isolated (its only possible block‑mates are now non‑grey). Sue’s next turn must use a block containing that last grey cell; but any such block contains only non‑grey cells besides that one, so she can paint it and turn it scarlet. However, the cell Linda painted remains lime – it is not in any block containing the remaining grey cell, and the game ends after Sue’s move. Thus Linda obtains exactly one lime.  
 27 | 
 28 | More formally, we can prove by induction on the number of grey cells that if Sue could maintain “no isolated grey cell” until only two grey cells remain, those two must be neighbours. Then Linda paints one of them, leaving one isolated grey cell. Sue paints that last grey cell (making it scarlet) and the game ends; the cell Linda painted is now the only lime. Hence Linda always secures at least one lime.  
 29 | 
 30 | ---
 31 | 
 32 | #### 2. Upper bound – Sue can force at most one lime cell
 33 | 
 34 | Now we describe a strategy for Sue that guarantees that at the end there is **at most one** lime cell.
 35 | 
 36 | Sue will maintain the following invariant after each of her turns:
 37 | 
 38 | > **Invariant:** Before Linda’s turn, every grey cell has at least one grey neighbour (i.e., for each grey cell \(c\) there exists a grey cell \(d\) such that \(c\) and \(d\) belong to a common \(2\times2\) block).
 39 | 
 40 | Initially this holds because the whole grid is grey.  
 41 | 
 42 | Assume the invariant holds at the start of Linda’s turn. Linda paints some cell \(c\). If \(c\) was grey, the invariant may be broken after her move (the removed cell \(c\) is gone). If \(c\) was already non‑grey, the invariant remains unchanged and we proceed directly to Sue’s reply.
 43 | 
 44 | We consider two cases.
 45 | 
 46 | *Case 1.* Before Linda’s turn there was **no isolated grey cell** (this is exactly the invariant).  
 47 | Then after Linda’s move, suppose the grey cell \(c\) she painted (if she painted a grey cell) has become non‑grey. Could any grey cell now be isolated? Yes – a neighbour of \(c\) might lose its only grey neighbour. However, we will show that Sue can repair the invariant on her next turn.
 48 | 
 49 | If after Linda’s move there exists an isolated grey cell \(d\), Sue can immediately choose any \(2\times2\) block \(B\) that contains \(d\). Such a block exists because \(d\) is grey, and the block may consist of \(d\) and three non‑grey cells (that is allowed because the block must contain at least one grey cell). She paints \(B\) scarlet, which removes \(d\) from the grey set and possibly other cells (but there are none because \(d\) was isolated). This removes exactly one grey cell, and it is the only one that could have been isolated. After this move, the invariant is restored: every remaining grey cell still has at least one grey neighbour. Indeed, if a remaining grey cell \(e\) had become isolated because it relied on \(d\) as its only grey neighbour, then after \(d\) is removed it would have no grey neighbour – but then it would itself be isolated. However, such an \(e\) cannot exist, because if there were two isolated grey cells \(d\) and \(e\), then \(d\) and \(e\) would be at distance at least \(2\) (they cannot be in a common block, otherwise they would not be isolated). But after Linda’s move, the total number of grey cells is at most the number before Linda’s turn minus one (if she painted a grey) or unchanged. Since before Linda’s turn there were no isolated cells, it is impossible that two cells become isolated simultaneously – removing one grey cell can create at most one isolated grey cell. Therefore after Sue removes that isolated cell (if any) the invariant is satisfied again.
 50 | 
 51 | If after Linda’s move **no isolated grey cell** exists (this can happen only if Linda painted a non‑grey cell, or if the removal of \(c\) did not create any isolated cells), then every grey cell still has a grey neighbour. In that situation Sue chooses a block \(B\) that contains two grey cells (such a block exists because we can take a block that contains any grey cell and its neighbour). She paints \(B\) scarlet, removing at least those two grey cells. This removal may create new isolated cells, but as argued above, at most one isolated cell can appear. Sue will handle it on her next turn if necessary, restoring the invariant.
 52 | 
 53 | *Case 2.* Before Linda’s turn there **is an isolated grey cell**.  
 54 | Then Linda might paint that isolated cell and turn it into a lime that can never be overwritten (because all blocks containing it have no other grey cells). To prevent this, Sue must act **before** Linda gets a chance to paint such a cell. Therefore the invariant must be maintained from the very beginning. The strategy described above (repeatedly removing any newly created isolated grey cell) ensures that at the start of every Linda turn there are no isolated grey cells. Consequently Linda can never paint an isolated grey cell. Moreover, the only way she could create a lime is by painting a grey cell that becomes isolated afterwards; but as argued, after any move by Linda, any newly created isolated grey cell is removed immediately on Sue’s next turn, so it never survives to the end.  
 55 | 
 56 | One more possibility: what if the game ends exactly after a move by Linda? That would mean that before her turn there was exactly one grey cell. But the invariant says there is no isolated grey cell – a single grey cell is isolated by definition. Thus this situation cannot occur under Sue’s strategy. Therefore the game always ends on Sue’s turn. On her final turn she paints a block containing the last grey cells and makes them scarlet. All cells that are painted by Linda have been overwritten by Sue at least once after Linda’s painting, except possibly one cell that became lime without ever having a grey neighbour at the time of painting. However, the invariant prevents any such cell from appearing, because it would require an isolated grey cell at the moment of Linda’s move. Since the invariant is maintained, Linda never paints an isolated grey cell. Consequently **no cell can end as lime**. Wait – this would give 0 limes, contradicting the lower bound we already proved.  
 57 | 
 58 | We must re‑examine the argument. The invariant “before Linda’s turn every grey cell has a grey neighbour” is actually **too strong**; it is possible that Sue maintains it, yet Linda might still force a lime without ever painting an isolated grey cell. In the \(3\times3\) example, the invariant held before each Linda turn (e.g. before L1 there was no isolated; before L2 there was no isolated; before L3 there was no isolated; before L4 there was no isolated). Yet Linda obtained a lime. How did that happen? She painted a grey cell that had neighbours at that moment, but those neighbours were later removed by Sue in such a way that the cell became permanently lime. Our invariant does not prevent that; it only guarantees that at the exact turn when Linda paints, the cell she paints has at least one grey neighbour. But after her move, the neighbour might be removed on Sue’s next turn, leaving the painted cell with no future possibility to be repainted. That is exactly how the lime appeared in the 3×3 optimal play.  
 59 | 
 60 | Thus Sue’s strategy must allow for **at most one** such “survivor”. We need to refine the invariant to allow at most one “pending” lime candidate, and to ensure that at most one candidate survives.
 61 | 
 62 | ---
 63 | 
 64 | #### A more precise strategy for Sue – limiting to one lime
 65 | 
 66 | We describe a strategy for Sue that guarantees at most one lime cell at the end.
 67 | 
 68 | **Notation.** Let \(G\) be the set of grey cells at a given moment.
 69 | 
 70 | **Observation.** If a grey cell \(c\) has the property that **all** other cells in every \(2\times2\) block containing \(c\) are already non‑grey, then any future move of Sue that includes \(c\) must also include at least one grey cell from elsewhere. Since there is no grey cell in the same block, she cannot use any block containing \(c\) as long as \(c\) remains grey. Therefore \(c\) would stay grey forever until Sue gets a chance to include it in a block that contains another grey cell. If that never happens, \(c\) will eventually be painted last by Linda and become lime.  
 71 | 
 72 | Sue wants to prevent such a situation from happening to more than one cell.
 73 | 
 74 | **Sue’s plan.** She will keep the grey set “compact” in the sense that it can be covered by a connected set of blocks, and she will always remove grey cells in a way that at most one cell can become “unprotected”.  
 75 | 
 76 | A convenient tool is the concept of a **“king‑move tree”** – the graph where two cells are adjacent if their row and column differ by at most 1. The condition “\(c\) has no grey neighbour” means \(c\) is isolated in this graph.
 77 | 
 78 | Sue maintains the following **invariant after each of her moves**:
 79 | 
 80 | > **Invariant \(I\):** The grey cells induce a connected subgraph of the king graph, and there is **at most one** grey cell that has degree 0 (i.e. is isolated).
 81 | 
 82 | *Initialisation.* The whole grid is grey, so it is connected and has no isolated cells (since every cell has neighbours). So \(I\) holds.
 83 | 
 84 | Now consider a turn of Linda. She may paint any cell – grey or not. If she paints a non‑grey cell, the grey set does not change, so \(I\) still holds. If she paints a grey cell \(c\), then \(G\) becomes \(G\setminus\{c\}\). The invariant might be violated if after removal \(G\) becomes disconnected or if more than one isolated vertex appears.
 85 | 
 86 | We show that Sue can always repair \(I\) on her next turn, and that this prevents Linda from ever creating a lime **except possibly once**.
 87 | 
 88 | **Case analysis after Linda’s move.**
 89 | 
 90 | 1. **If \(c\) was isolated in \(G\)** (degree 0). Then Linda paints it. After her move, \(c\) is gone. The invariant \(I\) was violated before her move because there was an isolated cell. However, could Linda have ever been in a position to paint an isolated grey cell? That would require that at the start of her turn there was an isolated grey cell. Since Sue’s strategy aims to prevent that, we must argue that under her repairs the invariant \(I\) is restored **before** Linda’s turn. Let’s check the maintenance.
 91 | 
 92 | 2. **Otherwise**, \(c\) had degree at least 1. Then \(G' = G\setminus\{c\}\) might still be connected (if \(c\) was not a cut‑vertex) and might have at most one isolated vertex. In fact, removing one vertex from a connected graph can create at most one isolated vertex (if \(c\) was a leaf, its neighbour might become isolated if it had degree 1 and no other neighbours). It can also disconnect the graph, but on a king graph of a grid, removing a single cell can split the grey set only if the grey set is exactly a connected component of size 2 or 3 that is fragile. Nevertheless, at most one isolated vertex appears.
 93 | 
 94 | Thus after Linda’s move, \(G'\) is either still satisfying \(I\) (connected with ≤1 isolated), or it has exactly one isolated vertex (and possibly remains connected), or it becomes disconnected but still with ≤1 isolated. In any case, the total number of isolated vertices is at most 1.
 95 | 
 96 | Now it is Sue’s turn. She must choose a block containing at least one grey cell. She will act as follows:
 97 | 
 98 | * **If there is an isolated grey cell \(d\)** (i.e. a grey cell with no grey neighbour), she paints **any** \(2\times2\) block \(B\) that contains \(d\). Such a block exists because \(d\) is grey. By doing so she removes \(d\) (and possibly other cells, but since \(d\) was isolated, the other cells in \(B\) are non‑grey). After this removal, the grey set becomes \(G'' = G' \setminus \{d\}\). This removal might create new isolated cells, but because we had at most one isolated cell and it was \(d\), after removing \(d\) there are none. Also the removal of a single cell cannot create more than one isolated cell (as argued). Hence \(G''\) again satisfies \(I\) (it is either still connected or has at most one isolated, but we need to ensure connectivity; however, even if it becomes disconnected, the invariant only requires at most one isolated, not necessarily connected. Actually we only need “at most one isolated”, not full connectivity. Let’s weaken \(I\) to just “at most one isolated grey cell”. This is sufficient for our purpose.)
 99 | 
100 | * **If there is no isolated grey cell**, then every grey cell has at least one grey neighbour. In this situation she picks any block \(B\) that contains **two** grey cells (such a block exists because we can take a block that contains a grey cell and one of its grey neighbours). She paints \(B\) scarlet. This removes at least those two grey cells (and possibly others). After removal, the grey set \(G'' = G' \setminus (B\cap G')\) might have isolated cells. As before, removing a block (which is a set of up to 4 cells) can create at most two isolated cells? Let's be precise. If we remove a block that contained several grey cells, the neighbours of those grey cells that were only connected through them might become isolated. However, because the original graph had minimum degree at least 1 (no isolated), after removing a block, a grey cell can become isolated only if it was adjacent only to grey cells that all lay in the same block we just removed. Since the block contains at most 4 cells, a grey cell outside the block could lose at most its neighbours that were inside the block. It could become isolated if it had exactly those neighbours and no others. This could produce multiple isolated cells. But note that the block is a \(2\times2\) area;
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
   - Fill in the header (Problem `4_COLOUR`, Submission `team_5`, your grader
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
   `grade_4_COLOUR_team_5_AI.tex`.
3. **Check it compiles.** Run `pdflatex -interaction=nonstopmode <file>.tex` and fix any
   errors so it builds to a PDF. (Keep the document self-contained — do not add external
   dependencies.)
4. **State the proposed mark** (0/1/6/7) clearly in your final message.

Do **not** commit anything to the repository — return the `.tex` (and its PDF if produced).
