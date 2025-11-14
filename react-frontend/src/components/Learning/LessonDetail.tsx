import * as React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';

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

const LessonDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [userProgress, setUserProgress] = useState<LessonProgress | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedAnswers, setSelectedAnswers] = useState<{[key: number]: number}>({});
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [showCompletionMessage, setShowCompletionMessage] = useState(false);
  
  // For demo purposes, we'll use a fixed user ID
  const userId = 'user123';

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch lesson
        const lessonResponse = await axios.get(`http://localhost:3001/api/lessons`);
        const allLessons = lessonResponse.data;
        const foundLesson = allLessons.find((l: Lesson) => l.id === parseInt(id || '0'));
        
        if (!foundLesson) {
          setError('Lesson not found');
          setLoading(false);
          return;
        }
        
        setLesson(foundLesson);
        
        // Fetch user progress
        const progressResponse = await axios.get(`http://localhost:3001/api/progress/${userId}`);
        const progress = progressResponse.data[parseInt(id || '0')] || { completed: false, quizScore: 0, completedAt: null };
        setUserProgress(progress);
        
        setLoading(false);
      } catch (err) {
        setError('Failed to load lesson. Please try again later.');
        setLoading(false);
        console.error('Error fetching data:', err);
      }
    };

    if (id) {
      fetchData();
    }
  }, [id]);

  const handleAnswerSelect = (questionIndex: number, optionIndex: number) => {
    setSelectedAnswers({
      ...selectedAnswers,
      [questionIndex]: optionIndex
    });
  };

  const calculateScore = () => {
    if (!lesson) return 0;
    
    let correctAnswers = 0;
    lesson.quiz.forEach((question, index) => {
      if (selectedAnswers[index] === question.correctAnswer) {
        correctAnswers++;
      }
    });
    
    return Math.round((correctAnswers / lesson.quiz.length) * 100);
  };

  const handleSubmitQuiz = async () => {
    if (!lesson) return;
    
    const score = calculateScore();
    setQuizSubmitted(true);
    
    // If score is 70% or higher, mark as completed
    const completed = score >= 70;
    
    if (completed) {
      setShowCompletionMessage(true);
    }
    
    try {
      // Update progress
      await axios.post('http://localhost:3001/api/progress', {
        userId,
        lessonId: lesson.id,
        completed,
        quizScore: score
      });
      
      // Update local state
      setUserProgress({
        completed,
        quizScore: score,
        completedAt: completed ? new Date().toISOString() : null
      });
    } catch (err) {
      console.error('Error updating progress:', err);
    }
  };

  const handleMarkAsComplete = async () => {
    if (!lesson) return;
    
    setShowCompletionMessage(true);
    
    try {
      // Update progress
      await axios.post('http://localhost:3001/api/progress', {
        userId,
        lessonId: lesson.id,
        completed: true,
        quizScore: userProgress?.quizScore || 0
      });
      
      // Update local state
      setUserProgress({
        completed: true,
        quizScore: userProgress?.quizScore || 0,
        completedAt: new Date().toISOString()
      });
    } catch (err) {
      console.error('Error updating progress:', err);
    }
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
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <strong className="font-bold">Error! </strong>
          <span className="block sm:inline">{error}</span>
        </div>
      </div>
    );
  }

  if (!lesson) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded relative" role="alert">
          <strong className="font-bold">Lesson not found! </strong>
          <span className="block sm:inline">The requested lesson could not be found.</span>
        </div>
      </div>
    );
  }

  const allAnswered = lesson.quiz.length > 0 && 
    Object.keys(selectedAnswers).length === lesson.quiz.length;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {showCompletionMessage && (
        <div className="fixed top-4 right-4 bg-green-500 text-white px-6 py-4 rounded-lg shadow-lg z-50 animate-bounce">
          <div className="flex items-center">
            <span className="text-2xl mr-2">🎉</span>
            <span className="font-bold">Lesson Completed!</span>
          </div>
        </div>
      )}
      
      <div className="mb-6">
        <button 
          onClick={() => navigate('/learning')}
          className="flex items-center text-blue-600 hover:text-blue-800 transition-colors duration-200"
        >
          <span className="mr-2">←</span> Back to Learning Center
        </button>
      </div>
      
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="p-6">
          <div className="flex justify-between items-start mb-4">
            <h1 className="text-3xl font-bold text-gray-800">{lesson.title}</h1>
            {userProgress?.completed && (
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                Completed
              </span>
            )}
          </div>
          
          <p className="text-gray-600 mb-6">{lesson.description}</p>
          
          <div className="prose max-w-none mb-8">
            <p className="text-gray-700 whitespace-pre-line">{lesson.content}</p>
          </div>
          
          {lesson.quiz.length > 0 && (
            <div className="border-t border-gray-200 pt-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Quick Quiz</h2>
              
              {quizSubmitted ? (
                <div className="bg-blue-50 rounded-lg p-6 mb-6">
                  <h3 className="text-xl font-bold text-gray-800 mb-2">Quiz Results</h3>
                  <p className="text-gray-700 mb-4">
                    Your score: <span className="font-bold text-blue-600">{calculateScore()}%</span>
                  </p>
                  {calculateScore() >= 70 ? (
                    <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative mb-4">
                      <strong className="font-bold">Congratulations! </strong>
                      <span className="block sm:inline">You passed the quiz. You can now mark this lesson as complete.</span>
                    </div>
                  ) : (
                    <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded relative mb-4">
                      <strong className="font-bold">Keep trying! </strong>
                      <span className="block sm:inline">You need to score at least 70% to complete this lesson.</span>
                    </div>
                  )}
                  <button 
                    onClick={() => {
                      setQuizSubmitted(false);
                      setSelectedAnswers({});
                    }}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
                  >
                    Retake Quiz
                  </button>
                </div>
              ) : (
                <div className="space-y-6">
                  {lesson.quiz.map((question, questionIndex) => (
                    <div key={questionIndex} className="bg-gray-50 rounded-lg p-4">
                      <h3 className="font-bold text-gray-800 mb-3">
                        {questionIndex + 1}. {question.question}
                      </h3>
                      <div className="space-y-2">
                        {question.options.map((option, optionIndex) => (
                          <div key={optionIndex} className="flex items-center">
                            <input
                              type="radio"
                              id={`question-${questionIndex}-option-${optionIndex}`}
                              name={`question-${questionIndex}`}
                              checked={selectedAnswers[questionIndex] === optionIndex}
                              onChange={() => handleAnswerSelect(questionIndex, optionIndex)}
                              className="h-4 w-4 text-blue-600 focus:ring-blue-500"
                            />
                            <label 
                              htmlFor={`question-${questionIndex}-option-${optionIndex}`}
                              className="ml-3 block text-gray-700"
                            >
                              {option}
                            </label>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                  
                  <button
                    onClick={handleSubmitQuiz}
                    disabled={!allAnswered}
                    className={`px-6 py-3 rounded-lg font-medium transition-colors duration-200 ${
                      allAnswered 
                        ? 'bg-blue-600 text-white hover:bg-blue-700' 
                        : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    }`}
                  >
                    Submit Quiz
                  </button>
                </div>
              )}
            </div>
          )}
          
          {userProgress?.completed ? (
            <div className="mt-6 p-4 bg-green-100 rounded-lg">
              <p className="text-green-800 font-medium">
                🎉 Congratulations! You've completed this lesson.
              </p>
              <p className="text-green-700">
                Quiz score: {userProgress.quizScore}%
              </p>
            </div>
          ) : (
            <div className="mt-6 flex flex-col sm:flex-row sm:space-x-4 space-y-4 sm:space-y-0">
              <button
                onClick={handleMarkAsComplete}
                className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors duration-200 flex items-center justify-center"
              >
                <span className="mr-2">✅</span> Mark as Complete
              </button>
              <button
                onClick={() => navigate('/learning')}
                className="px-6 py-3 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors duration-200"
              >
                Continue Learning Later
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LessonDetail;