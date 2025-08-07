import json
import pickle
from faker import Faker
from dataclasses import dataclass, asdict
from datetime import date
import time

@dataclass
class Transactions():
    id: str
    sender: str
    receiver: str
    date: date
    amount: float

    def to_json(self, include_null=False) -> dict:
        raw = asdict(self)

        if isinstance(raw.get("date"), date):
            raw["date"] = raw["date"].isoformat()

        return raw

faker = Faker()
Faker.seed(12345)

transactions: list[Transactions] = []

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

print(f"Tiempo de ejecucion con JSON: {(end_json - init_json)*1000:.4f} ms")
print(f"Tiempo de ejecucion con Pickle: {(end_pickle - init_pickle)*1000:.4f} ms")