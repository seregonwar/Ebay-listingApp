const express = require('express');
const { spawn } = require('child_process');
const cors = require('cors'); 

const app = express();
app.use(express.json());
app.use(cors()); // Enable CORS for cross-origin requests

const port = process.env.PORT || 5000;

app.post('/api/upload', (req, res) => {
    const fileData = req.body.fileData; 
    
    // Esegui lo script Python per il parsing
    const pythonProcess = spawn('python', ['backend/app.py', 'parse', fileData]);

    pythonProcess.stdout.on('data', (data) => {
        // Ricevi i dati elaborati da Python in JSON
        const parsedData = JSON.parse(data.toString());
        res.json(parsedData);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Errore Python: ${data}`);
        res.status(500).send('Errore nel parsing del file');
    });
});

app.listen(port, () => console.log(`Server avviato su ${port}`));
