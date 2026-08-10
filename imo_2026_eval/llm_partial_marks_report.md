# LLM-graded partial marks - a spot check of deedy/imo-2026

[deedy/imo-2026](https://github.com/deedy/imo-2026) is an open comparison of
nine autonomous model runs (across seven models) on the IMO 2026 problems,
graded 0-7 per problem entirely by LLM verifier agents - one Claude-based agent
per problem, with no human grader and no markscheme. Its headline result is
three runs graded 42/42.

We've argued elsewhere that LLM-awarded partial marks, given without access to
the official markschemes, are guesswork and should be treated with extreme
scepticism. Having read a sample of the graded solutions in this repo, we think
the partial marks here bear that out. This note collects the clearest examples.

## Scope - what we did and didn't do

To be clear up front about how limited this check is:

- We looked only at the partial marks that seemed most off, all on P2 and P3.
  This is a spot check, not an audit - we make no claim that the marks we don't
  discuss are fine.
- We made no attempt to verify the 7/7s. Whether a solution is complete and
  correct is a reasonably objective question (though it does depend on the
  strength of the grading model), so those are much less of a concern than the
  intermediate marks.
- For each run we worked from the provided PDF of the model's final write-up
  (its `current.md` tracking file). Where these were extremely long we haven't
  necessarily read every line, and we haven't worked through the side
  directories of approaches and scratch work. The repo's graders did credit
  material in those side files - but by the graders' own account, in every case
  below the crux of the problem is untouched, so this doesn't change the
  conclusions.

Before getting into it, credit where due: the repo publishes verbatim
solutions, per-turn logs and full grader verdicts (exactly the openness that
makes a check like this possible), and its own caveats say plainly that the
graders 'are Claude-based agents, not human medalists'. The issue is also much
broader than this one repo - most published 'IMO scores' for models rest on
LLM grading of exactly this kind.

## Why partial marks need a markscheme

The official IMO markschemes aren't public. Partial credit at the IMO is very
non-linear and its shape differs a lot from problem to problem: in 2026, P2
partials cluster at 1-2 with essentially nothing at 4-6, whilst P3 shows a
spike at 4 (39 contestants) but almost nothing at 2 (just 7) - partial credit
lands on specific milestones, not on a linear scale. The full distribution
(from
[imo-official.org](https://www.imo-official.org/results/individual/year/2026/)):

| Problem | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P2 | 288 | 183 | 54 | 26 | 13 | 0 | 2 | 100 |
| P3 | 507 | 86 | 7 | 9 | 39 | 2 | 3 | 13 |

The problem isn't that partial marks are rare - the table shows 1s and 2s are
awarded reasonably often - it's that without the markscheme you don't know what
they're awarded *for*. The bar is usually higher than an LLM grader assumes, so
it awards credit too early; in practice LLM graders invent their own
partial-progress criteria and mark against those instead. Two IMO conventions
matter for the examples below:

- Computational work on a geometry problem (coordinates, complex numbers,
  trigonometry) earns no partial credit unless the intermediate results are
  interpreted synthetically - i.e. back in terms of the diagram.
- On a hard problem, computing small cases and conjecturing an answer -
  especially a wrong answer - is not credit-worthy.

## P2 - four partial marks that would be zeros

P2 was the geometry problem. Four runs were awarded partial credit for
coordinate or complex-number reductions that stop before the crux. All four
would score 0 at the IMO.

**xAI Grok 4.5 (xhigh effort) - given 2/7.** The final write-up is under 1KB
and garbled throughout (even its restatement of the problem reads '$OMRegul =
ON$' [sic]). Quoted in full apart from the problem statement:

```
## Status
partial

## Approaches tried
- Numerics: claim true (OM=ON for the 1-param family).
- Isosceles case: proved by reflection.
- Spiral sims, sine lawآني expressions known.       [sic]
- Algebraic target with A=0 known.

## Current best
 Working toward a geometric proof: perhaps by showing that the reflection of O
across the midperp of MN coincides with O, or that triangle OMN is isosceles
with OM =ON by some equal angles or congruent triangles. Or use Cartesian with
origin at mid of MN.

## Full proof
(not yet)
```

That's it: a numerical check, the (trivial) isosceles case, and a plan. The
grader's own verdict concedes 'the crux is untouched' and that the saved
verification code is 'broken/trivial (syntax errors, a stub "hello sympy")' -
and still awards 2/7.

**DeepSeek V4 Pro - given 2/7.** A coordinate setup: it reduces OM=ON to a
polynomial identity P=0, translates the angle conditions into three polynomial
equations, and stops. The write-up ends:

```
Need to show P ∈ Ideal(R1,R2,R3) or at least that P=0 when the interior
conditions hold.

## Full proof
(TODO)
```

Everything else in the file is numerics and one special case (the right
isosceles triangle). The entire content is a reduction any coordinate approach
starts with; the proof itself is literally left as to-do.

**Meta Muse Spark 1.1 (xhigh effort) - given 2/7.** The same shape: a
coordinate reduction of OM=ON to 'Ox=0', a parametrisation of the
configuration, then 'We numerically suspect this holds.' followed by 'Full
proof: TBD.'

**GPT-5.6 Sol (default effort) - given 4/7.** This one claimed 'solved', but
it's a computational solution with the key step missing - and the grading
feedback itself says so: the crux lemma's proof 'is defective', the claimed
cancellation 'cannot be matched to the actual terms', and 'the crux identity is
therefore asserted, not proven'. A computational write-up whose central
identity is asserted is a 0 at the IMO, not a 4. For context, only **13 of the
666 contestants (2.0%)** scored exactly 4 on P2.

What's striking is that the graders correctly identified that the first three
runs all stop at the same point - one verdict describes a run 'stopping at the
same wall as muse-spark' - and then awarded 2/7 anyway. The marks measure the
amount of activity, not progress a markscheme would recognise: incomplete
computational geometry with no synthetic interpretation gets nothing at the
IMO.

## P3 - partial marks for wrong answers and busy work

P3 was a hard combinatorics problem; the answer is
\(c_n = 2^n/(2^{n+1}-1)\). 507 of 666 contestants scored 0 on it, and only 7
scored exactly 2.

**DeepSeek V4 Pro - given 1/7.** The write-up computes small cases and
conjectures the answer \((n+1)/(2n+1)\) - which has completely the wrong form
and is false for every \(n \ge 2\). By the grader's own checking, even the
file's brute-force value for n=2 is wrong. The file ends:

```
We need a rigorous proof:
- Upper bound: Xiang Yu can limit Liu Bang to at most (n+1)/(2n+1). Strategy
  for X?
- Lower bound: Liu Bang's strategy ensures at least (n+1)/(2n+1).

## Full proof
(To be completed)
```

Small cases plus a wrong conjecture would score 0 on a hard IMO problem, not 1.

**Meta Muse Spark 1.1 (xhigh effort) - given 1/7.** A 24KB
stream-of-consciousness file: lots of small examples and case work, the same
wrong answer \((n+1)/(2n+1)\), a central lower-bound claim the grader shows is
false, and - in the grader's words - 'no upper-bound argument at all'. The file
ends stuck, mid-plan. Busy work with a wrong answer is a 0.

**GPT-5.6 Sol (max effort) - given 1/7.** Quoted in full apart from the problem
statement:

```
## Status
unsolved

## Approaches tried
- Reformulated the claiming phase: rational play consists of taking a currently
  longest piece, so Liu Bang's payoff is the sum of the odd-indexed lengths
  after sorting all pieces nonincreasingly.
- Began investigating the equivalent alternating-sum discrepancy of refinements
  of Liu Bang's initial partition.

## Current best
No final expression yet. If the final piece lengths are $x_1\ge\cdots\ge x_m$,
Liu Bang receives $x_1+x_3+\cdots$, equivalently $(1+D)/2$ where
$D=x_1-x_2+x_3-\cdots+(-1)^{m+1}x_m\ge0$.

## Full proof
Not yet complete.
```

The grader notes the run ended after about a minute, states no answer at all,
and that 'the entire crux... is absent'. It still gets 1/7. This is an
elementary observation about the claiming phase - there's no version of an IMO
markscheme on a problem this hard that awards it a mark.

**GPT-5.6 Sol (default effort) - given 2/7.** A brief flag rather than a
verdict, as this write-up is long and we haven't read it in detail. It has the
correct answer, but both bounds rest on a proof of the key lemma that the
grader itself calls 'an unverifiable sketch'. Only **7 of 666 contestants
(1.1%)** scored exactly 2 on P3, and a 2 for the right answer plus the right
ideas seems unlikely to match whatever those seven human 2s were actually
awarded for. This one would need further investigation.

## The grading process itself

One process point, beyond the individual marks.

**The grading runs don't appear to be independent.** Grader verdicts repeatedly
reference other models' solutions: Grok 4.5's P2 verdict reads 'Self-reported
partial; genuine but incomplete, stopping at the same wall as muse-spark';
DeepSeek's P2 verdict says 'this is the same wall reached by muse-spark-1.1 and
grok-4.5... so it sits at the same level'; the P3 verdicts score runs relative
to 'the calibrated score-1 muse-spark entry'. Whilst cross-referencing other
candidates' scripts can make grading more consistent, it invites anchoring and
leakage between grades - each script should be assessed on its own content.

## Effect on the totals

Given the issues described above, we consider what happens if you simply
zeroise all of the partial marks. This is an extreme view, but it's likely
much closer to how these solutions would be marked at the actual IMO than the
published scores.

For reference, the IMO 2026 medal boundaries were Bronze 16, Silver 23,
Gold 29.

| Run | Published total | Medal | All partials zeroed | Medal |
| --- | --- | --- | --- | --- |
| Claude Fable 5 | 42 | Gold | **42** | Gold |
| GPT-5.6 Sol (xhigh effort) | 42 | Gold | **42** | Gold |
| Kimi K3 | 42 | Gold | **42** | Gold |
| GPT-5.6 Sol Pro | 37 | Gold | **35** | Gold |
| GPT-5.6 Sol (max effort) | 30 | Gold | **28** | Silver |
| GPT-5.6 Sol (default effort) | 28 | Silver | **21** | Bronze |
| Meta Muse Spark 1.1 | 26 | Silver | **21** | Bronze |
| DeepSeek V4 Pro | 19 | Bronze | **14** | - |
| xAI Grok 4.5 | 13 | - | **7** | - |

The ranking barely moves (GPT-5.6 Sol default and Muse Spark end up tied), but
the medal colours do: four of the nine runs drop a band - GPT-5.6 Sol (max)
from Gold to Silver, GPT-5.6 Sol (default) and Muse Spark from Silver to
Bronze, and DeepSeek out of the medals altogether.

To be clear, this is deliberately the most extreme adjustment, not our view of
the corrected leaderboard - ultimately, without access to the IMO markschemes,
no-one can know what the corrected marks would be.

## Takeaway

None of this is specific to one repo. Judging whether a solution is complete is
reasonably objective, and LLM graders can be genuinely useful there. But
LLM-awarded partial marks, given without access to the markscheme, are
guesswork: the grader invents its own partial-progress criteria, awards credit
for activity rather than for the progress a markscheme rewards, and the
resulting errors systematically inflate totals. The examples above - 2/7 for a
coordinate setup with the proof left as '(TODO)', 1/7 for small cases and a
wrong answer - would all be zeros if graded at the actual IMO. When you see a
model's 'IMO score' built on LLM grading, the 7s may well be sound (provided
the grading model is strong enough); treat the partial marks with extreme
scepticism.