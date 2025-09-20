class DashboardUpdater {
    constructor() {
        this.initializeEventListeners();
        this.updateDashboard();
    }

    initializeEventListeners() {
        // Écouter les mises à jour des analyses
        window.addEventListener('analysisDataUpdated', () => this.updateDashboard());
    }

    updateDashboard() {
        const metrics = window.analysisStorage.getMetrics();
        const weeklyData = window.analysisStorage.getWeeklyData();
        const scoreDistribution = window.analysisStorage.getScoreDistribution();

        // Mettre à jour les métriques
        this.updateMetricCard('analyses-count', metrics.totalAnalyses);
        this.updateMetricCard('cvs-count', metrics.totalCVs);
        this.updateMetricCard('average-score', metrics.averageScore.toFixed(1) + '%');
        this.updateMetricCard('success-rate', metrics.successRate.toFixed(1) + '%');

        // Mettre à jour les tendances
        this.updateTrendIndicator('analyses-trend', this.calculateTrend(weeklyData));
        this.updateTrendIndicator('cvs-trend', this.calculateTrend(weeklyData));
        this.updateTrendIndicator('score-trend', metrics.averageScore > 60 ? 1 : -1);
        this.updateTrendIndicator('success-trend', metrics.successRate > 70 ? 1 : -1);

        // Mettre à jour les graphiques
        this.updateAnalysisTrendChart(weeklyData);
        this.updateScoreDistributionChart(scoreDistribution);
    }

    updateMetricCard(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
            // Ajouter une animation de mise à jour
            element.classList.add('update-animation');
            setTimeout(() => element.classList.remove('update-animation'), 1000);
        }
    }

    updateTrendIndicator(id, trend) {
        const element = document.getElementById(id);
        if (element) {
            const trendText = trend > 0 ? '+' : '';
            element.textContent = `${trendText}${trend}% cette semaine`;
            element.className = `text-sm ${trend >= 0 ? 'text-green-600' : 'text-red-600'}`;
        }
    }

    calculateTrend(weeklyData) {
        // Calculer la tendance en comparant cette semaine avec la semaine précédente
        const currentWeek = new Date().getDay();
        const thisWeek = weeklyData[currentWeek];
        const lastWeek = weeklyData[(currentWeek - 1 + 7) % 7];
        
        if (lastWeek === 0) return 0;
        return Math.round(((thisWeek - lastWeek) / lastWeek) * 100);
    }

    updateAnalysisTrendChart(weeklyData) {
        const ctx = document.getElementById('analysisTrend');
        if (!ctx) return;

        const days = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'];
        const currentDay = new Date().getDay();
        const orderedDays = [...days.slice(currentDay), ...days.slice(0, currentDay)];

        if (!ctx.chart) {
            ctx.chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: orderedDays,
                    datasets: [{
                        label: 'Analyses',
                        data: weeklyData,
                        borderColor: 'rgb(59, 130, 246)',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        } else {
            ctx.chart.data.datasets[0].data = weeklyData;
            ctx.chart.update();
        }
    }

    updateScoreDistributionChart(distribution) {
        const ctx = document.getElementById('scoreDistribution');
        if (!ctx) return;

        const data = Object.values(distribution);
        const labels = ['0-20%', '21-40%', '41-60%', '61-80%', '81-100%'];

        if (!ctx.chart) {
            ctx.chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Nombre de CVs',
                        data: data,
                        backgroundColor: [
                            'rgba(239, 68, 68, 0.5)',   // Rouge
                            'rgba(245, 158, 11, 0.5)',  // Orange
                            'rgba(252, 211, 77, 0.5)',  // Jaune
                            'rgba(34, 197, 94, 0.5)',   // Vert
                            'rgba(59, 130, 246, 0.5)'   // Bleu
                        ],
                        borderColor: [
                            'rgb(239, 68, 68)',
                            'rgb(245, 158, 11)',
                            'rgb(252, 211, 77)',
                            'rgb(34, 197, 94)',
                            'rgb(59, 130, 246)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        } else {
            ctx.chart.data.datasets[0].data = data;
            ctx.chart.update();
        }
    }
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    window.dashboardUpdater = new DashboardUpdater();
});
