# Herdar da classe base 'Exception' do Python é a forma padrão de criar erros customizados.
class DataFileNotFoundError(Exception):
    """Erro customizado para ser levantado quando um arquivo de dados essencial não é encontrado."""
    pass

class InvalidFilterError(Exception):
    """Erro customizado para ser levantado se uma opção de filtro inválida for passada."""
    pass