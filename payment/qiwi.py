from pyqiwip2p import AioQiwiP2P

class QIWI():
    def __init__(self, auth_key):
        self.auth_key = auth_key
        self.p2p = AioQiwiP2P(auth_key=self.auth_key)

    async def main(self, amount):
        new_bill = await self.p2p.bill(amount=amount, lifetime=5)
        return [new_bill.pay_url,new_bill.bill_id]

    async def check_status(self, bill_id):
        status_result = await self.p2p.check(bill_id=bill_id)
        return status_result.status

