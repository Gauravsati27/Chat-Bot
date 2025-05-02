# Chat-Bot
# AI Chatbot with Admin Dashboard

A simple AI chatbot built with Streamlit, including an admin dashboard for usage analytics.

## Features
- Clean and modern chat interface
- Powered by an AI language model (e.g., Microsoft's DialoGPT)
- Real-time chat responses
- Chat history persistence during session
- **Admin dashboard to view chat logs and basic analytics (query frequency, locations)**
- **Logging of user queries and locations**

## Setup

1.  Install Python 3.8 or higher.
2.  Clone or download this repository.
3.  Navigate to the project directory in your terminal.
4.  **(Recommended)** Create and activate a virtual environment:
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
5.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
    *(Ensure `requirements.txt` includes `streamlit`, `pandas`, `altair`, `pyarrow`, and the necessary transformer library like `transformers`)*

## Running the Application

### 1. Running the Chatbot

-   Start the main Streamlit chat app:
    ```bash
    streamlit run app.py
    ```
-   Open your web browser and navigate to the URL shown in the terminal (usually `http://localhost:8501`).
-   Start chatting with the AI!

### 2. Running the Admin Dashboard

-   In a **separate terminal** (or after stopping the main app), run the admin page:
    ```bash
    streamlit run admin.py
    ```
-   Navigate to the URL provided (often `http://localhost:8501` if the main app isn't running, or a different port like `8502` if it is).
-   Log in using the credentials configured (likely in `admin_config.json` or similar).

## Notes
- The first run might download the AI model, which could take a few minutes depending on the model size and your internet connection.
- The chatbot and admin panel run entirely on your local machine.
- Chat history in the main app is maintained during the session but will be cleared when you close the browser tab/window.
- **User interactions (timestamp, query, location) are logged to `chat_logs.csv` (or a similar file) in the project directory.**
