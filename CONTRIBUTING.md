# Contributing to Student Study Buddy 🚀

We welcome contributions to improve **Student Study Buddy**! Follow these steps to set up the development environment and submit changes.

---

## 🛠️ Local Development Setup

1. **Fork and Clone**: Fork this repository and clone it to your local machine.
2. **Environment**: Create a python virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Dependencies**: Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run Dev Server**: Run the Streamlit development server:
   ```bash
   streamlit run app.py
   ```

---

## 📝 Contribution Guidelines

### Code Style & Quality
- Write clean, readable code and keep functions focused.
- Ensure all custom imports follow the standard layout.
- Handle exceptions defensively, logging errors using the setup logger.

### Git Branching
1. Create a feature branch: `git checkout -b feat/your-feature-name`
2. Commit your changes with clear messages: `git commit -m "feat: add support for X"`
3. Push to your branch and open a Pull Request (PR) or Merge Request.
