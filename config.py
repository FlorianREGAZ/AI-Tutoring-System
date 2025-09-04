import os
from dotenv import load_dotenv


class Config:
    
    def __init__(self):
        """Initialize configuration by loading environment variables."""
        # Load environment variables from .env.local
        load_dotenv(".env.local")
        
        # API Keys
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_API_KEY") 
        
        # Model Selection
        self.default_model = os.getenv("DEFAULT_MODEL", "openai:gpt-5")
        self.stage_judge_model = os.getenv("STAGE_JUDGE_MODEL", self.default_model)
        self.tutor_model = os.getenv("TUTOR_MODEL", self.default_model)
        self.pdf_assistant_model = os.getenv("PDF_ASSISTANT_MODEL", self.default_model)
        
        # Debug Configuration
        self.debug_mode = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes", "on")
        
        # Application Settings
        self.thread_id = os.getenv("THREAD_ID", "1")
    

# Global configuration instance
config = Config()


def get_config() -> Config:
    """Get the global configuration instance."""
    return config


def reload_config() -> Config:
    """Reload the configuration from environment variables."""
    global config
    config = Config()
    return config
