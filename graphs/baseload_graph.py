import matplotlib.pyplot as plt
from client.charging_client import *

def graph_baseload():
    baseload_numbers_list = get_baseload()

    hours = [str(i).zfill(2) for i in range(24)]

    plt.figure(figsize=(10, 6))
    plt.plot(hours, baseload_numbers_list, marker='o', linestyle='-', color='b', label='Baseload Numbers')
    plt.title('Baseload Numbers for Each Hour of the Day', fontsize=16)
    plt.xlabel('Hour of the Day', fontsize=12)
    plt.ylabel('Baseload Value', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha='right')
    plt.legend()

    for i, value in enumerate(baseload_numbers_list):
        plt.text(hours[i], value, str(value), ha='center', va='bottom', fontsize=9, color='black', weight='bold')

    plt.tight_layout()
    plt.show(block=False)
    