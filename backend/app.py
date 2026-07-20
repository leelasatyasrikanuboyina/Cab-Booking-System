from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

# Create Flask App
app = Flask(__name__)
CORS(app)

# MySQL Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "leela@2617"
app.config["MYSQL_DB"] = "cab_booking"

mysql = MySQL(app)

# ----------------------------
# Home Route
# ----------------------------
@app.route("/")
def home():
    return "Cab Booking Backend Connected to MySQL Successfully!"

# ----------------------------
# Register Route
# ----------------------------
@app.route("/api/auth/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        name = data["name"]
        email = data["email"]
        phone = data["phone"]
        password = data["password"]

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)",
            (name, email, phone, password)
        )

        mysql.connection.commit()
        cursor.close()

        return jsonify({
            "success": True,
            "message": "User Registered Successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ----------------------------
# Login Route
# ----------------------------
@app.route("/api/auth/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        email = data["email"]
        password = data["password"]

        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cursor.fetchone()
        cursor.close()

        if user:
            return jsonify({
                "success": True,
                "message": "Login Successful"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Invalid Email or Password"
            }), 401

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ----------------------------
# Book Cab Route
# ----------------------------
@app.route("/api/book", methods=["POST"])
def book_cab():
    try:
        data = request.get_json()

        user_id = data["user_id"]
        driver_id = data["driver_id"]
        pickup_location = data["pickup_location"]
        drop_location = data["drop_location"]
        fare = data["fare"]

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            INSERT INTO bookings
            (user_id, driver_id, pickup_location, drop_location, booking_date, fare)
            VALUES (%s, %s, %s, %s, NOW(), %s)
            """,
            (
                user_id,
                driver_id,
                pickup_location,
                drop_location,
                fare
            )
        )

        mysql.connection.commit()
        cursor.close()

        return jsonify({
            "success": True,
            "message": "Cab Booked Successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    # ----------------------------
# View All Bookings
# ----------------------------
@app.route("/api/bookings", methods=["GET"])
def view_bookings():
    try:
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT booking_id,
                   user_id,
                   driver_id,
                   pickup_location,
                   drop_location,
                   booking_date,
                   fare
            FROM bookings
        """)

        rows = cursor.fetchall()
        cursor.close()

        bookings = []

        for row in rows:
            bookings.append({
                "booking_id": row[0],
                "user_id": row[1],
                "driver_id": row[2],
                "pickup_location": row[3],
                "drop_location": row[4],
                "booking_date": str(row[5]),
                "fare": float(row[6]) if row[6] is not None else 0
            })

        return jsonify({
            "success": True,
            "bookings": bookings
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    # ----------------------------
# Cancel Booking API
# ----------------------------
@app.route("/api/bookings/<int:booking_id>", methods=["DELETE"])
def cancel_booking(booking_id):
    try:
        cursor = mysql.connection.cursor()

        # Check if booking exists
        cursor.execute(
            "SELECT * FROM bookings WHERE booking_id = %s",
            (booking_id,)
        )

        booking = cursor.fetchone()

        if not booking:
            cursor.close()
            return jsonify({
                "success": False,
                "message": "Booking Not Found"
            }), 404

        # Delete booking
        cursor.execute(
            "DELETE FROM bookings WHERE booking_id = %s",
            (booking_id,)
        )

        mysql.connection.commit()
        cursor.close()

        return jsonify({
            "success": True,
            "message": "Booking Cancelled Successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ----------------------------
# Payment API
# ----------------------------
@app.route("/api/payment", methods=["POST"])
def make_payment():
    try:
        data = request.get_json()

        booking_id = data["booking_id"]
        amount = data["amount"]
        payment_method = data["payment_method"]
        payment_status = data["payment_status"]

        cursor = mysql.connection.cursor()

        # Check if booking exists
        cursor.execute(
            "SELECT * FROM bookings WHERE booking_id = %s",
            (booking_id,)
        )

        booking = cursor.fetchone()

        if not booking:
            cursor.close()
            return jsonify({
                "success": False,
                "message": "Booking Not Found"
            }), 404

        # Insert payment
        cursor.execute(
            """
            INSERT INTO payments
            (booking_id, amount, payment_method, payment_status)
            VALUES (%s, %s, %s, %s)
            """,
            (booking_id, amount, payment_method, payment_status)
        )

        mysql.connection.commit()
        cursor.close()

        return jsonify({
            "success": True,
            "message": "Payment Successful"
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
   # ----------------------------
# Update Profile API
# ----------------------------
@app.route("/api/profile/<int:user_id>", methods=["PUT"])
def update_profile(user_id):
    try:
        data = request.get_json()

        email = data["email"]
        phone = data["phone"]
        password = data["password"]

        cursor = mysql.connection.cursor()

        # Check user exists
        cursor.execute(
    "SELECT * FROM users WHERE id=%s",
    (user_id,)
)
        user = cursor.fetchone()

        if not user:
            cursor.close()
            return jsonify({
                "success": False,
                "message": "User Not Found"
            }), 404

        # Update profile
        cursor.execute(
            """
            UPDATE users
            SET email=%s,
                phone=%s,
                password=%s
            WHERE id=%s
            """,
            (email, phone, password, user_id)
        )

        mysql.connection.commit()
        cursor.close()

        return jsonify({
            "success": True,
            "message": "Profile Updated Successfully"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    # ----------------------------
# Run Flask
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
    