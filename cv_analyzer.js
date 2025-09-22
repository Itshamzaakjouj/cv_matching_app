/**
 * Algorithme Dynamique d'Analyse CV-Offre d'Emploi
 * TalentScope - Ministère de l'Économie et des Finances
 */

class CVAnalyzer {
    constructor(jobOffer, weights) {
        this.jobOffer = jobOffer;
        this.weights = weights;
    }

    // Extraction du texte PDF (simulation pour l'instant)
    async extractTextFromPDF(file) {
        // Simulation de l'extraction PDF
        // Dans une vraie implémentation, on utiliserait pdfjs-dist
        return new Promise((resolve) => {
            setTimeout(() => {
                // Simulation de texte extrait basé sur le nom du fichier
                const fileName = file.name.toLowerCase();
                let simulatedText = '';
                
                if (fileName.includes('adam')) {
                    simulatedText = `
                        Adam Smith
                        Ingénieur en Informatique
                        Master en Data Science - Université de Paris
                        5 ans d'expérience en développement
                        Compétences: Python, JavaScript, React, Node.js, Machine Learning
                        Langues: Français (natif), Anglais (courant), Espagnol (intermédiaire)
                        Projets: Développement d'applications web, Analyse de données
                        Certifications: AWS, Google Cloud Platform
                    `;
                } else if (fileName.includes('ali')) {
                    simulatedText = `
                        Ali Benali
                        Développeur Full Stack
                        Licence en Informatique - École Polytechnique
                        3 ans d'expérience en développement web
                        Compétences: Java, Spring Boot, Angular, MySQL, Docker
                        Langues: Français (natif), Anglais (avancé)
                        Projets: Applications e-commerce, API REST
                        Certifications: Oracle Java, Microsoft Azure
                    `;
                } else if (fileName.includes('hafsa')) {
                    simulatedText = `
                        Hafsa El Ghazouani
                        Analyste de Données
                        Master en Statistiques - Université Hassan II
                        4 ans d'expérience en analyse de données
                        Compétences: R, Python, SQL, Tableau, Power BI
                        Langues: Français (natif), Anglais (courant), Arabe (natif)
                        Projets: Tableaux de bord, Modèles prédictifs
                        Certifications: Microsoft Data Analyst, Google Analytics
                    `;
                } else {
                    // CV générique
                    simulatedText = `
                        Candidat Générique
                        ${this.jobOffer.departement}
                        Formation en ${this.jobOffer.departement}
                        2 ans d'expérience
                        Compétences: ${this.jobOffer.competencesRequises.join(', ')}
                        Langues: Français, Anglais
                        Projets: Divers projets dans le domaine
                    `;
                }
                
                resolve(simulatedText.toLowerCase());
            }, 1000); // Simulation d'un délai d'extraction
        });
    }

    // Analyse de la formation
    analyzeFormation(cvText) {
        const formationKeywords = [
            'master', 'ingénieur', 'licence', 'bac+', 'diplôme', 'université',
            'école', 'formation', 'cursus', 'études', 'doctorat', 'phd',
            'informatique', 'data science', 'machine learning', 'statistiques',
            'polytechnique', 'hassan ii', 'paris', 'engineering', 'computer science'
        ];

        const jobKeywords = this.extractKeywordsFromJob('formation');
        const matches = [];
        let score = 0;

        // Vérification des mots-clés de formation
        formationKeywords.forEach(keyword => {
            if (cvText.includes(keyword)) {
                matches.push(keyword);
                score += 10;
            }
        });

        // Bonus si formation correspond au domaine du poste
        jobKeywords.forEach(keyword => {
            if (cvText.includes(keyword.toLowerCase())) {
                matches.push(keyword);
                score += 20;
            }
        });

        // Bonus pour formations prestigieuses
        if (cvText.includes('polytechnique') || cvText.includes('paris')) {
            score += 15;
            matches.push('Formation prestigieuse');
        }

        return {
            score: Math.min(score, 100),
            matches: matches.slice(0, 5)
        };
    }

