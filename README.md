# YouTube Comment Scraper

This is a Python script that uses the YouTube API to extract comments from a YouTube video and save them to a CSV file. The script also retrieves the likes and dislikes of the video, as well as the likes and replies for each comment.

## Prerequisites
To run this script, you will need:

Python 3.x
A Google Cloud project with the YouTube API enabled
A YouTube Data API key or a JSON credentials file
The google-auth and google-api-python-client Python modules

##Installation
1. Clone this repository to your local machine.
   
2. Install the required Python modules by running the following command in your
```
pip install -r requirements.txt
```

1. Obtain a YouTube Data API key by following the instructions here. Make sure to enable the YouTube Data API for your project.

2. (Optional) If you prefer to use a JSON credentials file instead of an API key, follow the instructions here to create a service account and download the credentials file.

3. Open the config.py file and replace the placeholders with your API key or credentials file path and the ID of the YouTube video you want to extract comments from.


6. Run the script by executing the following command in your terminal:
```
python main.py
```

## Usage
The script will extract the comments, likes, dislikes, likes and replies for each comment from the specified YouTube video and save them to a CSV file named comments.csv. The output file will be created in the same directory as the script.

## Contributing
If you find any issues or have suggestions for improvement, feel free to submit a pull request or open an issue.
