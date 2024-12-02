
## Voice-to-Voice Chatbot for Persian Language

This project is a **voice-to-voice chatbot** inspired by the capabilities of tools like ChatGPT. It utilizes open-source technologies to deliver a conversational AI experience entirely in the **Persian language**. By combining **Text-to-Speech (TTS)**, **Language Modeling (LM Studio)**, and **Automatic Speech Recognition (ASR)**, it creates a seamless environment for natural voice communication.

### Key Features:
- **Voice-to-Voice Interaction:** Users can speak to the chatbot and receive spoken responses.
- **Persian Language Support:** Focused on enhancing the experience for Persian-speaking users.
- **Open-Source Language Models:** Integrates widely available and adaptable TTS, LM, and ASR tools for efficient performance.
- **Customizable Components:** Built with modularity in mind, making it easy to replace or upgrade specific components like TTS or ASR systems.

This project showcases the power of open-source technology in building accessible, localized AI applications. Perfect for developers interested in natural language processing, voice technology, and Persian language support.


---

## Step 1: Install LMStudio and Set Up a Large Language Model

To power the voice-to-voice chatbot, we rely on **LMStudio** and its ability to host large language models (LLMs). Follow the steps below to install and set up LMStudio:

### Installation of LMStudio
1. Download and install **LMStudio** from its official repository or website. [LMStudio GitHub](https://github.com/your-link-here)
2. Set up LMStudio following the installation instructions provided in its documentation.

### Choosing a Language Model
For this project, we used the **[CohereForAI/aya-23b](https://huggingface.co/CohereForAI/aya-23-8B)** language model. You can choose a larger model if your hardware supports it.

- **Recommended Hardware:**
  - At least ** NVIDIA RTX 3070 GPU ** (or better for faster inference times).
  - The inference time for Aya-23b on our setup (2x3070 GPUs) is less than a minute per generation.

### Setting Up the Model
1. Download the model weights from Hugging Face: [Aya-23b Model](https://huggingface.co/CohereForAI/aya-23-8B).
2. Load the model in **LMStudio**.

### Running the LMStudio API
1. Once the model is set up in LMStudio, start the API server on **port 1234** .
2. Verify that the API server is running correctly by visiting `http://localhost:1234`.

You now have a functional API endpoint that the chatbot will use to generate responses.

---

## Step 2: Install and Set Up Text-to-Speech (TTS)

After successfully running the **Language Model (LLM)**, the next step is to convert the generated text into speech. For this, we use the **[Persian TTS Coqui](https://github.com/karim23657/Persian-tts-coqui)** project, which provides a robust and efficient text-to-speech engine for Persian.

### Installation Steps
1. Clone the Persian TTS Coqui repository:
   ```bash
   git clone https://github.com/karim23657/Persian-tts-coqui
   cd Persian-tts-coqui
   ```

2. Create a Python environment with **Python 3.9** (required for compatibility):
   ```bash
   python3.9 -m venv tts_env
   source tts_env/bin/activate  # For Linux/macOS
   tts_env\Scripts\activate     # For Windows
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the TTS System
1. To test the TTS system, run the `main.py` file in the repository:
   ```bash
   python main.py
   ```

2. Ensure the TTS system can successfully process input text and generate speech.

### Notes
- Make sure the **Python 3.9 environment** is active before running the TTS system.
- Check the repository's documentation for advanced configuration options if needed.

Once the TTS is running, it can be used to convert the LLM's text outputs into high-quality Persian speech.

---

## Step 3: Set Up the Application Environment and Run the App

The final step is to set up the main application, which integrates all components (LLM, TTS, and ASR) to create a fully functional voice-to-voice chatbot. This step uses the **[Hezar Persian Whisper](https://github.com/hezarai/)** system for converting human speech to text (ASR - Automatic Speech Recognition).

### Setting Up the Environment
1. Create a Python environment with **Python 3.11**:
   ```bash
   python3.11 -m venv app_env
   source app_env/bin/activate  # For Linux/macOS
   app_env\Scripts\activate     # For Windows
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Ensure all dependencies required by Hezar and the app are installed successfully.

### Running the Application
1. Navigate to the directory where the `main.py` file is located.
2. Run the application:
   ```bash
   python main.py
   ```

3. By default, your app will be accessible at `http://localhost:8000`. You should see a UI similar to the screenshot provided earlier.

### About Hezar Persian Whisper
This project utilizes **Hezar Persian Whisper**, an open-source Persian ASR (Automatic Speech Recognition) library. It converts spoken human input into text, which is then processed by the LLM and TTS systems.

You can find more about Hezar here: [Hezar Persian Whisper](https://github.com/hezarai/).  
Don’t forget to ⭐ **star their repository** if you find it helpful!

### Notes:
- Ensure all components (LLM API, TTS, and ASR) are running correctly before starting the app.
- For additional customization, refer to the `main.py` file and Hezar's documentation.


