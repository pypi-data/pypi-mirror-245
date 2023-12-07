from snowflake.core.task import StoredProcedureCall
from snowflake.core.task.dagv1 import DAG, DAGTask
from snowflake.snowpark import Session


def foo1(session: Session) -> str:
    return "abc"

def foo2(session: Session) -> str:
    return "abc"


def foo3(session: Session) -> str:
    return "abc"


def foo4(session: Session) -> str:
    return "abc"


def test__use_func_return_value_kicked_in():
    with DAG("dag1", stage_location="fake_stage", use_func_return_value=True):
        task1 = DAGTask("task1", foo1)

    with DAG("dag2", stage_location="fake_stage"):
        task2 = DAGTask("task2", foo2)

    with DAG("dag3", use_func_return_value=True):
        task3 = DAGTask("task3", StoredProcedureCall(foo3, stage_location="fake_stage"))

    with DAG("dag4"):
        task4 = DAGTask("task4", StoredProcedureCall(foo4, stage_location="fake_stage"))

    lower_task1 = task1._to_low_level_task()
    lower_task2 = task2._to_low_level_task()
    lower_task3 = task3._to_low_level_task()
    lower_task4 = task4._to_low_level_task()
    assert lower_task1.definition.func is not foo1
    assert lower_task2.definition.func is foo2
    assert lower_task3.definition.func is not foo3
    assert lower_task4.definition.func is foo4
