
import os
import json
import uuid
from google.adk.tools import BaseTool
from google.cloud import aiplatform
from google.cloud import storage

class ImagenTool(BaseTool):
    """Tool to generate an image from a text prompt using Vertex AI."""

    def __init__(self):
        super().__init__()
        self.name = "generate_image"
        self.description = "Generates an image from a text prompt."

    def run(self, prompt: str) -> str:
        """
        Generates an image using Vertex AI's ImageGenerationModel,
        uploads it to a GCS bucket, and returns the public URL.

        Args:
            prompt: The text prompt to generate the image from.

        Returns:
            A JSON string with the public 'gcs_url' of the generated image.
        """
        try:
            # Initialize Vertex AI
            aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))

            # Initialize the Image Generation Model
            model = aiplatform.ImageGenerationModel.from_pretrained("imagegeneration@005")

            # Generate the image
            response = model.generate_images(prompt=prompt)
            image_data = response.images[0]._image_bytes

            # Upload to GCS
            bucket_name = os.environ.get("GENMEDIA_BUCKET")
            if not bucket_name:
                raise ValueError("GENMEDIA_BUCKET environment variable not set.")

            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob_name = f"generated_image_{uuid.uuid4()}.png"
            blob = bucket.blob(blob_name)
            blob.upload_from_string(image_data, content_type="image/png")

            # Make the image public
            blob.make_public()

            # Return the public URL
            return json.dumps({"gcs_url": blob.public_url})

        except Exception as e:
            return json.dumps({"error": str(e)})
