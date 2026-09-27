from flask import Flask, request, jsonify, send_from_directory
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv


# ---------------------------------------------------------
# BASE DIRECTORY
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------

load_dotenv(os.path.join(BASE_DIR, ".env"))


# ---------------------------------------------------------
# FLASK APP
# ---------------------------------------------------------

app = Flask(__name__, static_folder=BASE_DIR)


# ---------------------------------------------------------
# SERVE PROFILE IMAGE
# ---------------------------------------------------------

@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(
        os.path.join(BASE_DIR, "images"),
        filename
    )


# ---------------------------------------------------------
# OPEN YOUR PORTFOLIO
# ---------------------------------------------------------

@app.route("/")
def home():
    return send_from_directory(
        BASE_DIR,
        "index.html"
    )


# ---------------------------------------------------------
# CONTACT FORM
# ---------------------------------------------------------

@app.route("/api/contact", methods=["POST"])
def contact():

    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    sender_email = data.get("email", "").strip()
    subject = data.get("subject", "").strip()
    message = data.get("message", "").strip()


    # -----------------------------------------------------
    # CHECK FORM FIELDS
    # -----------------------------------------------------

    if not name:
        return jsonify({
            "success": False,
            "message": "Please enter your name."
        }), 400

    if not sender_email:
        return jsonify({
            "success": False,
            "message": "Please enter your email."
        }), 400

    if not subject:
        return jsonify({
            "success": False,
            "message": "Please enter a subject."
        }), 400

    if not message:
        return jsonify({
            "success": False,
            "message": "Please enter your message."
        }), 400

    if "@" not in sender_email:
        return jsonify({
            "success": False,
            "message": "Please enter a valid email address."
        }), 400


    # -----------------------------------------------------
    # GMAIL SMTP SETTINGS
    # -----------------------------------------------------

    smtp_host = os.getenv(
        "SMTP_HOST",
        "smtp.gmail.com"
    )

    smtp_port = int(
        os.getenv(
            "SMTP_PORT",
            "587"
        )
    )

    smtp_user = os.getenv(
        "SMTP_USER",
        ""
    ).strip()

    smtp_password = os.getenv(
        "SMTP_PASSWORD",
        ""
    ).replace(" ", "").strip()

    recipient = os.getenv(
        "CONTACT_TO",
        "kaviyasarumathi@gmail.com"
    ).strip()


    # -----------------------------------------------------
    # CHECK EMAIL CONFIGURATION
    # -----------------------------------------------------

    if not smtp_user or not smtp_password:

        print("ERROR: SMTP_USER or SMTP_PASSWORD is missing.")

        return jsonify({
            "success": False,
            "message": "Email delivery is not configured."
        }), 503


    # -----------------------------------------------------
    # PRINT SAFE EMAIL DEBUG INFORMATION
    # -----------------------------------------------------

    print("")
    print("==========================================")
    print("PORTFOLIO CONTACT FORM")
    print("==========================================")
    print("SMTP HOST:", smtp_host)
    print("SMTP PORT:", smtp_port)
    print("SMTP USER:", smtp_user)
    print("EMAIL TO:", recipient)
    print("REPLY TO:", sender_email)
    print("SUBJECT:", subject)
    print("==========================================")


    # -----------------------------------------------------
    # CREATE EMAIL
    # -----------------------------------------------------

    email = EmailMessage()

    email["Subject"] = (
        "Portfolio Contact: " + subject
    )

    email["From"] = smtp_user

    email["To"] = recipient

    email["Reply-To"] = sender_email

    email.set_content(
        f"""
You received a new message from your portfolio website.

--------------------------------------------------

Name:
{name}

Email:
{sender_email}

Subject:
{subject}

--------------------------------------------------

Message:

{message}

--------------------------------------------------

This message was sent through the
SARUMATHI A Portfolio contact form.
"""
    )


    # -----------------------------------------------------
    # SEND EMAIL THROUGH GMAIL
    # -----------------------------------------------------

    try:

        print("Connecting to Gmail SMTP...")

        with smtplib.SMTP(
            smtp_host,
            smtp_port,
            timeout=30
        ) as server:

            server.set_debuglevel(1)

            print("Connected to Gmail SMTP.")

            server.ehlo()

            print("Starting TLS...")

            server.starttls()

            server.ehlo()

            print("Logging into Gmail...")

            server.login(
                smtp_user,
                smtp_password
            )

            print("Gmail login successful.")

            print("Sending email...")

            result = server.send_message(email)

            print("Gmail SMTP send result:", result)

            print("EMAIL ACCEPTED BY GMAIL SMTP.")

            print("==========================================")
            print("MESSAGE SENT SUCCESSFULLY")
            print("==========================================")
            print("")


        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        return jsonify({
            "success": True,
            "message": "Message sent successfully."
        }), 200


    # -----------------------------------------------------
    # GMAIL AUTHENTICATION ERROR
    # -----------------------------------------------------

    except smtplib.SMTPAuthenticationError as error:

        print("")
        print("==========================================")
        print("GMAIL AUTHENTICATION ERROR")
        print("==========================================")
        print(error)
        print("==========================================")
        print("")

        return jsonify({
            "success": False,
            "message": (
                "Gmail authentication failed. "
                "Please check your Gmail App Password."
            )
        }), 502


    # -----------------------------------------------------
    # RECIPIENT ERROR
    # -----------------------------------------------------

    except smtplib.SMTPRecipientsRefused as error:

        print("")
        print("==========================================")
        print("GMAIL RECIPIENT ERROR")
        print("==========================================")
        print(error)
        print("==========================================")
        print("")

        return jsonify({
            "success": False,
            "message": (
                "Gmail rejected the recipient address."
            )
        }), 502


    # -----------------------------------------------------
    # OTHER SMTP ERROR
    # -----------------------------------------------------

    except smtplib.SMTPException as error:

        print("")
        print("==========================================")
        print("GMAIL SMTP ERROR")
        print("==========================================")
        print(error)
        print("==========================================")
        print("")

        return jsonify({
            "success": False,
            "message": (
                "Gmail could not send the message. "
                "Please try again later."
            )
        }), 502


    # -----------------------------------------------------
    # GENERAL ERROR
    # -----------------------------------------------------

    except Exception as error:

        print("")
        print("==========================================")
        print("EMAIL ERROR")
        print("==========================================")
        print(error)
        print("==========================================")
        print("")

        return jsonify({
            "success": False,
            "message": (
                "The message could not be delivered. "
                "Please try again later."
            )
        }), 502


# ---------------------------------------------------------
# START SERVER
# ---------------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )