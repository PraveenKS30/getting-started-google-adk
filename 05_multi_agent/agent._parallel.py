from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.adk.tools import google_search

# define capital agent
natural_resource_agent = LlmAgent(
    name = "NaturalResourcesAgent",
    model="gemini-2.0-flash",
    instruction= """You are a research agent.
    Give me the list of countries based on the given input who are rich in natural resources.
    Summarize the information in 2 lines.
    Use the given Google Search tool to achieve the same.
    """,
    tools=[google_search],
    output_key= "natural_resources_countries",
)

# population agent 
gdp_percapita_agent = LlmAgent(
    name = "GDPPerCapitaResearchAgent",
    model="gemini-2.0-flash",
    instruction= """You are a research agent.
    Give me the list of countries based on the given input who are having the highest GDP per capita. 
    Use the given Google Search tool to achieve the same.
    """,
    tools = [google_search],
    output_key = "gdp_growth_countries",
)

# define sequential agent that uses capital and population agents
parallel_agent = ParallelAgent(
    name = "pipeline_agent",
    description= "Run multiple parallel agents in parallel to gather information about countries.",
    sub_agents=[natural_resource_agent, gdp_percapita_agent], 
)

# aggregate the results
merger_agent = LlmAgent(
    name = "MergerAgent",
    model="gemini-2.0-flash",
    instruction=""" You are an AI agent which would help in combining research results from multiple
    resources into structured format.

    **Input Summaries :**
    - Natural Resources Countries: {natural_resources_countries}
    - GDP Growth Countries: {gdp_growth_countries}

    **Output Format:**

    ## Summary of Countries Rich in Natural Resources and GDP Growth
    - Synthesize the information from the input summaries and provide a concise overview of the countries rich in natural resources and their GDP growth. Include key insights and comparisons where relevant.
    """,
    tools = [google_search]
)

# define sequential agent that uses parallel agent and merger agent
sequential_pipeline_agent = SequentialAgent(
    name = "ResearchAndSynthesisAgent",
    # Run parallel research first, then merge the results
    description = "Run parallel research agents and merge the results into a structured format.",
    sub_agents = [parallel_agent, merger_agent]
)

root_agent = sequential_pipeline_agent