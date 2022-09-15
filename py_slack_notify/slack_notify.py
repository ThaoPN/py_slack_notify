import requests
import logging
from enum import Enum


class RequestMethod(Enum):
    post = "post"
    get = "get"


class Action(Enum):
    add = "add"
    remove = "remove"


class SlackNotify:
    def __init__(
        self,
        bot_oauth_token,
        user_oauth_token,
        post_message_url="https://slack.com/api/chat.postMessage",
        search_message_url="https://slack.com/api/search.messages",
        reaction_url="https://slack.com/api/reactions.add",
        reaction_remove_url="https://slack.com/api/reactions.remove",
        update_message_url="https://slack.com/api/chat.update",
    ):

        self._bot_oauth_token = bot_oauth_token
        self._oauth_token = user_oauth_token
        self._post_message_url = post_message_url
        self._search_message_url = search_message_url
        self._reaction_url = reaction_url
        self._reaction_remove_url = reaction_remove_url
        self._update_url = update_message_url
        self._headers = {
            "Authorization": "Bearer " + self._bot_oauth_token,
            "Content-type": "application/json;charset=UTF-8",
        }
        logging.debug(self._headers)

    def post_message(
        self,
        channel_id,
        message=None,
        thread_ts=None,
        blocks=None,
        emoji=None,
        reply_broadcast=False,
    ):

        payload = {
            "channel": channel_id,
        }

        if blocks is not None:
            payload["blocks"] = blocks
        else:
            payload["text"] = message

        if thread_ts:
            payload["thread_ts"] = thread_ts
            if reply_broadcast:
                payload["reply_broadcast"] = True

        resp = self._request(
            RequestMethod.post,
            end_point=self._post_message_url,
            json_payload=payload,
        )

        resp_json = resp.json()
        if resp_json.get("ok") and emoji:
            ts = resp_json.get("message", {}).get("ts")
            channel = resp_json.get("channel")
            if ts:
                self.reaction(channel, emoji, ts)

        return resp_json

    def find_messages(self, channel_id, text):
        payload = {"channel": channel_id}
        params = {
            "query": '"' + text + '"',
            "sort": "timestamp",
            "sort_dir": "desc",
        }

        return self._request(
            RequestMethod.get,
            end_point=self._search_message_url,
            params=params,
            json_payload=payload,
        ).json()

    def reaction(self, channel_id, emoji, ts):
        return self._reaction(
            action=Action.add,
            channel_id=channel_id,
            emoji=emoji,
            ts=ts,
        ).json()

    def remove_reaction(self, channel_id, emoji, ts):
        return self._reaction(
            action=Action.remove,
            channel_id=channel_id,
            emoji=emoji,
            ts=ts,
        ).json()

    def edit_message(self, channel_id, message, ts, emoji):
        payload = {"channel": channel_id, "ts": ts, "text": message}

        resp = self._request(
            RequestMethod.post,
            end_point=self._update_url,
            json_payload=payload,
        )

        if emoji:
            self.reaction(channel_id, emoji, ts)

        return resp.json()

    def _reaction(self, action: Action, channel_id: str, emoji: str, ts: str):
        payload = {"channel": channel_id, "timestamp": ts, "name": emoji}
        urls = {
            Action.add.value: self._reaction_url,
            Action.remove.value: self._reaction_remove_url,
        }
        resp = self._request(
            RequestMethod.post,
            end_point=urls[action.value],
            json_payload=payload,
        )
        logging.debug(resp.text)

        resp_json = resp.json()
        if not resp_json.get("ok"):
            logging.error(resp_json)

        return resp

    def _request(
        self,
        method: RequestMethod,
        end_point: str,
        json_payload: dict,
        params=None,
        headers: dict = None,
    ):
        kwargs = {
            "method": method.value,
            "url": end_point,
            "headers": headers if headers else self._headers,
        }
        if params:
            kwargs["params"] = params
        if json_payload:
            kwargs["json"] = json_payload

        resp = requests.request(**kwargs)
        logging.debug(resp.request.url)
        logging.debug(resp.text)
        resp_json = resp.json()
        if not resp_json.get("ok"):
            logging.error(resp_json)

        return resp


# post_message(CHANNEL_ID, "Test a message", None, 'call_me_hand')
# reaction(CHANNEL_ID, 'tada', '1605086375.000900')
# find_messages(CHANNEL_ID, "Test a message")
# post_message(CHANNEL_ID, "Reply to message", '1605086946.001900', 'tada')
# edit_message(CHANNEL_ID, "Reply to message. This message has been edited", '1605089273.002500', 'call_me_hand')
# remove_reaction(CHANNEL_ID, 'call_me_hand', '1605089273.002500')
