// src/components/ResultDisplay.tsx
import React from 'react';

interface ResultDisplayProps {
    shortenedUrl: string | null;
    error: string | null;
    isLoading: boolean;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({ shortenedUrl, error, isLoading }) => {
    if (isLoading) {
        return <div className="result-loading">Processing...</div>;
    }

    if (error) {
        return <div className="result-error">Error: {error}</div>;
    }

    if (shortenedUrl) {
        return (
            <div className="result-success">
                Shortened URL: <a href={shortenedUrl} target="_blank" rel="noopener noreferrer">{shortenedUrl}</a>
            </div>
        );
    }
    
    return null;
};

export default ResultDisplay;