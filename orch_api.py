import requests

CONTENT_TYPE_JSON = "application/json"


class OrchApi:
    """Class to interact with the Orchestrator API."""

    def __init__(
        self,
        client_id: str,
        refresh_token: str,
        base_url: str,
        tokenurl="https://account.uipath.com/oauth/token",
    ):
        """
        Initialize the API client.

        Parameters:
        client_id (str): The client ID for the API.
        refresh_token (str): The refresh token for the API.
        base_url (str): The base URL for the API.
        token_url (str): The URL to get the token from. Defaults to "https://account.uipath.com/oauth/token".
        """

        token_url = tokenurl
        self.base_url = base_url

        body = {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "refresh_token": refresh_token,
        }

        headers = {"Authorization": "Bearer", "Content-Type": CONTENT_TYPE_JSON}

        response = requests.post(token_url, json=body, headers=headers)

        access = response.json()
        if response.status_code == 200:
            self.access_token = access["access_token"]
        else:
            raise ValueError(
                f"Failed to retrieve access token. Status code: {str(response.status_code)}. Response: {response.text}"
            )

    def get_all_assets(self):
        """
        Retrieve all assets.

        Returns:
        dict, Response: The JSON response from the API and the full response object.
        """
        uri = (
            self.base_url
            + "/odata/Assets/UiPath.Server.Configuration.OData.GetAssetsAcrossFolders"
        )
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json;odata.metadata=minimal;odata.streaming=True",
            "accept": CONTENT_TYPE_JSON,
        }
        response = requests.get(uri, headers=headers)
        if response.status_code == 200:
            return response.json(), response
        else:
            raise ValueError(
                f"Failed to retrieve assets. Status code: {str(response.status_code)}. Response: {response.text}"
            )

    def get_assets_by_key(self, key: int, id: int):
        """
        Retrieve assets by key.

        Parameters:
        key (int): The key of the asset to retrieve.
        id (int): The ID of the organization unit.

        Returns:
        dict, Response: The JSON response from the API and the full response object.
        """
        uri = self.base_url + f"/odata/Assets({key})"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-UIPATH-OrganizationUnitId": f"{id}",
            "accept": CONTENT_TYPE_JSON,
        }
        response = requests.get(uri, headers=headers)
        if response.status_code == 200:
            return response.json(), response
        else:
            raise ValueError(
                f"Failed to retrieve assets. Status code: {str(response.status_code)}. Response: {response.text}"
            )

    def delete_asset(self, key: int, id: int):
        uri = self.base_url + f"/odata/Assets({key})"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-UIPATH-OrganizationUnitId": f"{id}",
            "accept": CONTENT_TYPE_JSON,
        }
        response = requests.delete(uri, headers=headers)
        if response.status_code == 204:
            print("Asset has been deleted.")
        else:
            raise ValueError(
                f"Failed to delete asset. Status code: {str(response.status_code)}. Response: {response.text}"
            )

    def create_asset(
        self,
        id: int,
        name: str,
        value,
        value_type: str,
        value_scope: str = "Global",
        description: str = "using api",
        username=None,
        password=None,
    ):
        if value_type not in ["Integer", "Boolean", "String", "Credential"]:
            raise ValueError(
                "Invalid value_type. Expected 'Integer', 'Boolean', 'String', or 'Credential'."
            )

        uri = self.base_url + "/odata/Assets"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-UIPATH-OrganizationUnitId": f"{id}",
            "accept": CONTENT_TYPE_JSON,
        }

        body = {
            "Name": name,
            "CanBeDeleted": True,
            "ValueScope": value_scope,
            "ValueType": value_type,
            "Value": str(value),
            "StringValue": "",
            "BoolValue": False,
            "IntValue": 0,
            "CredentialUsername": "",
            "CredentialPassword": "",
            "ExternalName": "",
            "CredentialStoreId": 0,
            "KeyValueList": [],
            "HasDefaultValue": False,
            "Description": description,
            "RobotValues": [],
            "UserValues": [],
            "Tags": [],
        }

        if value_type == "Integer":
            body["IntValue"] = value
        elif value_type == "Boolean":
            body["BoolValue"] = value
            body["Value"] = str(value).lower()
        elif value_type == "String":
            body["StringValue"] = value
        elif value_type == "Credential":
            body["CredentialUsername"] = username
            body["CredentialPassword"] = password

        response = requests.post(uri, headers=headers, json=body)
        if response.status_code == 201:
            return response.json(), response
        else:
            raise ValueError(
                f"Failed to create asset. Status code: {str(response.status_code)}. Response: {response.text}"
            )

    def add_queue_item(self, id:int, queue_name:str, specific_content:dict,priority:str = "Normal",**kwargs):
        
        uri = self.base_url + "/odata/Queues/UiPathODataSvc.AddQueueItem"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-UIPATH-OrganizationUnitId": f"{id}",
            "accept": CONTENT_TYPE_JSON,
        }
        
        body = {
            "itemData": {
            "Name": queue_name,
            "Priority":priority ,
            "SpecificContent": specific_content,
            },
            }
        
        body.update(kwargs)

        response = requests.post(uri, headers=headers, json=body)
        if response.status_code == 201:
            return response.json(), response
        else:
            raise ValueError(
                f"Failed to create queue item. Status code: {str(response.status_code)}. Response: {response.text}"
            )
        
    def create_queue(self, id:int, name:str, description:str = "created using api",**kwargs):
        
        uri = self.base_url + "/odata/QueueDefinitions"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-UIPATH-OrganizationUnitId": f"{id}",
            "accept": CONTENT_TYPE_JSON,
        }
        
        body =    {
        "Name": name,
        "Description": description,
    }


        body.update(kwargs)

        response = requests.post(uri, headers=headers, json=body)
        if response.status_code == 201:
            return response.json(), response
        else:
            raise ValueError(
                f"Failed to create queue. Status code: {str(response.status_code)}. Response: {response.text}"
            )
       