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
    # key_words = ['remember', 'memorize', 'learn']

    embedding = LLM_calls.get_embedding(text)
    context = get_context(embedding, role="user", n=3)

    extracted_data = extract_user_data(text)
    if extracted_data:
        SQL_calls.save_message(
            role="user",
            message=str(extracted_data),
            embedding=embedding
        )

    if context.empty:
        print("Context is empty")
        combined_message = text
    else: # Now we will check if context we get is relevant to our message
        context_messages = context["message"].tolist()
        cleared_context = []
        for context_chunk in context_messages:
            if is_relevant(context_chunk, text):
                cleared_context.append(context_chunk)

        # If there are any chunks left:
        if len(cleared_context) > 0:
            print("Context:", *cleared_context, "------", sep="\n")
            context_message = '\n'.join(cleared_context)
            combined_message = f"Provided context:\n{context_message}\nUser message:\n{text}"    
        else:
            combined_message = text

    llm_response = LLM_calls.chat(combined_message, clear_after_response)
    
    return llm_response


def is_relevant(chunk: str, query: str):
    response = context_determinator.chat(
        f"Query: {query}\n\nChunk: {chunk}\n\nIs this chunk relevant to the query? Respond in JSON format.",
        should_print=False,
        clear_after_response=True
    )
    print("Chunk:\n", chunk)
    print("Response:\n", response.content[0].text)
    return json.loads(response.content[0].text)["is_relevant"]


def extract_user_data(query: str):
    extractor_tool = {
        "name": "save_extracted_data",
        "description": "Save a given data extracted from the users query.",
        "input_schema": {
            "type": "object",
            "properties": {
                "chunk": {
                    "type": "string",
                    "description": "Extracted data."
                }
            },
            "required": ["chunk"]
        }
    }
    
    response = user_data_extractor.chat(
        f"Query: {query}\n\nExtracts user related data from this query? Use tools to save it.",
        should_print=False,
        tools = [extractor_tool],
        clear_after_response=True
    )
    if response.stop_reason == "tool_use":
        for item in response.content:
            if item.type == "tool_use":
                if item.name == "save_extracted_data":
                    print("\nTool_use: ", item)
                    print("------")
                    return item.input.get("chunk", False)
    # print("Response:\n", response)
    return False


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
    context_determinator = AnthropicCalls(
        api_key=ANTHROPIC_API_KEY, 
        max_tokens=400,
        system_prompt="You are a helpful assistant that determines if a chunk of text is relevant to a given query.\n" +
            "Respond with JSON object containing a boolean 'is_relevant' field and a 'reason' field explaining your decision"
    )

    user_data_extractor = AnthropicCalls(
        api_key=ANTHROPIC_API_KEY, 
        max_tokens=1024,
        system_prompt="You are a helpful assistant that extracts chunk of user related data from given query.\n"
    )

    conversation()
