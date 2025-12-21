import time


def time_exec(funcao):
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = funcao(*args, **kwargs)
        fim = time.time()
        print(f'A função {funcao.__name__} levou {fim - inicio:.2f} segundos para executar')
        return resultado
    return wrapper