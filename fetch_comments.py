import json
import os

import googleapiclient.discovery

VIDEO_ID = "zK4TWXWEKAQ"
DEVELOPER_KEY = json.load(open("secrets.json"))["DEVELOPER_KEY"]


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    out = []  # TODO: Remove out and instead use a file append
    page_token = None

    while True:

        # show how many comments we got so far as a progress indicator
        print(len(out))

        # grab a batch of comments
        if not page_token:
            request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=VIDEO_ID,
                maxResults=100,
            )
        else:
            request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=VIDEO_ID,
                maxResults=100,
                pageToken=page_token
            )

        response = request.execute()

        # throw all the new comments into out
        out.extend(response['items'])

        # if we hit the last page then stop looping
        if "nextPageToken" not in response:
            break

        # otherwise load in the next page token
        page_token = response["nextPageToken"]

    # dump all the comments as json
    with open("out.json", "w") as f:
        f.write(json.dumps(out, indent=4))


if __name__ == "__main__":
    main()
