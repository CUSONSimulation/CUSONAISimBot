# AI Sim Bot

Revolutionizing education through AI-powered virtual patient systems.

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

## Setup

1. [Create an account](https://platform.openai.com/api-keys) on OpenAI.com.
    * [Generate an API key]((https://platform.openai.com/api-keys))
    * Make sure to write down the key because you won't be able to see it again.
    * You can always delete and create another one.
2. [Create an account](https://github.com/signup) on Github.com.
    * [Fork this project.](https://github.com/AISimBot/AISimBot/fork)
    * Give it a name and click "Create fork."
    * Save the URL to the forked repository.
3. [Create an account](https://streamlit.app/) on Streamlit.app.
    * Click "Create an app"
    * Select "Deploy from repo"
    * Type the url for your forked repository.
    * Give a unique and memorable URL for your app.
    * Choose Advanced settings.
    * Under the secrets, provide your OpenAI API key as well as the password to access the app with the exact format below.
    * Choose save and click deploy.

```toml
OPENAI_API_KEY = "xxxxxx"
password = "abcd1234"
```

Saving secrets takes a few minutes to propagate, so most likely you'll get an error messsage about missing key. Wait for a few minutes, and reboot the app under "Manage app."

If you still get the same error, make sure you can find the key in the [app settings > Secrets.](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)

Once everything goes well, you'll see the user interface.

In order to test to make sure everything works:
1. Click Share and get the link for your app.
2. Either log out from Sstreamlit or open the link in a private browsing window.
    * Chrome, Safari, Edge: Ctrl-Shift-N (Windows) or Command-Shift-N (macOS)
    * Firefox: Ctrl-Shift-P (Windows) or Command-Shift-P (macOS)---

Together, let's improve education through technology!

## Technologies Used

- **[Streamlit](https://streamlit.io/)**: For building an interactive user interface.
- **OpenAI Assistant API**: Powers the chatbot's natural language processing capabilities.


## Contributers

* Yash Pankhania
* Tiffany Kim
