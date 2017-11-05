
class Wallet:
    id = None
    # сумма, вложенная в кошелек, в исходной валюте
    src_currency = 0.
    # сумма в кошельке в целевой валюте
    dst_currency = 0.
    # полная сумма расходов (если больше нуля) или прибыли (если меньше нуля)
    full_outgoing = 0.
    # средний курс окупаемости вложенных средств
    avg_purchase_rate = 0.

    def __init__(self, chat_id):
        self.id = chat_id

    def __eq__(self, other):
        return self.id == other.id

    def __cmp__(self, other):
        return self.id.__cmp__(other.id)

    def __str__(self):
        result = 'invested:\t' + str(self.src_currency) + '\n'
        result += 'in wallet:\t' + str(self.dst_currency) + '\n'
        if self.full_outgoing < 0:
            result += 'all outlay:\t' + str(self.full_outgoing) + '\n'
        else:
            result += 'all profit:\t' + str(abs(self.full_outgoing))+'\n'
        result += 'average purchase rate:\t' + str(self.avg_purchase_rate)
        return result

    def purchase(self, purchase_sum, bank_tax, service_tax, purchase_rate):
        # вложенная сумма
        self.src_currency += purchase_sum
        # сумма в кошельке
        self.dst_currency += purchase_sum / purchase_rate
        self.dst_currency -= service_tax
        # полные затраты
        self.full_outgoing += purchase_sum + bank_tax
        self.avg_purchase_rate = self.full_outgoing / self.dst_currency

    def selling(self, selling_sum, service_tax, selling_rate):
        # поскольку получили некую сумму, то вложенная сумма и полные затраты уменьшаются на эту величину
        self.full_outgoing -= selling_sum
        self.src_currency -= selling_sum
        # вычисляем величину, на которую уменьшился кошелек
        self.dst_currency -= selling_sum / selling_rate
        self.dst_currency -= service_tax
        # вычисляем заново курс окупаемости оставшегося вложения
        self.avg_purchase_rate = self.full_outgoing / self.dst_currency
