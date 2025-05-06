import React, { useState, useCallback } from 'react';
import UrlInputForm from './components/UrlInputForm';
import ResultDisplay from './components/ResultDisplay';
import { shortenUrl, API_BASE_URL } from './services/api';
import './App.css';

function App() {
    const [url, setUrl] = useState<string>('');
    const [customId, setCustomId] = useState<string>('');
    const [useCustomId, setUseCustomId] = useState<boolean>(false);
    const [shortenedUrlResult, setShortenedUrlResult] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const handleUrlChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
        setUrl(event.target.value);
    }, []);

    const handleCustomIdChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
        setCustomId(event.target.value);
    }, []);

    const handleUseCustomIdToggle = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
        setUseCustomId(event.target.checked);
        if (!event.target.checked) {
            setCustomId('');
        }
    }, []);

    const handleSubmit = useCallback(async () => {
        const trimmedUrl = url.trim();
        if (!trimmedUrl) {
            setError('Please enter a URL to shorten.');
            setShortenedUrlResult(null);
            return;
        }

        setIsLoading(true);
        setError(null);
        setShortenedUrlResult(null);

        try {
            const idToSend = useCustomId && customId.trim() ? customId.trim() : null;
            const result = await shortenUrl(trimmedUrl, idToSend);

            setShortenedUrlResult(API_BASE_URL + "/s" + result.shorty);
        } catch (apiError) {
            if (apiError instanceof Error) {
                setError(apiError.message);
            } else {
                setError('An unexpected error occurred.');
            }
        } finally {
            setIsLoading(false);
        }
    }, [url, customId, useCustomId]);

    return (
        <div className="app-container">
            <h1>Shorty URL</h1>
            <UrlInputForm
                url={url}
                customId={customId}
                useCustomId={useCustomId}
                onUrlChange={handleUrlChange}
                onCustomIdChange={handleCustomIdChange}
                onUseCustomIdToggle={handleUseCustomIdToggle}
                onSubmit={handleSubmit}
                isLoading={isLoading}
            />
            <ResultDisplay
                shortenedUrl={shortenedUrlResult}
                error={error}
                isLoading={isLoading}
            />
        </div>
    );
}

export default App;