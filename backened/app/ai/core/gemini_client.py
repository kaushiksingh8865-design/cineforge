from google import genai


from backened.app.ai.schemas.scene import Scene
from .settings import settings


client = genai.Client(api_key=settings.gemini_api_key)


def generate_scene(prompt:str)-> str:
    response = client.models.generate_content(
        model ="gemini-3.6-flash",
        contents =prompt,
        config = {
            'response_mime_type': 'application/json',
            'response_schema': Scene,
        }
    )
    return response.parsed

if __name__ == "__main__":
    result = generate_scene(
        "In one sentence, what is a screenplay scene?"
    )

    print(result)
    print(type(result))

    

