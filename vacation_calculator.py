from datetime import datetime, timedelta

def ask_for_response_option(option_list, question):
    print(question)
    list_option = []
    for i in range(len(option_list)):
        list_option.append(i+1)
    for option in option_list:
        print(' '+str(option_list.index(option)+1) +': '+str(option))
    while True:
        selection = input('Choice: ')
        try:
            if int(selection) not in list_option:
                print('Please select a valid option')
            else:
                return int(selection)
        except:
            print('Please select a valid option')

def ask_for_response_date(question):
    while True:
        return_date = input(question)
        try:
            return datetime.strptime(return_date, '%m-%d-%Y')
        except:
            print('Please enter a date in a mm-dd-yyyy format')

def valid_string(question):
    while True:
        return_string = input(question)
        if return_string != '':
            return return_string
        else:
            print('Please enter a non-blank string')

class Trip:
    def __init__(self,start_date, end_date, location):
        self.start_date = datetime.strptime(start_date, '%m-%d-%Y')
        self.end_date = datetime.strptime(end_date,'%m-%d-%Y')
        self.location = location

    def __repr__(self):
        return 'Trip to {location} {started} - {ended}'.format(location = self.location, started = self.start_date.strftime('%m-%d-%Y'), ended = self.end_date.strftime('%m-%d-%Y'))

    def duration(self):
        days = self.end_date - self.start_date
        return days.days + 1

    def duration_vacation_days(self,company_holidays):
        counter = 0 
        holidays = []
        for i in range(self.duration()):
            day = self.start_date + timedelta(days=i)
            for holiday in company_holidays:
                holiday_dt = datetime.strptime((holiday + '-' + day.strftime('%Y')),'%m-%d-%Y')
                holidays.append(holiday_dt)
            if day.weekday() not in [5,6] and day not in holidays:
                counter += 1
        return counter

class Employee:
    def __init__(self, employee_name, employee_start_date, num_vacation_days,company_holidays, roll_over, limit, max_vaca,trips):
        self.employee_name = employee_name
        self.employee_start_date = employee_start_date
        self.num_vaction_days = num_vacation_days
        self.company_holidays = company_holidays
        self.roll_over = roll_over
        self.limit = limit
        self.max_vaca = max_vaca
        self.trips = trips
        self.accrual_rate = num_vacation_days / 365

    def __repr__(self):
        return '{} is a employee who started on {} and accrues {} vacation days a day'.format(self.employee_name, self.employee_start_date, round(self.accrual_rate,2))

    def return_trips(self):
        trips_lst = []
        self.trips.sort(key=lambda x: x.start_date)
        for trip in range(len(self.trips)):
            trip_str = 'Trip {trip_id} - {location} on {start} for {days} days using {vacation_days} vacation days'.format(
                trip_id = trip + 1
                , location = self.trips[trip].location
                , start = self.trips[trip].start_date.strftime('%m-%d-%Y')
                , days = self.trips[trip].duration()
                , vacation_days = self.trips[trip].duration_vacation_days(self.company_holidays)
            )
            trips_lst.append(trip_str)
        return trips_lst

    def add_trip(self):
        print('Please enter the vacation details:')
        start_date = ask_for_response_date('  Vacation Start Date: ')
        end_date = ask_for_response_date('  Vacation End Date: ')
        location = valid_string('  Destination: ')
        for trip in range(len(self.trips)):
            latest_start = max(self.trips[trip].start_date, start_date)
            earliest_end = min(self.trips[trip].end_date, end_date)
            delta = (earliest_end - latest_start).days + 1
            overlap = max(0, delta)
            if overlap != 0:
                break
            if (trip+1) == len(self.trips): 
                new_trip = Trip(start_date.strftime('%m-%d-%Y'), end_date.strftime('%m-%d-%Y'), location)
                self.trips.append(new_trip)
                return True
        print('Your vacation overlaps with a pre-existing vacation ..')
        return False

            
    def delete_trip(self):
        trips_del = []
        for trip in self.trips:
            trips_del.append(trip)
        trips_del.append('Cancel')
        choice = ask_for_response_option(trips_del, 'Which Trip would you like to delete?')
        print(choice)
        if choice == len(trips_del):
            return False
        else:
            self.trips.pop(choice - 1)
            return True
    
    def calculate_vacation(self):
        start_day = datetime.strptime(self.employee_start_date, '%m-%d-%Y')
        day_delta = 0
        if self.roll_over == False:
            if start_day.strftime('%Y') == datetime.now().strftime('%Y'):
                day_delta = (datetime.now() - start_day).days
            else:
                day_delta = (datetime.now() - datetime(int(datetime.now().strftime('%Y')), 1, 1)).days
        else:
            if (datetime.now() - start_day).days * self.accrual_rate >= self.max_vaca and self.limit == True:
                day_delta = self.max_vaca
            else: 
                day_delta = (datetime.now() - start_day).days
        day_delta = day_delta * self.accrual_rate
        for trip in self.trips:
            day_delta = day_delta - trip.duration_vacation_days(self.company_holidays)
        return round(day_delta)

