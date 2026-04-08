import os
from anthropic import Anthropic

class ClaudeConfig:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.client = Anthropic(api_key=self.api_key) if self.api_key else None
        self.model = "claude-3-5-sonnet-20241022"
        
    def get_response(self, prompt, system_prompt=None, max_tokens=4000):
        if not self.client:
            return "Erreur: Clé API Anthropic non configurée. Veuillez définir ANTHROPIC_API_KEY"
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=0.7,
                system=system_prompt or "Vous êtes un expert en rédaction administrative.",
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            return f"Erreur API: {e}"
