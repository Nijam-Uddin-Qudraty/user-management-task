import os
import django

from django.contrib.auth.hashers import make_password
from faker import Faker
from tqdm import tqdm  # progress bar

# 1️⃣ Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "usermanagement.settings")
django.setup()
from django.contrib.auth.models import User
# 2️⃣ Initialize Faker and progress bar
fake = Faker()
total_users = 100_000
chunk_size = 5000  # adjust if needed

# 3️⃣ Precompute hashed password once
hashed_password = make_password("123")

users = []

print(f"🚀 Starting creation of {total_users} users...")

for i in tqdm(range(1, total_users + 1), desc="Creating users"):
    username = f"user{i}"
    email = f"user{i}@example.com"
    
    users.append(User(
        username=username,
        email=email,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        password=hashed_password,
        is_active=True,
        is_staff=False,
        is_superuser=False
    ))
    
    # Insert in chunks
    if i % chunk_size == 0:
        User.objects.bulk_create(users, batch_size=chunk_size)
        users = []  # reset list

# Insert any remaining users
if users:
    User.objects.bulk_create(users, batch_size=chunk_size)

print("🎉 All users created successfully!")
