# Title: Built a serverless "Tamagotchi" using GitHub Actions, Python, and the new GitHub Models

Hey r/Python,

I wanted to show off a project I built using Python and the new free **GitHub Models** (Azure AI) integration.

**ForkMonkey** is a digital pet that lives in a repo. It doesn't use any external API keys or servers. It's all free, public and uses free mechanism of Github.
[https://github.com/roeiba/forkMonkey](https://github.com/roeiba/forkMonkey)

### Technical Implementation:
The entire backend is a CLI tool (`src/cli.py`) built with `click` and `rich`.

*   **State Management**: JSON files `monkey_data/dna.json` committed to the repo.
*   **The "Server"**: A GitHub Action cron job (`daily-evolution.yml`) running on `ubuntu-latest`.
*   **The AI**: I'm using the `openai` python client to hit the GitHub Models endpoint:
    ```python
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=os.environ["GITHUB_TOKEN"],
    )
    ```
    This allows `gpt-4o` to act as the "Dungeon Master", deciding how the pet evolves daily based on its history.

### Why Python?
It was super easy to handle the SVG generation (`cairosvg`) and the logic for the genetic inheritance (using `pydantic` for the DNA schema).

Code is here if you want to roast my implementation:
[https://github.com/roeiba/forkMonkey/tree/main/src](https://github.com/roeiba/forkMonkey/tree/main/src)
