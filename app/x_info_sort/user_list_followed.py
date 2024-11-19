import requests
import os
import json

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
# bearer_token = os.environ.get("AAAAAAAAAAAAAAAAAAAAADfHwgEAAAAAuS8zMCCJDB6XJNB%2FeEQiwaCHH70%3DiLW5EbNJDDJd4BII5HiOqNZj0W9gaIojBffpgxTMwaHLvIQXzV")
bearer_token = os.environ.get("AAAAAAAAAAAAAAAAAAAAADfHwgEAAAAAikUc4ZYxlCROWIgHTIrVc%2BAbydI%3DCL4tZcz0UPDVLJrXugJJgoJR58vgmocrQDZmTr1nFrXpy0EPZ3")


def create_url():
    # List fields are adjustable, options include:
    # created_at, description, owner_id,
    # private, follower_count, member_count,
    list_fields = "list.fields=created_at,follower_count"
    # You can replace the user-id with any valid User ID you wish to find what Lists they are following.
    id = "1686980065974722560"
    url = "https://api.twitter.com/2/users/{}/followed_lists".format(id)
    return url, list_fields


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2userListMembershipsPython"
    return r


def connect_to_endpoint(url, list_fields):
    response = requests.request("GET", url, auth=bearer_oauth, params=list_fields)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    url, list_fields = create_url()
    json_response = connect_to_endpoint(url, list_fields)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()