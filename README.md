# Patient Persona Chatbot

Revolutionizing nursing education through AI-powered virtual patient systems.

## Overview

The **Patient Persona Chatbot** is an innovative project designed to enhance nursing education by simulating realistic patient interactions. This AI-powered tool replaces traditional actor-based patient training with a more scalable, cost-effective, and flexible solution. It provides nursing students with diverse learning experiences while improving the quality and efficiency of their training.

### Key Features

- **Patient Simulation**: Simulates patients with varied backgrounds to help nursing students identify:
  - Substance use
  - Substance-related riding/driving risk
  - Substance use disorder (ages 12-21)
- **CRAFFT Manual Integration**: Students follow the CRAFFT manual to assess patient substance use problems.
- **Customizable Scenarios**: Nursing instructors can tailor patient histories and scenarios to meet specific educational goals.
- **Performance Feedback**: Offers immediate evaluations and feedback to students, enabling precise skill development.
- **Transcript Downloads**: Allows students to download a complete conversation with the virtual patient as a PDF.

## Technologies Used

- **[Streamlit](https://streamlit.io/)**: For building an interactive user interface.
- **OpenAI Assistant API**: Powers the chatbot's natural language processing capabilities.

## Installation

1. Clone this repository:
   ```bash
   https://github.com/Draconian10/Nursing_Project.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key:
   - Create a `.env` file in the root directory.
   - Add your OpenAI API key:
     ```env
     OPENAI_API_KEY=your_api_key_here
     SUPABASE_URL=your_api_key_here
     SUPABASE_KEY=your_api_key_here
     AZURE_ENDPOINT=your_api_key_here
     AZURE_OPENAI_KEY=your_api_key_here
     ```
4. Run the application:
   ```bash
   streamlit run Patient_Persona_Chat_Bot.py
   ```

## Usage

1. Launch the application in your browser.
2. Choose a patient persona and scenario.
3. Interact with the chatbot, asking and answering questions as you would with a real patient.
4. Receive instant feedback on your performance.
5. Download a transcript of the interaction as a PDF.

---

Together, let's improve nursing education through technology!
