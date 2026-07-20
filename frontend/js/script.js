async function login() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (email === "" || password === "") {
        alert("Please fill all fields");
        return;
    }

    const response = await fetch("http://127.0.0.1:5000/api/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    });

    const data = await response.json();

    if (data.success) {
        alert("Login Successful!");
        window.location.href = "dashboard.html";
    } else {
        alert(data.message);
    }
}

async function register() {

    const name = document.getElementById("name").value;
    const email = document.getElementById("regEmail").value;
    const phone = document.getElementById("phone").value;
    const password = document.getElementById("regPassword").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if (name === "" || email === "" || phone === "" || password === "" || confirmPassword === "") {
        alert("Please fill all fields");
        return;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match");
        return;
    }

    const response = await fetch("http://127.0.0.1:5000/api/auth/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name,
            email: email,
            phone: phone,
            password: password
        })
    });

    const data = await response.json();

    if (data.success) {
        alert("Registration Successful!");
        window.location.href = "login.html";
    } else {
        alert(data.error);
    }
}

 async function bookCab() {

    let pickup = document.getElementById("pickup").value;
    let drop = document.getElementById("drop").value;
    let date = document.getElementById("date").value;
    let time = document.getElementById("time").value;
    let cab = document.getElementById("cab").value;

    if (pickup === "" || drop === "" || date === "" || time === "" || cab === "") {
        alert("Please fill all details");
        return;
    }

    // Temporary values
    let user_id = 2;
    let driver_id = 1;
    let fare = 450;

    try {

        const response = await fetch("http://127.0.0.1:5000/api/book", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: user_id,
                driver_id: driver_id,
                pickup_location: pickup,
                drop_location: drop,
                fare: fare
            })
        });

        const data = await response.json();

        if (data.success) {
            alert("Cab Booked Successfully!");
            window.location.href = "bookings.html";
        } else {
            alert(data.error);
        }

    } catch (error) {
        alert("Cannot connect to backend.");
    }

}
async function loadBookings() {

    const response = await fetch("http://127.0.0.1:5000/api/bookings");

    const data = await response.json();

    if (data.success) {

        let rows = "";

        data.bookings.forEach(function (booking) {

            rows += `
            <tr>
                <td>${booking.booking_id}</td>
                <td>${booking.pickup_location}</td>
                <td>${booking.drop_location}</td>
                <td>${booking.fare}</td>
                <td>${booking.booking_date}</td>

                <td>
                    <button onclick="cancelBooking(${booking.booking_id})">
                        Cancel
                    </button>
                </td>

            </tr>
            `;

        });

        document.getElementById("bookingTable").innerHTML = rows;

    }

}
async function cancelBooking(booking_id) {

    let result = confirm("Are you sure you want to cancel this booking?");

    if (!result) {
        return;
    }

    const response = await fetch(
        "http://127.0.0.1:5000/api/bookings/" + booking_id,
        {
            method: "DELETE"
        }
    );

    const data = await response.json();

    if (data.success) {
        alert("Booking Cancelled Successfully!");
        loadBookings();   // Refresh the table
    } else {
        alert(data.message || data.error);
    }

}// ================= Payment =================
async function makePayment() {

    const booking_id = document.getElementById("booking_id").value;
    const amount = document.getElementById("amount").value;
    const payment_method = document.getElementById("payment_method").value;

    if (booking_id === "" || amount === "" || payment_method === "") {
        alert("Please fill all fields");
        return;
    }

    try {

        const response = await fetch("http://127.0.0.1:5000/api/payment", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                booking_id: booking_id,
                amount: amount,
                payment_method: payment_method,
                payment_status: "Success"

            })

        });

        const data = await response.json();

        if (data.success) {

            alert("Payment Successful!");

            window.location.href = "bookings.html";

        } else {

            alert(data.message || data.error);

        }

    } catch (error) {

        alert("Cannot connect to backend.");

    }

}
async function saveProfile() {

    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;
    const password = document.getElementById("newPassword").value;
    const confirm = document.getElementById("confirmNewPassword").value;

    if (email === "" || phone === "" || password === "" || confirm === "") {
        alert("Please fill all fields");
        return;
    }

    if (password !== confirm) {
        alert("Passwords do not match");
        return;
    }

    const response = await fetch("http://127.0.0.1:5000/api/profile/2", {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            email: email,
            phone: phone,
            password: password
        })

    });

    const data = await response.json();

    if (data.success) {
        alert("Profile Updated Successfully!");
    } else {
        alert(data.message || data.error);
    }

}
function logout() {

    // Clear stored user data (for future use)
    localStorage.clear();

    alert("Logged out successfully!");

    window.location.href = "index.html";
}