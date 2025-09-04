
from langchain_core.documents import Document
from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import CompositeElement, Image

from utils.image_parser import ImageParser


class PDFParser:

    def __init__(
        self,
        image_parser: ImageParser = None,
        languages: list[str] = ["eng"],
    ) -> None:
        self.image_parser = image_parser
        self.languages = languages

    def _extract_elements_from_chunks(self, chunks) -> tuple[list[str], list[str]]:
        images = []
        texts = []

        for chunk in chunks:
            if isinstance(chunk, CompositeElement):
                texts.append(chunk.text)

                chunk_els = chunk.metadata.orig_elements
                for el in chunk_els:
                    if isinstance(el, Image):
                        images.append(el.metadata.image_base64)

        return list(set(images)), texts

    def parse(self, pdf_path: str) -> list[Document]:
        chunks = partition_pdf(
            filename=pdf_path,
            strategy="hi_res" if self.image_parser else "fast",
            extract_image_block_types=["Image"] if self.image_parser else None,
            extract_image_block_to_payload=True if self.image_parser else False,
            chunking_strategy="by_title",
            max_characters=10000, 
            combine_text_under_n_chars=2000, 
            new_after_n_chars=6000,
            languages=self.languages,
        )

        # Extract images and texts
        images, texts = self._extract_elements_from_chunks(chunks)
        documents = []

        # Process text chunks
        for i, text in enumerate(texts):
            if not text.strip():
                continue

            doc = Document(
                page_content=text,
                metadata={
                    "source": pdf_path,
                    "source_type": "pdf_file",
                    "chunk_index": i,
                    "content_type": "text",
                }
            )
            documents.append(doc)

        # Process images if image parser is available
        if self.image_parser and images:
            for i, image_b64 in enumerate(images):
                image_doc = self.image_parser.parse(image_b64)
                # Update metadata to include PDF source information
                image_doc.metadata.update({
                    "source": pdf_path,
                    "source_type": "pdf_file",
                    "image_index": i,
                    "content_type": "image",
                })
                documents.append(image_doc)

        return documents
