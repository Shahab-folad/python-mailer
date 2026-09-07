import smtplib
import re
import html
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr


# ============================================================
#                  YOUR GMAIL CONFIGURATION
# ============================================================
#
# PUT YOUR INFORMATION HERE
#
# IMPORTANT:
# Use a Google App Password, NOT your normal Gmail password.
#
# ============================================================

GMAIL_ADDRESS = ""

GMAIL_APP_PASSWORD = ""

SENDER_NAME = ""


# ============================================================
#                     EMAIL HTML DESIGN
# ============================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{subject}}</title>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">

    <style>
        /* ---------- Reset & Base ---------- */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            margin: 0;
            padding: 0;
            background: #eef2f7;
            font-family: 'Poppins', Arial, Helvetica, sans-serif;
            -webkit-font-smoothing: antialiased;
        }

        .wrapper {
            width: 100%;
            padding: 30px 15px;
            background: linear-gradient(135deg, #eef2f7 0%, #d9e2ef 100%);
        }

        .container {
            max-width: 620px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 24px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0, 20, 40, 0.12);
        }

        /* ---------- Header ---------- */
        .header {
            background: linear-gradient(135deg, #1a2a6c, #4a6cf7, #6a3de8);
            padding: 40px 20px 32px;
            text-align: center;
            position: relative;
        }

        .header::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 6px;
            background: linear-gradient(90deg, #f9d423, #f7971e);
        }

        .logo {
            color: #ffffff;
            font-size: 28px;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }

        .logo span {
            display: inline-block;
            animation: pulse 2.5s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.04); }
            100% { transform: scale(1); }
        }

        .header-sub {
            color: rgba(255,255,255,0.85);
            font-size: 14px;
            font-weight: 300;
            margin-top: 6px;
            letter-spacing: 0.3px;
        }

        /* ---------- Content ---------- */
        .content {
            padding: 36px 30px 28px;
        }

        h1 {
            margin: 0 0 8px 0;
            color: #1a2a6c;
            font-size: 30px;
            font-weight: 700;
            line-height: 1.2;
        }

        h1 small {
            font-weight: 400;
            color: #4a6cf7;
        }

        .greeting {
            color: #4b5563;
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 24px;
            border-left: 4px solid #4a6cf7;
            padding-left: 16px;
            background: #f8faff;
            border-radius: 0 8px 8px 0;
        }

        .message {
            margin: 28px 0;
            padding: 20px 22px;
            background: #f9fcff;
            border-radius: 16px;
            border: 1px solid #e6edf6;
            color: #1e293b;
            font-size: 16px;
            line-height: 1.8;
            white-space: pre-wrap;
            box-shadow: 0 2px 8px rgba(74, 108, 247, 0.06);
        }

        .message strong {
            color: #1a2a6c;
        }

        .email-box {
            margin: 20px 0 24px;
            padding: 14px 20px;
            background: #f0f5ff;
            border-radius: 12px;
            display: inline-block;
            border: 1px solid #d6e0f5;
            color: #1a2a6c;
            font-size: 15px;
        }

        .email-box strong {
            font-weight: 600;
        }

        .cta-button {
            display: inline-block;
            margin: 8px 0 12px;
            padding: 14px 36px;
            background: linear-gradient(135deg, #4a6cf7, #6a3de8);
            color: #ffffff !important;
            font-weight: 600;
            font-size: 16px;
            text-decoration: none;
            border-radius: 50px;
            box-shadow: 0 6px 18px rgba(74, 108, 247, 0.3);
            transition: all 0.2s ease;
            letter-spacing: 0.3px;
        }

        .cta-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 28px rgba(74, 108, 247, 0.4);
        }

        .signoff {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #eef2f7;
            color: #4b5563;
            font-size: 16px;
        }

        .signoff strong {
            color: #1a2a6c;
            font-weight: 600;
        }

        /* ---------- Footer ---------- */
        .footer {
            background: #f8faff;
            padding: 30px 20px 24px;
            text-align: center;
            border-top: 1px solid #e6edf6;
        }

        .social-icons {
            margin-bottom: 16px;
            font-size: 24px;
            letter-spacing: 12px;
        }

        .social-icons a {
            color: #4a6cf7;
            text-decoration: none;
            transition: color 0.2s;
        }

        .social-icons a:hover {
            color: #1a2a6c;
        }

        .footer p {
            margin: 6px 0;
            font-size: 13px;
            color: #9ca3af;
            line-height: 1.5;
        }

        .footer p:last-child {
            margin-top: 10px;
            font-size: 12px;
            color: #b0b8c4;
        }

        /* ---------- Responsive ---------- */
        @media (max-width: 500px) {
            .wrapper { padding: 15px 10px; }
            .content { padding: 24px 18px; }
            .header { padding: 30px 15px 24px; }
            .logo { font-size: 22px; }
            h1 { font-size: 24px; }
            .message { padding: 16px; font-size: 15px; }
            .cta-button { padding: 12px 28px; font-size: 15px; }
        }
    </style>
