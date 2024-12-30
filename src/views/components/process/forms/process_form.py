"""Módulo do formulário de processo (deprecated)."""
from src.utils.deprecation import deprecated

@deprecated(
    "Este módulo será descontinuado em versões futuras. "
    "Use os novos formulários modulares em src.views.components.process.forms"
)
class ProcessForm:
    """Formulário de processo (deprecated)."""
    
    def __init__(self, container: Optional[DependencyContainer] = None):
        """Inicializa o orquestrador."""
        self.container = container or DependencyContainer()
        self.controller = self.container.resolve(ProcessController)
        
        # Inicializa os formulários com o mesmo container
        self.forms = {
            "identification": IdentificationForm(container=self.container),
            "details": ProcessDetailsForm(container=self.container),
            "rules": BusinessRulesForm(container=self.container),
            "goals": AutomationGoalsForm(container=self.container)
        }
        self._current_step = 0
        self._data: Dict[str, Any] = {}
        
    @property
    def current_form(self):
        """Retorna o formulário atual."""
        return list(self.forms.values())[self._current_step]
    
    def next_step(self) -> bool:
        """Avança para o próximo passo se validação ok."""
        if self.current_form.validate():
            self._data.update(self.current_form.data)
            if self._current_step < len(self.forms) - 1:
                self._current_step += 1
                return True
        return False
    
    def previous_step(self) -> bool:
        """Retorna ao passo anterior."""
        if self._current_step > 0:
            self._current_step -= 1
            return True
        return False
    
    def validate_all(self) -> bool:
        """Valida todos os formulários."""
        return all(form.validate() for form in self.forms.values())
    
    def save(self) -> bool:
        """Salva os dados de todos os formulários."""
        try:
            # Atualiza dados do formulário atual
            self._data.update(self.current_form.data)
            
            # Tenta salvar
            if self.controller.create_process(self._data):
                st.success("Processo salvo com sucesso!")
                return True
            else:
                st.error("Erro ao salvar processo")
                return False
        except Exception as e:
            st.error(f"Erro ao salvar: {str(e)}")
            return False
    
    def render(self) -> None:
        """Renderiza o formulário atual."""
        steps = ["Identificação", "Detalhes", "Regras", "Objetivos"]
        
        # Progress bar
        progress = st.progress(self._current_step / len(steps))
        st.write(f"Etapa {self._current_step + 1} de {len(steps)}: {steps[self._current_step]}")
        
        # Renderiza formulário atual
        self.current_form.render()
        
        # Botões de navegação
        col1, col2 = st.columns(2)
        with col1:
            if self._current_step > 0:
                if st.button("⬅️ Anterior"):
                    self.previous_step()
                    
        with col2:
            if self._current_step < len(steps) - 1:
                if st.button("Próximo ➡️"):
                    if not self.next_step():
                        st.error("Por favor, preencha todos os campos obrigatórios")
            else:
                if st.button("✅ Finalizar"):
                    if self.validate_all():
                        self.save() 