# Example usage
# query_text = "What are the latest news articles?"
# Example query and response generation
question = "Tell me about the pando startup and its recent funding round."
relevant_chunks = query_documents(question)
answer = generate_response(question, relevant_chunks)
print(f"Question: {question}\nAnswer: {answer}\n")

# OOV query example
oov_question = "What is the capital of France?"
oov_relevant_chunks = query_documents(oov_question)
oov_answer = generate_response(oov_question, oov_relevant_chunks)
print(f"Question: {oov_question}\nAnswer: {oov_answer}\n")