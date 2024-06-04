import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone'; 

function App() {
  const [listingData, setListingData] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null); 

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ 
    onDrop: acceptedFiles => {
      const file = acceptedFiles[0];
      const reader = new FileReader();

      reader.onload = (e) => {
        const fileData = e.target.result;
        fetch('/api/upload', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ fileData }),
        })
          .then(res => {
            if (!res.ok) {
              throw new Error(`Errore HTTP: ${res.status}`);
            }
            return res.json();
          })
          .then(data => {
            setListingData(data);
            setErrorMessage(null);
          })
          .catch(error => {
            console.error('Errore nel caricamento:', error);
            setErrorMessage(error.message);
          });
      };

      reader.readAsDataURL(file);
    },
    accept: '.xls,.xlsx' // Aggiungi accettazione per i file XLS/XLSX
  });

  return (
    <div className="App">
      <h1>Crea la tua inserzione eBay</h1>
      <div {...getRootProps()}>
        <input {...getInputProps()} />
        {isDragActive ? (
          <p>Rilascia il file qui...</p>
        ) : (
          <p>Trascina e rilascia un file XLS qui, o clicca per scegliere un file.</p>
        )}
      </div>

      {errorMessage && <div className="error">{errorMessage}</div>}

      {listingData && (
        <div>
          <h2>Anteprima dell'inserzione:</h2>
          <p>Titolo: {listingData.title}</p>
          <p>Descrizione: {listingData.description}</p>
          {/* ... altre informazioni */}
        </div>
      )}

    </div>
  );
}

export default App;
