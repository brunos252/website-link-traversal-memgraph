class ShortestPathNotFoundError(Exception):
    """exception raised when no path is present in database"""
    def __init__(self, message="Shortest path not found!"):
        self.message = message
        super().__init__(self.message)


class WebsiteNotFoundError(Exception):
    """exception raised when network URL does not exist or path URL is not present in database"""
    def __init__(self, website=""):
        self.message = "Website not found: " + website
        super().__init__(self.message)
