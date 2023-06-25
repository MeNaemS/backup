class Checker:
    def __init__(self, value: str):
        from email_validator.exceptions_types import EmailSyntaxError

        self.value = value
        self.boolean = False
        try:
            self.email
        except EmailSyntaxError:
            self.phone_number

    @property
    def email(self) -> bool:
        from email_validator import validate_email

        self.boolean = True if validate_email(self.value) else False

    @property
    def phone_number(self) -> bool:
        self.value = list(self.value)
        intersection = set([chr(j) for j in range(97, 123)]).intersection(set(self.value))
        if intersection != set(): self.boolean = False
        else:
            intersection = {'+', '(', ')', '-'}.intersection(set(self.value))
            if intersection != set():
                for inter in intersection:
                    while inter in self.value:
                        self.value.remove(inter)
            self.boolean = True if self.value.__len__() == 11 else False
