document.addEventListener("DOMContentLoaded", function () {
    var educationCounter = 1;

    function updateEducationItemNumbers() {
        var educationItems = document.querySelectorAll(".education-item");
        educationItems.forEach(function (item, index) {
            item.querySelector(".education-item-number").textContent = index + 1;
        });
    }

    function deleteEducationItem(educationItem) {
        if (document.querySelectorAll(".education-item").length > 1) {
            educationItem.parentNode.removeChild(educationItem);
            updateEducationItemNumbers();
        }
    }

    document.getElementById("addNewEducationItemButton").addEventListener("click", function () {
        if (document.querySelectorAll(".education-item")) {
            var educationContainer = document.getElementById("educationalBackground");
            var newEducationItem = educationContainer.querySelector(".education-item").cloneNode(true);
            educationCounter++;
            newEducationItem.id = "educationItem" + educationCounter;
            newEducationItem.querySelectorAll("input").forEach(function (input) {
                input.value = "";
            });
            educationContainer.appendChild(newEducationItem);
            updateEducationItemNumbers();
        }
    });

    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-education-button")) {
            var educationItem = event.target.closest(".education-item");
            deleteEducationItem(educationItem);
        }
    });

    document.getElementById("submitEducationButton").addEventListener("submit", function () {
        updateEducationItemNumbers();
    });
});
