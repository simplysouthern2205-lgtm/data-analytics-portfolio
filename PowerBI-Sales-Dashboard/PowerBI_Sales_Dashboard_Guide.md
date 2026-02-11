# Power BI Sales Dashboard (Build Guide)

## Files
- Dataset: `sales_data_clean.csv`

## Goal
Create an interactive Sales Performance dashboard that tracks:
- Total Sales (Revenue)
- Total Profit
- Profit Margin
- Monthly Trend
- Performance by Region / Category / Product

## Step 1: Load the data
1. Open Power BI Desktop
2. **Get Data** -> **Text/CSV** -> select `sales_data_clean.csv`
3. In Power Query:
   - Confirm `OrderDate` is a Date type
   - Confirm numeric columns are Decimal
4. **Close & Apply**

## Step 2: Create a Date table (recommended)
Model view -> New table:

```DAX
DateTable =
CALENDAR ( MIN ( SalesTable[OrderDate] ), MAX ( SalesTable[OrderDate] ) )
```

Then add:
```DAX
Year = YEAR ( DateTable[Date] )
Month = FORMAT ( DateTable[Date], "MMM YYYY" )
MonthSort = YEAR(DateTable[Date]) * 100 + MONTH(DateTable[Date])
```

Sort `Month` by `MonthSort`.

## Step 3: Create relationships
- Relate `SalesTable[OrderDate]` -> `DateTable[Date]` (Many-to-one)

## Step 4: Create DAX measures
Model view -> New measure:

```DAX
Total Sales = SUM ( SalesTable[Revenue] )
Total Profit = SUM ( SalesTable[Profit] )
Profit Margin = DIVIDE ( [Total Profit], [Total Sales] )
Total Orders = DISTINCTCOUNT ( SalesTable[OrderID] )
Avg Order Value = DIVIDE ( [Total Sales], [Total Orders] )
```

Optional (YoY):
```DAX
Sales YoY % =
VAR PrevYearSales =
    CALCULATE ( [Total Sales], SAMEPERIODLASTYEAR ( DateTable[Date] ) )
RETURN
    DIVIDE ( [Total Sales] - PrevYearSales, PrevYearSales )
```

## Step 5: Build the report page
Suggested visuals:
- Cards: Total Sales, Total Profit, Profit Margin, Avg Order Value
- Line chart: Total Sales by DateTable[Month]
- Bar chart: Total Profit by Region
- Matrix: Category -> Product with Total Sales and Total Profit
- Slicers: DateTable[Year], Region, Category, Channel

## Step 6: Publish a clickable link (optional)
- Publish to Power BI Service -> then use **Share** (or **Publish to web** if allowed)
- Put the link in your resume under the Power BI project
