class ResponseEvaluator:

    def evaluate(
        self,
        answer: str,
        expected_facts
    ):

        normalized_answer = " ".join(
            answer.lower().split()
        )

        missing_facts = []

        for fact in expected_facts:

            normalized_fact = " ".join(
                fact.lower().split()
            )

            if (
                normalized_fact
                not in normalized_answer
            ):
                missing_facts.append(
                    fact
                )

        return {
            "passed":
                len(missing_facts) == 0,

            "missing_facts":
                missing_facts
        }
