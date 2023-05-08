# FILE-TRACKING-AND-WORKFLOW-MANAGEMENT-StreamLit-App

This is a Streamlit app for QR code scanning and authentication. Here's how the app works:

The user is prompted to enter their username and password for authentication.
Upon successful authentication, the user is directed to the main app screen where they can scan a QR code using their device camera.
The captured image is then decoded using OpenCV and the decoded data is displayed on the screen.
The decoded data is then saved along with the user's name and the current date and time in an Excel sheet named "datasheet.xlsx".
