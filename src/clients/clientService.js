function addClient(clientList, name, phoneNumber) {
    clientList.push({ name, phoneNumber });
  }
  
  function removeClient(clientList, phoneNumber) {
    return clientList.filter(client => client.phoneNumber !== phoneNumber);
  }
  
  module.exports = { addClient, removeClient };
  