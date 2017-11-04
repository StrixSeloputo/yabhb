import requests
import datetime

from consts import bot_token
from cmd_parser import BotRegex


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


bot = BotHandler(bot_token)
bot_regex = BotRegex()
now = datetime.datetime.now()


def main():
    purchases = []
    wallet_currency_from = 0.
    wallet_currency_to = 0.
    full_outgoing = 0.
    avg_purchase_rate = 0.

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
                pur_bot_tax = bot_regex.get_bot_tax(last_chat_text)
                pur_rate = bot_regex.get_rate(last_chat_text)
                pur_full_tax = pur_bot_tax * pur_rate + pur_bank_tax

                purchases.append((pur_sum, pur_full_tax, pur_rate))

                wallet_currency_from += pur_sum
                wallet_currency_to += pur_sum / pur_rate

                full_outgoing += pur_sum + pur_full_tax
                avg_purchase_rate = full_outgoing / pur_rate

            except TypeError as er:
                print('Something goes wrong in parsing ('+er.__str__()+'). Try again')
            except ValueError as er:
                print(er)

            print(purchases)
            bot.send_message(
                last_chat_id,
                'wallet:\n' +
                '* (out currency):\t' + str(wallet_currency_from) + '\n' +
                '* (in currency):\t' + str(wallet_currency_to) + '\n' +
                'all outlay:\t' + str(full_outgoing) + '\n' +
                'average purchase rate:\t' + str(avg_purchase_rate)
            )

            new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
