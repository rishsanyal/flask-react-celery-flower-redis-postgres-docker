import random

# List of possible names and email domains
names = [ 'tiya', 'piya', 'riya', 'chana']
domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com']

def generate_users() -> list:
    """Generate mock user data for testing purposes"""

    users = []
    for i in range(4):
        # Generate a random username and password
        username = names[i].lower() + str(random.randint(100, 999))
        pwd = 'password' + str(random.randint(100, 999))

        # Generate a random full name, email, and phone number
        full_name = names[i] + ' Doe'
        email = username + '@' + random.choice(domains)
        phone = '+1-555-' + str(random.randint(100, 999)) + '-' + str(random.randint(1000, 9999))

        # Create a dictionary representing the user profile
        user_data = {
            'username': username,
            'pwd': pwd,
            'profile': {
                'full_name': full_name,
                'email': email,
                'phone': phone
            }
        }

        # Add the user data to the list of users
        users.append(user_data)

    return users