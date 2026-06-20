class RerankingEvaluator:

    def evaluate(
        self,
        reranked_result,
        expected_facts
    ):

        combined_text = ""

        for chunk in reranked_result.chunks:
            combined_text += (
                " "
                + chunk["text"]
            )

        combined_text = " ".join(
            combined_text.lower().split()
        )

        missing_facts = []

        for fact in expected_facts:

            if (
                fact.lower()
                not in combined_text
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
