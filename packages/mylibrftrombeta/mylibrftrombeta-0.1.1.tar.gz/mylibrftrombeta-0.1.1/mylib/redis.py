import redis


def get_Key(self, ambiente, perfil):
    """
        Método responsável por realizar uma consulta no redis.

        Arguments:
        ----------
        ambiente: Ambiente de utilização do redis.
        perfil: Chave para consulta.

        Returns:
        -------
        Retorna o valor guardado na chave consultada.
    """
    try:
        conn = self.connection(ambiente)
        return conn.get(perfil)
    except Exception as e:
        print(e)


def connection(ambiente):
    """
        Método responsável por realizar a conexão com o redis.

        Arguments:
        ----------
        ambiente: Ambiente de utilização do redis.

        Returns:
        -------
        Retorna uma conexão aberta com o redis para consulta ou gravação de dados.
    """
    if ambiente == 'develop':
        conn = redis.Redis(host="rdi-dev-auttkn.develop.internal.tag")
    elif ambiente == 'staging':
        conn = redis.Redis(host="rdi-stg-auttkn.staging.internal.tag")
    else:
        conn = redis.Redis(host="rdi-prd-auttkn.master.internal.tag")
    return conn
