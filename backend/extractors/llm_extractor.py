import json
import ollama

class LLMExtractor:
    def __init__(self, model_name: str = "llama3.2"):
        self.model_name = model_name

    def extract_from_resume(self, text: str) -> dict:
        prompt = f"""
        Extract the following information from the provided resume text:
        - full_name (string)
        - emails (list of strings)
        - phones (list of strings)
        - headline (string)
        - skills (list of strings)
        - education (list of strings)
        - experience (list of objects with fields: title, company, dates, description)
        - projects (list of objects with fields: name, description)
        
        Return ONLY a valid JSON object matching the requested fields. Do not include any markdown formatting like ```json.
        
        Resume Text:
        {text}
        """

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}],
                options={"temperature": 0.0}
            )
            response_content = response['message']['content'].strip()
            
            # Clean up potential markdown blocks if the model still returns them
            if response_content.startswith("```json"):
                response_content = response_content[7:]
            if response_content.startswith("```"):
                response_content = response_content[3:]
            if response_content.endswith("```"):
                response_content = response_content[:-3]
                
            return json.loads(response_content)
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON from LLM: {e}")
            print(f"Raw output: {response_content}")
            return {}
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return {}
