from google import genai

client = genai.Client(api_key="AQ.Ab8RN6JoyJqgJfVi1ZX4dX-XjYkuNu6KMSHb42mBRJUw2zfaCQ")

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="Explain how AI works in a few words"
)

print(interaction.output_text)