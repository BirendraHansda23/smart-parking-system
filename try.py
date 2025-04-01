from google.cloud import vision
import io
import os

def detect_text(image_path):
    """Detects text in an image using Google Cloud Vision API."""
    try:
        # Initialize client
        client = vision.ImageAnnotatorClient()

        # Read image
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
        
        image = vision.Image(content=content)

        # Call Vision API
        response = client.text_detection(image=image)
        texts = response.text_annotations

        if texts:
            print("Detected Text:\n", texts[0].description)
            return texts[0].description
        else:
            print("No text found")
            return None

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return None
    except Exception as e:
        print(f"Error calling Vision API: {e}")
        return None

# Test
if __name__ == "__main__":
    image_path = "../Images/WhatsApp Image 2025-01-17 at 01.40.24_9c46b3a9.jpg"
    
    # Check if file exists first
    if not os.path.exists(image_path):
        print(f"Error: Image file does not exist at {image_path}")
    else:
        detect_text(image_path)