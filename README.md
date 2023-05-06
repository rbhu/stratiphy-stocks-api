# stratiphy-stocks-api

## Running the project

To run the project, run:
```
docker-compose up
```

Once this is running, to run the tests, run:
```docker exec -it stratiphy-stocks-api-web-1 bash```
to log into the Django container. Then run ```python manage.py test``` to run all tests.


## API Guide

### Login as investor or admin
HTTP Action:
```
POST /stock-api/login
```
Request JSON:
```json
{
  "userName": "username",
  "password": "password"
}
```
Response JSON:

```json
{
  "authToken": "TOKENCODE"
}
```


### Listing (and searching) stocks (investors)
HTTP Action:
```
GET /stock-api/investor/stocks # lists all stocks
```
Response JSON:
```
{
  stocks: [
    {
      name: string
      price: number 
    },
    ...  
  ]
}

```
HTTP Action:
```
GET /stock-api/investor/stocks?search=something # search for all stocks matching search term
```
Response JSON:
```
{
  stocks: [
    {
      name: "name",
      price: 123.40 
    },
    ...  
  ]
}
```
HTTP Action:
```
GET /stock-api/investor/stocks/<specific_stock_name>
```
Response JSON:
```
{
  stock: {
    name: "name",
    price: 123.40 
  }
}
```


### Buy stocks (investors)
```
POST /stock-api/investor/stocks/buy
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
POST /stock-api/investor/stocks/sell
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