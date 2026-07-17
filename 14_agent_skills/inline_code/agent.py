from google.adk import Agent
from google.adk.skills import models
from google.adk.tools import skill_toolset

# define the weather skill
weather_skill = models.Skill(
    frontmatter = models.Frontmatter(
        name = "weather-skill",
        description = "A skill that provides weather information.",
    ),
    instructions = (
        "1. Read `references/weather_info.md` for the current weather.\n"
        "2. If humidity is requested, use `scripts/get_humidity.py` "
        "with the location argument.\n"
        "3. Provide a concise update to the user."
    ),
    resources = models.Resources(
        references = {
            "weather_info.md": (
                "# Weather reference\n"
                "London: cloudy, 18°C\n"
                "Mumbai: rainy, 29°C\n"
            ),
        },
        scripts = {
            "get_humidity.py": models.Script(
                src=(
                    "import sys\n"
                    "location = sys.argv[1]\n"
                    "print(f'Humidity for {location}: 72%')\n"
                )
            ),
        }

    )
)

# define skill toolset
weather_toolset = skill_toolset.SkillToolset(
    skills= [weather_skill]
)

# define root agent
root_agent = Agent(
    model="gemini-2.5-flash",
    name="skill_user_agent",
    description="An agent that can use specialized skills.",
    tools=[
        weather_toolset,
    ],
)
