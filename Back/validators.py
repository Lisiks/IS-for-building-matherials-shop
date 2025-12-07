def inn_validation(inn_number) -> bool:
    return inn_number.isdigit() and len(inn_number) == 10


def ogrn_validation(ogrn_number) -> bool:
    return ogrn_number.isdigit() and len(ogrn_number) == 13


def email_validation(email) -> bool:
    return (5 <= len(email) <= 30) and (email.count("@") == 1)


def telephone_validation(telephone_number) -> bool:
    telephone_component_list = telephone_number.strip().split("-")
    return (
            len(telephone_component_list) == 5 and
            (telephone_component_list[0].isdigit() and 1 <= len(telephone_component_list[0]) <= 3) and
            (telephone_component_list[1].isdigit() and len(telephone_component_list[1]) == 3) and
            (telephone_component_list[2].isdigit() and len(telephone_component_list[2]) == 3) and
            (telephone_component_list[3].isdigit() and len(telephone_component_list[3]) == 2) and
            (telephone_component_list[4].isdigit() and len(telephone_component_list[4]) == 2)
    )


def article_validation(article) -> bool:
    return len(article) == 10 and article.isdigit()

def client_card_validation(card) -> bool:
    return len(card) == 10 and card.isdigit()


def float_validation(attribute) -> bool:
    try:
        float(attribute)
    except ValueError:
        return False
    return True
