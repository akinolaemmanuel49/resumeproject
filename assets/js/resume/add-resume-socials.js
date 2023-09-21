document.addEventListener("DOMContentLoaded", function () {
    var maxSocialItems = 4;
    var socialCounter = 1;

    function updateSocialItemNumbers() {
        var socialItems = document.querySelectorAll(".social-item");
        socialItems.forEach(function (item, index) {
            item.querySelector(".social-item-number").textContent = index + 1;
        });
    }

    function enableAddButton() {
        document.getElementById("addNewSocialItemButton").disabled = false;
    }

    function disableAddButton() {
        document.getElementById("addNewSocialItemButton").disabled = true;
    }

    function checkMaxItems() {
        if (document.querySelectorAll(".social-item").length >= maxSocialItems) {
            disableAddButton();
        } else {
            enableAddButton();
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
            deleteSocialItem(socialItem);
        }
    });

    document.getElementById("submitSocialsButton").addEventListener("submit", function () {
        updateSocialItemNumbers();
    });

    // Initial checks
    checkMaxItems();
});
