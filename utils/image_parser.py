import io
import base64
from typing import Any, Dict, IO

from langchain_core.messages import SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from unstructured.partition.image import partition_image

from core.prompts import IMAGE_PARSER_SYSTEM_PROMPT
from core.schemas import ImageCaption


class ImageParser:

    def __init__(
        self,
        model: str,
        temperature: float = 0.0,
        enable_ocr: bool = True,
        max_ocr_chars: int = 2000,
    ) -> None:
        self.enable_ocr = enable_ocr
        self.max_ocr_chars = max_ocr_chars
        self.llm = init_chat_model(model, temperature=temperature).with_structured_output(ImageCaption)

    def parse(self, image_b64: str) -> Document:
        # Optional OCR (good for axes labels, captions, text-in-image)
        ocr_summary = ""
        if self.enable_ocr:
            try:
                ocr_els = partition_image(file=ImageParser._base64_to_bytes_io(image_b64))
                ocr_text = "\n".join(
                    e.text for e in ocr_els if getattr(e, "text", None)
                )
                if ocr_text:
                    ocr_summary = ocr_text[: self.max_ocr_chars]
            except Exception:
                ocr_summary = ""

        # Vision captioning
        image_caption_data = self._caption_image(image_b64)

        page_content_parts = [image_caption_data.short_caption, image_caption_data.detailed_caption]
        if ocr_summary:
            page_content_parts.append("OCR:\n" + ocr_summary)
        page_content = "\n\n".join(part for part in page_content_parts if part)

        return Document(
            page_content=page_content,
            metadata={
                "source_type": "image",
                "entities": image_caption_data.entities,
                "tags": image_caption_data.tags,
                "layout_notes": image_caption_data.layout_notes,
            },
        )

    @staticmethod
    def _base64_to_bytes_io(b64_str: str) -> IO[bytes]:
        raw_bytes = base64.b64decode(b64_str)
        return io.BytesIO(raw_bytes)

    def _caption_image(self, image_b64: str) -> Dict[str, Any]:
        messages = [
            SystemMessage(content=IMAGE_PARSER_SYSTEM_PROMPT),
            HumanMessage(content=[
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}}
            ]),
        ]

        return self.llm.invoke(messages)
