import random
import numpy as np
import math

init_pop = 1000
TRUE_VAL = random.gauss(0, 2)


def populate(pop=100):
    people = []
    for i in range(pop):
        people.append(gen_person(ID=i))
    return people


def make_groups(people, loc_trans=0.1, idea_trans=0.1):
    mles = [mle(person["beliefs"]) for person in people]
    for person in people:
        person["connections"] = []
        for other in [a for a in people if a["ID"] != person["ID"]]:
            spat_dist = np.linalg.norm(person["loc"] - other["loc"])
            idea_dist = abs(mles[person["ID"]] - mles[other["ID"]])
            logit = -np.log(1 / (loc_trans * spat_dist) + 1 / (idea_dist + idea_trans))
            if np.random.uniform(0, 1) > 1 / (1 + math.e ** (logit)):
                person["connections"].append(other["ID"])
    return people


def gen_person(ID):
    person = {}
    person["loc"] = np.random.uniform(0, 1, 2)
    person["ID"] = ID
    person["beliefs"] = [(0, random.gauss(0, 1))]
    return person


def info_event(ident, people, true_val, virality=0.6):
    info_val = true_val + random.gauss(0, 1)
    init_person = random.choice(people)
    gone_through = []
    queue = [init_person["ID"]]
    while True:
        share = people[queue.pop(0)]
        cons = [p for p in people if p["ID"] in share["connections"]]
        for p in cons:
            if (
                p["ID"] not in queue
                and p["ID"] not in gone_through
                and random.random() < virality
            ):
                queue.append(p["ID"])
        gone_through.append(share["ID"])
        if not queue:
            break
    for person in [people[i] for i in gone_through]:
        person["beliefs"].append((ident, info_val))
    print(len(gone_through))
    return people


def mle(beliefs):
    values = [a[1] for a in beliefs]
    return np.mean(values)


if __name__ == "__main__":
    people = populate(pop=init_pop)
    people = make_groups(people)
    print("Groups Generated.")
    group_sizes = [len(person["connections"]) for person in people]
    average_connections = np.mean(group_sizes)
    print(f"Average number of connections: {average_connections}")
    for i in range(0, 20):
        people = info_event(1, people, 2, virality=i / 20)
        people = make_groups(people)
