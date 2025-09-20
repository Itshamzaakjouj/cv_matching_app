import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Users, BarChart3, TrendingUp, Award, Plus } from 'lucide-react';
import { useData } from '../contexts/DataContext';
import Chart from '../components/Chart';

const Comparison: React.FC = () => {
  const { cvs, getComparisonData, getRadarChartData, getBarChartData, loading } = useData();
  const [selectedCVs, setSelectedCVs] = useState<string[]>([]);
  const [comparisonData, setComparisonData] = useState<any>(null);
  const [radarData, setRadarData] = useState<any>(null);
  const [barData, setBarData] = useState<any>(null);

  useEffect(() => {
    if (selectedCVs.length >= 2) {
      loadComparisonData();
    }
  }, [selectedCVs]);

  const loadComparisonData = async () => {
    try {
      const [comparison, radar, bar] = await Promise.all([
        getComparisonData(selectedCVs),
        getRadarChartData(selectedCVs),
        getBarChartData(selectedCVs)
      ]);
      
      setComparisonData(comparison);
      setRadarData(radar);
      setBarData(bar);
    } catch (error) {
      console.error('Error loading comparison data:', error);
    }
  };

  const handleCVToggle = (cvName: string) => {
    if (selectedCVs.includes(cvName)) {
      setSelectedCVs(selectedCVs.filter(name => name !== cvName));
    } else if (selectedCVs.length < 5) {
      setSelectedCVs([...selectedCVs, cvName]);
    }
  };

  const getBestCV = () => {
    if (!comparisonData?.comparison_data) return null;
    return comparisonData.comparison_data.reduce((best: any, current: any) => 
      current.score > best.score ? current : best
    );
  };

  const getWorstCV = () => {
    if (!comparisonData?.comparison_data) return null;
    return comparisonData.comparison_data.reduce((worst: any, current: any) => 
      current.score < worst.score ? current : worst
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl p-8 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">Comparaison des CVs</h1>
            <p className="text-purple-100 text-lg">
              Comparez et analysez les performances des candidats
            </p>
          </div>
          <div className="hidden md:block">
            <div className="w-32 h-32 bg-white/10 rounded-full flex items-center justify-center">
              <Users className="w-16 h-16 text-white" />
            </div>
          </div>
        </div>
      </div>

      {/* CV Selection */}
      <div className="bg-white rounded-2xl p-6 shadow-soft">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Sélectionner les CVs à comparer (2-5 CVs)
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {cvs.map((cv) => {
            const isSelected = selectedCVs.includes(cv.name);
            const canSelect = selectedCVs.length < 5 || isSelected;
            
            return (
              <motion.div
                key={cv.name}
                whileHover={{ scale: canSelect ? 1.02 : 1 }}
                whileTap={{ scale: canSelect ? 0.98 : 1 }}
                onClick={() => canSelect && handleCVToggle(cv.name)}
                className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                  isSelected
                    ? 'border-purple-500 bg-purple-50'
                    : canSelect
                    ? 'border-gray-200 hover:border-gray-300'
                    : 'border-gray-200 bg-gray-50 cursor-not-allowed opacity-50'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-medium text-gray-900">{cv.person}</h3>
                  <div className={`w-4 h-4 rounded-full border-2 ${
                    isSelected
                      ? 'border-purple-500 bg-purple-500'
                      : 'border-gray-300'
                  }`}>
                    {isSelected && (
                      <div className="w-full h-full rounded-full bg-white scale-50" />
                    )}
                  </div>
                </div>
                <p className="text-sm text-gray-600 mb-1">{cv.position}</p>
                <p className="text-xs text-gray-500 mb-2">{cv.level} • {cv.experience}</p>
                <div className="flex items-center justify-between">
                  <span className="text-lg font-bold text-gray-900">{cv.score}%</span>
                  <div className="w-16 bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-gradient-to-r from-purple-500 to-blue-500 h-2 rounded-full"
                      style={{ width: `${cv.score}%` }}
                    />
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* Comparison Results */}
      {selectedCVs.length >= 2 && comparisonData && (
        <div className="space-y-6">
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-2xl p-6 shadow-soft"
            >
              <div className="flex items-center space-x-3 mb-4">
                <div className="p-2 bg-green-100 rounded-lg">
                  <Award className="w-5 h-5 text-green-600" />
                </div>
                <h3 className="font-semibold text-gray-900">Meilleur CV</h3>
              </div>
              {getBestCV() && (
                <div>
                  <p className="text-lg font-bold text-gray-900">{getBestCV().person}</p>
                  <p className="text-sm text-gray-600">{getBestCV().position}</p>
                  <p className="text-2xl font-bold text-green-600 mt-2">{getBestCV().score}%</p>
                </div>
              )}
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-white rounded-2xl p-6 shadow-soft"
            >
              <div className="flex items-center space-x-3 mb-4">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <TrendingUp className="w-5 h-5 text-blue-600" />
                </div>
                <h3 className="font-semibold text-gray-900">Écart de Scores</h3>
              </div>
              {getBestCV() && getWorstCV() && (
                <div>
                  <p className="text-2xl font-bold text-blue-600">
                    {getBestCV().score - getWorstCV().score}%
                  </p>
                  <p className="text-sm text-gray-600">Différence max</p>
                </div>
              )}
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-white rounded-2xl p-6 shadow-soft"
            >
              <div className="flex items-center space-x-3 mb-4">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <Users className="w-5 h-5 text-purple-600" />
                </div>
                <h3 className="font-semibold text-gray-900">Nombre de CVs</h3>
              </div>
              <div>
                <p className="text-2xl font-bold text-purple-600">{selectedCVs.length}</p>
                <p className="text-sm text-gray-600">CVs comparés</p>
              </div>
            </motion.div>
          </div>

          {/* Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Radar Chart */}
            {radarData && (
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-white rounded-2xl p-6 shadow-soft"
              >
                <h3 className="text-lg font-semibold text-gray-900 mb-6">
                  Comparaison Radar
                </h3>
                <Chart
                  data={{
                    labels: radarData.categories,
                    datasets: radarData.data.map((item: any, index: number) => ({
                      label: item.name,
                      data: item.values,
                      borderColor: item.color,
                      backgroundColor: item.fillColor,
                      pointBackgroundColor: item.color,
                      pointBorderColor: '#fff',
                      pointHoverBackgroundColor: '#fff',
                      pointHoverBorderColor: item.color
                    }))
                  }}
                  type="line"
                  height={400}
                />
              </motion.div>
            )}

            {/* Bar Chart */}
            {barData && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-white rounded-2xl p-6 shadow-soft"
              >
                <h3 className="text-lg font-semibold text-gray-900 mb-6">
                  Comparaison par Catégorie
                </h3>
                <Chart
                  data={barData}
                  type="bar"
                  height={400}
                />
              </motion.div>
            )}
          </div>

          {/* Detailed Table */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl p-6 shadow-soft"
          >
            <h3 className="text-lg font-semibold text-gray-900 mb-6">
              Tableau de Comparaison Détaillé
            </h3>
            
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 font-medium text-gray-600">Candidat</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">Score Global</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">Compétences</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">Expérience</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">Formation</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">Niveau</th>
                  </tr>
                </thead>
                <tbody>
                  {comparisonData.comparison_data
                    .sort((a: any, b: any) => b.score - a.score)
                    .map((cv: any, index: number) => (
                    <tr key={cv.name} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-3 px-4">
                        <div className="flex items-center space-x-3">
                          <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center text-white font-bold text-sm">
                            {index + 1}
                          </div>
                          <div>
                            <p className="font-medium text-gray-900">{cv.person}</p>
                            <p className="text-sm text-gray-500">{cv.position}</p>
                          </div>
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <span className="text-lg font-bold text-gray-900">{cv.score}%</span>
                      </td>
                      <td className="py-3 px-4">
                        <span className="text-sm text-gray-600">{cv.skills}%</span>
                      </td>
                      <td className="py-3 px-4">
                        <span className="text-sm text-gray-600">{cv.experience}%</span>
                      </td>
                      <td className="py-3 px-4">
                        <span className="text-sm text-gray-600">{cv.education}%</span>
                      </td>
                      <td className="py-3 px-4">
                        <span className="text-sm text-gray-600">{cv.level}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </motion.div>
        </div>
      )}

      {/* Empty State */}
      {selectedCVs.length < 2 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl p-12 shadow-soft text-center"
        >
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Users className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Sélectionnez des CVs à comparer
          </h3>
          <p className="text-gray-600 mb-6">
            Choisissez au moins 2 CVs pour commencer la comparaison
          </p>
          <button
            onClick={() => setSelectedCVs(cvs.slice(0, 2).map(cv => cv.name))}
            className="btn-primary text-white px-6 py-2 rounded-lg font-medium"
          >
            Sélectionner automatiquement
          </button>
        </motion.div>
      )}
    </div>
  );
};

export default Comparison;

