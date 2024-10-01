import anthropic


class AnthropicCalls:
    def __init__(
            self,
            name="Anthropic Chat",
            api_key="",
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            temperature=0.7,
            system_prompt="",
            stream=False,
    ):
        self.name = name
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.system_prompt = system_prompt
        self.stream = stream
        self.history = []

        self.client = anthropic.Anthropic(
            api_key=self.api_key,
        )

    def add_message(self, role, content):
        self.history.append(
            {
                "role": role, 
                "content": content
            }
        )
    
    def clear_history(self):
        self.history.clear()

    def chat(self, message, **kwargs):
        self.add_message("user", message)
        return self.get_response(**kwargs)
        
    def get_response(self, should_print=True, **kwargs) -> str:
        params = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": self.history,
            "system": self.system_prompt,
            **kwargs
        }
        assistant_response = ""
        text_response = ""

        if self.stream:
            with self.client.messages.stream(
                **params
            ) as stream:
                for text_chunk in stream.text_stream:
                    text_response += str(text_chunk)
                    if should_print:
                        print(text_chunk, end="", flush=True)
                assistant_response = stream.get_final_message()
        else:
            assistant_response = self.client.messages.create(
                **params
            )
            text_response = assistant_response.content[0].text
            if should_print:
                print(text_response, end="")

        if should_print:
            print()

        self.add_message("assistant", text_response)
        return assistant_response
