document.addEventListener("DOMContentLoaded", function () {
    var skillCounter = 1;

    function updateSkillItemNumbers() {
        var skillItems = document.querySelectorAll(".skill-item");
        skillItems.forEach(function (item, index) {
            item.querySelector(".skill-item-number").textContent = index + 1;
        });
    }

    function deleteSkillItem(skillItem) {
        if (document.querySelectorAll(".skill-item").length > 1) {
            skillItem.parentNode.removeChild(skillItem);
            updateSkillItemNumbers();
        }
    }

    document.getElementById("addNewSkillItemButton").addEventListener("click", function () {
        if (document.querySelectorAll(".skill-item")) {
            var skillContainer = document.getElementById("skill");
            var newSkillItem = skillContainer.querySelector(".skill-item").cloneNode(true);
            skillCounter++;
            newSkillItem.id = "skillItem" + skillCounter;
            newSkillItem.querySelectorAll("input").forEach(function (input) {
                input.value = "";
            });
            skillContainer.appendChild(newSkillItem);
            updateSkillItemNumbers();
        }
    });

    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-skill-button")) {
            var skillItem = event.target.closest(".skill-item");
            deleteSkillItem(skillItem);
        }
    });

    document.getElementById("submitSkillButton").addEventListener("submit", function () {
        updateSkillItemNumbers();
    });
});
