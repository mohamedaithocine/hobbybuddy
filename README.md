# **HobbyBuddy**


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
- **Database:** SQLite
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
<img width="1920" height="1040" alt="251002193244_zen" src="https://github.com/user-attachments/assets/27c36af2-22a6-4e4d-ac2a-4fff59a5c685" />
<img width="1920" height="1708" alt="7hMGQVfADY" src="https://github.com/user-attachments/assets/4a8de3af-7e62-456c-a463-9449d3d3f5ae" />
<img width="1920" height="1040" alt="251002193344_zen" src="https://github.com/user-attachments/assets/3fb13f47-6e00-49fe-9886-bc6bad3cc555" />
<img width="1920" height="1040" alt="251002193353_zen" src="https://github.com/user-attachments/assets/41402094-0c1b-4f19-a8d2-f44eecd5737b" />

  

## **Test Users**

1.  **Username:** brook  
    **Password:** admin

2.  **Username:** chopper  
    **Password:** admin

3.  **Username:** ekko  
    **Password:** admin

4.  **Username:** franky  
    **Password:** admin

5.  **Username:** fsaint  
    **Password:** admin

6.  **Username:** harvey  
    **Password:** admin

7.  **Username:** janedoe  
    **Password:** admin

8.  **Username:** jinbei  
    **Password:** admin

9.  **Username:** johndoe  
    **Password:** admin

10. **Username:** ken  
    **Password:** admin
   
11. **Username:** luffy  
    **Password:** admin

12. **Username:** nami  
    **Password:** admin

13. **Username:** naruto  
    **Password:** admin

14. **Username:** pacman  
    **Password:** admin

15. **Username:** ralph  
    **Password:** admin

16. **Username:** robinn  
    **Password:** admin

17. **Username:** sanji  
    **Password:** admin

18. **Username:** ussopp  
    **Password:** admin

19. **Username:** zoro  
    **Password:** admin

20. **Username:** user20
    **Password:** admin
