"""Testes para o formulário de identificação do processo."""
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.views.components.process.forms.identification_form import render_identification_form
from src.views.components.process.config.constants import ERROR_MESSAGES, UI_CONFIG
from src.views.components.process.forms.identification_form import IdentificationForm

@pytest.fixture
def mock_streamlit():
    """Fixture para simular o Streamlit."""
    with patch('src.views.components.process.forms.identification_form.st') as mock_st:
        # Simula o contexto do form
        mock_st.form = MagicMock()
        mock_st.form.return_value.__enter__ = lambda x: None
        mock_st.form.return_value.__exit__ = lambda x, y, z, w: None
        
        # Simula os inputs
        mock_st.text_input = MagicMock()
        mock_st.text_area = MagicMock()
        mock_st.form_submit_button = MagicMock()
        
        # Simula as colunas
        col1, col2 = MagicMock(), MagicMock()
        mock_st.columns = MagicMock(return_value=[col1, col2])
        
        mock_st.error = MagicMock()
        mock_st.success = MagicMock()
        mock_st.spinner = MagicMock()
        mock_st.spinner.return_value.__enter__ = lambda x: None
        mock_st.spinner.return_value.__exit__ = lambda x, y, z, w: None
        mock_st.button = MagicMock()
        mock_st.write = MagicMock()
        mock_st.info = MagicMock()
        
        yield mock_st

@pytest.fixture
def mock_ai_service():
    """Fixture para simular o AIService."""
    with patch('src.views.components.process.forms.identification_form.AIService') as mock_ai:
        mock_instance = MagicMock()
        mock_ai.return_value = mock_instance
        mock_instance.formalize_description.return_value = "Descrição formalizada"
        yield mock_instance

def test_render_identification_form_empty(mock_streamlit):
    """Testa renderização do formulário vazio."""
    mock_streamlit.text_input.side_effect = ["", "", ""]
    mock_streamlit.text_area.return_value = ""
    mock_streamlit.form_submit_button.side_effect = [True, False]  # Salvar clicked, Formalizar not clicked
    
    result = render_identification_form()
    
    # Deve mostrar erro de campos obrigatórios
    mock_streamlit.error.assert_called_once_with(ERROR_MESSAGES['REQUIRED_FIELD'])
    assert result is None

def test_render_identification_form_valid_save(mock_streamlit):
    """Testa submissão válida do formulário (salvando)."""
    # Simula inputs preenchidos
    mock_streamlit.text_input.side_effect = ["Processo Teste", "João Silva"]
    mock_streamlit.text_area.return_value = "Descrição do processo"
    mock_streamlit.form_submit_button.side_effect = [True, False]  # Salvar clicked, Formalizar not clicked
    
    # Simula callback
    on_submit = MagicMock()
    
    result = render_identification_form(on_submit=on_submit)
    
    # Verifica se os dados estão corretos
    assert result is not None
    assert result['process_name'] == "Processo Teste"
    assert result['process_owner'] == "João Silva"
    assert result['process_description'] == "Descrição do processo"
    assert 'created_at' in result
    
    # Verifica se o callback foi chamado
    on_submit.assert_called_once_with(result)

def test_render_identification_form_formalize(mock_streamlit, mock_ai_service):
    """Testa formalização da descrição."""
    # Simula inputs preenchidos
    mock_streamlit.text_input.side_effect = ["Processo Teste", "João Silva"]
    mock_streamlit.text_area.return_value = "Descrição do processo"
    mock_streamlit.form_submit_button.side_effect = [False, True]  # Salvar not clicked, Formalizar clicked
    
    # Simula aceitação da versão formalizada
    mock_streamlit.button.side_effect = [True, False]  # Aceitar clicked, Rejeitar not clicked
    
    # Simula callback
    on_submit = MagicMock()
    
    result = render_identification_form(on_submit=on_submit)
    
    # Verifica se a IA foi chamada
    mock_ai_service.formalize_description.assert_called_once_with("Descrição do processo")
    
    # Verifica se os dados estão corretos
    assert result is not None
    assert result['process_description'] == "Descrição formalizada"
    
    # Verifica se o sucesso foi mostrado
    mock_streamlit.success.assert_called_once()

def test_render_identification_form_formalize_error(mock_streamlit, mock_ai_service):
    """Testa erro na formalização."""
    # Simula inputs preenchidos
    mock_streamlit.text_input.side_effect = ["Processo Teste", "João Silva"]
    mock_streamlit.text_area.return_value = "Descrição do processo"
    mock_streamlit.form_submit_button.side_effect = [False, True]  # Salvar not clicked, Formalizar clicked
    
    # Simula erro na IA
    mock_ai_service.formalize_description.side_effect = Exception("Erro teste")
    
    result = render_identification_form()
    
    # Verifica se o erro foi mostrado
    mock_streamlit.error.assert_called_once()
    assert "Erro ao formalizar descrição" in mock_streamlit.error.call_args[0][0]

