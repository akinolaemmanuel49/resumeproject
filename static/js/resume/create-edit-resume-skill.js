document.addEventListener('DOMContentLoaded', function () {
    const skillGroupsContainer = document.getElementById('skillGroupsContainer');
    const resumeId = document.querySelector('.form-create-edit-resume-skills').getAttribute('data-resume-id');

    // Function to add a new skill to a skill group
    function addNewSkill(groupId) {
        const skillGroup = document.querySelector(`.skill-group-item[data-group-id="${groupId}"]`);
        const skillsInGroup = skillGroup.querySelector(`#skillsInGroup${groupId}`);

        // Create new skill item
        const newSkillItem = document.createElement('div');
        newSkillItem.classList.add('skill-item');
        newSkillItem.setAttribute('data-skill-id', 'new');
        newSkillItem.innerHTML = `
            <input type="hidden" name="skill-id" value="">
            <div class="form-floating">
                <input type="text" class="form-control" id="floatingSkillName-${groupId}-new" placeholder="Skill Name"
                    name="skill_name" aria-required="true">
                <label for="floatingSkillName-${groupId}-new">Skill Name</label>
            </div>
            <button class="btn btn-danger delete-skill-button" type="button">Delete Skill</button>
        `;

        // Append new skill item to the group
        skillsInGroup.appendChild(newSkillItem);

        // Add delete skill functionality
        newSkillItem.querySelector('.delete-skill-button').addEventListener('click', function () {
            deleteSkill(newSkillItem);
        });
    }

    // Function to delete a skill
    function deleteSkill(skillItem) {
        const skillId = skillItem.getAttribute('data-skill-id');
        if (skillId && skillId !== 'new') {
            fetch(`/resume/delete/skill/${skillId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        skillItem.remove();
                    }
                });
        } else {
            skillItem.remove();
        }
    }

    // Function to delete a skill group
    function deleteSkillGroup(skillGroupItem) {
        const groupId = skillGroupItem.getAttribute('data-group-id');
        if (groupId && groupId !== '0') {
            fetch(`/resume/delete/skill-group/${groupId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        skillGroupItem.remove();
                    }
                });
        } else {
            skillGroupItem.remove();
        }
    }

    // Handle add new skill button clicks
    skillGroupsContainer.addEventListener('click', function (e) {
        if (e.target.classList.contains('add-new-skill-button')) {
            const groupId = e.target.getAttribute('data-group-id');
            addNewSkill(groupId);
        }
    });

    // Handle delete skill group button clicks
    skillGroupsContainer.addEventListener('click', function (e) {
        if (e.target.classList.contains('delete-skill-group-button')) {
            const skillGroupItem = e.target.closest('.skill-group-item');
            deleteSkillGroup(skillGroupItem);
        }
    });

    // Handle delete skill button clicks
    skillGroupsContainer.addEventListener('click', function (e) {
        if (e.target.classList.contains('delete-skill-button')) {
            const skillItem = e.target.closest('.skill-item');
            deleteSkill(skillItem);
        }
    });

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});