</head>

<body>
    <div class="wrapper">
        <div class="container">

            <!-- HEADER -->
            <div class="header">
                <div class="logo">
                    <span>✨ Naqeebullah Shirzai</span>
                </div>
                <div class="header-sub">Building the future, one email at a time</div>
            </div>

            <!-- EMAIL CONTENT -->
            <div class="content">
                <h1>
                    Hello {{name}} 👋
                </h1>

                <div class="greeting">
                    We hope this email finds you well. Here's a message just for you:
                </div>

                <div class="message">
                    {{content}}
                </div>

                <div class="email-box">
                    <strong>📬 Recipient:</strong> {{email}}
                </div>

                <!-- Optional Call-to-Action (you can remove if not needed) -->
                

                <div class="signoff">
                    Thank you for your time,<br>
                    <strong>{{sender_name}}</strong>
                </div>
            </div>

            <!-- FOOTER -->
            <div class="footer">
                <div class="social-icons">
                    <a href="#">🐦</a>
                    <a href="#">📘</a>
                    <a href="#">📸</a>
                    <a href="#">🔗</a>
                </div>
                <p>© 2026 My Company · All rights reserved</p>
                <p>This email was sent to {{email}}</p>
                <p>If you no longer wish to receive these emails, <a href="#" style="color:#4a6cf7; text-decoration:underline;">unsubscribe</a>.</p>
            </div>

        </div>
    </div>
</body>
</html>
"""


# ============================================================
#                     TEMPLATE ENGINE
# ============================================================

def render_template(template, data):

    def replace_variable(match):

        key = match.group(1).strip()

        value = data.get(key)

        if value is None:
            return match.group(0)

        return str(value)

    return re.sub(
        r"\{\{\s*(.*?)\s*\}\}",
        replace_variable,
        template
    )


# ============================================================
#                     GMAIL MAILER
# ============================================================

class GmailMailer:

    def __init__(self):

        self.email = GMAIL_ADDRESS

        self.password = GMAIL_APP_PASSWORD

        self.sender_name = SENDER_NAME

        self.smtp_server = "smtp.gmail.com"

        self.smtp_port = 587


    def send(
        self,
        recipient,
        recipient_name,
        subject,
        content
    ):

        # ----------------------------------------------------
        # Escape user input for safe HTML
        # ----------------------------------------------------

        safe_name = html.escape(
            recipient_name
        )

        safe_email = html.escape(
            recipient
        )

        safe_subject = html.escape(
            subject
        )

        safe_content = html.escape(
            content
        )

        safe_sender_name = html.escape(
            self.sender_name
        )


        # ----------------------------------------------------
        # Template data
        # ----------------------------------------------------

        data = {

            "name": safe_name,

            "email": safe_email,

            "subject": safe_subject,

            "content": safe_content,

            "sender_name": safe_sender_name

        }


        # ----------------------------------------------------
        # Generate HTML
        # ----------------------------------------------------

        html_body = render_template(
            HTML_TEMPLATE,
            data
        )


        # ----------------------------------------------------
        # Create email
        # ----------------------------------------------------

        message = MIMEMultipart(
            "alternative"
        )


        message["From"] = formataddr(
            (
                self.sender_name,
                self.email
            )
        )


        if recipient_name:

            message["To"] = formataddr(
                (
                    recipient_name,
                    recipient
                )
            )

        else:

            message["To"] = recipient


        message["Subject"] = subject


        # ----------------------------------------------------
        # Plain-text fallback
        # ----------------------------------------------------

        plain_text = f"""
