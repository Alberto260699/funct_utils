import simpy

def customer(env, name, counter, service_time):
    print(f"{name} arrives at the counter at {env.now}")
    with counter.request() as request:
        yield request
        print(f"{name} starts being served at {env.now}")
        yield env.timeout(service_time)
        print(f"{name} leaves the counter at {env.now}")

# Simulation setup
env = simpy.Environment()
counter = simpy.Resource(env, capacity=1)  # Single server
env.process(customer(env, "Customer 1", counter, 5))
env.process(customer(env, "Customer 2", counter, 3))
env.run(until=15)
