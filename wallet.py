
class Wallet:
    id = None
    src_currency = 0.
    dst_currency = 0.
    full_outgoing = 0.
    avg_purchase_rate = 0.

    def __init__(self, chat_id):
        self.id = chat_id

    def __eq__(self, other):
        return self.id == other.id

    def __cmp__(self, other):
        return self.id.__cmp__(other.id)

    def __str__(self):
        result = 'wallet:\n'
        result += '* (src currency):\t' + str(self.src_currency) + '\n'
        result += '* (dst currency):\t' + str(self.dst_currency) + '\n'
        result += 'all outlay:\t' + str(self.full_outgoing) + '\n'
        result += 'average purchase rate:\t' + str(self.avg_purchase_rate)
        return result

    def purchase(self, purchase_sum, bank_tax, service_tax, purchase_rate):
        self.src_currency += purchase_sum
        self.dst_currency += purchase_sum / purchase_rate
        full_tax = service_tax * purchase_rate + bank_tax
        self.full_outgoing += purchase_sum + full_tax
        self.avg_purchase_rate = self.full_outgoing / purchase_rate
