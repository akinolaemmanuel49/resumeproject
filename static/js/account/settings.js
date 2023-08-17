document.addEventListener('DOMContentLoaded', function () {
    const emailField = document.getElementById("email");
    const changeEmailButton = document.getElementById("changeEmailButton");
    const changeEmailForm = document.getElementById("changeEmailForm");
    const emailForm = document.getElementById("emailForm");
    const updateEmailButton = document.getElementById("updateEmailButton");
    const changePasswordButton = document.getElementById("changePasswordButton");
    const changePasswordForm = document.getElementById("changePasswordForm");
    const passwordForm = document.getElementById("passwordForm");
    const updatePasswordButton = document.getElementById("updatePasswordButton");
    const deleteAccountModalButton = document.getElementById("deleteAccountModalButton");
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

    updateEmailButton.addEventListener("click", function (event) {
        event.preventDefault();

        const formData = new FormData(emailForm);

        fetch(emailForm.getAttribute('action'), {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                emailField.textContent = formData.get("new_email");
                emailForm.reset();
            })
            .catch(error => {
                console.error("Error:", error);
            });
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

    updatePasswordButton.addEventListener("click", function (event) {
        event.preventDefault();

        const formData = new FormData(passwordForm);

        fetch(passwordForm.getAttribute('action'), {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                passwordForm.reset();
                window.location.replace("http://127.0.0.1:8000/account/login");
            })
            .catch(error => {
                console.error("Error:", error);
            })
    })

    deleteAccountModalButton.addEventListener("click", function (event) {
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

    deleteAccountButton.addEventListener("click", function (event) {
        event.preventDefault();

        window.location.replace("http://127.0.0.1:8000/account/login");
    })
});
