import pymysql
import pandas
from tabulate import tabulate

conn = pymysql.Connect(
    host = 'localhost',
    user = 'root',
    password = '1234',
    db = 'ccschool'
)

c = conn.cursor()

def add_items():
    while True:
        item = input("Enter the item name: ")
        typ = input("Enter the item type: ")
        qty = input("Enter the quantity: ")
        price = input("Enter the price per product: ")
        try:
            c.execute(f"INSERT INTO products values(NULL, '{item}', '{typ}', {qty}, {price});")
            conn.commit()
            loop = input("Do you want to continue??[y/n] ")
            if loop.lower() == 'n':
                break

        except:
            print("Unexpected Error")

def remove_items():
    while True:
        df = pandas.read_sql("SELECT * FROM products;", conn)
        print(tabulate(df, headers=['Item Number', 'Item', 'Type', 'Qty', 'Price Per Item'], showindex=False, tablefmt="fancy_grid"))
        item = int(input("Please enter the item number: "))

        print("""
Options:
    1. Change Quantity
    2. Change Name
    3. Change Price
    4. Change type
    5. Remove Item""")
        opt = input("Enter your choice: ")

        if opt == '1':
            qty = int(input("Please enter the quantity: "))
            c.execute(f"UPDATE products SET qty = {qty} where id = {item};")
            conn.commit()
            print("The changes have been made!!!")

        elif opt == '2':
            name = input("Please enter the name: ")
            c.execute(f"UPDATE products SET item = '{name}' where id = {item};")
            conn.commit()
            print("The changes have been made!!!")

        elif opt == '3':
            price = int(input("Please enter the price: "))
            c.execute(f"UPDATE products SET price = {price} where id = {item};")
            conn.commit()
            print("The changes have been made!!!")

        elif opt == '4':
            typ = input("Please enter the type: ")
            c.execute(f"UPDATE products SET type = '{typ}' where id = {item};")
            conn.commit()
            print("The changes have been made!!!")

        elif opt == '5':
            c.execute(f"DELETE FROM products where id = {item};")
            print("The changes have been made!!!")
        
        else:
            print("Invalid Option")
        
        loop = input("Do you want to continue??[y/n] ")
        if loop.lower() == 'n':
            break

def purchase():
    df = pandas.read_sql("SELECT * FROM products;", conn)
    print(tabulate(df, headers=['Item Number', 'Item', 'Type', 'Qty', 'Price Per Item'], showindex=False, tablefmt="fancy_grid"))
    item = int(input("Please enter the item number: "))
    qty = int(input("Enter the quantity: "))
    cart = pandas.DataFrame(None, columns=['Item', 'Price Per Item','Quantity', 'Tax', 'Total Price'])

    dic = {
        'Item': (df.loc[item - 1]['item']),
        'Price Per Item': df.loc[df['id'] == item]['price'],
        'Quantity': qty,
        'Tax': (int(df.loc[df['id'] == item]['price']) * qty) * 0.08,
        'Total Price': (int(df.loc[df['id'] == item]['price']) * qty) * 1.08
    }
    cart = cart.append(dic, ignore_index=True, sort=False)
    print(tabulate(cart, headers='keys', tablefmt='fancy_grid', showindex=False))
    confirm = input("Confirm Purchase??[y/n] ")
    if confirm.lower() == 'y':
        Item = df.loc[df['id'] == item]['item']
        Tax = (int(df.loc[df['id'] == item]['price']) * qty) * 0.08
        Tp = (int(df.loc[df['id'] == item]['price']) * qty) * 1.08
        c.execute(f"INSERT INTO purchase values(Null, '{Item}', {qty}, {Tax}, {Tp})")
        conn.commit()
        c.execute(f"UPDATE products SET qty = qty - {qty} where id = {item};")
        conn.commit()
    else:
        print("Good Bye!!!")

def main():
    print("""
1. Add item
2. Remove/Modify item
3. Purchase
4. Exit""")    
    opt = input("Enter your choice: ")
    if opt == '1':
        add_items()
    elif opt == '2':
        remove_items()
    elif opt == '3':
        purchase()
    else:
        pass
main()