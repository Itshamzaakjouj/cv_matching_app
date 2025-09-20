import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Settings, Save, RotateCcw, Palette, Globe, Download, Mail } from 'lucide-react';
import { useData } from '../contexts/DataContext';

const Configuration: React.FC = () => {
  const { loading } = useData();
  const [config, setConfig] = useState({
    technical_weight: 0.50,
    experience_weight: 0.30,
    education_weight: 0.20,
    language: 'Français',
    theme: 'Clair',
    auto_save: true,
    export_format: 'PDF',
    include_charts: true,
    email_reports: false
  });

  const [isSaving, setIsSaving] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  useEffect(() => {
    // Load configuration from API
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      // Simulate API call
      // const response = await fetch('/api/config');
      // const data = await response.json();
      // setConfig(data);
    } catch (error) {
      console.error('Error loading config:', error);
    }
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
    } catch (error) {
      console.error('Error saving config:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleReset = () => {
    setConfig({
      technical_weight: 0.50,
      experience_weight: 0.30,
      education_weight: 0.20,
      language: 'Français',
      theme: 'Clair',
      auto_save: true,
      export_format: 'PDF',
      include_charts: true,
      email_reports: false
    });
  };

  const totalWeight = config.technical_weight + config.experience_weight + config.education_weight;
  const isWeightValid = Math.abs(totalWeight - 1.0) < 0.01;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-gray-600 to-gray-800 rounded-2xl p-8 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">Configuration</h1>
            <p className="text-gray-200 text-lg">
              Personnalisez les paramètres de l'application
            </p>
          </div>
          <div className="hidden md:block">
            <div className="w-32 h-32 bg-white/10 rounded-full flex items-center justify-center">
              <Settings className="w-16 h-16 text-white" />
            </div>
          </div>
        </div>
      </div>

      {/* Success Message */}
      {showSuccess && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-green-50 border border-green-200 rounded-lg p-4"
        >
          <div className="flex items-center">
            <div className="w-5 h-5 bg-green-500 rounded-full flex items-center justify-center mr-3">
              <span className="text-white text-xs">✓</span>
            </div>
            <p className="text-green-800 font-medium">Configuration sauvegardée avec succès !</p>
          </div>
        </motion.div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Configuration */}
        <div className="lg:col-span-2 space-y-6">
          {/* Weights Configuration */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl p-6 shadow-soft"
          >
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Poids des Critères</h2>
            
            <div className="space-y-6">
              {/* Technical Skills */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <label className="text-sm font-medium text-gray-700">Compétences Techniques</label>
                  <span className="text-sm text-gray-500">{Math.round(config.technical_weight * 100)}%</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={config.technical_weight}
                  onChange={(e) => setConfig({...config, technical_weight: parseFloat(e.target.value)})}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                />
              </div>

              {/* Experience */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <label className="text-sm font-medium text-gray-700">Expérience Professionnelle</label>
                  <span className="text-sm text-gray-500">{Math.round(config.experience_weight * 100)}%</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={config.experience_weight}
                  onChange={(e) => setConfig({...config, experience_weight: parseFloat(e.target.value)})}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                />
              </div>

              {/* Education */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <label className="text-sm font-medium text-gray-700">Formation & Éducation</label>
                  <span className="text-sm text-gray-500">{Math.round(config.education_weight * 100)}%</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={config.education_weight}
                  onChange={(e) => setConfig({...config, education_weight: parseFloat(e.target.value)})}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                />
              </div>
            </div>

            {/* Weight Validation */}
            <div className={`mt-4 p-3 rounded-lg ${
              isWeightValid ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
            }`}>
              <p className={`text-sm ${
                isWeightValid ? 'text-green-800' : 'text-red-800'
              }`}>
                {isWeightValid 
                  ? `✓ Total des poids : ${Math.round(totalWeight * 100)}% (Valide)`
                  : `⚠ Total des poids : ${Math.round(totalWeight * 100)}% (Doit être 100%)`
                }
              </p>
            </div>
          </motion.div>

          {/* General Settings */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white rounded-2xl p-6 shadow-soft"
          >
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Paramètres Généraux</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Language */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Globe className="w-4 h-4 inline mr-2" />
                  Langue
                </label>
                <select
                  value={config.language}
                  onChange={(e) => setConfig({...config, language: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="Français">Français</option>
                  <option value="Anglais">English</option>
                </select>
              </div>

              {/* Theme */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Palette className="w-4 h-4 inline mr-2" />
                  Thème
                </label>
                <select
                  value={config.theme}
                  onChange={(e) => setConfig({...config, theme: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="Clair">Clair</option>
                  <option value="Sombre">Sombre</option>
                  <option value="Auto">Auto</option>
                </select>
              </div>

              {/* Export Format */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Download className="w-4 h-4 inline mr-2" />
                  Format d'export
                </label>
                <select
                  value={config.export_format}
                  onChange={(e) => setConfig({...config, export_format: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="PDF">PDF</option>
                  <option value="Excel">Excel</option>
                  <option value="Word">Word</option>
                </select>
              </div>

              {/* Auto Save */}
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-gray-700">
                  Sauvegarde automatique
                </label>
                <button
                  onClick={() => setConfig({...config, auto_save: !config.auto_save})}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    config.auto_save ? 'bg-blue-600' : 'bg-gray-200'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      config.auto_save ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>
            </div>
          </motion.div>

          {/* Advanced Settings */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-2xl p-6 shadow-soft"
          >
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Paramètres Avancés</h2>
            
            <div className="space-y-4">
              {/* Include Charts */}
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700">
                    Inclure les graphiques dans les rapports
                  </label>
                  <p className="text-xs text-gray-500">Ajoute des graphiques visuels aux exports</p>
                </div>
                <button
                  onClick={() => setConfig({...config, include_charts: !config.include_charts})}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    config.include_charts ? 'bg-blue-600' : 'bg-gray-200'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      config.include_charts ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>

              {/* Email Reports */}
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700">
                    <Mail className="w-4 h-4 inline mr-2" />
                    Rapports par email
                  </label>
                  <p className="text-xs text-gray-500">Envoie automatiquement les rapports par email</p>
                </div>
                <button
                  onClick={() => setConfig({...config, email_reports: !config.email_reports})}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    config.email_reports ? 'bg-blue-600' : 'bg-gray-200'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      config.email_reports ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Actions */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-2xl p-6 shadow-soft"
          >
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Actions</h3>
            
            <div className="space-y-3">
              <button
                onClick={handleSave}
                disabled={!isWeightValid || isSaving}
                className="w-full btn-primary text-white py-3 px-4 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
              >
                {isSaving ? (
                  <div className="loading-dots">
                    <div></div>
                    <div></div>
                    <div></div>
                    <div></div>
                  </div>
                ) : (
                  <>
                    <Save className="w-4 h-4 mr-2" />
                    Sauvegarder
                  </>
                )}
              </button>

              <button
                onClick={handleReset}
                className="w-full flex items-center justify-center py-3 px-4 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
              >
                <RotateCcw className="w-4 h-4 mr-2" />
                Réinitialiser
              </button>
            </div>
          </motion.div>

          {/* Current Settings Summary */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white rounded-2xl p-6 shadow-soft"
          >
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Résumé</h3>
            
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Langue:</span>
                <span className="font-medium">{config.language}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Thème:</span>
                <span className="font-medium">{config.theme}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Export:</span>
                <span className="font-medium">{config.export_format}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Auto-save:</span>
                <span className="font-medium">{config.auto_save ? 'Activé' : 'Désactivé'}</span>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Configuration;