Hello {recipient_name},

{content}

Thank you,
{self.sender_name}
"""


        message.attach(
            MIMEText(
                plain_text,
                "plain",
                "utf-8"
            )
        )


        # ----------------------------------------------------
        # HTML email
        # ----------------------------------------------------

        message.attach(
            MIMEText(
                html_body,
                "html",
                "utf-8"
            )
        )


        # ----------------------------------------------------
        # Gmail SMTP
        # ----------------------------------------------------

        with smtplib.SMTP(
            self.smtp_server,
            self.smtp_port
        ) as server:

            server.ehlo()

            server.starttls()

            server.ehlo()

            server.login(
                self.email,
                self.password
            )

            server.sendmail(
                self.email,
                recipient,
                message.as_string()
            )


# ============================================================
#                     CLI FUNCTIONS
# ============================================================

def print_header():

    print()

    print("=" * 60)

    print("                 PYTHON HTML MAILER")

    print("=" * 60)

    print()

    print(
        "Sender:",
        GMAIL_ADDRESS
    )

    print()


def ask_required(question):

    while True:

        value = input(
            question
        ).strip()

        if value:

            return value

        print(
            "This field is required."
        )


def ask_content():

    print()

    print("-" * 60)

    print("Enter your email content.")

    print()

    print(
        "You can enter multiple lines."
    )

    print()

    print(
        "Type END on a new line when finished."
    )

    print("-" * 60)

    print()

    lines = []

    while True:

        line = input()

        if line.strip() == "END":

            break

        lines.append(line)

    return "\n".join(lines)


# ============================================================
#                     PREVIEW
# ============================================================

def show_preview(
    recipient,
    recipient_name,
    subject,
    content
):

    print()

    print("=" * 60)

    print("                      PREVIEW")

    print("=" * 60)

    print()

    print(
        "From:",
        GMAIL_ADDRESS
    )

    print(
        "To:",
        recipient
    )

    print(
        "Name:",
        recipient_name
    )

    print(
        "Subject:",
        subject
    )

    print()

    print("-" * 60)

    print(content)

    print("-" * 60)

    print()


# ============================================================
#                     MAIN PROGRAM
# ============================================================

def main():

    print_header()


    # --------------------------------------------------------
    # Recipient
    # --------------------------------------------------------

    recipient = ask_required(
        "Recipient email: "
    )


    recipient_name = input(
        "Recipient name: "
    ).strip()


    subject = ask_required(
        "Subject: "
    )


    # --------------------------------------------------------
    # Content
    # --------------------------------------------------------

    content = ask_content()


    if not content.strip():

        print()

        print(
            "ERROR: Content cannot be empty."
        )

        return


    # --------------------------------------------------------
    # Preview
    # --------------------------------------------------------

    show_preview(
        recipient,
        recipient_name,
        subject,
        content
    )


    # --------------------------------------------------------
    # Confirmation
    # --------------------------------------------------------

    answer = input(
        "Send email? [y/N]: "
    ).strip().lower()


    if answer != "y":

        print()

        print(
            "Email cancelled."
        )

        return


    # --------------------------------------------------------
    # Send
    # --------------------------------------------------------

    print()

    print(
        "Sending email..."
    )


    try:

        mailer = GmailMailer()


        mailer.send(

            recipient=recipient,

            recipient_name=recipient_name,

            subject=subject,

            content=content

        )


        print()

        print("=" * 60)

        print(
            "             EMAIL SENT SUCCESSFULLY ✓"
        )

        print("=" * 60)

        print()


    except smtplib.SMTPAuthenticationError:

        print()

        print(
            "ERROR: Gmail authentication failed."
        )

        print()

        print(
            "Check your Gmail address and App Password."
        )

        print()

        print(
            "Remember: use a Google App Password,"
        )

        print(
            "not your normal Gmail password."
        )

        print()


    except smtplib.SMTPException as error:

        print()

        print(
            "Gmail SMTP error:"
        )

        print(error)

        print()


    except Exception as error:

        print()

        print(
            "ERROR:"
        )

        print(error)

        print()


# ============================================================
#                     START PROGRAM
# ============================================================

if __name__ == "__main__":

    main()
