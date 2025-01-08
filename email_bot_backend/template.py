


def email_template(name, property_name, property_address=None):
    first_name = get_first_name(name)
    template = (f"Hi {first_name},"
                f"Hope you’re doing well."
                f"It’s Eric Schwartz from BASE Realty Group."
                f"A client of mine came across your asset, {property_name}."
                f"They asked me to get in touch with you to see if you would entertain an offer on it."
                f"I'm happy to discuss further at your earliest convenience."
    )

    return template


def get_first_name(full_name):
    return full_name.split()[0]
