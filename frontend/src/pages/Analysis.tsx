import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Upload, 
  FileText, 
  Play, 
  CheckCircle, 
  BarChart3,
  Users,
  Award,
  Clock
} from 'lucide-react';
import { useData } from '../contexts/DataContext';

const Analysis: React.FC = () => {
  const { cvs, analyzeCVs, loading } = useData();
  const [currentStep, setCurrentStep] = useState(1);
  const [jobDescription, setJobDescription] = useState('');
  const [selectedCVs, setSelectedCVs] = useState<string[]>([]);
  const [analysisResults, setAnalysisResults] = useState<any>(null);

  const steps = [
    { id: 1, title: 'Description du poste', icon: FileText },
    { id: 2, title: 'Sélection des CVs', icon: Users },
    { id: 3, title: 'Lancement de l\'analyse', icon: Play },
    { id: 4, title: 'Résultats', icon: BarChart3 }
  ];

  const handleAnalyze = async () => {
    if (jobDescription && selectedCVs.length > 0) {
      try {
        const results = await analyzeCVs(jobDescription, selectedCVs);
        setAnalysisResults(results);
        setCurrentStep(4);
      } catch (error) {
        console.error('Error analyzing CVs:', error);
      }
    }
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Description du poste à pourvoir
              </h3>
              <p className="text-sm text-gray-600 mb-4">
                Décrivez le poste pour lequel vous souhaitez analyser les CVs
              </p>
            </div>
            
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Ex: Nous recherchons un Data Scientist senior avec 5+ ans d'expérience en machine learning, Python, et analyse de données. Le candidat devra travailler sur des projets d'IA et de deep learning..."
              className="w-full h-40 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            />
            
            <div className="flex justify-end">
              <button
                onClick={() => setCurrentStep(2)}
                disabled={!jobDescription.trim()}
                className="btn-primary text-white px-6 py-2 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Suivant
              </button>
            </div>
          </motion.div>
        );

      case 2:
        return (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Sélectionner les CVs à analyser
              </h3>
              <p className="text-sm text-gray-600 mb-4">
                Choisissez les CVs que vous souhaitez comparer pour ce poste
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {cvs.map((cv) => (
                <motion.div
                  key={cv.name}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => {
                    if (selectedCVs.includes(cv.name)) {
                      setSelectedCVs(selectedCVs.filter(name => name !== cv.name));
                    } else {
                      setSelectedCVs([...selectedCVs, cv.name]);
                    }
                  }}
                  className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                    selectedCVs.includes(cv.name)
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <div className={`w-4 h-4 rounded-full border-2 ${
                      selectedCVs.includes(cv.name)
                        ? 'border-blue-500 bg-blue-500'
                        : 'border-gray-300'
                    }`}>
                      {selectedCVs.includes(cv.name) && (
                        <CheckCircle className="w-4 h-4 text-white" />
                      )}
                    </div>
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900">{cv.person}</h4>
                      <p className="text-sm text-gray-600">{cv.position}</p>
                      <p className="text-xs text-gray-500">{cv.level} • {cv.experience}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-lg font-bold text-gray-900">{cv.score}%</p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
            
            <div className="flex justify-between">
              <button
                onClick={() => setCurrentStep(1)}
                className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
              >
                Précédent
              </button>
              <button
                onClick={() => setCurrentStep(3)}
                disabled={selectedCVs.length === 0}
                className="btn-primary text-white px-6 py-2 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Suivant
              </button>
            </div>
          </motion.div>
        );

      case 3:
        return (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <Play className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Prêt à lancer l'analyse
              </h3>
              <p className="text-sm text-gray-600 mb-6">
                L'analyse va comparer {selectedCVs.length} CV(s) pour le poste décrit
              </p>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="font-medium text-gray-900 mb-2">Résumé de l'analyse :</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Poste : {jobDescription.substring(0, 50)}...</li>
                <li>• CVs sélectionnés : {selectedCVs.length}</li>
                <li>• Critères d'évaluation : Compétences, Expérience, Formation</li>
              </ul>
            </div>
            
            <div className="flex justify-between">
              <button
                onClick={() => setCurrentStep(2)}
                className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
              >
                Précédent
              </button>
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="btn-primary text-white px-6 py-2 rounded-lg font-medium disabled:opacity-50"
              >
                {loading ? 'Analyse en cours...' : 'Lancer l\'analyse'}
              </button>
            </div>
          </motion.div>
        );

      case 4:
        return (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Analyse terminée !
              </h3>
              <p className="text-sm text-gray-600">
                Voici les résultats de votre analyse
              </p>
            </div>
            
            {analysisResults && (
              <div className="space-y-6">
                {/* Top Results */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {analysisResults.results.slice(0, 3).map((result: any, index: number) => (
                    <motion.div
                      key={result.name}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="bg-white rounded-lg p-4 shadow-soft border border-gray-200"
                    >
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium text-gray-900">{result.person}</h4>
                        <span className="text-sm text-gray-500">#{index + 1}</span>
                      </div>
                      <p className="text-sm text-gray-600 mb-3">{result.position}</p>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-gray-900 mb-1">
                          {result.score}%
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-1000"
                            style={{ width: `${result.score}%` }}
                          />
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
                
                {/* Detailed Results */}
                <div className="bg-white rounded-lg p-6 shadow-soft">
                  <h4 className="font-semibold text-gray-900 mb-4">Détails des résultats</h4>
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead>
                        <tr className="border-b border-gray-200">
                          <th className="text-left py-2 text-sm font-medium text-gray-600">Candidat</th>
                          <th className="text-left py-2 text-sm font-medium text-gray-600">Score Global</th>
                          <th className="text-left py-2 text-sm font-medium text-gray-600">Compétences</th>
                          <th className="text-left py-2 text-sm font-medium text-gray-600">Expérience</th>
                          <th className="text-left py-2 text-sm font-medium text-gray-600">Formation</th>
                        </tr>
                      </thead>
                      <tbody>
                        {analysisResults.results.map((result: any) => (
                          <tr key={result.name} className="border-b border-gray-100">
                            <td className="py-3">
                              <div>
                                <p className="font-medium text-gray-900">{result.person}</p>
                                <p className="text-sm text-gray-500">{result.position}</p>
                              </div>
                            </td>
                            <td className="py-3">
                              <span className="text-lg font-bold text-gray-900">{result.score}%</span>
                            </td>
                            <td className="py-3">
                              <span className="text-sm text-gray-600">{result.technical_score}%</span>
                            </td>
                            <td className="py-3">
                              <span className="text-sm text-gray-600">{result.experience_score}%</span>
                            </td>
                            <td className="py3">
                              <span className="text-sm text-gray-600">{result.education_score}%</span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            )}
            
            <div className="flex justify-center">
              <button
                onClick={() => {
                  setCurrentStep(1);
                  setJobDescription('');
                  setSelectedCVs([]);
                  setAnalysisResults(null);
                }}
                className="btn-primary text-white px-6 py-2 rounded-lg font-medium"
              >
                Nouvelle analyse
              </button>
            </div>
          </motion.div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Progress Steps */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          {steps.map((step, index) => {
            const Icon = step.icon;
            const isActive = currentStep === step.id;
            const isCompleted = currentStep > step.id;
            
            return (
              <div key={step.id} className="flex items-center">
                <div className="flex flex-col items-center">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition-all ${
                    isCompleted
                      ? 'bg-green-500 border-green-500 text-white'
                      : isActive
                      ? 'bg-blue-500 border-blue-500 text-white'
                      : 'bg-white border-gray-300 text-gray-400'
                  }`}>
                    {isCompleted ? (
                      <CheckCircle className="w-5 h-5" />
                    ) : (
                      <Icon className="w-5 h-5" />
                    )}
                  </div>
                  <span className={`text-xs font-medium mt-2 ${
                    isActive || isCompleted ? 'text-gray-900' : 'text-gray-400'
                  }`}>
                    {step.title}
                  </span>
                </div>
                {index < steps.length - 1 && (
                  <div className={`w-16 h-0.5 mx-4 ${
                    isCompleted ? 'bg-green-500' : 'bg-gray-300'
                  }`} />
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Step Content */}
      <div className="bg-white rounded-2xl p-8 shadow-soft">
        {renderStepContent()}
      </div>
    </div>
  );
};

export default Analysis;

