import uuid

from models.chunk import Chunk
from models.chunk_metadata import ChunkMetadata


DEFAULT_CHUNK_SIZE = 1000
HEADING_WORD_THRESHOLD = 8
MAX_HEADING_SIZE = 250


def is_heading(paragraph: str) -> bool:

    words = paragraph.split()

    if len(words) == 0:
        return False

    if "|" in paragraph:
        return False

    if paragraph.isdigit():
        return False

    if len(words) > HEADING_WORD_THRESHOLD:
        return False

    if paragraph.endswith(
        (".", "!", "?", ":")
    ):
        return False

    return True


def append_heading(
    current_heading: str | None,
    new_heading: str
) -> str:

    if current_heading is None:
        return new_heading

    heading = (
        current_heading
        + " > "
        + new_heading
    )

    if len(heading) <= MAX_HEADING_SIZE:
        return heading

    heading = heading[-MAX_HEADING_SIZE:]

    separator = heading.find(">")

    if separator != -1:
        heading = heading[
            separator + 1:
        ].strip()

    return heading


def split_into_paragraphs(
    pages: list[dict]
) -> list[tuple[int, str]]:

    paragraphs = []

    for page in pages:

        page_number = page["page_number"]

        for paragraph in page["text"].split("\n\n"):

            paragraph = paragraph.strip()

            if paragraph:

                paragraphs.append(
                    (
                        page_number,
                        paragraph
                    )
                )

    return paragraphs


def chunk_section(
    heading: str | None,
    content: str,
    page_number: int,
    document_id: str,
    document_name: str,
    chunk_size: int
) -> list[Chunk]:

    chunks = []

    heading_text = ""

    if heading:
        heading_text = (
            heading
            + "\n\n"
        )

    available_size = (
        chunk_size
        - len(heading_text)
    )

    start = 0

    while start < len(content):

        remaining = (
            len(content)
            - start
        )

        if remaining <= available_size:

            chunk_content = content[start:]

            chunk_text = (
                heading_text
                + chunk_content
            )

            chunks.append(
                Chunk(
                    id=str(uuid.uuid4()),
                    document_id=document_id,
                    text=chunk_text,
                    metadata=ChunkMetadata(
                        document_name=document_name,
                        page_number=page_number,
                        section=heading
                    )
                )
            )

            break

        candidate = content[
            start:start + available_size
        ]

        split_at = candidate.rfind(" ")

        if split_at == -1:
            split_at = len(candidate)

        chunk_content = candidate[
            :split_at
        ]

        chunk_text = (
            heading_text
            + chunk_content
        )

        chunks.append(
            Chunk(
                id=str(uuid.uuid4()),
                document_id=document_id,
                text=chunk_text,
                metadata=ChunkMetadata(
                    document_name=document_name,
                    page_number=page_number,
                    section=heading
                )
            )
        )

        start += split_at + 1

    return chunks


def create_chunks(
    pages: list[dict],
    document_id: str,
    document_name: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE
) -> list[Chunk]:

    chunks = []

    paragraphs = split_into_paragraphs(
        pages
    )
 
    current_heading = None
    current_content = ""
    current_page_number = None

    for page_number, paragraph in paragraphs:

        if is_heading(paragraph):

            if current_content:

                chunks.extend(
                    chunk_section(
                        heading=current_heading,
                        content=current_content,
                        page_number=current_page_number,
                        document_id=document_id,
                        document_name=document_name,
                        chunk_size=chunk_size
                    )
                )

                current_heading = paragraph
                current_content = ""
                current_page_number = page_number

            else:

                current_heading = append_heading(
                    current_heading,
                    paragraph
                )

                if current_page_number is None:
                    current_page_number = page_number

            continue

        if not current_content:

            current_content = paragraph

            if current_page_number is None:
                current_page_number = page_number

        else:

            current_content += (
                "\n\n"
                + paragraph
            )

    if current_content:

        chunks.extend(
            chunk_section(
                heading=current_heading,
                content=current_content,
                page_number=current_page_number,
                document_id=document_id,
                document_name=document_name,
                chunk_size=chunk_size
            )
        )

    return chunks
