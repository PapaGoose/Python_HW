import csv
import re

class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        return '.' + self.photo_file_name.split('.')[-1]


class Car(CarBase):
    car_type = 'car'

    def __init__(self,  brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        if '.' not in passenger_seats_count:
            self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying, body_lwh):
        super().__init__(brand, photo_file_name, carrying)
        if re.fullmatch('\d+(?:\.\d+)?x\d+(?:\.\d+)?x\d+(?:\.\d+)?', body_lwh):
            self.body_length, self.body_width, self.body_height = list(map(float, body_lwh.split('x')))
        else:
            self.body_length, self.body_width, self.body_height = 0.0, 0.0, 0.0


    def get_body_volume(self):
        return self.body_length*self.body_width*self.body_height


class SpecMachine(CarBase):
    car_type = 'spec_machine'

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            try:
                if not re.fullmatch('.\w+', row[3]) and len(row[3].split('.')) == 2:
                    if row[0] == 'car':
                        f_lst = [row[1], row[3], row[5], row[2]]
                        if f_lst.count('') > 0:
                            continue
                        else:
                            try:
                                car = Car(*f_lst)
                                car_list.append(car)
                            except:
                                continue
                    elif row[0] == 'truck':
                        f_lst = [row[1], row[3], row[5], row[4]]
                        if f_lst.count('') > 0:
                            if f_lst[-1] == '' and f_lst.count('') == 1:
                                try:
                                    car = Truck(*f_lst)
                                    car_list.append(car)
                                except:
                                    continue
                        else:
                            try:
                                car = Truck(*f_lst)
                                car_list.append(car)
                            except:
                                continue
                    elif row[0] == 'spec_machine':
                        f_lst = [row[1], row[3], row[5], row[6]]
                        if f_lst.count('') > 0:
                            continue
                        else:
                            try:
                                car = SpecMachine(*f_lst)
                                car_list.append(car)
                            except:
                                continue
            except:
                continue


    return car_list

