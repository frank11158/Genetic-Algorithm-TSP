import random
import sys

def parse_args():
    if len(sys.argv) != 2:
        raise Exception("Invalid arguments.")

    num_cities = int(sys.argv[1])
    return num_cities

def write_output(cities):
    try:
        with open(f"./tests/input_{len(cities)}.txt", 'w') as output_file:
            output_file.write(f'{len(cities)}\n')
            for city in cities:
                output_file.write(f'{city[0]} {city[1]} {city[2]}\n')
            output_file.close()
    except Exception as e:
        print("Failed to write to output file: ", e)
        exit()

def main():
    num_cities = parse_args()
    cities = []
    
    for _ in range(num_cities):
        x = int(random.random() * 200)
        y = int(random.random() * 200)
        z = int(random.random() * 200)
        cities.append((x, y, z))

    write_output(cities)


if __name__ == "__main__":
    main()