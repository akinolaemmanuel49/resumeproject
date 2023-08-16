document.addEventListener('DOMContentLoaded', function () {
    const changeEmailButton = document.getElementById("changeEmailButton");
    const changeEmailForm = document.getElementById("changeEmailForm");
    const changePasswordButton = document.getElementById("changePasswordButton");
    const changePasswordForm = document.getElementById("changePasswordForm");
    const deleteAccountButton = document.getElementById("deleteAccountButton");
    const deleteAccountModal = document.getElementById("deleteAccountModal");

    changeEmailButton.addEventListener("click", function (event) {
        event.preventDefault();

        // Toggle display of the email change form
        if (changeEmailForm.style.display === "none") {
            changeEmailForm.style.display = "block";
            changePasswordForm.style.display = "none";
        } else {
            changeEmailForm.style.display = "none";
        }
    });

    changePasswordButton.addEventListener("click", function (event) {
        event.preventDefault();

        // Toggle display of the password change form
        if (changePasswordForm.style.display === "none") {
            changePasswordForm.style.display = "block";
            changeEmailForm.style.display = "none";
        } else {
            changePasswordForm.style.display = "none";
        }
    });

    deleteAccountButton.addEventListener("click", function (event) {
        event.preventDefault();

        // Display the delete account modal
        deleteAccountModal.style.display = "block";
    });

    // Close the modal when the "Close" button is clicked
    const closeButton = deleteAccountModal.querySelector(".close")
    closeButton.addEventListener("click", function () {
        deleteAccountModal.style.display = "none";
    })

    // Close the modal when the "Cancel" button is clicked
    const cancelButton = deleteAccountModal.querySelector(".btn-secondary");
    cancelButton.addEventListener("click", function () {
        deleteAccountModal.style.display = "none";
    });

    // Function to toggle form display
    function toggleFormDisplay(formElement) {
        if (formElement.style.display === "none") {
            formElement.style.display = "block";
        } else {
            formElement.style.display = "none";
        }
    }
});
