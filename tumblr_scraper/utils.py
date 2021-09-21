def extract_filename(uri: str) -> str:
    pieces = uri.rsplit("/", 1)
    filename = pieces[-1]
    return filename
