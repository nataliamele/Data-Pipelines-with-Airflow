from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    facts_sql = """
    INSERT INTO {} {};
    """
    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql_source="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.sql_source = sql_source
        
    def execute(self, context):
        self.log.info('LoadFactOperator started')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Clear destination table")
        redshift.run("DELETE FROM {}".format(self.table))

        formatted_sql = LoadFactOperator.facts_sql.format(
            self.table,
            self.sql_source
        )
        self.log.info(f"Executing {formatted_sql} ...")
        redshift.run(formatted_sql)
