var firebaseConfig = {
    apiKey: "AIzaSyCqTWhstnYIMAWxFKlFmhqV5kXfDsMwm7Q",
    authDomain: "work-vibe.firebaseapp.com",
    databaseURL: "https://work-vibe-default-rtdb.firebaseio.com",
    projectId: "work-vibe",
    storageBucket: "work-vibe.appspot.com",
    messagingSenderId: "657553447517",
    appId: "1:657553447517:web:b31d13b5e033c32d7a8bb4",
    measurementId: "G-HEN3V080PD"
  };
  
  firebase.initializeApp(firebaseConfig);
  var db = firebase.firestore();
  
  function calculateTotal() {
    var productAmount = parseFloat(document.getElementById("tax-1").value) || 0;
    document.getElementById("total-amount").textContent = `INR ${productAmount.toFixed(2)}`;
  }
  
  function paymentProcess() {
    var totalAmount = document.getElementById("total-amount").textContent;
    var amount = parseFloat(totalAmount.replace("INR ", "")) * 100;
  
    if (isNaN(amount) || amount <= 0) {
      alert("Please enter a valid amount.");
      return;
    }
  
    var options = {
      "key": "rzp_test_RkrD1X74NWT4U5",
      "amount": amount,
      "currency": "INR",
      "name": "Aspirehub",
      "description": "Donation Amount",
      "image": "logo.png",
      "handler": function (response) {
        savetoDB(response);
        $('#myModal').modal();
      },
      "prefill": {
        "name": "Mitesh Singh",
        "email": "miteshsingh957@gmail.com",
        "contact": "7420027576"
      },
      "notes": {
        "address": "note value"
      },
      "theme": {
        "color": "#9932CC"
      }
    };
  
    var propay = new Razorpay(options);
    propay.open();
  }
  
  function savetoDB(response) {
    console.log('Payment Response:', response);
  }
  