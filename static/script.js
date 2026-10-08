const textarea = document.getElementById("policyText");

const charCount = document.getElementById("charCount");

const result = document.getElementById("result");

const button = document.getElementById("simplifyBtn");

const status = document.getElementById("status");


textarea.addEventListener("input", function () {

    charCount.innerText =
        textarea.value.length + " characters";

});


async function simplifyPolicy() {

    const text = textarea.value.trim();

    if (!text) {

        alert("Please paste an insurance policy first.");

        return;
    }


    button.disabled = true;

    button.innerText = "⏳ Simplifying...";

    status.innerText = "AI Processing";

    status.style.background = "#fff4df";

    status.style.color = "#a76a00";


    result.innerHTML = `
        <div class="empty-state">
            <div class="big-icon">🧠</div>
            <h3>AI is analyzing your policy...</h3>
            <p>
                Extracting coverage, exclusions,
                conditions and important details.
            </p>
        </div>
    `;


    try {

        const response = await fetch("/simplify", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: text
            })

        });


        const data = await response.json();


        if (data.error) {

            throw new Error(data.error);

        }


        result.innerText = data.result;


        status.innerText = "Completed";

        status.style.background = "#e9f8ef";

        status.style.color = "#208346";


    }

    catch (error) {

        result.innerText =
            "Something went wrong:\n\n"
            + error.message;

        status.innerText = "Error";

    }


    button.disabled = false;

    button.innerText = "✨ Simplify Policy";

}