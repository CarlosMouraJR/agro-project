from django.core.exceptions import ValidationError
from validate_docbr import CPF, CNPJ

def validate_cpf_cnpj(value):
    cpf = CPF()
    cnpj = CNPJ()

    clean_value = ''.join(filter(str.isdigit, value))

    if len(clean_value) == 11 and cpf.validate(clean_value):
        return
    elif len(clean_value) == 14 and cnpj.validate(clean_value):
        return
    else:
        raise ValidationError("Invalid CPF or CNPJ.")
