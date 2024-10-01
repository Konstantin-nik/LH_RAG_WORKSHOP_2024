import os
import json

import pandas as pd
import numpy as np

from dotenv import load_dotenv
from sqlite_calls import SQLiteCalls
from anthropic_calls import AnthropicCalls
from sklearn.metrics.pairwise import cosine_similarity


def get_context(embedding, role="", n=1):
    chat_df = SQL_calls.load_chat_to_dataframe(role)
    context = find_top_n_similar(chat_df, embedding, n)
    return context


def find_top_n_similar(df, user_input_embedding, n=5):
    if df.empty or 'embedding' not in df.columns:
        print("The DataFrame is empty or missing the 'embedding' column.")
        return pd.DataFrame()
    
    df['embedding'] = df['embedding'].apply(
        lambda emb: json.loads(emb) if isinstance(emb, str) else emb
    )
    df['similarity'] = df['embedding'].apply(
        lambda emb: similarty_search(user_input_embedding, emb)
    )

    top_n_df = df.sort_values(by='similarity', ascending=False).head(n)
    # To have messages in the correct order
    top_n_df = top_n_df.sort_values(by='date', ascending=True)

    return top_n_df


def similarty_search(embedding1, embedding2):
    embedding1 = np.array(embedding1).reshape(1, -1)
    embedding2 = np.array(embedding2).reshape(1, -1)

    similarity = cosine_similarity(embedding1, embedding2)

    return similarity[0][0]


def send_message(text: str, clear_after_response=False) -> str:
    key_words = ['remember', 'memorize', 'learn']

    embedding = LLM_calls.get_embedding(text)
    context = get_context(embedding, role="user", n=2)

    if any([ word in text.lower() for word in key_words ]): # Now we are saving only messages with key words
        SQL_calls.save_message(
            role="user",
            message=text,
            embedding=embedding
        )

    if context.empty:
        print("Context is empty")
        combined_message = text
    else:
        context_messages = context["message"].tolist()
        print("Context:", *context_messages, "------", sep="\n")
        context_message = '\n'.join(context_messages)
        combined_message = f"Provided context:\n{context_message}\nUser message:\n{text}"    

    llm_response = LLM_calls.chat(combined_message, clear_after_response)
    
    return llm_response


def conversation():
    message = ''

    while message != "END":
        message = input("User: ")
        print("------", message, "------", sep='\n')
        if message != "END":
            send_message(message, clear_after_response=True)


if __name__ == "__main__":
    load_dotenv()
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    LLM_calls = AnthropicCalls(api_key=ANTHROPIC_API_KEY, stream=True)
    SQL_calls = SQLiteCalls("key_words.db")

    conversation()