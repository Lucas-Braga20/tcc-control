from django import template


register = template.Library()


@register.filter(name='file_name_from_path')
def file_name_from_path(value):
    """
    Recebe um caminho de arquivo e retorna apenas o nome do arquivo.
    Exemplo de uso no template: {{ caminho_do_arquivo|file_name_from_path }}
    """
    try:
        return value.split('/')[-1]
    except:
        return ''


@register.filter(name='file_icon')
def file_icon(value):
    """
    Recebe um nome de arquivo e retorna o ícone correspondente à extensão do arquivo.
    Exemplo de uso no template: {{ nome_do_arquivo|file_icon }}
    """
    try:
        extension = value.split('.')[-1].lower()

        icon_mapping = {
            'pdf': 'far fa-file-pdf',
            'txt': 'far fa-file-alt',
            'jpg': 'far fa-file-image',
            'png': 'far fa-file-image',
            'doc': 'far fa-file-word',
            'docx': 'far fa-file-word',
        }

        return icon_mapping.get(extension, 'far fa-file')
    except:
        return 'far fa-file'
