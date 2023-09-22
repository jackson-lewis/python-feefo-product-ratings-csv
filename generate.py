import requests
import csv

total_product_count = 0
fetched_all = False
page = 1
PAGE_SIZE = 100

def get_feefo_product_ratings(page = 1):
    params = dict(
        merchant_identifier='motta-living',
        review_count='true',
        page_size=PAGE_SIZE,
        page=page,
        since_period='all'
    )

    res = requests.get('https://api.feefo.com/api/11/products/ratings', params)
    data = res.json()

    return data['products']


with open('feefo-product-ratings.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow([
        'SKU',
        'Rating',
        'Review count'
    ])

    while fetched_all is not True:
        products = get_feefo_product_ratings(page)
        count = len(products)

        for product in products:
            writer.writerow([
                product['sku'],
                product['rating'],
                product['review_count']
            ])

        if count == PAGE_SIZE:
            page += 1

        total_product_count += count
        fetched_all = count < PAGE_SIZE

    print('Success: CSV file generated with ' + str(total_product_count) + ' products.')