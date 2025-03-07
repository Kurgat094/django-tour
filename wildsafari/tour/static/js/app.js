document.getElementById('group-size').addEventListener('input', function () {
    if (this.value < 2) {
      this.setCustomValidity('Group size must be at least 2.');
    } else {
      this.setCustomValidity('');
    }
  });




  const modal = document.getElementById("paymentModal");
  const bookNowButton = document.getElementById("bookNowButton");
  const closeModal = document.getElementsByClassName("close")[0];
  const confirmPaymentButton = document.getElementById("confirmPayment");

  // Open the modal when "Book Now" is clicked
  bookNowButton.onclick = function() {
      modal.style.display = "block";
  };

  // Close the modal when the close button is clicked
  closeModal.onclick = function() {
      modal.style.display = "none";
  };

  // Close the modal when clicking outside of it
  window.onclick = function(event) {
      if (event.target === modal) {
          modal.style.display = "none";
      }
  };

  // Handle payment confirmation
  confirmPaymentButton.onclick = function() {
      const amount = document.getElementById("amount").value;
      const phoneNumber = document.getElementById("phoneNumber").value;

      // Send payment details to the backend via AJAX
      $.ajax({
          url: "{% url 'process_payment' %}",  // URL to your Django view for processing payment
          method: "POST",
          data: {
              amount: amount,
              phoneNumber: phoneNumber,
              csrfmiddlewaretoken: "{{ csrf_token }}"
          },
          success: function(response) {
              if (response.success) {
                  alert("Payment successful! Booking saved.");
                  modal.style.display = "none";
                  document.getElementById("bookingForm").submit();  // Submit the booking form
              } else {
                  alert("Payment failed: " + response.message);
              }
          },
          error: function(xhr, status, error) {
              alert("An error occurred during payment processing.");
          }
      });
  };




  document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        let messages = document.querySelectorAll('.popup-message');
        messages.forEach(function (msg) {
            msg.style.animation = "fadeOut 0.5s ease-in-out forwards";
            setTimeout(() => msg.remove(), 500);  // Remove message after animation
        });
    }, 5000);  // Message disappears after 5 seconds
});

// Get the input field
let dateInput = document.getElementById("date_of_visit");

// Get tomorrow's date in YYYY-MM-DD format
let today = new Date();
today.setDate(today.getDate() + 1); // Set to tomorrow
let minDate = today.toISOString().split("T")[0];

// Set the min attribute to tomorrow's date
dateInput.setAttribute("min", minDate);

document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        let messages = document.querySelectorAll('.popup-message');
        messages.forEach(function (msg) {
            msg.style.animation = "fadeOut 0.5s ease-in-out forwards";
            setTimeout(() => msg.remove(), 500);  // Remove message after fade-out
        });
    }, 5000);  // Disappear after 5 seconds
});

function closePopup(element) {
    element.parentElement.style.animation = "fadeOut 0.5s ease-in-out forwards";
    setTimeout(() => element.parentElement.remove(), 500);
}