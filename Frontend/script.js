const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");

const countBtn = document.getElementById("countBtn");
const againBtn = document.getElementById("againBtn");

const loading = document.getElementById("loading");
const result = document.getElementById("result");

const grainCount = document.getElementById("grainCount");
const dialogue = document.getElementById("dialogue");
const movieRef = document.getElementById("movieRef");
const timeWasted = document.getElementById("timeWasted");
const tier = document.getElementById("tier");
const message = document.getElementById("message");

const loadingTitle = document.getElementById("loadingTitle");
const loadingText = document.getElementById("loadingText");

const loadingMessages = [
["Ari manikal interrogation-il aanu... 🔍", "Oru nimisham... serious investigation aanu."],
["Rice ne chodhyam cheyyunnu... 🍚", "Aarum disturb cheyyaruthu."],
["Ithrem ari enthina? 😭", "Njangalkkum ariyilla."],
["Count cheythondirikkunnu...", "Engineering at its finest. 💀"]
];

// Backend base URL (Render deployment)
const BACKEND_URL = "https://rice-counter.onrender.com";

imageInput.addEventListener("change", function () {

const file = this.files[0];

if (!file) return;

const imageURL = URL.createObjectURL(file);

preview.src = imageURL;
preview.style.display = "block";

result.classList.add("hidden");

countBtn.textContent = "COUNT CHEYYATTE? 🍚";

});

countBtn.addEventListener("click", async function () {

const file = imageInput.files[0];

if (!file) {
    alert("Aadyam rice nte photo upload cheyyu! 🍚😭");
    return;
}

loading.classList.remove("hidden");
result.classList.add("hidden");

countBtn.disabled = true;

const randomMessage =
    loadingMessages[Math.floor(Math.random() * loadingMessages.length)];

loadingTitle.textContent = randomMessage[0];
loadingText.textContent = randomMessage[1];


const formData = new FormData();

formData.append("image", file);


try {

    const response = await fetch(`${BACKEND_URL}/api/count`, {
        method: "POST",
        body: formData
    });

    const data = await response.json();


    if (!data.success) {
        throw new Error(data.message || "Something went wrong");
    }


    grainCount.textContent =
        Number(data.grain_count).toLocaleString();

    dialogue.textContent = data.dialogue;

    movieRef.textContent =
        "🎬 " + data.movie_ref;

    timeWasted.textContent =
        data.time_wasted;

    tier.textContent =
        data.tier.replaceAll("_", " ").toUpperCase();

    message.textContent =
        data.message;


    loading.classList.add("hidden");
    result.classList.remove("hidden");

    result.scrollIntoView({
        behavior: "smooth"
    });

}

catch (error) {

    loading.classList.add("hidden");

    alert(
        "Backend-umayi connection kittiyilla 😭\n\n" +
        "Friend's Python server running aano?"
    );

    console.error(error);

}

finally {

    countBtn.disabled = false;

}

});

againBtn.addEventListener("click", function () {

imageInput.value = "";

preview.src = "";
preview.style.display = "none";

result.classList.add("hidden");

window.scrollTo({
    top: 0,
    behavior: "smooth"
});

});
