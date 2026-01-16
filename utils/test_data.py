import faker

fake = faker.Faker()


def generate_test_data():
    return fake.unique.first_name()
