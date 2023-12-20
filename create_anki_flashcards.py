import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class FlashcardGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def create_flashcards(self, input_file="flashcards_input.txt", output_file="flashcards_output.txt"):
        with open(input_file, "r") as flashcard_input:
            user_message = (
                f"Can you make flashcards with questions and answers in a CSV file format. "
                f"Please use these notes to create the flashcards {flashcard_input.read()} "
                "Include nothing else but the questions and answers in your reply."
            )

        messages = [
            {"role": "system", "content": "You are a helpful assistant that creates flashcards with questions and answers."},
            {"role": "user", "content": user_message},
        ]

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages, temperature=0.7, max_tokens=2000
        )

        flashcards = response.choices[0].message.content

        with open(output_file, "w") as f:
            replacements = {
                '?,': '?;',
                '?,"': '?;',
                '."': '.',
                'Question,Answer': ''
            }
            for old_str, new_str in replacements.items():
                flashcards = flashcards.replace(old_str, new_str)

            f.write(flashcards)

        print("New flashcards created!")


if __name__ == "__main__":
    api_key = os.environ.get("OPENAI_KEY")
    if not api_key:
        raise ValueError("API key not found. Make sure to set OPENAI_API_KEY in your environment variables.")

    generator = FlashcardGenerator(api_key)
    generator.create_flashcards()
