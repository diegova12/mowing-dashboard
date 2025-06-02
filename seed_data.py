# seed_data.py

import random
import string
from datetime import date, timedelta

from backend.models import Base, Client, Crew, Job
from backend.crud import engine, SessionLocal

print("Dropping & recreating database schema…")
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

crew_names = ["North Division", "South Division", "East Division", "West Division", "Central Team"]
crews = [Crew(name=name) for name in crew_names]
db.add_all(crews)
db.commit()
print(f"Created {len(crews)} crews")

def random_name():
    first = ''.join(random.choices(string.ascii_lowercase, k=random.randint(4,8))).capitalize()
    last  = ''.join(random.choices(string.ascii_lowercase, k=random.randint(4,8))).capitalize()
    return first, last

def random_email(first, last):
    return f"{first.lower()}.{last.lower()}@example.com"

def random_phone():
    return f"555-{random.randint(100,999)}-{random.randint(1000,9999)}"

def random_address():
    num = random.randint(100,9999)
    street = ''.join(random.choices(string.ascii_letters, k=random.randint(5,10))).capitalize()
    suffix = random.choice(["St", "Ave", "Blvd", "Ln", "Rd"])
    return f"{num} {street} {suffix}"

clients = []
for _ in range(25):
    fn, ln = random_name()
    clients.append(Client(
        name    = f"{fn} {ln}",
        email   = random_email(fn, ln),
        phone   = random_phone(),
        address = random_address(),
    ))

db.add_all(clients)
db.commit()
print(f"Created {len(clients)} clients")

service_types = ["mowing", "mulching", "design", "pruning"]
start_date = date(2025, 5, 18)
end_date   = date(2025, 6, 7)
span_days  = (end_date - start_date).days

jobs = []
for _ in range(30):
    client = random.choice(clients)
    crew   = random.choice(crews)
    sched  = start_date + timedelta(days=random.randint(0, span_days))
    jobs.append(Job(
        client_id = client.id,
        crew_id   = crew.id,
        service   = random.choice(service_types),
        scheduled = sched,
        price     = round(random.uniform(75, 350), 2),
        latitude  = 42.28  + random.uniform(-0.02, 0.02),
        longitude = -83.74 + random.uniform(-0.02, 0.02),
    ))

db.add_all(jobs)
db.commit()
print(f"Created {len(jobs)} jobs")

db.close()
print("Seeding complete!")
