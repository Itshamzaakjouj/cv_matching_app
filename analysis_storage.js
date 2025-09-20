class AnalysisStorage {
    constructor() {
        this.storageKey = 'talentscope_analyses';
        this.initializeStorage();
    }

    initializeStorage() {
        if (!localStorage.getItem(this.storageKey)) {
            localStorage.setItem(this.storageKey, JSON.stringify({
                analyses: [],
                metrics: {
                    totalAnalyses: 0,
                    totalCVs: 0,
                    averageScore: 0,
                    successRate: 0
                },
                weeklyData: Array(8).fill(0),
                scoreDistribution: {
                    '0-20': 0,
                    '21-40': 0,
                    '41-60': 0,
                    '61-80': 0,
                    '81-100': 0
                }
            }));
        }
    }

    saveAnalysis(analysisData) {
        const storage = this.getStorage();
        const timestamp = new Date().toISOString();

        // Ajouter la nouvelle analyse
        const analysis = {
            id: this.generateId(),
            timestamp: timestamp,
            jobTitle: analysisData.jobData.title,
            department: analysisData.jobData.department,
            cvCount: analysisData.results.candidates.length,
            averageScore: analysisData.results.globalMetrics.averageScore,
            bestScore: analysisData.results.globalMetrics.bestScore,
            candidates: analysisData.results.candidates
        };

        storage.analyses.unshift(analysis);

        // Mettre à jour les métriques globales
        this.updateMetrics(storage, analysis);

        // Mettre à jour les données hebdomadaires
        this.updateWeeklyData(storage, analysis);

        // Mettre à jour la distribution des scores
        this.updateScoreDistribution(storage, analysis);

        // Sauvegarder les modifications
        localStorage.setItem(this.storageKey, JSON.stringify(storage));

        // Déclencher un événement pour notifier la mise à jour
        window.dispatchEvent(new CustomEvent('analysisDataUpdated'));
    }

    updateMetrics(storage, analysis) {
        const metrics = storage.metrics;
        metrics.totalAnalyses++;
        metrics.totalCVs += analysis.cvCount;
        
        // Calculer la nouvelle moyenne des scores
        const totalScore = storage.analyses.reduce((sum, a) => sum + a.averageScore, 0);
        metrics.averageScore = totalScore / storage.analyses.length;

        // Calculer le taux de réussite (scores > 60%)
        const successfulCandidates = storage.analyses.reduce((count, a) => 
            count + a.candidates.filter(c => c.score > 60).length, 0);
        const totalCandidates = storage.analyses.reduce((count, a) => 
            count + a.candidates.length, 0);
        metrics.successRate = (successfulCandidates / totalCandidates) * 100;
    }

    updateWeeklyData(storage, analysis) {
        // Obtenir l'index de la semaine actuelle (0-7)
        const currentWeek = new Date().getDay();
        storage.weeklyData[currentWeek]++;
    }

    updateScoreDistribution(storage, analysis) {
        analysis.candidates.forEach(candidate => {
            const score = candidate.score;
            if (score <= 20) storage.scoreDistribution['0-20']++;
            else if (score <= 40) storage.scoreDistribution['21-40']++;
            else if (score <= 60) storage.scoreDistribution['41-60']++;
            else if (score <= 80) storage.scoreDistribution['61-80']++;
            else storage.scoreDistribution['81-100']++;
        });
    }

    getStorage() {
        return JSON.parse(localStorage.getItem(this.storageKey));
    }

    generateId() {
        return 'analysis_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    getMetrics() {
        return this.getStorage().metrics;
    }

    getWeeklyData() {
        return this.getStorage().weeklyData;
    }

    getScoreDistribution() {
        return this.getStorage().scoreDistribution;
    }

    getRecentAnalyses(limit = 5) {
        return this.getStorage().analyses.slice(0, limit);
    }
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    window.analysisStorage = new AnalysisStorage();
});
