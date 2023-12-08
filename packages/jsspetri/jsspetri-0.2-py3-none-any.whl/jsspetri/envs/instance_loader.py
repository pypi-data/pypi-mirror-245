import os
import pandas as pd


def load_instance(instance_id):
    """
    Load instance data from a file.

    Parameters:
        instance_id (str): The ID of the instance to be loaded.

    Returns:
        tuple: A tuple containing a DataFrame representing the instance and a specification tuple.
    """
    instance_path = os.path.join(os.path.dirname(__file__), "instances", instance_id)
    instance = pd.DataFrame()
    data = []

    try:
        with open(instance_path, 'r') as file:
            for line in file:
                elements = line.strip().split()
                data.append(elements)
            print(f"Instance '{instance_id}' is loaded.")
    except FileNotFoundError:
        print(f"The file '{instance_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    raw_instance = pd.DataFrame(data).fillna(0).drop(0)
    raw_instance = raw_instance.apply(pd.to_numeric, errors='coerce')

    # get the maximum number of operations/tokens
    max_bound = max([len(row) for row in raw_instance.values])
    max_bound = raw_instance.values.max().max()

    for i in range(0, raw_instance.shape[1], 2):
        machine = raw_instance.columns[i]
        time = raw_instance.columns[i + 1]
        machine_time = f" {int(i/2)}"
        instance[machine_time] = list(zip(raw_instance[machine], raw_instance[time]))

    n_jobs = instance.shape[0]
    n_machines = instance.shape[1]

    specification = (n_jobs, n_machines, max_bound)

    print(instance)

    return instance, specification


# %% Test
if __name__ == "__main__":
    load_instance("ta01")


    