def test_render_identification_form_with_initial_data(mock_streamlit):
    """Testa renderização com dados iniciais."""
    initial_data = {
        'process_name': 'Processo Inicial',
        'process_owner': 'Maria Silva',
        'process_description': 'Descrição inicial'
    }
    
    render_identification_form(initial_data=initial_data)
    
    # Verifica se os campos foram preenchidos com os dados iniciais
    mock_streamlit.text_input.assert_any_call(
        "Nome do Processo *",
        value='Processo Inicial',
        help="Nome descritivo do processo a ser automatizado",
        max_chars=UI_CONFIG['MAX_NAME_LENGTH'],
        key="identification_name"
    ) 

def test_identification_form_creation():
    """Testa se o formulário de identificação é criado corretamente."""
    form = IdentificationForm()
    assert form is not None
    assert isinstance(form, IdentificationForm)

def test_identification_form_fields():
    """Testa se os campos do formulário são inicializados corretamente."""
    form = IdentificationForm()
    assert form.process_name == ""
    assert form.process_owner == ""
    assert form.department == ""
    assert form.current_status == ""
    assert form.priority == "Média"
    assert form.complexity == "Média"
    assert form.estimated_time == ""
    assert form.observations == ""

def test_identification_form_validation():
    """Testa a validação dos campos obrigatórios."""
    form = IdentificationForm()
    
    # Campos vazios devem retornar False
    assert not form.validate()
    
    # Preenchendo campos obrigatórios
    form.process_name = "Processo Teste"
    form.process_owner = "João Silva"
    form.department = "TI"
    form.current_status = "Em andamento"
    form.estimated_time = "2 horas"
    
    # Agora deve validar corretamente
    assert form.validate()

def test_identification_form_to_dict():
    """Testa a conversão do formulário para dicionário."""
    form = IdentificationForm()
    form.process_name = "Processo Teste"
    form.process_owner = "João Silva"
    form.department = "TI"
    form.current_status = "Em andamento"
    form.priority = "Alta"
    form.complexity = "Baixa"
    form.estimated_time = "2 horas"
    form.observations = "Teste"
    
    data = form.to_dict()
    
    assert data["process_name"] == "Processo Teste"
    assert data["process_owner"] == "João Silva"
    assert data["department"] == "TI"
    assert data["current_status"] == "Em andamento"
    assert data["priority"] == "Alta"
    assert data["complexity"] == "Baixa"
    assert data["estimated_time"] == "2 horas"
    assert data["observations"] == "Teste" 

def test_identification_form_invalid_priority():
    """Testa se o formulário rejeita prioridades inválidas."""
    form = IdentificationForm()
    
    with pytest.raises(ValueError):
        form.priority = "Prioridade Inválida"
        
def test_identification_form_invalid_complexity():
    """Testa se o formulário rejeita complexidades inválidas."""
    form = IdentificationForm()
    
    with pytest.raises(ValueError):
        form.complexity = "Complexidade Inválida"

def test_identification_form_from_dict():
    """Testa a criação do formulário a partir de um dicionário."""
    data = {
        "process_name": "Processo Teste",
        "process_owner": "João Silva",
        "department": "TI",
        "current_status": "Em andamento",
        "priority": "Alta",
        "complexity": "Baixa",
        "estimated_time": "2 horas",
        "observations": "Teste"
    }
    
    form = IdentificationForm.from_dict(data)
    
    assert form.process_name == data["process_name"]
    assert form.process_owner == data["process_owner"]
    assert form.department == data["department"]
    assert form.current_status == data["current_status"]
    assert form.priority == data["priority"]
    assert form.complexity == data["complexity"]
    assert form.estimated_time == data["estimated_time"]
    assert form.observations == data["observations"]

def test_identification_form_clear():
    """Testa se o método clear limpa todos os campos."""
    form = IdentificationForm()
    form.process_name = "Processo Teste"
    form.process_owner = "João Silva"
    form.department = "TI"
    form.current_status = "Em andamento"
    form.priority = "Alta"
    form.complexity = "Baixa"
    form.estimated_time = "2 horas"
    form.observations = "Teste"
    
    form.clear()
    
    assert form.process_name == ""
    assert form.process_owner == ""
    assert form.department == ""
    assert form.current_status == ""
    assert form.priority == "Média"  # Valor padrão
    assert form.complexity == "Média"  # Valor padrão
    assert form.estimated_time == ""
    assert form.observations == ""

def test_identification_form_partial_validation():
    """Testa validação com apenas alguns campos preenchidos."""
    form = IdentificationForm()
    
    # Preenchendo apenas alguns campos obrigatórios
    form.process_name = "Processo Teste"
    form.process_owner = "João Silva"
    
    # Não deve validar com campos obrigatórios faltando
    assert not form.validate()
    
    # Preenchendo mais um campo obrigatório
    form.department = "TI"
    
    # Ainda não deve validar
    assert not form.validate() 