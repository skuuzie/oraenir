import React from 'react';

interface UrlInputFormProps {
    url: string;
    customId: string;
    useCustomId: boolean;
    onUrlChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
    onCustomIdChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
    onUseCustomIdToggle: (event: React.ChangeEvent<HTMLInputElement>) => void;
    onSubmit: () => void;
    isLoading: boolean;
}

const UrlInputForm: React.FC<UrlInputFormProps> = ({
    url,
    customId,
    useCustomId,
    onUrlChange,
    onCustomIdChange,
    onUseCustomIdToggle,
    onSubmit,
    isLoading,
}) => {
    const handleFormSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        onSubmit();
    };

    return (
        <form onSubmit={handleFormSubmit} className="url-form">
            <div className="form-group main-url-group">
                <input
                    type="url"
                    id="urlInput"
                    value={url}
                    onChange={onUrlChange}
                    placeholder="Enter URL to shorten"
                    aria-label="URL to shorten"
                    required
                    disabled={isLoading}
                    className="url-input"
                />
                <button
                    type="submit"
                    disabled={isLoading || !url.trim()}
                    className="submit-button"
                >
                    {isLoading ? 'Shortening...' : 'Shorten It'}
                </button>
            </div>

            <div className="form-group custom-id-group">
                <label htmlFor="useCustomIdCheckbox" className="custom-id-label">
                    <input
                        type="checkbox"
                        id="useCustomIdCheckbox"
                        checked={useCustomId}
                        onChange={onUseCustomIdToggle}
                        disabled={isLoading}
                        className="custom-id-checkbox"
                    />
                    Use Custom Alias
                </label>
                {/* Conditionally render the custom ID input */}
                {useCustomId && (
                    <input
                        type="text"
                        id="customIdInput"
                        value={customId}
                        onChange={onCustomIdChange}
                        placeholder="Enter custom alias (e.g., my-link)"
                        aria-label="Custom alias for short URL"
                        disabled={isLoading}
                        className="custom-id-input"
                    />
                )}
            </div>
        </form>
    );
};

export default UrlInputForm;