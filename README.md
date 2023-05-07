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

## API Guide

### Listing and searching stocks (investors)
HTTP Action:
```
GET /stock-api/investor/stocks # lists all stocks
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
GET /stock-api/investor/stocks/?search=something # search for all stocks matching search term on short_name or short_code
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


### Buy stocks (investors)
```
POST /stock-api/investor/buy/
```
Request JSON:
```
{
  stockId: string
  quantity: number
}
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
POST /stock-api/investor/sell
```
Request JSON:
```
{
  stockId: string
  quantity: number
}
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
GET /stock-api/investor/holdings
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
### Create new stocks (admin)
```
POST /stock-api/admin/stocks/create
```
Request Body:
```
{
  name: "name",
  initialPrice: 123.40
} 
```

Response Body:
```
{
  name: "name",
  price: 123.40
} 
```

### View stock info (admin)
```
GET /stock-api/admin/stocks/<stock_name>
```

### Edit stock info (admin)
```
PUT /stock-api/admin/stocks/<stock_id>/edit
```
Request body
```
{
  name: "name",
  price: 123.40
} 
```
Response Body:
```
{
  name: "name",
  price: 123.40
} 
```