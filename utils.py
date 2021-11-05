from dispositivo.models import EnderecoMac, EnderecoIp

# Aqui é tudo gambiarra, eu mesmo criei essa mrd :V


def VerificarIp(ip_valor):
    """Verifica se possui um ip igual no banco de dados"""
    if ip_valor and len(ip_valor) >= 1:
        novo_ip = EnderecoIp.objects.filter(ip_address=ip_valor)
        if novo_ip.count() >=1:
            raise IndexError('Valor já existe no db')
        else:
            return ip_valor
    else:
        return None


def VerificarMac(mac_valor):
    """Verifica se há um mac igual no banco de dados"""
    if mac_valor:
        novo_mac_pesquisa = EnderecoMac.objects.filter(mac_address=mac_valor)
        if novo_mac_pesquisa.count() >=1:
            raise IndexError('Valor já existe no db')
        else:
            return mac_valor
    else:
        return None
    