    // Analyse de l'expérience
    analyzeExperience(cvText) {
        const experienceKeywords = [
            'expérience', 'ans', 'année', 'mois', 'stage', 'emploi',
            'poste', 'fonction', 'responsable', 'développeur', 'analyste',
            'chef de projet', 'lead', 'senior', 'junior'
        ];

        const matches = [];
        let score = 0;

        // Extraction des années d'expérience
        const yearMatches = cvText.match(/(\d+)\s*(ans?|années?)/g);
        if (yearMatches) {
            const totalYears = yearMatches
                .map(match => parseInt(match.match(/\d+/)?.[0] || '0'))
                .reduce((sum, years) => sum + years, 0);

            // Score basé sur l'expérience requise
            const requiredExp = this.extractRequiredExperience();
            if (totalYears >= requiredExp.min && totalYears <= requiredExp.max) {
                score += 80;
                matches.push(`${totalYears} ans d'expérience (optimal)`);
            } else if (totalYears >= requiredExp.min) {
                score += 60;
                matches.push(`${totalYears} ans d'expérience (surqualifié)`);
            } else {
                score += Math.min(totalYears * 20, 40);
                matches.push(`${totalYears} ans d'expérience (insuffisant)`);
            }
        }

        // Vérification des mots-clés d'expérience
        experienceKeywords.forEach(keyword => {
            if (cvText.includes(keyword)) {
                matches.push(keyword);
                score += 5;
            }
        });

        // Bonus pour expérience senior
        if (cvText.includes('senior') || cvText.includes('chef de projet')) {
            score += 15;
            matches.push('Expérience senior');
        }

        return {
            score: Math.min(score, 100),
            matches: matches.slice(0, 5)
        };
    }

    // Analyse des compétences techniques
    analyzeSkills(cvText) {
        const requiredSkills = this.jobOffer.competencesRequises.map(s => s.toLowerCase());
        const matches = [];
        let score = 0;
        let foundSkills = 0;

        requiredSkills.forEach(skill => {
            if (cvText.includes(skill)) {
                matches.push(skill);
                foundSkills++;
                score += 100 / requiredSkills.length; // Score proportionnel
            }
        });

        // Bonus pour compétences techniques générales
        const technicalKeywords = [
            'programmation', 'développement', 'logiciel', 'base de données',
            'algorithme', 'architecture', 'framework', 'api', 'cloud',
            'docker', 'kubernetes', 'git', 'agile', 'scrum'
        ];

        technicalKeywords.forEach(keyword => {
            if (cvText.includes(keyword)) {
                matches.push(keyword);
                score += 5;
            }
        });

        // Bonus pour certifications
        const certifications = ['aws', 'azure', 'google cloud', 'oracle', 'microsoft'];
        certifications.forEach(cert => {
            if (cvText.includes(cert)) {
                matches.push(`Certification ${cert}`);
                score += 10;
            }
        });

        return {
            score: Math.min(score, 100),
            matches: matches.slice(0, 8)
        };
    }

    // Analyse des langues
    analyzeLanguages(cvText) {
        const languages = [
            'français', 'anglais', 'espagnol', 'allemand', 'italien',
            'arabe', 'chinois', 'russe', 'portugais'
        ];

        const levels = ['natif', 'courant', 'avancé', 'intermédiaire', 'débutant'];
        const matches = [];
        let score = 0;
        let languageCount = 0;

        languages.forEach(lang => {
            if (cvText.includes(lang)) {
                matches.push(lang);
                languageCount++;
                
                // Bonus si niveau spécifié
                levels.forEach(level => {
                    if (cvText.includes(`${lang} ${level}`) || cvText.includes(`${level} ${lang}`)) {
                        score += 15;
                        matches.push(`${lang} (${level})`);
                    }
                });
                
                score += 20;
            }
        });

        // Score de base pour multilingue
        if (languageCount >= 2) score += 20;
        if (languageCount >= 3) score += 30;

        // Bonus pour langues internationales
        if (cvText.includes('anglais')) {
            score += 10;
            matches.push('Anglais (important)');
        }

        return {
            score: Math.min(score, 100),
            matches: matches.slice(0, 5)
        };
    }

    // Extraction des mots-clés du poste
    extractKeywordsFromJob(category) {
        const text = `${this.jobOffer.titre} ${this.jobOffer.description}`.toLowerCase();
        
        switch (category) {
            case 'formation':
                return text.match(/\b(master|ingénieur|licence|informatique|data|science|statistiques)\b/g) || [];
            default:
                return [];
        }
    }

