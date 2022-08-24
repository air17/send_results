import json
import smtplib
from email.message import EmailMessage
from typing import Optional
from decouple import config


class EmailHandler:
    """Stores server connection info"""

    def __init__(
        self,
        server: str,
        login: str,
        password: str,
        port: int = 587,
        from_email: Optional[str] = None,
    ):
        """Inits EmailHandler with a data needed for connection"""
        self._server = server
        self._login = login
        self._password = password
        self._port = port
        self._from_email = from_email if from_email else login

    def send_message(self, to: str, text: str, subject: str = "") -> None:
        """Sends an email"""
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self._from_email
        msg["To"] = to
        msg.set_content(text)

        server = smtplib.SMTP(self._server, self._port)
        server.starttls()
        server.login(self._login, self._password)
        server.sendmail(self._from_email, to, msg.as_string())
        server.quit()


class Results:
    """Stores users results info.

    Attributes:
        users: list of users data
    """

    def __init__(self, results_file: str):
        """Inits Results with a provided json file data"""
        with open(results_file, "rb") as json_data:
            self.users: dict = json.load(json_data)

    def send_emails(self, email_handler: EmailHandler) -> None:
        """Sends emails containing results to all the users"""
        for user in self.users:
            email_handler.send_message(
                to=user["email"],
                text=f"Привет, {user.get('name')}, твой результат: {user.get('result')}",
                subject="Результат",
            )


def main():
    email = EmailHandler(
        server=config("EMAIL_SERVER"),
        port=config("EMAIL_PORT", cast=int),
        login=config("EMAIL_LOGIN"),
        password=config("EMAIL_PASSWORD"),
    )
    results = Results("results.json")

    results.send_emails(email)


if __name__ == "__main__":
    main()
