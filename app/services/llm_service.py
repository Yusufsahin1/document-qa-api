from openai import OpenAI
from app.core.config import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY) # singleton client instance for OpenAI API

def build_prompt(question: str, chunks: list[dict]) -> str:
    """
    Builds a RAG prompt by combining retrieved chunks as context with the user question.
    """
    context = ""
    for i, chunk in enumerate(chunks):
        context += f"\n[Source {i+1} - Page {chunk['page']}]\n{chunk['text']}\n"

    prompt = f"""You are a helpful assistant that answers questions based only on the provided context.
If the answer is not found in the context, say "This information is not available in the document."

Context:
{context}

Question: {question}

Answer:"""
    return prompt


def generate_answer(question: str, chunks: list[dict]) -> str:
    """
    Sends the prompt to OpenAI and returns the generated answer.
    """
    built_prompt = build_prompt(question, chunks)
    answer = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": built_prompt}]
    )
    return answer.choices[0].message.content