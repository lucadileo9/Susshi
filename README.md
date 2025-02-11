# Sushi Restaurant Ordering System

This project is a web application built with Django that allows users to browse the menu of a sushi restaurant and place orders. The restaurant staff, specifically a user with chef privileges, can manage incoming orders and update the status of the kitchen.

## Features
- **Menu browsing**: Customers can view an organized menu of sushi dishes.
- **Ordering system**: Users can select items from the menu, create an order, and send it to the kitchen.
- **Chef management**: A user with chef privileges can manage and track the status of incoming orders.
  
## Technologies Used
- **Django**: Backend framework.
- **HTML/CSS**: Frontend structure and styling.
- **SQLite**: Default database for development.
  
## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lucadileo9/Susshi.git
   cd Susshi
   ```
2. Ensure Python Version Compatibility:
   This project requires Python 3.8 or higher . Verify your Python version:
    ```bash
    python3 --version
    ```
3. Create a virtual environment and activate it:
   ```bash
   python3 -m venv env
   source env/bin/activate  # For Windows: env\Scripts\activate
   ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the website in your browser at `http://127.0.0.1:8000/`.

## Usage

- **Customer users**: Browse the sushi menu and place orders.
- **Chef users**: Log in to the admin interface, manage orders, and track the kitchen workflow.
Note:
If the menu in the header is not visible due to zooming, try reducing the zoom level in your browser (usually by pressing Ctrl + - ).
The application is designed for local use, so no external access is required.


### Test Credentials

To fully test the application, you can use the following credentials. **Note:** Often, the password is the first letter of the username repeated four times (e.g., `aaaa` for `Amicizia`).

---

#### **Visitor**
- A basic user who visits the page and can only view the menu, dishes, etc.
- **No login required.**


#### **Table Users**
These represent tables that can place orders. Each table has its own credentials:

| Username   | Password |
|------------|----------|
| Amicizia   | aaaa     |
| Fedeltà    | ffff     |
| Speranza   | ssss     |
| Fortuna    | ffff     |


#### **Chef**
Chefs can manage orders and preparations for the tables. They also have permissions to organize menus, dishes, and other site functionalities:

| Username   | Password |
|------------|----------|
| Zorro      | zzzz     |
| Valter     | vvvv     |


#### **Superuser**
The administrator with full access to all functionalities:

| Username   | Password |
|------------|----------|
| user       | user     |

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
