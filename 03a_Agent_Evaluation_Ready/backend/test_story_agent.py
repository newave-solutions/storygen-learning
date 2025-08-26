
import pytest
import asyncio
from google.genai.types import Content, Part
from google.adk.runners import InMemoryRunner
from story_agent.agent import root_agent as story_agent

@pytest.mark.asyncio
async def test_story_agent_generates_four_scenes():
    """Tests that the story agent generates a story with four scenes."""
    runner = InMemoryRunner(app_name="test_app", agent=story_agent)
    session = await runner.session_service.create_session(app_name="test_app", user_id="test_user")
    keywords = "brave robot and fluffy puppy"
    content = Content(role="user", parts=[Part(text=f"Keywords: {keywords}")])

    response = ""
    async for event in runner.run_async(user_id="test_user", session_id=session.id, new_message=content):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    response += part.text

    assert isinstance(response, str)
    # A simple way to check for four scenes is to check for the bookends.
    assert "[SCENE 1]" in response
    assert "[SCENE 4]" in response
