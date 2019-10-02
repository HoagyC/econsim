import logging
import random
import json
import math

logging.basicConfig(level=logging.INFO)

class Firm():
    def __init__(self, good, config):
        self.prod_cap = config["prod_cap"]
        self.money = config["init_money"]
        self.fcost_upkeep = config["fcost_upkeep"]
        self.fcost = config["fcost"]
        self.good = good
        
        self.supply_offers = [(p/2, q) for p in range(1, 20) for q in range(10, 100, 10)]
        if config["learning"] == "vre":
            self.vre_recency = 0.9
            self.vre_explore = 0.5
            self.vre_cool = 2
    
    def get_costs(self, prod_level):
        # Calculates the profit and net worth of the firm given the costs
        # which are stored in self and the quantity produced.

        fixed_cost = self.cost_upkeep*self.prod_cap + self.cost_upkeep
        total_cost = self.quad_mcost*(prod_cap**2) + self.mcost*prod_level + fixed_cost
        profit = self.price*prod_level - total_cost
        net_worth = self.money + self.cap_cost*self.prod_cap + profit
        return profit, net_worth

    def allocate_profit(self):
        if profit >= 0 and prod_level == prod_cap:
            self.prod_cap += ((1-self.inv_level)*profit)/cap_cost
            self.dividend = self.div_level*(self.money+inv_level*profit)
            self.money += inv_level*profit - self.dividend
        elif profit >= 0 and prod_level < prod_cap:
            self.dividend = self.div_level*(self.money + profit)
            self.money += profit - self.dividend
        
        else:
            ind = 1 if (self.money + profit >= 1) else 0
            self.cap += (1-ind)*(self.money + profit)/self.cap_cost
            self.money = ind*(self.money +profit)
            self.dividend = 0

    '''
    Learning algorithm that takes in profit given previous 
    supply decisions and potential more available information 
    to decide the output, represented as (Markup, % of max production)
    '''
    def supply_offer_vre(self):
        num_options = len(self.supply_offers)
        self.qs = [0]*num_options
        exp_qs = [math.exp(self.qs[i])/self.vre_cool for i in range(num_options)]
        denom = sum(exp_qs)
        ps = [exp_qs[i]/denom for i in range(num_options)]
        chosen_id = random.choices(list(range(num_options)), weights = ps)[0] 
        self.price, self.supply = self.supply_offers[chosen_id]

        # RL algorithm, should be a separate function
        # for i in range(num_options):
        #     if chosen_id == i:
        #         self.qs[i] = (1 - self.vre_explore)*profit + self.qs[i]*(1 - self.vre_recency)
        #     else:
        #         self.qs[i] = self.qs[i]*(1 - self.vre_recency) + (self.vre_explore*self.qs[i])/(num_options-1)
    

    def vre_init(supply_offers):
       self.ps = [1]*len(self.supply_offers)


    # def log(self):

def calc_global_div(firm_list, num_people):
    p = 0
    for firm in firm_list:
        p += firm.profit
    p /= num_people
    return p

class Consumer():
    def __init__(self, config, ID):
        self.ID = ID
        self.endowment = config["av_endowment"]
        self.income = self.endowment
        self.hash_need = config["hash_need"]
        self.bean_need = config["bean_need"]

        self.hash_value = config["hash_value"]
        self.bean_value = config["bean_value"]

        self.bean = 0
        self.hash = 0

        
    def get_income():
        # nonlocal global_div
        self.saving = self.income - self.expenditure
        self.income = self.saving + self.endowment(t) + global_div
    
    def get_demands(self, hash_low_price, bean_low_price):
        self.net_bean = self.bean_need - self.bean
        self.net_hash = self.hash_need - self.hash
        if not hash_low_price:
           if self.net_hash > 0 or bean_low_price*self.net_bean > self.income:
               return "dead", "dead"
           else: 
               self.hash_demand = 0
               self.bean_demand = self.income/bean_low_price

        if not bean_low_price:
           if self.net_bean > 0 or hash_low_price*self.net_hash > self.income:
               return "dead", "dead"
           else:
               self.bean_demand = 0
               self.hash_demand = self.income/hash_low_price

        if self.net_bean*bean_low_price + self.net_hash*hash_low_price > self.income:
            return "dead", "dead"
        


        if hash_low_price:
            self.hash_demand = (1-self.hash_value)*self.net_hash + \
                           ((self.hash_value * \
                           (self.income - self.net_bean*bean_low_price)) / \
                           hash_low_price)

        if bean_low_price:
            self.bean_demand = (1-self.bean_value)*self.net_bean + \
                           ((self.bean_value * \
                           (self.income - self.net_hash*hash_low_price)) / \
                           bean_low_price)
        if self.hash_demand < 0:
            self.hash_demand = 0
            if bean_low_price:
                self.bean_demand = self.income / bean_low_price
        if self.bean_demand < 0:
            self.bean_demand = 0
            if hash_low_price:
                self.hash_demand = self.income / hash_low_price

        return self.hash_demand, self.bean_demand


    def begin_step(self):
        self.bean = 0
        self.hash = 0




