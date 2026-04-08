from config.claude_config import ClaudeConfig

class ClaudeService:
    def __init__(self):
        self.claude = ClaudeConfig()
    
    def test_connection(self):
        """Test simple pour vérifier la configuration"""
        result = self.claude.get_response("Dis simplement 'Connexion OK'")
        return result
