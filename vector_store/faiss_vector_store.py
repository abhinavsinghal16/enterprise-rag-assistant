import json

import faiss
import numpy as np


class FaissVectorStore:

    def build_index_from_file(
        self,
        embeddings_file: str
    ):

        with open(
            embeddings_file,
            "r",
            encoding="utf-8"
        ) as file:

            embedding_records = json.load(file)

        # Extract embedding vectors from persisted records
        embeddings = np.array(
            [
                record["embedding"]
                for record in embedding_records
            ],
            dtype=np.float32
        )

        dimension = embeddings.shape[1]

        # Create a FAISS index using Euclidean distance
        index = faiss.IndexFlatL2(
            dimension
        )

        # Add all embeddings to the index
        index.add(
            embeddings
        )

        return index

    def save_index(
        self,
        index,
        index_file: str
    ):

        faiss.write_index(
            index,
            index_file
        )
