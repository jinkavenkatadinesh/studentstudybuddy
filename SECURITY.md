# Security Policy 🔒

We take security seriously and want to keep **Student Study Buddy** safe for everyone.

---

## ⚠️ API Key Safety
When utilizing cloud providers (**OpenAI** or **Google Gemini**):
- **Never commit API keys** directly to the code or configuration files.
- The `.gitignore` file is configured to ignore `.env` files.
- Paste keys dynamically in the Streamlit Sidebar during execution, or supply them securely via environment variables (e.g. `OPENAI_API_KEY` or `GEMINI_API_KEY`) on your hosting platform.

---

## Reporting a Vulnerability
If you discover any security vulnerability, please do not disclose it publicly. Email us directly at `dinesh@example.com` with a brief description and steps to reproduce. We will respond within 48 hours to coordinate a resolution.
