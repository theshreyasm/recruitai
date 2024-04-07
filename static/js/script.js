document.addEventListener('DOMContentLoaded', function () {
    const addSkillInput = document.getElementById('addSkillInput');
    const addSkillButton = document.getElementById('addSkillButton');
    const skillsContainer = document.getElementById('skills-container');
    const skillsInput = document.createElement('input');
    skillsInput.type = 'hidden';
    skillsInput.name = 'skills';
    skillsContainer.appendChild(skillsInput);

    addSkillButton.addEventListener('click', function () {
        const skill = addSkillInput.value.trim();
        if (skill) {
            const skillBox = document.createElement('div');
            skillBox.classList.add('skill-box');
            skillBox.textContent = skill;
            skillBox.style.color = 'black';
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'x';
            deleteButton.classList.add('delete-button');
            deleteButton.addEventListener('click', function () {
                skillsContainer.removeChild(skillBox);
                updateSkillsInput(); // Update skills input value when a skill is deleted
            });
            skillBox.appendChild(deleteButton);
            skillsContainer.appendChild(skillBox);
            addSkillInput.value = '';
            updateSkillsInput(); // Update skills input value when a skill is added
        }
    });

    function updateSkillsInput() {
        const skills = Array.from(skillsContainer.querySelectorAll('.skill-box')).map(skillBox => {
            return skillBox.textContent.replace(/\s*x$/, '');
        });
        skillsInput.value = skills.join(', ');
        console.log("Updated Skills:", skillsInput.value);

        // Log the skills value to the console
        console.log("Skills:", skills);
    }
    
});


function showLoading() {
    const video = document.getElementById('video').value;
    const transcript = document.getElementById('transcript').value;
    
    if(!((video === "") && (transcript === "")))
    {
        // Hide the title
        document.getElementById('formTitle').style.display = 'none';
        // Hide the form
        document.getElementById('jobApplicationForm').style.display = 'none';
        // Show the loading message
        document.getElementById('loadingMessage').style.display = 'block';
    }
  }
