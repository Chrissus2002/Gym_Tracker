from openai import OpenAI

client = OpenAI()

def get_chagpt_response(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"assitant", "content":"You are a exercise assistant that will recommend workouts for the user"},
            {"role":"user", "content":prompt}
            ],
            stream=True
    )
    return completion.choices[0].message