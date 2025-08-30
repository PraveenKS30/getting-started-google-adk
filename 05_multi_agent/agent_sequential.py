from google.adk.agents import LlmAgent, SequentialAgent

# define capital agent
capital_agent = LlmAgent(
    name = "capital_agent",
    model="gemini-2.0-flash",
    instruction= "You are an agent that provides the capital city of a country.",
    output_key= "capital_city"
)

# population agent 
population_agent = LlmAgent(
    name = "population_agent",
    model="gemini-2.0-flash",
    instruction= "You are an agent that provides the approx. population of a given {capital_city}."
)

# define sequential agent that uses capital and population agents
root_agent = SequentialAgent(
    name = "pipeline_agent",
    sub_agents=[capital_agent, population_agent], 
)