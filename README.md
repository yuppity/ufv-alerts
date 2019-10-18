# ufv-alerts

![Alert flow](docs/ufv-alerts.png)

Relay UniFi Video notifications to various destinations.

Acts as a SMTP server that you point UniFi Video server to. Notifications will be received as emails and the associated snapshot, along with the email body, will be passed on for further processing and will eventually be handled by one or more output modules that will send the processed event to outside services. Outside services can be Slack, Telegram, IRC, or anything that can talk via a socket.

**CAUTION: this is work in progress and might never progress beyond the quick test that it is atm.**
