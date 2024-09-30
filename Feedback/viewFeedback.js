window.onload = function() {
    const feedbacks = JSON.parse(getCookie("feedbacks") || "[]");
    const feedbackContainer = document.getElementById("feedbackContainer");

    feedbacks.forEach((feedback, index) => {
        const feedbackCard = document.createElement("div");
        feedbackCard.className = "feedback-card";
        feedbackCard.innerHTML = `
            <h3>Feedback #${index + 1}</h3>
            <p><strong>Session Quality:</strong> ${feedback.sessionQuality}</p>
            <p><strong>Mentor Knowledge:</strong> ${feedback.mentorKnowledge}</p>
            <p><strong>Communication:</strong> ${feedback.communication}</p>
            <p><strong>Engagement:</strong> ${feedback.engagement}</p>
            <p><strong>Suggestions:</strong> ${feedback.suggestions}</p>
        `;
        feedbackContainer.appendChild(feedbackCard);
    });
};

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
