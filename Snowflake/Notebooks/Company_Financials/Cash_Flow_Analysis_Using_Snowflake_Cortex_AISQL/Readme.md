# Demo of Snowflake Cortex AISQL Functions
## ```AI_FILTER``` & ```AI_AGG```

# The Challenge
- ### Analyzing large volumes of unstructured text, like executives' event transcripts, is a significant challenge. 
- ### Traditional SQL queries can't easily identify and summarize nuanced themes like "cash flow discussions." 
- ### To understand how a company's narrative around cash flow has changed over time, a financial analyst would typically have to:

    - #### Locate the transcripts for each company and year.
    - #### Manually read through each transcript to find relevant comments on cash flow.
    - #### Synthesize the information to identify similarities and differences.
    - #### This process is incredibly time-consuming, prone to human error, and difficult to scale across multiple companies.

# The Solution and Why It's Awesome
This query solves the challenge by leveraging Snowflake's AI SQL functions, specifically ```AI_AGG``` and ```AI_FILTER```, to perform a natural language processing (NLP) task directly within the database.

```AI_FILTER``` for Precision: The ```AI_FILTER``` function, combined with the PROMPT function, acts as a smart filter. It uses a large language model (LLM) to scan each piece of text and identify only the sentences that specifically discuss cash flow. This is a massive improvement over using simple keyword searches (like LIKE '%cash flow%'), which could miss important context or include irrelevant results.

```AI_AGG``` for Synthesis: The ```AI_AGG``` function is the most powerful part of the solution. After ```AI_FILTER``` has isolated the relevant comments for each company, ```AI_AGG``` aggregates this text and sends it to the LLM with a specific prompt. This prompt instructs the model to analyze all the cash flow-related comments for a single company across multiple years and synthesize them into a concise, structured summary, highlighting both similarities and differences. The prompt is also designed to format the output with markdown headings and bullet points, making the final result easy to read and use.

- ### This solution is **awesome** because it brings the power of generative AI directly into the data warehouse. 
- ### It transforms a complex, manual task into a simple, scalable SQL query. 
- ### Instead of spending hours reading transcripts, an analyst can now get a comprehensive, well-structured summary for multiple companies with a single query, **providing actionable insights in seconds**. 
- ### It shows how AI can be a powerful tool for analyzing unstructured data at scale.
