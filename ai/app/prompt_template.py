from langchain.prompts import PromptTemplate

prompt_template = """

Your task is to generate the Mermaid.js code based on the given inputs. Ensure the Mermaid.js code is correct and adheres to the standards.

    Your job is to write the code to generate a colorful mermaid diagram of {diagram_type}
    describing the below
    {details} information only , dont use any other information.
    only generate the code as output nothing extra and do not use ( brackets ) or no colors
    each line in the code must be terminated by ; 
    Code:
"""

graph_prompt = PromptTemplate(template=prompt_template)