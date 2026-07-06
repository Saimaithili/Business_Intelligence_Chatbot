import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

regions = {
    "North": ["Delhi", "Jaipur", "Chandigarh"],
    "South": ["Hyderabad", "Bengaluru", "Chennai"],
    "East": ["Kolkata", "Bhubaneswar", "Patna"],
    "West": ["Mumbai", "Pune", "Ahmedabad"]
}

categories = {
    "Electronics": [
        "Laptop", "Mobile", "Headphones", "Monitor", "Smart Watch"
    ],
    "Furniture": [
        "Chair", "Table", "Sofa", "Cupboard", "Bed"
    ],
    "Clothing": [
        "T-Shirt", "Jeans", "Jacket", "Shirt", "Shoes"
    ],
    "Home Appliances": [
        "Mixer", "Refrigerator", "Washing Machine", "Microwave", "Fan"
    ],
    "Grocery": [
        "Rice", "Oil", "Sugar", "Tea", "Milk"
    ]
}

payment_modes = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash"
]

sales_people = [
    "Rahul",
    "Priya",
    "Arjun",
    "Sneha",
    "Vikram",
    "Anjali",
    "Kiran",
    "Ravi"
]

customers = [
    "Amit",
    "Suresh",
    "Ramesh",
    "Lakshmi",
    "Divya",
    "Karthik",
    "Pooja",
    "Nikhil",
    "Anu",
    "Sai"
]

rows = []

start_date = datetime(2024, 1, 1)

for i in range(1, 1001):

    region = random.choice(list(regions.keys()))
    city = random.choice(regions[region])

    category = random.choice(list(categories.keys()))
    product = random.choice(categories[category])

    sales = random.randint(1000, 100000)

    profit = int(sales * random.uniform(0.08, 0.30))

    quantity = random.randint(1, 10)

    date = start_date + timedelta(days=random.randint(0, 365))

    rows.append({

        "Order_ID": f"ORD{i:04d}",

        "Date": date.strftime("%Y-%m-%d"),

        "Region": region,

        "City": city,

        "Category": category,

        "Product": product,

        "Sales": sales,

        "Profit": profit,

        "Quantity": quantity,

        "Customer": random.choice(customers),

        "Payment_Mode": random.choice(payment_modes),

        "Sales_Person": random.choice(sales_people),

        "Rating": random.randint(1,5)

    })

df = pd.DataFrame(rows)

df.to_csv("data/sales_data.csv", index=False)

print("✅ 1000 Records Generated Successfully")