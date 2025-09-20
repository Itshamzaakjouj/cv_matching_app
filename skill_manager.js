class SkillManager {
    constructor() {
        this.skillInput = document.getElementById('skillInput');
        this.skillTags = document.getElementById('skillTags');
        this.addButton = document.getElementById('addSkillBtn');
        this.skills = new Set();

        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Gestion de la touche Entrée
        this.skillInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault(); // Empêcher le formulaire de se soumettre
                this.addSkill();
            }
        });

        // Gestion du bouton d'ajout
        if (this.addButton) {
            this.addButton.addEventListener('click', () => {
                this.addSkill();
            });
        }
    }

    addSkill() {
        const skill = this.skillInput.value.trim();
        if (skill && !this.skills.has(skill)) {
            this.skills.add(skill);
            this.createSkillTag(skill);
            this.skillInput.value = ''; // Vider l'input
            this.skillInput.focus(); // Remettre le focus sur l'input
        }
    }

    createSkillTag(skill) {
        const tag = document.createElement('div');
        tag.className = 'skill-tag group flex items-center bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-sm';
        tag.innerHTML = `
            <span>${skill}</span>
            <button class="ml-2 text-blue-600 hover:text-blue-800 focus:outline-none opacity-0 group-hover:opacity-100 transition-opacity"
                    onclick="window.skillManager.removeSkill('${skill}')">
                <i class="fas fa-times"></i>
            </button>
        `;
        this.skillTags.appendChild(tag);
    }

    removeSkill(skill) {
        this.skills.delete(skill);
        const tag = Array.from(this.skillTags.children)
            .find(el => el.textContent.trim() === skill);
        if (tag) {
            tag.remove();
        }
    }

    getSkills() {
        return Array.from(this.skills);
    }

    clearSkills() {
        this.skills.clear();
        this.skillTags.innerHTML = '';
    }
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    window.skillManager = new SkillManager();
});
