import coverpy
import requests.exceptions


cover_py = coverpy.CoverPy()


def get_cover_art_url(title, artist, album):
    """Get 512x512 cover art from the iTunes API"""
    try:
        result = cover_py.get_cover(f'{title} {artist} {album}', 1)
        return result.artwork(512)
    except (coverpy.exceptions.NoResultsException, requests.exceptions.HTTPError):
        return
