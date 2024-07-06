# Car Auction Optimization

This repository contains Python code to optimize car auctions by selecting the most cost-effective bundle of cars and calculating Vickrey-Clarke-Groves (VCG) payments. The algorithm deterministically calculates the optimal bundle of cars based on seller prices and uses statistical methods to handle uncertainty and predict auction outcomes.

## Key Functions

### `opt_bnd(data, k, years)`

- Determines the optimal bundle of `k` cars for the given years, minimizing the total cost.
- Returns the total cost and the IDs of the selected cars.

### `proc_vcg(data, k, years)`

- Calculates VCG payments for the selected bundle.
- Ensures fair pricing by charging each winner based on their contribution to the total cost.
- Returns a dictionary of payments for each winning car.

### Statistical Methods

- `cdf(data, x)`: Calculates the cumulative distribution function (CDF) for a given value `x`.
- `os_cdf(r, n, x, data)`: Computes the order statistic CDF for the `r`-th smallest value out of `n` samples.
- `exp_rev(data, k, buyers_num)`: Estimates the expected revenue from future auctions.
- `reserve_price(data, k, buyers_num)`: Suggests a reserve price based on historical data.


