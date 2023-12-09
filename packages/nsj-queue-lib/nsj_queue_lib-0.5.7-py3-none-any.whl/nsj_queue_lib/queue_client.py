import datetime

from nsj_sql_utils_lib.dbadapter3 import DBAdapter3

from nsj_queue_lib.tarefa_dao import TarefaDAO


class QueueClient:
    def __init__(
        self,
        bd_conn,
        queue_table: str,
        queue_subscriber_table: str = None,
    ) -> None:
        self._tarefa_dao = TarefaDAO(
            DBAdapter3(bd_conn), queue_table, queue_subscriber_table
        )

    def _insert_task(
        self,
        origem: str,
        destino: str,
        processo: str,
        chave_externa: str,
        payload: str,
        tenant: int = None,
        grupo_empresarial: str = None,
        data_hora: datetime.datetime = None,
        pub_sub: bool = False,
    ):
        # Criando o objeto para realizar o insert
        task = {
            "origem": origem,
            "destino": destino,
            "processo": processo,
            "chave_externa": chave_externa,
            "payload": payload,
            "pub_sub": pub_sub,
        }

        if tenant is not None:
            task["tenant"] = tenant

        if grupo_empresarial is not None:
            task["grupo_empresarial"] = grupo_empresarial

        if data_hora is not None:
            task["data_hora"] = data_hora
            task["data_hora_inicial"] = data_hora

        # Inserinfo a tarefa
        self._tarefa_dao.insert(task)

    def insert_task(
        self,
        origem: str,
        destino: str,
        processo: str,
        chave_externa: str,
        payload: str,
        tenant: int = None,
        grupo_empresarial: str = None,
        data_hora: datetime.datetime = None,
    ):
        return self._insert_task(
            origem,
            destino,
            processo,
            chave_externa,
            payload,
            tenant,
            grupo_empresarial,
            data_hora,
            False,
        )

    def list_equivalent_task(
        self,
        origem: str,
        destino: str,
        processo: str,
        chave_externa: str,
        payload: str,
        tenant: int = None,
        grupo_empresarial: str = None,
        status: list[str] = ["sucesso", "pendente", "agendada"],
    ):
        """
        Lista as tarefas equivalentes, encontradas na fila, contemplando
        os status recebidos (padrão: sucesso, pendente e agendada).
        """

        # Listando as tarefas pela chave externa, pelo payload e pelo status
        tarefas = self._tarefa_dao.list_equivalent(chave_externa, payload, status)

        # Inserinfo a tarefa
        return [
            t
            for t in tarefas
            if origem == t["origem"]
            and destino == t["destino"]
            and processo == t["processo"]
            and (tenant or -1) == (t["tenant"] or -1)
            and (grupo_empresarial or "") == (t["grupo_empresarial"] or "")
        ]

    def insert_task_pub_sub(
        self,
        origem: str,
        destino: str,
        processo: str,
        chave_externa: str,
        payload: str,
        tenant: int = None,
        grupo_empresarial: str = None,
        data_hora: datetime.datetime = None,
    ):
        return self._insert_task(
            origem,
            destino,
            processo,
            chave_externa,
            payload,
            tenant,
            grupo_empresarial,
            data_hora,
            True,
        )

    def insert_task_webhook(
        self,
        origem: str,
        destino: str,
        processo: str,
        chave_externa: str,
        payload: str,
        tenant: int = None,
        grupo_empresarial: str = None,
        data_hora: datetime.datetime = None,
    ):
        return self._insert_task(
            origem,
            destino,
            processo,
            chave_externa,
            payload,
            tenant,
            grupo_empresarial,
            data_hora,
            True,
        )


# CODIGO DE TESTE MANUAL ABAIXO
# from nsj_queue_lib.settings import (
#     DB_HOST,
#     DB_PORT,
#     DB_BASE,
#     DB_USER,
#     DB_PASS,
# )

# from nsj_sql_utils_lib.dbconection_psycopg2 import DBConnectionPsycopg2

# with DBConnectionPsycopg2(DB_HOST, DB_PORT, DB_BASE, DB_USER, DB_PASS) as dbconn:
#     queue_client = QueueClient(dbconn.conn)
#     queue_client.insert_task(
#         "teste",
#         "teste_destino",
#         "processo_teste",
#         "1234567",
#         "conteúdo da mensagem",
#         1,
#         "grupo",
#     )

#     lista = queue_client.list_equivalent_task(
#         "teste",
#         "teste_destino",
#         "processo_teste",
#         "1234567",
#         "conteúdo da mensagem",
#         1,
#         "grupo",
#     )

#     print(lista)
