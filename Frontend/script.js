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

// Temporary counting button
countBtn.addEventListener("click", function () {

    if (!imageInput.files[0]) {
        count.textContent = "Please upload a rice image first! 😭";
        return;
    }

    count.textContent = "🔄 Counting rice grains...";

    setTimeout(function () {
        count.textContent = "🍚 347 rice grains detected!";
    }, 1500);

});
