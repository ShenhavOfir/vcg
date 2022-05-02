import itertools
import numpy as np
import pandas as pd
import math
from itertools import permutations



########## Part A ###############


def opt_bnd(data, k, years):
    # returns the optimal bundle of cars for that k and list of years and their total cost.
    temp = data.copy()
    brands = list(temp["brand"].unique())
    final_indexes = []
    final_cost = 0
    for _ in range(k):

        min_s_star = float("inf")
        index_of_min = []
        for per in permutations(years):
            set_index = []
            sum_of_min = 0
            for brand, year in zip(brands, per):
                df = temp[(temp['brand'] == brand) &
                          (temp['year'] == year)]
                min_value = df.iloc[df["value"].argmin()]
                set_index.append(min_value['id'])
                sum_of_min += min_value['value']

            if sum_of_min < min_s_star:
                min_s_star = sum_of_min
                index_of_min = set_index

        final_indexes.extend(index_of_min)
        final_cost += min_s_star

        to_remove = temp.loc[(temp['id'].isin(index_of_min))]
        temp = temp.drop(to_remove.index)



    return {"cost": final_cost, "bundle": final_indexes}


def proc_vcg(data, k, years):
    car_for_sale = opt_bnd(data, k, years)
    dic_of_pay = {}


    for index, row in data.iterrows():
        if row['id'] in car_for_sale["bundle"]:
            sum_if_car_sale = car_for_sale['cost'] - row['value']
            data_without_car = data.loc[(data.id != row['id'])]
            new_cars = opt_bnd(data_without_car, k, years)
            sum_without_winning_car = new_cars['cost']
            dic_of_pay[row['id']] = sum_without_winning_car - sum_if_car_sale
    return dic_of_pay


########## Part B ###############
def extract_data(brand, year, size, data):
    # extract the specific data for that type
    relevant_data = data.loc[(data['brand'] == brand) & (data['year'] == year)
                             & (data['engine_size'] == size)]['value']

    return sorted(relevant_data.values.tolist())


class Type:
    cars_num = 0
    buyers_num = 0

    def __init__(self, brand, year, size, data):
        self.data = extract_data(brand, year, size, data)

    def avg_buy(self):
        # runs a procurement vcg auction for buying cars_num cars on the given self.data.
        # returns the average price paid for a winning car.\
        if len(self.data) > self.cars_num:
            return self.data[self.cars_num]
        else:
            return 0

    def cdf(self, x):
        # return F(x) for the histogram self.data
        count_smaller = 0
        count_same_bigger = 1
        a = 0
        b = 0
        if x < min(self.data):
            return 0
        elif x >= max(self.data):
            return 1
        else:
            while self.data[count_smaller] <= x:
                count_smaller += 1
            a = self.data[count_smaller-1]

            index = count_smaller
            while (index != (len(self.data)-1) and self.data[index] == self.data[index+1]):
                count_same_bigger += 1
                index += 1
            b = self.data[index]

            return (count_smaller/len(self.data) + (count_same_bigger/len(self.data)) * ((x-a)/(b-a)))


    def os_cdf(self,r , n, x):
        # The r out of n order statistic CDF
        f_r = 0
        F_x = self.cdf(x)
        for j in range(r, n+1):
            n_bchar_j=math.factorial(n)/(math.factorial(j)*math.factorial(n-j))
            f_r +=(n_bchar_j) * (F_x ** j) *(1-F_x) ** (n - j)

        return f_r

    def exp_rev(self):
        # returns the expected revenue in future auction for cars_num items and buyers_num buyers
        tail = 0
        order = self.buyers_num - self.cars_num
        exp_rev = 0
        if self.buyers_num > self.cars_num:
            for i in range(0, self.data[len(self.data) - 1]):
                tail += (1 - self.os_cdf(order, self.buyers_num, i))
            exp_rev = tail * self.cars_num
            return exp_rev
        else:
            return exp_rev

    def median(self, lst):
        length = len(self.data)
        if length % 2 == 0:
            return (self.data[length // 2] + self.data[length // 2 - 1]) / 2
        else:
            return self.data[length // 2]




    def exp_rev_median(self, n):

        exp = 0
        # check if data length is even:
        median = self.median(self.data)
        payment_median = n * (self.cdf(median)) ** (n-1) * (1-self.cdf(median))

        for i in range(0, max(self.data)):
            if i >= median:
                exp += (1-self.os_cdf(n-1, n, x=i))
            else:
                exp += (1-self.os_cdf(n-1, n, median))
        exp_rev = exp + payment_median * median
        return exp_rev










########## Part C ###############

    def reserve_price(self):
        # returns your suggestion for a reserve price based on the self_data histogram.
        tail = 0
        order = self.buyers_num - self.cars_num+1
        for i in range(0, self.data[len(self.data) - 1]):
            tail += (1 - self.os_cdf(order, self.buyers_num, i))
        return tail
