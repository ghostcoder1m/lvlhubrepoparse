import React, { useState } from 'react';

const CampaignForm = ({ onSubmit }) => {
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!name || !description) {
            setError('Please fill in all fields.');
            return;
        }
        onSubmit({ name, description });
        setName('');
        setDescription('');
        setError('');
    };

    return (
        <form onSubmit={handleSubmit}>
            <h3>Create Campaign</h3>
            <div>
                <label>Name:</label>
                <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />
            </div>
            <div>
                <label>Description:</label>
                <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    required
                />
            </div>
            <button type="submit">Create Campaign</button>
            {error && <p>{error}</p>}
        </form>
    );
};

export default CampaignForm;
