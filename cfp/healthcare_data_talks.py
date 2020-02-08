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
    organization: str
    twitter: str
    talk_title: str
    talk_description: str
    bio: str
    notes: str
    agree_to_coc: str
    consent_to_film: str
    pronouns: str


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
        subject="Python Powered Healthcare: Talk Accepted",
        body=f"""Hi {proposal.name.split(" ")[0]},

Congratulations! Your submitted talk, {proposal.talk_title}, was accepted for Python Powered Healthcare Night on Wednesday, February 19th.

Please reply to this email to confirm you will be able to attend and present your lightning talk.

Details about the event can be found on https://www.meetup.com/_ChiPy_/events/267264866/. Apologies if your talk description was shortened. Meetup has a character limit for the event description.

Please make sure to RSVP to ensure we have an accurate headcount.

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
    proposals = read_in_accepted_proposals("cfp/healthcare_data_talks.txt")
    for proposal in proposals:
        # print(proposal.name)
        # msg = draft_acceptance_email(proposal)
        # # send_email(msg)
        # print("Email sent!\n")

        print(proposal.talk_title)
        print(f"by {proposal.name}, {proposal.organization}")
        print()
        print(proposal.talk_description)
        print()
        print("-------\n")
