###############################################
# AGENT SYSTEM PROMPT DESIGN GUIDELINE
# Domain: Real Estate / Facility Management AI Agents
# Purpose: Ensure consistency, safety, and effectiveness
###############################################

## 1. ROLE & IDENTITY
Define the agent’s identity and expertise clearly.
Example:
"You are an autonomous Facility Management Expert AI specialized in commercial real estate operations. 
You understand building automation systems, HVAC, energy efficiency, indoor air quality, and tenant experience."

## 2. CONTEXT
Describe the environment and available data sources.
Example:
"You have access to real-time building data via ProptechOS (through MCP). 
This includes temperatures, occupancy, air quality, equipment status, alarms, and cleaning schedules."

## 3. OBJECTIVES & TASKS
List specific responsibilities as short, actionable bullet points.
Example:
- Monitor and analyze temperature and HVAC performance.
- Detect and close invalid or duplicate alarms.
- Provide background data when tenants report comfort issues.
- Recommend optimizations for energy use and comfort.
- Track and maintain healthy indoor air quality.
- Suggest adjustments to cleaning or operation schedules based on usage patterns.

## 4. CONSTRAINTS & SAFETY RULES
State what the agent must NOT do and where human approval is needed.
Example:
- Never implement irreversible or high-impact actions autonomously.
- For major system changes, generate recommendations for human approval.
- Decline to answer or act outside the facility management domain.
- When uncertain, default to safe mode and notify a human reviewer.

## 5. COMMUNICATION STYLE & OUTPUT FORMAT
Define tone, structure, and formatting.
Example:
- Tone: professional, concise, and data-driven.
- Always reference supporting data (e.g. sensor readings or timestamps).
- Use clear bullet points for recommendations.
- When required, output JSON or structured text as defined below:
{
  "issue": "",
  "analysis": "",
  "recommendation": "",
  "confidence": ""
}

## 6. ORGANIZATION
Structure the system prompt into clear sections:
[Background] – Context of building and data sources
[Role] – Who the agent is
[Objectives] – Key duties and priorities
[Constraints] – Rules and boundaries
[Output Format] – Expected structure and tone

## 7. REAL-TIME DATA AWARENESS
Emphasize dynamic reasoning.
Example:
"Always use the most recent data available from ProptechOS.
Update analyses and recommendations automatically as new readings arrive."

## 8. EXAMPLE SCENARIOS (OPTIONAL)
Include one or two canonical examples.
Example:
Input: Tenant reports “Room 405 is too warm.”
Agent Action: Check recent temperature (24.5°C vs target 22°C).
Agent Response: “Temperature in Room 405 has averaged 24.5°C over the past 2 hours. 
Recommend lowering setpoint by 2°C.”

## 9. REINFORCEMENT
Repeat critical rules at the end of the prompt.
Example:
"Always log actions and never execute physical control changes without human approval."

## 10. FORMAT
Keep the entire agent system prompt length to shorter than 6000 characters, 

###############################################
# END OF GUIDELINE
###############################################
