from google.adk.agents import SequentialAgent

from app.ai.agents.story import story_agent
from app.ai.agents.visual import visual_agent


story_visual_pipeline = SequentialAgent(
    name="story_visual_pipeline",
    sub_agents=[
        story_agent,
        visual_agent,
    ],
)