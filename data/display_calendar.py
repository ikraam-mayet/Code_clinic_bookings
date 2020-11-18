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
        return [l[i:i + n] for i in range(0, len(l), n)]


def display_cal(src_fn):
        """
        This function reads the events .csv file. It then puts the information 
        in a list, seperating the list into the different events. It uses tabulate 
        to convert the list into a table.
        """
        with open(src_fn) as f:
                data = f.read()

        data_list = re.split(',|\n',data)

        header  =['Event name', 'Start Date', 'Start Time', 'End Date', 'End Time']

        data = [ elem for elem in data_list if elem not in header]

        data_list2 = divide_chunks(data, 5)

        return (tabulate(data_list2, header, tablefmt="fancy_grid"))


