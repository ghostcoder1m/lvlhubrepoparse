import React, { useState } from 'react';

const EditCampaignForm = ({ campaign, onSubmit }) => {
    const [name, setName] = useState(campaign.name);
    const [description, setDescription] = useState(campaign.description);
    const [error, setError] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!name || !description) {
            setError('Please fill in all fields.');
            return;
        }
        onSubmit({ ...campaign, name, description });
        setError('');
    };

    return (
        <form onSubmit={handleSubmit}>
            <h3>Edit Campaign</h3>
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
            <button type="submit">Update Campaign</button>
            {error && <p>{error}</p>}
        </form>
    );
};

export default EditCampaignForm;
