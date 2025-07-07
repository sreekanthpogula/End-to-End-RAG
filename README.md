# End-to-End RAG

An end-to-end Retrieval-Augmented Generation (RAG) project that demonstrates how to combine retrieval techniques with generative models for enhanced question answering and information retrieval.

## Project Structure

```
End-to-End-RAG/
├── data/
│   └── sample_documents/
├── app.py
├── requirements.txt
└── README.md
```

## Features

- **Data Ingestion:** Load and preprocess documents from the local directory.
- **Embedding:** Generate vector embeddings for documents and queries using modern models.
- **Retriever:** Efficiently retrieve relevant documents based on semantic similarity.
- **Generator:** Produce answers using a generative language model and retrieved context.
- **End-to-End Pipeline:** Seamlessly orchestrate the RAG workflow from ingestion to answer generation.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

1. **Prepare Data:** Add your documents to the `data/news_articles/` directory.
2. **Run the Pipeline:**
    ```bash
    python app.py
    ```

## File Overview

- `data/news_articles/`: Example documents for retrieval.
- `app.py`: Main entry point for the RAG pipeline.
- `requirements.txt`: Lists required Python packages.

## Example

```bash
python3 app.py
```

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE [LICENSE](LICENSE).

## Contributing
Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute.
