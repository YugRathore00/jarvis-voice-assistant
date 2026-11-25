from google import genai

client = genai.Client(api_key="Api_Key")

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="Explain how AI works in a few words"
)

print(interaction.output_text)
