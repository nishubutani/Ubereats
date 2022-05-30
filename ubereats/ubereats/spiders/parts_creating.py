

def parts():

    spider_name = input("Enter your spider name :- ")
    highest_value = input("enter your ending value :- ")
    start_value = input("enter your starting value :- ")
    parts_number = input("eneter number of parts :- ")
    bat_name = input("eneter bat file name :- ")
    partition =  (int(highest_value) - int(start_value))//int(parts_number)
    print(partition)

    import os
    if os.path.exists(f"{bat_name}.bat"):
        print("The file does not exist")
        os.remove(f"{bat_name}.bat")
    else:
        print("The file does not exist")

    with open(f"{bat_name}.bat", "a") as my_file:
        first_value = int(start_value)
        for i in range(int(parts_number)):
            new_value = first_value + int(partition)

            #-------------------------------------------------------------------------#
            final_value = f'start scrapy crawl {spider_name} -a a={first_value} -a b={new_value}'

            #------------------ if you are using start , end -------------------------------------#
            # final_value = f'start scrapy crawl {spider_name} -a start={first_value} -a end={new_value}'
            # final_value = f'start scrapy crawl {spider_name} -a start={first_value}'
            #-------------------------------------------------------newdataextraction1--------------------------------#
            # print(final_value)
            first_value = new_value
            my_file.write(final_value)
            my_file.write("\n")
        print("succesfully create bat file")


def create_bat():
    spider_name = input("Please enter spider_name:- ")
    start_point = input("Please Enter Start point:- ")
    end_point  = input("Please Enter End Point:- ")
    howmany_part = input("Please Enter Number of part:-")
    file_name = input("Please Enter Bat File Name:- ")
    loop_variable = (int(end_point)-int(start_point))//int(howmany_part)

    with open(f"{file_name}.bat", "a") as a_file:
        remember_value = int(start_point)
        for i in range(int(howmany_part)):
            changed_value = remember_value + int(loop_variable)
            a_file.write(f'start scrapy crawl {spider_name} -a a={remember_value} -a b={changed_value}')
            # a_file.write(f'start python data_upload.py {remember_value} {changed_value}')
            a_file.write("\n")
            remember_value = changed_value

if __name__ == '__main__':
    # create_bat()
    parts()