    // Extraction de l'expérience requise
    extractRequiredExperience() {
        const expText = this.jobOffer.experienceRequise.toLowerCase();
        
        if (expText.includes('débutant')) return { min: 0, max: 2 };
        if (expText.includes('intermédiaire')) return { min: 2, max: 5 };
        if (expText.includes('senior')) return { min: 5, max: 15 };
        
        // Extraction des nombres
        const numbers = expText.match(/\d+/g);
        if (numbers && numbers.length >= 2) {
            return { min: parseInt(numbers[0]), max: parseInt(numbers[1]) };
        }
        
        return { min: 2, max: 5 }; // Défaut
    }

    // Analyse complète d'un CV
    async analyzeCV(file) {
        try {
            const extractedText = await this.extractTextFromPDF(file);
            
            const formationAnalysis = this.analyzeFormation(extractedText);
            const experienceAnalysis = this.analyzeExperience(extractedText);
            const skillsAnalysis = this.analyzeSkills(extractedText);
            const languagesAnalysis = this.analyzeLanguages(extractedText);

            // Calcul du score total pondéré
            const totalScore = (
                (formationAnalysis.score * this.weights.formation / 100) +
                (experienceAnalysis.score * this.weights.experience / 100) +
                (skillsAnalysis.score * this.weights.competencesTechniques / 100) +
                (languagesAnalysis.score * this.weights.langues / 100)
            );

            // Génération de recommandations
            const recommendations = this.generateRecommendations({
                formation: formationAnalysis.score,
                experience: experienceAnalysis.score,
                competencesTechniques: skillsAnalysis.score,
                langues: languagesAnalysis.score
            });

            return {
                candidateId: `candidate_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
                fileName: file.name,
                extractedText: extractedText.substring(0, 500) + '...',
                scores: {
                    formation: Math.round(formationAnalysis.score),
                    experience: Math.round(experienceAnalysis.score),
                    competencesTechniques: Math.round(skillsAnalysis.score),
                    langues: Math.round(languagesAnalysis.score),
                    total: Math.round(totalScore)
                },
                matchDetails: {
                    formationMatch: formationAnalysis.matches,
                    experienceMatch: experienceAnalysis.matches,
                    competencesMatch: skillsAnalysis.matches,
                    languesMatch: languagesAnalysis.matches
                },
                recommendations
            };
        } catch (error) {
            console.error('Erreur lors de l\'analyse du CV:', error);
            throw new Error(`Impossible d'analyser le CV ${file.name}`);
        }
    }

    // Génération de recommandations
    generateRecommendations(scores) {
        const recommendations = [];
        
        if (scores.formation < 50) {
            recommendations.push("Formation insuffisante pour le poste");
        }
        if (scores.experience < 40) {
            recommendations.push("Manque d'expérience dans le domaine");
        }
        if (scores.competencesTechniques < 60) {
            recommendations.push("Compétences techniques à renforcer");
        }
        if (scores.langues < 30) {
            recommendations.push("Compétences linguistiques limitées");
        }
        
        if (scores.formation >= 80 && scores.experience >= 70) {
            recommendations.push("Profil très prometteur");
        }
        
        if (scores.total >= 85) {
            recommendations.push("Excellent candidat pour le poste");
        } else if (scores.total >= 70) {
            recommendations.push("Bon candidat avec potentiel");
        } else if (scores.total >= 50) {
            recommendations.push("Candidat acceptable avec formation");
        } else {
            recommendations.push("Profil nécessitant une évaluation approfondie");
        }
        
        return recommendations;
    }
}

// Fonction utilitaire pour analyser tous les CVs
async function analyzeAllCVs(jobOffer, weights, cvFiles) {
    if (!cvFiles || cvFiles.length === 0) return [];
    
    const analyzer = new CVAnalyzer(jobOffer, weights);
    const analysisResults = [];

    for (const file of cvFiles) {
        try {
            const result = await analyzer.analyzeCV(file);
            analysisResults.push(result);
        } catch (error) {
            console.error(`Erreur pour ${file.name}:`, error);
        }
    }

    // Tri par score décroissant
    analysisResults.sort((a, b) => b.scores.total - a.scores.total);
    return analysisResults;
}

// Export pour utilisation dans l'application
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CVAnalyzer, analyzeAllCVs };
}
