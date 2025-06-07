# Gemini Live API Workshop

This project is a demonstration for a beginner-friendly workshop on how to use the Gemini Live API. It shows how to build a simple application that captures audio from a microphone, streams it to the Google Gemini API for real-time generative responses, and plays back the audio output.

## Features

*   **Real-time Audio Streaming:** Captures audio from your microphone and streams it directly to the Gemini API.
*   **Audio Responses:** Receives audio output from Gemini and plays it back in real-time.
*   **Text Transcripts:** Displays the text version of Gemini's responses in the console.
*   **Function Calling Example:** Includes a demonstration of how to use function calling with the Gemini API to get structured data (e.g., list of GDG Buea organizers).

## Requirements

To run this project, you will need:

*   **Python 3.9 or higher:** Ensure you have a compatible Python version installed.
*   **Google API Key:** You'll need a Google API Key with the Gemini API enabled. You can obtain one from the [Google AI Studio](https://aistudio.google.com/app/apikey).
*   **Microphone:** A working microphone connected to your computer for audio input.
*   **Speakers or Headphones:** To hear the audio responses from Gemini.
*   **Git:** For cloning the repository.

## Installation Steps

Follow these steps to get the project set up and ready to run:

1.  **Clone the Repository:**
    Open your terminal or command prompt and run the following command to clone this project:
    ```bash
    git clone <repository_url> # Replace <repository_url> with the actual URL of this repository
    ```

2.  **Navigate to the Project Directory:**
    Change your current directory to the folder you just cloned:
    ```bash
    cd <project_folder_name> # Replace <project_folder_name> with the name of the cloned directory
    ```

3.  **Create a Virtual Environment (Recommended):**
    It's good practice to create a virtual environment to manage project dependencies separately.
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
    You should see `(venv)` at the beginning of your terminal prompt.

4.  **Install Dependencies:**
    Install all the required Python packages using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set Up Your Google API Key:**
    The application needs your Google API Key to interact with the Gemini API.
    *   Make a copy of the example environment file. In your terminal, run:
        *   On Windows:
            ```bash
            copy example.env .env
            ```
        *   On macOS and Linux:
            ```bash
            cp example.env .env
            ```
    *   Open the newly created `.env` file in a text editor.
    *   Replace `"PASTE YOUR GEMINI API KEY HERE"` with your actual Google API Key. It should look like this:
        ```
        GOOGLE_API_KEY="YOUR_ACTUAL_API_KEY"
        ```
    *   Save and close the `.env` file.

## How to Run

Once you have completed the installation steps:

1.  **Ensure your virtual environment is activated** (you should see `(venv)` in your terminal prompt). If not, reactivate it using the commands from the installation section.
2.  **Make sure your microphone is connected and working.**
3.  **Run the main script:**
    Execute the `live_workshop.py` file using Python:
    ```bash
    python live_workshop.py
    ```
4.  The application will start, and it will begin listening for audio input from your microphone. Speak into your microphone, and you should hear responses from Gemini and see text transcripts in your terminal.
5.  To stop the application, you can usually press `Ctrl+C` in the terminal.

## Function Calling Example

This workshop includes an example of how to use "function calling" with the Gemini API. Function calling allows you to describe functions from your application to Gemini, and have the model intelligently request to call those functions based on user input.

In `live_workshop.py`, you'll find:

*   **`get_gdg_buea_organizers_declaration`**: This is a JSON schema that describes a function named `get_gdg_buea_organizers` to Gemini. It tells Gemini what the function does and what parameters it expects (in this case, none).
*   **`get_gdg_buea_organizers()`**: This is the actual Python function that gets called. It returns a hardcoded list of GDG Buea organizers and their roles.
*   **`tools`**: The function declaration is wrapped in a `types.Tool` object.
*   **`CONFIG`**: The `LiveConnectConfig` is set up with a `system_instruction` that guides Gemini: `"You are an assistant knowledgeable about GDG Buea and its events. If asked about the organizers of GDG Buea, call the function 'get_gdg_buea_organizers'."` It also includes the `tools` in its configuration.

When you run the application, if you ask a question like "Who are the organizers of GDG Buea?", Gemini will understand that it needs to call the `get_gdg_buea_organizers` function. The `live_workshop.py` script doesn't currently explicitly show how the function call is handled and the response sent back to Gemini (this would typically involve receiving a `FunctionCall` object from Gemini, executing your Python function, and then sending a `FunctionResponse` back). However, the setup demonstrates the declaration and instruction part, which is key for enabling this feature.
