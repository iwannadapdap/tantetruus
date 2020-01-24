import smtplib
import app_config
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_confirmation_mail(name: str, mail: str, token: str):
    message_text = confirmation_text_template.format(
        PERSON_NAME=name, TOKEN=token)

    confirmation_html = confirmation_html_template.format(
        _name=name, _token=token)

    send_email(mail, "Tante truus confirmation email",
               confirmation_html, message_text)


def send_message_mail(name: str, email: str, subject: str, content: str):
    content_text = message_text_template.format(
        PERSON_NAME=name, MESSAGE=content)

    content_html = message_html_template.format(
        _name=name, _message=content)

    send_email(email, subject, content_html, content_text)


def send_email(email, subject, content_html, content_text):
    with smtplib.SMTP(host=app_config.MAIL_SERVER, port=app_config.MAIL_PORT) as s:
        s.starttls()
        s.login(app_config.MAIL_USERNAME, app_config.MAIL_PASSWORD)

        msg = MIMEMultipart("alternative")
        msg["From"] = app_config.MAIL_DEFAULT_SENDER
        msg["To"] = email
        msg["Subject"] = subject

        msg.attach(MIMEText(content_text, 'plain'))
        msg.attach(MIMEText(content_html, 'html'))

        s.send_message(msg)

        del msg

        s.quit()


message_html_template = """\
<body style="background: #F4F4F4;">
    <div class="mj-container" style="background-color:#F4F4F4;">
        <div style="margin:0px auto;max-width:600px;background:#FFFFFF;">
            <table role="presentation" cellpadding="0" cellspacing="0"
                style="font-size:0px;width:100%;background:#FFFFFF;" align="center" border="0">
                <tbody>
                    <tr>
                        <td
                            style="text-align:center;vertical-align:top;direction:ltr;font-size:0px;padding:9px 0px 9px 0px;">
                            <div class="mj-column-per-100 outlook-group-fix"
                                style="vertical-align:top;display:inline-block;direction:ltr;font-size:13px;text-align:left;width:100%;">
                                <table role="presentation" cellpadding="0" cellspacing="0" style="vertical-align:top;"
                                    width="100%" border="0">
                                    <tbody>
                                        <tr>
                                            <td style="word-wrap:break-word;font-size:0px;padding:20px 20px 20px 20px;"
                                                align="center">
                                                <img src="https://tantetruus.ovh/static/img/tantetruus.png">
                                                <div
                                                    style="cursor:auto;color:#000000;font-family:Helvetica, sans-serif;font-size:11px;line-height:1.5;text-align:center;">
                                                    <p><span style="font-size:28px;">Hello {_name},</span></p>
                                                    <p><span style="font-size:28px;">{_message}</span></p>
                                                </div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="word-wrap:break-word;font-size:0px;padding:15px 15px 15px 15px;"
                                                align="center">
                                                <div
                                                    style="cursor:auto;color:#000000;font-family:Ubuntu, Helvetica, Arial, sans-serif;font-size:11px;line-height:1.5;text-align:center;">
                                                    <p><span style="font-size:28px;">Greetings,</span></p>
                                                    <p><span style="font-size:28px;">Tante truus</span></p>
                                                </div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="word-wrap:break-word;font-size:0px;">
                                                <div style="font-size:1px;line-height:50px;white-space:nowrap;">&#xA0;
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</body>

</html>
                        """

confirmation_html_template = """\
<body style="background: #F4F4F4;">
    <div class="mj-container" style="background-color:#F4F4F4;">
        <div style="margin:0px auto;max-width:600px;background:#FFFFFF;">
            <table role="presentation" cellpadding="0" cellspacing="0"
                style="font-size:0px;width:100%;background:#FFFFFF;" align="center" border="0">
                <tbody>
                    <tr>
                        <td
                            style="text-align:center;vertical-align:top;direction:ltr;font-size:0px;padding:9px 0px 9px 0px;">
                            <div class="mj-column-per-100 outlook-group-fix"
                                style="vertical-align:top;display:inline-block;direction:ltr;font-size:13px;text-align:left;width:100%;">
                                <table role="presentation" cellpadding="0" cellspacing="0" style="vertical-align:top;"
                                    width="100%" border="0">
                                    <tbody>
                                        <tr>
                                            <td style="word-wrap:break-word;font-size:0px;padding:20px 20px 20px 20px;"
                                                align="center">
                                                <img src="https://tantetruus.ovh/static/img/tantetruus.png">
                                                <div style="cursor:auto;color:#000000;font-family:Helvetica, sans-serif;font-size:11px;line-height:1.5;text-align:center;">
                                                    <p><span style="font-size:28px;">Hello {_name},</span></p>
                                                    <p><span style="font-size:28px;">Thanks for using our app! Please
                                                            click the link below to confirm your account and complete
                                                            your registration.</span></p>
                                                </div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="word-wrap:break-word;font-size:0px;padding:20px 20px 20px 20px;"
                                                align="center">
                                                <table role="presentation" cellpadding="0" cellspacing="0"
                                                    style="border-collapse:separate;width:auto;" align="center"
                                                    border="0">
                                                    <tbody>
                                                        <tr>
                                                            <td style="border:0px solid #000;border-radius:101px;color:#fff;cursor:auto;padding:14px 40px 14px 40px;"
                                                                align="center" valign="middle" bgcolor="#A62EA9"><a
                                                                    href="https://tantetruus.ovh/auth/confirm/{_token}"
                                                                    style="text-decoration:none;background:#A62EA9;color:#fff;font-family:Ubuntu, Helvetica, Arial, sans-serif, Helvetica, Arial, sans-serif;font-size:20px;font-weight:normal;line-height:120%;text-transform:none;margin:0px;"
                                                                    target="_blank">Confirm my account!</a></td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="word-wrap:break-word;font-size:0px;padding:15px 15px 15px 15px;"
                                                align="center">
                                                <div
                                                    style="cursor:auto;color:#000000;font-family:Ubuntu, Helvetica, Arial, sans-serif;font-size:11px;line-height:1.5;text-align:center;">
                                                    <p><span style="font-size:28px;">Greetings,</span></p>
                                                    <p><span style="font-size:28px;">Tante truus</span></p>
                                                </div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="word-wrap:break-word;font-size:0px;">
                                                <div style="font-size:1px;line-height:50px;white-space:nowrap;">&#xA0;
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</body>

</html>
                        """

confirmation_text_template = """
Dear ${PERSON_NAME}, 

Please click the following link to confirm your account:
https://tantetruus.ovh/auth/confirm/${TOKEN}

Greetings,

Tante Truus
"""

message_text_template = """
Dear ${PERSON_NAME}, 

${MESSAGE}

Greetings,

Tante Truus
"""
