from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import random
import string

def launch_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    socketio = SocketIO(app)

    # Generate random PIN codes for admin and user
    admin_pin = random.randint(1000, 9999)
    user_pin = random.randint(1000, 9999)

    # Store the generated PIN codes in a dictionary
    pin_codes = {
        'Admin': admin_pin,
        'Participant': user_pin
    }

    # Route for index page
    @app.route('/')
    def index():
        return render_template('index.html')

    # Route for login page
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            input_pin = int(request.form['pin'])
            role = None

            # Check if the input PIN matches the stored PIN
            for r, pin in pin_codes.items():
                if input_pin == pin:
                    role = r
                    print("PIN Matched for", role)  # Print if the PIN matches
                    session['role'] = role  # Store role in session
                    break

            if role:
                print(f"{role} Logged In!")
                return redirect(url_for('chat'))
            else:
                print("Invalid PIN!")

        return render_template('login.html')

    # Route for chat page
    @app.route('/chat')
    def chat():
        if 'role' in session:
            role = session['role']
            return render_template('chat.html', role=role)
        else:
            return redirect(url_for('login'))

    # WebSocket event to handle messages
    @socketio.on('message')
    def handle_message(data):
        emit('message', {'role': data['role'], 'message': data['message']}, broadcast=True)

    if __name__ == '__main__':
        print("Admin PIN: ", admin_pin)
        print("User PIN: ", user_pin)
        socketio.run(app, debug=False)

# Call the function to create the Flask app
# launch_app()
