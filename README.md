# TheAI Chatbot

TheAI Chatbot is a Python-based desktop application that lets you chat with an AI-powered chatbot. Use the hugginFace chat language model to generate responses based on user input. To create this code I based myself on the [Soulter](https://github.com/Soulter) project  thanks to which I was able to exploit all the potential of this alternative to the API.
## Cookies

<details>
<summary>How to Get Cookies?</summary>

- Install the `Cookie-Editor` extension for [Chrome](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) or [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)
- Go to [HuggingChat](https://huggingface.co/chat) and **login**
- Open the extension
- Click `Export` on the bottom right, then `Export as JSON` (This saves your cookies to the clipboard)
- Paste your cookies into a file `cookies.json`

</details>

## Installation

<details>
<summary>How to install and run TheAI Chatbot?</summary>

1. Clone the repository from GitHub:
   ```shell
   git clone https://github.com/seregonwar/TheAi.git


2. Navigate to the project directory:
   ```shell
   cd TheAi

3. Create a virtual environment (optional but recommended):
   ```shell
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   venv\Scripts\activate  # On Windows

4. Install the required dependencies:
   ```shell
   pip install -r requirements.txt
5. Run the application:
   ```shell
   python AI.py
</details>

## Usage

<details>
<summary>How to Use?</summary>

1. Once the application is running, you can start chatting with the AI chatbot.
2. Type your message in the input field and press Enter to send it.
3. The chatbot will generate a response based on your input and display it in the chat window.
4. You can also perform online searches by typing "[SEARCH]" followed by your query. The chatbot will provide search results for you.
5. To change the theme of the application, click on the "Options" button and select either the "Light Theme" or "Dark Theme".
6. To upload a file containing your message, click on the "Options" button and select "Upload File". The contents of the file will be sent to the chatbot for processing.

</details>

## Dependencies

TheAI Chatbot relies on the following dependencies:

- PyQt5: Used for the graphical user interface.
- hugchat: A Python library that wraps hugginface for chatbot functionality.
- googlesearch: Used for performing online searches.
- pyttsx3: Used for text-to-speech synthesis.

You can find more details and installation instructions for these dependencies in their respective documentation.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.

## Acknowledgements

TheAI Chatbot was created by [Seregonwar](https://github.com/seregonwar) and [Maudrigal](https://github.com/Maudrigal) as a project for [Course/Workshop/Personal Learning].

If you have any questions or need assistance, feel free to contact  [Seregonwar](https://github.com/seregonwar) and [Maudrigal](https://github.com/Maudrigal).
