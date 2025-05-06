export const API_BASE_URL: string = 'redacted'; // replace with localhost or actual production url of be-oraenir

interface ShortenRequestBody {
    url: string;
    custom_id?: string;
}

interface ShortenSuccessResponse {
    shorty: string;
}

interface ApiErrorResponse {
    message: string;
}

/**
 * Call the backend service
 *
 * @param {string} url the url
 * @param {string | null} customId optional alias or id
 * @returns {Promise<ShortenSuccessResponse>}
 * @throws {Error}
 */
export const shortenUrl = async (url: string, customId: string | null = null): Promise<ShortenSuccessResponse> => {
    const endpoint = `${API_BASE_URL}/shorty`;

    const requestBody: ShortenRequestBody = {
        url: url,
    };

    if (customId && customId.trim()) {
        requestBody.custom_id = customId.trim();
    }

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
            let errorMessage = `API Error: ${response.status} ${response.statusText}`;
            try {
                const errorData: ApiErrorResponse = await response.json();

                if (errorData && typeof errorData.message === 'string') {
                    errorMessage = errorData.message;
                }
            } catch (jsonError) {
                console.error('Failed to parse error response JSON:', jsonError);
            }
            throw new Error(errorMessage);
        }

        const data: ShortenSuccessResponse = await response.json();

        if (!data || typeof data.shorty !== 'string') {
             console.error('Invalid success response format from server:', data);
             throw new Error('Invalid response format from server.');
        }

        return data;

    } catch (error) {
        console.error('API call failed:', error);

        if (error instanceof Error) {
            throw error;
        } else {
            throw new Error('An unexpected error occurred during the API call.');
        }
    }
};