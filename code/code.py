import json
import pickle
from faker import Faker
from dataclasses import dataclass, asdict
from datetime import date
import time
import transactions_pb2 as PBTransactions
import pandas as pd

faker = Faker()
Faker.seed(12345)

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

transactions: list[Transactions] = []
ProtobufList = PBTransactions.TransactionsList()

for _ in range(100000):
    transactions.append(Transactions(id=faker.uuid4(), 
                     sender=faker.name(), 
                     receiver=faker.name(), 
                     date=faker.date_object(), 
                     amount=faker.pyfloat(min_value=10.0, max_value=100000.0, right_digits=2)))

########### Serialization Time
init_json_serialization = time.perf_counter()
json_data = json.dumps([t.to_json() for t in transactions], indent=2)
end_json_serialization = time.perf_counter()

init_pickle_serialization = time.perf_counter()
pickle_data = pickle.dumps([t.to_json() for t in transactions])
end_pickle_serialization = time.perf_counter()

init_proto_serialization = time.perf_counter()
ProtobufList.transactions.extend(t.to_protob() for t in transactions)
protobuf_serialization = ProtobufList.SerializeToString()
end_proto_serialization = time.perf_counter() 


time_json_serialization = (end_json_serialization - init_json_serialization)*1000
time_pickle_serialization = (end_pickle_serialization - init_pickle_serialization)*1000
time_protobuff_serialization = (end_proto_serialization - init_proto_serialization)*1000

jsonbytes = len(json_data.encode("utf-8"))
picklebytes = len(pickle_data)
protobufbytes = len(protobuf_serialization)

# print(f"Tiempo de Serializacion con JSON: {time_json_serialization:.4f} ms")
# print(f"Tiempo de Serializacion con Pickle: {time_pickle_serialization:.4f} ms")
# print(f"Tiempo de Serializacion con Proto: {time_protobuff_serialization:.4f} ms")

# print(f"Tamaño de archivo Serializado con JSON: {jsonbytes} bytes")
# print(f"Tamaño de archivo Serializado con Pickle: {picklebytes} bytes")
# print(f"Tamaño de archivo Serializado con Protobuf: {protobufbytes} bytes")


########### DeSerialization Time
init_json_deserialization = time.perf_counter()
json_data_deserialization = json.loads(json_data)
end_json_deserialization = time.perf_counter()

init_pickle_deserialization = time.perf_counter()
pickle_data = pickle.loads(pickle_data)
end_pickle_deserialization = time.perf_counter()

init_protobuf_deserialization = time.perf_counter()
new_transactions = PBTransactions.TransactionsList()
new_transactions.ParseFromString(protobuf_serialization)
end_protobuf_deserialization = time.perf_counter()

time_json_deserialization = (end_json_deserialization - init_json_deserialization)*1000
time_pickle_deserialization = (end_pickle_deserialization - init_pickle_deserialization)*1000
time_protobuff_deserialization = (end_protobuf_deserialization - init_protobuf_deserialization)*1000

# print(f"\nTiempo de DeSerializacion con JSON: {time_json_deserialization:.4f} ms")
# print(f"\nTiempo de DeSerializacion con Pickle: {time_pickle_deserialization:.4f} ms")
# print(f"\nTiempo de DeSerializacion con Protobuff: {time_protobuff_deserialization:.4f} ms")

df = pd.DataFrame({
    "Tiempo de Serializacion": [time_json_serialization, time_pickle_serialization, time_protobuff_serialization],
    "Tiempo de Desrializacion": [time_json_deserialization, time_pickle_deserialization, time_protobuff_deserialization],
    "Tamaño de archivo Serializado": [jsonbytes, picklebytes, protobufbytes]
})

print(df)