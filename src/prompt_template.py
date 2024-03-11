RAG_PROMPT_TEMPLATE = """
    Your task is to answer questions based in the given context.
    Dont invent anything that is out of the context.
    Answer in atleast 350 characters.

    %CONTEXT%
    {context}

    %Question%
    {question}

    Do not copy the content. Use your own words
    Answer:
 """