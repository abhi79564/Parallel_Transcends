document.getElementById("feedbackForm").addEventListener("submit", (event) => {
    event.preventDefault();

    const sessionQuality = document.getElementById("sessionQuality").value;
    const mentorKnowledge = document.getElementById("mentorKnowledge").value;
    const communication = document.getElementById("communication").value;
    const engagement = document.getElementById("engagement").value;
    const suggestions = document.getElementById("suggestions").value;

    const feedback = {
        sessionQuality,
        mentorKnowledge,
        communication,
        engagement,
        suggestions,
    };

    const feedbacks = JSON.parse(getCookie("feedbacks") || "[]");
    feedbacks.push(feedback);
    setCookie("feedbacks", JSON.stringify(feedbacks), 7); // Store for 7 days

    alert("Feedback submitted successfully!");
    document.getElementById("feedbackForm").reset();
});

function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}
