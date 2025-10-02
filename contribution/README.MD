# **Hobbies Web App - Group Coursework**

## **Group Members**

1. **Mohamed**
   - **Assigned Task:** Describe Mohamed's assigned tasks, e.g., "Developed the backend API endpoints for user management."
   - **Actual Contribution:** Briefly describe what Mohamed actually worked on, e.g., "Implemented user authentication and wrote automated tests for login functionality."

2. **Zakariye**
   - **Assigned Task:** Describe Zakariye's assigned tasks, e.g., "Created the frontend for profile management and integrated it with the backend."
   - **Actual Contribution:** Briefly describe what Zakariye actually worked on, e.g., "Developed the profile page, allowing users to edit their hobbies and personal information."

3. **Asad Ali Khan (220257466)**
   - **Assigned Task:** Steps 4,5,6
   - **Actual Contribution:** Most of them 

4. **Kaif**
   - **Assigned Task:** Describe Kaif's assigned tasks, e.g., "Set up the deployment environment and worked on the pagination logic for user listings."
   - **Actual Contribution:** Briefly describe what Kaif actually worked on, e.g., "Handled the deployment on OpenShift and implemented pagination on the users page."

---

## **Deployed Application**

- **URL:** [Insert the URL of your deployed application here]

---

## **Admin User Credentials**

- **Username:** [Insert admin username]
- **Password:** [Insert admin password]

---

## **Test Users**

Below are the credentials for at least 5 test users:

1. **Username:** testuser1  
   **Password:** password1

2. **Username:** testuser2  
   **Password:** password2

3. **Username:** testuser3  
   **Password:** password3

4. **Username:** testuser4  
   **Password:** password4

5. **Username:** testuser5  
   **Password:** password5

---

## **Description of the Application**

The Hobbies Web App is a single-page application (SPA) that allows users to:

- Create an account, login, and logout using Django's authentication framework.
- Manage their profile, including name, email, date of birth, and hobbies.
- Add new hobbies that are shared across all users.
- View a list of users with similar hobbies, filter by age, and paginate the results.
- Send, accept, and reject friend requests.
- Use a Vue.js frontend with Vue Router for navigation and Pinia for state management.
- Perform all frontend-backend communication via `fetch` with static typing in both Python and TypeScript.

---

## **Technologies Used**

- **Backend:** Django 5.1
- **Frontend:** Vue.js with Vite, TypeScript, and Pinia
- **Database:** SQLite (or other database used)
- **Testing:** Selenium-based E2E testing
- **Deployment:** OpenShift

---

## **How to Run Locally**

1. Clone the repository:
   ```bash
   git clone [repository-url]
   ```
2. Set up the environment:
   ```bash
   conda create --name webapp python=3.11
   conda activate webapp
   pip install -r requirements.txt
   ```
3. Run the backend server:
   ```bash
   python manage.py runserver
   ```
4. Navigate to the `frontend` directory and start the Vue app:
   ```bash
   npm install
   npm run dev
   ```

---

## **Testing**

- **E2E Testing:** Run Selenium tests using:
  ```bash
  pytest tests/selenium
  ```
- **Backend Unit Tests:** Run Django tests using:
  ```bash
  python manage.py test
  ```