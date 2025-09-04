from core.schemas import AITutorState
from config import get_config

def print_state(state: AITutorState, info: str = ""):
    """Print state information if debug mode is enabled."""
    config = get_config()
    
    if not config.debug_mode:
        return
    
    print("--- AITutorState -----------------------------")
    if info:
        print("info:", info)
    
    print("\nHistory:")
    for message in state["history"]:
        print(f"{message.type}: {message.content}")
    
    print("\nLearning stage decision:")
    print(state["learning_stage_decision"])
    print("----------------------------------------------")
