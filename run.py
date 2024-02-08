from client.charging_client import *
from graphs.baseload_graph import *
from graphs.price_per_houre_graph import *
import time


charging_hours = []
charging_type = ""

def reset_battery_charge():
    print("Current battery charge: ",round(get_battery_charge()),"%")
    reset_battery()
    print("Battery charge reset to:",round(get_battery_charge()),"%")

def charge_battery_until_80_percent():
    while round(get_battery_charge()) < 80:

        start_charging()

        info = get_all_info()
        current_hour = info["sim_time_hour"]
        current_minute = info["sim_time_min"]
        current_time = f"{current_hour:02}:{current_minute:02}"
        current_consumption = info["base_current_load"]
        price_per_hour = get_price_per_hour()
        current_price = price_per_hour[current_hour]

        print("Currently chargin with no restrictions")
        print(f"Time: {current_time}, Consumption|price: {current_consumption}kWh|{round(current_price/100, 4)}sek, Charge: {round(get_battery_charge())}%")

        time.sleep(1)

    # Stop charging once the battery reaches 80%
    stop_charging()
    print("Battery charged to 80%, stopping charging.")

    print("Final Battery Charge Percentage:", round(get_battery_charge()))

def smart_charging():
    global charging_hours
    global charging_type
    charging_status = False

    while True:
        info = get_all_info()
        current_hour = info["sim_time_hour"]
        current_minute = info["sim_time_min"]
        current_time = f"{current_hour:02}:{current_minute:02}"
        current_consumption = info["base_current_load"]
        price_per_hour = get_price_per_hour()
        current_price = price_per_hour[current_hour]
        price_in_sek = round(current_price/100, 4)

        if charging_type == "consumption":
            print("Currently charging based on consumption")
            print(f"Time: {current_time}, Consumption: {current_consumption}kWh, Charge: {round(get_battery_charge())}%")
       
        elif charging_type == "price":
            print("Currently charging based on price per hour")
            print(f"Time: {current_time}, Prise: {price_in_sek}sek, Charge: {round(get_battery_charge())}%")
        
        elif charging_type == "both":
            print("Currently charging based on consumption and price/hour")
            print(f"Time: {current_time}, Consumption|price: {current_consumption}kWh|{price_in_sek}sek, Charge: {round(get_battery_charge())}%")
        
        else:
            print(f"Time: {current_time}, Consumption|price: {current_consumption}kWh|{price_in_sek}sek, Charge: {round(get_battery_charge())}%")
        
        #Makes sure it will not go beyond 11 kW
        if current_consumption < 11:
            
            if current_hour in charging_hours and not charging_status and round(get_battery_charge()) < 80:
                charging_status = True
                print("Start charging")
                start_charging()

            elif current_hour not in charging_hours and charging_status:
                charging_status = False
                print("Stop charging")
                stop_charging()

        elif current_consumption > 11 and charging_status:
            charging_status = False
            stop_charging()

        if round(get_battery_charge()) >= 80 and charging_status:
            charging_status = False
            stop_charging()
            print(f"Battery charged to {round(get_battery_charge())}%, stopping charging.")
        time.sleep(1)


def convert_to_hours_and_minutes(numbers):
    formatted_times = ["{:02d}:00".format(hours) for hours in numbers]
    return formatted_times

def choose_charging_hours():
    global charging_hours
    global charging_type

    baseload = get_baseload()
    price_per_hour = get_price_per_hour()
    print("How do you want to charge your car?")
    print("1. Based on kWh consumption")
    print("2. Based on price/kWh")
    print("3. Combine consumption and price")
    print("4. Start charging now")
    user_input = int(input("Enter a number: "))

    if user_input == 1:
        charging_type = "consumption"
        graph_baseload()
        choosen_hours = float(input("Charge you car while kWh consumption < "))
        charging_hours = [index for index, value in enumerate(baseload) if value < choosen_hours]
        converted_to_time = convert_to_hours_and_minutes(charging_hours)
        print("Your car will be charged during these hours", converted_to_time)

    elif user_input == 2:
        charging_type = "price"
        graph_price()
        choosen_hours = float(input("Charge you car while price/kWh < "))
        charging_hours = [index for index, value in enumerate(price_per_hour) if value < choosen_hours]
        converted_to_time = convert_to_hours_and_minutes(charging_hours)
        print("Your car will be charged during these hours", converted_to_time, "\n")

    elif user_input == 3:
        charging_type = "both"
        graph_baseload()
        graph_price()
        consumption = float(input("Charge you car while kWh consumption < "))
        price_hour = float(input("and while price/kWh < "))

        consumption_hours= [index for index, value in enumerate(baseload) if value < consumption]
        price_hours= [index for index, value in enumerate(price_per_hour) if value < price_hour]

        charging_hours = list(set(consumption_hours) & set(price_hours))
        print(charging_hours)

        converted_to_time = convert_to_hours_and_minutes(charging_hours)
        print("Your car will be charged during these hours", converted_to_time, "\n")

    elif user_input == 4:
        charging_type = "none"
        charge_battery_until_80_percent()
        return
        
    smart_charging()



if __name__ == "__main__":
    reset_battery_charge()
    choose_charging_hours()
    #smart_charging()
