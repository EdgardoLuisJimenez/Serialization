import json
import pickle
from faker import Faker
from dataclasses import dataclass, asdict
from datetime import date
import time
import transactions_pb2 as PBTransactions

# Declaring the structure of the Transactions
@dataclass
class Transactions():
    id: str
    sender: str
    receiver: str
    date: date
    amount: float

    def to_json(self) -> dict:
        raw = asdict(self)

        if isinstance(raw.get("date"), date):
            raw["date"] = raw["date"].isoformat()

        return raw

    def to_protob(self) -> PBTransactions.Transactions:
        msg = PBTransactions.Transactions()
        msg.id = self.id
        msg.sender = self.sender
        msg.receiver = self.receiver
        msg.date.year = self.date.year
        msg.date.month = self.date.month
        msg.date.day = self.date.day
        msg.amount = self.amount

        return msg

faker = Faker()
Faker.seed(12345)

transactions: list[Transactions] = []
ProtobufList = PBTransactions.TransactionsList()

for _ in range(100000):
    transactions.append(Transactions(id=faker.uuid4(), 
                     sender=faker.name(), 
                     receiver=faker.name(), 
                     date=faker.date_object(), 
                     amount=faker.pyfloat(min_value=10.0, max_value=100000.0, right_digits=2)))

init_json = time.perf_counter()
json_data = json.dumps([t.to_json() for t in transactions], indent=2)
end_json = time.perf_counter()


init_pickle = time.perf_counter()
pickle_data = pickle.dumps([t.to_json() for t in transactions])
end_pickle = time.perf_counter()

init_proto = time.perf_counter()
ProtobufList.transactions.extend(t.to_protob() for t in transactions)
end_proto = time.perf_counter() 

print(f"Tiempo de ejecucion con JSON: {(end_json - init_json)*1000:.4f} ms")
print(f"Tiempo de ejecucion con Pickle: {(end_pickle - init_pickle)*1000:.4f} ms")
print(f"Tiempo de ejecucion con Proto: {(end_proto - init_proto)*1000:.4f} ms")