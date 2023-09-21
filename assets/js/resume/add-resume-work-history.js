document.addEventListener("DOMContentLoaded", function () {
    var workHistoryCounter = 1;

    function updateWorkHistoryItemNumbers() {
        var workHistoryItems = document.querySelectorAll(".work-history-item");
        workHistoryItems.forEach(function (item, index) {
            item.querySelector(".work-history-item-number").textContent = index + 1;
        });
    }

    function deleteWorkHistoryItem(workHistoryItem) {
        if (document.querySelectorAll(".work-history-item").length > 1) {
            workHistoryItem.parentNode.removeChild(workHistoryItem);
            updateWorkHistoryItemNumbers();
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
});
