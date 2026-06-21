from models.source_attribution import (
    SourceAttribution
)


class SourceExtractor:

    def extract_sources(
        self,
        retrieval_result
    ) -> list[SourceAttribution]:

        sources = []

        seen = set()

        for chunk in retrieval_result.chunks:

            metadata = chunk["metadata"]
            section = metadata["section"].strip()
            section = " ".join(section.split())

            key = (
                metadata["document_name"],
                section,
                metadata["page_number"]
            )

            if key in seen:
                continue

            seen.add(key)

            sources.append(
                SourceAttribution(
                    document_name=
                        metadata["document_name"],
                    section=
                        section,
                    page_number=
                        metadata["page_number"]
                )
            )

        return sources
