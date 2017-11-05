import re


def was_recognized(searched, group_index):
    return (searched is not None) and \
            (searched.group(group_index) is not None)


class BotRegex:
    purchase_cmd_pat = '(purchase|buying|buy|bought|купить|куплено|покупать|к)'
    selling_cmd_pat = '(sale|selling|sell|sold|продавать|продать|продано|п)'
    double_pat = '(\d+([,\.]\d*)?)'
    sum_cmd_pat = '(sum|s|сумма|с)\s+' + double_pat
    bank_cmd_pat = '(bank|банк)'
    bot_cmd_pat = '(service|сервис)'
    tax_cmd_pat = '(tax|t|charge|комиссия|налог)\s+' + double_pat
    rate_cmd_pat = '(rate|r|курс)\s+' + double_pat

    def is_starts_from_purchase_cmd(self, string):
        matched = re.match(self.purchase_cmd_pat, string)
        return matched is not None

    def is_starts_from_selling_cmd(self, string):
        matched = re.match(self.selling_cmd_pat, string)
        return matched is not None

    def get_sum(self, string):
        searched = re.search(self.sum_cmd_pat, string)

        if not was_recognized(searched, 2):
            raise ValueError('The sum was not recognised')

        return float(searched.group(2))

    def get_bank_tax(self, string):
        pattern = self.bank_cmd_pat + '_' + self.tax_cmd_pat
        searched = re.search(pattern, string)

        if not was_recognized(searched, 3):
            return 0.

        return float(searched.group(3))

    def get_service_tax(self, string):
        pattern = self.bot_cmd_pat + '_' + self.tax_cmd_pat
        searched = re.search(pattern, string)

        if not was_recognized(searched, 3):
            return 0.

        return float(searched.group(3))

    def get_rate(self, string):
        searched = re.search(self.rate_cmd_pat, string)

        if not was_recognized(searched, 2):
            return 1.

        return float(searched.group(2))
