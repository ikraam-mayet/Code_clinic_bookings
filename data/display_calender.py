import re
from tabulate import tabulate


def divide_chunks(l, n): 
        """
        param:
        l - list
        n - the chucnks you want the list to be broken up into

        This function takes the list and sees in what chuncks you want the list 
        to be broken up into another list
        """
        for i in range(0, len(l), n):
                yield l[i:i + n] 


def display_cal ():
        """
        This function reads the events .csv file. It then puts the information 
        in a list, seperating the list into the different events. It uses tabulate 
        to convert the list into a table.
        """
        with open('events.csv') as f:
                data = f.read()

        data_list = re.split(',|\n',data)

        header  =['Event name', 'Start Date', 'Start Time', 'End Date', 'End Time']

        data = [ elem for elem in data_list if elem not in header]


        data_list2 = list(divide_chunks(data, 5)) 
        print(tabulate(data_list2, header, tablefmt="fancy_grid"))
