class LLMJudgeEvaluator:

    def evaluate(
        self,
        judge_response: str
    ) -> dict:

        response = (
            judge_response
            .strip()
        )

        passed = (
            response.upper()
            .startswith("PASS")
        )

        reason = ""

        if "Reason:" in response:

            reason = (
                response
                .split(
                    "Reason:",
                    1
                )[1]
                .strip()
            )

        return {
            "passed": passed,
            "reason": reason
        }
