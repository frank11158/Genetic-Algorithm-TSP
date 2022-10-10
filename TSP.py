from GeneticAlgorithm import GA
import matplotlib.pyplot as plt
import math
import time

class City:
    def __init__(self, id, x, y, z):
        self.id = id
        self.x = x
        self.y = y
        self.z = z

    def distance(self, dest_city):
        x_diff = abs(self.x - dest_city.x)
        y_diff = abs(self.y - dest_city.y)
        z_diff = abs(self.z - dest_city.z)
        distance = math.sqrt((x_diff)**2 + (y_diff)**2 + (z_diff)**2)
        return distance

def plot(progress):
    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.show()

def write_output(shortest_route):
    try:
        with open("./output.txt", 'w') as output_file:
            for city in shortest_route:
                output_file.write(f'{city.x} {city.y} {city.z}\n')
            first_city = shortest_route[0]
            output_file.write(f'{first_city.x} {first_city.y} {first_city.z}')
            output_file.close()
    except Exception as e:
        print("Failed to write to output file: ", e)
        exit()

def read_input():
    try:
        with open("./tests/input6.txt") as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            file.close()
            return lines            
    except Exception as e:
        print("Invalid input format or failed to open file: ", e)
        exit()

def process_input(lines):
    city_list = []
    for i in range(1, len(lines)):
        cords = lines[i].split()
        if len(cords) != 3:
            continue
        city = create_city(i, cords)
        city_list.append(city)
    return city_list

def create_city(id, cords):
    x = int(cords[0])
    y = int(cords[1])
    z = int(cords[2])
    return City(id, x, y, z)

def execute_ga(num_cities, city_list):
    # if num_cities > 400:
    #     ga = GA(city_list, 
    #             pop_size=60, 
    #             elite_size=30, 
    #             generations=40*len(city_list),
    #             early_stop=50)
    # elif num_cities > 300:
    #     ga = GA(city_list, 
    #             pop_size=80, 
    #             elite_size=40, 
    #             generations=40*len(city_list),
    #             early_stop=50)
    # elif num_cities > 200:
    #     ga = GA(city_list, 
    #             pop_size=100, 
    #             elite_size=50, 
    #             generations=40*len(city_list),
    #             early_stop=50)
    # elif num_cities >= 100:
    #     ga = GA(city_list, 
    #             pop_size=150, 
    #             elite_size=80, 
    #             generations=40*len(city_list),
    #             early_stop=80)
    # elif num_cities > 50:
    #     ga = GA(city_list, 
    #             pop_size=200, 
    #             elite_size=100, 
    #             generations=40*len(city_list),
    #             early_stop=80)
    # else:
    #     ga = GA(city_list, 
    #             pop_size=200, 
    #             elite_size=100, 
    #             generations=40*len(city_list),
    #             pop_growth=True,
    #             early_stop=100)

    ga = GA(city_list, 
            pop_size=100, 
            elite_size=50, 
            generations=60*len(city_list),
            early_stop=-1)

    results = ga.execute()
    return results.fittest_genome(), results.best_fitness(), results.get_progress()


def main():
    lines = read_input()
    num_cities = int(lines[0])
    city_list = process_input(lines)
    
    print(f"Start finding shortest path within {num_cities} cities...")

    start_time = time.time()
    shortest_route, fitness, progress = execute_ga(num_cities, city_list)
    write_output(shortest_route)
    duration = time.time() - start_time

    print("Done!")
    print("Best round shortest path: ", 1/fitness)
    print("Execution time:", duration)

    plot(progress)


if __name__ == "__main__":
    main()