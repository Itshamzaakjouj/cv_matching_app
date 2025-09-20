import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FileText, Search, Filter, Download, Eye, Trash2, Plus } from 'lucide-react';
import { useData } from '../contexts/DataContext';

const ProcessedCVs: React.FC = () => {
  const { cvs, loading } = useData();
  const [searchTerm, setSearchTerm] = useState('');
  const [filterLevel, setFilterLevel] = useState('all');
  const [sortBy, setSortBy] = useState('score');

  const filteredCVs = cvs
    .filter(cv => 
      cv.person.toLowerCase().includes(searchTerm.toLowerCase()) ||
      cv.position.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .filter(cv => filterLevel === 'all' || cv.level === filterLevel)
    .sort((a, b) => {
      switch (sortBy) {
        case 'score':
          return b.score - a.score;
        case 'name':
          return a.person.localeCompare(b.person);
        case 'level':
          return a.level.localeCompare(b.level);
        default:
          return 0;
      }
    });

  const getLevelColor = (level: string) => {
    const colors = {
      'Junior': 'bg-green-100 text-green-800',
      'Intermédiaire': 'bg-blue-100 text-blue-800',
      'Senior': 'bg-purple-100 text-purple-800',
      'Expert': 'bg-orange-100 text-orange-800'
    };
    return colors[level as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 80) return 'text-blue-600';
    if (score >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-600 to-red-600 rounded-2xl p-8 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">CVs Traités</h1>
            <p className="text-orange-100 text-lg">
              Gérez et consultez tous vos CVs analysés
            </p>
          </div>
          <div className="hidden md:block">
            <div className="w-32 h-32 bg-white/10 rounded-full flex items-center justify-center">
              <FileText className="w-16 h-16 text-white" />
            </div>
          </div>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="bg-white rounded-2xl p-6 shadow-soft">
        <div className="flex flex-col lg:flex-row gap-4">
          {/* Search */}
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Rechercher par nom ou poste..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            />
          </div>

          {/* Level Filter */}
          <select
            value={filterLevel}
            onChange={(e) => setFilterLevel(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
          >
            <option value="all">Tous les niveaux</option>
            <option value="Junior">Junior</option>
            <option value="Intermédiaire">Intermédiaire</option>
            <option value="Senior">Senior</option>
            <option value="Expert">Expert</option>
          </select>

          {/* Sort */}
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
          >
            <option value="score">Trier par score</option>
            <option value="name">Trier par nom</option>
            <option value="level">Trier par niveau</option>
          </select>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-xl p-4 shadow-soft"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total CVs</p>
              <p className="text-2xl font-bold text-gray-900">{cvs.length}</p>
            </div>
            <FileText className="w-8 h-8 text-blue-600" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-xl p-4 shadow-soft"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Score Moyen</p>
              <p className="text-2xl font-bold text-gray-900">
                {Math.round(cvs.reduce((acc, cv) => acc + cv.score, 0) / cvs.length)}%
              </p>
            </div>
            <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
              <span className="text-green-600 font-bold">↑</span>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-xl p-4 shadow-soft"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Meilleur Score</p>
              <p className="text-2xl font-bold text-gray-900">
                {Math.max(...cvs.map(cv => cv.score))}%
              </p>
            </div>
            <div className="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center">
              <span className="text-yellow-600 font-bold">★</span>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-xl p-4 shadow-soft"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Filtrés</p>
              <p className="text-2xl font-bold text-gray-900">{filteredCVs.length}</p>
            </div>
            <Filter className="w-8 h-8 text-purple-600" />
          </div>
        </motion.div>
      </div>

      {/* CVs Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredCVs.map((cv, index) => (
          <motion.div
            key={cv.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-white rounded-2xl p-6 shadow-soft hover:shadow-medium transition-all duration-300"
          >
            {/* Header */}
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900 mb-1">{cv.person}</h3>
                <p className="text-sm text-gray-600 mb-2">{cv.position}</p>
                <div className="flex items-center space-x-2">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getLevelColor(cv.level)}`}>
                    {cv.level}
                  </span>
                  <span className="text-xs text-gray-500">{cv.experience}</span>
                </div>
              </div>
              <div className="text-right">
                <p className={`text-2xl font-bold ${getScoreColor(cv.score)}`}>
                  {cv.score}%
                </p>
                <p className="text-xs text-gray-500">Score</p>
              </div>
            </div>

            {/* Score Breakdown */}
            <div className="space-y-2 mb-4">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Compétences</span>
                <span className="font-medium">{cv.skills}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-blue-500 to-blue-600 h-2 rounded-full"
                  style={{ width: `${cv.skills}%` }}
                />
              </div>

              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Expérience</span>
                <span className="font-medium">{cv.experience_score}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-green-500 to-green-600 h-2 rounded-full"
                  style={{ width: `${cv.experience_score}%` }}
                />
              </div>

              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Formation</span>
                <span className="font-medium">{cv.education}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-purple-500 to-purple-600 h-2 rounded-full"
                  style={{ width: `${cv.education}%` }}
                />
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center justify-between pt-4 border-t border-gray-100">
              <div className="flex space-x-2">
                <button className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                  <Eye className="w-4 h-4" />
                </button>
                <button className="p-2 text-gray-400 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors">
                  <Download className="w-4 h-4" />
                </button>
                <button className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
              <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                Voir détails
              </button>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Empty State */}
      {filteredCVs.length === 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl p-12 shadow-soft text-center"
        >
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <FileText className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Aucun CV trouvé
          </h3>
          <p className="text-gray-600 mb-6">
            {searchTerm || filterLevel !== 'all' 
              ? 'Aucun CV ne correspond à vos critères de recherche'
              : 'Aucun CV n\'a encore été traité'
            }
          </p>
          <button className="btn-primary text-white px-6 py-2 rounded-lg font-medium">
            <Plus className="w-4 h-4 mr-2" />
            Ajouter un CV
          </button>
        </motion.div>
      )}
    </div>
  );
};

export default ProcessedCVs;

