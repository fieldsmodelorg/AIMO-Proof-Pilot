"""Real OPD-32B output excerpts from Geremie's recorded runs
(bogoconic1 evaluation/runs/*/generation), for parser regression tests.

REAL_MISSING_CLOSE has its proof body truncated but preserves the exact
quirk -- <solution> then proof then <self_evaluation> with NO </solution> --
that gold's lenient parser was built to recover. The others are verbatim.
"""

REAL_MISSING_CLOSE = '<solution>\nWe prove that the only possible values of \\(k\\) are \\(0,1,3\\) for every \\(n\\ge3\\).\n\n---\n\n### 1.  Constructions\n\n#### 1.1  \\(k=0\\)\n\nTake the \\(n\\) vertical lines \\(x=1,\\dots,x=n\\).  \nEvery point \\((a,b)\\) with \\(a,b\\ge1,\\ a+b\\le n+1\\) has \\\n\n[... proof body ...]\n\n<self_evaluation>\nThe solution provides explicit constructions for \\(k=0,1,3\\) and rigorous impossibility proofs for \\(k=2\\) and \\(k\\ge4\\). All claims are justified, and no gaps remain.\n</self_evaluation>\n<score>1</score>'

REAL_CLEAN = '<solution>\nWe interpret the numbers in base $b$: $17_b = 1\\cdot b + 7 = b+7$ and $97_b = 9\\cdot b + 7 = 9b+7$. We need $b>9$ integer such that $(b+7) \\mid (9b+7)$.\n\nCompute: $9b+7 = 9(b+7) - 56$. Thus $9b+7 \\equiv -56 \\pmod{b+7}$. Hence $(b+7) \\mid (9b+7)$ if and only if $(b+7) \\mid 56$.\n\nSince $b>9$, we have $b+7 > 16$. The positive divisors of $56$ are $1,2,4,7,8,14,28,56$. Only $28$ and $56$ exceed $16$. Therefore $b+7 = 28$ or $b+7 = 56$, giving $b=21$ or $b=49$.\n\nBoth bases satisfy $b>9$, and the digits $9$ and $7$ are less than $b$, so the representations are valid. The sum of the two bases is $21+49 = 70$.\n\nThus the required sum is $\\boxed{70}$.\n</solution>\n<self_evaluation>\nThe proof is complete and rigorous. All steps are justified: the conversion to decimal, the division algorithm, the condition for divisibility, the enumeration of divisors, and the final sum. No gaps or unsupported claims.\n</self_evaluation>\n<score>1</score>'

REAL_VERIFY = '<evaluation>\nThe solution is correct and rigorous. All steps are justified, and the algebraic verification is complete. No gaps or errors.\n</evaluation>\n<suggestions>\nNone needed.\n</suggestions>\n<score>1</score>'

