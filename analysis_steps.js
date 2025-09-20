class AnalysisStepsManager {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 4;
        this.steps = Array.from({length: this.totalSteps}, (_, i) => document.getElementById(`step${i+1}`));
        this.lines = Array.from({length: this.totalSteps-1}, (_, i) => document.getElementById(`line${i+1}`));
        this.contents = Array.from({length: this.totalSteps}, (_, i) => document.getElementById(`step${i+1}-content`));
        this.prevBtn = document.getElementById('prevBtn');
        this.nextBtn = document.getElementById('nextBtn');
        this.skills = new Set();

        this.initializeEventListeners();
        this.initializeSkillsInput();
    }

    initializeEventListeners() {
        this.prevBtn.addEventListener('click', () => this.previousStep());
        this.nextBtn.addEventListener('click', () => this.nextStep());
    }

    initializeSkillsInput() {
        const skillInput = document.getElementById('skillInput');
        const skillTags = document.getElementById('skillTags');

        if (skillInput && skillTags) {
            // Gérer l'événement keydown au lieu de keypress
            skillInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault(); // Empêcher le comportement par défaut
                    const skill = skillInput.value.trim();
                    if (skill && !this.skills.has(skill)) {
                        this.addSkill(skill);
                        skillInput.value = '';
                    }
                }
            });

            // Ajouter aussi un gestionnaire pour le bouton d'ajout si présent
            const addSkillBtn = document.getElementById('addSkillBtn');
            if (addSkillBtn) {
                addSkillBtn.addEventListener('click', () => {
                    const skill = skillInput.value.trim();
                    if (skill && !this.skills.has(skill)) {
                        this.addSkill(skill);
                        skillInput.value = '';
                    }
                });
            }
        }
    }

    addSkill(skill) {
        const skillTags = document.getElementById('skillTags');
        this.skills.add(skill);
        
        const tag = document.createElement('div');
        tag.className = 'skill-tag group flex items-center';
        tag.innerHTML = `
            <span>${skill}</span>
            <button class="ml-2 text-blue-600 hover:text-blue-800 focus:outline-none" 
                    onclick="window.stepsManager.removeSkill('${skill}')">
                <i class="fas fa-times"></i>
            </button>
        `;
        skillTags.appendChild(tag);
    }

    removeSkill(skill) {
        const skillTags = document.getElementById('skillTags');
        const tag = Array.from(skillTags.children)
            .find(el => el.textContent.trim() === skill);
        
        if (tag) {
            tag.remove();
            this.skills.delete(skill);
        }
    }

    updateStepVisuals() {
        // Mise à jour des indicateurs d'étape
        this.steps.forEach((step, index) => {
            if (index + 1 === this.currentStep) {
                step.classList.add('active');
                step.classList.remove('completed');
            } else if (index + 1 < this.currentStep) {
                step.classList.remove('active');
                step.classList.add('completed');
            } else {
                step.classList.remove('active', 'completed');
            }
        });

        // Mise à jour des lignes de progression
        this.lines.forEach((line, index) => {
            if (index + 1 < this.currentStep) {
                line.classList.add('active');
            } else {
                line.classList.remove('active');
            }
        });

        // Mise à jour du contenu visible
        this.contents.forEach((content, index) => {
            if (index + 1 === this.currentStep) {
                content.classList.add('active');
            } else {
                content.classList.remove('active');
            }
        });

        // Mise à jour des boutons de navigation
        this.prevBtn.style.display = this.currentStep > 1 ? 'block' : 'none';
        this.nextBtn.textContent = this.currentStep === this.totalSteps ? 'Terminer' : 'Suivant';
    }

    validateStep1() {
        const title = document.getElementById('jobTitle').value.trim();
        const department = document.getElementById('department').value;
        const description = document.getElementById('jobDescription').value.trim();
        const skills = window.skillManager ? window.skillManager.getSkills() : [];

        if (!title) {
            alert('Veuillez saisir le titre du poste');
            document.getElementById('jobTitle').focus();
            return false;
        }

        if (!department) {
            alert('Veuillez sélectionner un département');
            document.getElementById('department').focus();
            return false;
        }

        if (!description) {
            alert('Veuillez saisir une description du poste');
            document.getElementById('jobDescription').focus();
            return false;
        }

        if (skills.length === 0) {
            alert('Veuillez ajouter au moins une compétence requise');
            document.getElementById('skillInput').focus();
            return false;
        }

        // Sauvegarder les données
        const jobData = {
            title,
            department,
            description,
            skills,
            experience: document.getElementById('experience').value
        };

        // Stocker les données pour une utilisation ultérieure
        localStorage.setItem('jobOffer', JSON.stringify(jobData));
        return true;
    }

    async validateCurrentStep() {
        switch (this.currentStep) {
            case 1:
                return this.validateStep1();

            case 2: // Import CVs
                if (matcher.cvList.length === 0) {
                    alert('Veuillez importer au moins un CV');
                    return false;
                }
                return true;

            case 3: // Vérification
                this.updateVerificationView();
                return true;

            case 4: // Résultats
                return true;

            default:
                return false;
        }
    }

    updateVerificationView() {
        const jobOffer = {
            title: document.getElementById('jobTitle').value,
            department: document.getElementById('department').value,
            description: document.getElementById('jobDescription').value,
            skills: Array.from(document.querySelectorAll('.skill-tag')).map(tag => tag.textContent.trim()),
            experience: document.getElementById('experience').value
        };

        const cvFiles = window.cvUploader ? window.cvUploader.getUploadedFiles() : [];
        
        // Résumé de l'offre
        document.getElementById('jobSummary').innerHTML = `
            <div class="space-y-4">
                <div class="flex items-center justify-between">
                    <h4 class="text-lg font-semibold text-gray-900">${jobOffer.title || 'Titre non spécifié'}</h4>
                    <span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                        ${jobOffer.department || 'Département non spécifié'}
                    </span>
                </div>
                
                <div class="bg-gray-50 p-4 rounded-lg">
                    <h5 class="font-medium text-gray-700 mb-2">Description</h5>
                    <p class="text-gray-600">${jobOffer.description || 'Aucune description fournie'}</p>
                </div>

                <div>
                    <h5 class="font-medium text-gray-700 mb-2">Compétences requises</h5>
                    <div class="flex flex-wrap gap-2">
                        ${jobOffer.skills.map(skill => `
                            <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-50 text-blue-700">
                                <i class="fas fa-check-circle mr-1"></i>
                                ${skill}
                            </span>
                        `).join('') || '<span class="text-gray-500">Aucune compétence spécifiée</span>'}
                    </div>
                </div>

                <div class="flex items-center mt-2">
                    <i class="fas fa-clock text-gray-400 mr-2"></i>
                    <span class="text-gray-600">
                        Expérience requise : ${this.formatExperience(jobOffer.experience)}
                    </span>
                </div>
            </div>
        `;

        // Liste des CVs
        document.getElementById('cvSummary').innerHTML = `
            <div class="space-y-4">
                <div class="flex items-center justify-between mb-4">
                    <span class="text-lg font-medium text-gray-900">
                        ${cvFiles.length} CV(s) à analyser
                    </span>
                    <span class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                        Prêt pour l'analyse
                    </span>
                </div>

                ${cvFiles.map(cv => `
                    <div class="flex items-center justify-between p-4 bg-white rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
                        <div class="flex items-center space-x-4">
                            <div class="p-2 bg-gray-50 rounded-lg">
                                <i class="fas fa-file-${cv.type.includes('pdf') ? 'pdf text-red-500' : 'word text-blue-500'} text-xl"></i>
                            </div>
                            <div>
                                <p class="font-medium text-gray-900">${cv.name}</p>
                                <p class="text-sm text-gray-500">${this.formatFileSize(cv.size)}</p>
                            </div>
                        </div>
                        <div class="flex items-center space-x-2">
                            <button onclick="window.cvUploader.previewFile('${cv.name}')" 
                                    class="p-1 hover:text-blue-600 transition-colors" 
                                    title="Aperçu">
                                <i class="fas fa-eye"></i>
                            </button>
                        </div>
                    </div>
                `).join('') || `
                    <div class="text-center py-8 bg-gray-50 rounded-lg">
                        <i class="fas fa-file-upload text-gray-400 text-3xl mb-3"></i>
                        <p class="text-gray-500">Aucun CV importé</p>
                    </div>
                `}
            </div>
        `;
    }

    formatExperience(years) {
        const yearsNum = parseInt(years);
        if (yearsNum === 0) return "0-2 ans (Junior)";
        if (yearsNum === 2) return "2-5 ans (Intermédiaire)";
        if (yearsNum === 5) return "5+ ans (Senior)";
        return `${yearsNum} ans`;
    }

    editJobOffer() {
        this.currentStep = 1;
        this.updateStepVisuals();
    }

    editCVs() {
        this.currentStep = 2;
        this.updateStepVisuals();
    }
    }

    async showResults() {
        try {
            // Afficher l'état de chargement
            document.getElementById('analysisLoading').classList.remove('hidden');
            document.getElementById('analysisResults').classList.add('hidden');

            const results = await fetch('/analyze_cvs', {
                method: 'POST',
                body: JSON.stringify({
                    jobOffer: {
                        title: document.getElementById('jobTitle').value,
                        department: document.getElementById('department').value,
                        description: document.getElementById('jobDescription').value,
                        skills: Array.from(document.querySelectorAll('.skill-tag')).map(tag => tag.textContent.trim()),
                        experience: document.getElementById('experience').value
                    },
                    cvs: window.cvUploader ? window.cvUploader.getUploadedFiles() : []
                })
            }).then(response => response.json());

            // Métriques globales
            document.getElementById('globalMetrics').innerHTML = `
                <div class="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg text-center">
                    <p class="text-sm text-blue-600 mb-1">Score moyen</p>
                    <p class="text-2xl font-bold text-blue-700">${(results.averageScore * 100).toFixed(1)}%</p>
                </div>
                <div class="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg text-center">
                    <p class="text-sm text-green-600 mb-1">Meilleur score</p>
                    <p class="text-2xl font-bold text-green-700">${(results.bestScore * 100).toFixed(1)}%</p>
                </div>
            `;

            // Classement des candidats
            document.getElementById('candidateRanking').innerHTML = results.candidates
                .map((candidate, index) => `
                    <div class="p-6 ${index === 0 ? 'bg-gradient-to-r from-yellow-50 to-yellow-100 border-l-4 border-yellow-400' : 'bg-white'} rounded-lg shadow-sm hover:shadow-md transition-shadow mb-4">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-4">
                                <div class="flex-shrink-0">
                                    ${index === 0 
                                        ? '<div class="w-10 h-10 bg-yellow-400 rounded-full flex items-center justify-center"><i class="fas fa-trophy text-white"></i></div>'
                                        : `<div class="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center text-gray-600">#${index + 1}</div>`
                                    }
                                </div>
                                <div>
                                    <h4 class="text-lg font-semibold ${index === 0 ? 'text-yellow-700' : 'text-gray-900'}">${candidate.name}</h4>
                                    <div class="flex items-center mt-1">
                                        <div class="text-sm px-2 py-1 rounded ${index === 0 ? 'bg-yellow-200 text-yellow-800' : 'bg-blue-100 text-blue-800'}">
                                            Match global: ${(candidate.score * 100).toFixed(1)}%
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="text-right">
                                <div class="space-y-2">
                                    <div class="flex items-center justify-end">
                                        <span class="text-sm text-gray-600 mr-2">Compétences</span>
                                        <div class="w-24 bg-gray-200 rounded-full h-2">
                                            <div class="bg-green-500 h-2 rounded-full" style="width: ${candidate.skillsScore * 100}%"></div>
                                        </div>
                                        <span class="text-sm font-medium text-gray-700 ml-2">${(candidate.skillsScore * 100).toFixed(0)}%</span>
                                    </div>
                                    <div class="flex items-center justify-end">
                                        <span class="text-sm text-gray-600 mr-2">Expérience</span>
                                        <div class="w-24 bg-gray-200 rounded-full h-2">
                                            <div class="bg-blue-500 h-2 rounded-full" style="width: ${candidate.experienceScore * 100}%"></div>
                                        </div>
                                        <span class="text-sm font-medium text-gray-700 ml-2">${(candidate.experienceScore * 100).toFixed(0)}%</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        ${index === 0 ? `
                            <div class="mt-4 p-4 bg-yellow-50 rounded-lg">
                                <h5 class="font-medium text-yellow-800 mb-2">Points forts</h5>
                                <div class="flex flex-wrap gap-2">
                                    ${candidate.details.matchingSkills.map(skill => `
                                        <span class="px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm">
                                            <i class="fas fa-check-circle mr-1"></i>${skill}
                                        </span>
                                    `).join('')}
                                </div>
                            </div>
                        ` : ''}
                    </div>
                `).join('');

            // Initialisation des graphiques
            const ctx1 = document.getElementById('scoreDistribution').getContext('2d');
            new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%'],
                    datasets: [{
                        label: 'Nombre de CVs',
                        data: results.scoreDistribution,
                        backgroundColor: [
                            'rgba(239, 68, 68, 0.5)',  // red
                            'rgba(245, 158, 11, 0.5)', // orange
                            'rgba(16, 185, 129, 0.5)', // green
                            'rgba(59, 130, 246, 0.5)', // blue
                            'rgba(99, 102, 241, 0.5)'  // indigo
                        ],
                        borderColor: [
                            'rgb(239, 68, 68)',
                            'rgb(245, 158, 11)',
                            'rgb(16, 185, 129)',
                            'rgb(59, 130, 246)',
                            'rgb(99, 102, 241)'
                        ],
                        borderWidth: 1,
                        borderRadius: 8,
                        maxBarThickness: 50
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            padding: 12,
                            titleFont: {
                                size: 14,
                                weight: 'bold'
                            },
                            bodyFont: {
                                size: 13
                            },
                            displayColors: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1,
                                font: {
                                    size: 12
                                }
                            },
                            grid: {
                                display: true,
                                color: 'rgba(0, 0, 0, 0.05)'
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            },
                            ticks: {
                                font: {
                                    size: 12
                                }
                            }
                        }
                    }
                }
            });

            const ctx2 = document.getElementById('skillsComparison').getContext('2d');
            new Chart(ctx2, {
                type: 'radar',
                data: {
                    labels: results.skillsAnalysis.labels,
                    datasets: [{
                        label: 'Requis',
                        data: results.skillsAnalysis.required,
                        backgroundColor: 'rgba(59, 130, 246, 0.2)',
                        borderColor: 'rgb(59, 130, 246)',
                        pointBackgroundColor: 'rgb(59, 130, 246)',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: 'rgb(59, 130, 246)',
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }, {
                        label: 'Trouvé (moyenne)',
                        data: results.skillsAnalysis.found,
                        backgroundColor: 'rgba(16, 185, 129, 0.2)',
                        borderColor: 'rgb(16, 185, 129)',
                        pointBackgroundColor: 'rgb(16, 185, 129)',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: 'rgb(16, 185, 129)',
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                            labels: {
                                padding: 20,
                                font: {
                                    size: 12
                                },
                                usePointStyle: true,
                                pointStyle: 'circle'
                            }
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            padding: 12,
                            titleFont: {
                                size: 14,
                                weight: 'bold'
                            },
                            bodyFont: {
                                size: 13
                            }
                        }
                    },
                    scales: {
                        r: {
                            angleLines: {
                                display: true,
                                color: 'rgba(0, 0, 0, 0.05)'
                            },
                            suggestedMin: 0,
                            suggestedMax: 1,
                            ticks: {
                                stepSize: 0.2,
                                font: {
                                    size: 11
                                },
                                backdropColor: 'transparent'
                            },
                            grid: {
                                color: 'rgba(0, 0, 0, 0.05)'
                            },
                            pointLabels: {
                                font: {
                                    size: 12,
                                    weight: '500'
                                }
                            }
                        }
                    }
                }
            });

            // Cacher le chargement et afficher les résultats
            document.getElementById('analysisLoading').classList.add('hidden');
            document.getElementById('analysisResults').classList.remove('hidden');

        } catch (error) {
            console.error('Erreur lors de l\'affichage des résultats:', error);
            alert('Une erreur est survenue lors de l\'analyse des CVs.');
        }
    }

    initializeCharts(results) {
        // Distribution des scores
        const ctx1 = document.getElementById('scoreDistribution').getContext('2d');
        new Chart(ctx1, {
            type: 'bar',
            data: {
                labels: ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%'],
                datasets: [{
                    label: 'Nombre de CVs',
                    data: results.scoreDistribution,
                    backgroundColor: [
                        'rgba(239, 68, 68, 0.5)',
                        'rgba(245, 158, 11, 0.5)',
                        'rgba(16, 185, 129, 0.5)',
                        'rgba(59, 130, 246, 0.5)',
                        'rgba(99, 102, 241, 0.5)'
                    ],
                    borderColor: [
                        'rgb(239, 68, 68)',
                        'rgb(245, 158, 11)',
                        'rgb(16, 185, 129)',
                        'rgb(59, 130, 246)',
                        'rgb(99, 102, 241)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });

        // Comparaison des compétences
        const ctx2 = document.getElementById('skillsComparison').getContext('2d');
        new Chart(ctx2, {
            type: 'radar',
            data: {
                labels: results.skillsAnalysis.labels,
                datasets: [{
                    label: 'Requis',
                    data: results.skillsAnalysis.required,
                    backgroundColor: 'rgba(59, 130, 246, 0.2)',
                    borderColor: 'rgb(59, 130, 246)',
                    pointBackgroundColor: 'rgb(59, 130, 246)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(59, 130, 246)'
                }, {
                    label: 'Trouvé (moyenne)',
                    data: results.skillsAnalysis.found,
                    backgroundColor: 'rgba(16, 185, 129, 0.2)',
                    borderColor: 'rgb(16, 185, 129)',
                    pointBackgroundColor: 'rgb(16, 185, 129)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(16, 185, 129)'
                }]
            },
            options: {
                responsive: true,
                elements: {
                    line: {
                        borderWidth: 3
                    }
                }
            }
        });
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    async previousStep() {
        if (this.currentStep > 1) {
            this.currentStep--;
            this.updateStepVisuals();
        }
    }

    async nextStep() {
        try {
            // Désactiver le bouton pendant la validation
            this.nextBtn.disabled = true;
            this.nextBtn.innerHTML = `
                <div class="flex items-center">
                    <div class="animate-spin mr-2 h-4 w-4 border-2 border-white border-t-transparent rounded-full"></div>
                    <span>Validation...</span>
                </div>
            `;

            // Valider l'étape actuelle
            if (await this.validateCurrentStep()) {
                // Animation de transition
                const currentContent = document.getElementById(`step${this.currentStep}-content`);
                currentContent.style.opacity = '0';
                
                await new Promise(resolve => setTimeout(resolve, 300));

                if (this.currentStep < this.totalSteps) {
                    this.currentStep++;
                    this.updateStepVisuals();
                    
                    // Afficher la nouvelle étape avec animation
                    const nextContent = document.getElementById(`step${this.currentStep}-content`);
                    nextContent.style.opacity = '0';
                    nextContent.classList.remove('hidden');
                    setTimeout(() => {
                        nextContent.style.opacity = '1';
                    }, 50);

                    if (this.currentStep === 4) {
                        await this.showResults();
                    }
                } else {
                    // Terminer l'analyse
                    window.location.href = '/dashboard';
                }
            }
        } catch (error) {
            console.error('Erreur lors de la navigation:', error);
            alert('Une erreur est survenue lors du changement d\'étape.');
        } finally {
            // Réactiver le bouton
            this.nextBtn.disabled = false;
            this.nextBtn.innerHTML = `
                <span>Suivant</span>
                <i class="fas fa-arrow-right ml-2"></i>
            `;
        }
    }
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    window.stepsManager = new AnalysisStepsManager();
});