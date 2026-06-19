import json
from pathlib import Path


class JsonStorage:

    def __init__(
        self,
        data_directory: str = "data"
    ):
        self.data_directory = Path(data_directory)

        self.data_directory.mkdir(
            exist_ok=True
        )

    def save_documents(
        self,
        documents: list[dict]
    ) -> None:

        self._save_json(
            "documents.json",
            documents
        )

    def save_chunks(
        self,
        chunks: list[dict]
    ) -> None:

        self._save_json(
            "chunks.json",
            chunks
        )

    def save_embeddings(
        self,
        embeddings: list[dict]
    ) -> None:

        self._save_json(
            "embeddings.json",
            embeddings
        )

    def _save_json(
        self,
        file_name: str,
        data: list[dict]
    ) -> None:

        file_path = (
            self.data_directory /
            file_name
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    def load_chunks(self):
        with open(
            self.data_directory / "chunks.json",
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def load_embeddings(self):
        with open(
            self.data_directory / "embeddings.json",
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)
