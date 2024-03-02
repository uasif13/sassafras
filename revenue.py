import csv
import uuid
import pprint
import math

class Revenue():
    def __init__(self) -> None:
        self.input = "saasafras - Input.csv"
        self.account_managers = None
        self.customers = []
        self.total_revenue = []

    def get_input(self) -> list:
        with open(self.input,mode="r") as infile:
            reader = csv.reader(infile)
            mydict = [[int(rows[0]),int(rows[1])] for rows in reader]
            self.customers = [rows[1] for rows in mydict]
            
        return mydict
    
    def add_account_manager(self, current_ams):
        current_am = uuid.uuid4()
        current_ams[current_am] = 0
        
    def add_month(self, current_ams):
        for am in current_ams:
            if current_ams[am] < 6:
                current_ams[am] += 1
                
    def remove_account_manager(self,current_ams):
        minimum = None
        minimum_value = 7
        for current_am in current_ams:
            if current_ams[current_am] < minimum_value:
                minimum = current_am
                minimum_value = current_ams[current_am]
        del current_ams[minimum] 

    def calculate_account_managers(self):
        am_customers = self.get_input()
        current_ams = {}
        account_managers = []
        # first month
        for month, (ams, _) in enumerate(am_customers):
            # no account manager change
            previous_ams_length = 0
            if month > 0:
                previous_ams_length = len(account_managers[month-1])
            # Less account managers
            if previous_ams_length > ams:
                for _ in range(previous_ams_length-ams):
                    self.remove_account_manager(current_ams)
            # More account managers
            elif previous_ams_length < ams:
                for _ in range(ams-previous_ams_length):
                    self.add_account_manager(current_ams)
            self.add_month(current_ams)
            current_ams = {k: v for k, v in sorted(current_ams.items(), key=lambda item: item[1])}
            account_managers.append(current_ams.copy())
        self.account_managers = account_managers
    
    def get_customers(self):
        return self.customers
    
    def get_account_managers(self):
        return self.account_managers
    
    def calculate_revenue(self):
        customers = self.customers
        account_manager_history = self.account_managers
        for i, account_manager_month in enumerate(account_manager_history):
            revenue = 0
            for manager in account_manager_month:
                revenue += 25*math.pow(1.2,(account_manager_month[manager]))*100
            # non account manager accounts
            revenue += (customers[i]-(len(account_manager_month)*25))*100
            self.total_revenue.append(revenue)

    def get_revenue_list(self):
        return self.total_revenue
    
    def get_revenue(self):
        return sum(self.total_revenue)
        
        

if __name__=="__main__":
    rc = Revenue()
    rc.calculate_account_managers()
    rc.calculate_revenue()
    # pprint.pprint(rc.get_account_managers())
    for (i,item) in enumerate(rc.get_revenue_list()):
        print(i, "  ", item)
    print(rc.get_revenue())
    