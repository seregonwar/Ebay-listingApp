const config = {
    // Porta del server
    port: process.env.PORT || 3000, // Usa la porta 3000 se non impostata da variabile di ambiente
  
    // Configurazione dell'API eBay (senza autenticazione)
    ebay: {
      appId: process.env.EBAY_APP_ID || 'your_ebay_app_id', // Sostituisci con il tuo eBay App ID
   },
  
   
  };
  
  module.exports = config;
