# ElevenLabs Conversation AI WebSocket Demo
This script demonstrates direct interaction with the ElevenLabs API via WebSocket for sending audio and receiving responses, including audio responses and logging.

## ⚙️ Requirements
- Python 3.x
- Access to the ElevenLabs API (API Key)
- An ElevenLabs Agent ID

## 💾 Installation

1.  **Clone the Repository (If you haven't already):**
    ```bash
    # If you cloned this repository, you are already here!
    # Otherwise:
    # git clone <your-repo-url> # Replace <your-repo-url> with the actual repo URL
    # cd <your-repo-directory>
    ```
2.  **Install Dependencies:** The easy way!
    ```bash
    pip install -r requirements.txt
    ```
    *(For Windows users, see the specific Windows installation section below)*

3.  **Configure Your Secrets:** Create a `.env` file in the project root (or rename `.env.example` if provided) and fill in your details. **Never commit your `.env` file!**
    ```dotenv
    API_KEY="YOUR_ELEVENLABS_API_KEY"
    AGENT_ID="YOUR_ELEVENLABS_AGENT_ID"
    # WEBSOCKET_BASE_URI= # Optional: Specify an alternative WebSocket server (defaults to ElevenLabs)
    INPUT_AUDIO_FILE=input.wav # Default input audio file name
    OUTPUT_DIR=output          # Directory for audio responses
    LOG_DIR=log                # Directory for text logs
    ```

## ▶️ Running the Demo

1.  **Prepare Your Input:** Make sure you have an audio file named `input.wav` (or whatever you set in `.env`) in the project directory. This is what the script will send.
2.  **Launch the Magic:**
    ```bash
    python app.py
    ```

The script will connect via WebSocket, send your audio file, receive responses (including audio!), save the audio replies in the `output` folder, and log the conversation details in the `log` folder.

---

### 💻 Installation (Windows Specifics)

Because Windows sometimes likes to do things its own way...

1.  **Install Python:** If you don't have it, grab it from [python.org](https://www.python.org/). **Crucially, check the box "Add Python to PATH"** during installation.
2.  **Install Dependencies (Windows Edition):**
    *   Open Command Prompt (`cmd`). Not PowerShell, just good old `cmd`.
    *   Navigate to your project directory: `cd path\to\your\project`. Use backslashes!
    *   Run the provided batch file (if one exists):
        ```cmd
        install_deps.bat
        ```
    *   Or, do it manually like a pro (recommended):
        ```cmd
        py -m pip install -r requirements.txt
        ```
    *   **Troubleshooting Notes:**
        *   Installing `numpy` might require Microsoft C++ Build Tools. If you see errors, you might need to install them from Microsoft's website.
        *   Installing `soundfile` might need the `libsndfile` library. If `pip install soundfile` fails, search online for instructions on installing `libsndfile` for Windows. It usually involves downloading a pre-compiled library file.
        *   Using an IDE like PyCharm or VS Code is highly recommended. They often handle environment complexities better.

### ▶️ Running (Windows Specifics)

1.  Open Command Prompt (`cmd`).
2.  Navigate to your project directory.
3.  Run the script using `py`:
    ```cmd
    py app.py
    ```

---

_And remember, like any good conversation, things might get interesting! Check the `output` and `log` directories to see (and hear) what happened. Happy experimenting!_ ✨🎙️

