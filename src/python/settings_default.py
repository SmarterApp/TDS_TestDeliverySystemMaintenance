# Copy to settings_secret.py, set strict permissions, and modify.
# DO NOT PUT THE SECRET FILE IN SOURCE CONTROL!

ENDPOINT = "http://localhost:8080/proctor/Services/exams/expire/"
CLIENT_NAME = "SBAC_PT"
SSL_CHECKS = True  # Set False for dev servers with invalid SSL. KEEP True FOR PROD!

# The AUTH settings are related to your OpenAM server setup (not Proctor itself).
AUTH_ENDPOINT = "https://your-sso-server.example.com/auth/oauth2/access_token?realm=/your_realm"
AUTH_PAYLOAD = {
    "client_id": "your_client_id",
    "client_secret": "your_secret",
    "grant_type": "password",
    "password": "your_password",
    "username": "your_user@example.com"
}
