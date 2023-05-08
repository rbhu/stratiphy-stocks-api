# stratiphy-stocks-api

## Running the project

To run the project, run:
```
docker-compose up
```

Once this is running, to run the tests, run:
```docker exec -it stratiphy-stocks-api-web-1 bash```
to log into the Django container. 

Run ```python manage.py test``` to run all tests.

Run ```python manage.py generate-api-tokens``` to get the auth tokens for all the users (our test data has 2 investors and 1 admin).

Run ```python manage.py generate_random_stock_prices &``` to start randomly moving the stock prices (every 5 seconds, will move up or down by small value)

## API Guide

### Listing and searching stocks (admin and investor)
HTTP Action:
```
curl -X GET --location 'http://localhost:8000/stock-api/stocks' \
--header 'Authorization: Token <auth_token>'
```
Response JSON:
```json lines
[
    {
        "stock_id": 1,
        "stock_name": "Apple Inc.",
        "short_code": "AAPL",
        "price": "150.50",
        "quantity": 100
    },
    ...
]
```
HTTP Action:
```
curl -X GET --location 'http://localhost:8000/stock-api/stocks/?search=Apple' \
--header 'Authorization: Token <auth_token>'
```
Response JSON:
```json lines
[
    {
        "stock_id": 1,
        "stock_name": "Apple Inc.",
        "short_code": "AAPL",
        "price": "150.50",
        "quantity": 100
    },
    ...
]
```

### Retrieve specific stock info (admin and investor)
```
curl -X GET --location 'http://localhost:8000/stock-api/stocks/<stock_id>' \
--header 'Authorization: Token <auth_token>'
```
Response Body:
```
{
  stock_id: 1
  stock_name: "name",
  price: 123.45,
  short_code: 'STK'
  quantity: 100
} 
```

### Buy stocks (investors)
```
curl --location 'http://localhost:8000/stock-api/buy/' \
--header 'Authorization: Token <auth_token>' \
--header 'Content-Type: application/json' \
--data '{
    "stockId": 1,
    "quantity": 20
}'
-X POST
```
Response JSON:
```
{
  stockId: string
  quantity: number
  totalCost: number
}
```

### Sell stocks (investors)
```
curl --location 'http://localhost:8000/stock-api/sell/' \
--header 'Authorization: Token <auth_token>' \
--header 'Content-Type: application/json' \
--data '{
    "stockId": 1,
    "quantity": 20
}'
-X POST
```
Response JSON:
```
{
  stockId: string
  quantity: number
  totalProfit: number
}
```
### View Holdings (investors)
```
curl --location 'http://localhost:8000/stock-api/holdings/' \
--header 'Authorization: Token <auth_token>'
```
Response JSON:
```
{
  holdings: [
    {
      stockId: string
      quantity: number
      currentStockPrice: number
      totalHoldingValue: number
    }
  ]
}
```
### Create new stock (admin)
```
curl --location 'http://localhost:8000/stock-api/stocks/' \
--header 'Authorization: Token <auth_token>' \
--header 'Content-Type: application/json' \
--data '{"stock_name": "New Stock", "short_code": "STK", "price": 10.99, "quantity": 100}'
```
Response Body:
```
{
  stock_id: 1
  stock_name: "name",
  price: 123.45,
  short_code: 'STK'
  quantity: 100
} 
```

### Edit stock info (admin)
```
curl --location --request PUT 'http://localhost:8000/stock-api/stocks/1/' \
--header 'Authorization: Token <auth_token>' \
--header 'Content-Type: application/json' \
--data '{"stock_name": "Updated Stock", "short_code": "UPD", "price": 19.99, "quantity": 50}'
```
Response Body:
```
{
  stock_id: 1
  stock_name: "name",
  price: 123.45,
  short_code: 'STK'
  quantity: 100
} 
```

### Partially edit stock info (admin)
```
curl --location --request PATCH 'http://localhost:8000/stock-api/stocks/1/' \
--header 'Authorization: Token <auth_token>' \
--header 'Content-Type: application/json' \
--data '{"stock_name": "Partial Update Stock", "short_code": "UPD" }'
```
Response Body:
```
{
  stock_id: 1
  stock_name: "name",
  price: 123.45,
  short_code: 'STK'
  quantity: 100
} 
```

### Delete stock (admin)
```
curl --location --request DELETE 'http://localhost:8000/stock-api/stocks/1/' \
--header 'Authorization: Token <auth_token>'
```
