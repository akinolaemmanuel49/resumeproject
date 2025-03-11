document.addEventListener("DOMContentLoaded", function () {
    var maxSocialItems = 4;
    var socialCounter = document.querySelectorAll(".social-item").length;
    var resumeId = document.querySelector(".form-create-edit-resume-socials").dataset.resumeId;

    function getCsrfToken() {
        return document.querySelector("input[name='csrfmiddlewaretoken']").value;
    }

    function updateSocialItemNumbers() {
        var socialItems = document.querySelectorAll(".social-item");
        socialItems.forEach(function (item, index) {
            item.querySelector(".social-item-number").textContent = index + 1;
            item.querySelectorAll("input").forEach(function (input) {
                if (input.name.includes("[name]")) {
                    input.name = `socials[${index}][name]`;
                } else if (input.name.includes("[url]")) {
                    input.name = `socials[${index}][url]`;
                }
            });
        });
    }

    function checkMaxItems() {
        if (document.querySelectorAll(".social-item").length >= maxSocialItems) {
            document.getElementById("addNewSocialItemButton").disabled = true;
        } else {
            document.getElementById("addNewSocialItemButton").disabled = false;
        }
    }

    function deleteSocialItem(socialItem) {
        if (document.querySelectorAll(".social-item").length > 1) {
            socialItem.parentNode.removeChild(socialItem);
            updateSocialItemNumbers();
            checkMaxItems();
        }
    }

    document.getElementById("addNewSocialItemButton").addEventListener("click", function () {
        if (document.querySelectorAll(".social-item").length < maxSocialItems) {
            var socialsContainer = document.getElementById("socials");
            var newSocialItem = socialsContainer.querySelector(".social-item").cloneNode(true);
            socialCounter++;
            newSocialItem.id = "socialsItem" + socialCounter;
            newSocialItem.querySelectorAll("input").forEach(function (input) {
                input.value = "";
            });
            socialsContainer.appendChild(newSocialItem);
            updateSocialItemNumbers();
            checkMaxItems();
        }
    });

    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-social-button")) {
            var socialItem = event.target.closest(".social-item");
            var socialIdInput = socialItem.querySelector("input[name='social-id']");

            if (socialIdInput && socialIdInput.value.trim() !== "") {
                var socialId = socialIdInput.value;

                fetch(`/resume/${resumeId}/delete/socials/${socialId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCsrfToken(),
                        "Content-Type": "application/json",
                    },
                })
                    .then(response => {
                        if (response.ok) {
                            socialItem.remove();
                            updateSocialItemNumbers();
                            checkMaxItems();
                        } else {
                            console.error("Failed to delete social:", response.status);
                        }
                    })
                    .catch(error => console.error("Error:", error));
            } else {
                // If it's a new, unsaved social, just remove it from the UI
                socialItem.remove();
                updateSocialItemNumbers();
                checkMaxItems();
            }
        }
    });

    document.querySelector(".form-create-edit-resume-socials").addEventListener("submit", function () {
        updateSocialItemNumbers();
    });

    // Initial checks
    checkMaxItems();
    updateSocialItemNumbers();
});
