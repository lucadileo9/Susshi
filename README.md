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
   cd sushi-restaurant
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv env
   source env/bin/activate  # For Windows: env\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (for managing the site):
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the website in your browser at `http://127.0.0.1:8000/`.

## Usage

- **Customer users**: Browse the sushi menu and place orders.
- **Chef users**: Log in to the admin interface, manage orders, and track the kitchen workflow.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
