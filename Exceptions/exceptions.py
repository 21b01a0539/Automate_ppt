class PDFProcessingError(Exception):
    """Exception raised for errors during PDF processing."""
    def __init__(self, message="An error occurred while processing the PDF"):
        self.message = message
        super().__init__(self.message)

class ImageExtractionError(Exception):
    """Exception raised for errors during image extraction."""
    def __init__(self, message="An error occurred while extracting images"):
        self.message = message
        super().__init__(self.message)

class OpenAIError(Exception):
    """Exception raised for errors related to OpenAI API."""
    def __init__(self, message="An error occurred with the OpenAI API"):
        self.message = message
        super().__init__(self.message)

class SlideGenerationError(Exception):
    """Exception raised for errors during slide generation."""
    def __init__(self, message="An error occurred while generating slides"):
        self.message = message
        super().__init__(self.message)