def get_holidays():
    more_holidays = True
    holidays = []
    while more_holidays == True:
        holidays.append(ask_for_response_date('Please enter a company holiday: ').strftime('%m-%d'))
        if ask_for_response_option(['Y','N'], 'Are there more company holidays? (1/2) ') == 2:
            more_holidays = False
    return holidays


def create_employee():
    name = valid_string('What is the employee\'s name? ')
    start_date = ask_for_response_date('What day did the employee start? ').strftime('%m-%d-%Y')
    print('We are now going to collect the company holidays, please enter the holidays in mm-dd-yyyy format with the year being the current year')
    holidays = get_holidays()
    vacation_days = int(valid_string('Please enter how many vacation days the employee gets per year excluding company holidays: '))
    roll_over = ask_for_response_option([True, False], 'Does the vacation time roll over year over year? (1/2) ')
    limit = ''
    total_days = ''
    if roll_over == 1:
        roll_over = True
        limit = ask_for_response_option([True, False], 'Is there a limit to how much vacation you can accumulate? (1/2) ')
        if limit == 1:
            limit = True
            total_days = int(valid_string('What is the max vacation you can accumulate? '))
        else:
            limit = False
            total_days = 0
    else:
        roll_over = False
        limit = False
        total_days = 0
    new_employee = Employee(name,start_date,vacation_days,holidays,roll_over,limit,total_days,[])
    return new_employee
    
def save_employee(employee):
    name = employee.employee_name
    start_date = employee.employee_start_date 
    vacation_days = employee.num_vaction_days
    holidays = employee.company_holidays
    roll_over = employee.roll_over
    limit = employee.limit
    total = employee.max_vaca
    path_to_save = input('Please enter a path to save the employee (EX. C:\\test\\123\\): ')
    holiday_string = ''
    for day in holidays:
        holiday_string = holiday_string + day + '*'
    holiday_string = holiday_string[:-1]
    string_to_write = 'Employee' + ' ' + name + ' ' + start_date + ' ' + str(vacation_days) + ' ' +  holiday_string + ' ' + str(roll_over) + ' ' + str(limit) + ' ' + str(total) + '\n'
    with open(path_to_save + name + '.txt', "w") as file1:
        file1.write(string_to_write)
        for trip in ned.trips:
            string_to_write = 'Trip' + ' ' + trip.start_date.strftime('%m-%d-%Y') + ' ' + trip.end_date.strftime('%m-%d-%Y') + ' ' + trip.location + '\n'
            print(string_to_write)
            file1.write(string_to_write)
        file1.truncate()
    return True


#print(ned.return_trips())
#ned.add_trip()
#ned.delete_trip()
#print(ned.return_trips())
#ned.calculate_vacation()
#C:\Users\Ned Charles\Documents\
#ned = create_employee()
summer_trip = Trip('7-22-2022','7-27-2022','Hawaii')
summer_trip2 = Trip('7-28-2022','7-29-2022','San Diego')
ned = Employee('Ned', '05-17-2021', 20, ['11-25','12-31'], False, False, 0, [summer_trip, summer_trip2])
save_employee(ned)

#Class Employee Vacation Benefits
##variables:
#---Employee Name
#---Employee Start Date
#---vacation Days per year
#---Company Holidays
#---accrual rate per day (calculated in class)

#---roll-over -> T/f


#Class Trip
##Variables:
#---Start Date
#---End Date
#---Location
##Methods:
#--Duration


#Functionality
##Section 1
#--Create new employee
#--Load existing employee
##Section 2
#--List Trips taken
#--Log a trip
#--Delete a trip
#--List vacation left
#--Update Employee:
#---add a new company holiday
#---remove a company holiday
#---change vaction days per year in employee file

#Save
#Exit without saving
        
