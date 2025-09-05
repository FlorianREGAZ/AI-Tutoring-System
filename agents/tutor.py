from langchain_core.messages import SystemMessage
from langchain.chat_models import init_chat_model

from core.schemas import LearningStageDecision, LearningStage, AITutorState
from core.prompts import (
    TUTOR_SYSTEM_PROMPT,
    TOPIC_CLARIFICATION_INSTRUCTIONS,
    GET_TO_KNOW_INSTRUCTIONS,
    KNOWLEDGE_EVAL_INSTRUCTIONS,
    CONCEPT_PRESENTATION_INSTRUCTIONS,
    GUIDED_PRACTICE_INSTRUCTIONS,
    INDEPENDENT_PRACTICE_INSTRUCTIONS,
    WRAP_UP_INSTRUCTIONS
)
from utils.debug import print_state
from config import get_config


class TutorAgent:
    STAGE_INSTRUCTIONS: dict[LearningStage, str] = {
        LearningStage.TOPIC     : TOPIC_CLARIFICATION_INSTRUCTIONS,
        LearningStage.KNOW_USER : GET_TO_KNOW_INSTRUCTIONS,
        LearningStage.BASELINE  : KNOWLEDGE_EVAL_INSTRUCTIONS,
        LearningStage.CONCEPT   : CONCEPT_PRESENTATION_INSTRUCTIONS,
        LearningStage.GUIDED    : GUIDED_PRACTICE_INSTRUCTIONS,
        LearningStage.INDEP     : INDEPENDENT_PRACTICE_INSTRUCTIONS,
        LearningStage.WRAP      : WRAP_UP_INSTRUCTIONS
    }

    def __init__(self):
        config = get_config()
        self.model = init_chat_model(config.tutor_model)

    def _get_system_message(self, learning_stage_decision: LearningStageDecision, pdf_context: str | None):
        stage = learning_stage_decision.current_stage
        reason = learning_stage_decision.reason

        additional_context = ""
        if pdf_context:
            additional_context = f"# PDF content:\nHere is additional context from the users PDF. Use it as a reference to help the user learn:\n{pdf_context}"

        return SystemMessage(content=TUTOR_SYSTEM_PROMPT.format(
            stage_instructions=self.STAGE_INSTRUCTIONS[stage],
            reason=reason,
            additional_context=additional_context
        ).strip())

    def invoke(self, state: AITutorState):
        history = state["history"]
        pdf_context = state["pdf_context"]

        system_message = self._get_system_message(state["learning_stage_decision"], pdf_context)
        messages = [
            system_message,
            *history
        ]
        return {"history": [self.model.invoke(messages)]}
