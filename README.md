# TmSlackReporter Crew

Welcome to the TmSlackReporter Crew project, powered by [crewAI](https://crewai.com)! This project uses a team of AI agents to analyze Slack channel activity and generate a performance report for a specified user.

## Core Functionality

The TmSlackReporter crew consists of two AI agents:

1.  **Slack Channel Summarizer (`slack_summarizer`):** This agent connects to your Slack workspace, gathers messages from a specified channel within a given time period, and identifies actions taken by a particular user.
2.  **User Performance Reporter (`action_reporter`):** This agent takes the list of actions and generates a performance report, detailing the user's contributions, potential strengths, weaknesses, and areas for improvement.

The primary output is a `report.md` file containing this performance analysis. The crew is configured to use models via [OpenRouter](https://openrouter.ai/) for its main AI capabilities and local Ollama models for embeddings.

## Installation

Ensure you have Python >=3.10 and <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management.

1.  **Install Ollama (for Embeddings):**
    This project uses local Ollama models for generating embeddings. Download and install Ollama from [ollama.com](https://ollama.com). After installation, ensure the Ollama application is running. You'll also need to pull the embedding model specified in your `.env` file (e.g., `ollama pull nomic-embed-text`).

2.  **Set up OpenRouter (for Main LLM):**
    The main AI agents in this project use models via OpenRouter. You will need an OpenRouter API key.

3.  **Install UV:**
    If you don't have UV installed, get it by running:
    ```bash
    pip install uv
    ```

4.  **Install Project Dependencies:**
    Navigate to your project directory and install the dependencies. You can use the crewAI CLI:
    ```bash
    crewai install
    ```
    Alternatively, you can install directly with UV using the `pyproject.toml` file:
    ```bash
    uv pip install .
    ```

## Configuration

1.  **Environment Variables (`.env` file):**
    Create a `.env` file in the root of your project. This file will store necessary configurations.
    You'll need to define:
    *   `CREWAI_OPENROUTER_MODEL_ID`: The OpenRouter model to be used by the agents (e.g., `openrouter/google/gemini-flash-1.5`).
    *   `CREWAI_OPENROUTER_BASE_URL`: The base URL for the OpenRouter API (usually `https://openrouter.ai/api/v1`).
    *   `OPENROUTER_API_KEY`: Your API key for OpenRouter.
    *   `CREWAI_OLLAMA_EMBEDDER_MODEL_ID`: The Ollama model to be used for embeddings (e.g., `nomic-embed-text`).

    The Slack tools used by the `slack_summarizer` agent (via `SlackToolSet`) might require additional environment variables, such as API keys for Slack or a service like Composio if it's used to manage tool integrations. Please check the documentation for `SlackToolSet` or any underlying libraries (like Composio) for specific requirements.

    Example `.env` content:
    ```env
    CREWAI_OPENROUTER_MODEL_ID="openrouter/google/gemini-flash-1.5"
    CREWAI_OPENROUTER_BASE_URL="https://openrouter.ai/api/v1"
    OPENROUTER_API_KEY="sk-or-your-openrouter-api-key"
    CREWAI_OLLAMA_EMBEDDER_MODEL_ID="nomic-embed-text"
    # Add other necessary keys like SLACK_API_TOKEN or COMPOSIO_API_KEY if required by SlackToolSet
    ```

2.  **Agent Configuration (`agents.yaml`):**
    Modify `src/tm_slack_reporter/config/agents.yaml` to customize the roles, goals, and backstories of the `slack_summarizer` and `action_reporter` agents.

3.  **Task Configuration (`tasks.yaml`):**
    Modify `src/tm_slack_reporter/config/tasks.yaml` to adjust the descriptions and expected outputs for the `gather_context_task` and `report_task`.

## Running the Project

The project defines several scripts in `pyproject.toml` for interacting with your crew. These are executed via Python's entry point mechanism (e.g., `python -m tm_slack_reporter.main run`) or potentially through a command like `run_crew` if your environment is set up to recognize project scripts.

*   **Run the Main Reporting Task:**
    The primary way to run the crew and generate a report is using the `run` command. You can execute this by calling the `run` function in `src/tm_slack_reporter/main.py`.
    By default, this uses inputs defined in `main.py`:
    ```python
    inputs = {
        "slack_channel_name": "#tm-slack-reporter-test",
        "time_period": "last 30 days",
        "slack_user_name": "echo",
    }
    ```
    Modify these inputs in `src/tm_slack_reporter/main.py` to target different channels, users, or time periods.
    To run using the script defined in `pyproject.toml` (assuming it's correctly installed in your path or using a virtual environment):
    ```bash
    run_crew 
    # Or, more explicitly:
    # python -m tm_slack_reporter.main run
    ```
    The command `crewai run` (mentioned in the original template) might also work if it's a generic crewAI CLI command that detects and runs the project.

*   **Other Operations:**
    The `pyproject.toml` also defines scripts for `train`, `replay`, and `test` operations, which correspond to functions in `src/tm_slack_reporter/main.py`. These are typically used for more advanced crew management and development:
    *   `train`: For training the crew.
        ```bash
        # Example: train_crew <n_iterations> <filename>
        # python -m tm_slack_reporter.main train <n_iterations> <filename>
        ```
    *   `replay`: For replaying a crew execution from a specific task.
        ```bash
        # Example: replay_crew <task_id>
        # python -m tm_slack_reporter.main replay <task_id>
        ```
    *   `test`: For testing the crew execution.
        ```bash
        # Example: test_crew <n_iterations> <eval_llm>
        # python -m tm_slack_reporter.main test <n_iterations> <eval_llm>
        ```
    Consult `src/tm_slack_reporter/main.py` for details on how these functions expect arguments.

## Output

The primary output of a successful run is the `report.md` file, created in the root folder of your project. This file contains the detailed performance report generated by the `action_reporter` agent.

## Understanding Your Crew

The TmSlackReporter Crew is composed of:

*   **Agents (`src/tm_slack_reporter/config/agents.yaml`):**
    *   `slack_summarizer`: Gathers user actions from Slack.
    *   `action_reporter`: Analyzes actions and generates a performance report.
*   **Tasks (`src/tm_slack_reporter/config/tasks.yaml`):**
    *   `gather_context_task`: Assigned to the `slack_summarizer` to collect data.
    *   `report_task`: Assigned to the `action_reporter` to produce the final report.
*   **Crew Logic (`src/tm_slack_reporter/crew.py`):** Defines how agents and tasks are orchestrated, including the LLM configuration (using OpenRouter for main tasks and Ollama for embeddings) and sequential processing.
*   **Tools (`src/tm_slack_reporter/tools/`):** Contains tools like `SlackToolSet` used by agents to interact with external services.

## Customizing Your Crew

*   Modify `src/tm_slack_reporter/config/agents.yaml` to redefine agent roles, goals, or backstories.
*   Modify `src/tm_slack_reporter/config/tasks.yaml` to change task descriptions or expected outputs.
*   Modify `src/tm_slack_reporter/crew.py` to alter the crew's workflow, change LLMs, add new tools, or integrate different agents.
*   Modify `src/tm_slack_reporter/main.py` to change default inputs for the `run` script or adjust how other scripts (`train`, `replay`, `test`) are invoked.

## Support

For support, questions, or feedback regarding the TmSlackReporter Crew or crewAI:
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
