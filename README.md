# SARUMATHI A — Portfolio

## Run locally
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. `python -m venv .venv`
4. Activate it:
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
5. `pip install -r requirements.txt`
6. `python app.py`
7. Open `http://127.0.0.1:5000`

## Contact form
The contact form sends messages to `kaviyasarumathi@gmail.com` through FormSubmit. The first submission may require one-time email activation by the FormSubmit service.

The bundled Flask backend remains available at `/api/contact` for deployments that configure SMTP credentials.

## Certificates
The first two certificate buttons open the supplied Google Drive files directly. The third program entry does not show a broken certificate link because no certificate URL was supplied.

The uploaded resume is included as `SARUMATHI_A_Resume.pdf` and is used by the Resume and Download Resume buttons.
