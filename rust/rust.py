class User:
    def __init__(self, name: str) -> None:
        self.name = name
        self.email = name + "@bindsoft.co.kr"

    def send_email(self, message: str) -> None:
        print(f"Sending email to {self.name} <{self.email}>")
        # Send the email here


def main() -> None:
    print("Hello, World!")


if __name__ == "__main__":
    main()
