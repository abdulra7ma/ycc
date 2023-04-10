def extract_handle(channel_url):
    """
    Extract the handle from a given YouTube channel URL.

    Args:
        channel_url (str): The URL of the YouTube channel.

    Returns:
        str: The handle of the YouTube channel.
    """
    return channel_url.split('@')[1].split('/')[0]