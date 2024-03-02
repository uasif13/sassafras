import csv
import uuid
import pprint
import math

class Revenue():
    def __init__(self) -> None:
        self.input_file = "saasafras - Input2.csv"
        self.account_managers = None
        self.customers = []
        self.total_revenue = []
        self.input_list = []
        self.csat = []
        self.churn = []
        
    def validate_row(self,row):
        return row[0]+row[1]+row[2] == 20
    
    def validate_input(self):
        for row in self.input_list:
            try:
                if not self.validate_row(row):
                    raise ValueError("Bad Input")
            except:
                raise ValueError("Input is Bad")

    def input(self):
        with open(self.input_file,mode="r") as infile:
            reader = csv.reader(infile)
            self.input_list = [[int(rows[0]),int(rows[1]),int(rows[2])] for rows in reader]
            self.validate_input()
    
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
        am = [row[1] for row in self.input_list]
        am_customers = list(zip(am,self.customers))
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
            remaining_customers = customers[i]
            revenue = 0
            for manager in account_manager_month:
                if remaining_customers -25 > 0:
                    revenue += 25*math.pow(1.2,(account_manager_month[manager]))*100
                    remaining_customers -= 25
                else:
                    revenue += remaining_customers*math.pow(1.2,(account_manager_month[manager]))*100
                    remaining_customers = 0
            # non account manager accounts
            revenue += remaining_customers*100
            self.total_revenue.append(revenue)

    def get_revenue_list(self):
        return self.total_revenue
    
    def get_revenue(self):
        return sum(self.total_revenue)
    
    def get_customers(self):
        return self.customers
        
    def calculate_customers(self):
        self.csat = [row[2] + 70 for row in self.input_list]
        self.churn = [math.pow(0.85,csat-70)*0.1 for csat in self.csat]
        previous_customers = 1000
        for i in range(len(self.input_list)):
            if i>0: previous_customers = self.customers[i-1]
            # TRUNC(PREV_CUS*(1-CHURN)+25+5*SALE_REPS)
            self.customers += [math.trunc(previous_customers*(1-self.churn[i])+25+self.input_list[i][0]*5)]
        

if __name__=="__main__":
    rc = Revenue()
    rc.input()
    rc.calculate_customers()
    rc.calculate_account_managers()
    rc.calculate_revenue()
    # pprint.pprint(rc.get_account_managers())
    for (i,item) in enumerate(rc.get_revenue_list()):
        print(i, "  ", item)
    print(rc.get_revenue())
    