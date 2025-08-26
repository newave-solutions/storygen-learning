
import pytest
import json
import os
from unittest.mock import MagicMock, patch
from story_agent.imagen_tool import ImagenTool
from google.adk.tools import ToolContext

# Mock classes for external dependencies
class MockImage:
    def save(self, location):
        with open(location, "w") as f:
            f.write("mock_image_data")

class MockImageGenerationModel:
    def generate_images(self, **kwargs):
        response = MagicMock()
        response.images = [MockImage()]
        return response

class MockBlob:
    def __init__(self, name):
        self.name = name
        self.public_url = f"https://storage.googleapis.com/test-bucket/{name}"

    def upload_from_file(self, file, content_type):
        pass

    def make_public(self):
        pass

class MockBucket:
    def blob(self, blob_name):
        return MockBlob(blob_name)

class MockStorageClient:
    def bucket(self, bucket_name):
        return MockBucket()

@pytest.fixture
def mock_environment(monkeypatch):
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "test-project")
    monkeypatch.setenv("GENMEDIA_BUCKET", "test-bucket")
    monkeypatch.setattr("vertexai.preview.vision_models.ImageGenerationModel", MockImageGenerationModel)
    monkeypatch.setattr("google.cloud.storage.Client", MockStorageClient)

@pytest.mark.asyncio
async def test_imagen_tool_run(mock_environment):
    """Tests the ImagenTool's run method with mocked external calls."""
    tool = ImagenTool(project_id="test-project")
    ctx = ToolContext(session=MagicMock())
    prompt = "a test prompt"

    result_json = await tool.run(ctx, prompt=prompt)
    result = json.loads(result_json)

    assert result["success"] is True
    assert len(result["images"]) == 1
    assert result["images"][0]["stored_in_bucket"] is True
    assert "gcs_url" in result["images"][0]
    assert result["images"][0]["gcs_url"].startswith("https://storage.googleapis.com/test-bucket/")
