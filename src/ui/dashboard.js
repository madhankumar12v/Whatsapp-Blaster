let clients = [];

function addClient() {
  const name = document.getElementById('clientName').value.trim();
  const number = document.getElementById('clientNumber').value.trim();

  if (!name || !number) {
    alert('Please fill both fields');
    return;
  }

  clients.push({ name, number });
  renderClients();
}

function deleteClient(index) {
  clients.splice(index, 1);
  renderClients();
}

function renderClients() {
  const table = document.querySelector('#clientsTable tbody');
  table.innerHTML = '';

  clients.forEach((client, index) => {
    const row = `
      <tr>
        <td>${client.name}</td>
        <td>${client.number}</td>
        <td><button onclick="deleteClient(${index})">Delete</button></td>
      </tr>
    `;
    table.innerHTML += row;
  });
}

function startBlast() {
  if (clients.length === 0) {
    alert('Add at least one client!');
    return;
  }

  fetch('/start-blast', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ clients })
  })
  .then(res => res.json())
  .then(data => alert(data.message))
  .catch(err => console.error('Error:', err));
}
