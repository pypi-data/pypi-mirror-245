import requests
import json
import logging

logger = logging.getLogger("azure")
logger.setLevel(logging.WARN)


def build_user_object(user_details: dict, extension_id: str, b2c_prefix: str) -> dict:
  
  if user_details['role'] == '8amAdmin':
    user_details['password'] = 'eightamAdmin!23'
  else:
    user_details['password'] = 'eightam!23'

  return {      
    "accountEnabled": True,
    "displayName": f"{user_details['firstName']} {user_details['lastName']}",
    "mailNickname": user_details['firstName'],
    "identities": [
      {
        "issuer": f"{b2c_prefix}.onmicrosoft.com",
        "issuerAssignedId": user_details['email'],
        "signInType": "emailAddress"
      }
    ],
    "passwordProfile" : {
      "forceChangePasswordNextSignIn": False,
      "password": user_details['password']
    },
    "mobilePhone": user_details['phone'],
    f"extension_{extension_id}_OrganizationID": user_details['company_id'],
    f"extension_{extension_id}_SignUpCode": user_details['sign_up_code'],
    f"extension_{extension_id}_UserRoles": user_details['role'],
    f"extension_{extension_id}_mustResetPassword": user_details['reset_password']  
  }


class B2CHelper:
  def __init__(self, token_request_data) -> None:
    self.token_request_data = {
      'grant_type': token_request_data['grant_type'],
      'client_id': token_request_data['user_mgmt_client_id'],
      'scope': token_request_data['scope'],
      'client_secret': token_request_data['user_mgmt_client_secret'],
      'b2c_tenant_id': token_request_data['tenant_id'],
      'extension_id': token_request_data['ext_app_client_id']
    }


  def get_token(self):
    return requests.post(
      f"https://login.microsoftonline.com/{self.token_request_data['b2c_tenant_id']}/oauth2/v2.0/token",
        data=self.token_request_data).json()['access_token'] 


  def get_auth_header(self):
    return {
      'Authorization': f'Bearer {self.get_token()}',
      'Content-type': 'application/json',
    }
  

  def create_item(self, auth_header: dict, item: dict):     
    return requests.post(
      "https://graph.microsoft.com/beta/users", 
      headers=auth_header,
      data=json.dumps(item)
    )

  
  def update_item(self, auth_header: dict, item: dict, id: str):
    del item['passwordProfile']    
    return requests.patch(
      f"https://graph.microsoft.com/beta/users/{id}",
      headers=auth_header,
      data=json.dumps(item)
    )
      
  
  def delete_item(self, auth_header: dict, user_id: dict):
    return requests.delete(f"https://graph.microsoft.com/beta/users/{user_id}",
      headers=auth_header
    )


  def get_user(self, user_id: str) -> dict:
    user = requests.get(f"https://graph.microsoft.com/beta/users/{user_id}", headers=self.get_auth_header()).json() 
    del user["@odata.context"]
    return user


  def get_users(self, company_id: str=None, role_type=None) -> list:
    if company_id is not None:
      users = requests.get(
        f"https://graph.microsoft.com/beta/users?$filter=extension_{self.token_request_data['extension_id']}_OrganizationID eq '{company_id}'",
        headers=self.get_auth_header()
      ).json()['value']
    if role_type is not None:
      users = requests.get(
        f"https://graph.microsoft.com/beta/users?$filter=extension_{self.token_request_data['extension_id']}_UserRoles eq '{role_type}'",
        headers=self.get_auth_header()
      ).json()['value']
    else:
      users = requests.get("https://graph.microsoft.com/beta/users", headers=self.get_auth_header())
      users = [x  for x in users.json()['value'] if x['mailNickname'] != 'Daveg_8amsolutions.com#EXT#']

    return users


  def create_user(self, user_details: dict, b2c_prefix: str) -> dict:
    user = build_user_object(user_details, self.token_request_data['extension_id'], b2c_prefix)
    return self.create_item(self.get_auth_header(), user)


  def create_users(self, user_details_list: list, b2c_prefix: str) -> list:   
    auth_header = self.get_auth_header() 
    for user_detail in user_details_list:
      user = build_user_object(user_detail, self.token_request_data['extension_id'], b2c_prefix)
      self.create_item(auth_header, user)


  def update_user(self, user_details: dict, b2c_prefix: str):
    user = build_user_object(user_details, self.token_request_data['extension_id'], b2c_prefix)  
    return self.update_item(self.get_auth_header(), user, user_details['id'])  


  def update_users(self, user_details_list: list, b2c_prefix: str):    
    auth_header = self.get_auth_header()
    for user_detail in user_details_list:
      user = build_user_object(user_detail, self.token_request_data['extension_id'], b2c_prefix)
      self.update_item(auth_header, user_detail['id'])


  def delete_user(self, user_id: str):
    return self.delete_item(self.get_auth_header(), user_id)


  def delete_users(self, user_id_list):
    ## Add code to delete by companyId  
    auth_header = self.get_auth_header()  
    for user_id in user_id_list:
      self.delete_item(auth_header, user_id)

  