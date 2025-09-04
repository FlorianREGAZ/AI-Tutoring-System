from enum import Enum
from typing import Annotated, TypeAlias, TypedDict
from pydantic import BaseModel, Field

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph.message import add_messages


class LearningStage(str, Enum):
    TOPIC     = "1_TOPIC_CLARIFICATION"
    KNOW_USER = "2_GET_TO_KNOW"
    BASELINE  = "3_KNOWLEDGE_EVAL"
    CONCEPT   = "4_CONCEPT"
    GUIDED    = "5_GUIDED_PRACTICE"
    INDEP     = "6_INDEPENDENT_PRACTICE"
    WRAP      = "7_WRAP_UP"


class LearningStageDecision(BaseModel):
    current_stage: LearningStage = Field(default=LearningStage.TOPIC, description="The current stage of the learning session")
    reason: str = Field(description="The reason why the current stage is chosen and instructions on what is missing to advance to the next stage")


History: TypeAlias = list[HumanMessage | AIMessage]


class AITutorState(TypedDict):
    history: Annotated[History, add_messages]
    learning_stage_decision: LearningStageDecision | None
    pdf_context: str | None


class ImageCaption(BaseModel):
    short_caption: str = Field(description="<= 20 words, high-signal alt text")
    detailed_caption: str = Field(description="Detailed caption of the image, factual, concise")
    entities: list[str] = Field(description="list of key objects/labels")
    tags: list[str] = Field(description="list of search tags (5–10, lowercase)")
    layout_notes: str = Field(description="brief notes on layout if relevant")
