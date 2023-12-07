import base64
import json
import string
from random import choice
from time import time


def create_x_context_properties(location_guild_id: str, location_channel_id: str) -> str:
    data = json.dumps({
        "location": "Accept Invite Page",
        "location_guild_id": location_guild_id,
        "location_channel_id": location_channel_id,
        "location_channel_type": 0
    }).encode('utf-8')
    return base64.b64encode(data).decode('utf-8')


def create_x_super_properties(user_agent: str) -> str:
    data = json.dumps({
        "os": "Windows",
        "browser": "Chrome",
        "device": "",
        "system_locale": "en-US",
        "browser_user_agent": user_agent,
        "browser_version": "110.0.0.0",
        "os_version": "10",
        "referrer": "https://discord.com/",
        "referring_domain": "discord.com",
        "referrer_current": "",
        "referring_domain_current": "",
        "release_channel": "stable",
        "client_build_number": 242566,
        # "client_build_number": 247232,
        "client_event_source": None
    }).encode('utf-8')
    return base64.b64encode(data).decode('utf-8')


class NewClient():

    def _set_response_cookies(self, response):
        cookies = response.headers.get_list("set-cookie")
        for cookie in cookies:
            key, value = cookie.split(';')[0].strip().split("=")
            self.session.cookies.set(name=key, value=value, domain="discord.com", path="/")

    async def _init_cloudflare(self):
        url = f"{self.BASE_URL}/login"
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
        }
        response, data = await self._request("GET", url, headers=headers)
        self._set_response_cookies(response)

    async def _request_s_key(self) -> tuple[str, str]:
        url = f"{self.BASE_URL}/cdn-cgi/challenge-platform/scripts/invisible.js"
        response, data = await self._request("GET", url)

        key = 'x3MU-7nK0tLQlyRoIXNDZOiPF+c26s$gdJAVzEv9qmapSuh5bwfjHYTk18eWBG4rC'
        for x in response.text.split(';'):
            if len(x) == 65 and '=' not in x:
                key = x

        x = re.findall(CLOUDFLARE_PATTERN, response.text)
        s = '0.' + ':'.join(x[0])
        return s, key

    async def _bypass_cloudflare(self):
        if self._cloudflare_is_bypassed:
            return

        # collect cloudflare cookies needed to bypass protection
        await self._init_cloudflare()
        # initialize cf_clearance bypasser and generate cf_clearance
        s, key = await self._request_s_key()
        wp = user_agent_to_wp(self.session.user_agent)
        wp = encrypt_wp(to_json(wp), key)
        payload = {'wp': wp, 's': s}
        url = f"{self.BASE_URL}/cdn-cgi/challenge-platform/h/b/jsd/r/{generate_cloudflare_code()}"
        await self._request("POST", url, json=payload)
        self._cloudflare_is_bypassed = True

    async def request(
            self,
            method,
            url,
            params: dict = None,
            headers: dict = None,
            json: Any = None,
            data: Any = None,
            **kwargs,
    ) -> tuple[requests.Response, dict[str, Any] or str]:
        await self._bypass_cloudflare()
        return await self._request(method, url, params, headers, json, data, **kwargs)

    def start_websockets(self):
        self.discum_client = discum.Client(
            token=self.account.auth_token,
            log={"console": False, "file": False},
        )
        self.discum_client.gateway.run(False)

    def end_websockets(self):
        self.discum_client.gateway.close()

    # async def _get_guild_ids(self, invite_code: str) -> tuple[str, str]:
    #     url = f"{self.BASE_API_URL}/invites/{invite_code}"
    #     response, data = await self.request("GET", url)
    #     # Может вылезти "You need to verify your account"
    #
    #     location_guild_id = data['guild_id']
    #     location_channel_id = data['channel']['id']
    #     return location_guild_id, location_channel_id

    async def agree_with_rules(
            self,
            invite_code: str,
            location_guild_id: int,
            location_channel_id: int,
    ):
        url = f"{self.BASE_API_URL}/guilds/{location_guild_id}/member-verification"
        params = {
            "with_guild": False,
            "invite_code": invite_code,
        }

        response, data = await self.request("GET", url, params=params)
        if "Unknown Guild" in response.text:
            print(f"This guild does not require agreement with the rules.")
            return

        url = f"{self.BASE_API_URL}/guilds/{location_guild_id}/requests/@me"
        headers = {
            "referrer": f'https://discord.com/channels/{location_guild_id}/{location_channel_id}'
        }
        form_fields = data['form_fields'][0]
        payload = {
            'version': data['version'],
            'form_fields': [
                {
                    'field_type': form_fields['field_type'],
                    'label': form_fields['label'],
                    'description': form_fields['description'],
                    'automations': form_fields['automations'],
                    'required': True,
                    'values': form_fields['values'],
                    'response': True,
                },
            ],
        }
        await self.request("PUT", url, headers=headers, json=payload)

    async def join_guild(
            self,
            invite_code: str,
            captcha_response: str = None,
            captcha_rqtoken: str = None,
    ):
        url = f"{self.BASE_API_URL}/invites/{invite_code}"
        headers = None
        if captcha_response and captcha_rqtoken:
            headers = {
                "x-captcha-key": captcha_response,
                "x-captcha-rqtoken": captcha_rqtoken,
            }
        response, data = await self.request("GET", url, headers=headers)
        # TODO Может вылезти "You need to verify your account"

        location_guild_id = data['guild_id']
        location_channel_id = data['channel']['id']
        x_content_properties = create_x_context_properties(location_guild_id, location_channel_id)
        headers = {"x_content_properties": x_content_properties}
        payload = {"session_id": None}
        await self.request("POST", url, headers=headers, json=payload)
        await self.agree_with_rules(invite_code, location_guild_id, location_channel_id)


    async def _change_user_data(
            self,
            payload: dict,
            captcha_response: str = None,
            captcha_rqtoken: str = None,
    ) -> dict:
        url = f"{self.BASE_API_URL}/users/@me"
        headers = None
        if captcha_response and captcha_rqtoken:
            headers = {
                "x-captcha-key": captcha_response,
                "x-captcha-rqtoken": captcha_rqtoken,
            }
        response, data = await self.request("PATCH", url, headers=headers, json=payload)
        return data

    async def change_username(
            self,
            username: str,
            captcha_response: str = None,
            captcha_rqtoken: str = None,
    ) -> dict:
        if not self.account.password:
            raise ValueError(f"Specify the current password before changing username.")

        payload = {
            "username": username,
            "password": self.account.password,
        }
        data = await self._change_user_data(payload, captcha_response, captcha_rqtoken)
        self.account.username = username
        return data

    async def change_name(
            self,
            name: str,
            captcha_response: str = None,
            captcha_rqtoken: str = None,
    ) -> dict:
        payload = {"global_name": name}
        data = await self._change_user_data(payload, captcha_response, captcha_rqtoken)
        self.account.name = name
        return data

    async def change_password(
            self,
            new_password: str,
    ):
        if not self.account.password:
            raise ValueError(f"Specify the current password before changing it.")

        url = f"{self.BASE_API_URL}/users/@me"
        headers = {
            'connection': 'keep-alive',
            'referer': url,
        }
        payload = {
            'password': self.account.password,
            'new_password': new_password,
        }
        response, data = await self.request("PATCH", url, headers=headers, json=payload)
        self.account.auth_token = data["token"]
        self.account.password = new_password
