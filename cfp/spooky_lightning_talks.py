from email.headerregistry import Address
from email.message import EmailMessage
from typing import List, NamedTuple
import csv
import os
import smtplib


EMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS", None)
EMAIL_PASSWORD = os.getenv("GMAIL_APPLICATION_PASSWORD", None)


class Proposal(NamedTuple):
    ts: str
    email: str
    name: str
    talk_title: str
    talk_description: str
    bio: str


def read_in_accepted_proposals(filename: str) -> List[Proposal]:
    accepted_proposals = []
    with open(filename, "r") as f:
        rows = csv.reader(f, delimiter=",")
        for row in rows:
            accepted_proposals.append(Proposal(*row))
    return accepted_proposals


def structure_accepted_proposals(proposals):
    collected_proposals = []
    for proposal in proposals:
        args = proposal.split(",")
        new_proposal = Proposal(*args)
        collected_proposals.append(new_proposal)
    return collected_proposals


def draft_acceptance_email(proposal: Proposal):
    # Recipent
    username, domain = proposal.email.split("@")
    to_address = (
        Address(display_name=proposal.name, username=username, domain=domain),
    )
    return create_email_message(
        from_address=EMAIL_ADDRESS,
        to_address=to_address,
        subject="Chicago Python presents Spooky Lightning Talk Status",
        body=f"""Hi {proposal.name.split(" ")[0]},

Congratulations! Your submitted talk, {proposal.talk_title}, was accepted for Spooky Lightning Talks night on Wednesday, October 30th.

Please reply to this email to confirm you will be able to present your 5 minute talk.

I have secured equipment and will be recording each session for upload to the ChiPy YouTube channel.

Best Regards,
Aly Sivji"""
    )


def create_email_message(from_address, to_address, subject, body):
    msg = EmailMessage()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.set_content(body)
    return msg


def send_email(message):
    with smtplib.SMTP("smtp.gmail.com", port=587) as smtp_server:
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp_server.send_message(msg)
    return True


if __name__ == "__main__":
    proposals = read_in_accepted_proposals("cfp/input.txt")
    for proposal in proposals:
        # print(proposal.name)
        # msg = draft_acceptance_email(proposal)
        # # send_email(msg)
        # print("Email sent!\n")

        print(proposal.talk_title)
        print(f"by {proposal.name}")
        print()
        print(proposal.talk_description)
        print()
        print("-------\n")
