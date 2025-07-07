import os
import chromadb

from dotenv import load_dotenv
from openai import OpenAI
from chromadb.utils import embedding_functions


# Load environment variables from .env file
load_dotenv()


# Set OpenAI API key
openai_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_key,
    model_name="text-embedding-3-small"
)

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(
    path="chroma_persistent_storage"
)
collection_name = "News_Articles"
collection = chroma_client.get_or_create_collection(
    name=collection_name,
    embedding_function=openai_ef
)

client = OpenAI(api_key=openai_key)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that provides information about news articles."
        },
        {
            "role": "user",
            "content": "What are the latest news articles?"
        }
    ],
)

print("Response from OpenAI:", response.choices[0].message.content)

# Function to add a news article to the collection
def load_documents_from_directory(directory_path):
    """Load text documents from a specified directory and add them to the ChromaDB collection.
    """
    print(f"Loading documents from directory: {directory_path}")
    documents = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            with open(os.path.join(directory_path, filename), "r", encoding="utf-8") as file:
                content = file.read()
                print(f"Loaded document: {filename}")
                # Append the content to the documents list
                documents.append({"id": filename, "text": content})
    return documents

# Function to split text into chunks
def split_text_into_chunks(text, chunk_size=1000, chunk_overlap=20):
    """Split text into smaller chunks of a specified size.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - chunk_overlap  # Overlap for the next chunk
    return chunks

# Load documents from the specified directory
directory_path = "./news_articles"  # Replace with your directory path
documents = load_documents_from_directory(directory_path)

print(f"Total documents loaded: {len(documents)}")

# Split documents into chunks and add them to the collection
chunked_documents = []
for doc in documents:
    chunks = split_text_into_chunks(doc["text"])
    for i, chunk in enumerate(chunks):
        chunked_documents.append({
            "id": f"{doc['id']}_chunk_{i}",
            "text": chunk
        })

print(f"Total chunks created: {len(chunked_documents)}")

# Function to generate embeddings using OpenAI API
def get_openai_embeddings(text):
    """Generate embeddings for a list of texts using OpenAI API.
    """
    client = OpenAI(api_key=openai_key)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    embedding = response.data[0]['embedding']
    print(f"===Generated embedding for text:===")
    return embedding

# Generate embeddings for the chunked documents
for doc in chunked_documents:
    print(f"===Generating embedding for document ID: {doc['id']}===")
    # Generate embedding for the text chunk
    embedding = get_openai_embeddings(doc["text"])
    doc["embedding"] = embedding

# Upsert documents with embeddings to the ChromaDB collection
for doc in chunked_documents:
    print(f"===Upserting document ID: {doc['id']}===")
    # Upsert the document into the collection
    collection.upsert(
        ids=[doc["id"]],
        documents=[doc["text"]],
        embeddings=[doc["embedding"]]
    )

# Query the collection to verify the documents
def query_documents(query_text, top_k=2):
    """Query the ChromaDB collection for similar documents based on a query text.
    """
    print(f"===Querying documents for: {query_text}===")
    query_embedding = get_openai_embeddings(query_text)
    results = collection.query(
        query_texts=query_text,
        n_results=top_k
    )
    
    # Extract the relevant information from the chunks
    relevant_chunks = [doc for sublist in results['documents'] for doc in sublist]
    print(f"===Found {len(relevant_chunks)} relevant chunks===")

    # for idx, doc in enumerate(relevant_chunks):
    #     doc_id = results['ids'][0][idx]
    #     distance = results['distances'][0][idx]
    #     print(f"Document ID: {doc_id}, Distance: {distance}")
    return relevant_chunks


# Function to generate a response based on the query using OpenAI API
def generate_response(question, relevant_chunks):
    """Generate a response to a question based on relevant chunks using OpenAI API.
    """
    print(f"===Generating response for question: {question}===")
    context = "\n\n".join(relevant_chunks)
    prompt = (
        "You are an assistant for question-answering tasks. Use the following pieces of "
        "retrieved context to answer the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the answer concise."
        "\n\nContext:\n" + context + "\n\nQuestion:\n" + question
    )
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            },
            {
                "role": "user",
                "content": question,
            }
        ],
    )

    answer = response.choices[0].message
    return answer


# Example usage
# query_text = "What are the latest news articles?"
# Example query and response generation
question = "Tell me about the pando startup and its recent funding round."
relevant_chunks = query_documents(question)
answer = generate_response(question, relevant_chunks)

# OOV query example
oov_question = "What is the capital of France?"
oov_relevant_chunks = query_documents(oov_question)
oov_answer = generate_response(oov_question, oov_relevant_chunks)

# Print the generated answer
print(f"===Generated Answer: {answer}===")
print(f"===Generated OOV Answer: {oov_answer}===")