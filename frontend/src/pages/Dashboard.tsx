import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Users, 
  TrendingUp, 
  FileText, 
  Award,
  BarChart3,
  Activity,
  Clock,
  Star
} from 'lucide-react';
import { useData } from '../contexts/DataContext';
import MetricCard from '../components/MetricCard';
import Chart from '../components/Chart';
import RecentActivity from '../components/RecentActivity';

const Dashboard: React.FC = () => {
  const { dashboardData, loading, error, fetchDashboardData } = useData();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="loading-dots">
          <div></div>
          <div></div>
          <div></div>
          <div></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  const metrics = [
    {
      title: 'Total CVs',
      value: dashboardData?.total_cvs || 0,
      icon: FileText,
      color: 'blue',
      trend: '+12%',
      trendUp: true
    },
    {
      title: 'Score Moyen',
      value: `${dashboardData?.average_score || 0}%`,
      icon: TrendingUp,
      color: 'green',
      trend: '+5.2%',
      trendUp: true
    },
    {
      title: 'Analyses Récentes',
      value: dashboardData?.recent_analyses?.length || 0,
      icon: Activity,
      color: 'purple',
      trend: '+3',
      trendUp: true
    },
    {
      title: 'Meilleur Score',
      value: `${Math.max(...(dashboardData?.top_cvs?.map(cv => cv.score) || [0]))}%`,
      icon: Award,
      color: 'orange',
      trend: 'Record',
      trendUp: true
    }
  ];

  const chartData = {
    labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun'],
    datasets: [
      {
        label: 'CVs Analysés',
        data: [12, 19, 15, 25, 22, 30],
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4
      },
      {
        label: 'Score Moyen',
        data: [75, 78, 82, 85, 88, 90],
        borderColor: 'rgb(16, 185, 129)',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        tension: 0.4
      }
    ]
  };

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white"
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">Bienvenue sur TalentScope</h1>
            <p className="text-blue-100 text-lg">
              Gérez et analysez vos CVs avec intelligence artificielle
            </p>
          </div>
          <div className="hidden md:block">
            <div className="w-32 h-32 bg-white/10 rounded-full flex items-center justify-center">
              <BarChart3 className="w-16 h-16 text-white" />
            </div>
          </div>
        </div>
      </motion.div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {metrics.map((metric, index) => (
          <motion.div
            key={metric.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <MetricCard {...metric} />
          </motion.div>
        ))}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Performance Chart */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white rounded-2xl p-6 shadow-soft"
        >
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Performance des Analyses</h3>
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <Clock className="w-4 h-4" />
              <span>Dernières 6 semaines</span>
            </div>
          </div>
          <Chart data={chartData} type="line" height={300} />
        </motion.div>

        {/* Level Distribution */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white rounded-2xl p-6 shadow-soft"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Répartition par Niveau</h3>
          <div className="space-y-4">
            {Object.entries(dashboardData?.level_distribution || {}).map(([level, count], index) => {
              const total = Object.values(dashboardData?.level_distribution || {}).reduce((a, b) => a + b, 0);
              const percentage = total > 0 ? (count / total) * 100 : 0;
              
              return (
                <div key={level} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium text-gray-700">{level}</span>
                    <span className="text-sm text-gray-500">{count} CVs</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${percentage}%` }}
                      transition={{ delay: index * 0.1, duration: 0.8 }}
                      className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </motion.div>
      </div>

      {/* Top CVs and Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top CVs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl p-6 shadow-soft"
        >
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Top CVs</h3>
            <Star className="w-5 h-5 text-yellow-500" />
          </div>
          <div className="space-y-4">
            {dashboardData?.top_cvs?.slice(0, 3).map((cv, index) => (
              <motion.div
                key={cv.name}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center justify-between p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg"
              >
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white font-bold">
                    {index + 1}
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{cv.person}</p>
                    <p className="text-sm text-gray-500">{cv.position}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-bold text-lg text-gray-900">{cv.score}%</p>
                  <p className="text-xs text-gray-500">Score</p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Recent Activity */}
        <RecentActivity />
      </div>
    </div>
  );
};

export default Dashboard;

