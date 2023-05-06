
# Database Design

- Table for investors (who are the investors?)
- Table for admins (who are the admins?)
- Table for stock data e.g. a record of each stock, and its price
- Table for investor holdings



## Stock Table
- stockId (PK)
- stockName
- price

# User Table
- userId (PK)
- userType (Investor or Admin)

# Transaction Table
Might not be ncessary 

# Holdings
- userId (FK)
- stockId (FK)
- quantity 



User Table will be prepopulated with 2 Investors and 2 Admins. No ability to add new.