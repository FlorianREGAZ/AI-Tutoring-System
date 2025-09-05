from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END

from agents.pdf_assistant import PDFAssistantAgent
from agents.stage_judge import StageJudgeAgent
from agents.tutor import TutorAgent
from config import get_config
from core.schemas import AITutorState
from core.prompts import START_MESSAGE
from utils.debug import print_state
from utils.pdf_parser import PDFParser

class AITutor:

    def __init__(self):
        config = get_config()
        self.config = {"configurable": {"thread_id": config.thread_id}}

        self.pdf_parser: PDFParser = PDFParser(languages=["eng"])

        self.pdf_assistant_agent: PDFAssistantAgent = PDFAssistantAgent()
        self.stage_judge_agent: StageJudgeAgent = StageJudgeAgent()
        self.tutor_agent: TutorAgent = TutorAgent()

        graph_builder = StateGraph(AITutorState)
        graph_builder.add_node("pdf_assistant", self.pdf_assistant_agent.invoke)
        graph_builder.add_node("stage_judge", self.stage_judge_agent.invoke)
        graph_builder.add_node("tutor", self.tutor_agent.invoke)

        graph_builder.add_edge(START, "pdf_assistant")
        graph_builder.add_edge(START, "stage_judge")
        graph_builder.add_edge("pdf_assistant", "tutor")
        graph_builder.add_edge("stage_judge", "tutor")
        graph_builder.add_edge("tutor", END)
        self.graph = graph_builder.compile(checkpointer=InMemorySaver())

        # Load state from snapshot if available
        snapshot = self.graph.get_state(self.config)
        if snapshot and snapshot.values:
            self.state: AITutorState = snapshot.values
        else:
            self.state: AITutorState = AITutorState(
                history=[AIMessage(content=START_MESSAGE)],
                learning_stage_decision=None,
                pdf_context=None
            )

    def _call_graph(self, user_input: str) -> AIMessage:
        self.state["history"].append(HumanMessage(content=user_input))

        result = self.graph.invoke(
            self.state,
            self.config,
            stream_mode="values",
        )

        # Update self.state with the result to persist learning_stage_decision
        self.state = result
        
        # Return latest message from history
        return result["history"][-1]

    def add_pdf(self, pdf_path: str) -> None:
        docs = self.pdf_parser.parse(pdf_path)
        self.pdf_assistant_agent.add_documents(docs)

    def run(self) -> None:
        print("AI Tutor: ", START_MESSAGE)

        while True:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            response = self._call_graph(user_input)
            print(f"AI Tutor: {response.content}")


if __name__ == "__main__":
    ai_tutor = AITutor()
    # Add files
    # ai_tutor.add_pdf("your-pdf-path.pdf")
    ai_tutor.run()
