import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

interface CVData {
  name: string;
  person: string;
  position: string;
  experience: string;
  level: string;
  score: number;
  skills: number;
  experience_score: number;
  education: number;
}

interface DashboardData {
  total_cvs: number;
  average_score: number;
  top_cvs: Array<{
    name: string;
    person: string;
    score: number;
    position: string;
  }>;
  level_distribution: Record<string, number>;
  recent_analyses: Array<{
    id: number;
    job_title: string;
    date: string;
    candidates: number;
    best_score: number;
  }>;
}

interface DataContextType {
  cvs: CVData[];
  dashboardData: DashboardData | null;
  loading: boolean;
  error: string | null;
  fetchCVs: () => Promise<void>;
  fetchDashboardData: () => Promise<void>;
  addCV: (cv: Omit<CVData, 'name'>) => Promise<void>;
  analyzeCVs: (jobDescription: string, selectedCVs: string[]) => Promise<any>;
  getComparisonData: (selectedCVs: string[]) => Promise<any>;
  getRadarChartData: (selectedCVs: string[]) => Promise<any>;
  getBarChartData: (selectedCVs: string[]) => Promise<any>;
}

const DataContext = createContext<DataContextType | undefined>(undefined);

export const useData = () => {
  const context = useContext(DataContext);
  if (context === undefined) {
    throw new Error('useData must be used within a DataProvider');
  }
  return context;
};

const API_BASE_URL = 'http://localhost:8000/api';

export const DataProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [cvs, setCvs] = useState<CVData[]>([]);
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchCVs = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_BASE_URL}/cvs`);
      setCvs(response.data.cvs);
    } catch (err) {
      setError('Erreur lors du chargement des CVs');
      console.error('Error fetching CVs:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_BASE_URL}/dashboard`);
      setDashboardData(response.data);
    } catch (err) {
      setError('Erreur lors du chargement du dashboard');
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  const addCV = async (cvData: Omit<CVData, 'name'>) => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.post(`${API_BASE_URL}/cvs`, cvData);
      await fetchCVs(); // Rafraîchir la liste
    } catch (err) {
      setError('Erreur lors de l\'ajout du CV');
      console.error('Error adding CV:', err);
    } finally {
      setLoading(false);
    }
  };

  const analyzeCVs = async (jobDescription: string, selectedCVs: string[]) => {
    try {
      setLoading(true);
      setError(null);
      const selectedCVData = cvs.filter(cv => selectedCVs.includes(cv.name));
      const response = await axios.post(`${API_BASE_URL}/analysis`, {
        job_description: jobDescription,
        cvs: selectedCVData
      });
      return response.data;
    } catch (err) {
      setError('Erreur lors de l\'analyse des CVs');
      console.error('Error analyzing CVs:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getComparisonData = async (selectedCVs: string[]) => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_BASE_URL}/comparison?selected_cvs=${selectedCVs.join(',')}`);
      return response.data;
    } catch (err) {
      setError('Erreur lors du chargement des données de comparaison');
      console.error('Error fetching comparison data:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getRadarChartData = async (selectedCVs: string[]) => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_BASE_URL}/charts/radar?selected_cvs=${selectedCVs.join(',')}`);
      return response.data;
    } catch (err) {
      setError('Erreur lors du chargement des données du graphique radar');
      console.error('Error fetching radar chart data:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getBarChartData = async (selectedCVs: string[]) => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_BASE_URL}/charts/bar?selected_cvs=${selectedCVs.join(',')}`);
      return response.data;
    } catch (err) {
      setError('Erreur lors du chargement des données du graphique en barres');
      console.error('Error fetching bar chart data:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCVs();
    fetchDashboardData();
  }, []);

  const value = {
    cvs,
    dashboardData,
    loading,
    error,
    fetchCVs,
    fetchDashboardData,
    addCV,
    analyzeCVs,
    getComparisonData,
    getRadarChartData,
    getBarChartData
  };

  return (
    <DataContext.Provider value={value}>
      {children}
    </DataContext.Provider>
  );
};

