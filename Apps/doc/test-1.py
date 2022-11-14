

all_data = []
basic_data_1 = {
    "id":1,
}
basic_data_2 = {
    "id":2,
}
basic_data_3 = {
    "id":3,
}
basic_data_4 = {
    "id":4,
}
upper_data_1 = []
upper_data_1.append(basic_data_1)
upper_data_1.append(basic_data_2)

upper_data_2 = []
upper_data_2.append(basic_data_3)
upper_data_2.append(basic_data_4)

all_data.append(upper_data_1)
all_data.append(upper_data_2)

if __name__ == '__main__':
    print(all_data)