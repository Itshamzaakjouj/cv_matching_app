// ============================================================================
// SERVICE DE GESTION DE L'HISTORIQUE DES ANALYSES - TalentScope
// ============================================================================

class AnalysisHistoryService {
    constructor() {
        this.storageKey = 'talentscope_analysis_history';
        this.maxHistoryItems = 1000; // Limite d'éléments dans l'historique
        this.history = this.loadHistory();
        this.currentUser = this.getCurrentUser();
    }

    // Obtenir l'utilisateur actuel
    getCurrentUser() {
        if (window.userDatabase && window.userDatabase.getCurrentUser) {
            return window.userDatabase.getCurrentUser();
        }
        return {
            id: 'anonymous',
            fullName: 'Utilisateur Anonyme',
            email: 'anonymous@example.com'
        };
    }

    // Charger l'historique depuis le localStorage
    loadHistory() {
        try {
            const stored = localStorage.getItem(this.storageKey);
            if (stored) {
                const parsed = JSON.parse(stored);
                return Array.isArray(parsed) ? parsed : [];
            }
        } catch (error) {
            console.error('Erreur lors du chargement de l\'historique:', error);
        }
        return [];
    }

    // Sauvegarder l'historique dans le localStorage
    saveHistory() {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(this.history));
            return true;
        } catch (error) {
            console.error('Erreur lors de la sauvegarde de l\'historique:', error);
            return false;
        }
    }

    // Ajouter une nouvelle analyse à l'historique
    addAnalysis(analysisData) {
        const historyItem = {
            id: this.generateId(),
            timestamp: new Date().toISOString(),
            user: {
                id: this.currentUser.id || 'anonymous',
                name: this.currentUser.fullName || 'Utilisateur Anonyme',
                email: this.currentUser.email || 'anonymous@example.com'
            },
            analysis: {
                cvName: analysisData.cvName || 'CV sans nom',
                cvContent: analysisData.cvContent || '',
                jobDescription: analysisData.jobDescription || '',
                position: analysisData.position || 'Poste non spécifié',
                department: analysisData.department || 'Département non spécifié',
                score: analysisData.score || 0,
                status: analysisData.status || 'completed',
                duration: analysisData.duration || 0, // en secondes
                algorithm: analysisData.algorithm || 'default'
            },
            results: {
                compatibilityScore: analysisData.compatibilityScore || 0,
                skillsMatch: analysisData.skillsMatch || {},
                experienceMatch: analysisData.experienceMatch || {},
                recommendations: analysisData.recommendations || [],
                strengths: analysisData.strengths || [],
                weaknesses: analysisData.weaknesses || [],
                missingSkills: analysisData.missingSkills || [],
                additionalNotes: analysisData.additionalNotes || ''
            },
            metadata: {
                fileSize: analysisData.fileSize || 0,
                fileType: analysisData.fileType || 'unknown',
                processingTime: analysisData.processingTime || 0,
                version: '1.0.0'
            }
        };

        // Ajouter au début de l'historique (plus récent en premier)
        this.history.unshift(historyItem);

        // Limiter le nombre d'éléments
        if (this.history.length > this.maxHistoryItems) {
            this.history = this.history.slice(0, this.maxHistoryItems);
        }

        // Sauvegarder
        const saved = this.saveHistory();
        
        if (saved) {
            console.log('Analyse ajoutée à l\'historique:', historyItem.id);
            this.notifyHistoryUpdate();
        }

        return historyItem;
    }

    // Obtenir l'historique complet
    getHistory(filters = {}) {
        let filteredHistory = [...this.history];

        // Filtrer par utilisateur si spécifié
        if (filters.userId) {
            filteredHistory = filteredHistory.filter(item => item.user.id === filters.userId);
        }

        // Filtrer par date
        if (filters.startDate) {
            filteredHistory = filteredHistory.filter(item => 
                new Date(item.timestamp) >= new Date(filters.startDate)
            );
        }

        if (filters.endDate) {
            filteredHistory = filteredHistory.filter(item => 
                new Date(item.timestamp) <= new Date(filters.endDate)
            );
        }

        // Filtrer par score minimum
        if (filters.minScore) {
            filteredHistory = filteredHistory.filter(item => 
                item.analysis.score >= filters.minScore
            );
        }

        // Filtrer par statut
        if (filters.status) {
            filteredHistory = filteredHistory.filter(item => 
                item.analysis.status === filters.status
            );
        }

        // Filtrer par position
        if (filters.position) {
            filteredHistory = filteredHistory.filter(item => 
                item.analysis.position.toLowerCase().includes(filters.position.toLowerCase())
            );
        }

        // Trier par date (plus récent en premier)
        filteredHistory.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

        return filteredHistory;
    }

    // Obtenir une analyse spécifique par ID
    getAnalysisById(id) {
        return this.history.find(item => item.id === id);
    }

    // Supprimer une analyse de l'historique
    deleteAnalysis(id) {
        const index = this.history.findIndex(item => item.id === id);
        if (index !== -1) {
            const deleted = this.history.splice(index, 1)[0];
            this.saveHistory();
            this.notifyHistoryUpdate();
            console.log('Analyse supprimée de l\'historique:', id);
            return deleted;
        }
        return null;
    }

    // Supprimer tout l'historique
    clearAllHistory() {
        this.history = [];
        this.saveHistory();
        this.notifyHistoryUpdate();
        console.log('Historique complètement vidé');
    }

    // Supprimer l'historique d'un utilisateur spécifique
    clearUserHistory(userId) {
        this.history = this.history.filter(item => item.user.id !== userId);
        this.saveHistory();
        this.notifyHistoryUpdate();
        console.log(`Historique de l'utilisateur ${userId} supprimé`);
    }

    // Obtenir les statistiques de l'historique
    getStatistics() {
        const stats = {
            total: this.history.length,
            byUser: {},
            byStatus: {},
            byScore: {
                excellent: 0, // 90-100
                good: 0,      // 70-89
                average: 0,   // 50-69
                poor: 0       // 0-49
            },
            averageScore: 0,
            totalProcessingTime: 0,
            byMonth: {},
            byPosition: {}
        };

        if (this.history.length === 0) {
            return stats;
        }

        let totalScore = 0;

        this.history.forEach(item => {
            // Par utilisateur
            const userId = item.user.id;
            stats.byUser[userId] = (stats.byUser[userId] || 0) + 1;

            // Par statut
            const status = item.analysis.status;
            stats.byStatus[status] = (stats.byStatus[status] || 0) + 1;

            // Par score
            const score = item.analysis.score;
            totalScore += score;
            if (score >= 90) stats.byScore.excellent++;
            else if (score >= 70) stats.byScore.good++;
            else if (score >= 50) stats.byScore.average++;
            else stats.byScore.poor++;

            // Temps de traitement total
            stats.totalProcessingTime += item.analysis.duration || 0;

            // Par mois
            const month = new Date(item.timestamp).toISOString().substring(0, 7);
            stats.byMonth[month] = (stats.byMonth[month] || 0) + 1;

            // Par position
            const position = item.analysis.position;
            stats.byPosition[position] = (stats.byPosition[position] || 0) + 1;
        });

        stats.averageScore = Math.round(totalScore / this.history.length);

        return stats;
    }

    // Exporter l'historique en JSON
    exportHistory(format = 'json') {
        const data = {
            exportDate: new Date().toISOString(),
            version: '1.0.0',
            totalItems: this.history.length,
            history: this.history
        };

        if (format === 'json') {
            return JSON.stringify(data, null, 2);
        } else if (format === 'csv') {
            return this.convertToCSV(this.history);
        }

        return data;
    }

    // Convertir l'historique en CSV
    convertToCSV(history) {
        const headers = [
            'ID', 'Date', 'Utilisateur', 'Nom CV', 'Position', 'Score', 
            'Statut', 'Durée (s)', 'Score Compatibilité', 'Note'
        ];

        const rows = history.map(item => [
            item.id,
            new Date(item.timestamp).toLocaleString(),
            item.user.name,
            item.analysis.cvName,
            item.analysis.position,
            item.analysis.score,
            item.analysis.status,
            item.analysis.duration,
            item.results.compatibilityScore,
            item.results.additionalNotes
        ]);

        return [headers, ...rows].map(row => 
            row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(',')
        ).join('\n');
    }

    // Importer l'historique depuis un fichier JSON
    importHistory(jsonData) {
        try {
            const data = typeof jsonData === 'string' ? JSON.parse(jsonData) : jsonData;
            
            if (data.history && Array.isArray(data.history)) {
                // Fusionner avec l'historique existant
                this.history = [...data.history, ...this.history];
                
                // Supprimer les doublons basés sur l'ID
                const uniqueHistory = [];
                const seenIds = new Set();
                
                this.history.forEach(item => {
                    if (!seenIds.has(item.id)) {
                        seenIds.add(item.id);
                        uniqueHistory.push(item);
                    }
                });
                
                this.history = uniqueHistory;
                this.saveHistory();
                this.notifyHistoryUpdate();
                
                console.log(`${data.history.length} analyses importées avec succès`);
                return true;
            }
        } catch (error) {
            console.error('Erreur lors de l\'importation:', error);
        }
        return false;
    }

    // Générer un ID unique
    generateId() {
        return 'analysis_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // Notifier les composants de la mise à jour de l'historique
    notifyHistoryUpdate() {
        // Déclencher un événement personnalisé
        const event = new CustomEvent('analysisHistoryUpdated', {
            detail: {
                history: this.history,
                statistics: this.getStatistics()
            }
        });
        window.dispatchEvent(event);
    }

    // Rechercher dans l'historique
    searchHistory(query, fields = ['cvName', 'position', 'user.name']) {
        if (!query || query.trim() === '') {
            return this.history;
        }

        const searchTerm = query.toLowerCase();
        
        return this.history.filter(item => {
            return fields.some(field => {
                const value = this.getNestedValue(item, field);
                return value && value.toString().toLowerCase().includes(searchTerm);
            });
        });
    }

    // Obtenir une valeur imbriquée d'un objet
    getNestedValue(obj, path) {
        return path.split('.').reduce((current, key) => current && current[key], obj);
    }

    // Obtenir les analyses récentes (dernières 10)
    getRecentAnalyses(limit = 10) {
        return this.history.slice(0, limit);
    }

    // Obtenir les analyses avec le meilleur score
    getTopScoringAnalyses(limit = 10) {
        return [...this.history]
            .sort((a, b) => b.analysis.score - a.analysis.score)
            .slice(0, limit);
    }

    // Obtenir les analyses d'aujourd'hui
    getTodayAnalyses() {
        const today = new Date().toISOString().split('T')[0];
        return this.history.filter(item => 
            item.timestamp.startsWith(today)
        );
    }

    // Obtenir les analyses de cette semaine
    getThisWeekAnalyses() {
        const now = new Date();
        const startOfWeek = new Date(now.setDate(now.getDate() - now.getDay()));
        startOfWeek.setHours(0, 0, 0, 0);
        
        return this.history.filter(item => 
            new Date(item.timestamp) >= startOfWeek
        );
    }

    // Obtenir les analyses de ce mois
    getThisMonthAnalyses() {
        const now = new Date();
        const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
        
        return this.history.filter(item => 
            new Date(item.timestamp) >= startOfMonth
        );
    }
}

// Instance globale
window.AnalysisHistoryService = AnalysisHistoryService;

// Initialiser le service au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    if (!window.analysisHistoryService) {
        window.analysisHistoryService = new AnalysisHistoryService();
        console.log('Service d\'historique des analyses initialisé');
    }
});
