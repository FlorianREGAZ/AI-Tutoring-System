from langchain_core.messages import SystemMessage
from langchain.chat_models import init_chat_model

from core.schemas import LearningStageDecision, AITutorState
from core.prompts import STAGE_JUDGE_SYSTEM_PROMPT
from utils.debug import print_state
from config import get_config


class StageJudgeAgent:

    def __init__(self):
        config = get_config()
        stage_judge_model = init_chat_model(config.stage_judge_model)
        self.model = stage_judge_model.with_structured_output(LearningStageDecision)

    def _get_system_message(self, learning_stage_decision: LearningStageDecision | None):
        if not learning_stage_decision:
            return SystemMessage(content=STAGE_JUDGE_SYSTEM_PROMPT)
        
        stage = learning_stage_decision.current_stage
        reason = learning_stage_decision.reason
        return SystemMessage(content=f"{STAGE_JUDGE_SYSTEM_PROMPT}\n# Current stage:\n{stage}\nReason: {reason}")

    def invoke(self, state: AITutorState):
        history = state["history"]
        learning_stage_decision = state["learning_stage_decision"]

        messages = [
            self._get_system_message(learning_stage_decision),
            *history
        ]
        response: LearningStageDecision = self.model.invoke(messages)
        return {"learning_stage_decision": response}
