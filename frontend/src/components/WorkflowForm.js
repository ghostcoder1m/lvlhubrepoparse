import React, { useState } from 'react';

const WorkflowForm = ({ onSubmit }) => {
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        const newWorkflow = { name, description };
        onSubmit(newWorkflow);
        setName('');
        setDescription('');
    };

    return (
        <form onSubmit={handleSubmit}>
            <h3>Add New Workflow</h3>
            <input
                type="text"
                placeholder="Workflow Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
            />
            <textarea
                placeholder="Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
            />
            <button type="submit">Add Workflow</button>
        </form>
    );
};

export default WorkflowForm;
