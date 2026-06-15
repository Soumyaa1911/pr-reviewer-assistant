def build_review_prompt(diff: str, context: str) -> str:
    """Build a prompt for the LLM to review a PR diff with codebase context."""
    return f"""You are an expert code reviewer. You are reviewing a pull request.

Here is the relevant context from the existing codebase:
{context}

Here is the PR diff (+ = added, - = removed):
{diff}

Please review this change and provide:
1. A brief summary of what this PR does
2. Potential issues or bugs introduced
3. Suggestions for improvement
4. Whether tests are needed for these changes

Be specific and reference actual code from the diff where relevant.
"""