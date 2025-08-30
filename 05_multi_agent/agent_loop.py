from google.adk.agents import LlmAgent, SequentialAgent, LoopAgent

# define capital agent
basic_agent = LlmAgent(
    name = "BasicArchagent",
    model="gemini-2.0-flash",
    instruction= "You are an agent specialized in the software architecture." \
    "You need to propose basic system design for the given scenario",
    output_key= "basic_arch_output"
)


critique_design_agent = LlmAgent(
    name = "critique_agent",
    model="gemini-2.0-flash",
    instruction= """ You are an agent specialized in critiquing software architecture designs.
    You need to critique the provided design and suggest improvements for scalability, maintainability, and performance.

    **Input**:
    {basic_arch_output}

    """, 
    output_key= "critique_output"

)

refine_design_agent = LlmAgent(
    name = "refine_agent",  
    model="gemini-2.0-flash",
    instruction= """ You are an agent specialized in refining the given architecture design.
    IF the design is good, you should return the design as is with the phrase "The design is good."
    Else, you need to refine the provided design based on the critique and suggest improvements for scalability, maintainability, and performance.
    
    **Input**:
    {basic_arch_output}
    {critique_output}

    """,

)

# define sequential agent that uses capital and population agents
loop_agent = LoopAgent(
    name = "loop_agent",
    sub_agents=[critique_design_agent, refine_design_agent],
    max_iterations = 3
)


root_agent = SequentialAgent(
    name = "sequential_agent",
    sub_agents=[basic_agent, loop_agent],
)
