# AI-Powered RAG Chatbot with Google Gemini and FAISS

This project is a fully functional **Retrieval-Augmented Generation (RAG)** chatbot built in Python. It leverages Google's Gemini AI, the FAISS library for vector search, and the Telegram Bot API to create an intelligent assistant that can answer questions based on a custom knowledge base.

This project demonstrates a complete end-to-end pipeline for building modern AI applications, from data processing to deployment.

## How It Works

The project consists of two main components:

**1. `database_builder.py` (The "Brain" Builder - Offline Process):**
-   **Reads** a source text document (`data.txt`).
-   **Chunks** the text into smaller, semantically meaningful paragraphs.
-   **Generates Embeddings:** Uses the `google-generativeai` API (`models/embedding-001`) to convert each text chunk into a high-dimensional vector.
-   **Builds Vector Index:** All generated vectors are indexed using **FAISS (Facebook AI Similarity Search)** for ultra-fast similarity search.
-   **Saves Artifacts:** The script outputs a binary `faiss_index.index` file and a `chunks.csv` file that maps the vectors back to their original text.

**2. `rag_bot.py` (The Chatbot - Online Process):**
-   **Loads Knowledge Base:** On startup, the bot loads the FAISS index and the text chunks into memory.
-   **Receives User Query:** Listens for user messages via the Telegram Bot API.
-   **Retrieval Step:**
    1.  Generates an embedding for the user's question.
    2.  Searches the FAISS index for the `k` most semantically similar text chunks from the knowledge base.
-   **Augmented Generation Step:**
    1.  Constructs a detailed **prompt** for the Gemini (`gemini-1.5-flash`) model, containing both the retrieved context chunks and the original user question.
    2.  Instructs the model to answer the question **strictly based on the provided context**.
-   **Delivers Answer:** Sends the generated, context-aware answer back to the user on Telegram.

## Core Concepts Demonstrated

-   **Retrieval-Augmented Generation (RAG):** Practical implementation of the leading architecture for knowledge-based AI assistants.
-   **Vector Embeddings:** Using language models to convert text into meaningful numerical representations.
-   **Vector Databases:** Using **FAISS** for efficient k-Nearest Neighbors (kNN) search.
-   **API Integration:** Working with `pyTelegramBotAPI` and `google-generativeai`.
-   **Data Processing:** Text chunking and management with `pandas`.
-   **Environment Management:** Using environment variables for API keys.

## How to Set Up

1.  **Clone the repository:**
    ```bash
    git clone [URL_ТВОГО_РЕПОЗИТОРІЯ]
    cd [НАЗВА_ПАПКИ]
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create your knowledge base:**
    -   Place your knowledge source in a file named `data.txt`.
    -   Run the database builder: `python3 database_builder.py`
4.  **Set up environment variables:**
    ```bash
    export BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
    export GOOGLE_API_KEY="YOUR_GOOGLE_AI_API_KEY"
    ```
5.  **Run the bot:**
    ```bash
    python3 rag_bot.py
    ```
