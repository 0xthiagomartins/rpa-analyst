"""Inicializador do pacote de componentes."""
# Importações sob demanda para evitar ciclos
__all__ = [
    'ProcessForm',
    'ProcessTimeline',
    'ValidationSummary',
    'NavigationBar'
]

def get_process_form():
    """Retorna a classe ProcessForm."""
    from .process_form import ProcessForm
    return ProcessForm

def get_process_timeline():
    """Retorna a classe ProcessTimeline."""
    from .timeline.process_timeline import ProcessTimeline
    return ProcessTimeline

def get_validation_summary():
    """Retorna a classe ValidationSummary."""
    from .validation.validation_summary import ValidationSummary
    return ValidationSummary

def get_navigation_bar():
    """Retorna a classe NavigationBar."""
    from .navigation.navigation_bar import NavigationBar
    return NavigationBar 