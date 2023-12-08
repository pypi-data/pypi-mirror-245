from zvolv_sdk.server_configuration import EnvVariables
import os
class AuthenticationBase:

    def __init__(
            self,
            zvolv_access_key_id: str = EnvVariables.get_admin_email(),
            zvolv_secret_access_key: str = EnvVariables.get_admin_password(),
            zvolv_domain_context: str = EnvVariables.get_business_domain(),
            zvolv_business_tag_id: str = "98NCMBD2KBZ4R",
            zvolv_url: str =  "https://zvolv.co/rest/v17/user/login"
            
        ) -> None:
            self.zvolv_access_key_id = zvolv_access_key_id
            self.zvolv_secret_access_key = zvolv_secret_access_key
            self.zvolv_domain_context = zvolv_domain_context
            self.zvolv_business_tag_id = zvolv_business_tag_id
            self.zvolv_url = zvolv_url

    def display(self):
        print(self.zvolv_access_key_id,self.zvolv_secret_access_key,self.zvolv_domain_context,self.zvolv_business_tag_id,self.zvolv_url)





# class EnvVariables(object):
#     if(os.path.exists("../../.env")):
#         load_dotenv()

#     @staticmethod
#     def get_val(key):
#         return os.environ[key] if key in os.environ else None


















    # def _add_client_authentication(self, payload: dict[str, Any]) -> dict[str, Any]:
    #     return add_client_authentication(
    #         payload,
    #         self.domain,
    #         self.client_id,
    #         self.client_secret,
    #         self.client_assertion_signing_key,
    #     )

    # def post(
    #     self,
    #     url: str,
    #     data: RequestData | None = None,
    #     headers: dict[str, str] | None = None,
    # ) -> Any:
    #     return self.client.post(url, data=data, headers=headers)


    # def authenticated_post(
    #     self,
    #     url: str,
    #     data: dict[str, Any],
    #     headers: dict[str, str] | None = None,
    # ) -> Any:
    #     return self.client.post(
    #         url, data=self._add_client_authentication(data), headers=headers
    #     )

    # def get(
    #     self,
    #     url: str,
    #     params: dict[str, Any] | None = None,
    #     headers: dict[str, str] | None = None,
    # ) -> Any:
    #     return self.client.get(url, params, headers)