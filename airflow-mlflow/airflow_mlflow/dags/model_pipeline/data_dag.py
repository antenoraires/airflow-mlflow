import datetime as dt
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
# Say this is Task1
def greet():
    '''
    A python function to write a text file
    '''
    print('Writing in file')
    with open('/Development/airflow_tutorial/greet.txt', 'a+', encoding='utf8') as f:
        now = dt.datetime.now()
        t = now.strftime("%Y-%m-%d %H:%M")
        f.write(str(t) + '\n')
    return 'Greeted'
# Say this is task2
def respond():
    '''
    A python function to return a simple greetingthon function to return a simple greeting
    '''
    return 'Greet Responded Again'
# Declaring DAG default settings
default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2018, 9, 24, 10, 00, 00),
    'concurrency': 1,
    'retries': 0
}
# Building the DAG, 'my_simple_dag' is the dag id, which will be
# visible in the airflow ui
with DAG('my_simple_dag',
         catchup=False,
         default_args=default_args,
         schedule_interval='*/10 * * * *',
         # schedule_interval=None,
         ) as dag:
    opr_hello = BashOperator(task_id='say_Hi',
                             bash_command='echo "Hi!!"')
    opr_greet = PythonOperator(task_id='greet',
                               python_callable=greet)
    opr_sleep = BashOperator(task_id='sleep_me',
                             bash_command='sleep 5')
    opr_respond = PythonOperator(task_id='respond',
                                 python_callable=respond)
    # Setting the task flow dependencies
    opr_hello >> opr_greet >> opr_sleep >> opr_respond