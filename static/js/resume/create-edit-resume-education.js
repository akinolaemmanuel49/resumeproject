document.addEventListener("DOMContentLoaded", function () {
    var maxEducationItems = 6;
    var educationCounter = document.querySelectorAll(".education-item").length;
    var resumeId = document.querySelector(".form-create-edit-resume-education").dataset.resumeId;

    function getCsrfToken() {
        return document.querySelector("input[name='csrfmiddlewaretoken']").value;
    }

    function updateEducationItemNumbers() {
        document.querySelectorAll(".education-item").forEach((item, index) => {
            item.querySelector(".education-item-number").textContent = index + 1;
            item.querySelectorAll("input").forEach(input => {
                if (input.name.includes("[institution]")) {
                    input.name = `educations[${index}][institution]`;
                } else if (input.name.includes("[start_date]")) {
                    input.name = `educations[${index}][start_date]`;
                } else if (input.name.includes("[end_date]")) {
                    input.name = `educations[${index}][end_date]`;
                } else if (input.name.includes("[degree]")) {
                    input.name = `educations[${index}][degree]`;
                }
            });
        });
    }

    function checkMaxItems() {
        document.getElementById("addNewEducationItemButton").disabled =
            document.querySelectorAll(".education-item").length >= maxEducationItems;
    }

    function deleteEducationItem(educationItem) {
        if (document.querySelectorAll(".education-item").length > 1) {
            var educationIdInput = educationItem.querySelector("input[name='education-id']");

            if (educationIdInput && educationIdInput.value.trim() !== "") {
                var educationId = educationIdInput.value;

                fetch(`/resume/${resumeId}/delete/education/${educationId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCsrfToken(),
                        "Content-Type": "application/json",
                    },
                })
                    .then(response => {
                        if (response.ok) {
                            educationItem.remove();
                            updateEducationItemNumbers();
                            checkMaxItems();
                        } else {
                            console.error("Failed to delete education:", response.status);
                        }
                    })
                    .catch(error => console.error("Error:", error));
            } else {
                educationItem.remove();
                updateEducationItemNumbers();
                checkMaxItems();
            }
        }
    }

    document.getElementById("addNewEducationItemButton").addEventListener("click", function () {
        if (document.querySelectorAll(".education-item").length < maxEducationItems) {
            var educationContainer = document.getElementById("educationalBackground");
            var newEducationItem = educationContainer.querySelector(".education-item").cloneNode(true);
            educationCounter++;
            newEducationItem.id = "educationItem" + educationCounter;
            newEducationItem.querySelectorAll("input").forEach(input => (input.value = ""));
            educationContainer.appendChild(newEducationItem);
            updateEducationItemNumbers();
            checkMaxItems();
        }
    });

    document.getElementById("educationalBackground").addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-education-button")) {
            deleteEducationItem(event.target.closest(".education-item"));
        }
    });

    document.querySelector(".form-create-edit-resume-education").addEventListener("submit", function () {
        updateEducationItemNumbers();
    });

    // Initial setup
    checkMaxItems();
    updateEducationItemNumbers();
});
