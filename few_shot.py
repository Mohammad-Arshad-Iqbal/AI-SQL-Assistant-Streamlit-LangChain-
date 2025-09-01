few_shot=[
    {
     "Question":"How many t-shirts do we have left for nike in extra small size and white color?",
     "SQLQuery":"SELECT stock_quantity FROM t_shirts WHERE [brand] = 'Nike' AND [size] = 'XS' AND [color] = 'White'",
     "SQLResult":"[(25,)]",
     "Answer":"There are 25 Nike XS white t-shirts left in stock."
    },
    {
     "Question":"How much is the price of the inventory for all small size tshirts?",
     "SQLQuery":"SELECT SUM([price] * [stock_quantity]) AS [total_inventory_price] FROM t_shirts WHERE [size] = 'S'",
     "SQLResult":"[(22092,)]",
     "Answer":"The total inventory price for all small size t-shirts is 22,092."
    },
    {
     "Question":"If we have to sell all the levi's T-shirts today with discounts applied.How much revenue our store will generate(post discount)",
     "SQLQuery":"""
        SELECT 
            SUM(
                [t].price * 
                (1 - ISNULL([d].discount_percentage, 0) / 100.0) * 
                [t].stock_quantity
            ) AS [TotalRevenuePostDiscount]
        FROM t_shirts AS [t]
        LEFT JOIN discounts AS [d]
            ON [t].t_shirt_id = [d].t_shirt_id
        WHERE [t].brand = 'Levi';
     """,
     "SQLResult":"[(24945.8614000,)]",
     "Answer":"The total revenue after discount from Levi's t-shirts would be 24,945.86."
    },
    {
     "Question":"How many white color levi Tshirt we have?",
     "SQLQuery":"SELECT SUM(stock_quantity) FROM t_shirts WHERE [color] = 'White' AND [brand] = 'Levi';",
     "SQLResult":"[(262,)]",
     "Answer":"There are 262 white Levi's t-shirts in stock."
    }
]
