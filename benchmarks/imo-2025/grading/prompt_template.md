# MathArena IMO grading prompt (checkpoint scheme)

model=gpt-5.6-sol  reasoning=high  attempts=8  aggregation=arithmetic_mean  max_output_tokens=32768

Grading scheme source: MathArena/imo_2025 (per-problem checkpoints summing to 7).

## SYSTEM
You are an expert grader for the International Mathematics Olympiad (IMO).

## USER (per problem; {problem}, {scheme}, {solution} filled in)
You are an expert grader for the International Mathematical Olympiad (IMO). Your task is to grade a proposed solution strictly and rigorously against the official grading scheme. IMO standards are extremely high: award points only for reasoning that is logically sound, complete, and precise.

### Scoring
Each problem is graded out of 7 points via a checkpoint-based grading scheme. Each checkpoint has a maximum number of points. For each checkpoint, award an integer number of points from 0 up to its maximum, depending on whether the proposed solution rigorously and completely establishes that checkpoint. Points are additive across checkpoints; the maximum total is 7. A checkpoint that is only asserted, hand-waved, or that contains a logical gap or error earns 0 points for that checkpoint. Partial progress that is not explicitly credited by a checkpoint earns nothing.

### Evaluation Process
1. **Understand the scheme.** Read the problem and every checkpoint; identify precisely what each checkpoint requires.
2. **Verify the solution.** Work through the proposed solution step by step. Identify every gap, unjustified claim, assumption, and error. Be especially careful of solutions that "pretend" to be correct or that assert a key step without proof — you must fully understand the logic behind each step.
3. **Award per checkpoint.** For each checkpoint, decide the integer points awarded (0 up to its maximum) and give a brief justification tied to the solution.
4. **Total.** Sum the awarded points for the final score out of 7.

### Output Requirements
Provide your final score in the format <points>N out of 7</points>. Use the '<points>' block **only once**; your answer is parsed from the first <points> </points> block that appears in your response.

**PROBLEM STATEMENT**
{problem}

**GRADING SCHEME (total 7 points)**
{scheme}

**PROPOSED SOLUTION**
{solution}

Present your per-checkpoint analysis and justification, then present your final score in the format <points>N out of 7</points>.
