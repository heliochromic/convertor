import random

products = [
    {
        "link":"https://gotoshop.ua/img/p/2023/09/242777/7672050-242777-napijj-na-osnovi-romu-bacardi-oakheart-original-35-1l-336.jpg?t=t1695245622",
        "before":969,
        "after":539,
        "name":"Ром Bacardi Spiced, 1л Bacardi"
    },
    {
        "link": "https://gotoshop.ua/img/p/2023/09/242462/7662935-242462-napijj-alkogolnijj-martini-royale-bianco-aromatizovanijj-8-075l-336.jpg?t=t1695371268",
        "before": 349,
        "after": 289,
        "name": "Напій алкогольний Martini Royale Bianco ароматизований 8% 0,75л Martini "
    },
    {
        "link": "https://content.silpo.ua/sku/ecommerce/57/480x480wwm/579462_480x480wwm_6f042f5f-a902-8986-5d6f-1f64802ec616.png",
        "before": 45,
        "after": 36,
        "name": "Сидр Apps солодкий газований з/б"
    }
]

def get_random_product():
    return random.choice(products)