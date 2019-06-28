import random, csv

def get_receipt(total):
    UPC = ['UPC']
    Price = ['Price']
    for i in range(total):
        #Fake UPC and Price
        UPC.append(int(random.random()*pow(10,9)))
        Price.append(round(random.random()*random.randint(1, 100),2))
    return UPC, Price
def get_records(total, mcc_list, date_list):
    Date = ['Date']
    Amount = ['Amount']
    Category = ['Category']
    for i in range(total):
        Amount.append(round(random.random()*random.randint(1, 100),2))
        date_index = random.randint(0, len(date_list)-1)
        mcc_index = random.randint(0, len(mcc_list)-1)
 
        Date.append(date_list[date_index])
        Category.append(mcc_list[mcc_index])
    return Date, Category, Amount
 
def save_csv(col_list, path):
    if len(col_list) == 3:
        rows = zip(col_list[0], col_list[1], col_list[2])
    elif len(col_list) == 4:
        rows = zip(col_list[0], col_list[1], col_list[2], col_list[3])
    #rows = zip(Items, UPC, Price)
    with open(path, "w") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)
 
if __name__ == "__main__":
    #put your favorate items in this list, note the first element is for the
    #header of csv file.
    Items = ["Items", "Banana","Apple", "TV", "Pens", "Booklet",
    "Coffee", "Outlet", "Camera", "Candy"]
 
    #put your favorate merchants in this list, note the first element is for the
    #header of csv file.
    Merchants = ["Merchants", "Walmart", "Target", "Amazon", "Costco", "H.E.B", "Whole Foods", 
    "AMC", "DollarTree", "Xbox store", "Starbucks", "Steam"]
 
    date_list = ['20190501', '20190404','20190606','20190403', '20190409']
    mcc_list = ['Eating Places, Restaurants',
                'Fast Food Restaurants',
                'Shoe Stores',
                'Electronics Stores',
                'Book Stores',
                'Grocery Stores, Supermarkets',
                'Department Stores',
                'Airlines, Air Carriers']
                
    print("INSERT INTO items(recieptID, itemName, UPC, price) VALUES ")

    for i in range(2,12):
        UPC, Price = get_receipt(len(Items))
        Date, Category, Amount = get_records(len(Merchants), \
                                            mcc_list, date_list)
        # Save receipts and loop it to get more
        save_csv([Items, UPC, Price], "/home/wescules/Downloads/template-flask-app-68d5cff10edae1c4e56e26a391528115f4afe298/fakeReceipts.csv")
        # Save the merchant records
        save_csv([Date, Merchants,Amount, Category], "/home/wescules/Downloads/template-flask-app-68d5cff10edae1c4e56e26a391528115f4afe298/fakeRecords.csv")



        # with open('fakeRecords.csv') as csv_file:
        #     csv_reader = csv.reader(csv_file, delimiter=',')
        #     line_count = 0
        #     for row in csv_reader:
        #         if line_count == 0:
        #             line_count += 1
        #         else:
        #             print("('"+row[0]+"'," + "'"+row[1]+"'," + ""+row[2]+"," + "'"+row[3]+"'),")
        #             line_count += 1

        with open('fakeReceipts.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    print("(" + str(i) +", '"+row[0]+"'," + "'"+row[1]+"'," + ""+row[2]+"" +"),")
                    line_count += 1




