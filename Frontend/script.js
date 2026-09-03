const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");
const countBtn = document.getElementById("countBtn");
const count = document.getElementById("count");

// Show image preview
imageInput.addEventListener("change", function () {
    const file = this.files[0];

    if (file) {
        const imageURL = URL.createObjectURL(file);
        preview.src = imageURL;
        preview.style.display = "block";
        count.textContent = "Ready to count! 🍚";
    }
});

// Real counting button (Connected to Python Flask Backend)
countBtn.addEventListener("click", function () {
    if (!imageInput.files[0]) {
        count.textContent = "Please upload a rice image first! 🍚";
        return;
    }

    count.textContent = "🔍 Counting rice grains...";

    const formData = new FormData();
    formData.append("image", imageInput.files[0]);

    // Flask Backend Call
    fetch("http://127.0.0.1:5000/api/count", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            count.innerHTML = `🍚 <strong>${data.grain_count}</strong> rice grains detected!<br><span style="font-size: 14px; color: #555;">${data.message}</span>`;
        } else {
            count.textContent = "Error processing image!";
        }
    })
    .catch(error => {
        console.error("Error:", error);
        count.textContent = "Backend server connect aayan pattunnilla! (app.py run cheyyunundoo enn nokku)";
    });
});
