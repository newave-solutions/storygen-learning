
from google.adk.agents import LlmAgent
from ..imagen_tool import ImagenTool

tools = [ImagenTool()]

root_agent = LlmAgent(
    model="gemini-1.5-flash",
    name="story_image_agent",
    description="Generates images for a story based on scene descriptions.",
    instruction="""You are an expert image prompt engineer. Your task is to generate a single image for a scene in a children's storybook.

You will be given the scene title, a description of the scene, and descriptions of the main characters.

Your instructions are to:
1.  Read the scene description and character descriptions.
2.  Combine these descriptions into a single, detailed prompt for the `generate_image` tool.
3.  The prompt should be descriptive and include details about the setting, characters, colors, and style to create a visually appealing image for a children's storybook.
4.  Call the `generate_image` tool with the combined prompt.
5.  Output the result from the tool directly.
""",
    tools=tools
)
