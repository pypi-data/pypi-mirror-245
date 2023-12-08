import requests
import yaml

def read_config_file(file_id):
    app_id = 'cli_a5eeb3ad3837100b'
    app_secret = 'ftLZbDJOzDxSx0xiigALNev1tgHTvR4V'

    # Obtain an access token
    auth_url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal/"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    # Authenticate and get your access token from Feishu
    response = requests.post(auth_url, headers=headers, json=payload)
    auth_token = response.json().get("app_access_token")

    # The endpoint for downloading files from Feishu might look like this

    download_endpoint = f'https://open.feishu.cn/open-apis/drive/v1/files/{file_id}/download'

    # Make the request to download the file
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    response = requests.get(download_endpoint, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Assuming the response content is the binary content of the YAML file
        file_content = response.content

        # Load the YAML content
        content = yaml.safe_load(file_content)
        try:
            yaml_file_path = './cfg.yaml'
            with open(yaml_file_path, 'r') as file:
                yaml_content = yaml.safe_load(file)
            yaml_content = content
        except:
            yaml_file_path = 'cfg.yaml'
            yaml_content = content
        with open(yaml_file_path, 'w') as file:
            yaml.safe_dump(yaml_content, file)

    else:
        return 'Failed to download the file:'+response.text