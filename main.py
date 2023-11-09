from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from googletrans import Translator

app = FastAPI()

class TranslationRequest(BaseModel):
    """
    A Pydantic model that represents the expected request body for the translation.
    Fields:
        sentence (str): The text to translate.
        choice (bool): A flag that determines the target language. If True, translates to Thai; otherwise, to English.
    """
    sentence: str
    choice: bool


def translate_to_thai(sentence: str, choice: bool) -> str:
    """
    Translate the text between English and Thai based on the 'choice' flag.
    
    Args:
        sentence (str): The text to translate.
        choice (bool): If True, translates text to Thai. If False, translates to English.

    Returns:
        str: The translated text.
    """
    translator = Translator()
    try:
        if choice:
            # Translate to Thai
            translate = translator.translate(sentence, dest='th')
        else:
            # Translate to English
            translate = translator.translate(sentence, dest='en')
        return translate.text
    except Exception as e:
        # Handle translation-related issues (e.g., network error, unexpected API response)
        raise ValueError(f"Translation failed: {str(e)}") from e


@app.post("/translate/")
async def translate(request: TranslationRequest):
    """
    Endpoint to handle translation requests. Translates text based on the request data.

    Args:
        request (TranslationRequest): A model instance containing the 'sentence' and 'choice' flag.

    Returns:
        JSON response with the translated text or an error message.
    """
    try:
        # Perform the translation
        translation = translate_to_thai(request.sentence, request.choice)
        return {"translation": translation}
    except ValueError as e:
        # If a translation error occurs, return a 500 status code with the error message
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    # Run the application with Uvicorn with specified host and port
    uvicorn.run(app, host="0.0.0.0", port=8071)