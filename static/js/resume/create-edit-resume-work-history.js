document.addEventListener("DOMContentLoaded", function () {
    var maxWorkHistoryItems = 6;
    var workHistoryCounter = document.querySelectorAll(".work-history-item").length;
    var resumeId = document.querySelector(".form-create-edit-resume-work-history").dataset.resumeId;

    function getCsrfToken() {
        return document.querySelector("input[name='csrfmiddlewaretoken']").value;
    }

    function updateWorkHistoryItemNumbers() {
        document.querySelectorAll(".work-history-item").forEach((item, index) => {
            item.querySelector(".work-history-item-number").textContent = index + 1;
            item.querySelectorAll("input").forEach(input => {
                if (input.name.includes("[organization_name]")) {
                    input.name = `work_histories[${index}][organization_name]`;
                } else if (input.name.includes("[start_date]")) {
                    input.name = `work_histories[${index}][start_date]`;
                } else if (input.name.includes("[end_date]")) {
                    input.name = `work_histories[${index}][end_date]`;
                } else if (input.name.includes("[position]")) {
                    input.name = `work_histories[${index}][position]`;
                } else if (input.name.includes("[description]")) {
                    input.name = `work_histories[${index}][description]`;
                }
            });
        });
    }

    function checkMaxItems() {
        document.getElementById("addNewWorkHistoryItemButton").disabled =
            document.querySelectorAll(".work-history-item").length >= maxWorkHistoryItems;
    }

    function deleteWorkHistoryItem(workHistoryItem) {
        if (document.querySelectorAll(".work-history-item").length > 1) {
            var workHistoryIdInput = workHistoryItem.querySelector("input[name='work-history-id']");

            if (workHistoryIdInput && workHistoryIdInput.value.trim() !== "") {
                var workHistoryId = workHistoryIdInput.value;

                fetch(`/resume/${resumeId}/delete/work-history/${workHistoryId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCsrfToken(),
                        "Content-Type": "application/json",
                    },
                })
                    .then(response => {
                        if (response.ok) {
                            workHistoryItem.remove();
                            updateWorkHistoryItemNumbers();
                            checkMaxItems();
                        } else {
                            console.error("Failed to delete work history:", response.status);
                        }
                    })
                    .catch(error => console.error("Error:", error));
            } else {
                workHistoryItem.remove();
                updateWorkHistoryItemNumbers();
                checkMaxItems();
            }
        }
    }

    document.getElementById("addNewWorkHistoryItemButton").addEventListener("click", function () {
        if (document.querySelectorAll(".work-history-item")) {
            var workHistoryContainer = document.getElementById("workHistory");
            var newWorkHistoryItem = workHistoryContainer.querySelector(".work-history-item").cloneNode(true);
            workHistoryCounter++;
            newWorkHistoryItem.id = "workHistoryItem" + workHistoryCounter;
            newWorkHistoryItem.querySelectorAll("input").forEach(function (input) {
                input.value = "";
            });
            // Clear the description textarea when cloning
            var descriptionTextarea = newWorkHistoryItem.querySelector("textarea[name='description']");
            if (descriptionTextarea) {
                descriptionTextarea.value = "";
            }
            workHistoryContainer.appendChild(newWorkHistoryItem);
            updateWorkHistoryItemNumbers();
        }
    });

    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-work-history-button")) {
            var workHistoryItem = event.target.closest(".work-history-item");
            deleteWorkHistoryItem(workHistoryItem);
        }
    });

    document.getElementById("submitWorkHistoryButton").addEventListener("submit", function () {
        updateWorkHistoryItemNumbers();
    });

    // Auto-resize textareas
    function autoResizeTextarea(textarea) {
        setTimeout(() => {
            textarea.style.height = "auto"; // Reset height
            textarea.style.height = textarea.scrollHeight + "px"; // Adjust height
        }, 0);
    }

    document.querySelectorAll("textarea[name='description']").forEach(function (textarea) {
        autoResizeTextarea(textarea); // Resize on load
        textarea.addEventListener("input", function () {
            autoResizeTextarea(this); // Resize on input
        });
    });

    // Initial setup
    checkMaxItems();
    updateWorkHistoryItemNumbers();
});
