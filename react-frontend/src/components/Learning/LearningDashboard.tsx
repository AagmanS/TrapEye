import * as React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';

interface Lesson {
  id: number;
  title: string;
  description: string;
  content: string;
  quiz: QuizQuestion[];
}

interface QuizQuestion {
  question: string;
  options: string[];
  correctAnswer: number;
}

interface LessonProgress {
  completed: boolean;
  quizScore: number;
  completedAt: string | null;
}

interface UserProgress {
  [lessonId: number]: LessonProgress;
}

const LearningDashboard: React.FC = () => {
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [userProgress, setUserProgress] = useState<UserProgress>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // For demo purposes, we'll use a fixed user ID
  const userId = 'user123';

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch lessons
        const lessonsResponse = await axios.get('http://localhost:3001/api/lessons');
        setLessons(lessonsResponse.data);
        
        // Fetch user progress
        const progressResponse = await axios.get(`http://localhost:3001/api/progress/${userId}`);
        setUserProgress(progressResponse.data);
        
        setLoading(false);
      } catch (err) {
        setError('Failed to load learning content. Please try again later.');
        setLoading(false);
        console.error('Error fetching data:', err);
      }
    };

    fetchData();
  }, [userId]);

  const calculateProgress = () => {
    if (lessons.length === 0) return 0;
    // Use Object.keys instead of Object.values to avoid TypeScript issues
    const completedLessons = Object.keys(userProgress)
      .map(key => userProgress[parseInt(key)])
      .filter(progress => progress.completed).length;
    return Math.round((completedLessons / lessons.length) * 100);
  };

  const getBadge = () => {
    const progress = calculateProgress();
    if (progress === 100) return 'Safety Pro';
    if (progress >= 50) return 'Cyber Rookie';
    return 'Beginner';
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <strong className="font-bold">Error! </strong>
        <span className="block sm:inline">{error}</span>
      </div>
    );
  }

  const progress = calculateProgress();
  const badge = getBadge();

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="text-center mb-10">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">Cyber Safety Learning Center</h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Enhance your cybersecurity knowledge with our interactive lessons and quizzes.
        </p>
      </div>

      {/* Progress Section */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <h2 className="text-2xl font-bold text-gray-800">Your Progress</h2>
            <p className="text-gray-600">Keep learning to improve your cyber safety skills</p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm font-medium">
              {badge}
            </div>
            <div className="text-right">
              <p className="text-2xl font-bold text-blue-600">{progress}%</p>
              <p className="text-gray-600">Complete</p>
            </div>
          </div>
        </div>
        <div className="mt-6">
          <div className="w-full bg-gray-200 rounded-full h-4">
            <div 
              className="bg-blue-600 h-4 rounded-full transition-all duration-500 ease-in-out" 
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Lessons Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {lessons.map(lesson => (
          <div key={lesson.id} className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
            <div className="p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-2">{lesson.title}</h3>
              <p className="text-gray-600 mb-4">{lesson.description}</p>
              <div className="flex justify-between items-center">
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                  {userProgress[lesson.id]?.completed ? 'Completed' : 'Not started'}
                </span>
                <button 
                  onClick={() => {
                    // Navigate to lesson detail page
                    window.location.hash = `/learning/lesson/${lesson.id}`;
                  }}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
                >
                  Start Learning
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LearningDashboard;