def selling_round(next_person, bean_low_firm, hash_low_firm, hd, bd):
    bean_out = False
    hash_out = False
    person_out = False

    if hash_low_firm.supply > hd and bean_low_firm.supply > bd:
        hash_low_firm.supply -= hd
        bean_low_firm.supply -= bd
        next_person.hash += hd
        next_person.bean += bd
        person_out = True
    elif hash_low_firm.supply > next_person.net_hash and \
         bean_low_firm.supply > next_person.net_bean:
        next_person.hash += hash_low_firm.supply 
        next_person.bean += bean_low_firm.supply
        hash_low_firm.supply - next_person.net_hash
        bean_low_firm.supply - next_person.net_bean
        person_out = True

    elif hash_low_firm.supply > next_person.net_hash and \
         bean_low_firm.supply < next_person.net_bean:
        next_person.hash += max([next_person.net_hash, 0])
        next_person.bean += bean_low_firm.supply
        hash_low_firm.supply -= max([next_person.net_hash, 0])
        bean_low_firm.supply = 0
        bean_out = True
    elif bean_low_firm.supply > next_person.net_bean and \
         hash_low_firm.supply < next_person.net_hash:
        next_person.bean += max([next_person.net_bean, 0])
        next_person.hash += hash_low_firm.supply
        bean_low_firm.supply -= max([next_person.net_bean, 0])
        hash_low_firm.supply = 0
        hash_out = True
    else:
        next_person.hash += hash_low_firm.supply
        next_person.bean += bean_low_firm.supply
        bean_low_firm.supply = 0
        hash_low_firm.supply = 0
        bean_out = True
        hash_out = True

    return bean_out, hash_out, person_out

    for person in people:
        if person.net_hash < 0 or person.net_beans < 0:
            person.die()


def setup(config):
    print(config)
    people = [Consumer(config, i) for i in range(config["np"])]
    print("People generated.")
    hash_firm_list = [Firm("hash", config) for _ in range(config["nh"])]
    bean_firm_list = [Firm("bean", config) for _ in range(config["nb"])]
    print("Firms generated")
    return hash_firm_list, bean_firm_list, people

def main(config):
    print("Starting Setup")
    hash_firm_list, bean_firm_list, people = setup(config)
    for step in range(config["total_steps"]):
        buyers = people[:]
        random.shuffle(buyers)
        random.shuffle(hash_firm_list)
        random.shuffle(bean_firm_list)

        for firm in hash_firm_list + bean_firm_list:
            firm.supply_offer_vre()

        hash_sell_list = sorted(hash_firm_list, key=lambda x: x.price)
        bean_sell_list = sorted(bean_firm_list, key=lambda x: x.price)
        
        hash_low_firm = hash_sell_list.pop(0)
        hash_low_price = hash_low_firm.price

        bean_low_firm = bean_sell_list.pop(0)
        bean_low_price = bean_low_firm.price
    
        next_person = buyers.pop(0)
        hd, bd = next_person.get_demands(hash_low_price, bean_low_price)

        while (hash_sell_list or bean_sell_list) and buyers:
            bs, hs, cd = selling_round(next_person, bean_low_firm, hash_low_firm, hd, bd)
            # print("sale made", bs, hs, cd, step, len(hash_sell_list), len(bean_sell_list), len(buyers))
            # print(hash_low_firm, hash_low_price)
            if hs and hash_sell_list:
                hash_low_firm = hash_sell_list.pop(0)
                hash_low_price = hash_low_firm.price

            if bs and bean_sell_list:
                bean_low_firm = bean_sell_list.pop(0)
                bean_low_price = bean_low_firm.price

            if not hash_sell_list:
                hash_low_price = 0
            if not bean_sell_list:
                bean_low_price = 0
            
            # print(bean_low_firm.supply)

            if cd:
                next_person = buyers.pop(0)
            
            hd, bd = next_person.get_demands(hash_low_price, bean_low_price)
            # logging.info(f'Hash demand: {hd}, Bean demand: {bd}, Hash price: {hash_low_price}, Bean price: {bean_low_price}')

            while hd == "dead" and buyers:
                logging.info(f'Person {next_person.ID} has died in step {step}, {len(people)} remain.')
                next_person = buyers.pop(0)
                people.remove(next_person)
                hd, bd = next_person.get_demands(hash_low_price, bean_low_price)
        
        for person in people:
            person.begin_step()
        # update_firms(hash_firm_list, bean_firm_list)



if __name__ == '__main__':
    with open('ace_config.json', 'r') as f:
        config = json.load(f)

    main(config)
