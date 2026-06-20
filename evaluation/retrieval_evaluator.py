class RetrievalEvaluator:

    def evaluate(
        self,
        retrieval_result,
        expected_facts
    ):

        retrieved_text = ""

        for chunk in retrieval_result.chunks:
            retrieved_text += chunk["text"]
            retrieved_text += "\n"

            retrieved_text = " ".join(retrieved_text.lower().split())
        
        missing_facts = []

        for fact in expected_facts:

            if fact.lower() not in retrieved_text:
                missing_facts.append(fact)

        return {
            "passed": len(missing_facts) == 0,
            "missing_facts": missing_facts
        }
