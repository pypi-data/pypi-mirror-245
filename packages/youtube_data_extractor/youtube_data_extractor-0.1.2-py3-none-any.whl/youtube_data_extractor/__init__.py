# read version from installed package
from importlib.metadata import version
__version__ = version("youtube_data_extractor")

# Import the functions
from .youtube_data_extractor import extract_translatable_languages_and_count, extract_quality_and_audio, extract_links