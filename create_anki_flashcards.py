import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class FlashcardGenerator:
    def __init__(self, api_key: str) -> None:
        self.client = OpenAI(api_key=api_key)

    def format_file(self, flashcards: str) -> None:
        with open("flashcards_output.txt", "w") as flashcard_output:
            replacements = {
                "Question,Answer": "",
                ",True": ";True",
                ",False": ";False",
                "?,": "?;",
            }
            for old_str, new_str in replacements.items():
                flashcards = flashcards.replace(old_str, new_str)

            flashcard_output.write(flashcards)

    def create_flashcards(
        self,
    ) -> None:
        with open("flashcards_input.txt", "r") as flashcard_input:
            user_notes = (
                f"Can you make flashcards with questions and answers. "
                f"Please use these notes to create the flashcards {flashcard_input.read()}. "
                "You must format your response in a CSV format with no other text than the flashcard question and answer"
            )

        messages = [
            {
                "role": "system",
                "content": "You are a helpful teacher that creates concise flashcards.",
            },
            {"role": "user", "content": user_notes},
        ]

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
            )
            flashcards = response.choices[0].message.content

        except Exception as error:
            logging.error(f"Error while interacting with OpenAI: {str(error)}")
            return

        self.format_file(flashcards)

        logging.info(
            "New flashcards have been created in the flashcards_output.txt file!"
        )


if __name__ == "__main__":
    API_KEY = os.environ.get("OPENAI_API_KEY")
    if not API_KEY:
        raise ValueError(
            "API key not found. Make sure to set OPENAI_API_KEY in your environment variables."
        )

    logging.basicConfig(level=logging.INFO)
    generator = FlashcardGenerator(API_KEY)
    generator.create_flashcards()
