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


def remove_attendees(data_list):
        """  
        Removes attendees from the list.
        """
        for i in range (len(data_list) - 1):
                data_list[i].pop(6) 

        return data_list


def display_cal(src_fn):
        """
        This function reads the events.csv file. It then puts the information 
        in a list, seperating the list into the different events. It uses the 
        tabulate function to convert the list into a table.
        """
        with open(src_fn) as f:
                data = f.read()

        data_list = re.split(',|\n',data)

        header =['Event name', 'Description', 'Start Date', 'Start Time', 'End Date', 'End Time']

        data = [ elem for elem in data_list if elem not in header]

        data_list2 = divide_chunks(data, 7)

        for i in range (len(data_list2) - 1):
                if int(data_list2[i][6]) > 1:
                        data_list2[i][0] = '\u001b[31;1m'+data_list2[i][0]
                        data_list2[i][5] = data_list2[i][5]+'\u001b[0m'

                elif int(data_list2[i][6]) == 1:
                        data_list2[i][0] = '\u001b[32;1m'+data_list2[i][0]
                        data_list2[i][5] = data_list2[i][5]+'\u001b[0m'

                else:
                        data_list2[i][0] = '\u001b[34m'+data_list2[i][0]
                        data_list2[i][5] = data_list2[i][5]+'\u001b[0m'
        
        remove_attendees(data_list2)

        return (tabulate(data_list2, header, tablefmt="fancy_grid"))


def display_volunteer_cal(src_fn):
        """
        This function reads the events.csv file. It then puts the information 
        in a list, seperating the list into the different events. It uses the 
        tabulate function to convert the list into a table. If the event only has 
        a volunteer the it will be displayed in green. If the event has a patient
        and volunteer meaning it is fully booked it will be displayed in red.
        """
        with open(src_fn) as f:
                data = f.read()

        data_list = re.split(',|\n',data)

        header =['Event name', 'Description', 'Start Date', 'Start Time', 'End Date', 'End Time']

        data = [ elem for elem in data_list if elem not in header]

        data_list2 = divide_chunks(data, 7)

        for i in range (len(data_list2) - 1):
                if int(data_list2[i][6]) > 1:
                        data_list2[i][0] = '\u001b[31;1m'+data_list2[i][0]
                        data_list2[i][5] = data_list2[i][5]+'\u001b[0m'

                elif int(data_list2[i][6]) == 1:
                        data_list2[i][0] = '\u001b[32;1m'+data_list2[i][0]
                        data_list2[i][5] = data_list2[i][5]+'\u001b[0m'

                else:
                        data_list2[i][0] = '\u001b[34m'+data_list2[i][0]
                        data_list2[i][5] = data_list2[i][5]+'\u001b[0m'

                        
        remove_attendees(data_list2)

        return (tabulate(data_list2, header, tablefmt="fancy_grid"))


