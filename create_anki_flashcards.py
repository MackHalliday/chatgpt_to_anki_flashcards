import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class FlashcardGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def user_notes(self, input_file="flashcards_input.txt"):
        with open(input_file, "r") as flashcard_input:
            user_notes = (
                f"Can you make flashcards with questions and answers in a CSV file format. "
                f"Please use these notes to create the flashcards {flashcard_input.read()} "
                "Include nothing else but the questions and answers in your reply."
            )
        return user_notes

    def create_flashcards(self, user_message, output_file="flashcards_output.txt"):
        messages = [
            {"role": "system", "content": "You are a helpful assistant that creates flashcards with questions and answers."},
            {"role": "user", "content": user_message},
        ]

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo", messages=messages, temperature=0.7, max_tokens=2000
            )
            flashcards = response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error while interacting with OpenAI: {str(e)}")
            return

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

        logging.info("New flashcards created!")


if __name__ == "__main__":
    API_KEY = os.environ.get("OPENAI_API_KEY")
    if not API_KEY:
        raise ValueError("API key not found. Make sure to set OPENAI_API_KEY in your environment variables.")

    logging.basicConfig(level=logging.INFO)  # Adjust the logging level as needed
    generator = FlashcardGenerator(API_KEY)
    user_notes = generator.user_notes()
    generator.create_flashcards(user_notes)
