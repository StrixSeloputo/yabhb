import requests
import datetime

from consts import bot_token
from cmd_parser import BotRegex
from wallet import Wallet


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update

    usr_wallets = {}

    def get_wallet(self, chat_id):
        wallet = self.usr_wallets.get(chat_id)
        if wallet is None:
            wallet = Wallet(chat_id)
        return wallet


bot = BotHandler(bot_token)
bot_regex = BotRegex()
now = datetime.datetime.now()


def main():
    new_offset = None
    while True:
        bot.get_updates(new_offset)
        last_update = bot.get_last_update()
        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        # last_chat_name = last_update['message']['chat']['first_name']

        if bot_regex.is_starts_from_purchase_cmd(last_chat_text):
            try:
                pur_sum = bot_regex.get_sum(last_chat_text)
                pur_bank_tax = bot_regex.get_bank_tax(last_chat_text)
                pur_serv_tax = bot_regex.get_service_tax(last_chat_text)
                pur_rate = bot_regex.get_rate(last_chat_text)

                wallet = bot.get_wallet(last_chat_id)
                wallet.purchase(pur_sum, pur_bank_tax, pur_serv_tax, pur_rate)

                bot.send_message(
                    last_chat_id,
                    wallet.__str__()
                )
            except TypeError as er:
                print('Something goes wrong in parsing ('+er.__str__()+'). Try again')
            except ValueError as er:
                print(er)

        if bot_regex.is_starts_from_selling_cmd(last_chat_text):
            try:
                sell_sum = bot_regex.get_sum(last_chat_text)
                # pur_bank_tax = bot_regex.get_bank_tax(last_chat_text)
                sell_serv_tax = bot_regex.get_service_tax(last_chat_text)
                sell_rate = bot_regex.get_rate(last_chat_text)

                wallet = bot.get_wallet(last_chat_id)
                wallet.selling(sell_sum, sell_serv_tax, sell_rate)

                bot.send_message(
                    last_chat_id,
                    wallet.__str__()
                )
            except TypeError as er:
                print('Something goes wrong in parsing ('+er.__str__()+'). Try again')
            except ValueError as er:
                print(er)

        new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
