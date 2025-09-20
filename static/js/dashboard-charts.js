// Gestionnaire des graphiques du dashboard
class DashboardCharts {
    constructor() {
        this.charts = {};
        this.initializeCharts();
    }

    initializeCharts() {
        this.initializeTrendChart();
        this.initializeDistributionChart();
        this.initializeSkillsChart();
        this.initializeActivityChart();
    }

    initializeTrendChart() {
        const ctx = document.getElementById('trend-chart');
        if (!ctx) return;

        this.charts.trend = new Chart(ctx, {
            type: 'line',
            data: {
                labels: this.getLast7Days(),
                datasets: [{
                    label: 'Analyses',
                    data: [12, 19, 15, 17, 14, 15, 16],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4,
                    fill: true
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
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(255, 255, 255, 0.9)',
                        titleColor: '#1F2937',
                        bodyColor: '#1F2937',
                        borderColor: '#E5E7EB',
                        borderWidth: 1,
                        padding: 12,
                        boxPadding: 6,
                        usePointStyle: true
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: '#F3F4F6'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    initializeDistributionChart() {
        const ctx = document.getElementById('distribution-chart');
        if (!ctx) return;

        this.charts.distribution = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Excellent', 'Très bon', 'Bon', 'Moyen', 'À améliorer'],
                datasets: [{
                    data: [30, 25, 20, 15, 10],
                    backgroundColor: [
                        '#10B981', // Vert
                        '#667EEA', // Bleu
                        '#F59E0B', // Orange
                        '#EF4444', // Rouge
                        '#6B7280'  // Gris
                    ],
                    borderRadius: 6
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
                        backgroundColor: 'rgba(255, 255, 255, 0.9)',
                        titleColor: '#1F2937',
                        bodyColor: '#1F2937',
                        borderColor: '#E5E7EB',
                        borderWidth: 1
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: '#F3F4F6'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    initializeSkillsChart() {
        const ctx = document.getElementById('skills-chart');
        if (!ctx) return;

        this.charts.skills = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Python', 'Data Science', 'Machine Learning', 'Web Dev', 'DevOps', 'Cloud'],
                datasets: [{
                    label: 'Compétences demandées',
                    data: [90, 85, 80, 75, 70, 65],
                    backgroundColor: 'rgba(102, 126, 234, 0.2)',
                    borderColor: '#667eea',
                    pointBackgroundColor: '#667eea'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                elements: {
                    line: {
                        borderWidth: 2
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    r: {
                        angleLines: {
                            color: '#E5E7EB'
                        },
                        grid: {
                            color: '#F3F4F6'
                        },
                        pointLabels: {
                            font: {
                                size: 12
                            }
                        },
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                }
            }
        });
    }

    initializeActivityChart() {
        const ctx = document.getElementById('activity-chart');
        if (!ctx) return;

        this.charts.activity = new Chart(ctx, {
            type: 'line',
            data: {
                labels: this.getLast30Days(),
                datasets: [{
                    label: 'Analyses',
                    data: this.generateRandomData(30, 10, 30),
                    borderColor: '#10B981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: '#F3F4F6'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            maxTicksLimit: 10
                        }
                    }
                }
            }
        });
    }

    // Méthodes utilitaires
    getLast7Days() {
        return Array.from({length: 7}, (_, i) => {
            const d = new Date();
            d.setDate(d.getDate() - (6 - i));
            return d.toLocaleDateString('fr-FR', {weekday: 'short'});
        });
    }

    getLast30Days() {
        return Array.from({length: 30}, (_, i) => {
            const d = new Date();
            d.setDate(d.getDate() - (29 - i));
            return d.toLocaleDateString('fr-FR', {day: 'numeric', month: 'short'});
        });
    }

    generateRandomData(length, min, max) {
        return Array.from({length}, () => 
            Math.floor(Math.random() * (max - min + 1)) + min
        );
    }

    // Méthodes de mise à jour
    updateCharts(newData) {
        if (newData.trend) {
            this.updateTrendChart(newData.trend);
        }
        if (newData.distribution) {
            this.updateDistributionChart(newData.distribution);
        }
        if (newData.skills) {
            this.updateSkillsChart(newData.skills);
        }
        if (newData.activity) {
            this.updateActivityChart(newData.activity);
        }
    }

    updateTrendChart(data) {
        if (this.charts.trend) {
            this.charts.trend.data.datasets[0].data = data;
            this.charts.trend.update();
        }
    }

    updateDistributionChart(data) {
        if (this.charts.distribution) {
            this.charts.distribution.data.datasets[0].data = data;
            this.charts.distribution.update();
        }
    }

    updateSkillsChart(data) {
        if (this.charts.skills) {
            this.charts.skills.data.datasets[0].data = data;
            this.charts.skills.update();
        }
    }

    updateActivityChart(data) {
        if (this.charts.activity) {
            this.charts.activity.data.datasets[0].data = data;
            this.charts.activity.update();
        }
    }
}

// Initialiser les graphiques au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    window.dashboardCharts = new DashboardCharts();
});

