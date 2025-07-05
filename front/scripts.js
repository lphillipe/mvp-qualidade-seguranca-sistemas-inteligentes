// Espera o DOM carregar para adicionar os listeners
document.addEventListener('DOMContentLoaded', () => {
    
    const patientForm = document.getElementById('patient-form');
    const resultsTable = document.getElementById('myTable').getElementsByTagName('tbody')[0];

    // Função para mostrar notificação "toast"
    const showToast = (message, isError = false) => {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.style.backgroundColor = isError ? '#e74c3c' : '#2ecc71';
        toast.className = "show";
        setTimeout(() => { toast.className = toast.className.replace("show", ""); }, 3000);
    };

    // Função para obter a lista inicial de pacientes
    const getList = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/pacientes');
            const data = await response.json();
            resultsTable.innerHTML = ''; // Limpa a tabela antes de popular
            data.pacientes.forEach(item => insertList(item));
        } catch (error) {
            console.error('Error:', error);
            showToast('Erro ao carregar pacientes.', true);
        }
    };

    // Função para inserir uma linha na tabela
    const insertList = (item) => {
    const table = document.getElementById('myTable').getElementsByTagName('tbody')[0];
    const row = table.insertRow();
    
    // Cria o HTML para a célula de diagnóstico com o novo design
    let diagnosticHTML;
    if (item.outcome === 1) {
        diagnosticHTML = `<span class="badge badge-danger"><i class="fa-solid fa-triangle-exclamation"></i> Alto Risco</span>`;
    } else {
        diagnosticHTML = `<span class="badge badge-success"><i class="fa-solid fa-shield-heart"></i> Baixo Risco</span>`;
    }

    row.innerHTML = `
        <td>${item.name}</td>
        <td>${item.age}</td>
        <td>${item.cp}</td>
        <td>${item.thalach}</td>
        <td>${item.exang}</td>
        <td>${item.oldpeak}</td>
        <td>${item.ca}</td>
        <td>${item.thal}</td>
        <td>${diagnosticHTML}</td>
        <td><i class="fa-solid fa-trash-can delete-btn"></i></td>
    `;
    };

    // Listener para o formulário de adição de paciente
    patientForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const formData = new FormData(patientForm);
        const data = Object.fromEntries(formData.entries()); 
        
        // Renomeia os campos para o que a API espera
        const apiData = {
            name: document.getElementById('newInput').value,
            age: document.getElementById('newAge').value,
            cp: document.getElementById('newCp').value,
            thalach: document.getElementById('newThalach').value,
            exang: document.getElementById('newExang').value,
            oldpeak: document.getElementById('newOldpeak').value,
            ca: document.getElementById('newCa').value,
            thal: document.getElementById('newThal').value
        };

        // Validação simples
        for (let key in apiData) {
            if (!apiData[key]) {
                showToast(`O campo '${key}' não pode ser vazio.`, true);
                return;
            }
        }
        
        try {
            const response = await fetch('http://127.0.0.1:5000/paciente', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(apiData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Erro no servidor.');
            }
            
            const result = await response.json();
            insertList(result);
            showToast(`Paciente '${result.name}' adicionado com sucesso!`);
            patientForm.reset();

        } catch (error) {
            console.error('Error:', error);
            showToast(error.message, true);
        }
    });

    // Delegação de Eventos para o botão de deletar
    resultsTable.addEventListener('click', async (event) => {
        if (event.target.classList.contains('delete-btn')) {
            const row = event.target.closest('tr');
            const itemName = row.cells[0].textContent;
            
            if (confirm(`Tem certeza que deseja remover o paciente '${itemName}'?`)) {
                try {
                    const response = await fetch(`http://127.0.0.1:5000/paciente?name=${encodeURIComponent(itemName)}`, { method: 'DELETE' });
                    if (!response.ok) {
                        throw new Error('Falha ao remover no servidor.');
                    }
                    row.remove();
                    showToast('Paciente removido com sucesso!');
                } catch (error) {
                    console.error('Error:', error);
                    showToast(error.message, true);
                }
            }
        }
    });

    // Carregamento inicial
    getList();
});