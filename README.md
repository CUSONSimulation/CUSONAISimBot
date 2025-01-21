# AI Sim Bot

Education through AI-Powered Simulations

## Overview

The AI SimBot is a cutting-edge tool designed to enhance educational experiences through realistic verbal interaction simulations. Initially created for nursing students to practice the CRAFFT, a screening tool for identifying substance use among youth, it now offers customizable settings for a wide range of educational and professional contexts focused on role-playing and communication skills.

### Key Features

- Customizable Scenarios: Adaptable for various disciplines and learning objectives, including:
  - Communication skills
  - Interviewing techniques
  - Role-playing scenarios
  - Verbal interaction practice

- Flexible Role-Playing: Supports diverse applications, such as:
  - Scenario-based learning in healthcare, social work, law, and more
  - Educational role-plays (e.g., teacher-student, counselor-client, or peer mediation)
  - Professional training (e.g., job interviews, customer service, or team communication)

- Real-Time Feedback: Provides instant evaluations and feedback to refine user skills effectively.

- Transcript Downloads: Allows users to save a complete transcript of the interaction as a Word document for review, reflection, or documentation.

### Benefits

- Accessibility: Practice anytime, anywhere, without the need for live actors or physical spaces.
- Scalability: Support diverse learners and training needs.
- Flexibility: Customize scenarios to meet specific educational or professional goals.
- Cost-Effectiveness: Replace costly and time-intensive role-playing exercises with a digital solution.

## Setup

1. [Create an OpenAI account](https://platform.openai.com/api-keys).  
   - [Generate an API key](https://platform.openai.com/api-keys).  
   - Write down your key, as it will not be shown again.  
   - You can delete and create a new key if needed.  

2. [Create a GitHub account](https://github.com/signup).  
   - [Fork this project](https://github.com/AISimBot/AISimBot/fork).  
   - Name your fork and click **Create fork**.  
   - Save the URL for your forked repository.  

3. [Create a Streamlit account](https://streamlit.app/).  
   - Click **Create an app**.  
   - Select **Deploy from repo**.  
   - Enter the URL of your forked repository.  
   - Provide a unique and memorable URL for your app.  
   - Choose **Advanced settings**, and under **Secrets**, add your OpenAI API key and app password in the following format:  

   ```toml
   OPENAI_API_KEY = "your_openai_api_key"
   password = "your_app_password"
   ```

   - Click **Save** and then **Deploy**.

> **Note:** Secrets may take a few minutes to propagate. If you see an error about a missing key, wait a few minutes and then reboot your app under **Manage app**.  

If the issue persists, confirm that the key appears under **App settings > Secrets**.  
Once set up correctly, you’ll see the app interface.

### Testing Your App

1. Click **Share** to get your app link.  
2. Open the link in a private browsing window or log out of Streamlit.  
   - **Shortcut keys:**  
     - Chrome, Safari, Edge: `Ctrl-Shift-N` (Windows) or `Command-Shift-N` (Mac).  
     - Firefox: `Ctrl-Shift-P` (Windows) or `Command-Shift-P` (Mac).

### Customize

1. Go to your forked repository on GitHub.  
2. Navigate to the `settings.toml` file and click **Edit file**.  
3. Update the file content as needed and click **Commit changes**.  
   - Add a short, descriptive title and summary for your changes.  

The `settings.toml` file uses [TOML](https://toml.io/en/) format. For multiline fields, enclose text in `'''`. You can also use [Markdown](https://www.markdownguide.org/getting-started/) for formatting.

- **Intro**: Displays before users start chatting.  
- **Instruction**: Defines the initial prompt sent to the model.  
- **Sidebar**: Contains fields that appear on the app’s sidebar.  

To update avatars, replace the relevant files in the `assets` folder.

**IMPORTANT**: After commit changes, you need to reboot your Streamlit app from the dropdown menu under Manage App.

## Technologies Used

- [Streamlit](https://streamlit.io/): For building an interactive user interface.
- OpenAI API: For text generation through GPT-4o (large language model), text to speech, and speech to text ((Whisper.)

## Potential Use Cases

The AI SimBot’s versatility makes it valuable for:

- Healthcare and Counseling Training: Practice patient-provider communication and diagnostic skills.
- Youth Development Programs: Role-play scenarios like peer mediation, bullying intervention, or leadership development.
- Cross-Cultural Communication: Improve interactions in diverse cultural contexts.
- Education and Teaching: Prepare for classroom scenarios, student counseling.
- Language Learning: Build conversational fluency and cultural competence.
- Legal Practice: Practice depositions, client consultations, or courtroom questioning.
- Law Enforcement Training: Simulate suspect or witness interviews to sharpen investigative skills.
- Sales and Marketing: Enhance client interaction techniques for persuasion and negotiation.
- Corporate Training: Improve job interview skills, customer service, conflict resolution, and team communication.

## Contributers

* Yash Pankhania
* Tiffany Kim
